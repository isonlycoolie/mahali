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


# ---------------------------------------------------------------- README banner
W, H = 1600, 760
random.seed(7)

# Terrain: a halftone field whose dots swell over a few soft hills, like a map seen from far above.
HILLS = [(720, 150, 230, 0.9), (800, 650, 250, 1.0), (1560, 110, 230, 0.95), (1540, 720, 210, 0.85), (1180, 40, 200, 0.6), (420, 740, 240, 0.45)]


def height(x, y):
    v = sum(w * math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (r * r)) for cx, cy, r, w in HILLS)
    return max(0.0, min(1.0, v + 0.08 * math.sin(x / 70) * math.cos(y / 55)))


dots = []
for gy in range(0, H + 14, 14):
    for gx in range(0, W + 14, 14):
        x, y = gx + (7 if (gy // 14) % 2 else 0), gy
        v = height(x, y)
        r = 0.5 + 4.4 * v
        if r > 0.9:
            dots.append(f'<circle cx="{x}" cy="{y}" r="{r:.2f}" fill="{GREEN}" fill-opacity="{0.18 + 0.62 * v:.2f}"/>')

PINS = [(722, 168), (808, 646), (1548, 150)]
rings = "".join(
    f'<circle cx="{px}" cy="{py}" r="{rr}" fill="none" stroke="{GREEN}" stroke-opacity="{0.34 - rr / 700:.2f}" stroke-width="1.2"/>'
    for px, py in PINS for rr in (46, 92, 138, 184))
pins = "".join(mark(GREEN, INK, px - 16, py - 40, 32) for px, py in PINS)

defs = (
    f'<linearGradient id="veil" x1="0" x2="1"><stop offset="0" stop-color="{INK}" stop-opacity="0.97"/>'
    f'<stop offset="0.3" stop-color="{INK}" stop-opacity="0.86"/><stop offset="0.55" stop-color="{INK}" stop-opacity="0.42"/><stop offset="1" stop-color="{INK}" stop-opacity="0.3"/></linearGradient>'
    f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{INK}" stop-opacity="0.55"/>'
    f'<stop offset="0.3" stop-color="{INK}" stop-opacity="0"/><stop offset="0.7" stop-color="{INK}" stop-opacity="0"/>'
    f'<stop offset="1" stop-color="{INK}" stop-opacity="0.6"/></linearGradient>'
    '<filter id="lift" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur in="SourceAlpha" stdDeviation="28"/>'
    '<feOffset dy="24"/><feComponentTransfer><feFuncA type="linear" slope="0.55"/></feComponentTransfer>'
    '<feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
)

# Left: app icon, wordmark and line.
left = [f'<rect x="120" y="200" width="96" height="96" rx="21.6" fill="{CARD}" stroke="{LINE}"/>', mark(GREEN, CARD, 144, 224, 48)]
size = 84 / ink_height(HEAD, "M", 1)
left.append(text("MAHALI", HEAD, size, 116, 428, LIGHT, tracking=0.0, bold=size * 0.012)[0])
left.append(text("Every place in Tanzania,", MED, 38, 120, 508, LIGHT, tracking=-0.01)[0])
left.append(text("from region down to street.", MED, 38, 120, 556, MUTED, tracking=-0.01)[0])


# Right: the dropdown people meet in a form, with real Dar es Salaam places.
def field(y, label, value, focused=False, placeholder=False):
    out = [text(label, MED, 15, 962, y, MUTED)[0],
           f'<rect x="962" y="{y + 12}" width="476" height="52" rx="12" fill="{INK}" stroke="{GREEN if focused else LINE}" stroke-width="{1.6 if focused else 1}"/>',
           text(value, REG, 18, 980, y + 44, MUTED if placeholder else LIGHT)[0],
           f'<path d="M1408 {y + 34}l6 6l6 -6" fill="none" stroke="{MUTED}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>']
    return "".join(out)


card = [f'<rect x="930" y="108" width="540" height="566" rx="24" fill="{CARD}" stroke="{LINE}"/>',
        field(156, "Region", "Dar es Salaam"), field(250, "District", "Kinondoni"), field(344, "Ward", "Choose", focused=True, placeholder=True)]
top = 424
card.append(f'<rect x="962" y="{top}" width="476" height="222" rx="14" fill="#232428" stroke="{LINE}"/>')
card.append(f'<circle cx="988" cy="{top + 25}" r="6.5" fill="none" stroke="{MUTED}" stroke-width="1.8"/>'
            f'<path d="M993 {top + 30}l5 5" stroke="{MUTED}" stroke-width="1.8" stroke-linecap="round"/>')
typed, tw = text("Ma", REG, 17, 1008, top + 31, LIGHT)
card.append(typed + f'<rect x="{1010 + tw:.1f}" y="{top + 15}" width="1.6" height="21" fill="{GREEN}"/>')
card.append(f'<rect x="962" y="{top + 49}" width="476" height="1" fill="{LINE}"/>')
for i, ward in enumerate(["Mabwepande", "Magomeni", "Makongo", "Makumbusho", "Mwananyamala"]):
    y = top + 58 + i * 32
    if ward == "Makongo":
        card.append(f'<rect x="970" y="{y}" width="460" height="30" rx="8" fill="#FFFFFF" fill-opacity="0.06"/>'
                    f'<path d="M1404 {y + 15}l5 5l9 -10" fill="none" stroke="{GREEN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    card.append(text(ward, MED if ward == "Makongo" else REG, 16, 984, y + 20, LIGHT)[0])

banner = (f'<rect width="{W}" height="{H}" fill="{INK}"/>' + "".join(dots) + rings + pins
          + f'<rect width="{W}" height="{H}" fill="url(#veil)"/><rect width="{W}" height="{H}" fill="url(#fade)"/>'
          + "".join(left) + f'<g filter="url(#lift)">{"".join(card)}</g>')
write("banner.svg", svg(W, H, banner, defs))
print("wrote", sorted(os.listdir(OUT)))
