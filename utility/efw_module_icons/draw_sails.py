"""Procedurally drawn sail icons (76x42, naval module size).

There is no vanilla sail icon to recolour, so the sails are drawn: shapes are
rasterised at 4x and averaged down for soft edges, then given a dark outline
like the vanilla module icons.
"""
import math
import random

W, H, S = 76, 42, 4

CANVAS = (236, 224, 192)
CANVAS_SHADE = (168, 150, 112)
PATCH = (182, 150, 104)
SEAM = (196, 182, 148)
WOOD = (112, 72, 38)
WOOD_LIGHT = (160, 110, 62)
ROPE = (90, 76, 58)
OUTLINE = (48, 38, 28)


def _inside(poly, x, y):
    hit = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            hit = not hit
        j = i
    return hit


def _curve(p0, p1, bulge, n=16):
    """Points from p0 to p1 bowed sideways by `bulge` (perpendicular offset)."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy) or 1
    nx, ny = -dy / length, dx / length
    return [(x0 + dx * t + nx * bulge * math.sin(math.pi * t),
             y0 + dy * t + ny * bulge * math.sin(math.pi * t)) for t in (i / n for i in range(n + 1))]


class Canvas:
    def __init__(self):
        self.px = [[None] * (W * S) for _ in range(H * S)]

    def poly(self, pts, colour_fn):
        pts = [(x * S, y * S) for x, y in pts]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        for y in range(max(0, int(min(ys))), min(H * S, int(max(ys)) + 1)):
            for x in range(max(0, int(min(xs))), min(W * S, int(max(xs)) + 1)):
                if _inside(pts, x + .5, y + .5):
                    self.px[y][x] = colour_fn(x / S, y / S)

    def rect(self, x0, y0, x1, y1, colour):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], lambda x, y: colour)

    def line(self, p0, p1, width, colour):
        (x0, y0), (x1, y1) = p0, p1
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy) or 1
        nx, ny = -dy / length * width / 2, dx / length * width / 2
        self.poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)],
                  lambda x, y: colour)

    def finish(self):
        """Average 4x4 blocks, then add a 1px dark outline around the shape."""
        out = []
        for y in range(H):
            row = []
            for x in range(W):
                cols = [self.px[y * S + j][x * S + i] for j in range(S) for i in range(S)]
                cols = [c for c in cols if c]
                if not cols:
                    row.append((0, 0, 0, 0))
                    continue
                a = len(cols) * 255 // (S * S)
                row.append(tuple(sum(c[k] for c in cols) // len(cols) for k in range(3)) + (a,))
            out.append(row)
        outlined = [r[:] for r in out]
        for y in range(H):
            for x in range(W):
                if out[y][x][3] > 40:
                    continue
                near = max((out[yy][xx][3] for yy in range(max(0, y - 1), min(H, y + 2))
                            for xx in range(max(0, x - 1), min(W, x + 2))), default=0)
                if near > 120:
                    outlined[y][x] = OUTLINE + (min(200, near),)
        return outlined


def _canvas_shader(x_light, x_dark, seams, patches, rnd):
    """Canvas colour: lit near x_light, shaded towards x_dark, with seams and patches."""
    def shade(x, y):
        t = min(1.0, max(0.0, (x - x_light) / (x_dark - x_light))) if x_dark != x_light else 0
        c = tuple(int(a + (b - a) * t * 0.8) for a, b in zip(CANVAS, CANVAS_SHADE))
        if any(abs(y - s) < 0.35 for s in seams):
            c = tuple(int(v * 0.86) for v in c)
        for (px0, py0, px1, py1) in patches:
            if px0 <= x <= px1 and py0 <= y <= py1:
                edge = min(x - px0, px1 - x, y - py0, py1 - y) < 0.4
                c = tuple(int(v * (0.7 if edge else 1)) for v in PATCH)
        return c
    return shade


def _hull(cv):
    cv.poly([(14, 34), (62, 34), (57, 39), (19, 39)], lambda x, y: WOOD if y > 36.5 else WOOD_LIGHT)


def small_sail():
    rnd = random.Random(5)
    cv = Canvas()
    _hull(cv)
    cv.line((37, 4), (37, 35), 2.2, WOOD)                      # mast
    cv.line((37, 31), (62, 30), 1.4, WOOD_LIGHT)               # boom
    sail = [(38.2, 5)] + _curve((38.2, 5), (61, 29.5), 4)[1:] + [(38.2, 30)]
    cv.poly(sail, _canvas_shader(39, 60, seams=(12, 19, 25), patches=[(44, 20, 49, 24)], rnd=rnd))
    cv.line((37, 4), (16, 33), 0.8, ROPE)                      # forestay
    return cv.finish()


def large_sail():
    rnd = random.Random(11)
    cv = Canvas()
    _hull(cv)
    # drawn back to front: jib, mast, square sails, then the yards on top
    cv.poly([(41, 4), (13, 33), (23, 33)], _canvas_shader(13, 40, seams=(), patches=[], rnd=rnd))
    cv.line((41, 4), (13, 34), 0.8, ROPE)                      # forestay
    cv.line((42, 2), (42, 35), 2.4, WOOD)                      # mast
    upper = _curve((33, 8), (51, 8), 0)[:1] + _curve((51, 8), (53, 18), -1.5)[1:] + \
        _curve((53, 18), (31, 18), 0)[1:] + _curve((31, 18), (33, 8), -1.5)[1:]
    lower = _curve((28, 21), (56, 21), 0)[:1] + _curve((56, 21), (59, 32), -2)[1:] + \
        _curve((59, 32), (25, 32), 0)[1:] + _curve((25, 32), (28, 21), -2)[1:]
    cv.poly(upper, _canvas_shader(33, 53, seams=(11.5, 14.5), patches=[(45, 10, 49, 14)], rnd=rnd))
    cv.poly(lower, _canvas_shader(27, 59, seams=(25, 28.5), patches=[(30, 24, 35, 28)], rnd=rnd))
    cv.line((31, 7.5), (53, 7.5), 1.6, WOOD_LIGHT)             # upper yard
    cv.line((26, 20.5), (58, 20.5), 1.8, WOOD_LIGHT)           # lower yard
    return cv.finish()
