# -*- coding: utf-8 -*-
"""
Generates the 1200x630 social share card (assets/img/og-cover.jpg) using the
site's own design tokens, so link previews on LinkedIn/Discord/Slack match the
site instead of showing a bare text snippet.

Run: python tools/make_og_image.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "og-cover.jpg")

W, H = 1200, 630

# Site tokens (hsl -> rgb, matching style.css)
BG = (19, 22, 32)            # --background 228 25% 10%
BG_DEEP = (9, 11, 17)        # --background-deep
PRIMARY = (247, 178, 59)     # --primary 38 92% 60%
ACCENT = (44, 175, 219)      # --accent 196 80% 54%
FG = (248, 250, 252)         # --foreground
MUTED = (140, 152, 173)      # --muted-foreground

FONT_DIR = r"C:\Windows\Fonts"
mono = lambda size: ImageFont.truetype(os.path.join(FONT_DIR, "consolab.ttf"), size)
mono_r = lambda size: ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), size)
sans_b = lambda size: ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- soft radial glows (same palette as the hero orbs) ---------------------
glow = Image.new("RGB", (W, H), BG)
gd = ImageDraw.Draw(glow)
gd.ellipse([-160, -220, 470, 410], fill=(60, 48, 28))      # amber, top-left
gd.ellipse([760, 250, 1360, 850], fill=(20, 52, 70))       # cyan, bottom-right
gd.ellipse([430, 430, 900, 900], fill=(34, 26, 52))        # violet, bottom
from PIL import ImageFilter
glow = glow.filter(ImageFilter.GaussianBlur(150))
img = Image.blend(img, glow, 0.85)
d = ImageDraw.Draw(img)

# --- grid lines ------------------------------------------------------------
for x in range(0, W, 48):
    d.line([(x, 0), (x, H)], fill=(30, 34, 47), width=1)
for y in range(0, H, 48):
    d.line([(0, y), (W, y)], fill=(30, 34, 47), width=1)

# --- logo mark: rounded square with </> ------------------------------------
d.rounded_rectangle([80, 74, 138, 132], radius=14, fill=(46, 38, 22), outline=(112, 84, 34), width=2)
d.text((94, 88), "</>", font=mono(24), fill=PRIMARY)

d.text((156, 90), "romain", font=mono(26), fill=FG)
d.text((156 + d.textlength("romain", font=mono(26)), 90), ".", font=mono(26), fill=PRIMARY)
d.text((156 + d.textlength("romain.", font=mono(26)), 90), "pitot", font=mono(26), fill=FG)

# --- role line -------------------------------------------------------------
d.text((80, 232), "G A M E P L A Y   P R O G R A M M E R", font=mono(23), fill=PRIMARY)

# --- name ------------------------------------------------------------------
d.text((80, 282), "Romain", font=mono(96), fill=FG)
name_w = d.textlength("Romain ", font=mono(96))
d.text((80 + name_w, 282), "Pitot", font=mono(96), fill=ACCENT)

# --- tagline ---------------------------------------------------------------
d.text((80, 410), "Unity / C# — gameplay systems, AI, procedural", font=sans_b(30), fill=(206, 214, 227))
d.text((80, 452), "generation and multiplayer netcode.", font=sans_b(30), fill=(206, 214, 227))

# --- bottom rule + facts ---------------------------------------------------
d.line([(80, 528), (W - 80, 528)], fill=(46, 52, 68), width=1)
facts = "12 projects   ·   4 game jams   ·   2 titles live on Google Play"
d.text((80, 552), facts, font=mono_r(21), fill=MUTED)
d.text((W - 80 - d.textlength("romainpitot.github.io", font=mono_r(21)), 552),
       "romainpitot.github.io", font=mono_r(21), fill=PRIMARY)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, "JPEG", quality=90, optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
