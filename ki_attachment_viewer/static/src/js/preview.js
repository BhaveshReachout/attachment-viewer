/** @odoo-module ignore */
// License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

// Mirrors the on-screen previous/next buttons on the left/right arrow
// keys. Skipped while a modifier key is held, so browser shortcuts (e.g.
// Ctrl+ArrowLeft for browser history) keep working as expected.
(function () {
    "use strict";

    document.addEventListener("keydown", function (event) {
        if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) {
            return;
        }
        var page = document.querySelector(".av_page");
        if (!page) {
            return;
        }
        if (event.key === "ArrowLeft" && page.dataset.previousUrl) {
            window.location.href = page.dataset.previousUrl;
        } else if (event.key === "ArrowRight" && page.dataset.nextUrl) {
            window.location.href = page.dataset.nextUrl;
        }
    });
})();
