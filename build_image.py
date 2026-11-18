#!/usr/bin/env python3
"""Build entry.png: a one-page world-news infographic for 18 November 2026.

Draws everything with PIL (no photos, no downloaded art). Deterministic:
same input always produces the same PNG bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 245, 239)
NAVY = (16, 35, 63)
RED = (178, 34, 34)
INK = (24, 24, 24)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)
BORDER = (200, 196, 188)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(d, cx, cy, r, color, width=3):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=color, width=width)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=width)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          200, 340, fill=color, width=width)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          20, 160, fill=color, width=width)


def draw_bridge(d, x, y, s, color):
    # two towers, deck, suspension arc
    d.line([x + 6, y + s - 4, x + s - 6, y + s - 4], fill=color, width=4)
    d.line([x + 12, y + 8, x + 12, y + s - 4], fill=color, width=4)
    d.line([x + s - 12, y + 8, x + s - 12, y + s - 4], fill=color, width=4)
    d.arc([x + 12, y + 2, x + s - 12, y + s - 8], 180, 360, fill=color, width=3)
    d.line([x + 12, y + 8, x + s // 2, y + 26], fill=color, width=2)
    d.line([x + s - 12, y + 8, x + s // 2, y + 26], fill=color, width=2)


def draw_radar(d, x, y, s, color):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
              outline=color, width=2)
    d.line([cx, cy, cx + r - 2, cy - r + 8], fill=color, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=color)


def draw_chip(d, x, y, s, color):
    m = 10
    d.rectangle([x + m, y + m, x + s - m, y + s - m], outline=color, width=4)
    d.rectangle([x + m + 8, y + m + 8, x + s - m - 8, y + s - m - 8],
                outline=color, width=2)
    for i in range(3):
        px = x + m + 8 + i * (s - 2 * m - 16) // 2
        d.line([px, y + 2, px, y + m], fill=color, width=3)
        d.line([px, y + s - m, px, y + s - 2], fill=color, width=3)
        py = y + m + 8 + i * (s - 2 * m - 16) // 2
        d.line([x + 2, py, x + m, py], fill=color, width=3)
        d.line([x + s - m, py, x + s - 2, py], fill=color, width=3)


def draw_cyclone(d, x, y, s, color):
    cx, cy = x + s // 2, y + s // 2
    for i, r in enumerate((26, 19, 12)):
        d.arc([cx - r, cy - r, cx + r, cy + r], 40 + i * 60, 300 + i * 60,
              fill=color, width=4)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=color)


def draw_virus(d, x, y, s, color):
    cx, cy, r = x + s // 2, y + s // 2, 16
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        x1, y1 = cx + int(r * math.cos(a)), cy + int(r * math.sin(a))
        x2, y2 = cx + int((r + 9) * math.cos(a)), cy + int((r + 9) * math.sin(a))
        d.line([x1, y1, x2, y2], fill=color, width=3)
        d.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], outline=color, width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.ellipse([cx - 6, cy - 5, cx - 1, cy], fill=color)
    d.ellipse([cx + 2, cy + 2, cx + 7, cy + 7], fill=color)


def draw_flags(d, x, y, s, color):
    # two small flags on poles (diplomacy)
    d.line([x + 14, y + 8, x + 14, y + s - 6], fill=color, width=3)
    d.line([x + s - 14, y + 8, x + s - 14, y + s - 6], fill=color, width=3)
    d.polygon([(x + 14, y + 8), (x + 34, y + 13), (x + 14, y + 19)],
              fill=color)
    d.polygon([(x + s - 14, y + 8), (x + s - 34, y + 13), (x + s - 14, y + 19)],
              fill=color)


STORIES = [
    ("EUROPE  •  WAR", (178, 34, 34),
     "Ukraine hits Crimean Bridge again",
     "Kyiv strikes the bridge for a second day as Russia hits bridges in Kyiv.",
     draw_bridge),
    ("MIDDLE EAST", (146, 90, 16),
     "Iran drones target US radar in Bahrain",
     "US says the drones were intercepted; US jets hit a missile site on Qeshm Island.",
     draw_radar),
    ("ASIA  •  DIPLOMACY", (16, 90, 140),
     "Trump lands in Manila for Quad talks",
     "US president joins Quad leaders before a planned visit to China.",
     draw_flags),
    ("TECH  •  BUSINESS", (24, 110, 70),
     "Nvidia sales double to $115.8bn",
     "Board rules out bringing back ex-CEO Jensen Huang after a record quarter.",
     draw_chip),
    ("WEATHER  •  ASIA", (10, 110, 140),
     "Cyclone Akvan gains strength",
     "Storm over the Bay of Bengal is set to become severe by 19 November.",
     draw_cyclone),
    ("HEALTH  •  USA", (110, 40, 120),
     "US loses measles-free status",
     "PAHO ends the 26-year status after 5,412 cases in 2026, the most since 1991.",
     draw_virus),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([0, 0, W, 132], fill=NAVY)
    d.rectangle([0, 132, W, 138], fill=RED)
    f_title = font(FONT_B, 52)
    f_date = font(FONT_B, 32)
    d.text((32, 16), "WORLD NEWS", font=f_title, fill=WHITE)
    d.text((32, 80), "WEDNESDAY, 18 NOVEMBER 2026", font=f_date, fill=(255, 214, 90))
    draw_globe(d, 940, 66, 42, (255, 214, 90), width=4)

    # Grid of story panels: 2 columns x 3 rows
    f_tag = font(FONT_B, 18)
    f_head = font(FONT_B, 28)
    f_sum = font(FONT_R, 21)
    px, py = 16, 156
    pw, ph, gut = 488, 256, 16
    for i, (tag, color, head, summ, icon) in enumerate(STORIES):
        x = px + (i % 2) * (pw + gut)
        y = py + (i // 2) * (ph + gut)
        d.rectangle([x, y, x + pw, y + ph], fill=PANEL, outline=BORDER, width=2)
        d.rectangle([x, y, x + pw, y + 10], fill=color)
        d.text((x + 20, y + 24), tag, font=f_tag, fill=color)
        icon(d, x + pw - 84, y + 22, 64, color)
        lines = wrap(d, head, f_head, pw - 40 - 84)
        ty = y + 58
        for line in lines[:2]:
            d.text((x + 20, ty), line, font=f_head, fill=INK)
            ty += 35
        d.line([x + 20, ty + 2, x + 90, ty + 2], fill=color, width=3)
        slines = wrap(d, summ, f_sum, pw - 40)
        sy = y + 58 + 35 * min(len(lines), 2) + 18
        for line in slines[:3]:
            d.text((x + 20, sy), line, font=f_sum, fill=GREY)
            sy += 28

    # Footer
    f_foot = font(FONT_R, 18)
    foot = "Sources: Reuters, AP, The Guardian, PAHO, Nvidia, IMD  •  18 November 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 972), foot, font=f_foot, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
