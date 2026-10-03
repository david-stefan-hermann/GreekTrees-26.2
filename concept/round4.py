"""Round 4 concept (2026-10-02): the Aries oak (Widdereiche, Quercus arietina), after the giant tree a fellow player
built in the Greek city (MC5 Backup, x -9955 z 4728), as a tree that grows from 4x4 saplings. Measured on the build (concept/round4_giant_original.png, data from extract_giant.py), heights
above the grass the trunk stands on:

- trunk: round, 5 wide and hollow, 55 tall (dark oak logs), widened at the foot (0-2), small knots at 8-11 and
  15-18; here a 4x4 trunk with the corners left out, on the 4x4 sapling square
- two tiers of four branches (cardinal), at 29-32 and 43-46, stepping out and up to radius 8 and 10
- lower canopy: a ring of leaves at 31-38, radius 4-14
- upper canopy: a hollow dome, a single leaf thick: a wall of radius 12.6 from 42 to 46, then narrowing to the
  top at 55; azalea leaves with a third flowering azalea leaves, moss blocks in both canopies
- vines round the outside: from the lower canopy to the ground, from the dome's wall down onto the lower canopy;
  glow berry vines hanging from the moss blocks (9 % with berries), some almost to the ground

The generator makes it more organic than the build: the trunk sways in smooth curves, short roots run out over
the ground, branches sit at uneven heights and kink on their way, the dome is bumpy and its lower edge uneven.

Fourth shape (2026-10-02), the user's mix of the earlier ones: the big main dome like the build's (a little bigger,
radius 13.5-15), the side crowns under it on the lower branches as in the second shape (a cloud at the end of each
branch and one half way, a thin ring between them), smaller roots than the third shape's. The third shape (a
cauliflower crown of puffs after big tree builds) was not wanted.

The build's leaves are player-placed and never decay; grown leaves do, more than six steps from wood. So the
generator adds wood where the build has none: ten branches below and twelve to fourteen above instead of four,
and ribs that run up under the dome's shell from every upper branch to the top, so no leaf of the shell is further than six from wood.
"""
import math

from trees import TAU, Tree, polar

WOOD = 'dark_oak_wood'


