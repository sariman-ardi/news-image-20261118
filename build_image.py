"""Draw the 18 November 2026 world-news poster, round 4: 52 stories,
7 regions, 16 flat illustrations drawn with Pillow, a UTC timeline,
a numbered world map and a date check. Pure Pillow, deterministic."""

import os
from collections import Counter

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (247, 244, 236)
NAVY = (14, 42, 71)
NAVY_DK = (9, 30, 52)
RED = (178, 35, 42)
GOLD = (201, 162, 39)
INK = (22, 22, 22)
GREY = (96, 96, 96)
GREY_LT = (226, 224, 216)
RULE = (196, 192, 180)
CARD = (255, 255, 255)
SKY = (186, 214, 235)

REGION_COLORS = {
    "ASIA": (123, 75, 166),
    "EUROPE": (43, 108, 176),
    "AMERICAS": (46, 125, 50),
    "MIDDLE EAST": (178, 35, 42),
    "GLOBAL": (90, 107, 122),
    "AFRICA": (197, 106, 26),
    "OCEANIA": (15, 118, 110),
}

# (num, region, field, kicker tag, headline, deck, source, lon, lat)
# lon/lat are approximate, for the map pins and dots.
STORIES = [
    (1, "MIDDLE EAST", "War & security", "CLAIM",
     "Iran says it fired on a US base in Kuwait",
     "Bahrain reports new attacks; Kuwait says its defences engaged \u201chostile drones\u201d.",
     "REUTERS", 48.0, 29.0),
    (2, "ASIA", "Diplomacy", "CONFIRMED \u00b7 AP",
     "Xi greets Trump on the tarmac in Shenzhen",
     "A rare airport welcome, and a hug, from China\u2019s leader; three-way talks Thursday.",
     "REUTERS \u00b7 DW", 114.0, 22.5),
    (3, "EUROPE", "War & security", "OFFICIALS \u00b7 KYIV",
     "Russian strikes kill four; 141 drones fired",
     "126 downed; hits at seven sites. Four die in Odesa\u2019s historic centre.",
     "KYIV AIR FORCE", 30.5, 46.5),
    (4, "GLOBAL", "Science & health", "CONFIRMED \u00b7 NASA",
     "Voyager 1 is one light-day from Earth",
     "At 10:16 UTC the 1977 probe passed 25.9bn km away; a first for a human-made object.",
     "NASA", -150.0, 12.0),
    (5, "EUROPE", "Economy & markets", "",
     "EU offers Kyiv a \u20ac45bn loan for 2027",
     "Fills two-thirds of a \u20ac70bn gap; repaid if Russia pays.",
     "REUTERS", 23.0, 50.0),
    (6, "AMERICAS", "Economy & markets", "",
     "Fed minutes: nearly all officials see more hikes",
     "A bigger December rise is floated; Dow \u22121.1%, down 561.",
     "FED \u00b7 AP", -77.0, 39.0),
    (7, "ASIA", "Climate & disasters", "",
     "Cyclone Akvan turns toward India\u2019s east coast",
     "Landfall is forecast Friday; evacuations begin.",
     "IMD", 82.0, 17.0),
    (8, "MIDDLE EAST", "War & security", "",
     "Israeli tanks push into central Gaza",
     "The army cites a tunnel; three are killed.",
     "REUTERS", 34.5, 31.5),
    (9, "AMERICAS", "Politics & courts", "",
     "Jeffries wins Democrats\u2019 nod for Speaker, 251\u201311",
     "First Black Speaker; the full House votes on 3 January.",
     "NPR \u00b7 CBS", -77.0, 39.0),
    (10, "GLOBAL", "Culture & sport", "",
     "GTA VI goes on sale after a 13-year wait",
     "Midnight launch starts in New Zealand; 16m pre-sold.",
     "ANADOLU", 172.0, -41.0),
    (11, "AFRICA", "War & security", "",
     "Amnesty: RSF drones killed 37 in El Obeid",
     "Nine strikes, June to August; it urges a war-crimes inquiry; RSF blames the army.",
     "AMNESTY", 30.5, 13.2),
    (12, "EUROPE", "Economy & markets", "",
     "UK inflation climbs to 3.6%, a one-year high",
     "Fuel and tobacco taxes push October CPI up from 3.5%.",
     "ONS", -0.1, 51.5),
    (13, "GLOBAL", "Climate & disasters", "",
     "COP31 still split over a fossil-fuel phase-out",
     "Arab states and Russia reject the draft text; a Friday deadline looms.",
     "AFP \u00b7 AGENCIES", 30.7, 36.9),
    (14, "ASIA", "Labour & society", "",
     "Bangladesh wage protests shut 55 garment factories",
     "Workers block a highway; about 300 arrests, police say.",
     "DAILY STAR", 90.4, 23.8),
    (15, "AFRICA", "War & security", "",
     "Ethiopia and Eritrea mass troops at their border",
     "Within striking distance, monitors say; Eritrea denies it.",
     "REUTERS", 39.0, 15.0),
    (16, "AMERICAS", "Business & tech", "",
     "Anthropic prices the biggest IPO ever: $83 a share",
     "$81.3bn raised, above its range; trading starts on Thursday.",
     "BLOOMBERG", -74.0, 40.7),
]

