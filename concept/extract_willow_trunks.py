"""Pulls the willow trunks the user rebuilt by hand out of the Prism test world "New World".

Writes reference/willow_trunk_<name>.json (the tree's wood, relative to its foot, in the format of the self-test
dumps) and prints every trunk layer by layer (x to the right, z down). Run: python extract_willow_trunks.py
"""
import glob
import json
import os
from collections import deque

import world

WORLD = os.path.expandvars(r'%APPDATA%\PrismLauncher\instances\26.2 Fabric new\minecraft\saves\New World')
WOOD = 'minecraft:pale_oak_wood'
# name -> a block of the trunk's foot (x, z), read off the world on 2026-10-03
TREES = {'small_1': (-46, 574), 'small_2': (13, 556), 'small_3': (-12, 565),
         'big_1': (-73, 559), 'big_2': (-104, 555), 'big_3': (-170, 224)}


def main():
    wood = {}
    for path in glob.glob(os.path.join(WORLD, 'dimensions', 'minecraft', 'overworld', 'region', '*.mca')):
        if os.path.getsize(path):
            for pos, _, props in world.blocks_in_region(path, {WOOD}):
                wood[pos] = props.get('axis', 'y')
    os.makedirs('reference', exist_ok=True)
    for name, (fx, fz) in TREES.items():
        start = min(wood, key=lambda p: (abs(p[0] - fx) + abs(p[2] - fz), p[1]))
        comp, todo = {start}, deque([start])
        while todo:  # the tree: wood joined over faces, edges and corners
            x, y, z = todo.popleft()
            for q in ((x + i, y + j, z + k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)):
                if q in wood and q not in comp:
                    comp.add(q)
                    todo.append(q)
        y0 = min(p[1] for p in comp)
        above = [p for p in comp if p[1] == y0 + 1 and abs(p[0] - fx) <= 3 and abs(p[2] - fz) <= 3]
        ox, oz = min(p[0] for p in above), min(p[2] for p in above)  # the foot: north-west cell of the layer above the flare
        cells = sorted((x - ox, y - y0, z - oz) for x, y, z in comp)
        with open(f'reference/willow_trunk_{name}.json', 'w') as f:
            json.dump([[x, y, z, 'pale_oak_wood', wood[(x + ox, y + y0, z + oz)]] for x, y, z in cells], f)
        print(f'\n{name} at {ox} {y0} {oz}: {len(cells)} wood')
        layers = []
        for y in range(max(c[1] for c in cells) + 1):
            layer = {(x, z) for x, yy, z in cells if yy == y and -3 <= x <= 4 and -3 <= z <= 4}
            layers.append(layer)
            if y > 1 and len(layer) > 9:
                break  # the limbs fan out
        for a in range(0, len(layers), 9):
            part = list(enumerate(layers))[a:a + 9]
            print('  '.join(f'y{y:<7}' for y, _ in part))
            for z in range(-3, 5):
                print('  '.join(''.join('#' if (x, z) in layer else '.' for x in range(-3, 5)) for _, layer in part))


if __name__ == '__main__':
    main()
