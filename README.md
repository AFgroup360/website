# AmeriFinancial website

The site for AmeriFinancial (ameri-group.ca). Static multi page HTML, CSS and a
small amount of vanilla JavaScript. No framework, no runtime, no build step
required to serve it. Every page is real HTML, so it loads immediately and
indexes properly.

## Pages

```
index.html         Home
who-we-are.html    Who We Are
what-we-do.html    What We Do
our-approach.html  Our Approach
contact.html       Contact Us
privacy.html  terms.html  404.html
```

The navigation is four items. Home is reached through the logo.

## Files

```
css/tokens.css     Colour, type, spacing and layout tokens. The palette is
                   sampled from the AmeriFinancial logo.
css/base.css       Reset and element defaults.
css/main.css       Every component, in the order the pages use them.
js/main.js         Menu, active nav state, contact form, calendar link.
assets/img/        The logo lockup, the monogram, icons and the social card.
.htaccess          Clean URLs, redirects from retired pages, compression,
                   cache headers, a few security headers.
sitemap.xml  robots.txt
tools/             The page generator. See below.
```

## Editing the site

Pages are assembled from fragments plus shared chrome, so the header, footer,
sample review and closing call to action live in one place.

```
tools/pages/*.html   The body of each page. Edit these.
tools/partials.py    Header, footer, sample review, closing block.
tools/build.py       Writes the finished pages into the repo root.
```

After editing, rebuild:

```
python3 tools/build.py
```

Never edit the built `.html` files at the repo root by hand; the next build
overwrites them.

To preview locally:

```
python3 tools/serve.py      # http://localhost:8300
```

## Design rules

- One typeface, Geist, in four weights.
- Navy `#08162f` is the logo navy and the only dark ground on the site.
- Gold appears as one button, the active nav underline, section rules,
  overlines, arrows and the low opacity light behind navy sections. Nowhere
  else.
- Square corners. No shadows, no gradients on type, no metallic effects.
- No section repeats the archetype of the section directly above it.
- Every diagram has to explain something faster than a paragraph would. If it
  does not, it should be a paragraph.

## Still outstanding

- The contact form posts to `contact.php`, which emails `hello@ameri-group.ca`.
  GoDaddy shared hosting runs PHP, so it works once `contact.php` is in
  `public_html` and needs no third party service. It will not work on GitHub
  Pages, which cannot run PHP; there the form falls back to showing the email
  address and phone number. To use a form service instead, put its URL in
  `CONTACT_ENDPOINT` in `js/main.js` and delete `contact.php`.
- `CALENDAR_URL` in `js/main.js` needs a scheduling link. Until it is set, the
  "Pick a time" button is removed rather than left pointing nowhere.
- Real photography of operating businesses. Five slots are filled with
  placeholder images that should be replaced. Drop new files in `assets/img/`
  under these exact names and run `python3 tools/build.py`:

  | File | Where it lands |
  |---|---|
  | `hero.jpg` | the right half of the home page hero |
  | `photo-home.jpg` | full width, under the audience section |
  | `photo-who-we-are.jpg` | full width, under the layer diagram |
  | `photo-what-we-do.jpg` | full width, after the engagement types |
  | `photo-our-approach.jpg` | full width, before what we look at |

  `.jpeg`, `.png` and `.webp` also work. Nothing is emitted while a file is
  absent, so a missing photograph leaves no gap and never shows a placeholder.
  The hero splits into a two column layout only when `hero.jpg` exists, and
  falls back to the panel layout when it does not. Captions are set in
  `tools/pages/*.html` next to each slot.
- The original logo vector, if one exists. The header lockup is built from the
  supplied raster artwork.
- Written permission before any client name or logo appears on the site.

## Deploying

Upload the repo root to `public_html` on GoDaddy. Back up whatever is there
first. `.htaccess` handles clean URLs and the redirects from the retired pages.
