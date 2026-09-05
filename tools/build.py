#!/usr/bin/env python3
"""Assemble the static pages from tools/pages/*.html plus the shared chrome.

    python3 tools/build.py

Output is standalone HTML in the repo root. Edit tools/pages and this file,
never the built pages.
"""
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import partials  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRAND = "AmeriFinancial"


def t(page):
    return f"{page} | {BRAND}"


PAGES = {
    "index": {
        "out": "index.html", "canonical": "/",
        "title": f"{BRAND} | Financial control for owner led businesses",
        "description": ("The financial control layer between bookkeeping and the decisions "
                        "you run the business on. For owner led businesses and the people "
                        "who fund them."),
    },
    "who-we-are": {
        "out": "who-we-are.html", "canonical": "/who-we-are",
        "title": t("Who We Are"),
        "description": ("A finance function you can hire by the month, for owner led "
                        "businesses in Ontario."),
    },
    "what-we-do": {
        "out": "what-we-do.html", "canonical": "/what-we-do",
        "title": t("What We Do"),
        "description": ("Cash flow control, management reporting, working capital and "
                        "financing readiness, run every month."),
    },
    "our-approach": {
        "out": "our-approach.html", "canonical": "/our-approach",
        "title": t("Our Approach"),
        "description": ("One idea read from two sides of the table. Better visibility and "
                        "stronger financial control make a healthier business."),
    },
    "contact": {
        "out": "contact.html", "canonical": "/contact",
        "title": t("Contact Us"),
        "description": "Book an introductory call with AmeriFinancial in Mississauga, Ontario.",
    },
    "privacy": {
        "out": "privacy.html", "canonical": "/privacy",
        "title": t("Privacy policy"),
        "description": "How AmeriFinancial collects, uses and protects client information.",
    },
    "terms": {
        "out": "terms.html", "canonical": "/terms",
        "title": t("Terms of service"),
        "description": "Terms governing use of the AmeriFinancial website.",
    },
    "404": {
        "out": "404.html", "canonical": "/404",
        "title": t("Page not found"),
        "description": "The page you were looking for could not be found.",
        "noindex": True,
    },
}


def build():
    year = datetime.date.today().year
    header = partials.header()
    footer = partials.FOOTER.replace("{year}", str(year))

    for name, meta in PAGES.items():
        body = (ROOT / "tools" / "pages" / f"{name}.html").read_text()
        body = partials.expand(body)
        head = partials.HEAD.format(
            title=meta["title"], description=meta["description"], canonical=meta["canonical"],
        )
        if meta.get("noindex"):
            head = head.replace('content="index, follow"', 'content="noindex, follow"')
        html = head + header + body + footer
        (ROOT / meta["out"]).write_text(html)
        print(f"  wrote {meta['out']:<36} {len(html):>7,} bytes")


if __name__ == "__main__":
    print("Building pages")
    build()
    print("Done.")
