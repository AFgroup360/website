#!/usr/bin/env python3
"""Bundle the built site into one self-contained HTML preview.

Every page, stylesheet, script and image goes into a single file, so the
preview can be published as an Artifact and viewed alongside the chat.
Each page is reconstructed at runtime as a blob URL and shown in an iframe,
which keeps sticky headers and width media queries behaving exactly as they
do on the real site.

    python3 tools/build_preview.py        # writes preview/preview.html
"""
import base64
import json
import mimetypes
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "preview" / "preview.html"

PAGES = [
    ("index.html", "Home"),
    ("services.html", "Services"),
    ("who-we-serve.html", "Who We Serve"),
    ("for-lenders.html", "For Lenders"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
    ("privacy.html", "Privacy"),
    ("terms.html", "Terms"),
    ("404.html", "404"),
]


def js_literal(value) -> str:
    """JSON for embedding inside a <script> tag.

    The pages carry their own inlined <script> blocks, and a literal
    "</script>" inside a string still closes the surrounding tag.
    """
    return json.dumps(value).replace("</", "<\\/")


def data_uri(path: pathlib.Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return "data:%s;base64,%s" % (mime, base64.b64encode(path.read_bytes()).decode())


def inline_page(name: str) -> str:
    """Fold the shared CSS and JS into a page so it stands alone."""
    html = (ROOT / name).read_text()

    css = "\n".join(
        (ROOT / f).read_text() for f in ("css/tokens.css", "css/base.css", "css/main.css")
    )
    html = re.sub(r'\s*<link rel="stylesheet" href="css/[^"]+">', "", html)
    html = html.replace("</head>", "<style>\n%s\n</style>\n</head>" % css)

    js = (ROOT / "js/main.js").read_text()
    html = html.replace('<script src="js/main.js" defer></script>',
                        "<script>\n%s\n</script>" % js)

    # Google Fonts is reachable from the published artifact, so the link stays.
    return html


def build() -> None:
    assets = {}
    for img in sorted((ROOT / "assets" / "img").iterdir()):
        if img.is_file():
            assets["assets/img/" + img.name] = data_uri(img)

    pages = {name: inline_page(name) for name, _ in PAGES}

    shell = (ROOT / "tools" / "preview_shell.html").read_text()
    shell = shell.replace("/*__ASSETS__*/", js_literal(assets))
    shell = shell.replace("/*__PAGES__*/", js_literal(pages))
    shell = shell.replace("/*__NAV__*/", js_literal([{"file": f, "label": l} for f, l in PAGES]))

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(shell)
    print("wrote %s  (%.1f MB)" % (OUT, OUT.stat().st_size / 1_048_576))


if __name__ == "__main__":
    build()
