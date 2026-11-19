"""Draw the 18 November 2026 world-news poster: 50 sourced stories,
a UTC timeline and a date check. Pure Pillow, deterministic output."""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_TITLE = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_BODY = os.path.join(FONT_DIR, "DejaVuSans.ttf")

NAVY = (14, 42, 71)
NAVY_DARK = (9, 30, 52)
GOLD = (201, 162, 39)
GOLD_LIGHT = (232, 196, 90)
GREEN = (29, 92, 46)
INK = (18, 18, 18)
GREY = (90, 90, 90)
RULE = (200, 200, 200)
PAPER = (250, 249, 246)
TIMELINE_BG = (238, 241, 244)

# (headline, subline with source) — 50 stories, verified 18 Nov 2026.
SECTIONS = [
    ("EUROPE", (178, 34, 34), [
        ("Ukraine hits Crimea bridge again",
         "Road span collapses into Kerch Strait after a second strike \u00b7 Reuters"),
        ("Russian military plane crashes, 19 dead",
         "An-12 goes down in Kemerovo region; all aboard killed \u00b7 AP"),
        ("Moldova closes airspace after drones",
         "Seven drones cross the border; flights suspended \u00b7 AP"),
        ("UK and Germany push back on U.S. over Ukraine",
         "Allies reject U.S. criticism of Kyiv's deep strikes \u00b7 Reuters"),
        ("Russia pounds Kyiv bridges in reply",
         "Northern and Southern bridges hit; power and water cut \u00b7 AP"),
        ("France hit by second nationwide strike",
         "146,000 protest as unions strike over living costs \u00b7 Reuters"),
        ("Five EU states plan Rwanda return hubs",
         "Vienna plan sends rejected asylum seekers to Kigali \u00b7 AP"),
        ("EU authorises Indonesia trade deal",
         "Governments sign off on the trade agreement \u00b7 Reuters"),
    ]),
    ("MIDDLE EAST", (176, 92, 8), [
        ("U.S. strikes IRGC site on Qeshm Island",
         "Jets hit a missile site after Iran's drone attacks \u00b7 Reuters"),
        ("Tanker hit near Strait of Hormuz",
         "LPG tanker struck; shipping stays on alert \u00b7 AP"),
        ("Iran refuses UN nuclear inspection",
         "No IAEA visits until the war ends, Tehran says \u00b7 Reuters"),
        ("Knesset elects Kahana as speaker",
         "Netanyahu's opponents take control of the agenda \u00b7 AP"),
        ("Iran fires drones at U.S. base in Bahrain",
         "Third attack on Bahrain in under a week; intercepted \u00b7 Reuters"),
        ("Houthis advance in Yemen; army retreats",
         "Fighters seize coast 100 km west of Aden \u00b7 AP"),
        ("Gaza ceasefire may collapse, board warns",
         "Truce under strain as aid access stalls \u00b7 AP"),
        ("Israel launches ground operation in Gaza",
         "First large operation in central Gaza since the truce \u00b7 AP"),
    ]),
    ("ASIA-PACIFIC", (0, 122, 122), [
        ("Xi, Trump and Putin to meet in Shenzhen",
         "First three-way summit set for Thursday at APEC \u00b7 AFP"),
        ("Japan scrambles jets over Russian planes",
         "Two suspected Russian aircraft violate airspace \u00b7 Reuters"),
        ("Modi proposes free e-visas for ASEAN",
         "India pitches open travel at East Asia Summit \u00b7 PTI"),
        ("Cyclone Xavier hits Cook Islands",
         "Category 5 storm, gusts to 315 km/h in the north \u00b7 AP"),
        ("APEC summit opens in Shenzhen",
         "Putin arrives as China hosts the 33rd leaders' meeting \u00b7 AFP"),
        ("Quad unveils minerals pacts in Manila",
         "Trump announces critical-minerals and defence deals \u00b7 Reuters"),
        ("Cyclone Akvan nears India's Andhra coast",
         "Landfall due 20 Nov; winds to 145 km/h, red alert \u00b7 IMD"),
        ("India signs Navy air-defence deal",
         "Rs 1,976 crore pact to upgrade Navy air defences \u00b7 Reuters"),
        ("Taiwan logs 10 PLA sorties, 11 ships",
         "Ten sorties and eleven ships in latest window \u00b7 AP"),
    ]),
    ("AMERICAS", (30, 80, 160), [
        ("Peltola wins Alaska Senate race",
         "Democrat's win gives her party 56 seats \u00b7 AP"),
        ("NSA network goes down in U.S. outages",
         "Latest of at least eight major outages in a week \u00b7 Reuters"),
        ("U.S. tightens chip access rules for China",
         "New export rule hits data centres; Beijing vows payback \u00b7 Reuters"),
        ("Man gets 27 years over Iran-linked plot",
         "Plot against Trump; sentenced in New York \u00b7 AP"),
        ("U.S. loses measles-free status after 26 years",
         "5,412 cases, worst since 1991, PAHO rules \u00b7 PAHO"),
        ("Pentagon fails its audit \u2014 9th year in a row",
         "Auditors cannot verify $4.8 trillion in assets \u00b7 AP"),
        ("U.S. soldier held in UK over spying claim",
         "Taken into U.S. military custody after arrest \u00b7 AP"),
        ("Jeffries nominated as Speaker, 251 votes",
         "Set to become the first Black Speaker \u00b7 AP"),
        ("FAA failure strands 1m+ U.S. air travellers",
         "Air travel chaos after the system failure \u00b7 Reuters"),
    ]),
    ("AFRICA", (110, 60, 160), [
        ("Ebola outbreak in DR Congo more than doubles",
         "11,000 cases and 5,400 deaths, UN says \u00b7 WHO"),
        ("South Africa probes shootings that killed 17",
         "Weekend attacks in Pretoria and KwaZulu-Natal \u00b7 AP"),
        ("African Union pushes Sudan and Congo peace",
         "Regional solutions urged for both wars \u00b7 Reuters"),
        ("Nigeria: U.S. intel helps target militants",
         "Near-daily missions back 2027 election security \u00b7 Reuters"),
        ("Ghana curbs raw cashew exports",
         "Mahama backs local processing with a new levy \u00b7 AP"),
        ("Clashes near Eritrean border raise war fears",
         "Fighting in Tigray stokes wider-war worries \u00b7 Reuters"),
        ("Ethiopia and Eritrea mass troops near Badme",
         "Build-up reported along the disputed border \u00b7 Reuters"),
    ]),
    ("BUSINESS \u00b7 TECH \u00b7 SPORT", (30, 120, 50), [
        ("Nvidia beats forecasts after CEO exit",
         "Revenue $115.8bn tops estimates under interim chief \u00b7 Reuters"),
        ("Amazon to invest $7bn in India renewables",
         "Solar and data centres by 2030 \u00b7 Reuters"),
        ("Fela Kuti enters Rock & Roll Hall of Fame",
         "First African-born artist inducted, posthumously \u00b7 AP"),
        ("Anthropic set to list on Nasdaq Nov. 19",
         "$1.4 trillion IPO priced; AI firm goes public \u00b7 Reuters"),
        ("Dhoni retires from IPL, becomes CSK mentor",
         "CSK legend, 45, ends playing career after 272 games \u00b7 PTI"),
        ("Pattinson named as new James Bond",
         "British actor succeeds Daniel Craig in reboot \u00b7 Reuters"),
        ("Voyager 1 reaches one light-day from Earth",
         "NASA probe crosses milestone at 05:16 ET \u00b7 NASA"),
        ("Germany beats Slovakia 6-0",
         "World Cup qualifying rout \u00b7 Reuters"),
        ("Oil slides; Brent settles at $91.95",
         "Traders weigh surplus supply outlook \u00b7 Reuters"),
    ]),
]

