#!/usr/bin/env python3
"""Render the Friday 20 November 2026 world news page, 1024x1024 PNG.

Pure Python stdlib plus Pillow for raster work. Deterministic: fixed seed,
fixed fonts, fixed compression. Rendered at 2x and downscaled for smooth
gradients. No network, no timestamps, no randomness outside the seeded PRNG.
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

SS = 2
W, H = 1024, 1024
CW, CH = W * SS, H * SS
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (247, 241, 224)
INK = (26, 24, 20)
CRIMSON = (140, 29, 24)
NAVY = (31, 58, 95)
GOLD = (176, 132, 24)
CARD = (255, 253, 247)
RULE = (120, 100, 70)
MUTED = (90, 82, 66)

RNG = random.Random(20261120)


def font(path, size):
    return ImageFont.truetype(path, int(size * SS))


def vgrad(draw, box, top, bottom, steps=48):
    x0, y0, x1, y1 = box
    for i in range(steps):
        t = i / (steps - 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        yy0 = y0 + (y1 - y0) * i // steps
        yy1 = y0 + (y1 - y0) * (i + 1) // steps
        draw.rectangle([x0, yy0, x1, yy1], fill=c)


def hgrad(draw, box, left, right, steps=48):
    x0, y0, x1, y1 = box
    for i in range(steps):
        t = i / (steps - 1)
        c = tuple(int(left[k] + (right[k] - left[k]) * t) for k in range(3))
        xx0 = x0 + (x1 - x0) * i // steps
        xx1 = x0 + (x1 - x0) * (i + 1) // steps
        draw.rectangle([xx0, y0, xx1, y1], fill=c)


def glow(draw, cx, cy, r, colour, steps=24):
    for i in range(steps, 0, -1):
        t = i / steps
        c = tuple(int(255 + (colour[k] - 255) * (1 - t) * 0.85) for k in range(3))
        draw.ellipse([cx - r * t, cy - r * t, cx + r * t, cy + r * t], fill=c)


def sun(draw, cx, cy, r, core=(255, 214, 120), halo=(255, 170, 60)):
    glow(draw, cx, cy, r * 1.5, halo)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=core)
    draw.ellipse([cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7],
                 fill=(255, 236, 170))


def skyline(draw, box, heights, colour, windows=True):
    x0, y0, x1, y1 = box
    n = len(heights)
    bw = (x1 - x0) / n
    for i, h in enumerate(heights):
        bx0 = x0 + i * bw
        bx1 = bx0 + bw * 0.92
        by1 = y1
        by0 = y1 - (y1 - y0) * h
        draw.rectangle([bx0, by0, bx1, by1], fill=colour)
        if h > 0.75:
            draw.polygon([(bx0, by0), ((bx0 + bx1) / 2, by0 - (y1 - y0) * 0.12),
                          (bx1, by0)], fill=colour)
        if windows:
            for wy in range(int(by0) + 6 * SS, int(by1) - 4 * SS, 9 * SS):
                for wx in range(int(bx0) + 3 * SS, int(bx1) - 3 * SS, 7 * SS):
                    if RNG.random() < 0.5:
                        draw.rectangle([wx, wy, wx + 2 * SS, wy + 3 * SS],
                                       fill=(255, 220, 130))


def flag(draw, x, y, w, h, stripes):
    n = len(stripes)
    for i, c in enumerate(stripes):
        draw.rectangle([x, y + h * i // n, x + w, y + h * (i + 1) // n], fill=c)
    draw.rectangle([x, y, x + w, y + h], outline=(40, 40, 40), width=SS)


def wrap(text, fnt, width, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, colour, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=colour)
        y += leading
    return y


# ---------------------------------------------------------------- scenes
def scene_cyclone(d, b):
    vgrad(d, b, (38, 64, 92), (120, 150, 170))
    x0, y0, x1, y1 = b
    cx, cy = (x0 + x1) * 0.55, (y0 + y1) * 0.5
    for k in range(7):
        r = (x1 - x0) * (0.08 + 0.055 * k)
        a0 = k * 0.9
        pts = []
        for s in range(0, 181, 6):
            a = a0 + math.radians(s) * 1.15
            rr = r * (0.55 + 0.45 * s / 180)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.62))
        d.line(pts, fill=(235, 240, 245), width=3 * SS)
    d.ellipse([cx - 9 * SS, cy - 6 * SS, cx + 9 * SS, cy + 6 * SS],
              fill=(250, 250, 245))
    d.polygon([(x0, y1), (x0 + (x1 - x0) * 0.35, y1 - (y1 - y0) * 0.28),
               (x0 + (x1 - x0) * 0.62, y1 - (y1 - y0) * 0.12), (x1, y1)],
              fill=(52, 96, 62))
    for _ in range(26):
        rx = RNG.uniform(x0, x1)
        ry = RNG.uniform(y0, y0 + (y1 - y0) * 0.6)
        d.line([(rx, ry), (rx - 3 * SS, ry + 9 * SS)], fill=(200, 215, 225),
               width=SS)


def scene_whitehouse(d, b):
    vgrad(d, b, (58, 88, 138), (214, 196, 150))
    x0, y0, x1, y1 = b
    sun(d, x1 - (x1 - x0) * 0.2, y0 + (y1 - y0) * 0.24, 9 * SS)
    d.rectangle([x0, y1 - (y1 - y0) * 0.30, x1, y1], fill=(46, 84, 52))
    bw = (x1 - x0) * 0.62
    bx0 = x0 + (x1 - x0 - bw) / 2
    bx1 = bx0 + bw
    by1 = y1 - (y1 - y0) * 0.30
    by0 = y1 - (y1 - y0) * 0.72
    d.rectangle([bx0, by0 + (by1 - by0) * 0.35, bx1, by1], fill=(238, 232, 214))
    d.polygon([(bx0 - 4 * SS, by0 + (by1 - by0) * 0.35),
               ((bx0 + bx1) / 2, by0), (bx1 + 4 * SS, by0 + (by1 - by0) * 0.35)],
              fill=(226, 218, 196))
    for i in range(6):
        cx = bx0 + bw * (0.08 + 0.168 * i)
        d.rectangle([cx - 3 * SS, by0 + (by1 - by0) * 0.38, cx + 3 * SS, by1],
                    fill=(210, 202, 178))
    flag(d, bx0 + bw * 0.42, by0 - 16 * SS, 16 * SS, 10 * SS,
         [(178, 34, 52), (255, 255, 255), (178, 34, 52)])


def scene_berlin(d, b):
    vgrad(d, b, (70, 96, 140), (200, 186, 150))
    x0, y0, x1, y1 = b
    d.rectangle([x0, y1 - (y1 - y0) * 0.26, x1, y1], fill=(58, 74, 58))
    bx0, bx1 = x0 + (x1 - x0) * 0.12, x1 - (x1 - x0) * 0.12
    by1 = y1 - (y1 - y0) * 0.26
    by0 = y1 - (y1 - y0) * 0.66
    d.rectangle([bx0, by0 + (by1 - by0) * 0.4, bx1, by1], fill=(214, 200, 168))
    dcx = (bx0 + bx1) / 2
    drx = (bx1 - bx0) * 0.20
    d.pieslice([dcx - drx, by0 + (by1 - by0) * 0.08,
                dcx + drx, by0 + (by1 - by0) * 0.48],
               180, 360, fill=(168, 188, 204))
    d.line([(dcx, by0 + (by1 - by0) * 0.08),
            (dcx, by0 + (by1 - by0) * 0.02)], fill=(120, 130, 140),
           width=2 * SS)
    for i in range(7):
        cx = bx0 + (bx1 - bx0) * (0.08 + 0.14 * i)
        d.rectangle([cx - 2 * SS, by0 + (by1 - by0) * 0.45, cx + 2 * SS, by1],
                    fill=(190, 176, 144))
    fx = x0 + (x1 - x0) * 0.06
    flag(d, fx, y0 + (y1 - y0) * 0.10, 18 * SS, 11 * SS,
         [(0, 51, 153), (255, 204, 0)])
    flag(d, fx + 24 * SS, y0 + (y1 - y0) * 0.10, 18 * SS, 11 * SS,
         [(0, 87, 184), (255, 215, 0)])
    flag(d, fx + 48 * SS, y0 + (y1 - y0) * 0.10, 18 * SS, 11 * SS,
         [(255, 255, 255), (0, 57, 166), (213, 43, 30)])


def scene_cop31(d, b):
    vgrad(d, b, (96, 150, 190), (250, 214, 130))
    x0, y0, x1, y1 = b
    sun(d, x1 - (x1 - x0) * 0.22, y0 + (y1 - y0) * 0.26, 10 * SS)
    d.polygon([(x0, y1), (x0 + (x1 - x0) * 0.3, y1 - (y1 - y0) * 0.34),
               (x0 + (x1 - x0) * 0.55, y1 - (y1 - y0) * 0.18), (x1, y1)],
              fill=(74, 110, 70))
    d.rectangle([x0, y1 - (y1 - y0) * 0.22, x1, y1], fill=(46, 110, 150))
    for k in range(3):
        d.arc([x0 + 8 * SS + k * 4 * SS, y1 - (y1 - y0) * 0.20 + k * 3 * SS,
               x1 - 8 * SS, y1 - (y1 - y0) * 0.04 + k * 3 * SS],
              200, 340, fill=(200, 230, 240), width=SS)
    tx = x0 + (x1 - x0) * 0.14
    ty = y0 + (y1 - y0) * 0.12
    d.rounded_rectangle([tx, ty, tx + 9 * SS, ty + 34 * SS], radius=4 * SS,
                        fill=(240, 240, 235), outline=CRIMSON, width=SS)
    d.ellipse([tx - 3 * SS, ty + 30 * SS, tx + 12 * SS, ty + 42 * SS],
              fill=CRIMSON)
    d.rectangle([tx + 3 * SS, ty + 12 * SS, tx + 6 * SS, ty + 32 * SS],
                fill=(220, 80, 50))
    for i in range(2):
        px = x1 - (x1 - x0) * (0.30 + 0.18 * i)
        py = y1 - (y1 - y0) * 0.42
        d.line([(px, py), (px, y1 - (y1 - y0) * 0.24)], fill=(240, 240, 230),
               width=2 * SS)
        for a in (0, 120, 240):
            ar = math.radians(a + 25)
            d.line([(px, py), (px + 10 * SS * math.cos(ar),
                                py + 10 * SS * math.sin(ar))],
                   fill=(240, 240, 230), width=2 * SS)


def scene_shenzhen(d, b):
    vgrad(d, b, (44, 66, 110), (238, 170, 110))
    x0, y0, x1, y1 = b
    sun(d, (x0 + x1) / 2, y0 + (y1 - y0) * 0.30, 10 * SS,
        core=(255, 226, 150), halo=(255, 190, 90))
    skyline(d, (x0, y0 + (y1 - y0) * 0.18, x1, y1),
            [0.55, 0.9, 0.7, 1.0, 0.62, 0.85, 0.5, 0.75], (34, 44, 66))
    d.rectangle([x0, y1 - 4 * SS, x1, y1], fill=(24, 32, 52))
    flag(d, x0 + (x1 - x0) * 0.10, y0 + (y1 - y0) * 0.08, 18 * SS, 11 * SS,
         [(222, 41, 16), (222, 41, 16)])
    flag(d, x0 + (x1 - x0) * 0.24, y0 + (y1 - y0) * 0.08, 18 * SS, 11 * SS,
         [(0, 0, 139), (255, 255, 255), (0, 0, 139)])


def scene_bridge(d, b):
    vgrad(d, b, (90, 110, 140), (220, 200, 160))
    x0, y0, x1, y1 = b
    d.rectangle([x0, y1 - (y1 - y0) * 0.34, x1, y1], fill=(52, 96, 128))
    for k in range(3):
        d.arc([x0 + 6 * SS, y1 - (y1 - y0) * 0.32 + k * 3 * SS,
               x1 - 6 * SS, y1 - (y1 - y0) * 0.06 + k * 3 * SS],
              200, 340, fill=(180, 210, 225), width=SS)
    dy = y1 - (y1 - y0) * 0.52
    d.rectangle([x0, dy - 5 * SS, x0 + (x1 - x0) * 0.42, dy + 3 * SS],
                fill=(70, 70, 74))
    d.rectangle([x0 + (x1 - x0) * 0.58, dy - 5 * SS, x1, dy + 3 * SS],
                fill=(70, 70, 74))
    d.arc([x0 + (x1 - x0) * 0.30, dy - 26 * SS, x0 + (x1 - x0) * 0.70,
           dy + 6 * SS], 180, 360, fill=(96, 96, 100), width=4 * SS)
    for i, px in enumerate((0.12, 0.30, 0.70, 0.88)):
        d.line([(x0 + (x1 - x0) * px, dy - 5 * SS),
                (x0 + (x1 - x0) * px, y1 - (y1 - y0) * 0.34)],
               fill=(80, 80, 84), width=2 * SS)
    gx = x0 + (x1 - x0) * 0.50
    for k in range(3):
        r = (x1 - x0) * (0.035 + 0.03 * k)
        d.ellipse([gx - r, dy - 22 * SS - r * 0.6,
                   gx + r, dy - 22 * SS + r * 0.5],
                  fill=(120 + 14 * k, 118 + 12 * k, 116 + 12 * k))
    d.polygon([(gx - 4 * SS, dy - 4 * SS), (gx + 4 * SS, dy - 4 * SS),
               (gx + 2 * SS, dy + 8 * SS), (gx - 2 * SS, dy + 8 * SS)],
              fill=(200, 90, 30))


def scene_tower(d, b):
    vgrad(d, b, (52, 66, 100), (240, 190, 120))
    x0, y0, x1, y1 = b
    d.rectangle([x0, y1 - (y1 - y0) * 0.22, x1, y1], fill=(40, 44, 58))
    cx = (x0 + x1) * 0.52
    top = y0 + (y1 - y0) * 0.06
    pts = []
    for i in range(9):
        t = i / 8
        wdt = (x1 - x0) * (0.10 + 0.05 * math.sin(t * 2.2))
        yy = top + (y1 - (y1 - y0) * 0.22 - top) * t
        pts.append((cx - wdt, yy))
    pts2 = []
    for i in range(9):
        t = i / 8
        wdt = (x1 - x0) * (0.10 + 0.05 * math.sin(t * 2.2))
        yy = top + (y1 - (y1 - y0) * 0.22 - top) * t
        pts2.append((cx + wdt, yy))
    d.polygon(pts + pts2[::-1], fill=(86, 100, 130))
    for wy in range(int(top) + 8 * SS, int(y1 - (y1 - y0) * 0.22) - 4 * SS,
                   8 * SS):
        for sgn in (-1, 1):
            wx = cx + sgn * (x1 - x0) * 0.055
            col = (255, 210, 110) if RNG.random() < 0.55 else (52, 58, 76)
            d.rectangle([wx - 3 * SS, wy, wx + 3 * SS, wy + 4 * SS], fill=col)
    for k in range(3):
        r = (x1 - x0) * (0.03 + 0.025 * k)
        d.ellipse([cx + (x1 - x0) * 0.10 - r, top + 6 * SS - r * 0.6,
                   cx + (x1 - x0) * 0.10 + r, top + 6 * SS + r * 0.6],
                  fill=(120 + 14 * k, 118 + 12 * k, 116 + 12 * k))
    skyline(d, (x0, y1 - (y1 - y0) * 0.30, x1, y1 - (y1 - y0) * 0.22),
            [0.5, 0.7, 0.45, 0.6], (36, 40, 54), windows=False)


def scene_caracas(d, b):
    vgrad(d, b, (80, 120, 170), (250, 210, 140))
    x0, y0, x1, y1 = b
    d.polygon([(x0, y1 - (y1 - y0) * 0.30), (x0 + (x1 - x0) * 0.30,
              y1 - (y1 - y0) * 0.72), (x0 + (x1 - x0) * 0.55,
              y1 - (y1 - y0) * 0.30)], fill=(52, 88, 60))
    d.polygon([(x0 + (x1 - x0) * 0.45, y1 - (y1 - y0) * 0.30),
               (x0 + (x1 - x0) * 0.72, y1 - (y1 - y0) * 0.80),
               (x1, y1 - (y1 - y0) * 0.30)], fill=(44, 76, 54))
    skyline(d, (x0, y1 - (y1 - y0) * 0.34, x1, y1),
            [0.5, 0.75, 0.6, 0.9, 0.55, 0.7], (52, 52, 60))
    fx = x0 + (x1 - x0) * 0.08
    flag(d, fx, y0 + (y1 - y0) * 0.10, 18 * SS, 11 * SS,
         [(178, 34, 52), (255, 255, 255), (0, 40, 104)])
    flag(d, fx + 26 * SS, y0 + (y1 - y0) * 0.10, 18 * SS, 11 * SS,
         [(255, 204, 0), (0, 47, 108), (206, 17, 38)])


def scene_yongbyon(d, b):
    vgrad(d, b, (40, 52, 84), (180, 150, 110))
    x0, y0, x1, y1 = b
    d.polygon([(x0, y1 - (y1 - y0) * 0.26), (x0 + (x1 - x0) * 0.25,
              y1 - (y1 - y0) * 0.62), (x0 + (x1 - x0) * 0.5,
              y1 - (y1 - y0) * 0.26)], fill=(48, 66, 52))
    d.polygon([(x0 + (x1 - x0) * 0.5, y1 - (y1 - y0) * 0.26),
               (x0 + (x1 - x0) * 0.78, y1 - (y1 - y0) * 0.70),
               (x1, y1 - (y1 - y0) * 0.26)], fill=(40, 58, 46))
    d.rectangle([x0, y1 - (y1 - y0) * 0.26, x1, y1], fill=(58, 60, 62))
    for i, fx in enumerate((0.18, 0.42, 0.68)):
        cx = x0 + (x1 - x0) * fx
        by = y1 - (y1 - y0) * 0.26
        d.rectangle([cx - 12 * SS, by - 18 * SS, cx + 12 * SS, by],
                    fill=(120, 118, 110))
        d.pieslice([cx - 12 * SS, by - 30 * SS, cx + 12 * SS, by - 6 * SS],
                   180, 360, fill=(150, 148, 138))
        d.rectangle([cx - 2 * SS, by - 34 * SS, cx + 2 * SS, by - 18 * SS],
                    fill=(90, 88, 84))
    ax, ay = x1 - (x1 - x0) * 0.20, y0 + (y1 - y0) * 0.24
    for ang in (0, 60, 120):
        pts = []
        for s in range(0, 361, 10):
            a = math.radians(s)
            ex = 15 * SS * math.cos(a)
            ey = 6 * SS * math.sin(a)
            ca = math.cos(math.radians(ang))
            sa = math.sin(math.radians(ang))
            pts.append((ax + ex * ca - ey * sa, ay + ex * sa + ey * ca))
        d.line(pts, fill=(255, 220, 120), width=2 * SS)
    d.ellipse([ax - 4 * SS, ay - 4 * SS, ax + 4 * SS, ay + 4 * SS],
              fill=(255, 220, 120))


def scene_seoul(d, b):
    vgrad(d, b, (70, 96, 140), (226, 214, 186))
    x0, y0, x1, y1 = b
    d.rectangle([x0, y1 - (y1 - y0) * 0.24, x1, y1], fill=(52, 68, 54))
    bx0, bx1 = x0 + (x1 - x0) * 0.14, x1 - (x1 - x0) * 0.14
    by1 = y1 - (y1 - y0) * 0.24
    by0 = y1 - (y1 - y0) * 0.68
    d.rectangle([bx0, by0 + (by1 - by0) * 0.3, bx1, by1], fill=(232, 224, 200))
    d.polygon([(bx0 - 4 * SS, by0 + (by1 - by0) * 0.3),
               ((bx0 + bx1) / 2, by0), (bx1 + 4 * SS, by0 + (by1 - by0) * 0.3)],
              fill=(216, 206, 178))
    for i in range(5):
        cx = bx0 + (bx1 - bx0) * (0.12 + 0.19 * i)
        d.rectangle([cx - 3 * SS, by0 + (by1 - by0) * 0.34, cx + 3 * SS, by1],
                    fill=(200, 190, 162))
    sx = x0 + (x1 - x0) * 0.78
    sy = y0 + (y1 - y0) * 0.16
    d.line([(sx, sy), (sx, sy + 16 * SS)], fill=(200, 170, 40), width=2 * SS)
    d.line([(sx - 12 * SS, sy + 2 * SS), (sx + 12 * SS, sy + 2 * SS)],
           fill=(200, 170, 40), width=2 * SS)
    d.line([(sx - 12 * SS, sy + 2 * SS), (sx - 8 * SS, sy + 12 * SS)],
           fill=(200, 170, 40), width=2 * SS)
    d.line([(sx + 12 * SS, sy + 2 * SS), (sx + 8 * SS, sy + 12 * SS)],
           fill=(200, 170, 40), width=2 * SS)
    d.ellipse([sx - 4 * SS, sy + 11 * SS, sx + 4 * SS, sy + 19 * SS],
              outline=(200, 170, 40), width=2 * SS)
    flag(d, x0 + (x1 - x0) * 0.06, y0 + (y1 - y0) * 0.08, 18 * SS, 11 * SS,
         [(255, 255, 255), (0, 0, 139), (255, 255, 255)])


def scene_fiji(d, b):
    vgrad(d, b, (120, 150, 190), (250, 220, 150))
    x0, y0, x1, y1 = b
    sun(d, x1 - (x1 - x0) * 0.20, y0 + (y1 - y0) * 0.22, 10 * SS)
    d.rectangle([x0, y1 - (y1 - y0) * 0.42, x1, y1], fill=(196, 150, 92))
    for _ in range(9):
        cx = RNG.uniform(x0, x1)
        cy = RNG.uniform(y1 - (y1 - y0) * 0.40, y1 - (y1 - y0) * 0.06)
        ln = RNG.uniform(6, 16) * SS
        ang = RNG.uniform(0, math.pi)
        d.line([(cx, cy), (cx + ln * math.cos(ang), cy + ln * math.sin(ang))],
               fill=(120, 80, 44), width=2 * SS)
    d.polygon([(x0 + (x1 - x0) * 0.55, y1 - (y1 - y0) * 0.30),
               (x0 + (x1 - x0) * 0.62, y1 - (y1 - y0) * 0.42),
               (x0 + (x1 - x0) * 0.72, y1 - (y1 - y0) * 0.30)],
              fill=(90, 110, 70))
    tx = x0 + (x1 - x0) * 0.12
    ty = y1 - (y1 - y0) * 0.30
    d.rounded_rectangle([tx, ty - 12 * SS, tx + 34 * SS, ty], radius=4 * SS,
                        fill=(70, 110, 150))
    d.ellipse([tx + 6 * SS, ty - 2 * SS, tx + 12 * SS, ty + 4 * SS],
              fill=(30, 30, 30))
    d.ellipse([tx + 22 * SS, ty - 2 * SS, tx + 28 * SS, ty + 4 * SS],
              fill=(30, 30, 30))
    d.text((tx, ty - 24 * SS), "WATER", font=font(SANS_B, 8), fill=(255, 255, 255))


def scene_sensex(d, b):
    vgrad(d, b, (36, 58, 88), (220, 200, 150))
    x0, y0, x1, y1 = b
    d.rectangle([x0, y1 - (y1 - y0) * 0.24, x1, y1], fill=(44, 66, 52))
    pts = [(x0 + (x1 - x0) * 0.06, y1 - (y1 - y0) * 0.38),
           (x0 + (x1 - x0) * 0.26, y1 - (y1 - y0) * 0.46),
           (x0 + (x1 - x0) * 0.44, y1 - (y1 - y0) * 0.40),
           (x0 + (x1 - x0) * 0.62, y1 - (y1 - y0) * 0.58),
           (x0 + (x1 - x0) * 0.80, y1 - (y1 - y0) * 0.52),
           (x0 + (x1 - x0) * 0.94, y1 - (y1 - y0) * 0.78)]
    d.line(pts, fill=(90, 200, 120), width=4 * SS, joint="curve")
    hx, hy = pts[-1]
    d.polygon([(hx - 10 * SS, hy + 2 * SS), (hx + 2 * SS, hy + 2 * SS),
               (hx - 4 * SS, hy - 10 * SS)], fill=(90, 200, 120))
    for i in range(4):
        bx = x0 + (x1 - x0) * (0.10 + 0.22 * i)
        bh = (y1 - y0) * (0.10 + 0.08 * i)
        d.rectangle([bx, y1 - (y1 - y0) * 0.24 - bh, bx + 12 * SS,
                     y1 - (y1 - y0) * 0.24], fill=(70, 120, 90))
    d.text((x0 + 6 * SS, y0 + 5 * SS), "+989", font=font(SERIF_B, 20),
           fill=(120, 230, 150))


def scene_cricket(d, b):
    vgrad(d, b, (110, 160, 210), (240, 220, 170))
    x0, y0, x1, y1 = b
    d.ellipse([x0 + (x1 - x0) * 0.06, y1 - (y1 - y0) * 0.42,
               x1 - (x1 - x0) * 0.06, y1 - (y1 - y0) * 0.02],
              fill=(72, 130, 62))
    d.ellipse([x0 + (x1 - x0) * 0.22, y1 - (y1 - y0) * 0.36,
               x1 - (x1 - x0) * 0.22, y1 - (y1 - y0) * 0.08],
              fill=(88, 148, 74))
    bx, by = x0 + (x1 - x0) * 0.42, y1 - (y1 - y0) * 0.52
    d.ellipse([bx - 7 * SS, by - 8 * SS, bx + 7 * SS, by + 8 * SS],
              fill=(226, 190, 150))
    d.polygon([(bx - 9 * SS, by + 6 * SS), (bx + 9 * SS, by + 6 * SS),
               (bx + 11 * SS, by + 34 * SS), (bx - 11 * SS, by + 34 * SS)],
              fill=(245, 245, 240))
    d.rectangle([bx - 9 * SS, by + 32 * SS, bx - 3 * SS, by + 52 * SS],
                fill=(40, 48, 70))
    d.rectangle([bx + 3 * SS, by + 32 * SS, bx + 9 * SS, by + 52 * SS],
                fill=(40, 48, 70))
    d.line([(bx + 10 * SS, by + 12 * SS), (bx + 26 * SS, by + 44 * SS)],
           fill=(214, 170, 110), width=5 * SS)
    d.line([(bx - 10 * SS, by + 12 * SS), (bx - 24 * SS, by + 40 * SS)],
           fill=(226, 190, 150), width=5 * SS)
    sx = x0 + (x1 - x0) * 0.78
    sy = y1 - (y1 - y0) * 0.34
    for dx in (-4 * SS, 0, 4 * SS):
        d.line([(sx + dx, sy), (sx + dx, sy + 14 * SS)], fill=(240, 220, 130),
               width=2 * SS)
    d.ellipse([x0 + (x1 - x0) * 0.68, y0 + (y1 - y0) * 0.14,
               x0 + (x1 - x0) * 0.68 + 7 * SS, y0 + (y1 - y0) * 0.14 + 7 * SS],
              fill=(178, 34, 52))


def scene_gemini(d, b):
    vgrad(d, b, (16, 22, 48), (58, 44, 110))
    x0, y0, x1, y1 = b
    for _ in range(46):
        sx = RNG.uniform(x0, x1)
        sy = RNG.uniform(y0, y0 + (y1 - y0) * 0.7)
        r = RNG.uniform(0.6, 1.8) * SS
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    cx, cy = (x0 + x1) * 0.5, y0 + (y1 - y0) * 0.42
    glow(d, cx, cy, 20 * SS, (120, 200, 255))
    pts = []
    for i in range(8):
        a = math.pi / 2 + i * math.pi / 4
        r = 20 * SS if i % 2 == 0 else 8 * SS
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(180, 220, 255))
    d.ellipse([cx - 4 * SS, cy - 4 * SS, cx + 4 * SS, cy + 4 * SS],
              fill=(255, 255, 255))
    for sx, sy in ((0.30, 0.30), (0.72, 0.30)):
        px, py = x0 + (x1 - x0) * sx, y0 + (y1 - y0) * sy
        d.line([(cx, cy), (px, py)], fill=(140, 170, 220), width=SS)
        d.ellipse([px - 2 * SS, py - 2 * SS, px + 2 * SS, py + 2 * SS],
                  fill=(200, 220, 255))
    d.rounded_rectangle([x0 + (x1 - x0) * 0.30, y1 - (y1 - y0) * 0.22,
                         x1 - (x1 - x0) * 0.30, y1 - (y1 - y0) * 0.08],
                        radius=3 * SS, fill=(30, 40, 70),
                        outline=(120, 200, 255), width=SS)
    d.text((x0 + (x1 - x0) * 0.36, y1 - (y1 - y0) * 0.20), "NEON",
           font=font(SANS_B, 9), fill=(150, 220, 255))


def scene_missiles(d, b):
    vgrad(d, b, (120, 70, 50), (240, 180, 110))
    x0, y0, x1, y1 = b
    sun(d, x1 - (x1 - x0) * 0.24, y0 + (y1 - y0) * 0.28, 9 * SS,
        core=(255, 220, 140), halo=(255, 180, 90))
    d.polygon([(x0, y1), (x0 + (x1 - x0) * 0.4, y1 - (y1 - y0) * 0.26),
               (x1, y1)], fill=(150, 110, 66))
    d.rectangle([x0, y1 - (y1 - y0) * 0.16, x1, y1], fill=(120, 88, 52))
    for i, fx in enumerate((0.16, 0.44, 0.72)):
        mx = x0 + (x1 - x0) * fx
        my = y1 - (y1 - y0) * 0.16
        hgt = (y1 - y0) * (0.42 + 0.10 * (i % 2))
        d.rectangle([mx - 7 * SS, my - 8 * SS, mx + 7 * SS, my],
                    fill=(52, 56, 60))
        d.polygon([(mx - 4 * SS, my - 8 * SS), (mx - 4 * SS, my - hgt),
                   (mx, my - hgt - 8 * SS), (mx + 4 * SS, my - hgt),
                   (mx + 4 * SS, my - 8 * SS)], fill=(200, 200, 195))
        d.rectangle([mx - 4 * SS, my - hgt * 0.55, mx + 4 * SS,
                     my - hgt * 0.55 + 3 * SS], fill=(178, 34, 52))


def scene_gold(d, b):
    vgrad(d, b, (44, 40, 60), (120, 100, 60))
    x0, y0, x1, y1 = b
    pts = [(x0 + (x1 - x0) * 0.06, y1 - (y1 - y0) * 0.55),
           (x0 + (x1 - x0) * 0.30, y1 - (y1 - y0) * 0.48),
           (x0 + (x1 - x0) * 0.52, y1 - (y1 - y0) * 0.62),
           (x0 + (x1 - x0) * 0.74, y1 - (y1 - y0) * 0.42),
           (x0 + (x1 - x0) * 0.94, y1 - (y1 - y0) * 0.30)]
    d.line(pts, fill=(255, 210, 90), width=4 * SS, joint="curve")
    hx, hy = pts[-1]
    d.polygon([(hx - 10 * SS, hy - 2 * SS), (hx + 2 * SS, hy - 2 * SS),
               (hx - 4 * SS, hy + 10 * SS)], fill=(255, 210, 90))
    for row, (n, yy) in enumerate(((3, 0.78), (2, 0.66), (1, 0.54))):
        for i in range(n):
            bx = x0 + (x1 - x0) * (0.30 + 0.16 * i + 0.08 * (2 - n))
            by = y1 - (y1 - y0) * yy
            d.polygon([(bx - 12 * SS, by), (bx - 8 * SS, by - 10 * SS),
                       (bx + 8 * SS, by - 10 * SS), (bx + 12 * SS, by)],
                      fill=(232, 180, 60))
            d.polygon([(bx - 12 * SS, by), (bx - 8 * SS, by - 10 * SS),
                       (bx + 8 * SS, by - 10 * SS), (bx + 12 * SS, by)],
                      outline=(150, 105, 20), width=SS)


SCENES = {
    "cyclone": scene_cyclone, "whitehouse": scene_whitehouse,
    "berlin": scene_berlin, "cop31": scene_cop31,
    "shenzhen": scene_shenzhen, "bridge": scene_bridge,
    "tower": scene_tower, "caracas": scene_caracas,
    "yongbyon": scene_yongbyon, "seoul": scene_seoul,
    "fiji": scene_fiji, "sensex": scene_sensex,
    "cricket": scene_cricket, "gemini": scene_gemini,
    "missiles": scene_missiles, "gold": scene_gold,
}

# ---------------------------------------------------------------- data
# region, field, headline, sub, scene, map pin (lon, lat)
LEADS = [
    ("Asia", "Weather", "Cyclone Akvan strikes Odisha coast",
     "300,000 people evacuated as the storm crosses near Gopalpur with winds of 100 kmph.",
     "cyclone", (85, 20)),
    ("North America", "Conflict", "Trump puts Iran decision off until 2027",
     "The president says he is in no rush, and the Senate rejects war powers curbs 51 to 48.",
     "whitehouse", (-77, 39)),
    ("Europe", "Diplomacy", "Europe says it is ready to talk to Russia",
     "Berlin allies demand a Ukraine peace deal first. Putin invites European envoys to Moscow.",
     "berlin", (13, 52)),
    ("Europe", "Climate", "COP31 closes with a $305bn adaptation gap",
     "The final draft drops fossil fuels and calls for tripling adaptation finance by 2035.",
     "cop31", (31, 37)),
]

SMALL = [
    ("Asia", "Diplomacy", "Albanese meets Xi in Shenzhen",
     "Fifth formal meeting. The Australian PM tells Putin to end the war.",
     "shenzhen", (114, 22)),
    ("Europe", "Conflict", "Crimean Bridge hit a third time",
     "Rail traffic halts after the overnight strike. The road span is already down.",
     "bridge", (36, 45)),
    ("Middle East", "Conflict", "Houthi missile hits Riyadh's tallest tower",
     "Windows blown out on seven floors of the PIF Tower in the KAFD.",
     "tower", (47, 25)),
    ("Latin America", "Diplomacy", "US and Venezuela restore military ties",
     "Hegseth signs a deal in Caracas. Joint training and intelligence sharing.",
     "caracas", (-67, 10)),
    ("Asia", "Conflict", "North Korea expands Yongbyon enrichment",
     "IAEA says a new extension is complete. Serious concern over the programme.",
     "yongbyon", (126, 39)),
    ("Asia", "Justice", "Seoul top court overturns ex-PM Han's term",
     "The 15-year sentence goes back for retrial. Detention extended two months.",
     "seoul", (127, 37)),
    ("Oceania", "Weather", "Fiji declares a national disaster",
     "El Nino drought drains water supplies. $20m set aside for relief.",
     "fiji", (178, -18)),
    ("Asia", "Markets", "Sensex jumps 989 points in a day",
     "Nifty reclaims 25,500 as auto and bank stocks lead the rebound.",
     "sensex", (72, 19)),
    ("Oceania", "Sport", "Nicholls 113 not out rescues New Zealand",
     "Hosts recover from 70 for 5 to 243 for 5 on day one in Wellington.",
     "cricket", (174, -41)),
    ("North America", "Tech", "Google ships Gemini 4 Neon",
     "Frontier-grade model at $3 per million tokens. Ranked third on the index.",
     "gemini", (-122, 37)),
    ("Middle East", "Conflict", "Iran still holds up to 2,500 missiles",
     "US intelligence estimate, low confidence, after months of strikes.",
     "missiles", (51, 36)),
    ("North America", "Markets", "Gold near $3,614 in its worst week since March",
     "The metal hits a 14-month low as hawkish Fed talk and an AI sell-off bite.",
     "gold", (-74, 41)),
]

BRIEFS = [
    ("Asia", "Diplomacy", "APEC adopts the Shenzhen Outlook on trade, data, AI."),
    ("North America", "Politics", "Trump to hold a White House press conference on Friday."),
    ("North America", "Politics", "Three Republicans backed the curb. One Democrat voted no."),
    ("Asia", "Markets", "Taiwan acts to steady stocks. Short-selling limits start."),
    ("Asia", "Politics", "Japan's Takaichi dodges a Taiwan contingency question."),
    ("North America", "Markets", "S and P 500 down 2.0 percent. Nikkei drops 4.68 percent."),
    ("North America", "Tech", "Nvidia faces a California probe after Huang's exit."),
    ("Europe", "Conflict", "Blast near the Dutch embassy in Kyiv. Minor damage."),
    ("Asia", "Tech", "Trump warns APEC nations on strict AI rules."),
    ("Asia", "Politics", "Modi opens FICCI's centenary convention in New Delhi."),
    ("North America", "Society", "World Children's Day marked around the globe."),
    ("Europe", "Conflict", "UK and Norway fund two Ukrainian naval craft."),
    ("Europe", "Politics", "Denmark approves a Greenland defence deal, 109 votes to none."),
    ("Middle East", "Conflict", "Gaza aid groups rate the peace plan 4 out of 26."),
    ("North America", "Politics", "Trump pardons baseball star Pete Rose, posthumously."),
    ("Europe", "Politics", "Serbia elects Aleksandar Cupic speaker, 140 votes."),
    ("Middle East", "Weather", "Saudi Arabia warns of storms and floods to 24 November."),
    ("Oceania", "Weather", "Storm alerts in the Cook Islands as Cyclone Xavier nears."),
    ("Middle East", "Markets", "Oil flat as Hormuz disruption offsets oversupply fears."),
    ("Asia", "Markets", "Rupee at 93.29 per dollar, its fourth straight gain."),
    ("Asia", "Diplomacy", "China urges Asia-Pacific economies to back open trade."),
    ("Oceania", "Markets", "Australian firms seek trade certainty in Beijing."),
    ("Middle East", "Conflict", "Iran steps up attacks on tankers in the Strait of Hormuz."),
    ("Africa", "Politics", "Five EU states plan a migrant centre in Rwanda."),
    ("Europe", "Diplomacy", "US envoy: Russia open to NATO-like guarantees for Ukraine."),
    ("Europe", "Conflict", "Ukraine: Neptune, Ruta and Flamingo missiles hit the bridge."),
    ("Europe", "Tech", "UK extends its NHS data contract with Palantir to 2029."),
    ("Europe", "Conflict", "UK hands a US soldier accused of spying to US military."),
    ("Asia", "Justice", "Philippine police file complaints against Thomas Markle."),
    ("Middle East", "Conflict", "Israeli ground operation in central Gaza forces displacement."),
    ("Europe", "Diplomacy", "Four nations urge Israel to allow aid into Gaza before winter."),
    ("Middle East", "Justice", "Jordan sentences three men to death for a church attack."),
    ("Europe", "Diplomacy", "Russia's ambassador to the US dies suddenly at 66."),
    ("Asia", "Politics", "APEC leaders discuss trade, investment and technology."),
]

TIMELINE = [
    ("00:00", "Gold $3,614"),
    ("01:45", "PIF Tower hit"),
    ("06:30", "Akvan landfall"),
    ("07:00", "Han term overturned"),
    ("10:00", "Sensex +989"),
    ("13:00", "COP31 $305bn gap"),
    ("15:00", "Albanese meets Xi"),
    ("19:00", "Trump: Iran waits"),
]

NUMBERS = [
    ("300,000", "evacuated from Akvan's path"),
    ("989", "points gained by the Sensex"),
    ("$305bn", "a year needed for adaptation"),
    ("113*", "Nicholls, not out, in Wellington"),
    ("$3,614", "an ounce of gold, 14-month low"),
    ("2,500", "missiles Iran still holds, at most"),
]

REGIONS = ["Asia", "Europe", "North America", "Middle East", "Oceania",
           "Africa", "Latin America"]
REGION_COLOURS = {
    "Asia": (178, 34, 52), "Europe": (31, 58, 95),
    "North America": (26, 110, 90), "Middle East": (176, 120, 24),
    "Oceania": (90, 90, 160), "Africa": (150, 90, 30),
    "Latin America": (120, 60, 120),
}
FIELDS = ["Politics", "Conflict", "Diplomacy", "Climate", "Markets", "Tech",
          "Weather", "Justice", "Sport", "Society"]
FIELD_COLOURS = {
    "Politics": (31, 58, 95), "Conflict": (178, 34, 52),
    "Diplomacy": (26, 110, 90), "Climate": (60, 140, 90),
    "Markets": (176, 120, 24), "Tech": (90, 90, 160),
    "Weather": (60, 120, 170), "Justice": (120, 60, 120),
    "Sport": (150, 90, 30), "Society": (110, 110, 100),
}

DATE_CHECK = ("DATE CHECK: Not 20 November news, and not shown as such. "
              "The ICJ ruling that Myanmar committed genocide against the "
              "Rohingya. Anthropic's $81.3bn IPO debut. The Shenzhen "
              "trilateral declaration by Trump, Xi and Putin. GTA VI release "
              "day. Hakeem Jeffries nominated as the first Black House "
              "Speaker. All first reported 19 November.")

# hand-tuned pin display positions on the map strip (x, y in final px)
PIN_POS = {
    1: (748, 918), 2: (298, 906), 3: (548, 897), 4: (590, 914),
    5: (829, 917), 6: (626, 892), 7: (643, 915), 8: (326, 925),
    9: (856, 906), 10: (878, 907), 11: (988, 944), 12: (712, 919),
    13: (968, 959), 14: (173, 907), 15: (668, 908), 16: (276, 920),
}


def s(v):
    return v * SS


def main():
    img = Image.new("RGB", (CW, CH), PAPER)
    d = ImageDraw.Draw(img)
    mx = s(12)
    right = CW - mx

    # paper grain, deterministic
    grain = Image.new("RGB", (CW, CH))
    gd = ImageDraw.Draw(grain)
    for _ in range(9000):
        x = RNG.randrange(CW)
        y = RNG.randrange(CH)
        v = RNG.randrange(232, 250)
        gd.point((x, y), fill=(v, v - 4, v - 14))
    img = Image.blend(img, grain, 0.05)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([mx, s(10), right, s(11)], fill=RULE)
    d.text((mx, s(16)), "THE WORLD IN ONE IMAGE",
           font=font(SANS_B, 11), fill=CRIMSON)
    d.text((right - d.textlength("50 STORIES  .  7 REGIONS  .  16 ILLUSTRATED",
                                 font=font(SANS_B, 11)), s(16)),
           "50 STORIES  .  7 REGIONS  .  16 ILLUSTRATED",
           font=font(SANS_B, 11), fill=NAVY)
    title = "Friday 20 November 2026"
    tf = font(SERIF_B, 40)
    d.text(((CW - d.textlength(title, font=tf)) / 2, s(28)), title, font=tf,
           fill=INK)
    d.rectangle([mx, s(70), right, s(71)], fill=RULE)

    # ---- timeline strip
    ty0, ty1 = s(76), s(100)
    d.rectangle([mx, ty0, right, ty1], fill=(238, 230, 208))
    d.text((mx + s(4), ty0 + s(7)), "THE DAY IN UTC",
           font=font(SANS_B, 10), fill=CRIMSON)
    tx0 = mx + s(118)
    tx1 = right - s(6)
    d.line([(tx0, ty0 + s(15)), (tx1, ty0 + s(15))], fill=RULE, width=SS)
    for i, (t, label) in enumerate(TIMELINE):
        frac = i / (len(TIMELINE) - 1)
        x = tx0 + (tx1 - tx0) * frac
        d.ellipse([x - s(3), ty0 + s(12), x + s(3), ty0 + s(18)], fill=CRIMSON)
        d.text((x - d.textlength(t, font=font(SANS_B, 8)) / 2, ty0 + s(2)), t,
               font=font(SANS_B, 8), fill=INK)
        lab = label if len(label) <= 26 else label[:24] + ".."
        lwdt = d.textlength(lab, font=font(SANS, 7))
        lx = min(max(x - lwdt / 2, tx0), tx1 - lwdt)
        d.text((lx, ty0 + s(19)), lab, font=font(SANS, 7), fill=MUTED)

    # ---- region bar and field bar, each with a legend line
    all_stories = [(r, f) for r, f, *_ in LEADS] + \
        [(r, f) for r, f, *_ in SMALL] + [(r, f) for r, f, _ in BRIEFS]
    rc = {r: sum(1 for a in all_stories if a[0] == r) for r in REGIONS}
    fc = {f: sum(1 for a in all_stories if a[1] == f) for f in FIELDS}
    total = len(all_stories)

    def legend(x, y, items, colours):
        cx = x
        for name, n, col in items:
            d.rectangle([cx, y, cx + s(7), y + s(7)], fill=col)
            txt = "%s %d" % (name, n)
            d.text((cx + s(9), y - s(1)), txt, font=font(SANS, 7.5), fill=INK)
            cx += s(9) + d.textlength(txt, font=font(SANS, 7.5)) + s(10)
        return cx

    d.text((mx, s(104)), "REGIONS", font=font(SANS_B, 8), fill=CRIMSON)
    bx = mx + s(56)
    for r in REGIONS:
        wdt = (right - bx) * rc[r] / total
        d.rectangle([bx, s(104), bx + wdt, s(110)], fill=REGION_COLOURS[r])
        bx += wdt
    legend(mx + s(56), s(112),
           [(r, rc[r], REGION_COLOURS[r]) for r in REGIONS], None)
    d.text((mx, s(121)), "FIELDS", font=font(SANS_B, 8), fill=NAVY)
    bx = mx + s(56)
    for f in FIELDS:
        wdt = (right - bx) * fc[f] / total if fc[f] else 0
        if wdt > s(1):
            d.rectangle([bx, s(121), bx + wdt, s(127)], fill=FIELD_COLOURS[f])
        bx += wdt
    legend(mx + s(56), s(129),
           [(f, fc[f], FIELD_COLOURS[f]) for f in FIELDS if fc[f]], None)

    # ---- lead cards, 2x2
    ly = s(140)
    lh = s(130)
    lw = (CW - 2 * mx - s(8)) // 2
    for i, (region, field, head, sub, scene, pin) in enumerate(LEADS):
        x = mx + (i % 2) * (lw + s(8))
        y = ly + (i // 2) * (lh + s(8))
        d.rectangle([x, y, x + lw, y + lh], fill=CARD, outline=RULE, width=SS)
        iw = s(196)
        SCENES[scene](d, (x + s(6), y + s(6), x + iw, y + lh - s(6)))
        d.rectangle([x + s(6), y + s(6), x + iw, y + lh - s(6)],
                    outline=(60, 50, 30), width=SS)
        nb = s(18)
        d.rectangle([x + s(6), y + s(6), x + s(6) + nb, y + s(6) + nb],
                    fill=CRIMSON)
        d.text((x + s(6) + nb / 2 - d.textlength(str(i + 1),
                font=font(SERIF_B, 11)) / 2, y + s(6) + s(2)), str(i + 1),
               font=font(SERIF_B, 11), fill=(255, 255, 255))
        tx = x + iw + s(12)
        tw = x + lw - tx - s(8)
        d.text((tx, y + s(8)), "%s  .  %s" % (region.upper(), field.upper()),
               font=font(SANS_B, 8), fill=REGION_COLOURS[region])
        lines = wrap(head, font(SERIF_B, 15.5), tw, d)
        yy = text_block(d, tx, y + s(22), lines[:3], font(SERIF_B, 15.5), INK,
                        s(17))
        slines = wrap(sub, font(SERIF, 10.5), tw, d)
        text_block(d, tx, yy + s(3), slines[:4], font(SERIF, 10.5), MUTED,
                   s(12))

    # ---- small cards, 4x3
    sy = ly + 2 * (lh + s(8))
    sh = s(78)
    sw = (CW - 2 * mx - 3 * s(8)) // 4
    for i, (region, field, head, sub, scene, pin) in enumerate(SMALL):
        n = i + 5
        x = mx + (i % 4) * (sw + s(8))
        y = sy + (i // 4) * (sh + s(8))
        d.rectangle([x, y, x + sw, y + sh], fill=CARD, outline=RULE, width=SS)
        iw = s(76)
        SCENES[scene](d, (x + s(4), y + s(4), x + iw, y + sh - s(4)))
        d.rectangle([x + s(4), y + s(4), x + iw, y + sh - s(4)],
                    outline=(60, 50, 30), width=SS)
        nb = s(15)
        d.rectangle([x + s(4), y + s(4), x + s(4) + nb, y + s(4) + nb],
                    fill=REGION_COLOURS[region])
        d.text((x + s(4) + nb / 2 - d.textlength(str(n),
                font=font(SERIF_B, 9)) / 2, y + s(4) + s(1)), str(n),
               font=font(SERIF_B, 9), fill=(255, 255, 255))
        tx = x + iw + s(8)
        tw = x + sw - tx - s(6)
        d.text((tx, y + s(5)), "%s . %s" % (region.upper(), field.upper()),
               font=font(SANS_B, 7), fill=REGION_COLOURS[region])
        lines = wrap(head, font(SERIF_B, 11), tw, d)
        yy = text_block(d, tx, y + s(16), lines[:2], font(SERIF_B, 11), INK,
                        s(12.5))
        slines = wrap(sub, font(SERIF, 8.5), tw, d)
        text_block(d, tx, yy + s(2), slines[:2], font(SERIF, 8.5), MUTED,
                   s(10))

    # ---- briefs band
    by = sy + 3 * (sh + s(8)) + s(2)
    bh = s(148)
    d.rectangle([mx, by, right, by + bh], fill=(240, 233, 210))
    d.text((mx + s(6), by + s(4)), "THE REST OF THE DAY, IN BRIEF",
           font=font(SANS_B, 10), fill=CRIMSON)
    d.text((right - d.textlength("17 to 50", font=font(SANS_B, 10)),
            by + s(4)), "17 to 50", font=font(SANS_B, 10), fill=NAVY)
    cols = [BRIEFS[i::3] for i in range(3)]
    colw = (CW - 2 * mx - s(12)) // 3
    bf = font(SERIF, 9.5)
    for ci, col in enumerate(cols):
        cx = mx + s(6) + ci * colw
        yy = by + s(20)
        for j, (region, field, text) in enumerate(col):
            num = 17 + ci + 3 * j
            d.text((cx, yy), "%d." % num, font=font(SERIF_B, 9.5), fill=CRIMSON)
            tw = colw - s(24)
            line = text
            while d.textlength(line, font=bf) > tw and len(line) > 20:
                line = line[:line.rfind(" ")].rstrip() + ".."
            d.text((cx + s(18), yy), line, font=bf, fill=INK)
            yy += s(10.5)

    # ---- day in numbers
    ny = by + bh + s(6)
    nh = s(34)
    d.rectangle([mx, ny, right, ny + nh], fill=NAVY)
    d.text((mx + s(8), ny + s(4)), "DAY IN NUMBERS",
           font=font(SANS_B, 10), fill=(255, 220, 120))
    nx = mx + s(132)
    segw = (right - nx - s(8)) / len(NUMBERS)
    for i, (val, lab) in enumerate(NUMBERS):
        x = nx + i * segw
        d.text((x, ny + s(3)), val, font=font(SERIF_B, 13),
               fill=(255, 255, 255))
        d.text((x, ny + s(19)), lab, font=font(SANS, 7.5),
               fill=(200, 210, 225))

    # ---- world map strip
    my = ny + nh + s(6)
    mh = s(100)
    d.rectangle([mx, my, right, my + mh], fill=(214, 226, 232))
    d.text((mx + s(6), my + s(3)), "WHERE IT HAPPENED",
           font=font(SANS_B, 9), fill=NAVY)
    d.text((right - d.textlength("Pins 1 to 16 match the illustrated cards",
                                 font=font(SANS, 8)), my + s(4)),
           "Pins 1 to 16 match the illustrated cards", font=font(SANS, 8),
           fill=MUTED)
    continents = [
        # North America
        [(60, 30), (95, 22), (140, 26), (185, 40), (230, 32), (255, 48),
         (285, 42), (300, 60), (270, 78), (235, 92), (200, 84), (160, 88),
         (120, 78), (80, 60), (55, 44)],
        # Greenland
        [(300, 18), (330, 14), (345, 26), (318, 32)],
        # South America
        [(300, 108), (330, 100), (360, 112), (372, 140), (352, 168),
         (330, 178), (312, 150), (296, 124)],
        # Africa
        [(480, 96), (530, 84), (585, 92), (610, 116), (590, 152),
         (560, 178), (530, 168), (500, 138), (472, 112)],
        # Eurasia
        [(560, 78), (600, 60), (660, 52), (730, 40), (800, 30),
         (880, 26), (950, 34), (985, 48), (960, 66), (920, 60),
         (880, 78), (830, 72), (790, 88), (740, 84), (700, 96),
         (650, 88), (600, 96), (565, 88)],
        # India
        [(700, 96), (725, 92), (735, 112), (715, 124), (700, 110)],
        # SE Asia islands
        [(820, 96), (845, 92), (855, 104), (832, 108)],
        # Australia
        [(860, 140), (910, 132), (945, 142), (940, 162), (895, 170),
         (865, 158)],
        # UK
        [(540, 40), (552, 36), (556, 48), (544, 52)],
        # Japan
        [(920, 48), (932, 44), (940, 58), (928, 62)],
    ]
    mapx, mapy = mx, my + s(12)
    mw, mh2 = CW - 2 * mx, mh - s(14)
    for poly in continents:
        pts = [(mapx + px / 1000 * mw, mapy + py / 200 * mh2) for px, py in poly]
        d.polygon(pts, fill=(120, 150, 110), outline=(70, 95, 70))
    for n, (px, py) in PIN_POS.items():
        x, y = s(px), s(py)
        d.ellipse([x - s(8), y - s(8), x + s(8), y + s(8)], fill=CRIMSON,
                  outline=(255, 255, 255), width=SS)
        d.text((x - d.textlength(str(n), font=font(SERIF_B, 9)) / 2,
                y - s(6)), str(n), font=font(SERIF_B, 9), fill=(255, 255, 255))

    # ---- date check footer
    fy = my + mh + s(6)
    fh = s(38)
    d.rectangle([mx, fy, right, fy + fh], fill=(238, 230, 208))
    lines = wrap(DATE_CHECK, font(SERIF, 9.5), CW - 2 * mx - s(16), d)
    text_block(d, mx + s(8), fy + s(4), lines[:3], font(SERIF, 9.5), INK,
               s(12))
    d.rectangle([mx, fy + fh + s(4), right, fy + fh + s(5)], fill=RULE)

    img = img.resize((W, H), Image.LANCZOS)
    img.save(OUT, format="PNG", optimize=False, compress_level=6)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
