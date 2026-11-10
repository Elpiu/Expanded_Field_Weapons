"""Crea l'icona del Trasporto in Legno EFW ricolorando l'icona vanilla del trasporto.

    python utility/efw_vehicle_icons/make_transport_icons.py "D:/.../Hearts of Iron IV"

Scrive in gfx/interface/equipment/efw_improvised/:
    efw_wooden_transport.dds   Trasporto in Legno
e le anteprime PNG in docs/images/.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'utility', 'efw_laws'))
sys.path.insert(0, os.path.join(ROOT, 'utility', 'efw_module_icons'))
from dds_tool import read_dds, write_dds, write_png  # noqa: E402
from make_module_icons import recolour, wear  # noqa: E402

BASE = 'gfx/interface/technologies/generic_transport_plane_equipment_1.dds'
ICONS = [
    ('efw_wooden_transport', ((70, 40, 18), (226, 178, 112)), 22, 101),
]


def main():
    van = sys.argv[1]
    w, h, px = read_dds(os.path.join(van, BASE))
    out_dir = os.path.join(ROOT, 'gfx', 'interface', 'equipment', 'efw_improvised')
    os.makedirs(os.path.join(ROOT, 'docs', 'images'), exist_ok=True)
    for name, (shadow, light), marks, seed in ICONS:
        img = wear(recolour(px, shadow, light), seed=seed, marks=marks)
        write_dds(os.path.join(out_dir, name + '.dds'), w, h, img)
        write_png(os.path.join(ROOT, 'docs', 'images', 'eq_%s.png' % name), w, h, img, 2)
        print(name, w, 'x', h)


if __name__ == '__main__':
    main()