def giant(seed, wood=WOOD):
    t = Tree(seed)
    r = t.rng

    def leaf():
        return 'flowering_azalea_leaves' if r.random() < 0.32 else 'azalea_leaves'

    H = r.randint(50, 56)  # top of the trunk; the dome closes a block above it
    # The trunk's middle line sways: offsets at a few heights, a random walk that keeps turning, eased in and out
    # between them (no straight stretches, no sharp kinks). The 4x4 trunk follows it layer by layer; a shift of one
    # block keeps three quarters of the trunk in place, so it stays one solid, smoothly bending trunk.
    ctrl = [(0, 0.0, 0.0)]
    ang = r.uniform(0, TAU)
    ox = oz = 0.0
    for f in (0.25, 0.5, 0.72, 1.0):
        ang += r.choice((-1, 1)) * r.uniform(1.2, 2.6)
        dx, dz = polar(ang, r.uniform(1.5, 3.0))
        ox, oz = ox + dx, oz + dz
        ctrl.append((round(H * f), ox, oz))

    def centre(y):
        for (ya, xa, za), (yb, xb, zb) in zip(ctrl, ctrl[1:]):
            if ya <= y <= yb:
                s = (1 - math.cos(math.pi * (y - ya) / max(1, yb - ya))) / 2
                return 1.5 + xa + (xb - xa) * s, 1.5 + za + (zb - za) * s
        return 1.5 + ctrl[-1][1], 1.5 + ctrl[-1][2]

    trunk = [(x, z) for x in range(4) for z in range(4) if not (x in (0, 3) and z in (0, 3))]
    for y in range(H):  # the dome's cap closes over it
        cx, cz = centre(y)
        bx, bz = round(cx - 1.5), round(cz - 1.5)
        for x, z in trunk:
            t.log((bx + x, y, bz + z), wood)
    # the foot widens a little (corners filled, a ring of half the cells round it at the bottom), and a few short
    # roots run out over the ground
    for y in range(2):
        for x, z in ((0, 0), (0, 3), (3, 0), (3, 3)):
            t.log((x, y, z), wood)
    for x in range(-1, 5):
        for z in range(-1, 5):
            if (x in (-1, 4)) != (z in (-1, 4)) and r.random() < 0.5:
                t.log((x, 0, z), wood)
    for i in range(r.randint(4, 6)):
        a = i * TAU / 5 + r.uniform(-0.4, 0.4)
        out = r.uniform(2.0, 3.5)
        p0 = (1.5 + math.cos(a) * 2.2, 1, 1.5 + math.sin(a) * 2.2)
        p1 = (1.5 + math.cos(a) * (2.2 + out), 0, 1.5 + math.sin(a) * (2.2 + out))
        t.path([p0, p1], wood)
    # a few knots on the bare trunk
    for _ in range(r.randint(3, 5)):
        y = r.randint(6, round(H * 0.45))
        cx, cz = centre(y)
        a = r.uniform(0, TAU)
        kx, kz = cx + math.cos(a) * 2.4, cz + math.sin(a) * 2.4
        t.log((kx, y, kz), wood)
        if r.random() < 0.5:
            t.log((kx, y + 1, kz), wood)

    def branch(y0, n, reach, spread, twist):
        """n branches from the trunk around height y0 (each a little higher or lower), out with a kink and up;
        returns their tips with their directions."""
        tips = []
        a0 = r.uniform(0, TAU)
        for i in range(n):
            a = a0 + i * TAU / n + r.uniform(-twist, twist)
            y = y0 + r.randint(-spread, spread)
            rr = reach * r.uniform(0.8, 1.15)
            rise = r.randint(1, 4)
            kink = a + r.uniform(-0.35, 0.35)
            cx, cz = centre(y)
            pts = [(cx + math.cos(a) * 1.8, y, cz + math.sin(a) * 1.8),
                   (cx + math.cos(kink) * rr * 0.55, y + max(1, rise // 2), cz + math.sin(kink) * rr * 0.55),
                   (cx + math.cos(a) * rr, y + rise, cz + math.sin(a) * rr)]
            t.path(pts, wood)
            tips.append((pts[-1], a))
        return tips

    # lower tier: branches, a cloud at the end of each and half way, a thin ring filling between them
    y1 = round(H * 0.55)
    for (x, y, z), a in branch(y1, 10, r.uniform(8.0, 9.5), 2, 0.15):
        s = r.uniform(3.2, 4.8)
        t.blob((x, y + 1.2, z), s, r.uniform(2.4, 3.4), s, leaf, erode=0.35, floor=y - 1)
        cx, cz = centre(y)
        mx, mz = (x + cx) / 2, (z + cz) / 2
        t.blob((mx, y + 1.5, mz), 2.6, 2.0, 2.6, leaf, erode=0.4, floor=y)
    cx1, cz1 = centre(y1)
    t.blob((cx1, y1 + 4.0, cz1), 11.0, 3.0, 11.0, leaf, erode=0.55, floor=y1 + 1, hollow=None)

    # upper tier and the dome, round the top of the trunk
    y2 = round(H * 0.8)
    ccx, ccz = centre(H)
    R0 = r.uniform(13.5, 15.0)
    bumps = [(r.uniform(0.04, 0.08), k, r.uniform(0, TAU)) for k in (2, 3, 5)]
    edge = (r.uniform(0.8, 2.0), r.randint(2, 3), r.uniform(0, TAU))  # how much lower the wall hangs, and where
    wall_top = y2 + r.randint(2, 3)
    dome_h = H + 1 - wall_top

    def wall_r(a):
        return R0 * (1 + sum(amp * math.sin(k * a + ph) for amp, k, ph in bumps))

    def wall_bottom(a):
        return y2 - 1 - round(edge[0] * (1 + math.sin(edge[1] * a + edge[2])))

    def shell_r(y, a):
        if y <= wall_top:
            return wall_r(a)
        k = (y - wall_top) / dome_h
        return wall_r(a) * math.sqrt(max(0.0, 1 - k * k))

    ribs = r.randint(12, 14)
    a0 = r.uniform(0, TAU)
    for i in range(ribs):
        a = a0 + i * TAU / ribs + r.uniform(-0.08, 0.08)
        y = y2 - 3 + r.randint(-1, 1)
        cx, cz = centre(y)
        foot = (ccx + math.cos(a) * (wall_r(a) - 2.0), y2 - 1, ccz + math.sin(a) * (wall_r(a) - 2.0))
        kink = a + r.uniform(-0.25, 0.25)
        t.path([(cx + math.cos(a) * 1.8, y, cz + math.sin(a) * 1.8),
                (cx + math.cos(kink) * wall_r(a) * 0.5, y + 1, cz + math.sin(kink) * wall_r(a) * 0.5), foot], wood)
        prev = foot
        for yy in range(y2, H + 1):
            rr = shell_r(yy + 1, a) - 1.6  # under the shell of this layer and the one above, so the shell hides it
            if rr < 2.5:
                break
            nxt = (ccx + math.cos(a) * rr, yy, ccz + math.sin(a) * rr)
            before = set(t.v)
            t.path([prev, nxt], wood, 'y')
            # leaves round the rib reach out to the shell a block further out, so the shell is fed from it
            for (bx, by, bz) in set(t.v) - before:
                for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    t.leaf((bx + dx, by, bz + dz), leaf)
            prev = nxt
    # the shell: one leaf thick, its lower edge uneven
    moss = []
    rmax = R0 * 1.25
    for y in range(y2 - 5, H + 2):
        for x in range(math.floor(ccx - rmax), math.ceil(ccx + rmax) + 1):
            for z in range(math.floor(ccz - rmax), math.ceil(ccz + rmax) + 1):
                a = math.atan2(z - ccz, x - ccx)
                if y < wall_bottom(a):
                    continue
                d = math.hypot(x - ccx, z - ccz)
                rad = shell_r(y, a)
                inner = shell_r(y + 1, a) if y < H + 1 else 0
                on = (rad - 1.0 <= d <= rad) or (y > wall_top and inner - 0.5 <= d <= rad) or (y >= H - 1 and d <= rad)
                if not on or (x, y, z) in t.v:
                    continue
                if r.random() < 0.05 and y > wall_top:
                    t.put((x, y, z), 'moss_block')
                    moss.append((x, y, z))
                else:
                    t.leaf((x, y, z), leaf)
    for (x, y, z), (b, _) in list(t.v.items()):  # moss in the lower canopy as well
        if y1 + 2 <= y <= y1 + 6 and b.endswith('_leaves') and r.random() < 0.02:
            t.put((x, y, z), 'moss_block')
            moss.append((x, y, z))
    t.finish()  # leaves out of reach of wood go; vines then hang on what is left
    # glow berries, hanging from the moss
    for (x, y, z) in moss:
        if (x, y - 1, z) in t.v:
            continue
        length = r.randint(5, y - 1)
        for yy in range(y - 1, max(0, y - 1 - length), -1):
            if (x, yy, z) in t.v:
                break
            t.v[(x, yy, z)] = ('cave_vines_plant_lit' if r.random() < 0.09 else 'cave_vines_plant', 'y')
    # vines down the outside, from the lowest leaf of the dome's and the lower canopy's outer columns; most reach
    # the ground or the canopy below, a third stop on the way
    lowest = {}
    for (x, y, z), (b, _) in t.v.items():
        if b.endswith('_leaves'):
            for key, lo, hi in (('dome', y2 - 6, H + 2), ('ring', y1 - 2, y1 + 9)):
                if lo <= y <= hi:
                    k = (key, x, z)
                    lowest[k] = min(lowest.get(k, y), y)
    for (key, x, z), y in lowest.items():
        if key == 'dome':
            dx, dz = x - ccx, z - ccz
            if math.hypot(dx, dz) < wall_r(math.atan2(dz, dx)) - 1.2:
                continue
        else:
            dx, dz = x - cx1, z - cz1
            if math.hypot(dx, dz) < 9.0:
                continue
        if r.random() > 0.6:
            continue
        out = (1 if dx > 0 else -1, 0) if abs(dx) >= abs(dz) else (0, 1 if dz > 0 else -1)
        vx, vz = x + out[0], z + out[1]
        bottom = 0 if r.random() < 0.65 else y - r.randint(3, max(3, y // 2))
        for yy in range(y, max(0, bottom) - 1, -1):
            if (vx, yy, vz) in t.v:
                break
            t.v[(vx, yy, vz)] = ('vine', 'y')
    t.ground(16)
    return t
