# Copyright 2026 Kalki Infinite (<https://kalkiinfinite.odoo.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request


class AttachmentViewerController(http.Controller):

    @http.route('/attachment/viewer/<int:attachment_id>', type='http',
                auth='user', sitemap=False)
    def open_preview(self, attachment_id, **kwargs):
        """Serve the in-browser viewer page for a single attachment.

        Everything here runs as the requesting user: the attachment is
        fetched with a plain browse/read rather than sudo, so
        ir.attachment's own access rules decide whether the request goes
        through, and someone without access gets a 404, never the content.
        """
        # A deleted id has to be caught before read(): on a missing record,
        # read() can come back with an empty result instead of raising,
        # which would let a MissingError escape further down. not_found()
        # only builds the HTTP exception - it must be raised explicitly, or
        # the response comes back as a 400 instead of a 404.
        attachment = request.env['ir.attachment'].browse(attachment_id).exists()
        if not attachment:
            raise request.not_found()
        try:
            attachment.read(['name'])
        except AccessError:
            # A 404, not a 403: a 403 would confirm to an unauthorized
            # visitor that the guessed id refers to a real attachment.
            raise request.not_found()

        previous, following = attachment._get_preview_neighbours()
        kind = attachment.preview_type
        return request.render('attachment_viewer.preview_page', {
            'attachment': attachment,
            'kind': kind,
            'text': attachment._get_preview_text() if kind == 'text' else '',
            'link': attachment._get_preview_link() if kind == 'link' else '',
            'size_label': attachment._get_preview_size_label(),
            'previous': previous,
            'next': following,
        })
