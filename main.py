#!/usr/bin/env python3
"""Entry program for the news-image-20261118 bounty (round 2).

Copies the pre-drawn entry.png (a one-page front page summing up
Wednesday 18 November 2026 world news in 40 stories) to the output
directory that make.fun reads. Standard library only, no network,
deterministic: the output bytes are always identical to the shipped
The bounty caps the image at 1 MiB (1,048,576 bytes), so the program
refuses to write any entry.png larger than that instead of silently
producing an oversize output the scorer would reject.
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # bounty cap: entry.png must be at most 1 MiB


def main():
    if not SRC.is_file():
        raise SystemExit("entry.png is missing next to main.py")
    data = SRC.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        raise SystemExit(
            f"entry.png is {len(data)} bytes, over the 1 MiB bounty cap"
        )
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.png"
    out_path.write_bytes(data)
    # Confirm the copy is byte-identical to the shipped image.
    if out_path.read_bytes() != data:
        raise SystemExit("output entry.png does not match the shipped image")


if __name__ == "__main__":
    main()
