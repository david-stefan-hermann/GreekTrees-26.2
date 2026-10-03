"""Pulls the hand-built trees of the Greek city out of the MC5 Backup world.

Leaves are grouped into trees (26-connected), the logs inside each tree's footprint are added, and every tree is
saved relative to its trunk base: built/trees.json. Run: python extract_trees.py
"""
import json
import os
from collections import Counter, deque

import world

WORLD = os.path.expandvars(r'%APPDATA%\PrismLauncher\instances\26.2 Fabric new\minecraft\saves\MC5 Backup')
AREA = (-10150, 4600, -9550, 5250)  # around waypoint "0. Tempel" (-9844, 149, 4905)
LEAVES = {'minecraft:azalea_leaves', 'minecraft:flowering_azalea_leaves', 'minecraft:oak_leaves',
          'minecraft:dark_oak_leaves', 'minecraft:spruce_leaves', 'minecraft:birch_leaves', 'minecraft:jungle_leaves',
          'minecraft:acacia_leaves', 'minecraft:mangrove_leaves', 'minecraft:cherry_leaves'}
LOGS = {f'minecraft:{w}_{k}' for w in ('oak', 'spruce', 'birch', 'jungle', 'acacia', 'dark_oak', 'mangrove', 'cherry',
                                       'pale_oak', 'stripped_oak', 'stripped_spruce', 'stripped_dark_oak')
        for k in ('log', 'wood')}


def regions():
    seen = set()
    for x in range(AREA[0], AREA[2] + 1, 256):
        for z in range(AREA[1], AREA[3] + 1, 256):
            p = world.region_file(WORLD, x, z)
            if p not in seen and os.path.exists(p):
                seen.add(p)
                yield p


def main():
    blocks = {}
    for path in regions():
        for pos, name, props in world.blocks_in_region(path, LEAVES | LOGS, area=AREA):
            if AREA[0] <= pos[0] <= AREA[2] and AREA[1] <= pos[2] <= AREA[3]:
                blocks[pos] = (name.split(':')[1], props.get('axis', 'y'), props.get('persistent'))
    leaves = {p for p, b in blocks.items() if b[0].endswith('_leaves')}
    print('blocks', len(blocks), Counter(b[0] for b in blocks.values()).most_common(12))

    # trees = leaf clusters, 26-connected
    seen, trees = set(), []
    for start in leaves:
        if start in seen:
            continue
        comp, q = [], deque([start])
        seen.add(start)
        while q:
            x, y, z = q.popleft()
            comp.append((x, y, z))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        n = (x + dx, y + dy, z + dz)
                        if n in leaves and n not in seen:
                            seen.add(n)
                            q.append(n)
        trees.append(comp)

    out = []
    for comp in trees:
        if len(comp) < 20:
            continue
        xs = [p[0] for p in comp]
        ys = [p[1] for p in comp]
        zs = [p[2] for p in comp]
        x0, x1, z0, z1 = min(xs) - 1, max(xs) + 1, min(zs) - 1, max(zs) + 1
        y0, y1 = min(ys) - 12, max(ys)
        logs = [p for p, b in blocks.items() if not b[0].endswith('_leaves')
                and x0 <= p[0] <= x1 and z0 <= p[2] <= z1 and y0 <= p[1] <= y1]
        if not logs:
            continue
        base = min(logs, key=lambda p: (p[1], p[0], p[2]))
        cells = {}
        for p in comp + logs:
            b = blocks[p]
            cells[f'{p[0] - base[0]},{p[1] - base[1]},{p[2] - base[2]}'] = [b[0], b[1]]
        kinds = Counter(blocks[p][0] for p in comp)
        out.append(dict(origin=list(base), size=[max(xs) - min(xs) + 1, max(ys) - base[1] + 1, max(zs) - min(zs) + 1],
                        leaves=dict(kinds), logs=dict(Counter(blocks[p][0] for p in logs)), blocks=cells))
    out.sort(key=lambda t: (-t['size'][1], t['origin']))
    os.makedirs('built', exist_ok=True)
    with open('built/trees.json', 'w') as f:
        json.dump(out, f)
    for t in out:
        print(t['origin'], 'size', t['size'], t['leaves'], t['logs'])


if __name__ == '__main__':
    main()
