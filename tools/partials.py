# Shared chrome and reusable blocks for the static pages. Run tools/build.py.
#
# Pages in tools/pages/ may drop in these placeholders, which build.py expands:
#   {{BREADCRUMB: Label}}                     one level under Home
#   {{BREADCRUMB: Parent label > Label}}      two levels, parent links to PARENTS[label]
#   {{HERO_PHOTO}}                            the hero photograph, if supplied
#   {{PHOTO: slug | caption}}                 a full bleed photograph, if supplied
#   {{REVIEW}}                                the rendered sample review page
#   {{LETS_CONNECT}}                          the closing navy call to action

import pathlib
import re

NAV = [
    {"file": "who-we-are.html", "label": "Who We Are"},
    {"file": "what-we-do.html", "label": "What We Do", "children": [
        {"file": "for-business-owners.html", "label": "For business owners",
         "note": "Three levels of involvement"},
        {"file": "for-capital-providers.html", "label": "For capital providers",
         "note": "Before funding, and after"},
    ]},
    {"file": "our-approach.html", "label": "Our Approach"},
    {"file": "contact.html", "label": "Contact Us"},
]

PARENTS = {"What We Do": "what-we-do.html"}

EMAIL = "hello@ameri-group.ca"
PHONE = "+1 (416) 879-0969"
PHONE_HREF = "tel:+14168790969"
CITY = "Mississauga, Ontario"

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://ameri-group.ca{canonical}">
<meta name="theme-color" content="#08162f">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AmeriFinancial">
<meta property="og:url" content="https://ameri-group.ca{canonical}">
<meta property="og:image" content="https://ameri-group.ca/assets/img/opengraph.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://ameri-group.ca/assets/img/opengraph.jpg">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/icon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="assets/img/icon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="assets/img/icon-512.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="css/main.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
'''

# The real logo assets. "Financial" is white in the artwork, so every ground
# the lockup sits on is navy.
LOCKUP = '''<a class="brand" href="index.html" aria-label="AmeriFinancial, back to home">
      <img class="brand__lockup" src="assets/img/logo-lockup.png"
           alt="AmeriFinancial" width="1182" height="150" decoding="async">
      <img class="brand__markonly" src="assets/img/logo-mark.png"
           alt="AmeriFinancial" width="271" height="181" loading="lazy" decoding="async">
    </a>'''


def nav_item(item, index):
    """One navigation entry, with a submenu when the page has two ways in."""
    if not item.get("children"):
        return '      <a class="nav__link" href="{file}">{label}</a>'.format(**item)

    menu_id = f"nav-menu-{index}"
    kids = "\n".join(
        '          <a class="nav__sub" href="{file}"><strong>{label}</strong>'
        '<span>{note}</span></a>'.format(**child)
        for child in item["children"]
    )
    return f'''      <div class="nav__group">
        <a class="nav__link" href="{item["file"]}">{item["label"]}</a>
        <button class="nav__caret" type="button" aria-expanded="false"
                aria-controls="{menu_id}"
                aria-label="Show {item["label"]} sections"></button>
        <div class="nav__menu" id="{menu_id}">
{kids}
        </div>
      </div>'''


def header():
    links = "\n".join(nav_item(item, i) for i, item in enumerate(NAV))
    return '''<header class="site-header">
  <div class="container site-header__inner">
    {lockup}
    <nav class="nav" id="primary-nav" aria-label="Primary">
{links}
      <a class="nav__link nav__link--portal" href="portal/">Client portal</a>
    </nav>
    <div class="header__actions">
      <a class="header__portal" href="portal/">Client portal</a>
      <button class="nav-toggle" type="button" aria-expanded="false"
              aria-controls="primary-nav" aria-label="Toggle menu">
        <span class="nav-toggle__bar"></span>
        <span class="nav-toggle__bar"></span>
        <span class="nav-toggle__bar"></span>
      </button>
    </div>
  </div>
