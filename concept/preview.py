"""Quick look: python preview.py <generator> [seed ...] -> out/preview_<generator>.png (iso row over side row)"""
import os
import sys

from PIL import Image

import species
import trees
import voxel


def gen(key):
    return getattr(species if key in species.PICKED else trees, key)


def build(name, seed):
    t = gen(name)(seed).finish()
    x0, x1, z0, z1, top = t.extent()
    sx = x1 + 2
    for gx in range(sx - 1, sx + 2):
        for gz in (-1, 0, 1):
            t.v.setdefault((gx, -1, gz), ('grass_block', 'y'))
    return t, (sx, 0)


def main():
    name = sys.argv[1]
    seeds = [int(s) for s in sys.argv[2:]] or [1, 2, 3]
    os.makedirs('out', exist_ok=True)
    iso, side = [], []
    for s in seeds:
        t, steve = build(name, s)
        bad = voxel.decay_report(t.v)
        x0, x1, z0, z1, top = t.extent()
        print(f'{name} seed {s}: {x1 - x0 + 1 - 3}x{z1 - z0 + 1} wide, {top + 1} tall, {len(t.pruned)} pruned, {len(bad)} still decay')
        iso.append(voxel.render(t.v, steve=steve))
        side.append(voxel.render_side(t.v, steve=steve))
    w = max(sum(i.width for i in iso), sum(i.width for i in side))
    h1 = max(i.height for i in iso)
    h2 = max(i.height for i in side)
    sheet = Image.new('RGBA', (w, h1 + h2), (150, 190, 230, 255))
    x = 0
    for i in iso:
        sheet.alpha_composite(i, (x, h1 - i.height))
        x += i.width
    x = 0
    for i in side:
        sheet.alpha_composite(i, (x, h1 + h2 - i.height))
        x += i.width
    sheet.save(f'out/preview_{name}.png')


if __name__ == '__main__':
    main()
