"""Concept art of round 3 (2026-10-02): mulberry and weeping willow.

cd concept && python make_round3.py  ->  cards/12_mulberry.png, cards/13_weeping_willow.png, round3_materials.png,
                                          round3_lineup.png
The line-up puts the new trees next to the ones the mod grew in the last self-test (run/greektrees-selftest/), so
run that first for an up-to-date comparison.
"""
import os
import sys

from PIL import Image, ImageDraw

import make_sheet
import round3
import voxel
from make_sheet import F_LABEL, F_SMALL, F_TEXT, F_TITLE, GREY, INK, PAPER, sky
from render_selftest import TITLES, load

sys.path.insert(0, os.path.join('..', 'tools'))
from make_textures import draw  # noqa: E402

NEW = [
    dict(key='mulberry', title='Maulbeerbaum', latin='Morus alba / Morus nigra', new=True, seeds=(2, 1, 6),
         form='Kurzer dicker Stamm, gabelt tief, dichte runde Kuppel; jeder dritte ein Kopfbaum mit Knubbel-Faust.',
         where='Dorfplatz (Schatten), Seidenhöfe, Brunnen; Früchte: Maulbeeren weiß → rot → schwarz'),
    dict(key='weeping_willow', title='Trauerweide', latin='Salix babylonica', new=True, seeds=(1, 3, 6),
         form='Schiefer kurzer Stamm, Äste steigen und biegen sich nach außen-unten, Laubvorhang bis fast zum Boden.',
         where='Quellen, Bachläufe, Dorfbrunnen, Teiche'),
]
MATERIALS = {
    'mulberry': [('A  dark_oak_wood + jungle_leaves', 'dark_oak_wood', 'jungle_leaves'),
                 ('B  spruce_wood + oak_leaves', 'spruce_wood', 'oak_leaves'),
                 ('C  pale_oak_wood + jungle_leaves', 'pale_oak_wood', 'jungle_leaves')],
    'weeping_willow': [('A  dark_oak_wood + birch_leaves', 'dark_oak_wood', 'birch_leaves'),
                       ('B  spruce_wood + oak_leaves', 'spruce_wood', 'oak_leaves'),
                       ('C  oak_wood + acacia_leaves', 'oak_wood', 'acacia_leaves')],
}


def cards():
    make_sheet.gen = lambda key: getattr(round3, key)
    for i, sp in enumerate(NEW, 12):
        make_sheet.SEEDS = sp['seeds']
        c = make_sheet.card(sp, i)
        out = f'cards/{i:02d}_{sp["key"]}.png'
        c.save(out)
        print(out, c.size)


# ------------------------------------------------------------------ mulberry fruit sketch (twig stages and item)

def jungle_greens():
    """Five shades of jungle leaves in the plains tint, dark to light, so the twig leaves match the crown."""
    tex = voxel.face_texture('jungle_leaves', 'top', 'y')
    cols = sorted({p[:3] for p in tex.getdata() if p[3] > 0}, key=sum)
    pick = [cols[round(i * (len(cols) - 1) / 4)] for i in range(5)]
    return {str(i + 1): c for i, c in enumerate(pick)}


MULBERRY_FRUIT = dict(a=(60, 42, 26), b=(80, 58, 36), c=(102, 76, 48),
                      w=(220, 226, 182), v=(184, 202, 132), g=(142, 168, 92),
                      p=(236, 130, 128), r=(198, 50, 62), R=(138, 24, 42),
                      k=(34, 10, 30), m=(72, 22, 62), h=(130, 62, 112), H=(176, 118, 156))
_TOP = [
    '.......ab.......',
    '..343..ba..343..',
    '.34543.ab.34543.',
    '.23432.ba.23432.',
    '..2.2.b..a.2.2..',
    '.....b....a.....',
]
_EMPTY = '................'
MULBERRY_TWIGS = [
    _TOP + ['.....v....v.....', '....wvg..wvg....', '....vgg..vgg....', '.....g....g.....'] + [_EMPTY] * 6,
    _TOP + ['.....g....g.....', '....prR..prR....', '....rRr..rRr....', '....RrR..RrR....', '.....R....R.....']
    + [_EMPTY] * 5,
    _TOP + ['.....b....b.....', '....Hmk..hmk....', '....mkm..mkm....', '....kmk..kmk....', '....mkm..mkm....',
            '.....k....k.....'] + [_EMPTY] * 4,
]
MULBERRY_ITEM = [
    _EMPTY,
    '........34......',
    '.......3453.....',
    '.......b232.....',
    '.......b........',
    '......hHm.......',
    '.....hmkmk......',
    '.....mkmkm......',
    '.....kmkmk......',
    '.....mkmkm......',
    '.....kmkmk......',
    '......kmk.......',
    '.......k........',
    _EMPTY, _EMPTY, _EMPTY,
]


