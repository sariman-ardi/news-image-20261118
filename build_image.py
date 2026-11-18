#!/usr/bin/env python3
"""Draw the front page for the make.fun news-image-20261118 bounty.

The page is a one-page newspaper front: a navy masthead with the date,
a three-item subhead, then six sections in two columns, forty stories in
total, each a bold headline over one grey fact line. Everything is drawn
from fixed data with the DejaVu fonts, so two runs produce identical bytes.

Usage:  python3 build_image.py [output.png]
Default output is entry.png next to this script.
"""

import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER = (250, 248, 242)
NAVY = (16, 35, 63)
GOLD = (201, 162, 39)
INK = (24, 24, 24)
FACT_GREY = (88, 88, 88)
RULE_GREY = (198, 196, 188)
WHITE = (255, 255, 255)

MARGIN = 24
RIGHT_COL_X = 521
COL_W = 479
STORY_PITCH = 34
FACT_DROP = 17

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SANS = FONT_DIR + "/DejaVuSans.ttf"
SANS_BOLD = FONT_DIR + "/DejaVuSans-Bold.ttf"
SERIF_BOLD = FONT_DIR + "/DejaVuSerif-Bold.ttf"

SUBHEAD = "Gulf strikes \u00b7 Crimea bridge falls \u00b7 Xi-Trump-Putin summit"
FOOTER = (
    "Events of Wednesday 18 November 2026, as reported. "
    "Sources: Reuters \u00b7 Al Jazeera \u00b7 AP \u00b7 BBC \u00b7 The Independent"
)

# Each section: name, marker colour, and its stories as (headline, fact).
# Left column takes the first half of each section, right column the rest.
SECTIONS = [
    {
        "name": "EUROPE",
        "colour": (179, 38, 30),
        "stories": [
            ("Ukraine hits Crimea bridge again",
             "Road span collapses into Kerch Strait after a second strike"),
            ("Russian military plane crashes, 19 dead",
             "An-12 goes down in Kemerovo region; all aboard killed"),
            ("Moldova closes airspace after drones",
             "Russian drones cross the border; flights suspended"),
            ("UK and Germany push back on U.S. over Ukraine",
             "Allies reject U.S. criticism of Kyiv's deep strikes"),
            ("Russia pounds Kyiv bridges in reply",
             "Northern and Southern bridges hit; power and water cut"),
            ("France hit by second nationwide strike",
             "146,000 protest as unions strike over living costs"),
            ("Five EU states plan Rwanda return hubs",
             "Vienna plan sends rejected asylum seekers to Kigali"),
        ],
    },
    {
        "name": "MIDDLE EAST",
        "colour": (194, 94, 0),
        "stories": [
            ("U.S. strikes IRGC site on Qeshm Island",
             "Jets hit a missile site after Iran's drone attacks"),
            ("Tanker hit near Strait of Hormuz",
             "LPG tanker Tara Gas struck; shipping stays on alert"),
            ("Iran refuses UN nuclear inspection",
             "No IAEA visits until the war ends, Tehran says"),
            ("Knesset elects Kahana as speaker",
             "Netanyahu's opponents take control of the agenda"),
            ("Iran fires drones at U.S. base in Bahrain",
             "Third attack on Bahrain in under a week; intercepted"),
            ("Houthis advance in Yemen; army retreats",
             "Fighters seize coast 100 km west of Aden"),
            ("Gaza ceasefire may collapse, board warns",
             "Truce under strain as aid access stalls"),
        ],
    },
    {
        "name": "ASIA-PACIFIC",
        "colour": (14, 124, 123),
        "stories": [
            ("Xi, Trump and Putin to meet in Shenzhen",
             "First three-way summit set for Thursday at APEC"),
            ("Japan scrambles jets over Russian planes",
             "Two suspected Russian aircraft violate airspace"),
            ("Modi proposes free e-visas for ASEAN",
             "India pitches open travel at East Asia Summit"),
            ("Cyclone Xavier hits Cook Islands",
             "Category 5 storm, gusts to 315 km/h in the north"),
            ("APEC summit opens in Shenzhen",
             "Putin arrives as China hosts the 33rd leaders' meeting"),
            ("Quad unveils minerals pacts in Manila",
             "Trump announces critical-minerals and defence deals"),
            ("Cyclone Akvan nears India's Andhra coast",
             "Landfall due 20 Nov; winds to 145 km/h, red alert"),
        ],
    },
    {
        "name": "AMERICAS",
        "colour": (31, 78, 121),
        "stories": [
            ("Peltola wins Alaska Senate race",
             "Democrat's win gives her party 56 seats"),
            ("NSA network goes down in U.S. outages",
             "Latest of at least eight major outages in a week"),
            ("U.S. tightens chip access rules for China",
             "New export rule hits data centres; Beijing vows payback"),
            ("Man gets 27 years over Iran-linked plot",
             "Plot against Trump; sentenced in New York"),
            ("U.S. loses measles-free status after 26 years",
             "5,412 cases, worst since 1991, PAHO rules"),
            ("Pentagon fails its audit \u2014 9th year in a row",
             "Auditors cannot verify $4.8 trillion in assets"),
            ("U.S. soldier held in UK over spying claim",
             "Taken into U.S. military custody after arrest"),
        ],
    },
    {
        "name": "AFRICA",
        "colour": (110, 80, 150),
        "stories": [
            ("Ebola outbreak in DR Congo more than doubles",
             "11,000 cases and 5,400 deaths, UN says"),
            ("South Africa probes shootings that killed 17",
             "Weekend attacks in Pretoria and KwaZulu-Natal"),
            ("African Union pushes Sudan and Congo peace",
             "Regional solutions urged for both wars"),
            ("Nigeria: U.S. intel helps target militants",
             "Near-daily missions back 2027 election security"),
            ("Ghana curbs raw cashew exports",
             "Mahama backs local processing with a new levy"),
            ("Clashes near Eritrean border raise war fears",
             "Fighting in Tigray stokes wider-war worries"),
        ],
    },
    {
        "name": "BUSINESS \u00b7 TECH \u00b7 SPORT",
        "colour": (46, 125, 50),
        "stories": [
            ("Nvidia beats forecasts after CEO exit",
             "Revenue $115.8bn tops estimates under interim chief"),
            ("Amazon to invest $7bn in India renewables",
             "Solar and data centres by 2030"),
            ("Fela Kuti enters Rock & Roll Hall of Fame",
             "First African-born artist inducted, posthumously"),
            ("Anthropic set to list on Nasdaq Nov. 19",
             "$1.4 trillion IPO priced; AI firm goes public"),
            ("Dhoni retires from IPL, becomes CSK mentor",
             "CSK legend, 45, ends playing career after 272 games"),
            ("Pattinson named as new James Bond",
             "British actor succeeds Daniel Craig in reboot"),
        ],
    },
]


