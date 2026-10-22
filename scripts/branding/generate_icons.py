#!/usr/bin/env python3
"""
Sidely icon generator.

Renders the Sidely app icon (and every alternate icon) from one geometry
definition, so the whole icon pack can be restyled by editing the PALETTES
table below.

Usage:
    python scripts/branding/generate_icons.py

Requires: Pillow, numpy.

Outputs:
    AltStore/Resources/Icons.xcassets/AppIcon.appiconset/*.png
    AltStore/Resources/Icons.xcassets/Modern/*.appiconset/*.png
    AltStore/Resources/Icons.xcassets/Modern/*.imageset/*.png  (picker previews)
    AltStore/Resources/Assets.xcassets/Sidely.imageset/1024.png
    AltWidget/Assets.xcassets/Sidely.imageset/1024.png
    AltWidget/Assets.xcassets/Badge.imageset/sidely-logo.svg
    branding/SidelyIcon-1024.png
    branding/SidelyIcon-preview.png
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

BASE = 1024
SS = 4  # supersampling factor
CANVAS = BASE * SS


@dataclass(frozen=True)
class Palette:
    name: str
    stops: tuple[tuple[float, float, float], ...]
    glyph: str = "#FFFFFF"
    shadow_alpha: int = 70
    rainbow: bool = False


# Each palette is a diagonal multi-stop gradient. Add/remove palettes here and
# also add/remove the matching entry in AltStore/Resources/AltIcons.plist.
PALETTES: dict[str, Palette] = {
    "AppIcon": Palette(
        "Aurora",
        ((0.36, 0.24, 0.95), (0.58, 0.28, 0.98), (0.05, 0.72, 0.88)),
    ),
    "BlueIcon": Palette(
        "Blue", ((0.06, 0.16, 0.44), (0.15, 0.39, 0.92), (0.34, 0.65, 0.98))
    ),
    "DarkIcon": Palette(
        "Dark", ((0.03, 0.05, 0.11), (0.09, 0.13, 0.22), (0.19, 0.24, 0.33))
    ),
    "HoneydewIcon": Palette(
        "Honeydew",
        ((0.62, 0.94, 0.78), (0.20, 0.83, 0.60), (0.02, 0.51, 0.40)),
        glyph="#073B32",
        shadow_alpha=45,
    ),
    "PrideIcon": Palette(
        "Pride", ((0.93, 0.16, 0.29), (0.99, 0.55, 0.09), (1.0, 0.90, 0.13)),
        rainbow=True,
    ),
    "SandyIcon": Palette(
        "Sandy", ((0.99, 0.90, 0.54), (0.96, 0.62, 0.07), (0.71, 0.33, 0.04))
    ),
    "SkyIcon": Palette(
        "Sky", ((0.73, 0.90, 0.99), (0.22, 0.74, 0.97), (0.01, 0.52, 0.78))
    ),
    "SnowIcon": Palette(
        "Snow",
        ((1.0, 1.0, 1.0), (0.90, 0.93, 0.97), (0.65, 0.71, 0.80)),
        glyph="#1E293B",
        shadow_alpha=30,
    ),
    "StarburstIcon": Palette(
        "Starburst", ((0.96, 0.45, 0.71), (0.96, 0.62, 0.04), (0.99, 0.90, 0.20))
    ),
    "StormIcon": Palette(
        "Storm", ((0.04, 0.06, 0.11), (0.20, 0.25, 0.33), (0.42, 0.48, 0.57))
    ),
    "VistaIcon": Palette(
        "Vista", ((0.02, 0.65, 0.91), (0.02, 0.72, 0.65), (0.52, 0.80, 0.09))
    ),
    "WinterIcon": Palette(
        "Winter", ((0.07, 0.18, 0.55), (0.04, 0.53, 0.80), (0.88, 0.95, 0.99))
    ),
}

RAINBOW_STOPS = (
    (0.92, 0.12, 0.20),
    (0.98, 0.45, 0.08),
    (0.99, 0.82, 0.10),
    (0.15, 0.72, 0.35),
    (0.06, 0.45, 0.90),
    (0.42, 0.20, 0.72),
)


def _hex(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def _gradient(stops: tuple[tuple[float, float, float], ...]) -> Image.Image:
    """Diagonal gradient with slight dithering to avoid banding."""
    y, x = np.mgrid[0:CANVAS, 0:CANVAS]
    t = (x + y) / (2.0 * (CANVAS - 1))
    t = np.clip(t, 0.0, 1.0)

    positions = np.linspace(0.0, 1.0, len(stops))
    rgb = np.empty((CANVAS, CANVAS, 3), dtype=np.float32)
    for channel in range(3):
        rgb[..., channel] = np.interp(
            t, positions, [stop[channel] for stop in stops]
        )
    # Subtle noise hides 8-bit banding on big gradients.
    rng = np.random.default_rng(7)
    rgb += rng.normal(0.0, 0.0018, size=(CANVAS, CANVAS, 1))
    rgb = np.clip(rgb, 0.0, 1.0)
    return Image.fromarray((rgb * 255).astype(np.uint8), "RGB")


def _rainbow() -> Image.Image:
    y, x = np.mgrid[0:CANVAS, 0:CANVAS]
    t = (x + y) / (2.0 * (CANVAS - 1))
    positions = np.linspace(0.0, 1.0, len(RAINBOW_STOPS))
    rgb = np.empty((CANVAS, CANVAS, 3), dtype=np.float32)
    for channel in range(3):
        rgb[..., channel] = np.interp(
            t, positions, [stop[channel] for stop in RAINBOW_STOPS]
        )
    return Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")


def _radial_glow(img: Image.Image) -> Image.Image:
    """Soft light source in the top-left, plus a gentle vignette."""
    y, x = np.mgrid[0:CANVAS, 0:CANVAS].astype(np.float32)
    cx, cy = CANVAS * 0.26, CANVAS * 0.18
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / (CANVAS * 0.75)
    glow = np.clip(1.0 - dist, 0.0, 1.0) ** 2 * 0.16

    arr = np.asarray(img).astype(np.float32) / 255.0
    arr = arr + (1.0 - arr) * glow[..., None]
    arr = np.clip(arr, 0.0, 1.0)
    return Image.fromarray((arr * 255).astype(np.uint8), "RGB")


def _glyph_layer(color: str) -> Image.Image:
    """Rounded download arrow dropping into an open tray."""
    layer = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    s = SS
    w = 84 * s
    r = w // 2

    def line(points, width=w):
        d.line([(px * s, py * s) for px, py in points], fill=color, width=width, joint="curve")

    # Tray: open-top U with rounded bottom corners.
    line([(240, 586), (240, 748), (312, 820), (712, 820), (784, 748), (784, 586)])
    for px, py in ((240, 586), (784, 586)):
        d.ellipse(
            ((px * s) - r, (py * s) - r, (px * s) + r, (py * s) + r), fill=color
        )

    # Arrow shaft + solid head.
    line([(512, 178), (512, 520)])
    d.polygon(
        [(362 * s, 486 * s), (662 * s, 486 * s), (512 * s, 646 * s)], fill=color
    )
    return layer


def render_icon(palette: Palette) -> Image.Image:
    background = _rainbow() if palette.rainbow else _gradient(palette.stops)
    background = _radial_glow(background).convert("RGBA")

    glyph = _glyph_layer(palette.glyph)

    shadow = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    shadow.paste(glyph, (0, 0), glyph)
    shadow = shadow.filter(ImageFilter.GaussianBlur(18 * SS))
    alpha = shadow.getchannel("A").point(
        lambda a: int(a * palette.shadow_alpha / 255)
    )
    shadow.putalpha(alpha)

    background.alpha_composite(shadow, (0, 20 * SS))
    background.alpha_composite(glyph)
    return background.convert("RGB")


def _contents(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_appicon_set(appiconset: str, master: Image.Image) -> None:
    contents = _contents(os.path.join(appiconset, "Contents.json"))
    for image in contents.get("images", []):
        filename = image.get("filename")
        if not filename:
            continue
        if image.get("size") and image.get("scale"):
            points = float(image["size"].split("x")[0])
            scale = int(image["scale"].rstrip("x"))
            px = round(points * scale)
        elif image.get("size"):
            px = int(float(image["size"].split("x")[0]))
        else:
            px = 1024
        master.resize((px, px), Image.LANCZOS).save(
            os.path.join(appiconset, filename), optimize=True
        )


def write_imageset(imageset: str, master: Image.Image) -> None:
    contents = _contents(os.path.join(imageset, "Contents.json"))
    for image in contents.get("images", []):
        filename = image.get("filename")
        if filename and filename.lower().endswith(".png"):
            master.resize((1024, 1024), Image.LANCZOS).save(
                os.path.join(imageset, filename), optimize=True
            )


BADGE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <g fill="none" stroke="#bebbb4" stroke-width="7.6" stroke-linecap="round" stroke-linejoin="round">
    <path d="M23.5 57.5 V73.2 Q23.5 80.1 30.4 80.1 H69.6 Q76.5 80.1 76.5 73.2 V57.5"/>
    <path d="M50 17.5 V54.5"/>
    <path d="M35 47.5 L50 64 L65 47.5"/>
  </g>
</svg>
"""


