# Shared chrome and reusable blocks for the static pages. Run tools/build.py.
#
# Pages in tools/pages/ may drop in these placeholders, which build.py expands:
#   {{BREADCRUMB: Label}}                     one level under Home
#   {{BREADCRUMB: Parent label > Label}}      two levels, parent links to PARENTS[label]
#   {{REVIEW}}                                the rendered sample review page
#   {{LETS_CONNECT}}                          the closing navy call to action

import pathlib
import re

NAV = [
    {"file": "who-we-are.html", "label": "Who We Are"},
    {"file": "what-we-do.html", "label": "What We Do"},
    {"file": "our-approach.html", "label": "Our Approach"},
    {"file": "contact.html", "label": "Contact Us"},
]

PARENTS = {}

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


def header():
    links = "\n".join(
        '      <a class="nav__link" href="{file}">{label}</a>'.format(**item)
        for item in NAV
    )
    return '''<header class="site-header">
  <div class="container site-header__inner">
    {lockup}
    <nav class="nav" id="primary-nav" aria-label="Primary">
{links}
      <a class="btn btn--primary nav__cta" href="contact.html">Book an introductory call</a>
    </nav>
    <div class="header__actions">
      <a class="btn btn--primary" href="contact.html">Book an introductory call</a>
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
    for name in ("hero.jpg", "hero.jpeg", "hero.png", "hero.webp"):
        if (root / "assets" / "img" / name).exists():
            return (f'<img class="hero__photo" src="assets/img/{name}" alt="" '
                    'aria-hidden="true" fetchpriority="high">\n'
                    '    <span class="hero__scrim" aria-hidden="true"></span>')
    return ""


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
        aria-label="The first page of a sample Financing Readiness Review. A verdict at the top with three possible outcomes and one of them marked, then three columns setting out what supports the position, what conditions would have to be met, and what was verified against source documents.">
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
      <li class="is-set">Financeable on conditions</li>
      <li>Not financeable in the current position</li>
    </ul>
  </div>
  <div class="review__cols">
    <div class="review__col">
      <h4>What supports the position</h4>
      <ul role="list">
        <li>Operating cash flow over the period reviewed</li>
        <li>Quality of the receivables book</li>
        <li>Work already contracted</li>
      </ul>
    </div>
    <div class="review__col">
      <h4>What the conditions address</h4>
      <ul role="list">
        <li>Obligations that rank ahead of new capital</li>
        <li>Arrears to be put on a schedule</li>
        <li>Amount sized to the measured gap</li>
      </ul>
    </div>
    <div class="review__col">
      <h4>What was verified</h4>
      <ul role="list">
        <li>Balances confirmed to source documents</li>
        <li>Method stated for each figure</li>
        <li>Anything still open is disclosed</li>
      </ul>
    </div>
  </div>
  <div class="review__foot">
    <span>Sample layout. No client information is shown.</span>
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
        </ul>
      </div>
      <div>
        <h4>The work</h4>
        <ul role="list">
          <li><a href="what-we-do.html#owners">For business owners</a></li>
          <li><a href="what-we-do.html#capital">For capital providers</a></li>
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
