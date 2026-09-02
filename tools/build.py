#!/usr/bin/env python3
"""Assemble the static pages from tools/pages/*.html plus the shared chrome.

Output is plain, standalone HTML in the repo root — the server needs nothing but
these files. Re-run this only when the shared header/footer changes:

    python3 tools/build.py
"""
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import partials  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRAND = "AmeriFinancial"

PAGES = {
    "index": {
        "out": "index.html",
        "canonical": "/",
        "title": f"{BRAND} — Finance control for owner-led businesses",
        "description": (
            "AmeriFinancial gives owner-led businesses a clear forward view of their "
            "finances — cash visibility, monthly reporting, collections and payments "
            "discipline, and financing readiness. The finance-control layer between "
            "your bookkeeper and accountant."
        ),
        "cta": True,
    },
    "services": {
        "out": "services.html",
        "canonical": "/services",
        "title": f"Services — {BRAND}",
        "description": (
            "Four pillars of financial control delivered through transparent monthly "
            "packages: cash flow control, monthly reporting, working-capital discipline "
            "and financing readiness."
        ),
        "cta": True,
    },
    "who-we-serve": {
        "out": "who-we-serve.html",
        "canonical": "/who-we-serve",
        "title": f"Who We Serve — {BRAND}",
        "description": (
            "Owners and capital providers ask the same question from opposite chairs. "
            "Can the business carry the money. The same numbers answer both."
        ),
        "cta": True,
    },
    "for-owners": {
        "out": "for-owners.html",
        "canonical": "/for-owners",
        "title": f"For Owners — {BRAND}",
        "description": (
            "For owner-led businesses that outgrew bookkeeping. Current numbers, a "
            "forward view of cash, and a clear answer on what the business can carry "
            "before taking on financing."
        ),
        "cta": {
            "eyebrow": "Where it starts",
            "heading": "One call. We tell you what we would look at first.",
            "body": ("A short conversation about the business, the numbers you have, and "
                     "what is actually pressing. If we're not the right partner, we'll "
                     "tell you on that call."),
            "action": "Book an introductory call",
        },
    },
    "for-capital-providers": {
        "out": "for-capital-providers.html",
        "canonical": "/for-capital-providers",
        "title": f"For Capital Providers — {BRAND}",
        "description": (
            "Independent financial diagnostic before a lender or investor funds an "
            "owner-led business, and monthly oversight for the life of the facility. "
            "Bank statement led analysis, not bookkeeping led."
        ),
        "cta": True,
    },
    "about": {
        "out": "about.html",
        "canonical": "/about",
        "title": f"About — {BRAND}",
        "description": (
            "Why AmeriFinancial exists, the approach behind the work, and the people "
            "running it — founded by Farid Ameri to close the gap between bookkeeping "
            "and financial visibility."
        ),
        "cta": True,
    },
    "contact": {
        "out": "contact.html",
        "canonical": "/contact",
        "title": f"Contact — {BRAND}",
        "description": (
            "Start with an introductory conversation. Inquiries are read personally and "
            "treated in confidence. Toronto / GTA, Canada."
        ),
        "cta": False,
    },
    "privacy": {
        "out": "privacy.html",
        "canonical": "/privacy",
        "title": f"Privacy Policy — {BRAND}",
        "description": "How AmeriFinancial collects, uses and protects client information.",
        "cta": False,
    },
    "terms": {
        "out": "terms.html",
        "canonical": "/terms",
        "title": f"Terms of Service — {BRAND}",
        "description": "Terms governing use of the AmeriFinancial website and client portal.",
        "cta": False,
    },
    "404": {
        "out": "404.html",
        "canonical": "/404",
        "title": f"Page not found — {BRAND}",
        "description": "The page you were looking for could not be found.",
        "cta": False,
        "noindex": True,
    },
}


def build():
    year = datetime.date.today().year
    header = partials.header()
    footer = partials.FOOTER.format(year=year)

    for name, meta in PAGES.items():
        body = (ROOT / "tools" / "pages" / f"{name}.html").read_text()
        head = partials.HEAD.format(
            title=meta["title"],
            description=meta["description"],
            canonical=meta["canonical"],
        )
        if meta.get("noindex"):
            head = head.replace(
                '<meta name="robots" content="index, follow">',
                '<meta name="robots" content="noindex, follow">',
            )

        html = head + header + body
        if meta.get("cta"):
            over = meta["cta"] if isinstance(meta["cta"], dict) else None
            html += partials.cta(over)
        html += footer

        (ROOT / meta["out"]).write_text(html)
        print(f"  wrote {meta['out']:<20} {len(html):>7,} bytes")


if __name__ == "__main__":
    print("Building pages…")
    build()
    print("Done.")
