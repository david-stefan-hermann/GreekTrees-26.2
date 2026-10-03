"""Round 3 concepts (2026-10-02): mulberry and weeping willow, vanilla blocks only, wood blocks all round like the mod.

Same conventions as trees.py: a generator takes a seed and returns a Tree; y = 0 is the sapling's block. Each
generator takes its blocks as arguments, so make_round3.py can show the same tree in other materials.
"""
import math

from trees import CARDINALS, TAU, Tree, polar


# ==================================================================================== mulberry

MULBERRY = dict(wood='dark_oak_wood', leaves='jungle_leaves')


def mulberry(seed, wood=MULBERRY['wood'], leaves=MULBERRY['leaves'], pollard=None, fruit=True):
    """Morus alba / nigra (Maulbeerbaum, Mouria): the shade tree of the village square and the silk farms. A short,
    thick trunk with a root flare forks low into three to five limbs under a dense, round, fresh green dome that is
    as wide as it is tall or wider. One in three is pollarded (Kopfbaum): a taller trunk ending in a knobbly fist
    with a compact ball of shoots. Mulberries hang under the crown like the olives."""
    t = Tree(seed)
    r = t.rng
    if pollard is None:
        pollard = r.random() < 0.3
    th = r.randint(3, 4) if pollard else r.randint(2, 3)
    for y in range(th + 1):
        t.log((0, y, 0), wood)
    for dx, dz in r.sample(CARDINALS, r.randint(2, 3)):  # root flare
        t.log((dx, 0, dz), wood)
    a0 = r.uniform(0, TAU)
    if pollard:
        # the fist: knobs round the top, a few short thick limbs, each with its own knob, under a flat umbrella
        for dx, dz in CARDINALS:
            if r.random() < 0.6:
                t.log((dx, th, dz), wood)
        for i in range(r.randint(3, 4)):
            ex, ez = polar(a0 + i * TAU / 4 + r.uniform(-0.4, 0.4), r.uniform(1.8, 2.4))
            t.stem([(0, th, 0), (ex, th + 2, ez)], wood)
            t.log((ex, th + 3, ez), wood)
        rad = r.uniform(3.8, 4.4)
        t.blob((0, th + 4.2, 0), rad, 2.1, rad, leaves, erode=0.15, floor=th + 3)
    else:
        n = r.randint(3, 5)
        tips = []
        for i in range(n):
            ang = a0 + i * TAU / n + r.uniform(-0.35, 0.35)
            ex, ez = polar(ang, r.uniform(2.0, 3.0))
            mid = (ex * 0.55, th + r.randint(1, 2), ez * 0.55)
            tip = (ex, th + r.randint(3, 4), ez)
            t.stem([(0, th, 0), mid, tip], wood)
            tips.append(tip)
        top = th + 4
        t.stem([(0, th, 0), (0, top - 1, 0)], wood)  # a leader into the dome keeps its middle within reach of wood
        rad = r.uniform(4.3, 5.2)
        t.blob((0, top + 0.5, 0), rad, 3.0, rad, leaves, erode=0.14, floor=th + 1, hollow=(1.6, th + 2))
        for (x, y, z) in tips:
            t.blob((x * 1.2, y + 0.8, z * 1.2), 2.4, 1.8, 2.4, leaves, erode=0.3, floor=th + 1)
    if fruit:
        hang_under(t, r.randint(5, 9), 'mulberry_twig')
    t.ground(6)
    return t


def hang_under(t, count, block):
    """Fruit right under the lowest leaf of random crown columns (the mod's Shape.hangUnder)."""
    lowest = {}
    for (x, y, z), (b, _) in t.v.items():
        if b.endswith('_leaves'):
            lowest[(x, z)] = min(lowest.get((x, z), y), y)
    spots = [(x, y - 1, z) for (x, z), y in lowest.items() if (x, y - 1, z) not in t.v and y > 1]
    t.rng.shuffle(spots)
    for p in spots[:count]:
        t.v[p] = (block, 'y')


# ==================================================================================== weeping willow

WILLOW = dict(wood='dark_oak_wood', leaves='birch_leaves')


def weeping_willow(seed, wood=WILLOW['wood'], leaves=WILLOW['leaves']):
    """Salix babylonica (Trauerweide, Itia): by springs, streams and the village fountain. A short trunk, often
    leaning, whose steps sideways stay face to face (no blocks touching by an edge only); limbs that rise, run over
    an arch and come down to the rim; a rounded crown, highest over the middle; from its rim strands of leaves hang
    towards the ground, a curtain with a room inside, and a few vines hang down its outside. The strands end where
    vanilla leaf decay would take them (six steps from wood), so the arching limbs come down to the rim."""
    return _willow(seed, False, wood, leaves)


def large_weeping_willow(seed, wood=WILLOW['wood'], leaves=WILLOW['leaves']):
    """The big one, grown from four saplings in a square like a vanilla dark oak: a 2x2 trunk, taller, wider, more
    limbs, longer strands and more vines."""
    return _willow(seed, True, wood, leaves)


