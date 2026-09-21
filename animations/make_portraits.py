#!/usr/bin/env python3
"""Build portrait cards for the two teleportation characters,
Penelope (q1, sender) and Odysseus (q3, receiver), for the interactive
teleportation page and the GIF.

If a source photo exists at animations/img/src/{penelope,odysseus}.jpg it is used
as the portrait (the film's leads — Anne Hathaway and Matt Damon, from The Odyssey
(2026), dir. C. Nolan; sources fetched from themoviedb.org). Otherwise a drawn
placeholder is produced so the build never fails. In both cases a gold frame and a
nameplate (character, qubit role, film credit) are overlaid.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

W, H = 480, 600
BASE = os.path.dirname(__file__)
OUT = os.path.join(BASE, "img")
SRC = os.path.join(OUT, "src")
GOLD = (212, 160, 23)

def font(sz, serif=True):
    cands = ([
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
    ] if serif else [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ])
    for p in cands:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()

def lerp(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))

def photo_bg(path):
    """Cover-crop the source photo to WxH, biased toward the top (keep the face)."""
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s + 0.5), int(im.height * s + 0.5)), Image.LANCZOS)
    left = (im.width - W) // 2
    top = (im.height - H) // 4
    return im.crop((left, top, left + W, top + H))

def placeholder_bg(top, bot, skin, shadow):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(top, bot, y / H))
    cx, cy, r = W // 2, 250, 96
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=skin)
    d.pieslice([cx - 138, cy + r + 12, cx + 138, cy + r + 300], 180, 360, fill=skin)
    return img

def nameplate(img, name, role, credit):
    band = 190
    grad = Image.new("L", (1, band))
    for i in range(band):
        grad.putpixel((0, i), int(240 * (i / band) ** 1.25))
    overlay = Image.new("RGBA", (W, band), (5, 9, 18, 0))
    overlay.putalpha(grad.resize((W, band)))
    img.paste(overlay, (0, H - band), overlay)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([8, 8, W - 9, H - 9], outline=GOLD, width=3)
    d.line([(30, H - band + 22), (W - 30, H - band + 22)], fill=GOLD, width=1)

    def ctext(y, s, fnt, fill):
        w = d.textlength(s, font=fnt)
        d.text(((W - w) / 2, y), s, font=fnt, fill=fill)
    ctext(H - 128, name, font(52), (255, 255, 255))
    ctext(H - 66, role, font(22, serif=False), (232, 232, 238))
    ctext(H - 38, f"THE ODYSSEY (2026)  ·  {credit}", font(14, serif=False), GOLD)

def card(fname, name, role, credit, ph_colors):
    src = os.path.join(SRC, fname)
    img = photo_bg(src) if os.path.exists(src) else placeholder_bg(*ph_colors)
    nameplate(img, name, role, credit)
    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, fname), quality=92)
    print("saved", os.path.join(OUT, fname), "(photo)" if os.path.exists(src) else "(placeholder)")

if __name__ == "__main__":
    card("penelope.jpg", "PENELOPE", "q1  ·  sender of the message", "Anne Hathaway",
         ((109, 58, 160), (24, 10, 48), (232, 221, 199), (150, 120, 90)))
    card("odysseus.jpg", "ODYSSEUS", "q3  ·  receiver", "Matt Damon",
         ((20, 80, 122), (4, 16, 28), (226, 210, 186), (120, 100, 78)))