</header>
<main id="main">
'''.format(links=links, lockup=LOCKUP)


def hero_photo():
    """The hero photograph, if one has been supplied.

    Drop a wide photograph of an operating business at
    assets/img/hero.jpg and rebuild. Nothing is emitted while the file is
    absent, so the hero is plain navy rather than a placeholder.
    """
    root = pathlib.Path(__file__).resolve().parent.parent
    src = _find("hero")
    if not src:
        return ""
    return (f'<img class="hero__photo" src="{src}" alt="" '
            'aria-hidden="true" fetchpriority="high">\n'
            '    <span class="hero__scrim" aria-hidden="true"></span>')


PHOTO_EXTS = ("jpg", "jpeg", "png", "webp")


def _find(slug):
    """The supplied photograph for a slot, if there is one."""
    root = pathlib.Path(__file__).resolve().parent.parent
    for ext in PHOTO_EXTS:
        if (root / "assets" / "img" / f"{slug}.{ext}").exists():
            return f"assets/img/{slug}.{ext}"
    return None


def photo(spec):
    """A full bleed photograph, if the file for that slot has been supplied.

    Used as {{PHOTO: slug | caption}}. Drop the picture at
    assets/img/<slug>.jpg and rebuild. Nothing is emitted while the file is
    absent, so a missing photograph leaves no gap and no placeholder.
    """
    parts = [x.strip() for x in spec.split("|")]
    slug = parts[0]
    caption = parts[1] if len(parts) > 1 else ""
    mode = parts[2] if len(parts) > 2 else ""
    src = _find(slug)
    if not src:
        return ""
    alt = caption or "An operating business at work"
    if mode == "overlay":
        return (f'<figure class="photo-band photo-band--overlay">\n'
                f'  <img src="{src}" alt="{alt}" loading="lazy" decoding="async">\n'
                f'  <figcaption><span>{caption}</span></figcaption>\n'
                f'</figure>')
    if mode == "bare":
        return (f'<figure class="photo-band">\n'
                f'  <img src="{src}" alt="{alt}" loading="lazy" decoding="async">\n'
                f'</figure>')
    cap = f'\n  <figcaption>{caption}</figcaption>' if caption else ""
    return (f'<figure class="photo-band">\n'
            f'  <img src="{src}" alt="{alt}" loading="lazy" decoding="async">{cap}\n'
            f'</figure>')


def breadcrumb(spec):
    parts = [p.strip() for p in spec.split(">")]
    items = ['<li><a href="index.html">Home</a></li>']
    for p in parts[:-1]:
        href = PARENTS.get(p, "#")
        items.append(f'<li><a href="{href}">{p}</a></li>')
    items.append(f'<li aria-current="page">{parts[-1]}</li>')
    inner = "\n    ".join(items)
    return f'''<nav aria-label="Breadcrumb">
  <ol class="breadcrumb" role="list">
    {inner}
  </ol>
