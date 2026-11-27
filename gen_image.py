#!/usr/bin/env python3
"""Draw the news-image-20261126 entry: 'THE WORLD IN ONE DAY' — Thursday 26 November 2026.

Fresh code, written from the prose brief for this edition only.
Draws a 1024x1024 PNG with PIL, no network, no randomness, no timestamps:
two runs produce byte-identical output.
Usage: python3 gen_image.py [out_path]   (default: entry.png next to this file)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

INK = (26, 26, 26)
PAPER = (247, 243, 234)
CARD_BG = (255, 255, 255)
CARD_LINE = (203, 199, 188)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
GREY = (90, 88, 82)
LIGHT_GREY = (120, 118, 110)
MAP_BG = (214, 230, 240)
MAP_LAND = (226, 220, 196)
MAP_LINE = (150, 142, 118)

REGION_COLORS = {
    "Europe": (29, 78, 216),
    "Middle East": (180, 83, 9),
    "East Asia": (15, 118, 110),
    "Southeast Asia": (109, 40, 217),
    "South Asia": (190, 24, 93),
    "Africa": (21, 128, 61),
    "North America": (185, 28, 28),
    "Latin America": (161, 98, 7),
    "Oceania": (3, 105, 161),
    "Global": (71, 85, 105),
}

TAG_COLORS = {
    "OFFICIAL": (21, 128, 61),
    "REPORTED": (29, 78, 216),
    "CLAIM": (220, 38, 38),
    "CONFIRMED": (20, 83, 45),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF_R = lambda s: font("DejaVuSerif.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines, min_size=None):
    """Wrap text to <= max_lines; shrink font one step at a time if needed.
    Returns (lines, font_used). Truncates with an ellipsis only as last resort."""
    f = fnt
    size = f.size
    while True:
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines or (min_size is not None and size <= min_size):
            break
        size -= 1
        fname = f.path
        f = ImageFont.truetype(fname, size)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        # trim last line until the ellipsis fits
        while lines and draw.textlength(lines[-1] + " ...", font=f) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = (lines[-1] + " ...").strip()
    return lines, f


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def centered(draw, cx, y, s, fnt, fill=INK):
    draw.text((cx, y), s, font=fnt, fill=fill, anchor="ma")


# ---------------------------------------------------------------- scenes
# Each scene draws a simple vector illustration inside box (x, y, w, h).

def scene_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(23, 32, 58))
    # stars
    for sx, sy in [(0.12, 0.2), (0.3, 0.12), (0.55, 0.25), (0.78, 0.14), (0.9, 0.3)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1], fill=(255, 255, 255))
    # missile trails (orange arcs)
    d.line([x + w * 0.15, y + h * 0.9, x + w * 0.45, y + h * 0.25], fill=(249, 115, 22), width=3)
    d.line([x + w * 0.7, y + h * 0.95, x + w * 0.85, y + h * 0.4], fill=(249, 115, 22), width=3)
    d.ellipse([x + w * 0.42, y + h * 0.18, x + w * 0.5, y + h * 0.32], fill=(251, 191, 36))
    # skyline
    for i, (bx, bw, bh) in enumerate([(0.02, 0.16, 0.45), (0.2, 0.12, 0.6), (0.34, 0.18, 0.38), (0.54, 0.14, 0.55), (0.7, 0.16, 0.42), (0.88, 0.1, 0.5)]):
        d.rectangle([x + w * bx, y + h * (1 - bh), x + w * (bx + bw), y + h], fill=(12, 18, 38))
        for wy in range(3):
            d.rectangle([x + w * (bx + 0.03), y + h * (1 - bh + 0.08 + wy * 0.14),
                         x + w * (bx + 0.06), y + h * (1 - bh + 0.12 + wy * 0.14)], fill=(251, 191, 36))
    # explosion at mall
    d.ellipse([x + w * 0.55, y + h * 0.55, x + w * 0.75, y + h * 0.85], fill=(234, 88, 12))
    d.ellipse([x + w * 0.6, y + h * 0.62, x + w * 0.7, y + h * 0.78], fill=(253, 224, 71))


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(124, 45, 18))
    # apartment block
    d.rectangle([x + w * 0.1, y + h * 0.3, x + w * 0.55, y + h], fill=(68, 64, 60))
    for r in range(3):
        for c in range(4):
            d.rectangle([x + w * (0.14 + c * 0.1), y + h * (0.36 + r * 0.2),
                         x + w * (0.2 + c * 0.1), y + h * (0.48 + r * 0.2)], fill=(253, 230, 138))
    # damaged corner + smoke
    d.polygon([(x + w * 0.55, y + h * 0.3), (x + w * 0.62, y + h * 0.45), (x + w * 0.55, y + h * 0.55)],
              fill=(41, 37, 36))
    d.ellipse([x + w * 0.6, y + h * 0.1, x + w * 0.78, y + h * 0.35], fill=(120, 113, 108))
    d.ellipse([x + w * 0.68, y + h * 0.02, x + w * 0.82, y + h * 0.2], fill=(87, 83, 78))
    # blast flash
    d.polygon([(x + w * 0.58, y + h * 0.5), (x + w * 0.66, y + h * 0.38), (x + w * 0.7, y + h * 0.52),
               (x + w * 0.78, y + h * 0.44), (x + w * 0.72, y + h * 0.6), (x + w * 0.8, y + h * 0.62),
               (x + w * 0.68, y + h * 0.7), (x + w * 0.62, y + h * 0.64)], fill=(251, 191, 36))
    # ground line
    d.rectangle([x, y + h * 0.92, x + w, y + h], fill=(41, 37, 36))


def scene_cairo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(254, 243, 199))
    # ring road
    d.rectangle([x, y + h * 0.72, x + w, y + h * 0.85], fill=(87, 83, 78))
    d.line([x, y + h * 0.78, x + w, y + h * 0.78], fill=(255, 255, 255), width=2)
    # tanker truck on its side
    d.rounded_rectangle([x + w * 0.18, y + h * 0.42, x + w * 0.62, y + h * 0.68], radius=8, fill=(185, 28, 28))
    d.rectangle([x + w * 0.62, y + h * 0.5, x + w * 0.74, y + h * 0.68], fill=(41, 37, 36))
    d.ellipse([x + w * 0.3, y + h * 0.64, x + w * 0.38, y + h * 0.74], fill=(26, 26, 26))
    d.ellipse([x + w * 0.52, y + h * 0.64, x + w * 0.6, y + h * 0.74], fill=(26, 26, 26))
    # flames
    d.polygon([(x + w * 0.3, y + h * 0.42), (x + w * 0.38, y + h * 0.12), (x + w * 0.44, y + h * 0.34),
               (x + w * 0.52, y + h * 0.08), (x + w * 0.58, y + h * 0.42)], fill=(234, 88, 12))
    d.polygon([(x + w * 0.38, y + h * 0.42), (x + w * 0.44, y + h * 0.26), (x + w * 0.5, y + h * 0.42)],
              fill=(253, 224, 71))
    # smoke
    d.ellipse([x + w * 0.7, y + h * 0.08, x + w * 0.86, y + h * 0.3], fill=(120, 113, 108))
    d.ellipse([x + w * 0.78, y + h * 0.02, x + w * 0.9, y + h * 0.18], fill=(87, 83, 78))


def scene_bears(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 101, 52))
    # yard lines
    for i in range(6):
        lx = x + w * (0.08 + i * 0.17)
        d.line([lx, y, lx, y + h], fill=(255, 255, 255), width=2)
    # football
    d.ellipse([x + w * 0.32, y + h * 0.3, x + w * 0.68, y + h * 0.7], fill=(124, 45, 18))
    d.line([x + w * 0.38, y + h * 0.5, x + w * 0.62, y + h * 0.5], fill=(255, 255, 255), width=2)
    for lx in [0.44, 0.5, 0.56]:
        d.line([x + w * lx, y + h * 0.44, x + w * lx, y + h * 0.56], fill=(255, 255, 255), width=2)
    # scoreboard, top-right (kept clear of the number badge at top-left)
    d.rectangle([x + w * 0.58, y + h * 0.06, x + w * 0.94, y + h * 0.26], fill=(26, 26, 26))
    d.text((x + w * 0.61, y + h * 0.09), "39-35", font=F_BOLD(max(10, int(h * 0.14))), fill=(253, 224, 71))


def scene_bangkok(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(254, 226, 226))
    # refinery towers
    for bx, bw, bh in [(0.08, 0.12, 0.6), (0.24, 0.1, 0.75), (0.38, 0.14, 0.5), (0.56, 0.1, 0.68)]:
        d.rectangle([x + w * bx, y + h * (1 - bh), x + w * (bx + bw), y + h], fill=(68, 64, 60))
        d.rectangle([x + w * (bx + 0.02), y + h * (1 - bh - 0.08), x + w * (bx + bw - 0.02), y + h * (1 - bh)],
                    fill=(41, 37, 36))
    # pipes
    d.line([x + w * 0.1, y + h * 0.85, x + w * 0.9, y + h * 0.85], fill=(41, 37, 36), width=4)
    # flame + smoke
    d.polygon([(x + w * 0.66, y + h * 0.55), (x + w * 0.72, y + h * 0.25), (x + w * 0.78, y + h * 0.45),
               (x + w * 0.84, y + h * 0.2), (x + w * 0.9, y + h * 0.55)], fill=(234, 88, 12))
    d.ellipse([x + w * 0.72, y + h * 0.02, x + w * 0.88, y + h * 0.22], fill=(87, 83, 78))


def scene_mine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 53, 15))
    # hillside
    d.polygon([(x, y + h), (x + w * 0.35, y + h * 0.25), (x + w, y + h * 0.55), (x + w, y + h)], fill=(68, 64, 60))
    d.polygon([(x, y + h), (x + w * 0.2, y + h * 0.5), (x + w * 0.55, y + h * 0.75), (x + w, y + h)], fill=(87, 83, 78))
    # shaft entrance
    d.rectangle([x + w * 0.38, y + h * 0.55, x + w * 0.58, y + h * 0.85], fill=(26, 26, 26))
    d.rectangle([x + w * 0.34, y + h * 0.5, x + w * 0.62, y + h * 0.56], fill=(41, 37, 36))
    # water pouring out
    d.polygon([(x + w * 0.42, y + h * 0.85), (x + w * 0.54, y + h * 0.85), (x + w * 0.6, y + h),
               (x + w * 0.36, y + h)], fill=(14, 165, 233))
    # rescue helmet
    d.pieslice([x + w * 0.68, y + h * 0.6, x + w * 0.88, y + h * 0.82], 180, 360, fill=(253, 224, 71))
    d.rectangle([x + w * 0.66, y + h * 0.8, x + w * 0.9, y + h * 0.84], fill=(253, 224, 71))
    # rain
    for rx in [0.1, 0.25, 0.75, 0.9]:
        d.line([x + w * rx, y + h * 0.1, x + w * (rx - 0.03), y + h * 0.3], fill=(186, 230, 253), width=2)


def scene_kim(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(69, 10, 10))
    # centrifuge cascades (rows of circles)
    for r in range(3):
        for c in range(5):
            cx = x + w * (0.12 + c * 0.14)
            cy = y + h * (0.22 + r * 0.2)
            d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=(253, 224, 71), width=2)
    # warhead cone
    d.polygon([(x + w * 0.68, y + h * 0.15), (x + w * 0.78, y + h * 0.55), (x + w * 0.58, y + h * 0.55)],
              fill=(226, 232, 240))
    d.rectangle([x + w * 0.6, y + h * 0.55, x + w * 0.76, y + h * 0.68], fill=(148, 163, 184))
    d.rectangle([x + w * 0.55, y + h * 0.68, x + w * 0.81, y + h * 0.74], fill=(100, 116, 139))
    # red banner
    d.rectangle([x, y + h * 0.82, x + w, y + h], fill=(185, 28, 28))
    d.text((x + w * 0.05, y + h * 0.85), "NUCLEAR", font=F_BOLD(max(9, int(h * 0.1))), fill=(255, 255, 255))


def scene_bok(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(219, 234, 254))
    # bank building
    d.rectangle([x + w * 0.12, y + h * 0.45, x + w * 0.88, y + h * 0.9], fill=(255, 255, 255))
    d.polygon([(x + w * 0.08, y + h * 0.45), (x + w * 0.5, y + h * 0.18), (x + w * 0.92, y + h * 0.45)],
              fill=(30, 58, 95))
    for i in range(4):
        cx = x + w * (0.2 + i * 0.2)
        d.rectangle([cx - 4, y + h * 0.48, cx + 4, y + h * 0.88], fill=(30, 58, 95))
    # rising arrow
    d.line([x + w * 0.1, y + h * 0.5, x + w * 0.35, y + h * 0.35, x + w * 0.55, y + h * 0.42,
            x + w * 0.9, y + h * 0.12], fill=(21, 128, 61), width=3)
    d.polygon([(x + w * 0.9, y + h * 0.12), (x + w * 0.8, y + h * 0.12), (x + w * 0.9, y + h * 0.24)],
              fill=(21, 128, 61))
    d.text((x + w * 0.06, y + h * 0.06), "3.25%", font=F_BOLD(max(11, int(h * 0.16))), fill=(21, 128, 61))


def scene_kuwait(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(254, 243, 199))
    # radar station
    d.rectangle([x + w * 0.1, y + h * 0.6, x + w * 0.3, y + h * 0.9], fill=(68, 64, 60))
    d.ellipse([x + w * 0.12, y + h * 0.3, x + w * 0.28, y + h * 0.55], outline=(41, 37, 36), width=3)
    d.line([x + w * 0.2, y + h * 0.42, x + w * 0.34, y + h * 0.28], fill=(41, 37, 36), width=3)
    # drone quadcopter
    cx, cy = x + w * 0.68, y + h * 0.3
    d.rectangle([cx - 14, cy - 5, cx + 14, cy + 5], fill=(26, 26, 26))
    for dx, dy in [(-18, -10), (18, -10), (-18, 10), (18, 10)]:
        d.ellipse([cx + dx - 7, cy + dy - 2, cx + dx + 7, cy + dy + 2], fill=(87, 83, 78))
        d.line([cx, cy, cx + dx, cy + dy], fill=(26, 26, 26), width=2)
    # explosion
    d.polygon([(cx - 6, cy + 22), (cx + 2, cy + 8), (cx + 10, cy + 20), (cx + 18, cy + 8),
               (cx + 14, cy + 24), (cx + 24, cy + 26), (cx + 8, cy + 32), (cx + 2, cy + 30)],
              fill=(234, 88, 12))


def scene_ebola(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(254, 226, 226))
    # virus: circle with spikes
    cx, cy, r = x + w * 0.3, y + h * 0.5, int(h * 0.28)
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        x2, y2 = cx + (r + 9) * math.cos(a), cy + (r + 9) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=(185, 28, 28), width=3)
        d.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=(185, 28, 28))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 38, 38))
    d.ellipse([cx - r // 2, cy - r // 2, cx - r // 6, cy - r // 6], fill=(254, 202, 202))
    # red cross badge
    d.rectangle([x + w * 0.66, y + h * 0.2, x + w * 0.94, y + h * 0.62], fill=(255, 255, 255))
    d.rectangle([x + w * 0.77, y + h * 0.26, x + w * 0.83, y + h * 0.56], fill=(220, 38, 38))
    d.rectangle([x + w * 0.7, y + h * 0.36, x + w * 0.9, y + h * 0.46], fill=(220, 38, 38))
    d.text((x + w * 0.64, y + h * 0.7), "12,021", font=F_BOLD(max(11, int(h * 0.16))), fill=(185, 28, 28))


def scene_uk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(219, 234, 254))
    # falling bars
    bars = [(0.12, 0.75), (0.3, 0.6), (0.48, 0.45), (0.66, 0.28), (0.82, 0.18)]
    for bx, bh in bars:
        d.rectangle([x + w * bx, y + h * (1 - bh), x + w * (bx + 0.12), y + h * 0.95], fill=(29, 78, 216))
    d.line([x + w * 0.08, y + h * 0.95, x + w * 0.95, y + h * 0.95], fill=(26, 26, 26), width=2)
    # plane
    px, py = x + w * 0.72, y + h * 0.18
    d.polygon([(px, py), (px + 26, py + 6), (px, py + 12)], fill=(41, 37, 36))
    d.rectangle([px - 8, py + 3, px + 4, py + 9], fill=(41, 37, 36))
    d.text((x + w * 0.06, y + h * 0.06), "77,000", font=F_BOLD(max(11, int(h * 0.16))), fill=(29, 78, 216))


def scene_nfl(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(23, 32, 58))
    # stadium lights
    for lx in [0.15, 0.5, 0.85]:
        d.line([x + w * lx, y, x + w * lx, y + h * 0.18], fill=(255, 255, 255), width=2)
        d.ellipse([x + w * lx - 7, y + h * 0.14, x + w * lx + 7, y + h * 0.26], fill=(253, 224, 71))
    # field
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(22, 101, 52))
    for i in range(5):
        lx = x + w * (0.1 + i * 0.2)
        d.line([lx, y + h * 0.55, lx, y + h], fill=(255, 255, 255), width=1)
    # scoreboard
    d.rectangle([x + w * 0.28, y + h * 0.28, x + w * 0.72, y + h * 0.5], fill=(26, 26, 26))
    d.text((x + w * 0.31, y + h * 0.3), "39-38", font=F_BOLD(max(11, int(h * 0.16))), fill=(253, 224, 71))
    # football
    d.ellipse([x + w * 0.42, y + h * 0.62, x + w * 0.58, y + h * 0.82], fill=(124, 45, 18))


def scene_unctad(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(219, 234, 254))
    # waves (kept low so they never cross the ship)
    for wy in [0.82, 0.92]:
        d.arc([x - w * 0.1, y + h * wy, x + w * 0.5, y + h * (wy + 0.2)], 180, 360, fill=(14, 165, 233), width=2)
        d.arc([x + w * 0.5, y + h * wy, x + w * 1.1, y + h * (wy + 0.2)], 180, 360, fill=(14, 165, 233), width=2)
    # cargo ship
    d.polygon([(x + w * 0.12, y + h * 0.55), (x + w * 0.88, y + h * 0.55), (x + w * 0.78, y + h * 0.75),
               (x + w * 0.22, y + h * 0.75)], fill=(41, 37, 36))
    for i, col in enumerate([(185, 28, 28), (29, 78, 216), (21, 128, 61), (217, 119, 6)]):
        d.rectangle([x + w * (0.2 + i * 0.16), y + h * 0.38, x + w * (0.34 + i * 0.16), y + h * 0.55], fill=col)
    d.rectangle([x + w * 0.82, y + h * 0.3, x + w * 0.86, y + h * 0.55], fill=(255, 255, 255))
    d.text((x + w * 0.06, y + h * 0.06), "0% GROWTH", font=F_BOLD(max(10, int(h * 0.13))), fill=(30, 58, 95))


SCENES = {
    1: scene_kyiv, 2: scene_gaza, 3: scene_cairo, 4: scene_bears,
    5: scene_bangkok, 6: scene_mine, 7: scene_kim, 8: scene_bok,
    9: scene_kuwait, 10: scene_ebola, 11: scene_uk, 12: scene_nfl,
    13: scene_unctad,
}

# ---------------------------------------------------------------- data

CARDS = [
    dict(n=1, region="Europe", kicker="KYIV · UKRAINE",
         headline="Kyiv hit by missiles, 7 wounded",
         body="Russia fired ballistic missiles + 113 drones overnight; Prospekt mall struck. Air defences downed 87 drones.",
         source="Reuters", tag="CONFIRMED"),
    dict(n=2, region="Middle East", kicker="GAZA · MIDDLE EAST",
         headline="Israel kills 9 in Gaza, incl. Hamas finance chief",
         body="Strike on Deir al-Balah flat kills Khaled Abu Nada + wife; 3rd night of strikes despite ceasefire. 1,600+ dead since Oct 2025.",
         source="Reuters", tag="CONFIRMED"),
    dict(n=3, region="Africa", kicker="CAIRO · EGYPT",
         headline="Cairo tanker inferno: 31 dead, driver held",
         body="Fuel tanker blast on Ring Road burned 27 vehicles. Toll: 31 dead, 26 hurt; driver, 21, detained.",
         source="Reuters / AP", tag="CONFIRMED"),
    dict(n=4, region="North America", kicker="DETROIT · NFL",
         headline="Bears stun Lions 39–35 on Thanksgiving",
         body="Rally from 11 down in the 4th; Odunze's 6-yd TD with 3 secs left wins it.",
         source="NFL / Sportradar", tag="CONFIRMED"),
    dict(n=5, region="Southeast Asia", kicker="BANGKOK · THAILAND",
         headline="Bangkok refinery blast injures 9",
         body="Blast + fire at Bangchak's Phra Khanong refinery; 3 critical. All units shut.",
         source="AP / CNN", tag="CONFIRMED"),
    dict(n=6, region="Southeast Asia", kicker="BOGOR · INDONESIA",
         headline="Indonesia mine toll hits 16, 10 missing",
         body="Toll rose all Thursday as rescuers battled floodwater 100 m underground.",
         source="AP / Reuters", tag="CONFIRMED"),
    dict(n=7, region="East Asia", kicker="PYONGYANG · N. KOREA",
         headline="Kim orders wider nuclear deployment",
         body="KCNA reports Thursday: Kim ordered tactical nukes “across multiple domains”.",
         source="Reuters / AP", tag="REPORTED"),
    dict(n=8, region="East Asia", kicker="SEOUL · SOUTH KOREA",
         headline="Bank of Korea hikes to 3.25%",
         body="Rate up 25bp; chip boom + 2.8% CPI cited. Growth now seen at 3.9% in 2026.",
         source="Reuters", tag="OFFICIAL"),
    dict(n=9, region="Middle East", kicker="KUWAIT CITY · KUWAIT",
         headline="Drones kill 2 Italians in Kuwait",
         body="Drones hit a Kuwaiti air-defence station, killing 2 Italians. Iran denies blame.",
         source="Reuters / CNN", tag="CLAIM"),
    dict(n=10, region="Africa", kicker="ITURI · DR CONGO",
         headline="Congo Ebola passes 12,000 cases",
         body="12,021 infections, 5,904 dead — fastest-growing Ebola outbreak ever recorded.",
         source="Reuters / UN", tag="CONFIRMED"),
    dict(n=11, region="Europe", kicker="LONDON · UK",
         headline="UK net migration falls to 77,000",
         body="Lowest since 1997, down 62% in a year; 738,000 arrived, 661,000 left.",
         source="ONS / Reuters", tag="OFFICIAL"),
    dict(n=12, region="North America", kicker="DALLAS · NFL",
         headline="Eagles stun Cowboys 39–38; Bills–Chiefs in play",
         body="Milton 331 yds, 4 TD; Elliott's 59-yd FG wins it. Chiefs–Bills 10-10 in Q4.",
         source="Reuters / NFL", tag="CONFIRMED"),
    dict(n=13, region="Global", kicker="GENEVA · TRADE",
         headline="Sea trade to stall in 2026 — UNCTAD",
         body="Trade 12.3bn t in 2025, zero growth in 2026; container rates doubled.",
         source="UN News", tag="OFFICIAL"),
]

LIST_ITEMS = [
    (14, "Europe", "Milan & Bournemouth comeback in Europa League", "UEFA"),
    (15, "Europe", "Salah inspires Trabzonspor comeback at CSKA Sofia", "Flashscore"),
    (16, "Europe", "Zelenskiy warns Russia readying new mass strike", "Reuters"),
    (17, "Europe", "EU summit: €45bn Ukraine loan, €1.58tn budget fight", "Reuters"),
    (18, "Europe", "Spain's De Cos picked as next ECB president", "Reuters"),
    (19, "Europe", "Depardieu to face rape trial, Paris court rules", "Reuters"),
    (20, "Middle East", "Houthi projectile hits Aramco Jazan refinery; 1 killed", "Reuters"),
    (21, "Middle East", "Tanker Kun Peng hit in Hormuz; 1 crew badly hurt", "Reuters"),
    (22, "Middle East", "FlyDubai resumes Dubai–Tel Aviv flights 3 Dec", "Reuters"),
    (23, "East Asia", "China launches Yaogan 49 satellite", "Next Spaceflight"),
    (24, "East Asia", "BBC: China-linked network made 500+ AI fake videos", "BBC"),
    (25, "East Asia", "Hong Kong marks 1 year since Tai Po fire killed 168", "HKFP"),
    (26, "Southeast Asia", "Nvidia halts AI server shipments to SE Asia", "FT / Reuters"),
    (27, "Southeast Asia", "Philippines confirms Chinese H-6 bomber near Luzon", "AFP"),
    (28, "Southeast Asia", "Indonesia names nickel firm PT BSJ in laundering case", "Reuters"),
    (29, "South Asia", "Bangladesh wage protests shut 360 garment factories", "Reuters"),
    (30, "South Asia", "India marks Constitution Day as Modi, Congress clash", "Jagran"),
    (31, "South Asia", "New Delhi rejects US tariff finding", "IBC"),
    (32, "Africa", "Guinea-Bissau junta postpones elections to Nov 2028", "Reuters"),
    (33, "North America", "Nor'easter drenches NYC on Thanksgiving", "NWS"),
    (34, "North America", "Trump urges Putin to stop “military aggression”", "USA Today"),
    (35, "Latin America", "Brazil inflation eases: IPCA-15 +0.22%", "Reuters"),
    (36, "Latin America", "WHO gives $1m to Haiti's last big public hospital", "WHO"),
    (37, "Oceania", "Sinner to miss Australian Open after knee surgery", "Reuters"),
    (38, "Oceania", "Flinders Island fire burns >10% of island, 6 homes lost", "ABC"),
    (39, "Oceania", "Liberal senator Blyth defects to One Nation", "Guardian"),
    (40, "Global", "Asia shares bounce: Nikkei +1.6%, Kospi +1.9%", "Reuters"),
]

NUMBERS = [
    ("12,021", "Congo Ebola cases"),
    ("77,000", "UK net migration, lowest since 1997"),
    ("31", "dead in Cairo tanker inferno"),
    ("16", "dead in Indonesia mine flood"),
    ("39–35", "Bears beat Lions"),
    ("0%", "sea-trade growth 2026"),
]

TIMELINE = [
    ("00:00", "Kyiv missiles hit"),
    ("01:00", "BOK hikes to 3.25%"),
    ("07:45", "Bangkok blast"),
    ("09:38", "Yaogan 49 launch"),
    ("13:06", "Brazil inflation"),
    ("14:29", "WHO $1m Haiti"),
    ("21:15", "Bears 39–35 Lions"),
]

REGION_CHIPS = [
    ("EUROPE", 8), ("MIDDLE EAST", 5), ("EAST ASIA", 5), ("SE ASIA", 5),
    ("SOUTH ASIA", 3), ("AFRICA", 3), ("N. AMERICA", 4), ("LATIN AM.", 2),
    ("OCEANIA", 3), ("GLOBAL", 2),
]
REGION_NAMES = ["Europe", "Middle East", "East Asia", "Southeast Asia",
                "South Asia", "Africa", "North America", "Latin America",
                "Oceania", "Global"]

DATE_CHECK_LINES = [
    "Wed 25 Nov: US tariff proposal · Hormuz tanker mine claim · Dow erases 1,100-pt drop · Macy's parade moved · Mamdani rent freeze · 1Password breach · Musk SpaceX shares · Trump–Rutte meeting · Copernicus 2°C report",
    "Tue 24 Nov: Huawei guilty on 10 counts · Sinner surgery announced · Venezuela wage march · FinCEN breach notice.  Mon 23 Nov: Nvidia +31% / Huang reinstated · Copernicus record 2.24°C · Pakistan astronaut boards Tiangong",
    "Sun 22 Nov / earlier: COP31 collapse · 49ers 35-10 Vikings · Bayelsa boat capsize (Fri 20 Nov).  Fri 27 Nov (future): Tokyo CPI +2.9% · NZ election result · Rocket Lab Electron launch",
]

# (lon, lat) of each lead story for the map pins
PINS = {
    1: (30.5, 50.5), 2: (34.4, 31.4), 3: (31.2, 30.0), 4: (-83.0, 42.3),
    5: (100.5, 13.8), 6: (106.8, -6.6), 7: (125.8, 39.0), 8: (127.0, 37.5),
    9: (48.0, 29.4), 10: (29.5, 1.5), 11: (-0.1, 51.5), 12: (-96.8, 32.8),
    13: (6.1, 46.2),
}

CONTINENTS = {
    "North America": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73), (-70, 62), (-60, 52), (-55, 47), (-65, 44), (-75, 38), (-81, 26), (-84, 30), (-90, 29), (-97, 26), (-97, 16), (-90, 14), (-83, 9), (-77, 4), (-80, 7), (-90, 14), (-105, 20), (-114, 28), (-120, 34), (-125, 40), (-124, 48), (-130, 55), (-150, 61), (-168, 66)],
    "South America": [(-80, 9), (-75, -2), (-81, -12), (-77, -18), (-70, -23), (-73, -44), (-66, -55), (-65, -45), (-57, -35), (-48, -27), (-41, -22), (-35, -8), (-44, 2), (-55, 6), (-65, 10), (-75, 10), (-80, 9)],
    "Africa": [(-6, 35), (-10, 31), (-17, 21), (-17, 15), (-12, 8), (-4, 5), (6, 4), (12, -1), (12, -10), (13, -17), (16, -28), (20, -35), (32, -29), (35, -24), (40, -15), (42, -5), (51, 2), (51, 11), (44, 11), (38, 18), (35, 28), (28, 32), (15, 32), (10, 37), (0, 36), (-6, 35)],
    "Europe": [(-10, 36), (-9, 43), (-2, 44), (-4, 48), (0, 51), (5, 53), (8, 57), (12, 56), (21, 55), (28, 60), (30, 65), (25, 71), (14, 67), (5, 60), (0, 53), (-5, 48), (-9, 44), (-10, 36)],
    "Asia": [(30, 70), (50, 69), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70), (170, 67), (178, 65), (162, 56), (150, 59), (140, 50), (130, 42), (122, 38), (122, 28), (110, 21), (105, 10), (100, 7), (95, 15), (90, 22), (80, 13), (77, 8), (72, 20), (66, 25), (58, 26), (50, 29), (44, 29), (38, 36), (30, 36), (30, 46), (30, 60), (30, 70)],
    "Australia": [(113, -22), (114, -30), (118, -35), (124, -33), (132, -32), (138, -35), (145, -38), (153, -32), (153, -27), (150, -22), (142, -15), (142, -11), (135, -15), (130, -13), (122, -17), (113, -22)],
    "Indonesia": [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10), (125, -9), (130, -3), (135, -4), (140, -8), (95, 5)],
}


# ---------------------------------------------------------------- drawing

def draw_card(d, c, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=CARD_LINE, width=1)
    region = c["region"]
    col = REGION_COLORS[region]
    # region accent bar on top of card
    d.rectangle([x, y, x + w, y + 3], fill=col)
    # scene
    scene_h = 84 if big else 52
    SCENES[c["n"]](d, x + 1, y + 4, w - 2, scene_h)
    # number badge (top-left, over scene)
    r = 11 if big else 9
    cx, cy = x + 4 + r, y + 4 + r
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=(255, 255, 255), width=2)
    nf = F_BOLD(13 if big else 11)
    d.text((cx, cy), str(c["n"]), font=nf, fill=(255, 255, 255), anchor="mm")
    # kicker
    ky = y + 4 + scene_h + 4
    kf = F_BOLD(10 if big else 9)
    text(d, (x + 6, ky), c["kicker"], kf, fill=col)
    # headline (max 2 lines)
    hy = ky + (13 if big else 12)
    hf = F_BOLD(14 if big else 11)
    lines, hf2 = fit_lines(d, c["headline"], hf, w - 12, 2, min_size=10)
    lh = 17 if big else 13
    for i, ln in enumerate(lines):
        text(d, (x + 6, hy + i * lh), ln, hf2)
    # body (max 2 lines)
    by = hy + 2 * lh + 2
    bf = F_SANS(10 if big else 9)
    blines, bf2 = fit_lines(d, c["body"], bf, w - 12, 2, min_size=8)
    blh = 12 if big else 11
    for i, ln in enumerate(blines):
        text(d, (x + 6, by + i * blh), ln, bf2, fill=(60, 58, 52))
    # bottom row: source left, trust tag right
    tag = c["tag"]
    tf = F_BOLD(8)
    tag_w = d.textlength(tag, font=tf) + 10
    tag_h = 13
    ty = y + h - tag_h - 5
    d.rounded_rectangle([x + w - tag_w - 5, ty, x + w - 5, ty + tag_h], radius=3,
                        fill=TAG_COLORS[tag])
    d.text((x + w - 5 - tag_w / 2, ty + tag_h / 2), tag, font=tf, fill=(255, 255, 255), anchor="mm")
    sf = F_SANS(8 if big else 7)
    text(d, (x + 6, ty + 2), c["source"], sf, fill=GREY)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=MAP_BG, outline=CARD_LINE, width=1)
    title_f = F_BOLD(11)
    text(d, (x + 8, y + 5), "WHERE IT HAPPENED", title_f, fill=NAVY)
    mx, my, mw, mh = x + 4, y + 22, w - 8, h - 26

    def proj(lon, lat):
        px = mx + (lon + 180.0) / 360.0 * mw
        py = my + (90.0 - lat) / 150.0 * mh
        return px, py

    for name, pts in CONTINENTS.items():
        poly = [proj(lon, lat) for lon, lat in pts]
        d.polygon(poly, fill=MAP_LAND, outline=MAP_LINE)
    # pins
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        card = CARDS[n - 1]
        col = REGION_COLORS[card["region"]]
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=col, outline=(255, 255, 255), width=2)
        d.text((px, py), str(n), font=F_BOLD(9), fill=(255, 255, 255), anchor="mm")


def draw_list(d, x, y, w, h):
    title_f = F_BOLD(11)
    text(d, (x, y), "THE REST OF THE DAY — STORIES 14–40", title_f, fill=NAVY)
    col_w = (w - 12) // 2
    row_h = (h - 22) // 14
    f_num = F_BOLD(9)
    f_txt = F_SANS(9)
    f_src = F_SANS(8)
    for idx, (n, region, headline, source) in enumerate(LIST_ITEMS):
        col_i = 0 if idx < 14 else 1
        row_i = idx if idx < 14 else idx - 14
        lx = x + col_i * (col_w + 12)
        ly = y + 22 + row_i * row_h
        col = REGION_COLORS[region]
        text(d, (lx, ly), str(n), f_num, fill=col)
        # headline, truncated to fit with source
        max_w = col_w - 24
        hl = headline
        while d.textlength(hl + " (" + source + ")", font=f_txt) > max_w and len(hl) > 12:
            hl = hl[:-1]
        if hl != headline:
            hl = hl.rstrip() + "…"
        tx = lx + 20
        text(d, (tx, ly), hl, f_txt)
        sw = d.textlength(hl, font=f_txt)
        text(d, (tx + sw + 3, ly), "(" + source + ")", f_src, fill=GREY)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    centered(d, W // 2, 4, "THE WORLD IN ONE DAY", F_SERIF(27), fill=NAVY)
    centered(d, W // 2, 36, "40 STORIES  ·  10 REGIONS  ·  EVERY ONE DATED THURSDAY 26 NOVEMBER 2026",
             F_BOLD(11), fill=INK)
    d.line([10, 54, W - 10, 54], fill=RED, width=2)

    # ---- date line + sub-headline
    centered(d, W // 2, 60, "Thursday 26 November 2026", F_SERIF(30), fill=INK)
    centered(d, W // 2, 94, "Kyiv hit by missiles and drones  ·  Gaza strikes kill nine  ·  Bears stun Lions 39–35",
             F_SERIF(13), fill=RED)

    # ---- big-numbers strip
    ny, nh = 122, 42
    bw = (W - 20 - 5 * 4) // 6
    for i, (num, label) in enumerate(NUMBERS):
        bx = 10 + i * (bw + 4)
        d.rectangle([bx, ny, bx + bw, ny + nh], fill=(255, 255, 255), outline=CARD_LINE, width=1)
        nf = F_BOLD(20)
        centered(d, bx + bw // 2, ny + 3, num, nf, fill=RED if i == 0 else INK)
        lf = F_SANS(8)
        lines = wrap(d, label, lf, bw - 10)
        for j, ln in enumerate(lines[:2]):
            centered(d, bx + bw // 2, ny + 25 + j * 9, ln, lf, fill=GREY)

    # ---- UTC timeline strip
    ty = 170
    d.rectangle([10, ty, W - 10, ty + 30], fill=NAVY)
    text(d, (18, ty + 8), "THURSDAY IN UTC", F_BOLD(10), fill=(255, 255, 255))
    tw = (W - 20 - 150) // 7
    for i, (t, label) in enumerate(TIMELINE):
        tx = 160 + i * tw
        text(d, (tx, ty + 3), t, F_BOLD(10), fill=(253, 224, 71))
        lf = F_SANS(8)
        lines = wrap(d, label, lf, tw - 8)
        for j, ln in enumerate(lines[:2]):
            text(d, (tx, ty + 15 + j * 8), ln, lf, fill=(255, 255, 255))

    # ---- region chips
    cy = 206
    cw = (W - 20 - 9 * 4) // 10
    for i, (label, count) in enumerate(REGION_CHIPS):
        cx = 10 + i * (cw + 4)
        col = REGION_COLORS[REGION_NAMES[i]]
        d.rounded_rectangle([cx, cy, cx + cw, cy + 20], radius=9, fill=col)
        centered(d, cx + cw // 2, cy + 4, f"{label} {count}", F_BOLD(10), fill=(255, 255, 255))

    # ---- cards row 1: 3 big
    y1, h1 = 232, 192
    w1 = (W - 20 - 2 * 8) // 3
    for i in range(3):
        draw_card(d, CARDS[i], 10 + i * (w1 + 8), y1, w1, h1, big=True)

    # ---- cards row 2: 5
    y2, h2 = 430, 150
    w2 = (W - 20 - 4 * 6) // 5
    for i in range(5):
        draw_card(d, CARDS[3 + i], 10 + i * (w2 + 6), y2, w2, h2, big=False)

    # ---- cards row 3: 5
    y3, h3 = 586, 150
    for i in range(5):
        draw_card(d, CARDS[8 + i], 10 + i * (w2 + 6), y3, w2, h2, big=False)

    # ---- bottom: map + list
    by, bh = 742, 194
    draw_map(d, 10, by, 342, bh)
    draw_list(d, 360, by + 2, W - 10 - 360, bh - 2)

    # ---- HOW SURE legend
    ly = 942
    lx = 10
    text(d, (lx, ly), "HOW SURE:", F_BOLD(9), fill=NAVY)
    lx += d.textlength("HOW SURE: ", font=F_BOLD(9)) + 4
    legend = [("OFFICIAL", "on the record"), ("REPORTED", "wires / outlets"),
              ("CLAIM", "one side's account, unverified"), ("CONFIRMED", "2+ outlets")]
    for tag, meaning in legend:
        tf = F_BOLD(8)
        twd = d.textlength(tag, font=tf) + 8
        d.rounded_rectangle([lx, ly, lx + twd, ly + 12], radius=3, fill=TAG_COLORS[tag])
        d.text((lx + twd / 2, ly + 6), tag, font=tf, fill=(255, 255, 255), anchor="mm")
        lx += twd + 3
        text(d, (lx, ly + 1), "= " + meaning, F_SANS(9), fill=GREY)
        lx += d.textlength("= " + meaning, font=F_SANS(9)) + 12

    # ---- DATE CHECK box
    dy, dh = 960, 48
    d.rectangle([10, dy, W - 10, dy + dh], fill=(255, 251, 235), outline=(217, 119, 6), width=1)
    text(d, (18, dy + 3), "DATE CHECK — LEFT OUT (happened other days, NOT Thursday news):",
         F_BOLD(9), fill=(146, 64, 14))
    df = F_SANS(8)
    for j, ln in enumerate(DATE_CHECK_LINES):
        text(d, (18, dy + 15 + j * 11), ln, df, fill=(68, 64, 60))

    # ---- footer
    centered(d, W // 2, 1011, "Compiled after Thursday ended in UTC  ·  Pictures drawn in code, not photos  ·  Sources: Reuters, AP, BBC, AFP, ONS, UN, UEFA, NFL",
             F_SANS(8), fill=GREY)

    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
