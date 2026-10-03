"""Side by side: hand-built cypresses from the MC5 backup (top) and generated ones (bottom), same scale.

python compare_cypress.py -> cypress_compare.png
"""
import json
from collections import Counter

from PIL import Image, ImageDraw

import species
import voxel
from make_sheet import F_LABEL, F_SMALL, F_TEXT, F_TITLE, GREY, INK, PAPER, sky

REAL = ['-9955,109,4922', '-9866,123,4860', '-9798,138,4881', '-9944,109,4890', '-9848,138,4881', '-9942,109,4948']


def real_trees():
    out = []
    for t in json.load(open('built/trees.json')):
        key = ','.join(map(str, t['origin']))
        if key not in REAL:
            continue
        raw = {tuple(map(int, k.split(','))): v for k, v in t['blocks'].items()}
        logs = [p for p, v in raw.items() if not v[0].endswith('_leaves')]
        cx, cz = Counter((p[0], p[2]) for p in logs).most_common(1)[0][0]
        y0 = min(p[1] for p in logs if (p[0], p[2]) == (cx, cz))
        v = {(p[0] - cx, p[1] - y0, p[2] - cz): (b[0], b[1]) for p, b in raw.items()}
        for x in range(-3, 4):
            for z in range(-3, 4):
                if x * x + z * z <= 12.25:
                    v[(x, -1, z)] = ('grass_block', 'y')
        out.append((key, v))
    out.sort(key=lambda kv: REAL.index(kv[0]))
    return out


def main():
    real = real_trees()
    gen = []
    for seed in range(1, 7):
        t = species.grow('cypress', seed)
        gen.append((seed, t.v, t.params))
    imgs_r = [voxel.render(v, margin=8) for _, v in real]
    imgs_g = [voxel.render(v, margin=8) for _, v, _ in gen]
    cell_w = max(i.width for i in imgs_r + imgs_g) + 20
    cell_h = max(i.height for i in imgs_r + imgs_g) + 50
    W = cell_w * 6 + 40
    H = 110 + 2 * (cell_h + 50) + 20
    img = Image.new('RGBA', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((24, 14), 'Zypresse · deine Bäume und der Generator', font=F_TITLE, fill=INK)
    d.text((26, 60), 'Oben: 6 der 32 Zypressen aus der Stadt (MC5-Backup, Eichenstamm wie gebaut). '
           'Unten: 6 Wüchse des Generators (Akazienstamm). Gleicher Maßstab.', font=F_TEXT, fill=GREY)
    for row, (label, imgs, caps) in enumerate((
            ('Deine Bäume', imgs_r, [k.replace(',', ' / ') for k, _ in real]),
            ('Generator', imgs_g, [species.summary('cypress', p)[0] for _, _, p in gen]))):
        y = 110 + row * (cell_h + 50)
        d.text((24, y), label, font=F_LABEL, fill=INK)
        panel = sky(W - 40, cell_h)
        for i, (im, cap) in enumerate(zip(imgs, caps)):
            x = 20 + i * cell_w
            panel.alpha_composite(im, (x - 20 + (cell_w - im.width) // 2, cell_h - 40 - im.height))
            pd = ImageDraw.Draw(panel)
            tw = pd.textlength(cap, font=F_SMALL)
            pd.text((x - 20 + (cell_w - tw) / 2, cell_h - 30), cap, font=F_SMALL, fill=INK)
        img.alpha_composite(panel, (20, y + 30))
    img.save('cypress_compare.png')
    print(img.size)


if __name__ == '__main__':
    main()