BRIEFS = [
    (17, "OCEANIA", "Sydney: Tame Impala sweeps ARIAs"),
    (18, "EUROPE", "Turin: Alcaraz beats Medvedev at Finals"),
    (19, "ASIA", "Manila: Trump hails \u2018biggest\u2019 trade deal"),
    (20, "ASIA", "Tokyo: Takaichi\u2019s first China visit as PM"),
    (21, "ASIA", "Seoul: Lee seeks Xi\u2019s help on N. Korea"),
    (22, "AMERICAS", "Ottawa: Carney and Xi agree tariff relief"),
    (23, "MIDDLE EAST", "Riyadh: coalition downed a Houthi missile"),
    (24, "MIDDLE EAST", "Hormuz: Iran says it downed a US MQ-9"),
    (25, "EUROPE", "Berlin: air defences, F-16s pledged to Kyiv"),
    (26, "EUROPE", "Kosovo: ex-president Thaci gets 17 months"),
    (27, "EUROPE", "London: US Army spy suspect handed to US"),
    (28, "EUROPE", "Stockholm: Europe off track on superbugs"),
    (29, "AFRICA", "DR Congo: WHO keeps Ebola emergency"),
    (30, "EUROPE", "Kemerovo: 19 die as an An-12 crashes"),
    (31, "AFRICA", "Guinea: 224 jailed over illegal gold mining"),
    (32, "AFRICA", "Senegal: migrant boat capsizes off coast"),
    (33, "AFRICA", "Mauritius: Chagos deadline set for UK"),
    (34, "AFRICA", "Maputo: Mondlane goes on trial"),
    (35, "AMERICAS", "Bogot\u00e1: economy shrinks 0.8% in Q3"),
    (36, "AMERICAS", "Bras\u00edlia: Senate passes Lula\u2019s $10bn plan"),
    (37, "AMERICAS", "Mexico: US trade talks \u2018very far along\u2019"),
    (38, "AMERICAS", "Peru: Tumbes River passes red-alert level"),
    (39, "AMERICAS", "Washington: NSA network struck after patch"),
    (40, "AMERICAS", "Haiti: troops raze a gang chief\u2019s home"),
    (41, "AMERICAS", "Caracas: Hegseth visit seals defence pact"),
    (42, "GLOBAL", "FIFA: Diallo to challenge Infantino"),
    (43, "EUROPE", "Bucharest: magnitude 5.3 quake shakes city"),
    (44, "OCEANIA", "PNG: magnitude 6.0 quake shakes capital"),
    (45, "OCEANIA", "Cook Islands: Cyclone Xavier hits Cat 5"),
    (46, "GLOBAL", "The Hague: ICJ sets Rohingya ruling"),
    (47, "GLOBAL", "Gold: lowest price in more than a year"),
    (48, "GLOBAL", "Oil: Brent settles 1.3% lower at $91.95"),
    (49, "AMERICAS", "Wall St: Nvidia falls 2.9%; AMD up 5.3%"),
    (50, "GLOBAL", "Tech: Microsoft to use Intel chip packaging"),
    (51, "ASIA", "Kashmir: Indian forces kill a militant chief"),
    (52, "GLOBAL", "Pew: Islam set to be largest religion by 2035"),
]
BRIEF_FIELDS = {
    17: "Culture & sport", 18: "Culture & sport", 19: "Diplomacy",
    20: "Diplomacy", 21: "Diplomacy", 22: "Diplomacy", 23: "War & security",
    24: "War & security", 25: "War & security", 26: "Politics & courts",
    27: "Politics & courts", 28: "Science & health", 29: "Science & health",
    30: "Climate & disasters", 31: "Politics & courts",
    32: "Climate & disasters", 33: "Diplomacy", 34: "Politics & courts",
    35: "Economy & markets", 36: "Economy & markets", 37: "Diplomacy",
    38: "Climate & disasters", 39: "War & security", 40: "War & security",
    41: "Diplomacy", 42: "Culture & sport", 43: "Climate & disasters",
    44: "Climate & disasters", 45: "Climate & disasters",
    46: "Politics & courts", 47: "Economy & markets",
    48: "Economy & markets", 49: "Economy & markets",
    50: "Business & tech", 51: "War & security", 52: "Labour & society",
}

TIMELINE = [
    ("OVERNIGHT", "Drones over Kuwait, Bahrain and Ukraine"),
    ("07:00 UTC", "UK inflation: 3.6%"),
    ("MORNING", "Xi greets Trump in Shenzhen"),
    ("10:16 UTC", "Voyager 1: one light-day"),
    ("11:00 UTC", "GTA VI unlocks in New Zealand"),
    ("AFTERNOON", "EU offers Kyiv \u20ac45bn"),
    ("19:00 UTC", "Fed minutes: more hikes"),
    ("21:00 UTC", "Wall Street: Dow closes down 561"),
]

NUMBERS = [
    ("141", "drones fired"),
    ("\u20ac45bn", "EU loan for Kyiv"),
    ("25.9bn km", "Voyager 1 from Earth"),
    ("$81.3bn", "record IPO"),
    ("\u22121.1%", "Dow after Fed minutes"),
    ("$3,746", "gold, a 14-month low"),
]

DATE_CHECK = (
    "Left out, as first reported on Tuesday 17 November: Nvidia\u2019s results \u00b7 "
    "the Alaska Senate call \u00b7 the US strike on Qeshm \u00b7 the Knesset speaker vote \u00b7 the Kerch Bridge "
    "collapse. Not yet news on Wednesday: the Trump\u2013Xi\u2013Putin summit (Thu 19 Nov) \u00b7 Cyclone Akvan\u2019s "
    "landfall (Fri 20 Nov). Claims are attributed to whoever made them."
)

FOOT_SOURCES = ("Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 DW \u00b7 Al Jazeera \u00b7 NPR \u00b7 CBS \u00b7 Fed \u00b7 "
                "ONS \u00b7 IMD \u00b7 NASA \u00b7 Amnesty \u00b7 WHO \u00b7 Bloomberg \u00b7 ATP \u00b7 AAP \u00b7 "
                "Daily Star \u2014 Original drawings.")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, fnt, width):
    """Shorten text with an ellipsis until it fits the width."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "\u2026", font=fnt) > width:
        text = text[:-1]
    return text + "\u2026"


def wrap(draw, text, fnt, width, max_lines=None):
    """Word-wrap text to the width; returns a list of lines."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = fit(draw, lines[-1], fnt, width)
    return lines


# ---------------------------------------------------------------- illustrations
# Every illustration is flat vector-style drawing, drawn into a box
# (x, y, w, h). Bold shapes, few colours, readable at half size.

def illo_gulf(draw, x, y, w, h):
    """Stylised Gulf map: Iran top right, Kuwait/Bahrain, dashed drone paths."""
    draw.rectangle([x, y, x + w, y + h], fill=(223, 232, 238))
    # land masses
    draw.polygon([(x + 8, y + 8), (x + w - 8, y + 6), (x + w - 14, y + h * 0.42),
                  (x + w * 0.55, y + h * 0.55), (x + 10, y + h * 0.5)], fill=(232, 220, 180))
    draw.polygon([(x + 6, y + h * 0.55), (x + w * 0.5, y + h * 0.5),
                  (x + w * 0.62, y + h - 8), (x + 8, y + h - 6)], fill=(222, 208, 164))
    # the gulf water
    draw.polygon([(x + w * 0.42, y + h * 0.42), (x + w * 0.78, y + h * 0.30),
                  (x + w * 0.86, y + h * 0.62), (x + w * 0.60, y + h * 0.72)],
                 fill=(96, 148, 188))
    # dashed drone paths (red)
    for (x1, y1, x2, y2) in [(0.80, 0.18, 0.52, 0.55), (0.72, 0.12, 0.46, 0.48),
                             (0.86, 0.30, 0.58, 0.60)]:
        px1, py1 = x + w * x1, y + h * y1
        px2, py2 = x + w * x2, y + h * y2
        steps = 9
        for i in range(steps):
            if i % 2:
                continue
            t1, t2 = i / steps, (i + 0.8) / steps
            draw.line([px1 + (px2 - px1) * t1, py1 + (py2 - py1) * t1,
                       px1 + (px2 - px1) * t2, py1 + (py2 - py1) * t2],
                      fill=RED, width=2)
        draw.polygon([(px2, py2), (px2 - 7, py2 - 2), (px2 - 7, py2 + 2)], fill=RED)
    # labels, kept clear of the dashed drone paths (which run top-right
    # to centre): the two place names sit on the land, left of the Gulf
    f = font(SANS_B, 11)
    draw.text((x + w * 0.66, y + 6), "IRAN", font=f, fill=INK)
    draw.text((x + w * 0.06, y + h * 0.46), "KUWAIT", font=f, fill=RED)
    draw.text((x + w * 0.06, y + h * 0.60), "BAHRAIN", font=f, fill=RED)
    draw.text((x + 8, y + h - 16), "SAUDI ARABIA", font=font(SANS_B, 8), fill=GREY)
    draw.text((x + w * 0.60, y + h * 0.40), "THE GULF", font=font(SANS_B, 8),
              fill=(255, 255, 255))


