#!/usr/bin/env python3
"""Generate raster portrait cards for the two teleportation characters,
Penelope (q1, sender) and Odysseus (q3, receiver), themed to Homer's Odyssey
(evoking the 2026 film). These are original illustrative portraits used as the
default images in the interactive teleportation page and the GIF; drop in
licensed film stills at animations/img/{penelope,odysseus}.jpg to replace them.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

W, H = 480, 600
OUT = os.path.join(os.path.dirname(__file__), "img")
GOLD = (212, 160, 23)

def font(sz, serif=True, bold=True):
    cands = ([
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
        "/System/Library/Fonts/Supplemental/Baskerville.ttc",
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

def gradient(top, bot):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(top, bot, y / H))
    return img

def meander(d, y, color):
    """A simple Greek-key (meander) band across the width at height y."""
    u = 20
    x = 20
    while x + 3 * u < W - 20:
        d.line([(x, y), (x, y - u), (x + u, y - u), (x + u, y - 2 * u),
                (x + 2 * u, y - 2 * u), (x + 2 * u, y)], fill=color, width=3)
        x += 2 * u

def leaf_sprite(color, w=34, h=15):
    s = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(s).ellipse([0, 0, w - 1, h - 1], fill=color + (235,))
    return s

def wreath(img, cx, cy, R, color):
    leaf = leaf_sprite(color)
    # two symmetric branches sweeping up each side of the head
    for side in (-1, +1):
        for k in range(7):
            ang = math.radians(120 - k * 15) * side + math.radians(90)
            x = cx + R * math.cos(ang)
            y = cy - R * math.sin(ang)
            deg = -math.degrees(ang) + (90 if side > 0 else -90)
            rot = leaf.rotate(deg, expand=True)
            img.paste(rot, (int(x - rot.width / 2), int(y - rot.height / 2)), rot)

def silhouette(d, skin, shadow):
    cx, cy, r = W // 2, 250, 96
    d.ellipse([cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4], fill=shadow)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=skin)          # head
    # neck + shoulders
    d.rectangle([cx - 26, cy + r - 20, cx + 26, cy + r + 26], fill=skin)
    d.pieslice([cx - 150, cy + r + 6, cx + 150, cy + r + 320], 180, 360, fill=skin)
    d.pieslice([cx - 150, cy + r - 6, cx + 150, cy + r + 300], 180, 360, fill=shadow, outline=None)
    d.pieslice([cx - 138, cy + r + 12, cx + 138, cy + r + 300], 180, 360, fill=skin)

def card(name, role, actor, top, bot, skin, shadow, fname):
    img = gradient(top, bot)
    d = ImageDraw.Draw(img, "RGBA")
    # decorative frame
    d.rectangle([10, 10, W - 11, H - 11], outline=GOLD, width=3)
    d.rectangle([18, 18, W - 19, H - 19], outline=(GOLD[0], GOLD[1], GOLD[2], 120), width=1)
    meander(d, 60, (GOLD[0], GOLD[1], GOLD[2], 200))
    silhouette(d, skin, shadow)
    wreath(img, W // 2, 250, 150, GOLD)
    d = ImageDraw.Draw(img, "RGBA")
    # bottom nameplate
    d.rectangle([0, H - 150, W, H - 30], fill=(0, 0, 0, 150))
    d.line([(30, H - 150), (W - 30, H - 150)], fill=GOLD, width=2)
    def ctext(y, s, fnt, fill):
        w = d.textlength(s, font=fnt)
        d.text(((W - w) / 2, y), s, font=fnt, fill=fill)
    ctext(H - 138, name, font(54), (255, 255, 255))
    ctext(H - 78, role, font(22, serif=False), (230, 230, 235))
    ctext(H - 52, f"THE ODYSSEY (2026) · {actor}", font(15, serif=False), GOLD)
    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, fname), quality=92)
    print("saved", os.path.join(OUT, fname))

if __name__ == "__main__":
    card("PENELOPE", "q1  ·  sender of the message", "Anne Hathaway",
         (109, 58, 160), (24, 10, 48), (232, 221, 199), (150, 120, 90), "penelope.jpg")
    card("ODYSSEUS", "q3  ·  receiver", "Matt Damon",
         (20, 80, 122), (4, 16, 28), (226, 210, 186), (120, 100, 78), "odysseus.jpg")
