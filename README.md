# Wednesday 18 November 2026 — one page, 52 stories

[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/c/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/sariman-ardi/news-image-20261118/rank.svg)](https://make.fun/c/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/sariman-ardi/news-image-20261118/reward.svg)](https://make.fun/c/news-image-20261118)

A single 1024×1024 newspaper page summarising world news from
Wednesday 18 November 2026 — everything on the page happened, or was
first reported, on that day.

## What is on the page

- **52 stories across 7 regions** (Asia 7, Europe 10, Americas 12,
  Middle East 4, Global 9, Africa 7, Oceania 3), every story named with
  its source.
- **16 original AI illustrations** — no photos. The four lead stories
  and the twelve drawn stories each carry a detailed editorial
  drawing: the Gulf drone routes, the Shenzhen tarmac welcome, the
  night drone attack on Ukraine, Voyager 1 one light-day out, the
  €45bn EU loan, the Fed's falling Dow, Cyclone Akvan, the Gaza
  yellow line, the Speaker vote, the GTA VI launch, El Obeid, UK
  inflation, the COP31 split, the Bangladesh factory shutdowns, the
  Ethiopia–Eritrea border, and the record Anthropic IPO. The pictures
  carry no words; the big figures (141 fired, 1 light-day, 37 killed,
  3.6%, 55 factories, $83) are laid out on top of them.
- **A UTC timeline** of the day in eight moments, from the overnight
  drone attacks to the Wall Street close.
- **A numbered world map** ("Where it happened") with region-coloured
  pins for stories 1–16 and dots for the 36 briefs.
- **"How sure"** — every claim is tagged CONFIRMED, CLAIM or
  SOURCES, and the big numbers carry their proof (141 drones fired —
  Kyiv air force; 126 downed).
- **"The day in numbers"** — 141 drones, €45bn, 25.9bn km, $81.3bn,
  −1.1%, $3,746 gold.
- **A date check** — stories first reported on Tuesday 17 November
  are left out, and events that had not happened yet on Wednesday
  (the Trump–Xi–Putin summit, Cyclone Akvan's landfall) are marked
  as not yet news.

## How it is built

`build_image.py` lays out the whole page with Pillow over the
pre-rendered illustrations in `illustrations/` — no network, no
randomness. Running it twice produces a byte-identical PNG
(`entry.png`, 1024×1024, under 1 MiB). `main.py` verifies the PNG
and copies it to `/output/entry.png`.

```sh
python3 build_image.py   # writes entry.png
python3 main.py          # writes /output/entry.png
```

## Sources

Reuters · AP · AFP · DW · Al Jazeera · NPR · CBS · Fed · ONS · IMD ·
NASA · Amnesty · WHO · Bloomberg · ATP · AAP · Daily Star.
All illustrations are original AI artwork.