</nav>'''


# The sample review carries the format and the verdict, not figures. There are
# no company specific numbers on it because there is no real company behind it.
REVIEW = '''<figure class="review" role="img"
        aria-label="The first page of a sample Financing Readiness Review. A verdict with three possible outcomes and one of them marked, a chart of the cash position over the next thirteen weeks with the tightest week marked, a bar showing how much of the cash the business has already committed and how much is left to carry new capital, and three lines on how the figures were checked.">
  <div class="review__head">
    <div>
      <p class="review__kicker">Financing Readiness Review</p>
      <p class="review__company">Summary and verdict</p>
    </div>
    <span class="review__tag">Sample format</span>
  </div>
  <div class="review__verdict">
    <p class="review__kicker">Readiness verdict</p>
    <ul class="review__options" role="list">
      <li>Financeable</li>
      <li class="is-set">On conditions</li>
      <li>Not yet</li>
    </ul>
  </div>
  <div class="review__panels">
    <div class="review__panel">
      <p class="review__kicker">Cash, next 13 weeks</p>
      <div class="rvchart">
      <span class="rvchart__bar" style="--h: 74%"></span>
      <span class="rvchart__bar" style="--h: 66%"></span>
      <span class="rvchart__bar" style="--h: 58%"></span>
      <span class="rvchart__bar" style="--h: 63%"></span>
      <span class="rvchart__bar" style="--h: 50%"></span>
      <span class="rvchart__bar" style="--h: 42%"></span>
      <span class="rvchart__bar" style="--h: 34%"></span>
      <span class="rvchart__bar is-low" style="--h: 27%"></span>
      <span class="rvchart__bar" style="--h: 40%"></span>
      <span class="rvchart__bar" style="--h: 54%"></span>
      <span class="rvchart__bar" style="--h: 62%"></span>
      <span class="rvchart__bar" style="--h: 71%"></span>
      <span class="rvchart__bar" style="--h: 79%"></span>
      </div>
      <p class="review__note">Tightest week marked</p>
    </div>
    <div class="review__panel">
      <p class="review__kicker">What it can carry</p>
      <div class="rvbars">
        <div class="rvbar">
          <span>Already committed</span>
          <span class="rvbar__track"><i style="--w: 68%"></i></span>
        </div>
        <div class="rvbar rvbar--free">
          <span>Room for new capital</span>
          <span class="rvbar__track"><i style="--w: 32%"></i></span>
        </div>
      </div>
      <p class="review__note">Sized to the measured gap</p>
    </div>
  </div>
  <ul class="review__points" role="list">
    <li>Balances confirmed to source documents</li>
    <li>Method stated for each figure</li>
    <li>Anything still open is disclosed</li>
  </ul>
  <div class="review__foot">
    <span>Sample layout. No client figures are shown.</span>
    <span>Page 1</span>
  </div>
</figure>'''


LETS_CONNECT = f'''<section class="connect-band rays" id="connect">
  <div class="container">
    <div class="connect">
      <div>
        <span class="overline">Let's connect</span>
        <h2>Start with an introductory conversation.</h2>
      </div>
      <div>
        <ul class="connect__details" role="list">
          <li><a href="{PHONE_HREF}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{CITY}</li>
        </ul>
        <a class="btn btn--primary" href="contact.html">Book an introductory call</a>
      </div>
    </div>
  </div>
</section>'''


def expand(body):
    """Replace the page placeholders with their blocks."""
    body = re.sub(r"\{\{BREADCRUMB:\s*(.+?)\s*\}\}", lambda m: breadcrumb(m.group(1)), body)
    body = re.sub(r"\{\{PHOTO:\s*(.+?)\s*\}\}", lambda m: photo(m.group(1)), body)
    body = body.replace("{{HERO_PHOTO}}", hero_photo())
    body = body.replace("{{REVIEW}}", REVIEW)
    body = body.replace("{{LETS_CONNECT}}", LETS_CONNECT)
    return body


FOOTER = f'''</main>
<footer class="site-footer rays rays--soft">
  <div class="container">
    <div class="site-footer__grid">
      <div>
        {LOCKUP}
        <p class="site-footer__blurb">Financial visibility, reporting and control for
          owner led businesses and the people who finance them.</p>
      </div>
      <div>
        <h4>Pages</h4>
        <ul role="list">
          <li><a href="who-we-are.html">Who We Are</a></li>
          <li><a href="what-we-do.html">What We Do</a></li>
          <li><a href="our-approach.html">Our Approach</a></li>
          <li><a href="contact.html">Contact Us</a></li>
          <li><a href="portal/">Client portal</a></li>
        </ul>
      </div>
      <div>
        <h4>The work</h4>
        <ul role="list">
          <li><a href="for-business-owners.html">For business owners</a></li>
          <li><a href="for-capital-providers.html">For capital providers</a></li>
          <li><a href="what-we-do.html#review">Financing Readiness Review</a></li>
          <li><a href="our-approach.html#month">How a month runs</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <address>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
          <a href="{PHONE_HREF}">{PHONE}</a>
          <span>{CITY}</span>
        </address>
      </div>
    </div>
    <div class="site-footer__base">
      <span>&copy; {{year}} AmeriFinancial. {CITY}.</span>
      <span><a href="privacy.html">Privacy policy</a> &nbsp;&middot;&nbsp; <a href="terms.html">Terms of service</a></span>
    </div>
  </div>
</footer>
<script src="js/main.js" defer></script>
</body>
</html>
'''
