# AmeriFinancial — website

Rebuild of ameri-group.ca. New design, existing content.

The previous site was a compiled React SPA; this is a static multi-page site.
Every page is real HTML, so it loads instantly, indexes properly, and keeps
working without maintenance.

## Phase 1 — marketing site (this repo)

Eight pages: Home, Services, Who We Serve, About, Contact, Privacy, Terms, 404.
All copy is carried over verbatim from the previous site — see `CONTENT.md`.

## Phase 2 — client portal (not built yet)

Sign-in plus document upload (bank statements, credit-card statements). The nav
links to `/portal`, which does not exist in this repo yet.

> **Before deploying, read "Deploying" below.** If the current portal is live and
> clients use it, do not delete it from the server.

## Stack

Static HTML, CSS and JavaScript. No dependencies, no runtime, no build step
required to serve the site.

```
index.html  services.html  who-we-serve.html  about.html
contact.html  privacy.html  terms.html  404.html

css/tokens.css   Design tokens — colour, type, spacing, elevation
css/base.css     Reset and default element styling
css/main.css     Components and page sections
js/main.js       Nav, FAQ accordion, contact form, scroll reveal
assets/img/      Logos and photography
.htaccess        Clean URLs, 404, compression, caching
CONTENT.md       Source copy, recovered from the previous site
tools/           Optional page generator (see below)
```

## Previewing on GitHub Pages

Pages is enabled on the working branch, so the site is live at
**https://afgroup360.github.io/website/** for review.

That is a project page served from a `/website/` subpath, which is why every
internal link and asset path in this repo is relative rather than root-absolute.
The same relative paths work unchanged when the site sits at the domain root on
GoDaddy, so nothing needs adjusting between preview and production.

`.nojekyll` stops GitHub from running the files through Jekyll.

Turn Pages off under Settings → Pages once the site is live on the real domain,
so the preview copy doesn't linger in search results.

## Live preview panel

`tools/build_preview.py` bundles the whole site into a single self-contained
HTML file at `preview/preview.html`: every page, with the stylesheets, script
and images inlined. That file is published as an Artifact so the site can be
viewed alongside a chat while changes are being made.

```sh
python3 tools/build_preview.py
```

Each page is reconstructed at runtime as a blob URL and shown in an iframe, so
sticky headers and width media queries behave exactly as they do on the real
site. The toolbar switches pages and viewport width. Links inside the preview
drive the tabs rather than dead-ending.

The bundle is generated output and is not committed. Rebuild it after changing
any page, then republish to the same artifact URL to keep the link stable.

## Local preview

```sh
python3 tools/serve.py
```

Then visit http://localhost:8000. This mirrors the production `.htaccess`, so
extensionless URLs like `/services` resolve the same way they do live. Opening
the `.html` files directly from Finder or Explorer also works, but the clean
URLs won't.

## Editing content

Edit the `.html` files directly — the text is right there in the markup.

The one exception is the shared header and footer, which appear on all eight
pages. To change those, edit `tools/partials.py` and run:

```sh
python3 tools/build.py
```

That regenerates the eight HTML files from `tools/pages/*.html` plus the shared
chrome. It is a convenience for keeping the nav and footer in sync — the site
itself never needs it.

## Design tokens

Colour, type scale, spacing and shadows live in `css/tokens.css` as CSS custom
properties. The palette carries over from the previous site: navy `#1a2947`,
amber `#c89c51`, cream `#f2ede3`. Components reference the variables rather than
hard-coded values, so a rebrand is a one-file change.

Typography is Geist throughout, loaded from Google Fonts — one grotesque at
several weights rather than a serif/sans pairing. Headlines are set large, at
tight leading with negative tracking.

The visual register is institutional: white ground with light-grey bands, square
corners, hairline rules instead of drop shadows, flat surfaces, and a single
amber accent used sparingly for rules, markers and the primary action.

## Contact form

`js/main.js` posts the form as JSON to the endpoint in `CONTACT_ENDPOINT` at the
top of the file, currently `/api/contact` — the same endpoint the previous site
used.

**Static hosting cannot serve that endpoint.** If the form returns an error once
deployed, change `CONTACT_ENDPOINT` to a form service (Formspree, Web3Forms);
nothing else needs to change. The form already fails gracefully, showing the
email address and phone number if the request doesn't go through.

## Deploying to GoDaddy

**Before the first deploy:** download a copy of what is currently in
`public_html`. If the existing React portal is live and clients use it, keep
`assets/index-*.js`, the portal routes, and the old `.htaccess` somewhere safe —
uploading this site over it will replace the single-page-app routing that the
portal depends on.

**cPanel File Manager**

1. GoDaddy account → Hosting → cPanel Admin → File Manager
2. Open `public_html`
3. Upload the contents of this repo — the files themselves, not the folder that
   contains them, so `index.html` sits directly in `public_html`
4. Hard-refresh the site (Ctrl/Cmd + Shift + R) to get past cached files

**FTP**

Get the FTP host, username and password from GoDaddy's hosting dashboard,
connect with any FTP client, and upload into `public_html`.

Note that `.htaccess` is ignored by GitHub Pages — it only applies on GoDaddy.

`.htaccess` needs Apache with `mod_rewrite`, which GoDaddy shared hosting has on
by default. If clean URLs 404 after deploying, confirm the file uploaded —
`.htaccess` is hidden, so enable "show hidden files" in File Manager.