def fruit_strip(width):
    pal = dict(MULBERRY_FRUIT, **jungle_greens())
    leaf = voxel.face_texture('jungle_leaves', 'top', 'y')
    img = Image.new('RGBA', (width, 330), PAPER)
    d = ImageDraw.Draw(img)
    d.text((20, 6), 'Maulbeere · Skizze: Zweig unter dem Laub, Stufe 0 / 1 / 2, und das Item', font=F_LABEL, fill=INK)
    x = 20
    for stage, rows in enumerate(MULBERRY_TWIGS):
        tile = Image.new('RGBA', (16, 32), (150, 190, 230, 255))
        tile.alpha_composite(leaf, (0, 0))
        tile.alpha_composite(draw(pal, rows), (0, 16))
        img.alpha_composite(tile.resize((128, 256), Image.NEAREST), (x, 36))
        d.text((x, 298), ('weiß-grün', 'rot', 'schwarz, reif')[stage], font=F_SMALL, fill=INK)
        x += 160
    item = Image.new('RGBA', (16, 16), (150, 190, 230, 255))
    item.alpha_composite(draw(pal, MULBERRY_ITEM))
    img.alpha_composite(item.resize((192, 192), Image.NEAREST), (x + 20, 36))
    d.text((x + 20, 236), 'Maulbeere (Item)', font=F_SMALL, fill=INK)
    return img


def materials():
    """Same seed in three materials per species, iso views."""
    rows = []
    for sp in NEW:
        gen = getattr(round3, sp['key'])
        views = []
        for label, wood, leaves in MATERIALS[sp['key']]:
            v = gen(sp['seeds'][0], wood=wood, leaves=leaves).finish().v
            views.append((label, voxel.render(v, margin=10)))
        rows.append((sp, views))
    cell_w = max(i.width for _, views in rows for _, i in views)
    W = 3 * (cell_w + 30) + 30
    parts = []
    for sp, views in rows:
        h = max(i.height for _, i in views)
        img = Image.new('RGBA', (W, h + 90), PAPER)
        d = ImageDraw.Draw(img)
        d.text((24, 10), f'{sp["title"]} · Material-Varianten (gleicher Wuchs)', font=F_LABEL, fill=INK)
        for k, (label, iso) in enumerate(views):
            panel = sky(cell_w, h)
            panel.alpha_composite(iso, ((cell_w - iso.width) // 2, h - iso.height))
            img.alpha_composite(panel, (30 + k * (cell_w + 30), 40))
            d.text((30 + k * (cell_w + 30), h + 48), label, font=F_TEXT, fill=INK)
        parts.append(img)
    parts.append(fruit_strip(W))
    out = Image.new('RGBA', (W, sum(p.height for p in parts) + 70), PAPER)
    d = ImageDraw.Draw(out)
    d.text((24, 14), 'Runde 3 · Material und Frucht', font=F_TITLE, fill=INK)
    y = 70
    for p in parts:
        out.alpha_composite(p, (0, y))
        y += p.height
    out.save('round3_materials.png')
    print('round3_materials.png', out.size)


def lineup():
    """The mod's trees (last self-test) and the two concepts, side view, same scale, a player for reference."""
    s = 10
    entries = []
    for key in ('cypress', 'olive', 'fig', 'strawberry_tree', 'date_palm', 'large_date_palm'):
        path = os.path.join('..', 'run', 'greektrees-selftest', key + '_0.json')
        if os.path.exists(path):
            entries.append((TITLES[key], load(key + '_0')))
    for sp in NEW:
        for seed in sp['seeds'][:2]:
            entries.append((sp['title'] + ' (neu)', getattr(round3, sp['key'])(seed).finish().v))
    views = [(label, voxel.render_side(v, s=s, margin=8)) for label, v in entries]
    gap = 26
    player = voxel.render_side({(0, -1, 0): ('grass_block', 'y')}, s=s, steve=(0, 1), margin=8)
    w = sum(v.width for _, v in views) + gap * (len(views) + 2) + player.width
    top = max(v.height for _, v in views)
    img = sky(w, top + 130)
    d = ImageDraw.Draw(img)
    d.text((gap, 12), 'Größenvergleich · Mod-Bäume (letzter Selbsttest) und die zwei neuen Konzepte', font=F_TITLE,
           fill=INK)
    ground = 80 + top
    x = gap
    img.alpha_composite(player, (x, ground - player.height))
    x += player.width + gap
    for label, v in views:
        img.alpha_composite(v, (x, ground - v.height))
        lw = d.textlength(label, font=F_SMALL)
        d.text((x + (v.width - lw) / 2, ground + 8), label, font=F_SMALL, fill=INK if '(neu)' in label else GREY)
        x += v.width + gap
    img.save('round3_lineup.png')
    print('round3_lineup.png', img.size)


if __name__ == '__main__':
    cards()
    materials()
    lineup()