def _willow(seed, big, wood, leaves):
    t = Tree(seed)
    r = t.rng
    size = 2 if big else 1
    th = r.randint(5, 7) if big else r.randint(3, 5)
    lean = polar(r.uniform(0, TAU), r.uniform(0.0, 1.5 if big else 1.4))
    for ox in range(size):
        for oz in range(size):
            t.path([(ox, 0, oz), (lean[0] + ox, th, lean[1] + oz)], wood, 'y')
    # root flare round the foot
    feet = [(x, z) for x in range(-1, size + 1) for z in range(-1, size + 1)
            if (x in (-1, size)) != (z in (-1, size))]
    for x, z in r.sample(feet, r.randint(4, 6) if big else r.randint(2, 3)):
        t.log((x, 0, z), wood)
    bx, bz = round(lean[0]), round(lean[1])
    cx, cz = bx + (size - 1) / 2, bz + (size - 1) / 2  # middle of the trunk top
    top = th + (r.randint(4, 5) if big else r.randint(3, 4))
    for ox in range(size):
        for oz in range(size):
            t.path([(bx + ox, th, bz + oz), (bx + ox, top, bz + oz)], wood, 'y')
    # rounded crown, highest over the middle
    rad = r.uniform(4.2, 4.8) if big else r.uniform(3.0, 3.6)
    t.blob((cx, top + 1.0, cz), rad, 3.0 if big else 2.4, rad, leaves, erode=0.2, floor=top - 1)
    # limbs: up and out, over the arch, down to the rim; leaves wrap them up in the crown
    n = r.randint(7, 9) if big else r.randint(5, 7)
    a0 = r.uniform(0, TAU)
    reach = r.uniform(6.3, 7.3) if big else r.uniform(4.3, 5.2)
    drop = 3 if big else 2
    for i in range(n):
        ang = a0 + i * TAU / n + r.uniform(-0.25, 0.25)
        rr = reach + r.uniform(-0.5, 0.5)
        pts = []
        for f, dy in ((0.0, th + 1), (0.3, top), (0.6, top), (0.85, top - 1), (1.0, top - drop - r.randint(0, 1))):
            ox, oz = polar(ang, rr * f)
            pts.append((cx + ox, dy, cz + oz))
        before = set(t.v)
        t.stem(pts, wood)
        for (x, y, z) in set(t.v) - before:
            if y >= top - drop:
                for dx, dy, dz in ((0, 1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (1, 1, 0), (-1, 1, 0),
                                   (0, 1, 1), (0, 1, -1)):
                    if r.random() < 0.85:
                        t.leaf((x + dx, y + dy, z + dz), leaves)
        tip = pts[-1]
        t.blob((tip[0], tip[1] + 0.5, tip[2]), 1.6, 1.0, 1.6, leaves, erode=0.25)
    # curtain: strands from the lowest leaf of the outer columns, long at the rim, short further in
    lowest = {}
    for (x, y, z), (b, _) in t.v.items():
        if b == leaves:
            lowest[(x, z)] = min(lowest.get((x, z), y), y)
    rim = max(math.hypot(x - cx, z - cz) for x, z in lowest)
    inner = 3.5 if big else 2.5
    for (x, z), y in lowest.items():
        d = math.hypot(x - cx, z - cz)
        if d >= rim - 1.6:
            chance, length = 0.65, (r.randint(5, 11) if big else r.randint(4, 9))
        elif d >= inner:
            chance, length = 0.23, r.randint(1, 4 if big else 3)
        else:
            continue
        if r.random() > chance:
            continue
        for yy in range(y - 1, max(0, y - 1 - length), -1):
            if (x, yy, z) in t.v:
                break
            t.leaf((x, yy, z), leaves)
    t.finish()  # strands end where leaves would decay; the vines go on what is left
    # a few vines down the outside of the curtain
    rim_leaves = [(x, y, z) for (x, y, z), (b, _) in t.v.items()
                  if b == leaves and math.hypot(x - cx, z - cz) >= rim - 1.2 and y < top - 1]
    r.shuffle(rim_leaves)
    vines, used = r.randint(6, 10) if big else r.randint(3, 6), set()
    for (x, y, z) in rim_leaves:
        if vines == 0:
            break
        dx, dz = x - cx, z - cz
        out = (1 if dx > 0 else -1, 0) if abs(dx) >= abs(dz) else (0, 1 if dz > 0 else -1)
        vx, vz = x + out[0], z + out[1]
        if (vx, vz) in used or (vx, y, vz) in t.v:
            continue
        used.add((vx, vz))
        vines -= 1
        for yy in range(y, max(0, y - r.randint(3, 8 if big else 6)), -1):
            if (vx, yy, vz) in t.v:
                break
            t.v[(vx, yy, vz)] = ('vine', 'y')
    t.ground(10 if big else 8)
    return t
