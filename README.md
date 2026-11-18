[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/sariman-ardi/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/sariman-ardi/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

# World News in One Image — 18 November 2026

One image that sums up Wednesday 18 November 2026's world news, built for
the [make.fun bounty](https://make.fun/bounty/news-image-20261118)
"news-image-20261118" (total prize $250, 1st place $50).

## The six stories

1. **Ukraine hits Crimean Bridge again** — Kyiv strikes the bridge for a
   second day as Russia hits bridges in Kyiv.
2. **Iran drones target US radar in Bahrain** — the US says the drones were
   intercepted; US jets hit a missile site on Qeshm Island in reply.
3. **Trump lands in Manila for Quad talks** — the US president joins Quad
   leaders before a planned visit to China.
4. **Nvidia sales double to $115.8bn** — the board rules out bringing back
   ex-CEO Jensen Huang after a record quarter.
5. **Cyclone Akvan gains strength** — the storm over the Bay of Bengal is
   set to become severe by 19 November.
6. **US loses measles-free status** — PAHO ends the 26-year status after
   5,412 cases in 2026, the most since 1991.

Sources: Reuters, AP, The Guardian, PAHO, Nvidia, IMD.

## The image

`entry.png` (1024×1024, PNG) is a clean infographic drawn with Python's
Pillow library: a dated header, one panel per story with a short headline,
one line of summary and a small drawn icon. No photographs and no
downloaded artwork — every pixel is drawn by the build script.

## How to run

```sh
python3 build_image.py        # rebuild entry.png from the news data
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` uses only the Python standard library, needs no network, and
copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. Running it twice
writes byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
