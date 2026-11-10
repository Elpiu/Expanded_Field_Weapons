"""Crea una copia pulita della mod da pubblicare sul Workshop.

    uv run python utility/build_release.py                 # crea/aggiorna la cartella release
    uv run python utility/build_release.py --point-launcher

Il launcher di Paradox carica TUTTO il contenuto della cartella della mod
(.git, .venv, utility, docs...). Questo script copia solo i file che servono
al gioco in una cartella separata, accanto a quella di sviluppo:

    Documents/Paradox Interactive/Hearts of Iron IV/mod/Expanded_Field_Weapons_release/

--point-launcher fa puntare Expanded_Field_Weapons.mod (il file che legge il launcher)
alla cartella release, con un backup .bak. Da quel momento gioco e caricamento usano
la copia pulita: dopo ogni modifica rilanciare lo script prima di provare in gioco.
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD_DIR = os.path.dirname(ROOT)
RELEASE = os.path.join(MOD_DIR, os.path.basename(ROOT) + '_release')
LAUNCHER_MOD = os.path.join(MOD_DIR, os.path.basename(ROOT) + '.mod')
MARKER = '.efw_release'

# Solo queste cartelle e questi file finiscono nella mod pubblicata.
GAME_DIRS = ['common', 'events', 'gfx', 'history', 'interface', 'localisation',
             'map', 'music', 'portraits', 'sound']
GAME_FILES = ['descriptor.mod', 'thumbnail.png']
SKIP_EXT = {'.pyc', '.bak', '.tmp', '.psd', '.xcf'}


def copy_tree(src, dst):
    count = size = 0
    for base, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for name in files:
            if name.startswith('.') or os.path.splitext(name)[1].lower() in SKIP_EXT:
                continue
            s = os.path.join(base, name)
            d = os.path.join(dst, os.path.relpath(s, src))
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
            count += 1
            size += os.path.getsize(s)
    return count, size


def build():
    # Cancella solo una cartella creata da questo script (contiene il marker).
    if os.path.isdir(RELEASE):
        if not os.path.exists(os.path.join(RELEASE, MARKER)):
            sys.exit('La cartella %s esiste ma non e una release EFW: non la tocco.' % RELEASE)
        shutil.rmtree(RELEASE)
    os.makedirs(RELEASE)
    open(os.path.join(RELEASE, MARKER), 'w').write('Cartella generata da utility/build_release.py\n')

    total_n = total_b = 0
    for d in GAME_DIRS:
        src = os.path.join(ROOT, d)
        if os.path.isdir(src):
            n, b = copy_tree(src, os.path.join(RELEASE, d))
            total_n += n
            total_b += b
    for f in GAME_FILES:
        src = os.path.join(ROOT, f)
        if not os.path.exists(src):
            sys.exit('Manca %s' % f)
        shutil.copy2(src, os.path.join(RELEASE, f))
        total_n += 1
        total_b += os.path.getsize(src)
    print('Release: %s\n  %d file, %.1f MB' % (RELEASE, total_n, total_b / 1e6))


def point_launcher():
    if not os.path.exists(LAUNCHER_MOD):
        sys.exit('Non trovo %s' % LAUNCHER_MOD)
    text = open(LAUNCHER_MOD, encoding='utf-8').read()
    new_path = RELEASE.replace('\\', '/')
    if 'path="%s"' % new_path in text:
        print('Il launcher punta gia alla release.')
        return
    shutil.copy2(LAUNCHER_MOD, LAUNCHER_MOD + '.bak')
    text = re.sub(r'path="[^"]*"', 'path="%s"' % new_path, text)
    open(LAUNCHER_MOD, 'w', encoding='utf-8').write(text)
    print('%s ora punta a %s (backup: .mod.bak)' % (os.path.basename(LAUNCHER_MOD), new_path))


if __name__ == '__main__':
    build()
    if '--point-launcher' in sys.argv:
        point_launcher()
