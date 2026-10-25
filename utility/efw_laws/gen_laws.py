"""Generate EFW politics-panel law categories from laws_data.py.

usage: gen_laws.py <mod_dir> <blp_dir> <vanilla_dir>
"""
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from laws_data import CATEGORIES, PICS
from dds_tool import read_dds, write_dds
from blobs import find_blobs

mod, blp, van = (Path(a) for a in sys.argv[1:4])
errors = []
SLOT_COSTS = [50] * 5 + [100] * 3

# ---------------------------------------------------------------- validation
doc = (van / 'documentation/modifiers_documentation.md').read_text(encoding='utf-8', errors='ignore')
known = set(re.findall(r'^## ([a-z_0-9]+)', doc, re.M))
ids, used_pics = set(), set()
for cat in CATEGORIES:
    # The politics panel shows at most 6 slots per row: a 7th falls outside it.
    if len(cat['slots']) > 6:
        errors.append(f"{cat['id']}: {len(cat['slots'])} slots, the panel only shows 6")
    for slot in cat['slots']:
        # Every slot: 5 laws at 50 PP followed by 3 slightly stronger laws at 100 PP.
        costs = [law[1] for law in slot['laws']]
        if costs != SLOT_COSTS:
            errors.append(f"{slot['id']}: costs {costs}, expected {SLOT_COSTS}")
        for law in slot['laws']:
            lid, cost, pic, mods = law[0], law[1], law[2], law[3]
            if len(mods) < 2:
                errors.append(f'{lid}: needs at least a bonus and a malus')
            if lid in ids:
                errors.append('duplicate id ' + lid)
            ids.add(lid)
            if pic not in PICS:
                errors.append(f'{lid}: unknown picture {pic}')
            used_pics.add(pic)
            for m in mods:
                if m not in known and not re.fullmatch(r'production_speed_[a-z_]+_factor', m):
                    errors.append(f'{lid}: unknown modifier {m}')
for pic in used_pics:
    if not (blp / 'gfx/interface/ideas' / PICS[pic]).exists():
        errors.append('missing BLP texture ' + PICS[pic])
if errors:
    print('\n'.join(errors))
    sys.exit(1)


# ---------------------------------------------------------------- helpers
def fmt(v):
    return str(v) if isinstance(v, int) else ('%.3f' % v).rstrip('0').rstrip('.')