def load_font(path, size):
    """Load one DejaVu face at the requested size."""
    return ImageFont.truetype(path, size)


def fit_line(draw, text, path, size, max_width):
    """Pick the largest size at or below `size` that fits `max_width`.

    Falls back to trimming the tail with an ellipsis if even the
    smallest size is still too wide, so no line can ever overflow
    its column. Returns the font together with the text to draw,
    because the trimmed text is what the caller must render.
    """
    while size > 10:
        font = load_font(path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font, text
        size -= 1
    font = load_font(path, 10)
    while draw.textlength(text + "\u2026", font=font) > max_width and len(text) > 1:
        text = text[:-1]
    return font, text + "\u2026"


def draw_globe(draw, cx, cy, radius, colour):
    """A wireframe globe: outer ring, two meridians, three parallels."""
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        outline=colour, width=3,
    )
    draw.ellipse(
        [cx - radius // 3, cy - radius, cx + radius // 3, cy + radius],
        outline=colour, width=2,
    )
    draw.ellipse(
        [cx - (2 * radius) // 3, cy - radius, cx + (2 * radius) // 3, cy + radius],
        outline=colour, width=1,
    )
    for dy in (-radius // 2, 0, radius // 2):
        half = int((radius * radius - dy * dy) ** 0.5)
        draw.line([cx - half, cy + dy, cx + half, cy + dy], fill=colour, width=2)


def draw_masthead(draw):
    """Navy band: globe, kicker, date, story count, gold rule."""
    draw.rectangle([0, 0, PAGE_W, 84], fill=NAVY)
    draw_globe(draw, 48, 42, 24, GOLD)
    draw.text((88, 14), "THE WORLD IN ONE DAY",
              font=load_font(SANS_BOLD, 16), fill=GOLD)
    draw.text((88, 34), "Wednesday, 18 November 2026",
              font=load_font(SERIF_BOLD, 40), fill=WHITE)
    draw.text((PAGE_W - MARGIN, 14), "40 STORIES",
              font=load_font(SANS_BOLD, 19), fill=GOLD, anchor="ra")
    draw.text((PAGE_W - MARGIN, 42), "6 CONTINENTS",
              font=load_font(SANS_BOLD, 13), fill=WHITE, anchor="ra")
    draw.rectangle([0, 84, PAGE_W, 88], fill=GOLD)


def draw_section_head(draw, y, name, colour):
    """Coloured square plus section name, with a hairline rule below."""
    draw.rectangle([MARGIN, y, MARGIN + 12, y + 12], fill=colour)
    draw.text((MARGIN + 18, y - 2), name,
              font=load_font(SANS_BOLD, 15), fill=colour)
    draw.line([MARGIN, y + 17, PAGE_W - MARGIN, y + 17], fill=RULE_GREY, width=1)
    return y + 22


def draw_story(draw, x, y, headline, fact):
    """One story: bold headline, grey fact line underneath."""
    head_font, head_text = fit_line(draw, headline, SANS_BOLD, 15, COL_W)
    draw.text((x, y), head_text, font=head_font, fill=INK)
    fact_font, fact_text = fit_line(draw, fact, SANS, 12, COL_W)
    draw.text((x, y + FACT_DROP), fact_text, font=fact_font, fill=FACT_GREY)


def render():
    """Compose the whole front page and return it as an image."""
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)
    draw_masthead(draw)
    draw.text((MARGIN, 95), SUBHEAD, font=load_font(SANS_BOLD, 17), fill=INK)
    cursor = 114
    for section in SECTIONS:
        cursor = draw_section_head(draw, cursor, section["name"], section["colour"])
        stories = section["stories"]
        split = (len(stories) + 1) // 2
        left, right = stories[:split], stories[split:]
        rows = max(len(left), len(right))
        for row in range(rows):
            top = cursor + row * STORY_PITCH
            if row < len(left):
                draw_story(draw, MARGIN, top, *left[row])
            if row < len(right):
                draw_story(draw, RIGHT_COL_X, top, *right[row])
        cursor += rows * STORY_PITCH + 2
    draw.text((MARGIN, 1008), FOOTER, font=load_font(SANS, 11), fill=FACT_GREY)
    return page


def main(argv):
    """Render the page and write it as a PNG; print its size and hash."""
    if len(argv) > 1:
        out_path = Path(argv[1])
    else:
        out_path = Path(__file__).resolve().parent / "entry.png"
    page = render()
    page.save(out_path, format="PNG")
    data = out_path.read_bytes()
    print(f"wrote {out_path} ({page.size[0]}x{page.size[1]}, "
          f"{len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
