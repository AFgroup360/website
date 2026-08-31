# Ameri Group — website

Rebuild of ameri-group.ca. Same content, new design.

## Stack

Plain static HTML, CSS and JavaScript. No build step, no dependencies, no
runtime. The files in this repo are the files that go on the server.

This is deliberate, given the hosting:

- GoDaddy serves static files directly — nothing to compile or install.
- Pages load fast and keep working without maintenance.
- Any text change is a direct edit to an HTML file.

## Layout

```
index.html          Home
css/tokens.css      Design tokens — colour, type, spacing, elevation
css/base.css        Reset and default element styling
css/main.css        Components and page sections
js/main.js          Navigation and small interactions
assets/img/         Logo and images
CONTENT.md          Source copy for the site
```

## Working on it locally

Open `index.html` in a browser. That's it.

For a local server (needed if forms or fetch calls are added later):

```sh
python3 -m http.server 8000
```

Then visit http://localhost:8000

## Design tokens

Colour, type scale, spacing and shadows all live in `css/tokens.css` as CSS
custom properties. Components reference the variables rather than hard-coded
values, so rebranding is a matter of editing that one file.

## Deploying to GoDaddy

**cPanel File Manager**

1. GoDaddy account → Hosting → cPanel Admin → File Manager
2. Open `public_html`
3. Upload the contents of this repo — the files themselves, not the folder
   that contains them, so `index.html` sits directly in `public_html`
4. Hard-refresh the site (Ctrl/Cmd + Shift + R) to get past cached files

**FTP**

Get the FTP host, username and password from GoDaddy's hosting dashboard,
connect with any FTP client, and upload into `public_html`.

Keep a copy of the current site before overwriting it, so there's a way back.
