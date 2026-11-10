"""Crea l'icona del Furgone con Cannone EFW componendo due icone vanilla.

    python utility/efw_vehicle_icons/make_gun_truck_icon.py "D:/.../Hearts of Iron IV"

Cannone anticarro (AT_1_axis) rimpicciolito e montato sul cassone del
camion italiano (ITA_motorized_equipment_0), con una leggera patina di ruggine.
Scrive gfx/interface/equipment/efw_improvised/efw_gun_truck.dds (+ PNG di anteprima in docs/images).
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'utility', 'efw_laws'))
from dds_tool import read_dds, write_dds, write_png  # noqa: E402


def crop(px, x0, y0, x1, y1):
    return [row[x0:x1] for row in px[y0:y1]]


def downscale(px, k):
    """Riduzione con media a blocchi (k = fattore, es. 0.6)."""
    h, w = len(px), len(px[0])
    nw, nh = max(1, int(w * k)), max(1, int(h * k))
    out = []
    for y in range(nh):
        row = []
        for x in range(nw):
            xs = range(int(x / k), max(int(x / k) + 1, int((x + 1) / k)))
            ys = range(int(y / k), max(int(y / k) + 1, int((y + 1) / k)))
            acc = [0, 0, 0, 0]
            n = 0
            for sy in ys:
                for sx in xs:
                    if sy < h and sx < w:
                        r, g, b, a = px[sy][sx]
                        acc[0] += r * a
                        acc[1] += g * a
                        acc[2] += b * a
                        acc[3] += a
                        n += 1
            if acc[3]:
                row.append((acc[0] // acc[3], acc[1] // acc[3], acc[2] // acc[3], acc[3] // n))
            else:
                row.append((0, 0, 0, 0))
        out.append(row)
    return out


def paste(dst, src, ox, oy):
    for y, row in enumerate(src):
        for x, (r, g, b, a) in enumerate(row):
            dx, dy = ox + x, oy + y
            if a == 0 or not (0 <= dy < len(dst) and 0 <= dx < len(dst[0])):
                continue
            R, G, B, A = dst[dy][dx]
            t = a / 255
            dst[dy][dx] = (int(r * t + R * (1 - t)), int(g * t + G * (1 - t)),
                           int(b * t + B * (1 - t)), max(A, a))


def rust(px):
    """Leggera tinta ruggine/fango: è un mezzo improvvisato."""
    out = []
    for row in px:
        out.append([(min(255, int(r * 1.06 + 6)), int(g * 0.98), int(b * 0.88), a) for r, g, b, a in row])
    return out


def main():
    van = sys.argv[1]
    tech = os.path.join(van, 'gfx', 'interface', 'technologies')
    tw, th, truck = read_dds(os.path.join(tech, 'ITA_motorized_equipment_0.dds'))
    gw, gh, gun = read_dds(os.path.join(tech, 'AT_1_axis.dds'))

    # Cancella il numerale "I" in alto a sinistra, poi rimpicciolisce il cannone
    for y in range(0, 18):
        for x in range(18, 34):
            gun[y][x] = (0, 0, 0, 0)
    gun = downscale(crop(gun, 0, 0, gw, gh), 0.46)

    canvas = [list(r) for r in truck]
    # Ruota del cannone appoggiata sul cassone (y ~27), canna verso la cabina
    paste(canvas, gun, 28, 27 - len(gun) + 5)
    canvas = rust(canvas)

    out = os.path.join(ROOT, 'gfx', 'interface', 'equipment', 'efw_improvised', 'efw_gun_truck.dds')
    write_dds(out, tw, th, canvas)
    os.makedirs(os.path.join(ROOT, 'docs', 'images'), exist_ok=True)
    write_png(os.path.join(ROOT, 'docs', 'images', 'eq_gun_truck.png'), tw, th, canvas, 2)
    print('scritto', out, tw, 'x', th)


if __name__ == '__main__':
    main()
