"""Costruisce i file di localizzazione tradotti a partire dall'inglese.

    python utility/efw_translations/build_translations.py

Sorgenti:
    localisation/english/*.yml                  testo di riferimento (prima occorrenza di ogni chiave)
    utility/efw_translations/<lingua>/*.tsv     traduzioni: una riga "chiave<TAB>testo" per voce

Per ogni file inglese efw_X_l_english.yml scrive localisation/<lingua>/efw_X_l_<lingua>.yml.
Le voci ripetitive degli edifici (velocità di costruzione, valori, icone) sono generate
dai modelli TEMPLATES qui sotto. Una chiave senza traduzione resta in inglese e viene
elencata a fine esecuzione. Lo script si ferma se una traduzione perde codici colore
(§Y ... §!), variabili ($VALUE$, [Root.GetName]), icone (£...) o a capo (\\n).

Nota: le leggi sono generate da utility/efw_laws/gen_laws.py solo in italiano e inglese.
Se si cambia laws_data.py, le traduzioni delle leggi vanno aggiornate a mano nei TSV.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ['russian', 'german', 'polish', 'simp_chinese']

TEMPLATES = {
    'russian': {
        'speed': 'Скорость строительства: {name}',
        'speed_desc': 'Изменяет скорость строительства: {name}.',
        'local': 'Местная скорость строительства: {name}',
        'local_desc': 'Изменяет местную скорость строительства: {name}.',
        'provides': 'Это здание даёт региону',
    },
    'german': {
        'speed': 'Baugeschwindigkeit: {name}',
        'speed_desc': 'Verändert die Baugeschwindigkeit von {name}.',
        'local': 'Lokale Baugeschwindigkeit: {name}',
        'local_desc': 'Verändert die lokale Baugeschwindigkeit von {name}.',
        'provides': 'Dieses Gebäude liefert dem Staat',
    },
    'polish': {
        'speed': 'Szybkość budowy: {name}',
        'speed_desc': 'Zmienia szybkość budowy: {name}.',
        'local': 'Lokalna szybkość budowy: {name}',
        'local_desc': 'Zmienia lokalną szybkość budowy: {name}.',
        'provides': 'Ten budynek zapewnia regionowi',
    },
    'simp_chinese': {
        'speed': '{name}建造速度',
        'speed_desc': '修改{name}的建造速度。',
        'local': '本地{name}建造速度',
        'local_desc': '修改本地{name}的建造速度。',
        'provides': '该建筑为本州提供',
    },
}

LINE = re.compile(r'^ ([A-Za-z0-9_.\-]+):(\d*) ?"(.*)"\s*$')
TOKENS = re.compile(r'§.|£[A-Za-z_|$]+|\$[A-Za-z_|=0-9]+\$|\[[^\]]+\]|\\n')


def english():
    files, seen = {}, set()
    for path in sorted(glob.glob(os.path.join(ROOT, 'localisation', 'english', '*.yml'))):
        name = os.path.basename(path).replace('_l_english.yml', '')
        items = []
        for line in open(path, encoding='utf-8-sig'):
            m = LINE.match(line)
            if m and m.group(1) not in seen:
                seen.add(m.group(1))
                items.append((m.group(1), m.group(3)))
        files[name] = items
    return files


def load_tsv(lang):
    out = {}
    for path in sorted(glob.glob(os.path.join(HERE, lang, '*.tsv'))):
        for n, line in enumerate(open(path, encoding='utf-8'), 1):
            line = line.rstrip('\n')
            if not line.strip() or line.startswith('#'):
                continue
            if '\t' not in line:
                sys.exit('%s:%d: manca il TAB' % (path, n))
            k, v = line.split('\t', 1)
            out[k.strip()] = v.strip()
    return out


def templated(key, en_all, tr, tpl):
    """Voci generate dai modelli; None se la chiave non è templata."""
    m = re.match(r'^modifier_(production_speed|state_production)_(efw_\w+?)_factor(_desc)?$', key)
    if m:
        name = tr.get(m.group(2), en_all.get(m.group(2), m.group(2)))
        kind = ('speed' if m.group(1) == 'production_speed' else 'local') + ('_desc' if m.group(3) else '')
        return tpl[kind].format(name=name)
    if key.endswith('_amount') or key.endswith('_resource'):
        return en_all[key]
    if en_all.get(key) == 'This building provides the state with':
        return tpl['provides']
    return None


def check(key, en, txt):
    a, b = sorted(TOKENS.findall(en)), sorted(TOKENS.findall(txt))
    if a != b:
        return '%s: token diversi\n   en %s\n   tr %s' % (key, a, b)
    if '"' in txt.replace('\\"', ''):
        return '%s: virgolette non escapate' % key
    return None


def main():
    files = english()
    en_all = {k: v for items in files.values() for k, v in items}
    problems = []
    for lang in (sys.argv[1:] or LANGS):
        tr = load_tsv(lang)
        tpl = TEMPLATES[lang]
        missing, extra = [], set(tr) - set(en_all)
        os.makedirs(os.path.join(ROOT, 'localisation', lang), exist_ok=True)
        for name, items in files.items():
            lines = ['l_%s:' % lang]
            for key, en in items:
                txt = templated(key, en_all, tr, tpl)
                if txt is None:
                    txt = tr.get(key)
                    if txt is None:
                        missing.append(key)
                        txt = en
                err = check(key, en, txt)
                if err:
                    problems.append('[%s] %s' % (lang, err))
                lines.append(' %s:0 "%s"' % (key, txt))
            path = os.path.join(ROOT, 'localisation', lang, '%s_l_%s.yml' % (name, lang))
            open(path, 'w', encoding='utf-8-sig').write('\n'.join(lines) + '\n')
        print('%-13s tradotte %d, mancanti %d, chiavi sconosciute %d' % (lang, len(en_all) - len(missing), len(missing), len(extra)))
        for k in missing[:15]:
            print('   manca', k)
        for k in sorted(extra)[:10]:
            print('   sconosciuta', k)
    if problems:
        print('\n'.join(problems))
        sys.exit(1)


if __name__ == '__main__':
    main()
