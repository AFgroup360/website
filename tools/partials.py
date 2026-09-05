# Shared chrome and reusable blocks for the static pages. Run tools/build.py.
#
# Pages in tools/pages/ may drop in these placeholders, which build.py expands:
#   {{BREADCRUMB: Label}}                     one level under Home
#   {{BREADCRUMB: Parent label > Label}}      two levels, parent links to PARENTS[label]
#   {{JUMPTO: id=Label | id=Label | ...}}     the in page anchor row
#   {{REVIEW}}                                the rendered sample review page
#   {{LETS_CONNECT}}                          the details and one button, id="connect"

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
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://ameri-group.ca{canonical}">
<meta property="og:image" content="https://ameri-group.ca/assets/img/opengraph.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://ameri-group.ca/assets/img/opengraph.jpg">
<link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
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


def header():
    links = "\n".join(
        '        <a class="nav__link" href="{file}">{label}</a>'.format(**item)
        for item in NAV
    )
    return '''<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="index.html" aria-label="AmeriFinancial, back to home">
      <svg class="brand__mark" viewBox="0 0 120 96" fill="currentColor" aria-hidden="true" focusable="false">
        <path fill-rule="evenodd" d="M34 0 L52 0 L78 96 L60 96 L54.5 76 L23.5 76 L18 96 L0 96 Z M29 58 L49 58 L39 26 Z"/>
        <path d="M62 0 L78 0 L78 96 L62 96 Z"/>
        <path d="M78 0 L118 0 L108 18 L78 18 Z"/>
        <path d="M78 38 L106 38 L97 56 L78 56 Z"/>
      </svg>
      <span class="brand__rule" aria-hidden="true"></span>
      <span class="brand__word"><b>Ameri</b><i>Financial</i></span>
    </a>
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
'''.format(links=links)


def breadcrumb(spec):
    parts = [p.strip() for p in spec.split(">")]
    items = ['<li><a href="index.html">Home</a></li>']
    for p in parts[:-1]:
        href = PARENTS.get(p, "#")
        items.append(f'<li><a href="{href}">{p}</a></li>')
    items.append(f'<li aria-current="page">{parts[-1]}</li>')
    inner = "\n    ".join(items)
    return f'''<nav class="breadcrumb" aria-label="Breadcrumb">
  <ol class="breadcrumb" role="list">
    {inner}
  </ol>
</nav>'''


def jumpto(spec):
    links = []
    for pair in spec.split("|"):
        anchor, label = [s.strip() for s in pair.split("=", 1)]
        links.append(f'<a href="#{anchor}">{label}</a>')
    inner = "\n  ".join(links)
    return f'''<nav class="jumpto" aria-label="Jump to">
  <span class="jumpto__label">Jump to</span>
  {inner}
</nav>'''


# Fictional company, fictional figures. Labelled as a sample on the page.
REVIEW = '''<figure class="review" role="img"
        aria-label="The first page of a sample Financing Readiness Review for a fictional company. A verdict at the top, then three columns setting out what supports the case, what the conditions must address, and what makes it transaction ready.">
  <div class="review__head">
    <div>
      <p class="review__kicker">Financing Readiness Review</p>
      <p class="review__company">Northfield Packaging Systems Inc.</p>
    </div>
    <span class="review__tag">Sample</span>
  </div>
  <div class="review__verdict">
    <p class="review__kicker">Readiness verdict</p>
    <p>Financeable on specific, addressable conditions.</p>
  </div>
  <div class="review__cols">
    <div class="review__col">
      <h4>What supports it</h4>
      <ul role="list">
        <li>Operating cash positive in 9 of the last 12 months</li>
        <li>Receivables largely current, institutional customers</li>
        <li>Order book covers the coming two quarters</li>
      </ul>
    </div>
    <div class="review__col">
      <h4>What the conditions address</h4>
      <ul role="list">
        <li>Supplier balances past 90 days</li>
        <li>Tax arrears to be put on a schedule</li>
        <li>Stabilisation amount to be validated</li>
      </ul>
    </div>
    <div class="review__col">
      <h4>What makes it transaction ready</h4>
      <ul role="list">
        <li>Debt balances confirmed to source</li>
        <li>Monthly controls in place before funding</li>
        <li>Conditions met and evidenced</li>
      </ul>
    </div>
  </div>
  <div class="review__foot">
    <span>Fictional company and figures, shown to illustrate the format</span>
    <span>Page 1 of 5</span>
  </div>
</figure>'''


LETS_CONNECT = f'''<section class="section" id="connect">
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
    body = re.sub(r"\{\{JUMPTO:\s*(.+?)\s*\}\}", lambda m: jumpto(m.group(1)), body)
    body = body.replace("{{REVIEW}}", REVIEW)
    body = body.replace("{{LETS_CONNECT}}", LETS_CONNECT)
    return body


FOOTER = f'''</main>
<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div>
        <a class="brand" href="index.html" aria-label="AmeriFinancial, back to home">
        <svg class="brand__mark" viewBox="0 0 120 96" fill="currentColor" aria-hidden="true" focusable="false">
          <path fill-rule="evenodd" d="M34 0 L52 0 L78 96 L60 96 L54.5 76 L23.5 76 L18 96 L0 96 Z M29 58 L49 58 L39 26 Z"/>
          <path d="M62 0 L78 0 L78 96 L62 96 Z"/>
          <path d="M78 0 L118 0 L108 18 L78 18 Z"/>
          <path d="M78 38 L106 38 L97 56 L78 56 Z"/>
        </svg>
        <span class="brand__rule" aria-hidden="true"></span>
        <span class="brand__word"><b>Ameri</b><i>Financial</i></span>
    </a>
        <p class="site-footer__blurb">Financial visibility, reporting and control for
          owner led businesses and the people who fund them.</p>
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
        <h4>What we do</h4>
        <ul role="list">
          <li><a href="what-we-do.html#cash-flow">Cash flow control</a></li>
          <li><a href="what-we-do.html#reporting">Management reporting</a></li>
          <li><a href="what-we-do.html#working-capital">Working capital</a></li>
          <li><a href="what-we-do.html#financing">Financing readiness</a></li>
          <li><a href="what-we-do.html#review">The Financing Readiness Review</a></li>
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