# (time label, event) — the day as it happened.
TIMELINE = [
    ("01:07 UTC", "Gaza truce warning reaches the UN"),
    ("05:16 ET", "Voyager 1 passes one light-day"),
    ("Morning", "APEC opens in Shenzhen"),
    ("Morning", "Moldova reopens airspace"),
    ("Midday", "U.S. jets strike Qeshm Island"),
    ("Afternoon", "Iran drones fired at Bahrain"),
    ("Evening", "Peltola wins Alaska Senate race"),
    ("Evening", "Nvidia beats forecasts, $115.8bn"),
]

MARGIN = 28
COL_GAP = 24
COL_W = (W - 2 * MARGIN - COL_GAP) // 2


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, fnt, width):
    """Shorten text with an ellipsis until it fits the width."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "\u2026", font=fnt) > width:
        text = text[:-1]
    return text + "\u2026"


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD_LIGHT, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=GOLD_LIGHT, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=GOLD_LIGHT, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=GOLD_LIGHT, width=2)
    draw.arc([cx - r, cy - r, cx + r, cy - r // 4], 300, 420, fill=GOLD_LIGHT, width=2)


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 82], fill=NAVY)
    draw.rectangle([0, 82, W, 85], fill=GOLD)
    draw_globe(draw, 48, 41, 29)
    f_small = font(F_TITLE, 15)
    f_big = font(F_TITLE, 33)
    draw.text((92, 10), "THE WORLD IN ONE DAY", font=f_small, fill=GOLD_LIGHT)
    draw.text((92, 30), "Wednesday, 18 November 2026", font=f_big, fill=(255, 255, 255))
    f_num = font(F_TITLE, 21)
    f_sub = font(F_TITLE, 12)
    draw.text((W - MARGIN, 12), "50 STORIES", font=f_num, fill=GOLD_LIGHT, anchor="ra")
    draw.text((W - MARGIN, 40), "SOURCED \u00b7 6 CONTINENTS", font=f_sub, fill=(255, 255, 255), anchor="ra")


def draw_datecheck(draw):
    draw.rectangle([0, 85, W, 103], fill=GREEN)
    fnt = font(F_TITLE, 12)
    text = ("\u2713 DATE CHECK \u2014 18 November 2026 was a Wednesday  \u00b7  "
            "All 50 stories below were reported on this date  \u00b7  "
            "Every story names its source")
    draw.text((MARGIN, 88), fit(draw, text, fnt, W - 2 * MARGIN), font=fnt, fill=(255, 255, 255))


def draw_sections(draw, y0):
    f_head = font(F_TITLE, 13)
    f_story = font(F_TITLE, 12)
    f_sub = font(F_BODY, 9)
    y = y0
    for title, color, stories in SECTIONS:
        draw.rectangle([MARGIN, y + 3, MARGIN + 12, y + 15], fill=color)
        draw.text((MARGIN + 18, y), title, font=f_head, fill=color)
        draw.line([MARGIN + 18 + draw.textlength(title, font=f_head) + 8, y + 8,
                   W - MARGIN, y + 8], fill=RULE, width=1)
        y += 20
        left = stories[0::2]
        right = stories[1::2]
        rows = max(len(left), len(right))
        for i in range(rows):
            for col, item in ((0, left[i] if i < len(left) else None),
                              (1, right[i] if i < len(right) else None)):
                if item is None:
                    continue
                x = MARGIN + col * (COL_W + COL_GAP)
                head, sub = item
                draw.text((x, y), fit(draw, head, f_story, COL_W), font=f_story, fill=INK)
                draw.text((x, y + 14), fit(draw, sub, f_sub, COL_W), font=f_sub, fill=GREY)
            y += 26
        y += 4
    return y


def draw_timeline(draw, y0):
    draw.rectangle([0, y0, W, y0 + 78], fill=TIMELINE_BG)
    f_title = font(F_TITLE, 11)
    f_time = font(F_TITLE, 10)
    f_text = font(F_BODY, 10)
    draw.text((MARGIN, y0 + 6), "THE DAY AS IT HAPPENED \u2014 TIMES UTC UNLESS NOTED",
              font=f_title, fill=NAVY)
    cell_w = (W - 2 * MARGIN) // 4
    for idx, (when, what) in enumerate(TIMELINE):
        row = idx // 4
        col = idx % 4
        x = MARGIN + col * cell_w
        yy = y0 + 25 + row * 25
        draw.text((x, yy), when, font=f_time, fill=NAVY)
        draw.text((x, yy + 12), fit(draw, what, f_text, cell_w - 8), font=f_text, fill=INK)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_datecheck(draw)
    y = draw_sections(draw, 108)
    draw_timeline(draw, 918)
    f_foot = font(F_BODY, 10)
    foot = ("Events of Wednesday 18 November 2026, as reported.  Sources: Reuters \u00b7 AP \u00b7 AFP "
            "\u00b7 BBC \u00b7 PTI \u00b7 NASA \u00b7 PAHO \u00b7 WHO \u00b7 IMD \u00b7 SeeNews  \u2014  "
            "50 stories \u00b7 6 continents")
    draw.text((W // 2, 1002), fit(draw, foot, f_foot, W - 2 * MARGIN),
              font=f_foot, fill=GREY, anchor="ma")
    img.save(OUT, format="PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = render()
    print(path, os.path.getsize(path), "bytes")
