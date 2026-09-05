# -*- coding: utf-8 -*-
"""
Generates typographic cover art for the projects that have no real screenshot,
so every project card carries the same visual weight instead of some looking
"finished" and others looking empty.

Covers use the site's own tokens, tinted per category, and are written to
assets/img/projects/<id>-cover.jpg.

Run: python tools/make_project_covers.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "img", "projects")
FONT_DIR = r"C:\Windows\Fonts"

W, H = 1280, 720
BG = (19, 22, 32)
FG = (248, 250, 252)
MUTED = (140, 152, 173)
GRID = (32, 36, 50)

# Category tints (converted from the CSS HSL tokens)
TINTS = {
    "Work": (62, 224, 207),       # --teal
    "School": (59, 222, 119),     # --green
    "Game Jam": (200, 135, 232),  # --violet
    "Personal": (130, 142, 248),  # --indigo
}

mono_b = lambda s: ImageFont.truetype(os.path.join(FONT_DIR, "consolab.ttf"), s)
mono_r = lambda s: ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), s)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make_cover(pid, title, category, engine, year, role):
    tint = TINTS.get(category, (62, 224, 207))

    img = Image.new("RGB", (W, H), BG)

    # Soft corner glow in the category colour
    glow = Image.new("RGB", (W, H), BG)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-260, -300, 620, 500], fill=tuple(int(c * 0.30) for c in tint))
    gd.ellipse([820, 420, 1560, 1060], fill=tuple(int(c * 0.16) for c in tint))
    glow = glow.filter(ImageFilter.GaussianBlur(170))
    img = Image.blend(img, glow, 0.9)

    d = ImageDraw.Draw(img)

    # Grid texture
    for x in range(0, W, 48):
        d.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, 48):
        d.line([(0, y), (W, y)], fill=GRID, width=1)

    # Title block, vertically centred so it survives both the 16:9 card crop
    # and the 21:8 crop used on project detail pages. No category chip or year:
    # the card already shows those as badges, and duplicating them looks noisy.
    size = 92 if len(title) <= 18 else 74
    tfont = mono_b(size)
    lines = wrap(d, title, tfont, W - 200)
    while len(lines) > 2 and size > 48:
        size -= 8
        tfont = mono_b(size)
        lines = wrap(d, title, tfont, W - 200)

    line_h = size + 16
    meta_gap = 58
    block_h = line_h * len(lines) + meta_gap
    top = (H - block_h) // 2

    d.line([(100, top - 30), (100 + 92, top - 30)], fill=tint, width=4)

    for i, ln in enumerate(lines):
        d.text((98, top + i * line_h), ln, font=tfont, fill=FG)

    meta = "%s   ·   %s" % (engine, role)
    mfont = mono_r(25)
    if d.textlength(meta, font=mfont) > W - 200:
        mfont = mono_r(21)
    d.text((100, top + line_h * len(lines) + 14), meta, font=mfont, fill=MUTED)

    out = os.path.join(OUT_DIR, "%s-cover.jpg" % pid)
    img.save(out, "JPEG", quality=88, optimize=True)
    print("wrote", os.path.basename(out), os.path.getsize(out), "bytes")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from build import PROJECTS

    os.makedirs(OUT_DIR, exist_ok=True)
    for p in PROJECTS:
        if p.get("image"):
            continue  # already has a real screenshot
        make_cover(p["id"], p["title"], p["category"], p["engine"], p["year"], p["role"])
