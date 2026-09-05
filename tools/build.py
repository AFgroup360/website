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
        "title": f"{BRAND} | Financial control and financing readiness",
        "description": ("Monthly financial control and the Financing Readiness Review for "
                        "owner led businesses, and for the lenders and investors who fund them."),
    },
    "services": {
        "out": "services.html", "canonical": "/services",
        "title": t("What we do"),
        "description": ("Four areas of financial control, the Financing Readiness Review, "
                        "and how a month runs with AmeriFinancial."),
    },
    "for-owners": {
        "out": "for-owners.html", "canonical": "/for-owners",
        "title": t("For owners"),
        "description": ("For owner led businesses that outgrew bookkeeping. Current numbers, "
                        "a forward view of cash, and a review a lender can act on."),
    },
    "for-capital-providers": {
        "out": "for-capital-providers.html", "canonical": "/for-capital-providers",
        "title": t("For lenders and investors"),
        "description": ("An independent Financing Readiness Review before you fund an owner "
                        "led business, and monthly financial control for as long as the "
                        "engagement runs."),
    },
    "about": {
        "out": "about.html", "canonical": "/about",
        "title": t("Our work"),
        "description": ("What AmeriFinancial has done for owner led businesses and the "
                        "people who fund them."),
    },
    "our-work-systems-supplier": {
        "out": "our-work-systems-supplier.html", "canonical": "/our-work-systems-supplier",
        "title": t("A systems supplier preparing for private financing"),
        "description": ("Twenty four months of bank activity rebuilt and a verdict on page one "
                        "for an owner led systems supplier."),
    },
    "our-work-food-producer": {
        "out": "our-work-food-producer.html", "canonical": "/our-work-food-producer",
        "title": t("A food producer under lender pressure"),
        "description": ("Cash brought under control and monthly reporting landed for a food "
                        "producer under lender pressure."),
    },
    "our-work-family-business": {
        "out": "our-work-family-business.html", "canonical": "/our-work-family-business",
        "title": t("A family business with no finance function"),
        "description": ("A finance department built from nothing and supplier terms realigned "
                        "so money out matched money in."),
    },
    "contact": {
        "out": "contact.html", "canonical": "/contact",
        "title": t("Contact"),
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