def illo_plane(draw, x, y, w, h):
    """Airliner on the tarmac, Shenzhen skyline, sun, three flags."""
    draw.rectangle([x, y, x + w, y + h], fill=(250, 226, 178))
    draw.ellipse([x + w * 0.78, y + 6, x + w * 0.92, y + 20], fill=(245, 166, 52))
    # skyline
    for bx, bw, bh in [(0.02, 0.10, 0.42), (0.14, 0.08, 0.55), (0.24, 0.12, 0.38),
                       (0.38, 0.07, 0.62), (0.47, 0.10, 0.45), (0.60, 0.08, 0.58),
                       (0.70, 0.12, 0.40), (0.84, 0.09, 0.50)]:
        draw.rectangle([x + w * bx, y + h - 14 - h * bh, x + w * (bx + bw),
                        y + h - 14], fill=(120, 110, 96))
    # runway
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=(90, 90, 96))
    for i in range(6):
        draw.rectangle([x + 8 + i * 38, y + h - 8, x + 30 + i * 38, y + h - 5],
                       fill=(255, 255, 255))
    # plane: fuselage, wing, tail, windows
    py = y + h * 0.42
    draw.ellipse([x + w * 0.06, py - 9, x + w * 0.94, py + 9], fill=(240, 244, 248))
    draw.polygon([(x + w * 0.88, py - 6), (x + w * 0.99, py - 26),
                  (x + w * 0.99, py - 4)], fill=(60, 90, 130))
    draw.polygon([(x + w * 0.45, py + 4), (x + w * 0.62, py + 26),
                  (x + w * 0.70, py + 4)], fill=(60, 90, 130))
    draw.polygon([(x + w * 0.06, py - 4), (x + w * 0.02, py - 18),
                  (x + w * 0.10, py - 4)], fill=(60, 90, 130))
    for i in range(9):
        draw.ellipse([x + w * (0.14 + i * 0.075), py - 3,
                      x + w * (0.14 + i * 0.075) + 4, py + 1], fill=NAVY)
    # red carpet + flags
    draw.rectangle([x + w * 0.30, y + h - 26, x + w * 0.72, y + h - 14], fill=RED)
    for fx, col in [(0.34, (222, 41, 16)), (0.50, (60, 90, 160)), (0.66, (200, 200, 200))]:
        draw.rectangle([x + w * fx, y + h - 52, x + w * fx + 16, y + h - 38], fill=col)
        draw.line([x + w * fx + 2, y + h - 52, x + w * fx + 2, y + h - 26],
                  fill=INK, width=2)


