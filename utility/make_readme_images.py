"""Converte le icone DDS della mod in PNG per il README (docs/images/).

Uso (dalla root della mod):
    python utility/make_readme_images.py

Non serve Pillow: usa il lettore DDS di utility/efw_laws/dds_tool.py.
Il gioco ignora la cartella docs/, quindi i PNG non vengono caricati da HOI4.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'utility', 'efw_laws'))
from dds_tool import read_dds, write_png  # noqa: E402

OUT = os.path.join(ROOT, 'docs', 'images')
GFX = os.path.join(ROOT, 'gfx', 'interface')

EMPTY = (0, 0, 0, 0)


def load(rel):
    return read_dds(os.path.join(GFX, rel))


def crop(img, x0, y0, x1, y1):
    w, h, px = img
    return x1 - x0, y1 - y0, [row[x0:x1] for row in px[y0:y1]]


def scale(img, k):
    w, h, px = img
    out = []
    for row in px:
        big = [p for p in row for _ in range(k)]
        out += [list(big) for _ in range(k)]
    return w * k, h * k, out


def sheet(imgs, pad=10):
    """Affianca le immagini su sfondo trasparente, centrate in verticale."""
    h = max(i[1] for i in imgs) + pad * 2
    w = sum(i[0] for i in imgs) + pad * (len(imgs) + 1)
    px = [[EMPTY] * w for _ in range(h)]
    x = pad
    for iw, ih, ipx in imgs:
        y0 = (h - ih) // 2
        for y in range(ih):
            px[y0 + y][x:x + iw] = ipx[y]
        x += iw + pad
    return w, h, px


def save(name, img):
    os.makedirs(OUT, exist_ok=True)
    w, h, px = img
    write_png(os.path.join(OUT, name), w, h, px)
    print('docs/images/' + name, w, 'x', h)


def main():
    # Equipaggiamenti singoli
    singles = {
        'eq_machinegun.png': 'equipment/efw/efw_machinegun.dds',
        'eq_antitank.png': 'equipment/efw/efw_hmg.dds',  # il file si chiama hmg ma è l'icona anticarro
        'eq_mortar.png': 'equipment/efw/efw_mortar.dds',
        'eq_pipe_gun_rifle.png': 'equipment/efw/efw_pipe_gun_rifle.dds',
        'eq_wooden_plane.png': 'equipment/efw_improvised/efw_wooden_plane.dds',
        'eq_motorboat.png': 'equipment/efw_naval/efw_motorboat.dds',
        'eq_midget_sub.png': 'equipment/efw_naval/efw_midget_sub.dds',
        'eq_tankette.png': 'equipment/efw_improvised/efw_tin_tank.dds',
    }
    for name, rel in singles.items():
        save(name, load(rel))

    # Armi da campo affiancate
    save('sheet_field_weapons.png', sheet([
        load('equipment/efw/efw_pipe_gun_rifle.dds'),
        load('equipment/efw/efw_machinegun.dds'),
        load('equipment/efw/efw_hmg.dds'),
        load('equipment/efw/efw_mortar.dds'),
    ]))

    # Moduli improvvisati del designer (piccoli: x2)
    mods = ['efw_wooden_boost_airframe', 'efw_improvised_drop_tank', 'efw_multirole_combat_rack',
            'efw_cast_iron_stove_armor', 'efw_bazooka_charlie_tubes']
    save('sheet_air_modules.png', scale(sheet(
        [load('equipmentdesigner/efw_modules/%s.dds' % m) for m in mods], pad=6), 2))
    mods = ['efw_improvised_fuel_tank', 'efw_careened_hull', 'efw_small_sail', 'efw_large_sail']
    save('sheet_naval_modules.png', scale(sheet(
        [load('equipmentdesigner/efw_modules/%s.dds' % m) for m in mods], pad=6), 2))

    # Idee delle decisioni nazionali
    pols = ['industrial_phase', 'grand_works', 'autarky_fuel', 'social_pact',
            'coordinated_economy', 'national_mobilization']
    save('sheet_policies.png', sheet(
        [load('ideas/efw_policies/efw_pol_%s.dds' % p) for p in pols]))

    # Edifici EFW: ultimi 9 frame della strip (40 frame da 46 px)
    strip = load('buildings/building_icon_strip.dds')
    fw = strip[0] // 40
    frames = [crop(strip, i * fw, 0, (i + 1) * fw, strip[1]) for i in range(31, 40)]
    save('sheet_buildings.png', scale(sheet(frames, pad=4), 2))

    # Un assaggio delle icone delle leggi
    laws_dir = os.path.join(GFX, 'ideas', 'efw_laws')
    laws = sorted(f for f in os.listdir(laws_dir) if f.endswith('.dds'))
    pick = laws[::max(1, len(laws) // 12)][:12]
    save('sheet_laws.png', sheet([load('ideas/efw_laws/' + f) for f in pick], pad=6))

    # Icone delle unità (divisions_large)
    units = ['efw_machinegun_company', 'efw_hmg_company', 'efw_mortar_company', 'efw_elite_company']
    save('sheet_unit_counters.png', scale(sheet(
        [load('counters/divisions_large/%s.dds' % u) for u in units], pad=6), 2))


if __name__ == '__main__':
    main()
