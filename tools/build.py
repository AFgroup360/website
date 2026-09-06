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
        "title": f"{BRAND} | Financial visibility, reporting and control",
        "description": ("We put the reporting, forecasting and financial controls in place "
                        "so owner led businesses, and the people financing them, know where "
                        "the business stands and what it can do next."),
    },
    "who-we-are": {
        "out": "who-we-are.html", "canonical": "/who-we-are",
        "title": t("Who We Are"),
        "description": ("A firm that goes into a business and builds the financial "
                        "visibility, reporting and control the decisions depend on."),
    },
    "what-we-do": {
        "out": "what-we-do.html", "canonical": "/what-we-do",
        "title": t("What We Do"),
        "description": ("Engagement types for business owners, work before and after "
                        "funding for capital providers, and the Financing Readiness Review."),
    },
    "for-business-owners": {
        "out": "for-business-owners.html", "canonical": "/for-business-owners",
        "title": t("For business owners"),
        "description": ("Three levels of involvement, from a clear monthly view to "
                        "someone working in the numbers with you through the month."),
    },
    "for-capital-providers": {
        "out": "for-capital-providers.html", "canonical": "/for-capital-providers",
        "title": t("For capital providers"),
        "description": ("Understanding a business before capital goes in, and keeping "
                        "it visible and under control after it does."),
    },
    "our-approach": {
        "out": "our-approach.html", "canonical": "/our-approach",
        "title": t("Our Approach"),
        "description": ("What we look at, how a month runs, and how a current view of "
                        "cash, margin and obligations gets the decision made in time."),
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