def illo_drones_night(draw, x, y, w, h):
    """Night sky, drone silhouettes, explosions, big numbers."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 46))
    for sx, sy in [(0.08, 0.12), (0.3, 0.08), (0.55, 0.15), (0.8, 0.07), (0.92, 0.2)]:
        draw.ellipse([x + w * sx, y + h * sy, x + w * sx + 3, y + h * sy + 3],
                     fill=(255, 255, 255))
    # explosions
    for ex, ey, r in [(0.22, 0.55, 14), (0.62, 0.38, 18), (0.85, 0.62, 12)]:
        cx, cy = x + w * ex, y + h * ey
        for a in range(8):
            import math
            ang = a * math.pi / 4
            draw.line([cx, cy, cx + r * math.cos(ang), cy + r * math.sin(ang)],
                      fill=(245, 166, 52), width=3)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 214, 90))
    # drones: small quadcopter silhouettes
    for dx, dy in [(0.35, 0.30), (0.55, 0.55), (0.78, 0.28)]:
        cx, cy = x + w * dx, y + h * dy
        draw.rectangle([cx - 8, cy - 3, cx + 8, cy + 3], fill=(220, 220, 220))
        draw.line([cx - 12, cy - 6, cx + 12, cy - 6], fill=(220, 220, 220), width=2)
        draw.line([cx - 12, cy + 6, cx + 12, cy + 6], fill=(220, 220, 220), width=2)
    # dashed flight paths
    for (x1, y1, x2, y2) in [(0.05, 0.75, 0.35, 0.32), (0.95, 0.80, 0.60, 0.55)]:
        px1, py1 = x + w * x1, y + h * y1
        px2, py2 = x + w * x2, y + h * y2
        steps = 10
        for i in range(steps):
            if i % 2:
                continue
            t1, t2 = i / steps, (i + 0.8) / steps
            draw.line([px1 + (px2 - px1) * t1, py1 + (py2 - py1) * t1,
                       px1 + (px2 - px1) * t2, py1 + (py2 - py1) * t2],
                      fill=(245, 166, 52), width=2)
    f = font(SANS_B, 15)
    draw.text((x + 8, y + 6), "141 FIRED", font=f, fill=(255, 255, 255))
    draw.text((x + 8, y + 26), "126 DOWNED", font=f, fill=(255, 214, 90))


def illo_voyager(draw, x, y, w, h):
    """Deep space: Earth, Voyager probe, dashed signal line."""
    draw.rectangle([x, y, x + w, y + h], fill=(10, 14, 34))
    for sx, sy in [(0.05, 0.1), (0.2, 0.25), (0.45, 0.08), (0.65, 0.2), (0.85, 0.12),
                   (0.1, 0.7), (0.35, 0.85), (0.7, 0.75), (0.92, 0.55)]:
        draw.ellipse([x + w * sx, y + h * sy, x + w * sx + 2, y + h * sy + 2],
                     fill=(255, 255, 255))
    # Earth
    ex, ey, er = x + w * 0.14, y + h * 0.62, 20
    draw.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(58, 130, 200))
    draw.ellipse([ex - 12, ey - 8, ex - 2, ey + 2], fill=(80, 170, 90))
    draw.ellipse([ex + 2, ey + 4, ex + 12, ey + 12], fill=(80, 170, 90))
    draw.text((ex - 14, ey + er + 2), "EARTH", font=font(SANS_B, 8), fill=(255, 255, 255))
    # dashed signal line Earth -> Voyager
    vx, vy = x + w * 0.86, y + h * 0.28
    steps = 14
    for i in range(steps):
        if i % 2:
            continue
        t1, t2 = i / steps, (i + 0.8) / steps
        draw.line([ex + (vx - ex) * t1, ey + (vy - ey) * t1,
                   ex + (vx - ex) * t2, ey + (vy - ey) * t2],
                  fill=(245, 200, 80), width=2)
    # Voyager probe: dish + boom + gold body
    draw.ellipse([vx - 16, vy - 16, vx + 16, vy + 2], outline=(220, 220, 220), width=2)
    draw.line([vx, vy - 2, vx - 26, vy + 18], fill=(220, 220, 220), width=2)
    draw.rectangle([vx - 4, vy + 2, vx + 8, vy + 12], fill=(212, 175, 55))
    draw.line([vx + 8, vy + 7, vx + 24, vy - 2], fill=(220, 220, 220), width=2)
    f = font(SANS_B, 17)
    draw.text((x + w * 0.30, y + 8), "1 LIGHT-DAY", font=f, fill=(255, 214, 90))
    draw.text((x + w * 0.30, y + 30), "25.9 billion km from Earth",
              font=font(SANS, 10), fill=(255, 255, 255))


def illo_eu_loan(draw, x, y, w, h):
    """EU flag, euro figure, arrow to Ukraine's blue-yellow flag."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 238, 244))
    # EU flag, top left
    fx, fy, fw, fh = x + 8, y + 8, 46, 26
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(0, 51, 153))
    import math
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        sx, sy = fx + fw / 2 + 15 * math.cos(ang), fy + fh / 2 + 8 * math.sin(ang)
        draw.polygon([(sx, sy - 2), (sx + 1, sy - 1), (sx + 2, sy),
                      (sx + 1, sy + 1), (sx, sy + 2), (sx - 1, sy + 1),
                      (sx - 2, sy), (sx - 1, sy - 1)], fill=(255, 209, 0))
    # figure, right of the flag
    draw.text((x + 60, y + 10), "\u20ac45bn", font=font(SANS_B, 20), fill=NAVY)
    # arrow to Ukraine flag, bottom right
    draw.line([x + 60, y + 46, x + 100, y + 46], fill=NAVY, width=3)
    draw.polygon([(x + 100, y + 46), (x + 92, y + 40), (x + 92, y + 52)], fill=NAVY)
    ux, uy = x + w - 46, y + 36
    draw.rectangle([ux, uy, ux + 38, uy + 10], fill=(0, 91, 187))
    draw.rectangle([ux, uy + 10, ux + 38, uy + 20], fill=(255, 213, 0))


def illo_fed(draw, x, y, w, h):
    """Columned Fed building, red falling chart. No text inside."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 236, 228))
    # building, left
    bx, by = x + 10, y + 8
    draw.polygon([(bx, by + 12), (bx + 22, by), (bx + 44, by + 12)],
                 fill=(150, 148, 138))
    for i in range(4):
        draw.rectangle([bx + 3 + i * 11, by + 14, bx + 10 + i * 11, by + 34],
                       fill=(190, 186, 174))
    draw.rectangle([bx, by + 34, bx + 44, by + 40], fill=(150, 148, 138))
    # falling chart, right
    pts = [(x + 72, y + 12), (x + 86, y + 8), (x + 100, y + 20),
           (x + 114, y + 16), (x + 132, y + 32)]
    draw.line(pts, fill=RED, width=3)
    draw.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 8, pts[-1][1] - 2),
                  (pts[-1][0] - 2, pts[-1][1] + 8)], fill=RED)


def illo_cyclone(draw, x, y, w, h):
    """India coast outline, spiral cyclone, landfall arrow."""
    draw.rectangle([x, y, x + w, y + h], fill=(196, 224, 232))
    # India-ish triangle
    draw.polygon([(x + 48, y + 6), (x + 96, y + 6),
                  (x + 88, y + 34), (x + 66, y + 54),
                  (x + 50, y + 30)], fill=(222, 208, 164))
    draw.text((x + 6, y + 6), "INDIA", font=font(SANS_B, 9), fill=GREY)
    # spiral, kept small so it never touches a label
    import math
    cx, cy = x + 118, y + 34
    pts = []
    for t in range(0, 540, 12):
        a = math.radians(t)
        r = 3 + t / 540 * 13
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.line(pts, fill=(30, 90, 140), width=3)
    # short arrow toward the coast
    draw.line([cx - 18, cy - 4, x + 92, y + 30], fill=RED, width=2)
    draw.polygon([(x + 92, y + 30), (x + 100, y + 28), (x + 94, y + 38)], fill=RED)


def illo_gaza(draw, x, y, w, h):
    """Map strip: sea, yellow line, Nuseirat, tank silhouette."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 200))
    # sea
    draw.polygon([(x, y), (x + w * 0.28, y), (x + w * 0.22, y + h),
                  (x, y + h)], fill=(150, 190, 214))
    draw.text((x + 6, y + h * 0.45), "SEA", font=font(SANS_B, 9), fill=(255, 255, 255))
    # yellow line (dashed), no label: the story text below names it
    lx = x + w * 0.55
    for i in range(8):
        y1 = y + 4 + i * (h - 8) / 8
        y2 = y + 4 + (i + 0.55) * (h - 8) / 8
        draw.line([lx, y1, lx, y2], fill=(230, 190, 20), width=4)
    # tank
    tx, ty = x + w * 0.62, y + h * 0.62
    draw.rectangle([tx, ty, tx + 34, ty + 10], fill=(90, 96, 70))
    draw.rectangle([tx + 6, ty - 8, tx + 22, ty], fill=(90, 96, 70))
    draw.line([tx + 22, ty - 4, tx + 40, ty - 8], fill=(60, 64, 46), width=3)
    for i in range(4):
        draw.ellipse([tx + 3 + i * 8, ty + 10, tx + 9 + i * 8, ty + 16], fill=(60, 64, 46))


