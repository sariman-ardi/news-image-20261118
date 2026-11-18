"""Write the 18 November 2026 world-news image to the output directory.

The image (entry.png) is built by build_image.py from the day's reported
news and shipped in this repository. This program only copies it to
$MAKEFUN_OUTPUT_DIR/entry.png, so every run writes identical bytes.
Standard library only; no network.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    if not os.path.isfile(SRC):
        print("entry.png is missing from the repository", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    # Determinism check: the output must be byte-identical to the source.
    if sha256(SRC) != sha256(dst):
        print("output does not match entry.png", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
