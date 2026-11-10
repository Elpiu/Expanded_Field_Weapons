"""Compone la copertina della mod (thumbnail.png) sopra un'illustrazione.

    uv run python utility/efw_thumbnail/make_thumbnail.py [illustrazione] [uscita]

Default: thumbnail_new.jpg -> thumbnail.png. Dipendenze: uv sync (Pillow).
Usa font di Windows (Impact, Bahnschrift, Microsoft YaHei per il cinese).
Per una nuova versione basta cambiare VERSION, FEATURES e LANGS qui sotto.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTS = 'C:/Windows/Fonts/'

VERSION = 'v1.3.0'
SUBTITLE = 'HEARTS OF IRON IV  ·  1.19'
# (etichetta in oro, dettaglio in bianco)
FEATURES = [
    ('NEW PRODUCTION', 'machine guns, mortars, AT weapons, Pipe-Gun, STEN'),
    ('NEW VEHICLES', 'tankettes, gun trucks, MG motorcycles'),
    ('NEW IDEAS', '192 laws, 21 designers, National Vocations'),
    ('NEW CONSTRUCTIONS', 'resource plants, research & propaganda centers'),
    ('NEW UPGRADE MODULES', 'air & naval: plywood, sails, stove armor'),
    ('EARLY PARADROPS', 'wooden transports from day one'),
    ('FPS BOOST', 'smoother late game, built in'),
]
LANGS = ['EN', 'RU', 'DE', 'PL', '中文', 'IT']
SLOGAN = "When you can't afford the best, build the rest."

OUT_W = 1024          # larghezza finale (16:9 circa). Steam e launcher la ridimensionano.
MAX_BYTES = 1_000_000  # limite del Workshop per l'anteprima

INK = (246, 236, 214)        # bianco carta
GOLD = (236, 190, 96)
SHADOW = (24, 18, 10)


def font(name, size, index=0):
    return ImageFont.truetype(FONTS + name, size, index=index)


def text_shadow(draw, xy, text, fnt, fill, offset=3, blur_layer=None):
    x, y = xy
    if blur_layer is not None:
        blur_layer.text((x + offset, y + offset), text, font=fnt, fill=SHADOW + (210,))
    draw.text((x, y), text, font=fnt, fill=fill, stroke_width=2, stroke_fill=SHADOW)


def rounded_panel(size, box, radius, fill):
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(box, radius=radius, fill=fill)
    return layer


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'thumbnail_new.jpg')
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'thumbnail.png')
    base = Image.open(src).convert('RGBA')
    W, H = base.size
    k = W / 1376.0  # le misure sotto sono pensate per un'immagine larga 1376 px

    def s(v):
        return int(round(v * k))

    # 1) velature scure per la leggibilità: angolo in alto a sinistra e striscia in basso
    shade = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for i in range(s(780)):
        a = int(165 * (1 - i / s(780)) ** 1.5)
        sd.line([(i, 0), (i, s(560))], fill=(20, 14, 6, a))
    shade = shade.filter(ImageFilter.GaussianBlur(s(40)))
    base = Image.alpha_composite(base, shade)
    bar_h = s(62)
    base = Image.alpha_composite(base, rounded_panel((W, H), (0, H - bar_h, W, H), 0, (18, 13, 6, 200)))

    # 2) testi (con un livello d'ombra sfocata separato)
    shadow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sl = ImageDraw.Draw(shadow_layer)
    txt = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt)

    f_title = font('impact.ttf', s(92))
    f_sub = font('bahnschrift.ttf', s(26))
    f_feat = font('bahnschrift.ttf', s(25))
    f_ver = font('impact.ttf', s(34))
    f_lang = font('msyhbd.ttc', s(26))
    f_small = font('bahnschrift.ttf', s(22))

    x0, y0 = s(44), s(30)
    text_shadow(td, (x0, y0), 'EXPANDED', f_title, INK, s(4), sl)
    text_shadow(td, (x0, y0 + s(84)), 'FIELD WEAPONS', f_title, GOLD, s(4), sl)

    # badge versione accanto a "EXPANDED"
    tw = td.textlength('EXPANDED', font=f_title)
    bx, by = x0 + tw + s(22), y0 + s(26)
    vw = td.textlength(VERSION, font=f_ver)
    td.rounded_rectangle((bx, by, bx + vw + s(26), by + s(48)), radius=s(10), fill=(150, 40, 28, 235),
                         outline=INK, width=max(1, s(2)))
    td.text((bx + s(13), by + s(2)), VERSION, font=f_ver, fill=INK)

    text_shadow(td, (x0 + s(4), y0 + s(186)), SUBTITLE, f_sub, INK, s(2), sl)

    # elenco funzionalità: etichetta "NEW ..." in oro + dettaglio in bianco
    f_label = font('impact.ttf', s(27))
    fy = y0 + s(232)
    for label, detail in FEATURES:
        cx, cy, r = x0 + s(12), fy + s(17), s(7)
        td.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=GOLD, outline=SHADOW)
        lx0 = x0 + s(28)
        text_shadow(td, (lx0, fy), label, f_label, GOLD, s(2), sl)
        dx = lx0 + td.textlength(label, font=f_label) + s(12)
        text_shadow(td, (dx, fy + s(3)), detail, f_feat, INK, s(2), sl)
        fy += s(38)

    # striscia in basso: lingue a sinistra, nota a destra
    ly = H - bar_h + (bar_h - s(34)) // 2
    lx = x0
    td.text((lx, ly + s(4)), 'LANGUAGES', font=f_small, fill=GOLD)
    lx += td.textlength('LANGUAGES', font=f_small) + s(18)
    for code in LANGS:
        cw = td.textlength(code, font=f_lang)
        td.rounded_rectangle((lx, ly, lx + cw + s(20), ly + s(36)), radius=s(7), fill=(70, 58, 34, 230),
                             outline=GOLD, width=max(1, s(1)))
        td.text((lx + s(10), ly - s(1)), code, font=f_lang, fill=INK)
        lx += cw + s(30)
    f_slogan = font('impact.ttf', s(27))
    nw = td.textlength(SLOGAN, font=f_slogan)
    td.text((W - nw - s(30), ly + s(1)), SLOGAN, font=f_slogan, fill=GOLD)

    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(s(3)))
    out = Image.alpha_composite(Image.alpha_composite(base, shadow_layer), txt).convert('RGB')

    # 3) esportazione: PNG sotto 1 MB (se serve, riduce la palette)
    h = int(round(H * OUT_W / W))
    out = out.resize((OUT_W, h), Image.LANCZOS)
    out.save(dst, optimize=True)
    if os.path.getsize(dst) > MAX_BYTES:
        out.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(dst, optimize=True)
    print(dst, out.size, os.path.getsize(dst), 'byte')


if __name__ == '__main__':
    main()
