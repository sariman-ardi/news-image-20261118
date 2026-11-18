#!/usr/bin/env python3
"""Build entry.png v2 for the make.fun news-image-20261118 bounty.

Draws a one-page newspaper-style front page of Wednesday 18 November
2026 world news with Pillow: 40 stories across 6 sections, grouped by
region/field. Purely a build tool: it is NOT part of the entry
repository (the entry ships only main.py, entry.png, LICENSE and
README.md). Run: python3 build_image.py  -> writes entry.png next to it.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

NAVY = (16, 35, 63)
GOLD = (201, 162, 39)
PAPER = (250, 248, 242)
INK = (24, 28, 36)
MUTED = (96, 102, 112)
RULE = (208, 203, 192)

# 40 stories: (headline, one-line fact). All reported in the 18 Nov 2026
# news cycle, verified against OneTurn, Reuters, Al Jazeera, AP, BBC,
# The Independent and the day's roundups.
SECTIONS = [
    ("EUROPE", (179, 38, 30), [
        ("Ukraine hits Crimea bridge again",
         "Road span collapses into Kerch Strait after a second strike"),
        ("Russia pounds Kyiv bridges in reply",
         "Northern and Southern bridges hit; power and water cut"),
        ("Russian military plane crashes, 19 dead",
         "An-12 goes down in Kemerovo region; all aboard killed"),
        ("France hit by second nationwide strike",
         "146,000 protest as unions strike over living costs"),
        ("Moldova closes airspace after drones",
         "Russian drones cross the border; flights suspended"),
        ("Five EU states plan Rwanda return hubs",
         "Vienna plan sends rejected asylum seekers to Kigali"),
        ("UK and Germany push back on U.S. over Ukraine",
         "Allies reject U.S. criticism of Kyiv's deep strikes"),
    ]),
    ("MIDDLE EAST", (194, 94, 0), [
        ("U.S. strikes IRGC site on Qeshm Island",
         "Jets hit a missile site after Iran's drone attacks"),
        ("Iran fires drones at U.S. base in Bahrain",
         "Third attack on Bahrain in under a week; intercepted"),
        ("Tanker hit near Strait of Hormuz",
         "LPG tanker Tara Gas struck; shipping stays on alert"),
        ("Houthis advance in Yemen; army retreats",
         "Fighters seize coast 100 km west of Aden"),
        ("Iran refuses UN nuclear inspection",
         "No IAEA visits until the war ends, Tehran says"),
        ("Gaza ceasefire may collapse, board warns",
         "Truce under strain as aid access stalls"),
        ("Knesset elects Kahana as speaker",
         "Netanyahu's opponents take control of the agenda"),
    ]),
    ("ASIA-PACIFIC", (14, 124, 123), [
        ("Xi, Trump and Putin to meet in Shenzhen",
         "First three-way summit set for Thursday at APEC"),
        ("APEC summit opens in Shenzhen",
         "Putin arrives as China hosts the 33rd leaders' meeting"),
        ("Japan scrambles jets over Russian planes",
         "Two suspected Russian aircraft violate airspace"),
        ("Quad unveils minerals pacts in Manila",
         "Trump announces critical-minerals and defence deals"),
        ("Modi proposes free e-visas for ASEAN",
         "India pitches open travel at East Asia Summit"),
        ("Cyclone Akvan nears India's Andhra coast",
         "Landfall due 20 Nov; winds to 145 km/h, red alert"),
        ("Cyclone Xavier hits Cook Islands",
         "Category 5 storm, gusts to 315 km/h in the north"),
    ]),
    ("AMERICAS", (31, 78, 121), [
        ("Peltola wins Alaska Senate race",
         "Democrat's win gives her party 56 seats"),
        ("U.S. loses measles-free status after 26 years",
         "5,412 cases, worst since 1991, PAHO rules"),
        ("NSA network goes down in U.S. outages",
         "Latest of at least eight major outages in a week"),
        ("Pentagon fails its audit \u2014 9th year in a row",
         "Auditors cannot verify $4.8 trillion in assets"),
        ("U.S. tightens chip access rules for China",
         "New export rule hits data centres; Beijing vows payback"),
        ("U.S. soldier held in UK over spying claim",
         "Taken into U.S. military custody after arrest"),
        ("Man gets 27 years over Iran-linked plot",
         "Plot against Trump; sentenced in New York"),
    ]),
    ("AFRICA", (110, 80, 150), [
        ("Ebola outbreak in DR Congo more than doubles",
         "11,000 cases and 5,400 deaths, UN says"),
        ("Nigeria: U.S. intel helps target militants",
         "Near-daily missions back 2027 election security"),
        ("South Africa probes shootings that killed 17",
         "Weekend attacks in Pretoria and KwaZulu-Natal"),
        ("Ghana curbs raw cashew exports",
         "Mahama backs local processing with a new levy"),
        ("African Union pushes Sudan and Congo peace",
         "Regional solutions urged for both wars"),
        ("Clashes near Eritrean border raise war fears",
         "Fighting in Tigray stokes wider-war worries"),
    ]),
    ("BUSINESS \u00b7 TECH \u00b7 SPORT", (46, 125, 50), [
        ("Nvidia beats forecasts after CEO exit",
         "Revenue $115.8bn tops estimates under interim chief"),
        ("Anthropic set to list on Nasdaq Nov. 19",
         "$1.4 trillion IPO priced; AI firm goes public"),
        ("Amazon to invest $7bn in India renewables",
         "Solar and data centres by 2030"),
        ("Dhoni retires from IPL, becomes CSK mentor",
         "CSK legend, 45, ends playing career after 272 games"),
        ("Fela Kuti enters Rock & Roll Hall of Fame",
         "First African-born artist inducted, posthumously"),
        ("Pattinson named as new James Bond",
         "British actor succeeds Daniel Craig in reboot"),
    ]),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_one_line(d, text, fnt, max_w):
    """Truncate to a single line with an ellipsis if it is too wide."""
    if d.textlength(text, font=fnt) <= max_w:
        return text
    ell = "\u2026"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if d.textlength(text[:mid] + ell, font=fnt) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo].rstrip() + ell


def draw_globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=color, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          start=200, end=340, fill=color, width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          start=20, end=160, fill=color, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 84], fill=NAVY)
    d.rectangle([0, 84, W, 87], fill=GOLD)
    draw_globe(d, 46, 42, 22, GOLD)
    d.text((80, 12), "THE WORLD IN ONE DAY",
           font=font(FONT_BOLD, 17), fill=GOLD)
    d.text((78, 34), "Wednesday, 18 November 2026",
           font=font(FONT_SERIF, 34), fill=(255, 255, 255))
    f_side = font(FONT_BOLD, 20)
    d.text((1000 - d.textlength("40 STORIES", font=f_side), 16),
           "40 STORIES", font=f_side, fill=GOLD)
    f_side2 = font(FONT_BOLD, 14)
    d.text((1000 - d.textlength("6 CONTINENTS", font=f_side2), 44),
           "6 CONTINENTS", font=f_side2, fill=(255, 255, 255))

    # ---- subhead: the day's three biggest stories ----
    d.text((24, 92),
           "Gulf strikes  \u00b7  Crimea bridge falls  \u00b7  Xi\u2013Trump\u2013Putin summit",
           font=font(FONT_BOLD, 15), fill=INK)

    # ---- sections ----
    f_sec = font(FONT_BOLD, 14)
    f_head = font(FONT_BOLD, 14)
    f_sub = font(FONT_REG, 11)
    margin, gutter = 24, 16
    col_w = (W - 2 * margin - gutter) // 2
    y = 110
    for name, color, stories in SECTIONS:
        # section header: colour chip + name + rule
        d.rectangle([margin, y + 5, margin + 12, y + 17], fill=color)
        d.text((margin + 20, y + 1), name, font=f_sec, fill=color)
        name_w = d.textlength(name, font=f_sec)
        rule_x = margin + 20 + name_w + 12
        d.line([rule_x, y + 11, W - margin, y + 11], fill=RULE, width=2)
        gy = y + 24
        for i, (head, sub) in enumerate(stories):
            col, row = i % 2, i // 2
            x = margin + col * (col_w + gutter)
            cy = gy + row * 34
            d.text((x, cy),
                   fit_one_line(d, head, f_head, col_w),
                   font=f_head, fill=INK)
            d.text((x, cy + 17),
                   fit_one_line(d, sub, f_sub, col_w),
                   font=f_sub, fill=(74, 80, 92))
        # 7-story sections take 4 rows, 6-story sections 3 rows
        rows = (len(stories) + 1) // 2
        y += 24 + rows * 34

    # ---- footer ----
    d.text((24, 1008),
           "Events of Wednesday 18 November 2026, as reported. "
           "Sources: Reuters \u00b7 Al Jazeera \u00b7 AP \u00b7 BBC \u00b7 The Independent",
           font=font(FONT_REG, 10), fill=MUTED)

    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