def write_text(path, text, bom=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((b'\xef\xbb\xbf' if bom else b'') + text.replace('\r\n', '\n').encode('utf-8'))


HEADER = ('# Generated from laws_data.py - EFW politics-panel laws.\n'
          '# Concepts and icons adapted from Better Laws and Policies (Workshop 3097661966).\n')

# ---------------------------------------------------------------- idea_tags
out = [HEADER, 'idea_categories = {\n']
for cat in CATEGORIES:
    out.append(f"\n    {cat['id']} = {{\n")
    for slot in cat['slots']:
        out.append(f"        slot = {slot['id']}\n")
    out.append('\n        ledger = civilian\n\n        cost = 100\n        removal_cost = -1\n    }\n')
out.append('}\n')
write_text(mod / 'common/idea_tags/efw_policy_categories.txt', ''.join(out))

# ---------------------------------------------------------------- ideas
out = [HEADER, '# No default law: slots start empty and only the player fills them (ai_will_do = 0).\n'
       '# Each slot: 5 laws at 50 PP, then 3 slightly stronger laws at 100 PP.\n\nideas = {\n']
for cat in CATEGORIES:
    out.append(f"\n    # {'=' * 70}\n    # {cat['it'][0].upper()}\n    # {'=' * 70}\n")
    for slot in cat['slots']:
        out.append(f"\n    {slot['id']} = {{\n        law = yes\n        use_list_view = yes\n")
        for lid, cost, pic, mods, avail, *_rest in slot['laws']:
            out.append(f'\n        {lid} = {{\n')
            if avail:
                out.append(f'            available = {{\n                {avail}\n            }}\n\n')
            out.append(f'            cost = {cost}\n            removal_cost = -1\n')
            out.append(f'            picture = efw_law_{pic}\n')
            if mods:
                out.append('\n            modifier = {\n')
                for k, v in mods.items():
                    out.append(f'                {k} = {fmt(v)}\n')
                out.append('            }\n')
            out.append('\n            cancel_if_invalid = no\n')
            out.append('            ai_will_do = { factor = 0 }\n        }\n')
        out.append('    }\n')
out.append('}\n')
write_text(mod / 'common/ideas/efw_policy_laws.txt', ''.join(out))

# ---------------------------------------------------------------- law + slot icons
pic_dir = mod / 'gfx/interface/ideas/efw_laws'
slot_dir = mod / 'gfx/interface/efw_idea_slots'
if pic_dir.exists():
    shutil.rmtree(pic_dir)
pic_dir.mkdir(parents=True)
slot_dir.mkdir(parents=True, exist_ok=True)
out = [HEADER, 'spriteTypes = {\n']
for pic in sorted(used_pics):
    shutil.copyfile(blp / 'gfx/interface/ideas' / PICS[pic], pic_dir / f'efw_law_{pic}.dds')
    out.append(f'\n    spriteType = {{\n        name = "GFX_idea_efw_law_{pic}"\n'
               f'        texturefile = "gfx/interface/ideas/efw_laws/efw_law_{pic}.dds"\n    }}\n')
for cat in CATEGORIES:
    shutil.copyfile(blp / 'gfx/interface' / cat['slot_icon'], slot_dir / cat['slot_icon'].lower())
    for slot in cat['slots']:
        out.append(f'\n    spriteType = {{\n        name = "GFX_idea_slot_{slot["id"]}"\n'
                   f'        texturefile = "gfx/interface/efw_idea_slots/{cat["slot_icon"].lower()}"\n    }}\n')
out.append('}\n')
write_text(mod / 'interface/efw_policy_laws.gfx', ''.join(out))

# ---------------------------------------------------------------- category header icons
# Frame N of GFX_idea_categories belongs to the N-th idea category (vanilla defines 14,
# so EFW categories start at frame 15). Frames 1-6 are vanilla, 7-14 repeat the helmet.
FW, NFRAMES = 48, 20
vw, vh, vpx = read_dds(str(van / 'gfx/interface/idea_categories.dds'))
assert (vw, vh) == (6 * FW, 33), (vw, vh)
bw, bh, bpx = read_dds(str(blp / 'gfx/interface/idea_categories.dds'))
blobs = find_blobs(bpx, bw, bh)
strip = [[(0, 0, 0, 0)] * (FW * NFRAMES) for _ in range(vh)]


def put_frame(dst, src_px, x0, x1):
    w = x1 - x0 + 1
    ox = dst * FW + (FW - w) // 2
    for y in range(vh):
        for x in range(w):
            strip[y][ox + x] = src_px[y][x0 + x]


for f in range(6):
    for y in range(vh):
        strip[y][f * FW:(f + 1) * FW] = vpx[y][f * FW:(f + 1) * FW]
for f in range(6, 14):
    for y in range(vh):
        strip[y][f * FW:(f + 1) * FW] = vpx[y][4 * FW:5 * FW]
for i, cat in enumerate(CATEGORIES):
    a, b = blobs[cat['blp_blob']]
    assert b - a + 1 <= FW
    put_frame(14 + i, bpx, a, b)
(mod / 'gfx/interface').mkdir(parents=True, exist_ok=True)
write_dds(str(mod / 'gfx/interface/efw_idea_categories.dds'), FW * NFRAMES, vh, strip)
write_text(mod / 'interface/zzz_efw_idea_categories.gfx',
           '# Overrides vanilla GFX_idea_categories (countrypoliticsview.gfx) with 20 frames:\n'
           f'# frames 15-{14 + len(CATEGORIES)} are the EFW policy categories. zzz_ so it loads after vanilla.\n'
           'spriteTypes = {\n    spriteType = {\n        name = "GFX_idea_categories"\n'
           '        texturefile = "gfx/interface/efw_idea_categories.dds"\n'
           f'        noOfFrames = {NFRAMES}\n    }}\n}}\n')

# ---------------------------------------------------------------- localisation
for lang, key, folder in (('it', 'l_italian', 'italian'), ('en', 'l_english', 'english')):
    lines = [f'{key}:\n', ' # Generated from laws_data.py - EFW politics-panel laws.\n']
    for cat in CATEGORIES:
        name, desc = cat[lang]
        lines.append(f"\n # === {name} ===\n")
        lines.append(f' {cat["id"]}:0 "{name}"\n {cat["id"]}_desc:0 "{desc}"\n')
        for slot in cat['slots']:
            lines.append(f' {slot["id"]}:0 "{slot[lang]}"\n')
            for lid, _c, _p, _m, _a, it_n, it_d, en_n, en_d in slot['laws']:
                n, d = (it_n, it_d) if lang == 'it' else (en_n, en_d)
                lines.append(f' {lid}:0 "{n}"\n {lid}_desc:0 "{d}"\n')
    write_text(mod / f'localisation/{folder}/efw_laws_l_{folder}.yml', ''.join(lines), bom=True)

n_laws = sum(len(s['laws']) for c in CATEGORIES for s in c['slots'])
print(f'ok: {len(CATEGORIES)} categories, {sum(len(c["slots"]) for c in CATEGORIES)} slots, '
      f'{n_laws} laws, {len(used_pics)} law icons')
