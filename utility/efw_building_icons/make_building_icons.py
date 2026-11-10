"""Disegna le icone dei 4 edifici strategici EFW e le aggiunge alla strip degli edifici.

    python utility/efw_building_icons/make_building_icons.py

Stile vanilla: glifo arancione sfumato (giallo in alto, arancio scuro in basso)
con ombra, su fondo scuro preso da un'icona vanilla della strip.
La strip passa da 40 a 44 frame:
    41 Centro di Propaganda e Mobilitazione   megafono con onde sonore
    42 Direzione del Lavoro Nazionale         ingranaggio con martello
    43 Centro Logistico e Difesa Civile       scudo con cassa
    44 Centro Nazionale di Ricerca            beuta con bolle
Se la strip ha già 44 frame, i 4 frame EFW vengono ridisegnati (lo script è ripetibile).
Ricordarsi noOfFrames = 44 in interface/countrystateview.gfx.
"""
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'utility', 'efw_laws'))
from dds_tool import read_dds, write_dds, write_png  # noqa: E402

STRIP = os.path.join(ROOT, 'gfx', 'interface', 'buildings', 'building_icon_strip.dds')
BASE_FRAMES = 40
SS = 4  # supersampling per l'antialiasing


# ---------------------------------------------------------------- forme
# Ogni forma è una funzione (x, y) -> bool in coordinate 0..46 del frame.

def circle(cx, cy, r):
    return lambda x, y: (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def ring(cx, cy, r0, r1, a0=-math.pi, a1=math.pi):
    def f(x, y):
        d = math.hypot(x - cx, y - cy)
        a = math.atan2(y - cy, x - cx)
        return r0 <= d <= r1 and a0 <= a <= a1
    return f


def rect(x0, y0, x1, y1):
    return lambda x, y: x0 <= x <= x1 and y0 <= y <= y1


def poly(pts):
    def f(x, y):
        inside = False
        j = len(pts) - 1
        for i in range(len(pts)):
            xi, yi = pts[i]
            xj, yj = pts[j]
            if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                inside = not inside
            j = i
        return inside
    return f


def rotated(shape, cx, cy, ang):
    c, s = math.cos(-ang), math.sin(-ang)
    return lambda x, y: shape(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c)


def union(*shapes):
    return lambda x, y: any(s(x, y) for s in shapes)


def minus(a, *b):
    return lambda x, y: a(x, y) and not any(s(x, y) for s in b)


# ---------------------------------------------------------------- glifi

def megaphone():
    body = poly([(9, 19), (17, 19), (30, 11), (30, 35), (17, 27), (9, 27)])
    handle = poly([(14, 27), (19, 27), (21, 34), (17, 35)])
    waves = union(ring(30, 23, 5, 7, -0.9, 0.9), ring(30, 23, 9.5, 11.5, -0.9, 0.9))
    return union(body, handle, waves)


def gear_hammer():
    cx, cy = 19, 22
    teeth = union(*[rotated(rect(cx - 2.6, cy - 13.5, cx + 2.6, cy - 8), cx, cy, k * math.pi / 4) for k in range(8)])
    gear = minus(union(circle(cx, cy, 10), teeth), circle(cx, cy, 4.2))

    # martello diagonale sopra l'ingranaggio, staccato da un bordo scuro
    def hammer_shape(grow):
        head = rect(22 - grow, 9 - grow, 38 + grow, 16 + grow)
        shaft = rect(28 - grow, 16 - grow, 32 + grow, 40 + grow)
        return rotated(union(head, shaft), 30, 25, 0.62)
    return union(minus(gear, hammer_shape(1.8)), hammer_shape(0))


def shield_crate():
    shield = poly([(23, 5), (38, 10), (37, 24), (31, 34), (23, 41), (15, 34), (9, 24), (8, 10)])
    inner = poly([(23, 8.5), (35, 12.5), (34, 23.5), (29.5, 31.5), (23, 37.5), (16.5, 31.5), (12, 23.5), (11, 12.5)])
    box = rect(16, 15, 30, 29)
    box_hole = rect(18.2, 17.2, 27.8, 26.8)
    plank = rect(16, 21, 30, 23)
    return union(minus(shield, inner), minus(box, box_hole), plank)


def flask():
    neck = rect(19, 7, 27, 18)
    rim = rect(17, 6, 29, 9)
    body = poly([(19, 17), (27, 17), (38, 37), (36, 40), (10, 40), (8, 37)])
    liquid_line = rect(11, 26, 35, 27.5)
    bubbles = union(circle(19, 33, 2.2), circle(27, 31, 1.6), circle(24, 36, 1.3))
    return union(rim, minus(union(neck, body), liquid_line, bubbles))


GLYPHS = [megaphone, gear_hammer, shield_crate, flask]


# ---------------------------------------------------------------- rendering

def coverage(shape, size):
    cov = [[0.0] * size for _ in range(size)]
    step = 1.0 / SS
    for y in range(size):
        for x in range(size):
            n = 0
            for sy in range(SS):
                for sx in range(SS):
                    if shape(x + (sx + 0.5) * step, y + (sy + 0.5) * step):
                        n += 1
            cov[y][x] = n / (SS * SS)
    return cov


def orange(y, size):
    """Gradiente vanilla: giallo-arancio in alto, arancio bruciato in basso."""
    t = min(1.0, max(0.0, (y - 6) / (size - 12)))
    top, bot = (255, 196, 64), (232, 96, 10)
    return tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))


