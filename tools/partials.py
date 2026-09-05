# Shared chrome and reusable blocks for the static pages. Run tools/build.py.
#
# Pages in tools/pages/ may drop in these placeholders, which build.py expands:
#   {{BREADCRUMB: Label}}                     one level under Home
#   {{BREADCRUMB: Parent label > Label}}      two levels, parent links to PARENTS[label]
#   {{JUMPTO: id=Label | id=Label | ...}}     the in page anchor row
#   {{REVIEW}}                                the rendered sample review page
#   {{GET_IN_TOUCH}}                          the contact card section, id="contact"
#   {{LETS_CONNECT}}                          the details and one button, id="connect"

import re

NAV = [
    {"file": "services.html", "label": "What we do"},
    {"file": "for-owners.html", "label": "For owners"},
    {"file": "for-capital-providers.html", "label": "For lenders and investors"},
    {"file": "about.html", "label": "Our work"},
    {"file": "contact.html", "label": "Contact"},
]

PARENTS = {
    "Our work": "about.html",
    "What we do": "services.html",
}

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
    <a class="brand" href="index.html">Ameri<em>Financial</em></a>
    <nav class="nav" id="primary-nav" aria-label="Primary">
{links}
        <a class="link-arrow" href="contact.html">Let's connect</a>
        <a class="btn btn--navy" href="contact.html">Book an introductory call</a>
    </nav>
    <div class="header__actions">
      <a class="link-arrow" href="contact.html">Let's connect</a>
      <a class="btn btn--navy" href="contact.html">Book an introductory call</a>
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


GET_IN_TOUCH = f'''<section class="section" id="contact">
  <div class="container">
    <span class="overline">Get in touch</span>
    <div class="contact-card">
      <img class="contact-card__photo" src="assets/img/photo-farid.jpg" width="160" height="160"
           alt="Farid Ameri" loading="lazy">
      <div>
        <p class="contact-card__name">Farid Ameri</p>
        <p class="contact-card__role">Founder, AmeriFinancial</p>
        <ul class="contact-card__list" role="list">
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{PHONE_HREF}">{PHONE}</a></li>
          <li><a href="#" data-placeholder="linkedin">LinkedIn</a></li>
        </ul>
      </div>
    </div>
  </div>
</section>'''


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
    body = body.replace("{{GET_IN_TOUCH}}", GET_IN_TOUCH)
    body = body.replace("{{LETS_CONNECT}}", LETS_CONNECT)
    return body


FOOTER = f'''</main>
<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div>
        <a class="brand" href="index.html">Ameri<em>Financial</em></a>
        <p class="site-footer__blurb">Monthly financial control and the Financing
          Readiness Review, for owner led businesses and the people who fund them.</p>
      </div>
      <div>
        <h4>Pages</h4>
        <ul role="list">
          <li><a href="services.html">What we do</a></li>
          <li><a href="for-owners.html">For owners</a></li>
          <li><a href="for-capital-providers.html">For lenders and investors</a></li>
          <li><a href="about.html">Our work</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Services</h4>
        <ul role="list">
          <li><a href="services.html#cash-flow">Cash flow control</a></li>
          <li><a href="services.html#reporting">Monthly reporting</a></li>
          <li><a href="services.html#working-capital">Working capital</a></li>
          <li><a href="services.html#financing">Financing readiness</a></li>
          <li><a href="services.html#review">The Financing Readiness Review</a></li>
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
