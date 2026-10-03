"""Concept sheets of the Aries oak, round 6 (round6.py):

- round6_design.png: the build next to three growths (the user's pick, growth 2, first), each seen whole, cut open
  through the trunk and from the side
- round6_details.png: growth 2 up close: a side crown cut open (room, twigs, firefly bush), the branches without
  dome and vines (side branches, glow lichen, glow berries), the dome cut open (ribs and their forks)

cd concept && python make_round6.py [design|details]
"""
import math
import sys

from PIL import Image, ImageDraw

import round6
import voxel
from make_round4 import original
from make_round5 import cut, scaled, sheet, steve
from make_sheet import F_LABEL, F_TEXT, F_TITLE, GREY, INK, PAPER, sky

SEEDS = (2, 1, 3)
LICHEN = (128, 150, 136)
_BOX = {'west': (0, 0, 0, 0.2, 1, 1), 'east': (0.8, 0, 0, 0.2, 1, 1), 'down': (0, 0, 0, 1, 0.2, 1),
        'up': (0, 0.8, 0, 1, 0.2, 1), 'north': (0, 0, 0, 1, 1, 0.2), 'south': (0, 0, 0.8, 1, 1, 0.2)}
for _face, _box in _BOX.items():
    voxel.BOX_BLOCKS['glow_lichen@' + _face] = (_box, LICHEN)
voxel.BOX_BLOCKS['firefly_bush'] = ((0.15, 0, 0.15, 0.7, 0.8, 0.7), (196, 150, 60))
# a player standing in a crown, in three cells (feet, body, head): one box per cell, the boxes reach down past it
_PX = 1.8 / 32
voxel.BOX_BLOCKS['steve_legs'] = ((0.5 - 4 * _PX, 0, 0.5 - 2 * _PX, 8 * _PX, 12 * _PX, 4 * _PX), (59, 60, 140))
voxel.BOX_BLOCKS['steve_body'] = ((0.5 - 8 * _PX, 12 * _PX - 1, 0.5 - 2 * _PX, 16 * _PX, 12 * _PX, 4 * _PX),
                                  (0, 168, 168))
voxel.BOX_BLOCKS['steve_head'] = ((0.5 - 4 * _PX, 24 * _PX - 2, 0.5 - 4 * _PX, 8 * _PX, 8 * _PX, 8 * _PX),
                                  (180, 128, 95))


PLANKS = (66, 43, 20)  # dark oak planks
_HALF = {'bottom': (0, 0, 0, 1, 0.5, 1), 'top': (0, 0.5, 0, 1, 0.5, 1)}
_STEP = {'north': (0, 0, 0, 1, 0.5, 0.5), 'south': (0, 0, 0.5, 1, 0.5, 0.5), 'west': (0, 0, 0, 0.5, 0.5, 1),
         'east': (0.5, 0, 0, 0.5, 0.5, 1)}
for _half, _box in _HALF.items():
    voxel.BOX_BLOCKS['dark_oak_slab@' + _half] = (_box, PLANKS)
    for _facing, (_x, _y, _z, _w, _h, _d) in _STEP.items():
        # the slab half, and the step on the facing side in the other half
        voxel.BOX_BLOCKS[f'dark_oak_stairs@{_facing}_{_half}'] = [
            (_box, PLANKS), ((_x, 0.5 if _half == 'bottom' else 0, _z, _w, 0.5, _d), PLANKS)]


def drawable(v):
    """Glow lichen lies on one side of its cell: draw it as a thin plate there. Stairs and slabs as boxes."""
    out = {}
    for p, (b, a) in v.items():
        if b in ('glow_lichen', 'dark_oak_stairs', 'dark_oak_slab'):
            out[p] = (f'{b}@{a}', 'y')
        else:
            out[p] = (b, a)
    return out


def design():
    cols = [('Original (Stadt, Stand Backup)', original())]
    for s in SEEDS:
        label = 'Entwurf 2 ausgebaut (Wuchs 2)' if s == 2 else f'Wuchs {s}'
        cols.append((label, drawable(round6.giant(s).v)))
    rendered = []
    for label, v in cols:
        rendered.append((label, [scaled(voxel.render(v, steve=steve(v), margin=10), 0.5),
                                 scaled(voxel.render(cut(v), margin=10), 0.5),
                                 voxel.render_side(v, s=6, steve=steve(v), margin=8)]))
    sheet(rendered, 'Widdereiche, Runde 6: Entwurf 2 ausgebaut, neben dem Bau eines Mitspielers',
          'oben ganz, Mitte aufgeschnitten durch den Stamm, unten von der Seite; hohle Kronen von kleinen Ästen '
          'aufgespannt, Leuchtflechten (hellgrau), Laub zerfällt nicht', 'round6_design.png')


def wrap(d, text, font, width):
    lines, line = [], ''
    for word in text.split():
        if line and d.textlength(line + ' ' + word, font=font) > width:
            lines.append(line)
            line = word
        else:
            line = (line + ' ' + word).strip()
    return lines + [line]


