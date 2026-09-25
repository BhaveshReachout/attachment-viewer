# Copyright 2026 Kalki Infinite (<https://kalkiinfinite.odoo.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
{
    'name': 'Attachment Viewer',
    'version': '19.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Open attachments in an in-browser viewer instead of downloading them',
    'description': """
Attachment Viewer
=================

Every attachment gets a **Preview** action that opens a dedicated page
showing its content, so nobody has to download a file just to find out
what is in it.

What gets rendered
------------------
* **Images** fit to the window on a neutral background.
* **PDF** files render inline, scaled to the page width.
* **Plain-text formats** - .txt, .csv, .log, .json, .xml, .sql, .yaml and
  similar - display in a scrollable pane. Browsers normally force-download
  these instead of showing them, which is where this module helps most.
* **Video and audio** play through the browser's native player.
* **External links** (attachments stored as a URL rather than a file) open
  that link directly, once its scheme has been checked as safe.
* Anything else gets an honest "cannot be previewed" card with a download
  button instead of a broken embed.

Navigating attachments
-----------------------
* A **Preview** button is available from the attachment list and its form.
* Previous / next controls step through the other attachments on the same
  record - by mouse click or with the left/right arrow keys.
* Text previews stop at a configurable size (200 KB by default, via a
  system parameter) so a huge log file cannot freeze the tab.
* File size is displayed in a human-readable unit (KB/MB) rather than as a
  raw byte count.

Security
--------
The viewer page is served under the requesting user's own permissions -
nothing is read with elevated rights. Standard ir.attachment access rules
decide what each user may open, and a visitor who is not logged in is sent
to the login page rather than the file.
""",
    'author': 'Kalki Infinite',
    'maintainer': 'Kalki Infinite',
    'website': 'https://kalkiinfinite.odoo.com',
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'data': [
        'views/preview_templates.xml',
        'views/attachment_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'attachment_viewer/static/src/css/preview.css',
            'attachment_viewer/static/src/js/preview.js',
        ],
    },
    'images': ['static/description/banner.png'],  # add once artwork is supplied
    'installable': True,
    'application': False,
    'auto_install': False,
}
