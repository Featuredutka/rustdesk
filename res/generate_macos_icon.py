#!/usr/bin/env python3
"""Generate flutter/macos/Runner/AppIcon.icns from flutter/assets/icon.png."""

from pathlib import Path

import io

from icnsutil import IcnsFile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "flutter" / "assets" / "icon.png"
OUT = ROOT / "flutter" / "macos" / "Runner" / "AppIcon.icns"

# macOS icon sizes (points @ scale)
SIZES = [
    (16, 1),
    (16, 2),
    (32, 1),
    (32, 2),
    (128, 1),
    (128, 2),
    (256, 1),
    (256, 2),
    (512, 1),
    (512, 2),
]


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Missing source icon: {SRC}")

    img = Image.open(SRC).convert("RGBA")
    icns = IcnsFile()
    for size, scale in SIZES:
        px = size * scale
        resized = img.resize((px, px), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        suffix = "@2x" if scale == 2 else ""
        name = f"icon_{size}{suffix}.png"
        resized.save(buf, format="PNG")
        icns.add_media(file=name, data=buf.getvalue())

    OUT.parent.mkdir(parents=True, exist_ok=True)
    icns.write(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