def illo_jeffries(draw, x, y, w, h):
    """Capitol dome and a ballot box with a green check. No text inside."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 236, 240))
    # dome, left of centre
    dx, dy = x + 62, y + 26
    draw.pieslice([dx - 22, dy - 22, dx + 22, dy + 4], 180, 360, fill=(240, 240, 238))
    draw.rectangle([dx - 25, dy + 2, dx + 25, dy + 9], fill=(220, 220, 216))
    for i in range(5):
        draw.rectangle([dx - 23 + i * 10, dy + 11, dx - 16 + i * 10, dy + 26],
                       fill=(220, 220, 216))
    draw.rectangle([dx - 27, dy + 26, dx + 27, dy + 31], fill=(200, 200, 194))
    draw.line([dx, dy - 22, dx, dy - 30], fill=INK, width=2)
    # ballot box + check, top right
    bx, by = x + w - 44, y + 8
    draw.rectangle([bx, by, bx + 36, by + 26], fill=(255, 255, 255),
                   outline=NAVY, width=2)
    draw.line([bx + 8, by + 14, bx + 15, by + 21], fill=(30, 120, 60), width=3)
    draw.line([bx + 15, by + 21, bx + 29, by + 6], fill=(30, 120, 60), width=3)


def illo_gta(draw, x, y, w, h):
    """Purple panel, game controller. The headline below names the game."""
    draw.rectangle([x, y, x + w, y + h], fill=(88, 40, 140))
    # controller
    cx, cy = x + w * 0.5, y + h * 0.5
    draw.rounded_rectangle([cx - 52, cy - 20, cx + 52, cy + 20], radius=16,
                           fill=(240, 240, 244))
    draw.ellipse([cx - 40, cy - 8, cx - 26, cy + 6], fill=(88, 40, 140))
    draw.ellipse([cx + 26, cy - 8, cx + 40, cy + 6], fill=(88, 40, 140))
    for dx, dy, col in [(-32, -2, (220, 60, 60)), (32, -2, (60, 160, 80)),
                        (-32, 8, (60, 110, 220)), (32, 8, (230, 200, 40))]:
        draw.ellipse([cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4], fill=col)


def illo_sudan(draw, x, y, w, h):
    """Desert town, drone overhead, big 37 KILLED."""
    draw.rectangle([x, y, x + w, y + h], fill=(244, 222, 178))
    draw.ellipse([x + w * 0.82, y + 6, x + w * 0.94, y + 18], fill=(245, 166, 52))
    # town blocks
    for bx, bw, bh in [(0.04, 0.18, 0.30), (0.26, 0.14, 0.42), (0.44, 0.20, 0.34),
                       (0.68, 0.16, 0.46), (0.86, 0.12, 0.30)]:
        draw.rectangle([x + w * bx, y + h - 12 - h * bh, x + w * (bx + bw),
                        y + h - 12], fill=(190, 160, 120))
    draw.rectangle([x, y + h - 12, x + w, y + h], fill=(214, 186, 140))
    # drone, moved right so it never touches the big figure
    dx, dy = x + 108, y + 14
    draw.rectangle([dx - 10, dy - 3, dx + 10, dy + 3], fill=(60, 60, 60))
    draw.line([dx - 15, dy - 7, dx + 15, dy - 7], fill=(60, 60, 60), width=2)
    draw.line([dx - 15, dy + 7, dx + 15, dy + 7], fill=(60, 60, 60), width=2)
    draw.text((x + 8, y + 6), "37 KILLED", font=font(SANS_B, 16), fill=RED)


def illo_uk(draw, x, y, w, h):
    """Rising bar chart, 3.6% in clear space at top left."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 240, 244))
    # bars, all inside the box
    base = y + h - 18
    for i, bh in enumerate([10, 14, 18, 24, 30]):
        bx = x + 12 + i * 26
        draw.rectangle([bx, base - bh, bx + 18, base], fill=NAVY if i < 4 else RED)
    draw.line([x + 8, base, x + w - 8, base], fill=INK, width=2)
    draw.text((x + 8, y + 6), "3.6%", font=font(SANS_B, 20), fill=RED)


def illo_cop31(draw, x, y, w, h):
    """Globe with a leaf, two arrows pulling apart. No text inside."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 238, 226))
    # globe, fully inside the box
    cx, cy, r = x + 48, y + 32, 20
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 200))
    draw.ellipse([cx - 13, cy - 10, cx - 3, cy + 2], fill=(90, 170, 90))
    draw.ellipse([cx + 2, cy + 2, cx + 12, cy + 12], fill=(90, 170, 90))
    # leaf on top of the globe
    draw.ellipse([cx - 5, cy - r - 6, cx + 13, cy - r + 8], fill=(60, 140, 60))
    # split arrows
    ax = x + 96
    draw.line([ax, cy - 6, ax + 34, cy - 22], fill=RED, width=3)
    draw.polygon([(ax + 34, cy - 22), (ax + 26, cy - 24), (ax + 30, cy - 14)], fill=RED)
    draw.line([ax, cy + 6, ax + 34, cy + 22], fill=NAVY, width=3)
    draw.polygon([(ax + 34, cy + 22), (ax + 26, cy + 20), (ax + 30, cy + 12)], fill=NAVY)


def illo_factory(draw, x, y, w, h):
    """Sawtooth factory, chimney, small crowd. One short label, clear of the roof."""
    draw.rectangle([x, y, x + w, y + h], fill=(240, 232, 214))
    # factory, roof peaks below the label
    fx, fy = x + 8, y + 34
    draw.rectangle([fx, fy, fx + w - 16, y + h - 10], fill=(180, 120, 90))
    for i in range(4):
        draw.polygon([(fx + i * 34, fy), (fx + i * 34 + 17, fy - 12),
                      (fx + i * 34 + 34, fy)], fill=(150, 96, 70))
    draw.rectangle([fx + w - 30, fy - 22, fx + w - 20, fy], fill=(120, 110, 100))
    draw.ellipse([fx + w - 32, fy - 32, fx + w - 16, fy - 20], fill=(200, 200, 200))
    # crowd, in front of the factory
    for i in range(5):
        cx = x + 16 + i * 26
        draw.ellipse([cx, y + h - 22, cx + 10, y + h - 12], fill=(60, 60, 90))
        draw.rectangle([cx - 2, y + h - 12, cx + 12, y + h - 4], fill=(60, 60, 90))
    draw.text((x + 8, y + 4), "55 FACTORIES", font=font(SANS_B, 13), fill=RED)


def illo_border(draw, x, y, w, h):
    """Two arrows facing across a border line, mountains behind."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    # mountains
    draw.polygon([(x, y + h - 12), (x + w * 0.3, y + 14), (x + w * 0.55, y + h - 12)],
                 fill=(170, 160, 130))
    draw.polygon([(x + w * 0.4, y + h - 12), (x + w * 0.7, y + 22),
                  (x + w, y + h - 12)], fill=(150, 140, 112))
    # border line
    bx = x + w * 0.5
    for i in range(6):
        y1 = y + 6 + i * (h - 18) / 6
        draw.line([bx, y1, bx, y1 + (h - 18) / 12], fill=RED, width=3)
    # arrows
    draw.line([x + 10, y + h * 0.4, bx - 8, y + h * 0.4], fill=NAVY, width=4)
    draw.polygon([(bx - 8, y + h * 0.4), (bx - 18, y + h * 0.4 - 6),
                  (bx - 18, y + h * 0.4 + 6)], fill=NAVY)
    draw.line([x + w - 10, y + h * 0.6, bx + 8, y + h * 0.6], fill=RED, width=4)
    draw.polygon([(bx + 8, y + h * 0.6), (bx + 18, y + h * 0.6 - 6),
                  (bx + 18, y + h * 0.6 + 6)], fill=RED)


