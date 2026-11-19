"""Entrypoint: copy the pre-rendered poster to /output/entry.png.

The poster itself is drawn by build_image.py (Pillow layout over
pre-rendered AI illustrations, no network, deterministic). This
entrypoint only verifies the file is a real PNG and places it where
the harness expects it.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    with open(SRC, "rb") as f:
        magic = f.read(8)
    if magic != PNG_MAGIC:
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    if os.path.getsize(SRC) != os.path.getsize(DST):
        print("copy size mismatch", file=sys.stderr)
        return 1
    # The copy must be byte-identical to the poster the build produced.
    print("wrote", DST, os.path.getsize(DST), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
