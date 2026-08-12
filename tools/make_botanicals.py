#!/usr/bin/env python3
"""
make_botanicals.py — original botanical line-art for the Sambodhi watermark layer.

Draws three new pieces, all in the same hairline idiom as the existing artwork
(fine unfilled strokes, organic curves, no fills) but sized for the large
desktop canvases where the old 700x420 pieces read as too small:

  wm-bloom.svg    900 x 900   open lotus/peony bloom + leaves   -> corners
  wm-branch.svg   560 x 1000  tall flowering branch             -> left/right edges
  wm-vine.svg     1000 x 560  trailing vine with blossoms       -> top/bottom edges

Shapes are computed rather than hand-plotted so leaves sit on the stem tangent
and petals fan evenly, with small deterministic jitter so nothing looks stamped.
"""

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
INK = "#17291E"

# ----------------------------------------------------------------- primitives


def bez(p0, p1, p2, p3, t):
    """Point on a cubic Bezier."""
    u = 1 - t
    x = u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0]
    y = u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]
    return x, y


def bez_tan(p0, p1, p2, p3, t):
    """Unit tangent angle (radians) on a cubic Bezier."""
    u = 1 - t
    dx = 3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0])
    dy = 3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1])
    return math.atan2(dy, dx)


def f(v):
    return f"{v:.1f}"


def rot(px, py, cx, cy, a):
    s, c = math.sin(a), math.cos(a)
    dx, dy = px - cx, py - cy
    return cx + dx * c - dy * s, cy + dx * s + dy * c


# ----------------------------------------------------------------- components


def qbez(p0, c, p1, t):
    """Point on a quadratic Bezier."""
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0],
            u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1])


def leaf(cx, cy, ang, length, width, veins=4, curl=0.30):
    """Lanceolate leaf: two flanks, a curved midrib, and veins that stay inside it."""
    out = []
    base = (cx, cy)
    tip = (cx + math.cos(ang) * length, cy + math.sin(ang) * length)
    px, py = math.cos(ang + math.pi / 2), math.sin(ang + math.pi / 2)
    m = 0.46
    bow = width * curl * 0.5          # both flanks bow the same way -> drawn feel

    ctrl = {}
    for side in (1, -1):
        ctrl[side] = (cx + math.cos(ang) * length * m + px * (width * side + bow),
                      cy + math.sin(ang) * length * m + py * (width * side + bow))
        out.append(f'<path d="M{f(base[0])},{f(base[1])} '
                   f'Q{f(ctrl[side][0])},{f(ctrl[side][1])} {f(tip[0])},{f(tip[1])}"/>')

    mid = (cx + math.cos(ang) * length * 0.5 + px * bow,
           cy + math.sin(ang) * length * 0.5 + py * bow)
    out.append(f'<path d="M{f(base[0])},{f(base[1])} Q{f(mid[0])},{f(mid[1])} {f(tip[0])},{f(tip[1])}"/>')

    # veins run from a point on the midrib to a point further along the flank,
    # both sampled from the real curves, so they can never fall outside the leaf
    for i in range(1, veins + 1):
        t = i / (veins + 1.0)
        a = qbez(base, mid, tip, t)
        for side in (1, -1):
            e = qbez(base, ctrl[side], tip, min(t + 0.16, 0.97))
            ex = a[0] + (e[0] - a[0]) * 0.80
            ey = a[1] + (e[1] - a[1]) * 0.80
            qx = a[0] + (e[0] - a[0]) * 0.42 + math.cos(ang) * width * 0.06
            qy = a[1] + (e[1] - a[1]) * 0.42 + math.sin(ang) * width * 0.06
            out.append(f'<path d="M{f(a[0])},{f(a[1])} Q{f(qx)},{f(qy)} {f(ex)},{f(ey)}"/>')
    return out


