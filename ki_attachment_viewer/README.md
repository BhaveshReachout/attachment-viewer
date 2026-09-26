# Attachment Viewer

**by [BK](https://kalkiinfinite.odoo.com)**

Turns the "Preview" action on every Odoo attachment into an actual preview:
images, PDFs, text files, video, audio and stored links open in a page that
shows them, instead of dropping a file into your downloads folder just so
you can see what it is.

## What it does

- **Renders plain-text formats** - `.csv`, `.log`, `.json`, `.xml`, `.sql`
  and similar files open in a scrollable pane. Browsers otherwise
  force-download these, which is exactly where this module pays off.
- **Shows images and PDFs inline** - images are scaled to fit the window,
  PDFs render at page width, both without leaving Odoo.
- **Plays video and audio** through the browser's own player - no plugin,
  no download.
- **Opens stored links** - an attachment saved as a URL (rather than a
  file) opens that link directly, after its scheme is checked as safe.
- **Falls back honestly** - a file type that cannot be shown gets a plain
  card explaining that, with a download button, instead of a broken embed.
- **Steps through a record's attachments** - previous/next controls, by
  mouse or the left/right arrow keys.
- **Protects the browser tab** - text previews stop at a configurable size
  (200 KB by default) so a large log file cannot freeze the page.
- **Shows a readable file size** (KB/MB) instead of a raw byte count.

## Using it

1. Install the module.
2. Open any attachment - from *Settings > Technical > Attachments*, or
   from a record's own attachment list.
3. Click **Preview**. The file opens in a new tab.

## Configuration

The text-preview size cap can be changed without touching code, through a
system parameter:

| Key | Default | Meaning |
| --- | --- | --- |
| `ki_attachment_viewer.text_preview_limit_kb` | `200` | Max size (KB) of a text file shown inline before it is truncated. |

## Security notes

- The viewer page runs under the requesting user's own permissions - it
  never reads with elevated rights. Standard `ir.attachment` access rules
  decide what each user may open.
- A visitor who is not logged in is redirected to the login page, never to
  a file.
- Links from URL-type attachments are only rendered as clickable when they
  use `http`/`https`, so a stored `javascript:` value can never execute.

## License

LGPL-3. See the `LICENSE` file.

## About BK

[kalkiinfinite.odoo.com](https://kalkiinfinite.odoo.com)
