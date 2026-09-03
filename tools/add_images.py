#!/usr/bin/env python3
"""Drop new photography into the site.

    python3 tools/add_images.py <folder-with-the-unzipped-images>

Matches files by keyword, copies them into assets/img/ under stable names,
points the hero and the showcase bands at them, and rebuilds.
"""
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"

# keyword in the filename -> the name the site uses
WANTED = {
    ("tower", "building", "skyscraper", "sky", "architect"): "hero-towers.jpg",
    ("tablet", "review", "chart", "meeting", "analys", "report"): "photo-review.jpg",
}


def main(src: pathlib.Path) -> None:
    found = {}
    for f in sorted(src.rglob("*")):
        if f.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        low = f.name.lower()
        for keys, target in WANTED.items():
            if target in found:
                continue
            if any(k in low for k in keys):
                shutil.copy(f, IMG / target)
                found[target] = f.name
                break

    # Anything unmatched still gets copied, in file order, into the free slots.
    leftovers = [f for f in sorted(src.rglob("*"))
                 if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
                 and f.name not in found.values()]
    for target in WANTED.values():
        if target not in found and leftovers:
            f = leftovers.pop(0)
            shutil.copy(f, IMG / target)
            found[target] = f.name

    for target, original in found.items():
        print(f"  {original}  ->  assets/img/{target}")
    if not found:
        print("  no images found in", src)
        return

    subprocess.run([sys.executable, str(ROOT / "tools" / "build.py")], check=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python3 tools/add_images.py <folder>")
    main(pathlib.Path(sys.argv[1]))