def petal(cx, cy, ang, length, width, pinch=0.42, r0=0.0):
    """Teardrop petal. r0 lifts the origin off the centre so hubs stay open."""
    sx = cx + math.cos(ang) * r0
    sy = cy + math.sin(ang) * r0
    L = length - r0
    tipx, tipy = sx + math.cos(ang) * L, sy + math.sin(ang) * L
    px, py = math.cos(ang + math.pi / 2), math.sin(ang + math.pi / 2)
    parts = []
    for side in (1, -1):
        c1x = sx + math.cos(ang) * L * pinch + px * width * side
        c1y = sy + math.sin(ang) * L * pinch + py * width * side
        c2x = sx + math.cos(ang) * L * 0.86 + px * width * 0.52 * side
        c2y = sy + math.sin(ang) * L * 0.86 + py * width * 0.52 * side
        parts.append(f'<path d="M{f(sx)},{f(sy)} C{f(c1x)},{f(c1y)} '
                     f'{f(c2x)},{f(c2y)} {f(tipx)},{f(tipy)}"/>')
    return parts


def blossom(cx, cy, r, n=5, phase=0.0, stamens=True, rnd=None):
    """Small open flower: n petals off an open hub, plus a short stamen cluster."""
    out = []
    rnd = rnd or random.Random(1)
    hub = r * 0.20
    for i in range(n):
        a = phase + i * (2 * math.pi / n) + rnd.uniform(-0.05, 0.05)
        out += petal(cx, cy, a, r * rnd.uniform(0.92, 1.08), r * 0.40, r0=hub)
    out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(hub)}"/>')
    if stamens:
        for i in range(6):
            a = phase + i * (2 * math.pi / 6) + 0.3
            sx, sy = cx + math.cos(a) * hub, cy + math.sin(a) * hub
            ex, ey = cx + math.cos(a) * r * 0.40, cy + math.sin(a) * r * 0.40
            out.append(f'<path d="M{f(sx)},{f(sy)} L{f(ex)},{f(ey)}"/>')
            out.append(f'<circle cx="{f(ex)}" cy="{f(ey)}" r="{f(r * 0.05)}"/>')
    return out


def bud(cx, cy, ang, size):
    """Closed teardrop bud on a short pedicel."""
    out = petal(cx, cy, ang, size, size * 0.38, pinch=0.5)
    # calyx
    for side in (1, -1):
        ex = cx + math.cos(ang + side * 0.9) * size * 0.30
        ey = cy + math.sin(ang + side * 0.9) * size * 0.30
        out.append(f'<path d="M{f(cx)},{f(cy)} Q{f((cx + ex) / 2)},{f((cy + ey) / 2)} {f(ex)},{f(ey)}"/>')
    return out


def tendril(cx, cy, ang, size, turns=1.6, cw=1):
    """A curling tendril, drawn as a polyline spiral."""
    pts = []
    steps = 46
    for i in range(steps + 1):
        t = i / steps
        a = ang + cw * turns * 2 * math.pi * t
        r = size * (1 - t) ** 1.25
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts)
    return [f'<path d="{d}"/>']


def wrap(w, h, body, sw=1.4):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}">'
        f'<g fill="none" stroke="{INK}" stroke-width="{sw}" '
        f'stroke-linecap="round" stroke-linejoin="round">'
        + "".join(body)
        + "</g></svg>"
    )


# ----------------------------------------------------------------- the pieces


