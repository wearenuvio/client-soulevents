#!/usr/bin/env python3
"""Build responsive AVIF + WebP variants for the site's photographs.

What next/image does at request time, done once at build time: every source
JPEG/PNG gets resized copies at a fixed ladder of widths, in AVIF and WebP,
written to an `opt/` folder beside it as `<stem>-<width>.<ext>`. The page asks
for them through <picture>/srcset; the original file stays as the fallback.

The width ladder must match WIDTHS in index.html (function `variants`):
    [w for w in WIDTHS if w < original] + [original]

Run from the repo root after adding or replacing photographs:
    python3 tools/optimize-images.py
Existing variants newer than their source are skipped.
"""
from pathlib import Path
from PIL import Image, ImageOps

WIDTHS = (480, 960, 1440)
AVIF_QUALITY = 52
WEBP_QUALITY = 78

# folder -> glob of sources to optimise
SOURCES = {
    "assets/gallery": "*.jpg",
    "assets/samples": "*.jpg",
    "assets/brand": "hero-lotus.png",
}


def ladder(width):
    return [w for w in WIDTHS if w < width] + [width]


def build(src: Path):
    out_dir = src.parent / "opt"
    out_dir.mkdir(exist_ok=True)
    im = ImageOps.exif_transpose(Image.open(src))
    keep_alpha = im.mode in ("RGBA", "LA") or "transparency" in im.info
    im = im.convert("RGBA" if keep_alpha else "RGB")
    made = 0
    for w in ladder(im.width):
        h = round(im.height * w / im.width)
        resized = None
        for ext, opts in (("avif", {"quality": AVIF_QUALITY}),
                          ("webp", {"quality": WEBP_QUALITY, "method": 6})):
            dst = out_dir / f"{src.stem}-{w}.{ext}"
            if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
                continue
            if resized is None:
                resized = im if w == im.width else im.resize((w, h), Image.LANCZOS)
            resized.save(dst, **opts)
            made += 1
    return made


def main():
    root = Path(__file__).resolve().parent.parent
    total = 0
    for folder, pattern in SOURCES.items():
        for src in sorted((root / folder).glob(pattern)):
            total += build(src)
    print(f"wrote {total} variant files")


if __name__ == "__main__":
    main()