def illo_ipo(draw, x, y, w, h):
    """Rising stock chart, $83 in clear space at top left."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 240, 232))
    pts = [(x + 8, y + 40), (x + 48, y + 34), (x + 80, y + 22),
           (x + 112, y + 28), (x + 148, y + 12)]
    draw.line(pts, fill=(30, 120, 60), width=3)
    draw.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 9, pts[-1][1] - 1),
                  (pts[-1][0] - 2, pts[-1][1] + 9)], fill=(30, 120, 60))
    for px, py in pts:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(30, 120, 60))
    draw.text((x + 8, y + 6), "$83", font=font(SANS_B, 26), fill=NAVY)


ILLOS = {
    1: illo_gulf, 2: illo_plane, 3: illo_drones_night, 4: illo_voyager,
    5: illo_eu_loan, 6: illo_fed, 7: illo_cyclone, 8: illo_gaza,
    9: illo_jeffries, 10: illo_gta, 11: illo_sudan, 12: illo_uk,
    13: illo_cop31, 14: illo_factory, 15: illo_border, 16: illo_ipo,
}


# ---------------------------------------------------------------- layout

LAND = [
    (0, [(10, 20), (36, 58)]),
    (1, [(8, 22), (36, 60)]),
    (2, [(7, 23), (35, 60)]),
    (3, [(8, 22), (24, 26), (31, 34), (36, 58)]),
    (4, [(9, 21), (30, 36), (35, 57)]),
    (5, [(10, 20), (30, 35), (36, 56)]),
    (6, [(11, 19), (31, 34), (38, 54)]),
    (7, [(12, 18), (31, 34), (40, 52)]),
    (8, [(13, 17), (30, 36), (42, 50)]),
    (9, [(15, 18), (30, 37), (44, 50)]),
    (10, [(20, 24), (30, 37), (45, 49)]),
    (11, [(20, 25), (30, 36)]),
    (12, [(20, 26), (31, 35), (49, 52)]),
    (13, [(21, 26), (31, 34)]),
    (14, [(21, 25), (32, 34)]),
    (15, [(22, 25), (32, 34), (46, 50)]),
    (16, [(22, 24), (33, 35), (46, 56)]),
    (17, [(23, 24), (50, 55)]),
    (18, [(23, 24), (43, 43), (51, 54)]),
    (19, [(24, 24), (32, 36), (51, 54)]),
    (20, [(24, 25), (33, 35), (51, 53)]),
    (21, [(25, 25), (34, 34), (52, 53)]),
    (22, [(25, 25), (60, 60)]),
    (23, [(60, 60)]),
]

# Hand-tuned pin positions (map box x 8..308, y 658..798).
PINS = {
    1: (198, 709), 2: (253, 715), 3: (183, 691), 5: (170, 682),
    6: (94, 699), 7: (226, 721), 8: (180, 712), 9: (100, 710),
    10: (301, 766), 11: (183, 725), 12: (158, 686), 13: (194, 698),
    14: (233, 714), 15: (197, 728), 16: (88, 692),
}

# (brief num, lon, lat) for the locatable briefs.
BRIEF_DOTS = [
    (17, 151.2, -33.9), (18, 7.7, 45.1), (19, 121.0, 14.6), (20, 139.7, 35.7),
    (21, 127.0, 37.5), (22, -75.7, 45.4), (23, 46.7, 24.6), (24, 56.5, 27.0),
    (25, 13.4, 52.5), (26, 21.0, 42.6), (27, -0.1, 51.5), (28, 18.0, 59.3),
    (29, 23.0, -2.0), (30, 86.0, 55.4), (31, -13.7, 9.5), (32, -17.4, 14.7),
    (33, 57.5, -20.2), (34, 32.6, -25.9), (35, -74.0, 4.7), (36, -47.9, -15.8),
    (37, -99.1, 19.4), (38, -80.4, -3.6), (39, -77.0, 39.0), (40, -72.3, 18.5),
    (41, -66.9, 10.5), (42, 8.5, 47.4), (43, 26.1, 44.4), (44, 147.1, -9.5),
    (45, -159.8, -21.2), (46, 4.3, 52.1), (49, -74.0, 40.7), (50, -122.1, 47.7),
    (51, 74.8, 34.1),
]


def region_counts():
    c = Counter()
    for s in STORIES:
        c[s[1]] += 1
    for _, r, _ in BRIEFS:
        c[r] += 1
    return c


def field_counts():
    c = Counter()
    for s in STORIES:
        c[s[2]] += 1
    for num, _r, _t in BRIEFS:
        c[BRIEF_FIELDS[num]] += 1
    return c


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 84], fill=NAVY)
    draw.rectangle([0, 84, W, 87], fill=GOLD)
    # date block
    draw.rectangle([8, 8, 84, 76], fill=RED)
    draw.text((46, 10), "NOV", font=font(SANS_B, 13), fill=(255, 255, 255), anchor="ma")
    draw.text((46, 26), "18", font=font(SANS_B, 36), fill=(255, 255, 255), anchor="ma")
    draw.text((46, 64), "WED \u00b7 2026", font=font(SANS_B, 9), fill=(255, 255, 255),
              anchor="ma")
    draw.text((96, 12), "Wednesday 18 November 2026", font=font(SERIF_B, 36),
              fill=(255, 255, 255))
    draw.text((W - 8, 12), "52 STORIES \u00b7 7 REGIONS \u00b7 16 DRAWN \u00b7 ONE PAGE",
              font=font(SANS_B, 10), fill=(232, 196, 90), anchor="ra")
    draw.text((96, 60),
              "Everything on this page happened, or was first reported, on Wednesday 18 November 2026.",
              font=font(SERIF, 13), fill=(220, 224, 232))


def draw_region_bar(draw, y):
    counts = region_counts()
    order = ["ASIA", "EUROPE", "AMERICAS", "MIDDLE EAST", "GLOBAL", "AFRICA", "OCEANIA"]
    seg = (W - 16) / 7
    x = 8
    for region in order:
        draw.rectangle([x, y, x + seg - 1, y + 16], fill=REGION_COLORS[region])
        draw.text((x + seg / 2, y + 3), "%s %d" % (region, counts[region]),
                  font=font(SANS_B, 10), fill=(255, 255, 255), anchor="ma")
        x += seg


def draw_field_bar(draw, y):
    counts = field_counts()
    short = {"Diplomacy": "Diplomacy", "War & security": "War & security",
             "Economy & markets": "Economy", "Politics & courts": "Politics",
             "Culture & sport": "Culture", "Business & tech": "Business",
             "Labour & society": "Labour", "Climate & disasters": "Climate",
             "Science & health": "Science"}
    order = ["Diplomacy", "War & security", "Economy & markets", "Politics & courts",
             "Culture & sport", "Business & tech", "Labour & society",
             "Climate & disasters", "Science & health"]
    parts = ["%s %d" % (short[f], counts[f]) for f in order if counts[f]]
    draw.rectangle([0, y, W, y + 14], fill=NAVY_DK)
    text = "BY FIELD  " + "  \u00b7  ".join(parts)
    draw.text((8, y + 2), fit(draw, text, font(SANS_B, 9), W - 16),
              font=font(SANS_B, 9), fill=(255, 255, 255))


def draw_timeline(draw, y):
    draw.rectangle([8, y, 78, y + 30], fill=RED)
    draw.text((43, y + 4), "THE DAY", font=font(SANS_B, 9), fill=(255, 255, 255),
              anchor="ma")
    draw.text((43, y + 16), "IN UTC", font=font(SANS_B, 9), fill=(255, 255, 255),
              anchor="ma")
    cell_w = (W - 16 - 78) / 8
    for i, (when, what) in enumerate(TIMELINE):
        cx = 84 + i * cell_w
        if i:
            draw.line([cx - 3, y + 3, cx - 3, y + 27], fill=RULE, width=1)
        draw.text((cx, y + 1), when, font=font(SANS_B, 9), fill=NAVY)
        for j, ln in enumerate(wrap(draw, what, font(SANS, 8), cell_w - 8, 2)):
            draw.text((cx, y + 13 + j * 10), ln, font=font(SANS, 8), fill=INK)


def card_frame(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=RULE, width=1)


def draw_lead(draw, s, x, y, w, h):
    num, region, _field, tag, head, deck, src, _lon, _lat = s
    card_frame(draw, x, y, w, h)
    # measure the headline first: a two-line headline shrinks the picture
    # so the deck still fits inside the card (no text may cross the frame)
    lines = wrap(draw, head, font(SERIF_B, 15), w - 16, 2)
    ih = 104 if len(lines) == 1 else 92
    ILLOS[num](draw, x + 1, y + 1, w - 2, ih)
    ty = y + ih + 4
    # number chip + region kicker; proof tag and source right-aligned
    draw.rectangle([x + 8, ty, x + 24, ty + 14], fill=REGION_COLORS[region])
    draw.text((x + 16, ty + 2), str(num), font=font(SANS_B, 10),
              fill=(255, 255, 255), anchor="ma")
    draw.text((x + 28, ty + 2), region, font=font(SANS_B, 9),
              fill=REGION_COLORS[region])
    right = (tag + "  \u00b7  " + src) if tag else src
    draw.text((x + w - 8, ty + 2), right, font=font(SANS_B, 8), fill=RED, anchor="ra")
    hy = ty + 17
    for j, ln in enumerate(lines):
        draw.text((x + 8, hy + j * 18), ln, font=font(SERIF_B, 15), fill=INK)
    dy = hy + 18 * len(lines) + 3
    for j, ln in enumerate(wrap(draw, deck, font(SANS, 9), w - 16, 2)):
        draw.text((x + 8, dy + j * 11), ln, font=font(SANS, 9), fill=(60, 60, 60))


def draw_small(draw, s, x, y, w, h):
    num, region, _field, _tag, head, deck, src, _lon, _lat = s
    card_frame(draw, x, y, w, h)
    ILLOS[num](draw, x + 1, y + 1, w - 2, 62)
    ty = y + 66
    draw.rectangle([x + 6, ty, x + 20, ty + 12], fill=REGION_COLORS[region])
    draw.text((x + 13, ty + 1), str(num), font=font(SANS_B, 9),
              fill=(255, 255, 255), anchor="ma")
    draw.text((x + 24, ty + 1), region, font=font(SANS_B, 8),
              fill=REGION_COLORS[region])
    draw.text((x + w - 6, ty + 1), src, font=font(SANS_B, 7), fill=GREY, anchor="ra")
    hy = ty + 14
    lines = wrap(draw, head, font(SERIF_B, 11), w - 12, 3)
    for j, ln in enumerate(lines):
        draw.text((x + 6, hy + j * 13), ln, font=font(SERIF_B, 11), fill=INK)
    dy = hy + 13 * len(lines) + 2
    for j, ln in enumerate(wrap(draw, deck, font(SANS, 8), w - 12, 2)):
        draw.text((x + 6, dy + j * 10), ln, font=font(SANS, 8), fill=(60, 60, 60))


def draw_map(draw, x0, y0, w, h):
    """Dotted world map with numbered region-coloured pins and brief dots."""
    draw.text((x0, y0), "WHERE IT HAPPENED", font=font(SANS_B, 11), fill=NAVY)
    mx, my = x0, y0 + 18
    mw, mh = w, h - 18
    # dotted land: grid 62 x 26 over lon -180..180, lat 80..-60
    cols, rows = 62, 26
    for r, spans in LAND:
        for c1, c2 in spans:
            for c in range(c1, c2 + 1):
                px = mx + (c + 0.5) * mw / cols
                py = my + (r + 0.5) * mh / rows
                draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(168, 178, 158))
    # brief dots (region colour)
    brief_region = {n: r for n, r, _ in BRIEFS}
    for num, lon, lat in BRIEF_DOTS:
        px = mx + (lon + 180) / 360 * mw
        py = my + (80 - lat) / 140 * mh
        draw.ellipse([px - 2, py - 2, px + 2, py + 2],
                     fill=REGION_COLORS[brief_region[num]])
    # Voyager star (deep space, off the map)
    sx, sy = mx + mw - 8, my + 6
    draw.polygon([(sx, sy - 6), (sx + 2, sy - 2), (sx + 6, sy - 2), (sx + 3, sy + 1),
                  (sx + 4, sy + 5), (sx, sy + 3), (sx - 4, sy + 5), (sx - 3, sy + 1),
                  (sx - 6, sy - 2), (sx - 2, sy - 2)], fill=GOLD)
    draw.text((sx - 12, sy - 5), "4", font=font(SANS_B, 9), fill=NAVY, anchor="ra")
    # numbered pins
    for s in STORIES:
        num, region = s[0], s[1]
        if num == 4:
            continue
        px, py = PINS[num]
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=REGION_COLORS[region],
                     outline=(255, 255, 255), width=1)
        draw.text((px, py - 6), str(num), font=font(SANS_B, 8),
                  fill=(255, 255, 255), anchor="ma")


def draw_legend(draw, x, y, w):
    draw.text((x, y), "Numbered pins: stories 1\u201316 \u00b7 dots: briefs",
              font=font(SANS, 8), fill=GREY)
    draw.text((x, y + 12), "\u2605 4 Voyager 1 \u2014 deep space, not on the map",
              font=font(SANS, 8), fill=GREY)
    # region colour key, two rows
    order = ["ASIA", "EUROPE", "AMERICAS", "MIDDLE EAST", "GLOBAL", "AFRICA", "OCEANIA"]
    cx, cy = x, y + 28
    for i, region in enumerate(order):
        if i == 4:
            cx, cy = x, y + 44
        draw.ellipse([cx, cy + 1, cx + 8, cy + 9], fill=REGION_COLORS[region])
        draw.text((cx + 11, cy), region, font=font(SANS_B, 8), fill=INK)
        cx += 11 + draw.textlength(region, font=font(SANS_B, 8)) + 12


def draw_howsure(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=NAVY, width=1)
    draw.text((x + 8, y + 6), "HOW SURE", font=font(SANS_B, 10), fill=NAVY)
    lines = [
        ("CONFIRMED", "on the record, filings, recordings"),
        ("CLAIM", "one side\u2019s account, not independently verified"),
        ("SOURCES", "monitors or unnamed sources, via a news agency"),
    ]
    yy = y + 22
    for tag, what in lines:
        draw.text((x + 8, yy), tag, font=font(SANS_B, 9), fill=RED)
        tw = draw.textlength(tag, font=font(SANS_B, 9))
        wrapped = wrap(draw, what, font(SANS, 9), w - 20 - tw, 2)
        for j, ln in enumerate(wrapped):
            draw.text((x + 12 + tw, yy + j * 11), ln, font=font(SANS, 9), fill=INK)
        yy += 12 + 11 * len(wrapped)
    draw.text((x + 8, yy + 2),
              "Every story names its source; claims are attributed.",
              font=font(SANS, 8), fill=GREY)


def draw_briefs(draw, x, y, w, h):
    draw.text((x, y), "ALSO ON WEDNESDAY 18 NOVEMBER",
              font=font(SANS_B, 11), fill=NAVY)
    col_w = (w - 2 * 14) / 3
    f_num = font(SANS_B, 9)
    f_txt = font(SANS, 9)
    rows = 12
    for i, (num, _region, text) in enumerate(BRIEFS):
        col, row = divmod(i, rows)
        bx = x + col * (col_w + 14)
        by = y + 18 + row * 15
        draw.text((bx, by), "%d" % num, font=f_num, fill=RED)
        draw.text((bx + 20, by), fit(draw, text, f_txt, col_w - 20),
                  font=f_txt, fill=INK)


def draw_numbers(draw, x, y, w):
    draw.text((x, y), "THE DAY IN NUMBERS", font=font(SANS_B, 11), fill=NAVY)
    cell_w = w / len(NUMBERS)
    for i, (big, label) in enumerate(NUMBERS):
        cx = x + i * cell_w
        if i:
            draw.line([cx - 4, y + 18, cx - 4, y + 52], fill=RULE, width=1)
        draw.text((cx + cell_w / 2, y + 18), big, font=font(SANS_B, 17),
                  fill=RED if i in (0, 4) else NAVY, anchor="ma")
        draw.text((cx + cell_w / 2, y + 40), label, font=font(SANS, 8),
                  fill=GREY, anchor="ma")


def draw_datecheck(draw, y):
    draw.rectangle([8, y, W - 8, y + 36], outline=RED, width=2)
    draw.text((16, y + 12), "DATE CHECK", font=font(SANS_B, 10), fill=RED)
    for j, ln in enumerate(wrap(draw, DATE_CHECK, font(SANS, 9), W - 120 - 16, 2)):
        draw.text((120, y + 5 + j * 11), ln, font=font(SANS, 9), fill=INK)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_region_bar(draw, 88)
    draw_field_bar(draw, 106)
    draw_timeline(draw, 124)
    # 4 leads
    lead_w = 246
    for i, s in enumerate(STORIES[:4]):
        draw_lead(draw, s, 8 + i * (lead_w + 8), 158, lead_w, 176)
    # 12 small cards, two rows of six
    small_w = 161
    for i, s in enumerate(STORIES[4:10]):
        draw_small(draw, s, 8 + i * (small_w + 8), 338, small_w, 146)
    for i, s in enumerate(STORIES[10:16]):
        draw_small(draw, s, 8 + i * (small_w + 8), 488, small_w, 146)
    # bottom: map + briefs
    draw_map(draw, 8, 640, 300, 140)
    draw_legend(draw, 8, 802, 300)
    draw_howsure(draw, 8, 856, 300, 96)
    draw_briefs(draw, 316, 640, 700, 210)
    draw_numbers(draw, 316, 856, 700)
    draw.text((666, 934), "Reads at three sizes: the date and 4 leads at thumbnail size \u00b7 "
              "16 pictures at half size \u00b7 all 52 stories at full size.",
              font=font(SERIF, 9), fill=GREY, anchor="ma")
    draw_datecheck(draw, 956)
    draw.text((W // 2, 1000), fit(draw, FOOT_SOURCES, font(SANS, 8), W - 16),
              font=font(SANS, 8), fill=GREY, anchor="ma")
    img.save(OUT, format="PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = render()
    print(path, os.path.getsize(path), "bytes")