def background(strip, fw, h, frame_index):
    """Fondo scuro di un'icona vanilla, con il glifo cancellato riga per riga."""
    w, _, px = strip
    x0 = frame_index * fw
    frame = [list(row[x0:x0 + fw]) for row in px]
    for y in range(5, h - 5):
        ref = frame[y][6]
        for x in range(6, fw - 6):
            frame[y][x] = ref
    return frame


def draw(bg, glyph, size):
    cov = coverage(glyph(), size)
    out = [list(r) for r in bg]
    # ombra 1px in basso a destra
    for y in range(size):
        for x in range(size):
            c = cov[y - 1][x - 1] if x > 0 and y > 0 else 0
            if c:
                r, g, b, a = out[y][x]
                k = 1 - 0.55 * c
                out[y][x] = (int(r * k), int(g * k), int(b * k), a)
    for y in range(size):
        col = orange(y, size)
        for x in range(size):
            c = cov[y][x]
            if c:
                r, g, b, a = out[y][x]
                out[y][x] = (int(col[0] * c + r * (1 - c)), int(col[1] * c + g * (1 - c)),
                             int(col[2] * c + b * (1 - c)), a)
    return out


def main():
    strip = read_dds(STRIP)
    w, h, px = strip
    fw = h  # frame quadrati
    frames = w // fw
    if frames not in (BASE_FRAMES, BASE_FRAMES + len(GLYPHS)):
        sys.exit('strip inattesa: %d frame' % frames)
    base = [row[:BASE_FRAMES * fw] for row in px]
    bg = background(strip, fw, h, 6)  # frame 7 vanilla: quasi tutto fondo

    icons = [draw(bg, g, fw) for g in GLYPHS]
    new = [base[y] + sum((icon[y] for icon in icons), []) for y in range(h)]
    nw = len(new[0])
    write_dds(STRIP, nw, h, new)

    prev = [sum((icon[y] for icon in icons), []) for y in range(h)]
    os.makedirs(os.path.join(ROOT, 'docs', 'images'), exist_ok=True)
    write_png(os.path.join(ROOT, 'docs', 'images', 'sheet_strategic_buildings.png'), len(prev[0]), h, prev, 2)
    print('strip: %d -> %d frame' % (frames, nw // fw))


if __name__ == '__main__':
    main()
