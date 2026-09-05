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
    ("who-we-are.html", "Who We Are"),
    ("what-we-do.html", "What We Do"),
    ("our-approach.html", "Our Approach"),
    ("contact.html", "Contact Us"),
    ("privacy.html", "Privacy"),
    ("terms.html", "Terms"),
    ("404.html", "404"),
]

OLD = []
SHOTS = pathlib.Path("/tmp/none")


def old_page(label: str, shot: str) -> str:
    """A capture of the previous site, shown at its own width."""
    img = SHOTS / shot
    if not img.exists():
        return None
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<style>html,body{margin:0;background:#f2ede3}"
        "img{display:block;width:100%;height:auto}"
        ".tag{position:sticky;top:0;z-index:2;background:#1a2947;color:#fff;"
        "font:600 12px/1 system-ui,sans-serif;letter-spacing:.12em;"
        "text-transform:uppercase;padding:10px 16px}</style></head><body>"
        f"<div class='tag'>Previous live site &middot; {label}</div>"
        f"<img src='{data_uri(img)}' alt='{label} on the previous site'>"
        "</body></html>"
    )


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

    nav = [{"file": f, "label": l} for f, l in PAGES]
    for file, label, shot in OLD:
        html = old_page(label.replace("OLD ", ""), shot)
        if html:
            pages[file] = html
            nav.append({"file": file, "label": label})

    shell = (ROOT / "tools" / "preview_shell.html").read_text()
    shell = shell.replace("/*__ASSETS__*/", js_literal(assets))
    shell = shell.replace("/*__PAGES__*/", js_literal(pages))
    shell = shell.replace("/*__NAV__*/", js_literal(nav))

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(shell)
    print("wrote %s  (%.1f MB)" % (OUT, OUT.stat().st_size / 1_048_576))


if __name__ == "__main__":
    build()
