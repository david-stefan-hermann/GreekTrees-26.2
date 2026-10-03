"""Builds the concept art: one card per species, a size line-up and an overview sheet.

python make_sheet.py  ->  cards/NN_<key>.png, lineup.png, sheet.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

import species
import trees
import voxel

SPECIES = [
    dict(key='cypress', title='Zypresse', latin='Cupressus sempervirens', new=False,
         form='Nach deinen 32 Zypressen: Stamm 4, 3×3-Körper mit Leisten, Kreuz-Band, Kappe, Spitze.',
         where='Alleen, Tempelterrassen, Hänge, Friedhöfe'),
    dict(key='olive', title='Olivenbaum', latin='Olea europaea', new=False,
         form='Kurzer knorriger Stamm, gabelt sich mit Loch dazwischen, breite flache Krone.',
         where='Haine, Innenhöfe, Terrassenfelder'),
    dict(key='stone_pine', title='Schirmpinie', latin='Pinus pinea', new=True,
         form='Hoher kahler Stamm, leicht schief, oben ein flacher Schirm aus Nadeln.',
         where='Küste, Hügelkuppen, Silhouette über der Stadt'),
    dict(key='aleppo_pine', title='Aleppo-Kiefer', latin='Pinus halepensis', new=True,
         form='Schräger, geknickter Stamm, Krone in einzelne helle Wolken zerlegt.',
         where='Küstenwald, Felsen, schräg über Klippen'),
    dict(key='plane', title='Morgenländische Platane', latin='Platanus orientalis', new=True,
         form='Riese vom Dorfplatz: 2×2-Stamm mit Wurzelanlauf, gefleckte Rinde, breite Schattenkrone.',
         where='Dorfplatz (Platia), Quellen, Bachläufe'),
    dict(key='fig', title='Feigenbaum', latin='Ficus carica', new=True,
         form='Niedrig und breiter als hoch, mehrere graue Stämme direkt aus dem Boden.',
         where='Gärten, Hofecken, an Mauern'),
    dict(key='almond', title='Mandelbaum (Blüte)', latin='Prunus dulcis', new=True,
         form='Kleine Vasenform, luftige Krone in Rosa, Blütenblätter am Boden.',
         where='Obstgärten, Frühlingsakzent zwischen Oliven'),
    dict(key='oleander', title='Oleander', latin='Nerium oleander', new=True,
         form='Mehrstämmiger Strauchbaum, dicht, rosa Blüten.',
         where='Wegränder, Flussbetten, Gärten, Hafenpromenade'),
    dict(key='strawberry_tree', title='Erdbeerbaum (Andrachne)', latin='Arbutus andrachne', new=True,
         form='Dünne glatte orangerote Stämme, gespreizt wie Akazienäste, offene dunkle Krone.',
         where='Macchia, Felshänge, Klosterhöfe'),
    dict(key='date_palm', title='Kretische Dattelpalme', latin='Phoenix theophrasti', new=True,
         form='Horst aus 2–3 gebogenen Stämmen, hängende Wedel, Kakao als Datteln.',
         where='Strände (Palmenwald von Vai), Hafen'),
    dict(key='carob', title='Johannisbrotbaum', latin='Ceratonia siliqua', new=True,
         form='Kurzer dunkler Stamm, sehr dichte dunkle Kuppel fast bis zum Boden.',
         where='Trockene Hänge, Gehöfte, Schattenplatz'),
]
SEEDS = (1, 2, 3)

FONTS = 'C:/Windows/Fonts/'
F_TITLE = ImageFont.truetype(FONTS + 'segoeuib.ttf', 34)
F_LATIN = ImageFont.truetype(FONTS + 'segoeuii.ttf', 20)
F_BADGE = ImageFont.truetype(FONTS + 'segoeuib.ttf', 16)
F_LABEL = ImageFont.truetype(FONTS + 'segoeuib.ttf', 17)
F_TEXT = ImageFont.truetype(FONTS + 'segoeui.ttf', 17)
F_MONO = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
F_SMALL = ImageFont.truetype(FONTS + 'segoeui.ttf', 14)

PAPER = (245, 241, 232, 255)
INK = (29, 53, 87, 255)
BLUE = (13, 94, 175, 255)
GREY = (120, 128, 140, 255)
SKY_TOP, SKY_BOTTOM = (156, 195, 230), (219, 233, 244)

CARD_W = 1000
ISO_H = 600
SIDE_H = 270
SIDE_S = 10


def gen(key):
    return getattr(species if key in species.PICKED else trees, key)


def sky(w, h):
    img = Image.new('RGBA', (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(SKY_TOP, SKY_BOTTOM)) + (255,))
    return img


def build(key, seed):
    t = gen(key)(seed).finish()
    x0, x1, z0, z1, top = t.extent()
    sx = x1 + 2
    for gx in range(sx - 1, sx + 2):
        for gz in (-1, 0, 1):
            t.v.setdefault((gx, -1, gz), ('grass_block', 'y'))
    return t, (sx, 0), (x1 - x0 + 1, z1 - z0 + 1, top + 1)


def fit(img, w, h):
    if img.width <= w and img.height <= h:
        return img
    f = min(w / img.width, h / img.height)
    return img.resize((int(img.width * f), int(img.height * f)), Image.LANCZOS)


def block_icon(block):
    return voxel.render({(0, 0, 0): (block, 'y')}, margin=2)


def card(sp, index):
    built = [build(sp['key'], s) for s in SEEDS]
    blocks = []
    for t, _, _ in built:
        for (x, y, z), (b, _) in t.v.items():
            if y >= 0 and b not in blocks:
                blocks.append(b)
    order = {'log': 0, 'wood': 1, 'leaves': 2}
    blocks.sort(key=lambda b: (order.get(b.rsplit('_', 1)[-1], 3), b))

    info_h = 210
    h = 100 + ISO_H + SIDE_H + info_h
    img = Image.new('RGBA', (CARD_W, h), PAPER)
    d = ImageDraw.Draw(img)

    # header
    d.text((28, 16), f'{index:02d}  {sp["title"]}', font=F_TITLE, fill=INK)
    d.text((70, 62), sp['latin'], font=F_LATIN, fill=GREY)
    badge = 'NEU' if sp['new'] else 'VORHANDEN'
    bw = d.textlength(badge, font=F_BADGE) + 28
    d.rounded_rectangle([CARD_W - 28 - bw, 26, CARD_W - 28, 58], radius=16,
                        fill=BLUE if sp['new'] else (150, 160, 172, 255))
    d.text((CARD_W - 28 - bw + 14, 31), badge, font=F_BADGE, fill=(255, 255, 255, 255))

    # main iso view, native scale so all cards compare
    t, steve, _ = built[0]
    iso = fit(voxel.render(t.v, steve=steve), CARD_W - 40, ISO_H - 20)
    panel = sky(CARD_W - 40, ISO_H)
    panel.alpha_composite(iso, ((panel.width - iso.width) // 2, panel.height - iso.height - 10))
    img.alpha_composite(panel, (20, 100))

    # side views of three seeds
    y0 = 100 + ISO_H + 10
    d.text((28, y0), 'Varianten · Seitenansicht auf Augenhöhe', font=F_LABEL, fill=INK)
    sides = []
    for t, steve, _ in built:
        sv = voxel.render_side(t.v, s=SIDE_S, steve=steve, margin=8)
        sides.append(fit(sv, (CARD_W - 80) // 3, SIDE_H - 50))
    strip = sky(CARD_W - 40, SIDE_H - 40)
    slot = strip.width // 3
    for i, sv in enumerate(sides):
        strip.alpha_composite(sv, (i * slot + (slot - sv.width) // 2, strip.height - sv.height - 4))
    img.alpha_composite(strip, (20, y0 + 30))

    # info
    y = 100 + ISO_H + SIDE_H + 12
    d.text((28, y), 'Form', font=F_LABEL, fill=INK)
    d.text((140, y), sp['form'], font=F_TEXT, fill=INK)
    y += 30
    ws = [s[0] for s in (b[2] for b in built)]
    ds = [s[1] for s in (b[2] for b in built)]
    hs = [s[2] for s in (b[2] for b in built)]
    rng = lambda v: f'{min(v)}' if min(v) == max(v) else f'{min(v)}–{max(v)}'
    d.text((28, y), 'Größe', font=F_LABEL, fill=INK)
    d.text((140, y), f'Höhe {rng(hs)} Blöcke · Breite {rng(ws + ds)} Blöcke', font=F_TEXT, fill=INK)
    y += 30
    d.text((28, y), 'Passt zu', font=F_LABEL, fill=INK)
    d.text((140, y), sp['where'], font=F_TEXT, fill=INK)
    y += 36
    d.text((28, y + 8), 'Blöcke', font=F_LABEL, fill=INK)
    x = 140
    for b in blocks:
        icon = block_icon(b)
        label = b
        lw = d.textlength(label, font=F_MONO)
        if x + icon.width + lw + 24 > CARD_W - 20:
            y += 44
            x = 140
        img.alpha_composite(icon, (x, y))
        d.text((x + icon.width + 4, y + 12), label, font=F_MONO, fill=INK)
        x += int(icon.width + lw + 22)
    return img.crop((0, 0, CARD_W, min(h, y + 56)))


def lineup():
    """All species next to each other, side view, same scale, one player for reference."""
    s = 12
    views = []
    for i, sp in enumerate(SPECIES, 1):
        t = gen(sp['key'])(1).finish()
        views.append((i, sp, voxel.render_side(t.v, s=s, margin=10)))
    gap = 24
    steve_w = 40
    w = sum(v.width for _, _, v in views) + gap * (len(views) + 1) + steve_w
    top = max(v.height for _, _, v in views)
    h = top + 120
    img = sky(w, h)
    d = ImageDraw.Draw(img)
    d.text((gap, 14), 'Griechische Bäume · Größenvergleich (Seitenansicht, gleicher Maßstab)', font=F_TITLE, fill=INK)
    ground = 70 + top
    x = gap
    # player for scale, standing on the same ground line
    sv = voxel.render_side({(0, -1, 0): ('grass_block', 'y')}, s=s, steve=(0, 1), margin=10)
    img.alpha_composite(sv, (x, ground - sv.height))
    x += steve_w + gap
    for i, sp, v in views:
        img.alpha_composite(v, (x, ground - v.height))
        label = f'{i:02d} {sp["title"].split(" (")[0]}'
        lw = d.textlength(label, font=F_SMALL)
        d.text((x + (v.width - lw) / 2, ground + 8), label, font=F_SMALL, fill=INK)
        x += v.width + gap
    return img


def main():
    os.makedirs('cards', exist_ok=True)
    cards = []
    for i, sp in enumerate(SPECIES, 1):
        c = card(sp, i)
        c.save(f'cards/{i:02d}_{sp["key"]}.png')
        cards.append(c)
        print('card', i, sp['key'], c.size)
    lu = lineup()
    lu.save('lineup.png')
    print('lineup', lu.size)

    cols = 3
    scale = 0.5
    cw = int(CARD_W * scale)
    rows = (len(cards) + cols - 1) // cols
    row_h = [max(int(c.height * scale) for c in cards[r * cols:(r + 1) * cols]) for r in range(rows)]
    pad = 12
    sheet = Image.new('RGBA', (cols * (cw + pad) + pad, sum(row_h) + pad * (rows + 1)), (222, 214, 198, 255))
    y = pad
    for r in range(rows):
        for c_i, c in enumerate(cards[r * cols:(r + 1) * cols]):
            small = c.resize((cw, int(c.height * scale)), Image.LANCZOS)
            sheet.alpha_composite(small, (pad + c_i * (cw + pad), y))
        y += row_h[r] + pad
    sheet.save('sheet.png')
    print('sheet', sheet.size)


if __name__ == '__main__':
    main()
