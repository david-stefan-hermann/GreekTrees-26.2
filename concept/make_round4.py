"""Concept sheet of the giant tree: the build next to three growths of the generator in round4.py, each seen whole,
cut open through the trunk, and from the side.

cd concept && python make_round4.py  ->  round4_giant.png
The build itself comes from built/giant.json (written by extract_giant.py from the MC5 Backup).
"""
import json
import os

from PIL import Image, ImageDraw

import round4
import voxel
from make_sheet import F_LABEL, F_TEXT, F_TITLE, GREY, INK, PAPER, sky

SEEDS = (1, 2, 3)


def original():
    v = {}
    for x, y, z, b, a in json.load(open(os.path.join('built', 'giant.json'))):
        v[(x, y, z)] = (b, a)
    return v


def views(v, steve):
    # cut open through the middle of the trunk at every height (the trunk sways, a flat cut would miss it)
    trunk_z = {}
    for (x, y, z), (b, _) in v.items():
        if b in ('dark_oak_wood', 'dark_oak_log') and abs(x - 1.5) <= 9:
            trunk_z.setdefault(y, []).append(z)
    mid = {y: sorted(zs)[len(zs) // 2] for y, zs in trunk_z.items()}
    last = 1
    cut_at = {}
    for y in range(min(p[1] for p in v), max(p[1] for p in v) + 1):
        last = mid.get(y, last)
        cut_at[y] = last
    cut = {p: b for p, b in v.items() if p[2] <= cut_at[p[1]]}
    return (voxel.render(v, steve=steve, margin=10), voxel.render(cut, margin=10),
            voxel.render_side(v, s=6, steve=steve, margin=8))


def main():
    cols = [('Original (Stadt, 1:1)', original())]
    for s in SEEDS:
        t = round4.giant(s)
        cols.append((f'Konzept, Wuchs {s}', t.v))
    rendered = []
    for label, v in cols:
        xs = [p[0] for p in v]
        rendered.append((label, views(v, (max(xs) + 1, 0))))
    scale = 0.5
    imgs = [(label, [im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS) for im in ims])
            for label, ims in rendered]
    cw = max(im.width for _, ims in imgs for im in ims) + 20
    rows = [max(ims[k].height for _, ims in imgs) for k in range(3)]
    W = cw * len(imgs) + 40
    H = 130 + sum(rows) + 3 * 40
    img = Image.new('RGBA', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((24, 14), 'Widdereiche (Aries Oak, Quercus arietina): der Bau eines Mitspielers und drei Wüchse des Konzepts', font=F_TITLE,
           fill=INK)
    d.text((26, 60), 'oben ganz, Mitte aufgeschnitten durch den Stamm, unten von der Seite; die Ranken sind hier als '
                     'Würfel gezeichnet, im Spiel hängen sie flach an der Seite', font=F_TEXT, fill=GREY)
    panel = sky(W - 40, H - 120)
    pd = ImageDraw.Draw(panel)
    y = 0
    for k in range(3):
        for i, (label, ims) in enumerate(imgs):
            im = ims[k]
            panel.alpha_composite(im, (i * cw + (cw - im.width) // 2, y + rows[k] - im.height))
            if k == 0:
                pd.text((i * cw + 10, y + 4), label, font=F_LABEL, fill=INK)
        y += rows[k] + 40
    img.alpha_composite(panel, (20, 110))
    img.save('round4_giant.png')
    print('round4_giant.png', img.size)


if __name__ == '__main__':
    main()
