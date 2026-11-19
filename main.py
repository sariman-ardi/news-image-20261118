"""Copy the 18 November 2026 world-news poster to the output directory."""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(DST_DIR, "entry.png")

os.makedirs(DST_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)
with open(DST, "rb") as f:
    magic = f.read(8)
if magic != b"\x89PNG\r\n\x1a\n":
    raise SystemExit("output is not a PNG file: " + DST)
print("wrote", DST, os.path.getsize(DST), "bytes")
