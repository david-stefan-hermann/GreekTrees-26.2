"""Pulls the giant tree of the Greek city out of the MC5 Backup world (x -9955, z 4728) into built/giant.json,
relative to the middle of its trunk foot (stairs and slabs as planks, glow berry vines with or without berries).

python extract_giant.py
"""
import json
import os
from collections import Counter, deque

import world

WORLD = os.path.expandvars(r'%APPDATA%\PrismLauncher\instances\26.2 Fabric new\minecraft\saves\MC5 Backup')
CX, CZ, R = -9955, 4728, 32
AREA = (CX - R, CZ - R, CX + R, CZ + R)
TREE = {'azalea_leaves', 'flowering_azalea_leaves', 'vine', 'cave_vines_plant', 'cave_vines', 'dark_oak_log',
        'moss_block', 'dark_oak_stairs', 'dark_oak_slab'}


class AnyBlock:
    def __contains__(self, name):
        return name.split(':')[1] in TREE


def main():
    blocks = {}
    seen = set()
    for x in range(AREA[0], AREA[2] + 1, 16):
        for z in range(AREA[1], AREA[3] + 1, 16):
            p = world.region_file(WORLD, x, z)
            if p in seen or not os.path.exists(p):
                continue
            seen.add(p)
            for pos, name, props in world.blocks_in_region(p, AnyBlock(), area=AREA):
                if AREA[0] <= pos[0] <= AREA[2] and AREA[1] <= pos[2] <= AREA[3]:
                    blocks[pos] = (name.split(':')[1], props)
    # the tree: everything 26-connected to the lowest log
    start = min((p for p, b in blocks.items() if b[0] == 'dark_oak_log'), key=lambda p: p[1])
    tree = {start}
    q = deque([start])
    while q:
        x, y, z = q.popleft()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    n = (x + dx, y + dy, z + dz)
                    if n not in tree and n in blocks:
                        tree.add(n)
                        q.append(n)
    print('tree blocks', len(tree), Counter(blocks[p][0] for p in tree).most_common())
    foot = [p for p in tree if p[1] == start[1] and blocks[p][0] == 'dark_oak_log']
    bx = round(sum(p[0] for p in foot) / len(foot))
    bz = round(sum(p[2] for p in foot) / len(foot))
    out = []
    for (x, y, z) in tree:
        n, pr = blocks[(x, y, z)]
        if n in ('dark_oak_stairs', 'dark_oak_slab'):
            n = 'dark_oak_planks'
        elif n.startswith('cave_vines'):
            n += '_lit' if pr.get('berries') == 'true' else ''
        out.append([x - bx, y - start[1], z - bz, n, pr.get('axis', 'y')])
    xs = [p[0] for p in out]
    zs = [p[2] for p in out]
    for x in range(min(xs) - 1, max(xs) + 2):
        for z in range(min(zs) - 1, max(zs) + 2):
            out.append([x, -1, z, 'grass_block', 'y'])
    os.makedirs('built', exist_ok=True)
    json.dump(out, open(os.path.join('built', 'giant.json'), 'w'))
    print('built/giant.json', len(out))


if __name__ == '__main__':
    main()