def main() -> None:
    masters = {name: render_icon(p) for name, p in PALETTES.items()}

    icons_root = os.path.join(ROOT, "AltStore", "Resources", "Icons.xcassets")
    write_appicon_set(os.path.join(icons_root, "AppIcon.appiconset"), masters["AppIcon"])

    for name, master in masters.items():
        if name == "AppIcon":
            continue
        appicon = os.path.join(icons_root, "Modern", f"{name}.appiconset")
        preview = os.path.join(icons_root, "Modern", f"{name.removesuffix('Icon')}.imageset")
        if os.path.isdir(appicon):
            write_appicon_set(appicon, master)
        if os.path.isdir(preview):
            write_imageset(preview, master)

    # In-app logo used by the splash screen/widgets.
    for imageset in (
        os.path.join(ROOT, "AltStore", "Resources", "Assets.xcassets", "Sidely.imageset"),
        os.path.join(ROOT, "AltWidget", "Assets.xcassets", "Sidely.imageset"),
    ):
        write_imageset(imageset, masters["AppIcon"])

    badge_dir = os.path.join(ROOT, "AltWidget", "Assets.xcassets", "Badge.imageset")
    with open(os.path.join(badge_dir, "sidely-logo.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(BADGE_SVG)

    branding_dir = os.path.join(ROOT, "branding")
    os.makedirs(branding_dir, exist_ok=True)
    masters["AppIcon"].save(os.path.join(branding_dir, "SidelyIcon-1024.png"))

    # Contact sheet for quick visual review.
    cell = 256
    cols = 4
    rows = math.ceil(len(masters) / cols)
    sheet = Image.new("RGB", (cols * cell, rows * cell), "#0B1020")
    for index, master in enumerate(masters.values()):
        sheet.paste(
            master.resize((cell, cell), Image.LANCZOS),
            ((index % cols) * cell, (index // cols) * cell),
        )
    sheet.save(os.path.join(branding_dir, "SidelyIcon-preview.png"))

    print(f"Generated {len(masters)} icon variants for Sidely.")


if __name__ == "__main__":
    main()
