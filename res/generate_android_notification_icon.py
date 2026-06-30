#!/usr/bin/env python3
"""Generate Android notification icons (ic_stat_logo) from res/icon.png."""

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "res" / "notification_icon.png"
if not SRC.is_file():
    SRC = ROOT / "res" / "icon.png"

OUT_DIR = ROOT / "flutter" / "android" / "app" / "src" / "main" / "res"

# Android notification small-icon sizes (px).
SIZES = {
    "mipmap-mdpi": 24,
    "mipmap-hdpi": 36,
    "mipmap-xhdpi": 48,
    "mipmap-xxhdpi": 72,
    "mipmap-xxxhdpi": 96,
}


def _is_background(r: int, g: int, b: int, a: int) -> bool:
    if a < 16:
        return True
    return r > 230 and g > 230 and b > 230


def to_notification_icon(img: Image.Image, size: int) -> Image.Image:
    fitted = ImageOps.fit(img.convert("RGBA"), (size, size), Image.Resampling.LANCZOS)
    out = Image.new("RGBA", fitted.size, (0, 0, 0, 0))
    src_px = fitted.load()
    out_px = out.load()
    for y in range(fitted.height):
        for x in range(fitted.width):
            r, g, b, a = src_px[x, y]
            if _is_background(r, g, b, a):
                continue
            out_px[x, y] = (255, 255, 255, max(a, 220))
    return out


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Missing source icon: {SRC}")

    img = Image.open(SRC)
    for folder, px in SIZES.items():
        out = OUT_DIR / folder / "ic_stat_logo.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        to_notification_icon(img, px).save(out, format="PNG")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