def make_bloom():
    """900x900 — one oversized open bloom with foliage. Corner piece."""
    rnd = random.Random(7)
    W = H = 900
    cx, cy = 452.0, 430.0
    g = []

    # petals sit on rings that start clear of the hub, so the centre stays open
    rings = [
        (9, 372.0, 0.30, 0.00, 74.0),
        (8, 262.0, 0.31, 0.36, 58.0),
        (6, 162.0, 0.34, 0.62, 42.0),
    ]
    for n, length, wf, ph, r0 in rings:
        for i in range(n):
            a = ph + i * (2 * math.pi / n) + rnd.uniform(-0.03, 0.03)
            L = length * rnd.uniform(0.95, 1.05)
            g += petal(cx, cy, a, L, L * wf, pinch=0.42, r0=r0)
            if length > 200:      # one fold line down the larger petals
                s = (cx + math.cos(a) * r0, cy + math.sin(a) * r0)
                e = (cx + math.cos(a) * L * 0.80, cy + math.sin(a) * L * 0.80)
                q = (cx + math.cos(a + 0.09) * L * 0.46, cy + math.sin(a + 0.09) * L * 0.46)
                g.append(f'<path d="M{f(s[0])},{f(s[1])} Q{f(q[0])},{f(q[1])} {f(e[0])},{f(e[1])}"/>')

    # stamen crown, started off the hub circle rather than the exact centre
    hub = 30.0
    for i in range(16):
        a = i * (2 * math.pi / 16) + 0.11
        r = 68 * rnd.uniform(0.82, 1.0)
        s = (cx + math.cos(a) * hub, cy + math.sin(a) * hub)
        e = (cx + math.cos(a) * r, cy + math.sin(a) * r)
        q = (cx + math.cos(a - 0.22) * (hub + r) * 0.42, cy + math.sin(a - 0.22) * (hub + r) * 0.42)
        g.append(f'<path d="M{f(s[0])},{f(s[1])} Q{f(q[0])},{f(q[1])} {f(e[0])},{f(e[1])}"/>')
        g.append(f'<circle cx="{f(e[0])}" cy="{f(e[1])}" r="3.2"/>')
    g.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(hub)}"/>')

    # stem down out of frame, with pads and a bud
    p0, p1, p2, p3 = (cx, cy + 120), (470, 620), (392, 730), (410, 920)
    d = f"M{f(p0[0])},{f(p0[1])} C{f(p1[0])},{f(p1[1])} {f(p2[0])},{f(p2[1])} {f(p3[0])},{f(p3[1])}"
    g.append(f'<path d="{d}"/>')

    for t, ang, L, Wd in [(0.30, 3.55, 300, 96), (0.52, -0.45, 268, 88), (0.78, 3.30, 210, 70)]:
        x, y = bez(p0, p1, p2, p3, t)
        g += leaf(x, y, ang, L, Wd, veins=5)

    bx, by = bez(p0, p1, p2, p3, 0.42)
    g.append(f'<path d="M{f(bx)},{f(by)} Q{f(bx + 96)},{f(by - 26)} {f(bx + 148)},{f(by - 96)}"/>')
    g += bud(bx + 148, by - 96, -0.95, 92)

    # a couple of drifting seed heads for air
    for sx, sy, sr in [(146, 176, 54), (770, 214, 44)]:
        for i in range(16):
            a = i * (2 * math.pi / 16)
            ex, ey = sx + math.cos(a) * sr, sy + math.sin(a) * sr
            bx0, by0 = sx + math.cos(a) * sr * 0.16, sy + math.sin(a) * sr * 0.16
            g.append(f'<path d="M{f(bx0)},{f(by0)} L{f(ex)},{f(ey)}"/>')
            g.append(f'<circle cx="{f(ex)}" cy="{f(ey)}" r="2.6"/>')

    return wrap(W, H, g, sw=1.5)