def details(seed=2):
    t = round6.giant(seed)
    v = drawable(t.v)
    hang = ('vine',)
    # the frame: all wood with what grows on it, no leaves and no vines
    frame = {p: b for p, b in v.items() if not b[0].endswith('_leaves') and b[0] not in hang}
    row1 = [('Gerüst: alles Holz, ohne Laub und Ranken',
             'Stamm mit Stummeln und Knollen, Äste mit Seitenästen und Zweigen, in jeder Seitenkrone ein Zweigschirm, '
             'unter der Kuppel die Rippen mit ihren Gabeln; Leuchtflechten hellgrau, Leuchtbeeren an den Ästen, '
             'grüne Würfel = Moos',
             scaled(voxel.render(frame, steve=steve(frame), margin=10), 0.6))]
    dome_low = min(p[1] for p, (b, _) in t.v.items() if b.endswith('_leaves') and p[1] > 30
                   and math.hypot(p[0] - 1.5, p[2] - 1.5) > 11)
    dome = {p: b for p, b in cut(v).items() if p[1] >= dome_low - 4 and b[0] not in hang}
    row1.append(('Hauptkuppel aufgeschnitten', 'hohl, von den Rippen und ihren Gabeln aufgespannt',
                 scaled(voxel.render(dome, margin=10), 0.6)))
    # the biggest side crown: from outside, with its lid off, cut open from top to bottom
    cr = max(t.crowns, key=lambda c: c['rad'])
    (cx, cy, cz), rad, half, room = cr['c'], cr['rad'], cr['half'], cr['room']
    near = {p: v[p] for p in cr['cells'] | cr['limb'] if p in v and v[p][0] not in hang
            and math.hypot(p[0] - cx, p[2] - cz) <= rad + 4}
    # a player inside, on the wood nearest the middle with room for him
    spots = [(x, y, z) for (x, y, z) in room if (x, y, z) not in t.v and (x, y + 1, z) not in t.v
             and (x, y + 1, z) in room and (x, y + 2, z) not in t.v and t.v.get((x, y - 1, z), ('',))[0] in
             (round6.WOOD, 'moss_block') and z <= round(cz)]
    if spots:
        sx, sy, sz = min(spots, key=lambda p: (abs(p[2] - round(cz)), math.dist(p, (cx, cy, cz))))
        for k, part in enumerate(('steve_legs', 'steve_body', 'steve_head')):
            near[(sx, sy + k, sz)] = (part, 'y')
    lid = {p: b for p, b in near.items() if p[1] <= round(cy) + 1}
    half_cut = {p: b for p, b in near.items() if p[2] <= round(cz)}
    room_free = sum(1 for p in room if p not in t.v)
    row2 = [('Seitenkrone von außen', f'Radius {rad:.1f}, Laub zwei Blöcke dick, unten offen',
             voxel.render(near, margin=10)),
            ('Deckel abgenommen', f'der Zweigschirm von der Astspitze aus; {room_free} freie Blöcke Raum',
             voxel.render(lid, margin=10)),
            ('senkrecht aufgeschnitten', 'ein Spieler steht im Raum auf dem Ast; Moosblock mit Glühwürmchenbusch',
             voxel.render(half_cut, margin=10))]
    rows = [row1, row2]
    probe = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    texts = [[wrap(probe, what, F_TEXT, max(260, im.width)) for _, what, im in row] for row in rows]
    heads = [max(30 + 24 * len(lines) for lines in tr) for tr in texts]
    W = max(sum(max(260, im.width) + 40 for _, _, im in row) for row in rows) + 60
    H = 130 + sum(h + max(im.height for _, _, im in row) + 40 for h, row in zip(heads, rows))
    img = Image.new('RGBA', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((24, 14), f'Widdereiche, Runde 6: Einzelheiten von Wuchs {seed}', font=F_TITLE, fill=INK)
    d.text((26, 60), f'{len(t.crowns)} Seitenkronen; mit normalem statt dauerhaftem Laub würden {t.would_decay} '
                     'Blätter zerfallen', font=F_TEXT, fill=GREY)
    panel = sky(W - 40, H - 120)
    pd = ImageDraw.Draw(panel)
    y = 14
    for row, tr, head in zip(rows, texts, heads):
        x = 20
        tall = max(im.height for _, _, im in row)
        for (label, _, im), lines in zip(row, tr):
            pd.text((x, y), label, font=F_LABEL, fill=INK)
            for k, line in enumerate(lines):
                pd.text((x, y + 26 + 24 * k), line, font=F_TEXT, fill=GREY)
            panel.alpha_composite(im, (x, y + head + tall - im.height))
            x += max(260, im.width) + 40
        y += head + tall + 40
    img.alpha_composite(panel, (20, 110))
    img.save('round6_details.png')
    print('round6_details.png', img.size)


if __name__ == '__main__':
    which = sys.argv[1:] or ['design', 'details']
    if 'design' in which:
        design()
    if 'details' in which:
        details()
