# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from urllib.parse import urlparse

from odoo import _, api, fields, models
from odoo.tools import human_size

# Mime types a browser can display on its own; anything not matched here
# falls back to a plain "download instead" card.
KIND_BY_MIME_PREFIX = (
    ('image/', 'image'),
    ('video/', 'video'),
    ('audio/', 'audio'),
    ('text/', 'text'),
)
KIND_BY_EXACT_MIMETYPE = {
    'application/pdf': 'pdf',
    'application/json': 'text',
    'application/xml': 'text',
    'application/javascript': 'text',
    'application/x-javascript': 'text',
    'application/x-sh': 'text',
    'application/sql': 'text',
    'application/x-yaml': 'text',
}
# A link is only ever rendered as a clickable href when it uses one of
# these schemes, so a stored "javascript:" (or similar) value can never run.
SAFE_LINK_SCHEMES = ('http', 'https')

# Fallback cap (in KB) for text previews, used when the system parameter
# below is missing or not a usable number. Past this size the pane stops
# being useful and starts loading megabytes of text into the tab.
DEFAULT_TEXT_PREVIEW_LIMIT_KB = 200
TEXT_PREVIEW_LIMIT_PARAM = 'attachment_viewer.text_preview_limit_kb'


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    preview_type = fields.Selection(
        [('image', 'Image'), ('pdf', 'PDF'), ('text', 'Text'),
         ('video', 'Video'), ('audio', 'Audio'), ('link', 'External link'),
         ('none', 'Not previewable')],
        compute='_compute_preview_type',
        help="How the viewer page renders this attachment.")

    @api.depends('mimetype', 'type')
    def _compute_preview_type(self):
        for attachment in self:
            if attachment.type == 'url':
                attachment.preview_type = 'link'
            else:
                attachment.preview_type = self._preview_type_for_mimetype(attachment.mimetype)

    @api.model
    def _preview_type_for_mimetype(self, mimetype):
        mimetype = (mimetype or '').split(';')[0].strip().lower()
        if mimetype in KIND_BY_EXACT_MIMETYPE:
            return KIND_BY_EXACT_MIMETYPE[mimetype]
        for prefix, kind in KIND_BY_MIME_PREFIX:
            if mimetype.startswith(prefix):
                return kind
        return 'none'

    def action_open_preview(self):
        """Open this attachment's viewer page in a new browser tab."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/attachment/viewer/%d' % self.id,
            'target': 'new',
        }

    # -- viewer page helpers -------------------------------------------

    @api.model
    def _get_text_preview_limit(self):
        """Byte cap applied to a text preview.

        Read from the ``attachment_viewer.text_preview_limit_kb`` system
        parameter, so it can be raised or lowered without touching code.
        """
        raw_value = self.env['ir.config_parameter'].sudo().get_param(
            TEXT_PREVIEW_LIMIT_PARAM, DEFAULT_TEXT_PREVIEW_LIMIT_KB)
        try:
            limit_kb = int(raw_value)
        except (TypeError, ValueError):
            limit_kb = DEFAULT_TEXT_PREVIEW_LIMIT_KB
        return max(limit_kb, 1) * 1024

    def _get_preview_text(self):
        """Attachment content decoded as text, cut off at the configured
        limit so a large file cannot be dumped whole into the page."""
        self.ensure_one()
        limit = self._get_text_preview_limit()
        data = self.raw or b''
        truncated = len(data) > limit
        text = data[:limit].decode('utf-8', errors='replace')
        if truncated:
            text += _("\n\n--- truncated, download the file to see the rest ---")
        return text

    def _get_preview_link(self):
        """External URL to expose as a link, or '' when there is none or
        it does not use a scheme that is safe to render as a href."""
        self.ensure_one()
        url = (self.url or '').strip()
        if url and urlparse(url).scheme in SAFE_LINK_SCHEMES:
            return url
        return ''

    def _get_preview_size_label(self):
        """File size in a human-readable form (e.g. '482.30 Kb')."""
        self.ensure_one()
        return human_size(self.file_size) if self.file_size else ''

    def _get_preview_neighbours(self):
        """Other attachments on the same record, for the previous/next
        controls on the viewer page.

        Returns a (previous, next) tuple; either side may come back empty.
        """
        self.ensure_one()
        if not self.res_model or not self.res_id:
            return self.browse(), self.browse()
        siblings = self.search([
            ('res_model', '=', self.res_model),
            ('res_id', '=', self.res_id),
        ], order='id')
        ids = siblings.ids
        if self.id not in ids:
            return self.browse(), self.browse()
        index = ids.index(self.id)
        previous = self.browse(ids[index - 1]) if index else self.browse()
        following = self.browse(ids[index + 1]) if index + 1 < len(ids) else self.browse()
        return previous, following