def make_branch():
    """560x1000 — tall flowering branch. Reads well entering a left/right edge."""
    rnd = random.Random(23)
    W, H = 560, 1000
    g = []

    p0, p1, p2, p3 = (78.0, 1030.0), (206.0, 760.0), (128.0, 430.0), (330.0, -40.0)
    d = f"M{f(p0[0])},{f(p0[1])} C{f(p1[0])},{f(p1[1])} {f(p2[0])},{f(p2[1])} {f(p3[0])},{f(p3[1])}"
    g.append(f'<path d="{d}"/>')

    # a secondary shoot splitting off low down
    q0, q1, q2, q3 = (128.0, 862.0), (300.0, 760.0), (392.0, 600.0), (508.0, 388.0)
    g.append(
        f'<path d="M{f(q0[0])},{f(q0[1])} C{f(q1[0])},{f(q1[1])} '
        f'{f(q2[0])},{f(q2[1])} {f(q3[0])},{f(q3[1])}"/>'
    )

    # leaves alternate along the main stem, shrinking toward the tip
    for i, t in enumerate([0.06, 0.16, 0.27, 0.38, 0.49, 0.60, 0.71, 0.82, 0.91]):
        x, y = bez(p0, p1, p2, p3, t)
        tan = bez_tan(p0, p1, p2, p3, t)
        side = 1 if i % 2 == 0 else -1
        ang = tan + side * rnd.uniform(0.85, 1.15)
        L = (232 - 132 * t) * rnd.uniform(0.9, 1.1)
        g += leaf(x, y, ang, L, L * 0.33, veins=4)

    for i, t in enumerate([0.22, 0.46, 0.70, 0.90]):
        x, y = bez(q0, q1, q2, q3, t)
        tan = bez_tan(q0, q1, q2, q3, t)
        side = -1 if i % 2 == 0 else 1
        L = (176 - 76 * t) * rnd.uniform(0.9, 1.08)
        g += leaf(x, y, tan + side * 1.0, L, L * 0.32, veins=3)

    # blossoms at the nodes
    for t, r in [(0.34, 62.0), (0.63, 54.0), (0.86, 44.0)]:
        x, y = bez(p0, p1, p2, p3, t)
        tan = bez_tan(p0, p1, p2, p3, t)
        px = x + math.cos(tan - 1.1) * r * 1.5
        py = y + math.sin(tan - 1.1) * r * 1.5
        g.append(f'<path d="M{f(x)},{f(y)} Q{f((x + px) / 2 - 14)},{f((y + py) / 2)} {f(px)},{f(py)}"/>')
        g += blossom(px, py, r, n=6, phase=rnd.uniform(0, 1.2), rnd=rnd)

    x, y = bez(q0, q1, q2, q3, 0.58)
    g += blossom(x + 46, y - 40, 48, n=5, phase=0.5, rnd=rnd)

    # buds and a tendril for lightness
    x, y = bez(p0, p1, p2, p3, 0.52)
    g += bud(x + 92, y - 58, -0.7, 62)
    x, y = bez(p0, p1, p2, p3, 0.76)
    g += bud(x - 74, y - 36, 3.7, 50)
    x, y = bez(q0, q1, q2, q3, 0.84)
    g += tendril(x + 30, y - 22, 0.4, 74, turns=1.5, cw=-1)

    return wrap(W, H, g, sw=1.45)


def make_vine():
    """1000x560 — horizontal trailing vine. For top and bottom edge entries."""
    rnd = random.Random(41)
    W, H = 1000, 560
    g = []

    p0, p1, p2, p3 = (-40.0, 402.0), (240.0, 250.0), (610.0, 470.0), (1040.0, 214.0)
    d = f"M{f(p0[0])},{f(p0[1])} C{f(p1[0])},{f(p1[1])} {f(p2[0])},{f(p2[1])} {f(p3[0])},{f(p3[1])}"
    g.append(f'<path d="{d}"/>')

    for i, t in enumerate([0.05, 0.14, 0.23, 0.32, 0.41, 0.50, 0.59, 0.68, 0.77, 0.86, 0.95]):
        x, y = bez(p0, p1, p2, p3, t)
        tan = bez_tan(p0, p1, p2, p3, t)
        side = 1 if i % 2 == 0 else -1
        L = rnd.uniform(150, 214)
        g += leaf(x, y, tan + side * rnd.uniform(0.95, 1.25), L, L * 0.34, veins=4)

    for t, r in [(0.18, 56.0), (0.47, 66.0), (0.74, 50.0)]:
        x, y = bez(p0, p1, p2, p3, t)
        tan = bez_tan(p0, p1, p2, p3, t)
        px = x + math.cos(tan - 1.25) * r * 1.7
        py = y + math.sin(tan - 1.25) * r * 1.7
        g.append(f'<path d="M{f(x)},{f(y)} Q{f((x + px) / 2)},{f((y + py) / 2 - 16)} {f(px)},{f(py)}"/>')
        g += blossom(px, py, r, n=6, phase=rnd.uniform(0, 1.0), rnd=rnd)

    for t, cw in [(0.30, 1), (0.62, -1), (0.88, 1)]:
        x, y = bez(p0, p1, p2, p3, t)
        tan = bez_tan(p0, p1, p2, p3, t)
        g += tendril(x, y, tan + cw * 1.3, 66, turns=1.7, cw=cw)

    x, y = bez(p0, p1, p2, p3, 0.36)
    g += bud(x + 40, y + 96, 1.35, 58)

    return wrap(W, H, g, sw=1.45)


if __name__ == "__main__":
    jobs = {
        "wm-bloom.svg": make_bloom(),
        "wm-branch.svg": make_branch(),
        "wm-vine.svg": make_vine(),
    }
    for name, svg in jobs.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"{name:16} {len(svg):>7,} bytes")
