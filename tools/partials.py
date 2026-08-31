# Shared chrome for the static pages. Run tools/build.py to regenerate.

NAV = [
    ("index.html", "Home"),
    ("services.html", "Services"),
    ("who-we-serve.html", "Who We Serve"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add("js");</script>
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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=Geist:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/base.css">
<link rel="stylesheet" href="css/main.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
'''

def header():
    links = "\n".join(
        '        <a class="nav__link" href="{}">{}</a>'.format(h, l) for h, l in NAV
    )
    return '''<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="index.html">Ameri<em>Financial</em></a>
    <nav class="nav" id="primary-nav" aria-label="Primary">
{links}
        <a class="nav__link nav__link--portal" href="portal.html">Client Portal</a>
    </nav>
    <div class="header__actions">
      <a class="btn btn--ghost btn--desktop" href="portal.html">Client Portal</a>
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

CTA = '''<section class="cta">
  <div class="container">
    <p class="eyebrow eyebrow--on-dark" style="justify-content:center">Not sure if it's the right fit?</p>
    <h2>A short conversation is the easiest way to find out.</h2>
    <p>If we're not the right partner, we'll tell you. Inquiries are read personally
       and treated in confidence.</p>
    <div class="cta__actions">
      <a class="btn btn--accent" href="contact.html">Request a Financing Readiness Review
        <span class="btn__arrow" aria-hidden="true">&rarr;</span></a>
      <a class="btn btn--on-dark" href="tel:+14168790969">+1 (416) 879-0969</a>
    </div>
  </div>
</section>
'''

FOOTER = '''</main>
<footer class="site-footer">
  <div class="container">
    <div class="site-footer__grid">
      <div>
        <a class="brand" href="index.html">Ameri<em>Financial</em></a>
        <p class="site-footer__blurb">AmeriFinancial works with owner-led businesses on
          cash-flow visibility, management reporting, financial control and financing
          readiness. Toronto / GTA, Canada.</p>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="who-we-serve.html">Who We Serve</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="services.html#cash-flow">Cash Flow Control</a></li>
          <li><a href="services.html#reporting">Management Reporting</a></li>
          <li><a href="services.html#working-capital">Working Capital</a></li>
          <li><a href="services.html#financing">Financing Readiness</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:hello@ameri-group.ca">hello@ameri-group.ca</a></li>
          <li><a href="tel:+14168790969">+1 (416) 879-0969</a></li>
          <li><a href="portal.html">Client Portal</a></li>
        </ul>
      </div>
    </div>
    <div class="site-footer__base">
      <span>&copy; {year} AmeriFinancial. Toronto / GTA &middot; Canada.</span>
      <span><a href="privacy.html">Privacy Policy</a> &middot; <a href="terms.html">Terms of Service</a></span>
    </div>
  </div>
</footer>
<script src="js/main.js" defer></script>
</body>
</html>
'''
