"""Generate the mahali brand SVGs into ../svg: mark, lockup, app icon and the README banner.

Every letter is outlined, so the files need no font. The outlines come from Stack Sans Headline (wordmark)
and Switzer (interface text); point MAHALI_FONTS at a folder holding StackSansHeadline-400.woff2 and
Switzer-400/500/600.woff2.

Run from the repo root: python -I brand/build/make_brand.py
"""
import math
import os
import random

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "svg")
FONTS = os.environ.get("MAHALI_FONTS", os.path.join(HERE, "..", "..", "..", "studioonxend", "apps", "landing", "src", "app", "fonts"))
os.makedirs(OUT, exist_ok=True)

INK = "#141517"
CARD = "#1C1D20"
LINE = "#2A2B2F"
LIGHT = "#F0F0F0"
MUTED = "#8E8E93"
GREEN = "#1EB53A"

# The mark, 48 x 48: a drop with three round corners and one point (the place), and the dot that marks it.
DROP = "M0 24A24 24 0 0 1 24 0A24 24 0 0 1 48 24A24 24 0 0 1 24 48H0Z"


def mark(drop, dot, x=0.0, y=0.0, size=48.0):
    s = size / 48
    return (f'<g transform="translate({x:.2f} {y:.2f}) scale({s:.5f})">'
            f'<path d="{DROP}" fill="{drop}"/><circle cx="24" cy="24" r="9" fill="{dot}"/></g>')


def svg(w, h, body, defs=""):
    d = f"<defs>{defs}</defs>" if defs else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="mahali"><title>mahali</title>{d}{body}</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


_fonts = {}


def text(s, font, size, x, y, fill, tracking=0.0, bold=0.0):
    """Outlines s with its baseline at y; returns the path and the advance width."""
    f = _fonts.setdefault(font, TTFont(os.path.join(FONTS, font)))
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    k = size / f["head"].unitsPerEm
    pen, cx = SVGPathPen(gs), 0.0
    for ch in s:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x + cx, y)))
        cx += gs[g].width * k + tracking * size
    stroke = f' stroke="{fill}" stroke-width="{bold:.2f}" stroke-linejoin="round"' if bold else ""
    return f'<path d="{pen.getCommands()}" fill="{fill}"{stroke}/>', cx - tracking * size


def ink_height(font, s, size):
    f = _fonts.setdefault(font, TTFont(os.path.join(FONTS, font)))
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    b = BoundsPen(gs)
    for ch in s:
        gs[cmap[ord(ch)]].draw(b)
    return (b.bounds[3] - b.bounds[1]) * size / f["head"].unitsPerEm


HEAD = "StackSansHeadline-400.woff2"
REG, MED, SEMI = "Switzer-400.woff2", "Switzer-500.woff2", "Switzer-600.woff2"


def lockup(drop, dot, word, h=48):
    """Mark plus the MAHALI wordmark, cap height two thirds of the mark, centred on it."""
    size = h * 0.66 / (ink_height(HEAD, "M", 1) or 1)
    cap = ink_height(HEAD, "M", size)
    path, width = text("MAHALI", HEAD, size, h * 1.33, h / 2 + cap / 2, word, tracking=0.0, bold=size * 0.012)
    return mark(drop, dot, 0, 0, h) + path, h * 1.33 + width


def app_icon(tile, drop, dot, s=1024):
    return svg(s, s, f'<rect width="{s}" height="{s}" rx="{s * 0.225:.1f}" fill="{tile}"/>' + mark(drop, dot, s * 0.25, s * 0.25, s * 0.5))


# The dot takes the background's colour, so it reads as a hole in the drop.
write("mark.svg", svg(48, 48, mark(GREEN, "#FFFFFF")))
write("mark-on-dark.svg", svg(48, 48, mark(GREEN, INK)))
for name, dot, word in (("lockup.svg", "#FFFFFF", INK), ("lockup-on-dark.svg", INK, LIGHT)):
    body, w = lockup(GREEN, dot, word)
    write(name, svg(math.ceil(w + 2), 48, body))
write("app-icon.svg", app_icon(INK, GREEN, INK))
write("app-icon-light.svg", app_icon(LIGHT, GREEN, LIGHT))
