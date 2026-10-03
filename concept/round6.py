"""Round 6 concept (2026-10-03): the Aries oak, the user's pick from round 5 ("Entwurf 2", the design's second
growth) built out after the user's screenshots of the build as it stands on the server now (Prism screenshots
2026-10-02_23.56.14 to 23.57.08):

- more detailed branches: every limb carries two to four side branches with a tuft of leaves and a few short
  twigs; short broken-off stubs sit on the bare trunk, as on the build
- glow lichen in patches on the trunk and the branches; glow berries hang from the undersides of the limbs (on the
  build they hang along the trunk from the branches), and from moss in the dome
- every crown is hollow and spanned by small branches, so there is room inside to build: the side crowns are
  upturned bowls of leaves two thick, open underneath round the limb, with twigs running from the limb's tip up to
  the leaves; the main dome's ribs show inside it (no more leaves wrapped round them) and fork once on the way up
- the leaves never decay (in the mod they are placed persistent), so the leaves need no wood within six steps and
  nothing is pruned
- a moss block with a firefly bush on the limb inside some side crowns (the build has one in a crown)

Trunk, limbs, dome and vines are round 5's design (round5.py).
"""
import math

from trees import TAU, Tree, polar
from voxel import decay_report

WOOD = 'dark_oak_wood'
FACES = {'west': (-1, 0, 0), 'east': (1, 0, 0), 'down': (0, -1, 0), 'up': (0, 1, 0), 'north': (0, 0, -1),
         'south': (0, 0, 1)}

DESIGN = dict(
    H=(50, 56),            # height of the trunk's top; the dome closes a block above it
    # trunk
    r_base=(5.2, 5.8),     # radius at the ground (the flare)
    r_mid=(3.3, 3.7),      # radius where the flare has run out
    r_top=(2.1, 2.4),      # radius under the dome
    flare=(6, 8),          # height the flare runs up
    buttress=0.28,         # depth of the buttresses at the ground, a share of the radius
    ridges=0.09,           # depth of the ridges up the bark
    twist=0.035,           # how far the ridges turn per block (radians)
    sway=(1.6, 2.6),       # how far the middle line wanders per step
    burls=(3, 5),
    stubs=(3, 5),          # short broken-off branches on the bare trunk
    roots=(1.5, 2.8),      # how far the roots run out beyond the foot
    # side crowns
    limbs=(5, 7),
    limb_y=(0.40, 0.62),   # heights the limbs leave the trunk at, shares of H
    reach=(1.10, 1.35),    # where the crown's middle lies, a share of the dome's radius
    lift=(4, 7),           # how much the limb climbs on its way out
    limb_r=(1.5, 1.9),     # limb radius at the trunk
    crown=(5.6, 6.8),      # crown radius
    crown_h=(4.4, 5.0),    # crown half height
    shell=2.0,             # thickness of the crowns' leaves
    puffs=(3, 5),
    side_branches=(2, 4),  # per limb, each with a tuft of leaves
    twigs=(2, 4),          # short bare twigs per limb
    fireflies=0.6,         # chance a side crown gets moss with a firefly bush on its limb
    # main dome
    R=(13.5, 15.0),
    wall=0.80,             # where the dome's wall starts, a share of H
    bumps=(0.04, 0.08),
    # hangings and colour
    vines=0.25,            # chance an outer rim leaf gets a vine
    long_vines=0.35,       # chance a vine runs to the ground (or onto what is below)
    moss=0.02,
    berries=0.09,          # glow berries on a cave vine
    limb_berries=0.03,     # chance a limb block with air below grows a glow berry vine
    lichen=(35, 50),       # glow lichen patches on the wood
    flowering=0.32,
)


def giant(seed, **over):
    t = Tree(seed)
    r = t.rng
    P = dict(DESIGN, **over)

    def val(key):
        v = P[key]
        if isinstance(v, tuple):
            return r.randint(*v) if isinstance(v[0], int) else r.uniform(*v)
        return v

    def leaf():
        return 'flowering_azalea_leaves' if r.random() < P['flowering'] else 'azalea_leaves'

    H = val('H')
    # ------------------------------------------------------------------------------------------------ trunk
    # the middle line: a random walk that keeps turning, eased between its points (no straight stretches, no kinks)
    ctrl = [(0, 0.0, 0.0)]
    ang = r.uniform(0, TAU)
    ox = oz = 0.0
    for f in (0.25, 0.5, 0.75, 1.0):
        ang += r.choice((-1, 1)) * r.uniform(1.2, 2.6)
        dx, dz = polar(ang, val('sway'))
        ox, oz = ox + dx, oz + dz
        ctrl.append((round(H * f), ox, oz))

    def centre(y):
        for (ya, xa, za), (yb, xb, zb) in zip(ctrl, ctrl[1:]):
            if ya <= y <= yb:
                s = (1 - math.cos(math.pi * (y - ya) / max(1, yb - ya))) / 2
                return 1.5 + xa + (xb - xa) * s, 1.5 + za + (zb - za) * s
        return 1.5 + ctrl[-1][1], 1.5 + ctrl[-1][2]

    r_base, r_mid, r_top, flare = val('r_base'), val('r_mid'), val('r_top'), val('flare')
    ridges, twist, buttress = P['ridges'], P['twist'], P['buttress']
    lobes = r.randint(4, 5)
    ph = [r.uniform(0, TAU) for _ in range(3)]

    def radius(y):
        """Mean radius at height y: a slow narrowing from r_mid to r_top, plus the flare at the foot."""
        k = min(1.0, max(0.0, y / H))
        f = max(0.0, 1 - y / flare)
        return r_top + (r_mid - r_top) * (1 - k) ** 1.3 + (r_base - r_mid) * f * f

    def radius_at(y, a):
        f = max(0.0, 1 - y / flare)
        wave = ridges * (0.6 * math.sin(3 * a + ph[0] + twist * y) + 0.4 * math.sin(5 * a + ph[1] - 0.7 * twist * y))
        wave += buttress * f * f * max(0.0, math.sin(lobes * a + ph[2]))
        return radius(y) * (1 + wave)

    for y in range(H):
        cx, cz = centre(y)
        rm = radius(y) * (1 + ridges + buttress) + 1
        for x in range(math.floor(cx - rm), math.ceil(cx + rm) + 1):
            for z in range(math.floor(cz - rm), math.ceil(cz + rm) + 1):
                d = math.hypot(x - cx, z - cz)
                if d <= radius_at(y, math.atan2(z - cz, x - cx)):
                    t.log((x, y, z), WOOD)
    # short roots out of the buttresses
    for i in range(lobes):
        a = (math.pi / 2 - ph[2] + i * TAU) / lobes + r.uniform(-0.15, 0.15)  # the lobes' outer points
        cx, cz = centre(0)
        d0 = r_base * (1 + buttress) - 0.5
        out = val('roots')
        t.path([(cx + math.cos(a) * d0, 1, cz + math.sin(a) * d0),
                (cx + math.cos(a) * (d0 + out), 0, cz + math.sin(a) * (d0 + out))], WOOD)
    # burls
    for _ in range(val('burls')):
        y = r.randint(flare, round(H * 0.6))
        cx, cz = centre(y)
        a = r.uniform(0, TAU)
        d = radius_at(y, a)
        s = r.uniform(0.9, 1.6)
        bx, bz = cx + math.cos(a) * (d + 0.3), cz + math.sin(a) * (d + 0.3)
        for x in range(math.floor(bx - s), math.ceil(bx + s) + 1):
            for yy in range(math.floor(y - s * 1.3), math.ceil(y + s * 1.3) + 1):
                for z in range(math.floor(bz - s), math.ceil(bz + s) + 1):
                    if ((x - bx) / s) ** 2 + ((yy - y) / (s * 1.3)) ** 2 + ((z - bz) / s) ** 2 <= 1:
                        t.log((x, yy, z), WOOD)

    # ------------------------------------------------------------------------------------------------ helpers
    def bezier(pts, s):
        n = len(pts) - 1
        out = [0.0, 0.0, 0.0]
        for i, p in enumerate(pts):
            w = math.comb(n, i) * (1 - s) ** (n - i) * s ** i
            for k in range(3):
                out[k] += w * p[k]
        return tuple(out)

    def tube(pts, r0, r1):
        """A round limb along a Bezier curve, radius r0 at the start narrowing to r1; a face-connected core line
        keeps it whole where it gets thin."""
        length = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
        n = max(2, int(length * 3))
        line = [bezier(pts, i / n) for i in range(n + 1)]
        t.path(line, WOOD)
        for i, (px, py, pz) in enumerate(line):
            rad = r0 + (r1 - r0) * i / n
            if rad < 0.7:
                continue
            for x in range(math.floor(px - rad), math.ceil(px + rad) + 1):
                for y in range(math.floor(py - rad), math.ceil(py + rad) + 1):
                    for z in range(math.floor(pz - rad), math.ceil(pz + rad) + 1):
                        if (x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2 <= rad * rad:
                            t.log((x, y, z), WOOD)
        return line

    # stubs: short broken-off branches on the bare trunk, some with a tuft of leaves
    for _ in range(val('stubs')):
        y = r.randint(flare + 2, round(H * 0.38))
        cx, cz = centre(y)
        a = r.uniform(0, TAU)
        d = radius_at(y, a)
        length = r.uniform(2.0, 4.0)
        end = (cx + math.cos(a) * (d + length), y + r.uniform(0, 2), cz + math.sin(a) * (d + length))
        tube([(cx + math.cos(a) * (d - 0.5), y, cz + math.sin(a) * (d - 0.5)), end], 0.9, 0.5)
        if r.random() < 0.5:
            t.blob((end[0], end[1] + 0.8, end[2]), 1.6, 1.2, 1.6, leaf, erode=0.3)

    crowns = []  # the side crowns: middle, radius, half height, room cells and own cells, for the hangings and figures
    moss = []

    def crown(c, rad, half, puffs):
        """A hollow crown round c: puffs of leaves two thick over a room that is open underneath where the limb comes
        in; twigs from the limb's tip (c, one below) span the leaves from the inside."""
        cx, cy, cz = c
        before = set(t.v)
        # a wide puff in the middle, a higher one on top of it (the crown arches), smaller ones round the rim
        spots = [(cx, cy, cz, rad, half), (cx + r.uniform(-1, 1), cy + half * 0.8, cz + r.uniform(-1, 1),
                                           rad * r.uniform(0.6, 0.72), half * 0.8)]
        a0 = r.uniform(0, TAU)
        for i in range(puffs - 1):
            a = a0 + i * TAU / (puffs - 1) + r.uniform(-0.4, 0.4)
            d = rad * r.uniform(0.5, 0.75)
            spots.append((cx + math.cos(a) * d, cy + r.uniform(-1.0, 1.2), cz + math.sin(a) * d,
                          rad * r.uniform(0.55, 0.72), half * r.uniform(0.8, 1.0)))
        shell = P['shell']
        outer, room = {}, set()
        for x, y, z, s, h in spots:
            yc = y + 0.6
            floor_y = round(y - h * 0.7)
            for X in range(math.floor(x - s), math.ceil(x + s) + 1):
                for Y in range(floor_y, math.ceil(yc + h) + 1):
                    for Z in range(math.floor(z - s), math.ceil(z + s) + 1):
                        d = ((X - x) / s) ** 2 + ((Y - yc) / h) ** 2 + ((Z - z) / s) ** 2
                        if d > 1:
                            continue
                        outer[(X, Y, Z)] = min(d, outer.get((X, Y, Z), 2))
                        # the room: the puff shrunk by the shell's thickness above its middle; below the middle it
                        # keeps the full height, so it runs out through the bottom and the bowl is open there
                        si = s - shell
                        hi = h - shell if Y >= yc else h
                        if si > 0.5 and ((X - x) / si) ** 2 + ((Y - yc) / hi) ** 2 + ((Z - z) / si) ** 2 <= 1:
                            room.add((X, Y, Z))
        for p, d in outer.items():
            if p in room or (d > 0.8 and r.random() < 0.18):
                continue
            t.leaf(p, leaf)
        # twigs: one to the middle of every puff, from there three out to the leaves
        tip = (cx, cy - 1, cz)
        for x, y, z, s, h in spots:
            fork = (x, y + 0.6, z)
            t.path([tip, fork], WOOD)
            for k in range(3):
                a = r.uniform(0, TAU)
                up = r.uniform(0.2, 0.9)
                reach = (s - shell + 0.6)
                end = (x + math.cos(a) * reach * math.sqrt(1 - up * up), y + 0.6 + (h - shell + 0.6) * up,
                       z + math.sin(a) * reach * math.sqrt(1 - up * up))
                t.path([fork, end], WOOD)
        # moss with a firefly bush on the limb, inside the room
        if r.random() < P['fireflies']:
            for dx, dz in sorted(((dx, dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1)), key=lambda q: r.random()):
                x, z = round(cx) + dx, round(cz) + dz
                ys = [y for y in range(round(cy) - 3, round(cy) + 2) if t.v.get((x, y, z), ('',))[0] == WOOD]
                if not ys:
                    continue
                y = max(ys) + 1
                if all((x, yy, z) not in t.v and (x, yy, z) in room for yy in (y, y + 1)):
                    t.put((x, y, z), 'moss_block')
                    t.put((x, y + 1, z), 'firefly_bush')
                    break
        crowns.append(dict(c=c, rad=rad, half=half, room=room, cells=set(t.v) - before))

    # ------------------------------------------------------------------------------------------------ dome
    R0 = val('R')
    y2 = round(H * P['wall'])
    ccx, ccz = centre(H)

    # ------------------------------------------------------------------------------------------------ side crowns
    n = val('limbs')
    lo, hi = P['limb_y']
    heights = [lo + (hi - lo) * (i + r.uniform(-0.3, 0.3)) / max(1, n - 1) for i in range(n)]
    r.shuffle(heights)
    a0 = r.uniform(0, TAU)
    limb_cells = set()
    for i in range(n):
        a = a0 + i * TAU / n + r.uniform(-0.2, 0.2)
        y = round(H * heights[i])
        cx, cz = centre(y)
        rt = radius_at(y, a)
        D = R0 * val('reach')
        lift = val('lift')
        drift = r.uniform(-0.35, 0.35)
        before = set(t.v)
        start = (cx + math.cos(a) * (rt - 0.8), y, cz + math.sin(a) * (rt - 0.8))
        # rises out of the trunk, arcs outward, lifts again at the tip
        p1 = (cx + math.cos(a) * D * 0.3, y + lift * 0.7, cz + math.sin(a) * D * 0.3)
        p2 = (cx + math.cos(a + drift) * D * 0.7, y + lift * 0.6, cz + math.sin(a + drift) * D * 0.7)
        tip = (cx + math.cos(a + drift * 0.6) * D, y + lift, cz + math.sin(a + drift * 0.6) * D)
        r0 = val('limb_r')
        line = tube([start, p1, p2, tip], r0, 0.4)
        # side branches with a tuft of leaves, and bare twigs
        for k in range(val('side_branches')):
            j = r.randint(len(line) // 4, 3 * len(line) // 4)
            px, py, pz = line[j]
            fa = a + drift + r.choice((-1, 1)) * r.uniform(0.6, 1.3)
            fl = r.uniform(3.0, 5.5)
            ftip = (px + math.cos(fa) * fl, py + r.uniform(1.5, 4.0), pz + math.sin(fa) * fl)
            tube([(px, py, pz), (px + math.cos(fa) * fl * 0.55, py + 0.6, pz + math.sin(fa) * fl * 0.55), ftip],
                 max(0.4, (r0 + (0.4 - r0) * j / len(line)) * 0.55), 0.4)
            t.blob((ftip[0], ftip[1] + 1.0, ftip[2]), r.uniform(2.0, 2.8), r.uniform(1.5, 2.0), r.uniform(2.0, 2.8),
                   leaf, erode=0.35, floor=round(ftip[1]))
        for k in range(val('twigs')):
            px, py, pz = line[r.randint(len(line) // 5, 4 * len(line) // 5)]
            fa = r.uniform(0, TAU)
            rad = r0 + (0.4 - r0) * 0.5
            t.path([(px, py, pz), (px + math.cos(fa) * (rad + r.uniform(1.0, 2.2)), py + r.uniform(0.5, 2.0),
                                   pz + math.sin(fa) * (rad + r.uniform(1.0, 2.2)))], WOOD)
        own = set(t.v) - before
        limb_cells |= own
        crown((tip[0], tip[1] + 1, tip[2]), val('crown'), val('crown_h'), val('puffs'))
        crowns[-1]['limb'] = own

    # ------------------------------------------------------------------------------------------------ dome
    bumps = [(val('bumps'), k, r.uniform(0, TAU)) for k in (2, 3, 5)]
    edge = (r.uniform(0.8, 2.0), r.randint(2, 3), r.uniform(0, TAU))  # how much lower the wall hangs, and where
    wall_top = y2 + r.randint(2, 3)
    dome_top = H + 1
    dome_h = dome_top - wall_top

    def wall_r(a):
        return R0 * (1 + sum(amp * math.sin(k * a + p) for amp, k, p in bumps))

    def wall_bottom(a):
        return y2 - 1 - round(edge[0] * (1 + math.sin(edge[1] * a + edge[2])))

    def shell_r(y, a):
        if y <= wall_top:
            return wall_r(a)
        k = (y - wall_top) / dome_h
        return wall_r(a) * math.sqrt(max(0.0, 1 - k * k))

    def rib(a, prev, y_from):
        """Up under the shell along angle a from prev, a layer at a time."""
        for yy in range(y_from, dome_top):
            rr = shell_r(yy + 1, a) - 1.6  # under the shell of this layer and the one above, so the shell hides it
            if rr < 2.5:
                break
            nxt = (ccx + math.cos(a) * rr, yy, ccz + math.sin(a) * rr)
            t.path([prev, nxt], WOOD, 'y')
            prev = nxt

    ribs = max(12, round(R0 * 0.9))
    gap = TAU / ribs
    a0 = r.uniform(0, TAU)
    for i in range(ribs):
        a = a0 + i * gap + r.uniform(-0.08, 0.08)
        y = y2 - 3 + r.randint(-1, 1)
        cx, cz = centre(y)
        rt = radius_at(y, a)
        foot = (ccx + math.cos(a) * (wall_r(a) - 2.0), y2 - 1, ccz + math.sin(a) * (wall_r(a) - 2.0))
        kink = a + r.uniform(-0.25, 0.25)
        tube([(cx + math.cos(a) * (rt - 0.5), y - 1, cz + math.sin(a) * (rt - 0.5)),
              (cx + math.cos(kink) * wall_r(a) * 0.5, y + 1.5, cz + math.sin(kink) * wall_r(a) * 0.5), foot], 1.1, 0.4)
        rib(a, foot, y2)
        # a fork from the rib where the dome starts to close, half way to the next rib
        fy = wall_top + r.randint(0, 2)
        fa = a + r.choice((-1, 1)) * gap * r.uniform(0.4, 0.55)
        rr = shell_r(fy + 1, a) - 1.6
        rib(fa, (ccx + math.cos(a) * rr, fy, ccz + math.sin(a) * rr), fy + 1)
    rmax = R0 * 1.3
    for y in range(y2 - 5, dome_top + 1):
        for x in range(math.floor(ccx - rmax), math.ceil(ccx + rmax) + 1):
            for z in range(math.floor(ccz - rmax), math.ceil(ccz + rmax) + 1):
                a = math.atan2(z - ccz, x - ccx)
                if y < wall_bottom(a):
                    continue
                d = math.hypot(x - ccx, z - ccz)
                rad = shell_r(y, a)
                inner = shell_r(y + 1, a) if y < dome_top else 0
                on = (rad - 1.0 <= d <= rad) or (y > wall_top and inner - 0.5 <= d <= rad) or \
                     (y >= dome_top - 1 and d <= rad)
                if not on or (x, y, z) in t.v:
                    continue
                if r.random() < 0.05 and y > wall_top:
                    t.put((x, y, z), 'moss_block')
                    moss.append(((x, y, z), 'dome'))
                else:
                    t.leaf((x, y, z), leaf)
    # the leaves are persistent: nothing is pruned; count what would decay if they were not
    t.pruned = []
    t.would_decay = len(decay_report(t.v))

    # ------------------------------------------------------------------------------------------------ hangings
    def free(p):
        return p not in t.v

    in_room = set().union(*(c['room'] for c in crowns)) if crowns else set()
    leaves = [p for p, (b, _) in t.v.items() if b.endswith('_leaves')]
    for p in leaves:  # moss under the canopies grows glow berries
        x, y, z = p
        if free((x, y - 1, z)) and r.random() < P['moss']:
            t.put(p, 'moss_block')
            moss.append((p, 'room' if (x, y - 1, z) in in_room else 'dome'))
    for (x, y, z), where in moss:
        if t.v.get((x, y, z), ('',))[0] != 'moss_block' or not free((x, y - 1, z)):
            continue
        # short in the side crowns' rooms (light, but room to build), long under the dome
        length = r.randint(1, 4) if where == 'room' else r.randint(3, max(3, min(24, y - 2)))
        for yy in range(y - 1, max(0, y - 1 - length), -1):
            if not free((x, yy, z)):
                break
            t.v[(x, yy, z)] = ('cave_vines_plant_lit' if r.random() < P['berries'] else 'cave_vines_plant', 'y')
    # glow berries from the limbs' undersides
    for (x, y, z) in sorted(limb_cells):
        if t.v.get((x, y, z), ('',))[0] != WOOD or not free((x, y - 1, z)) or r.random() > P['limb_berries']:
            continue
        for yy in range(y - 1, max(0, y - 1 - r.randint(3, 14)), -1):
            if not free((x, yy, z)):
                break
            t.v[(x, yy, z)] = ('cave_vines_plant_lit' if r.random() < 0.3 else 'cave_vines_plant', 'y')
    # vines on the outer side of rim leaves: air below the leaf and beside it, and no canopy over the vine's cell
    for (x, y, z) in leaves:
        if not t.v.get((x, y, z), ('',))[0].endswith('_leaves') or not free((x, y - 1, z)):
            continue
        dx, dz = x - ccx, z - ccz
        if math.hypot(dx, dz) < R0 * 0.6:
            continue
        out = (1 if dx > 0 else -1, 0) if abs(dx) >= abs(dz) else (0, 1 if dz > 0 else -1)
        vx, vz = x + out[0], z + out[1]
        if not free((vx, y, vz)) or any(not free((vx, y + k, vz)) for k in range(1, 5)) or r.random() > P['vines']:
            continue
        length = y + 1 if r.random() < P['long_vines'] else r.randint(2, 10)
        for yy in range(y, max(-1, y - length), -1):
            if not free((vx, yy, vz)):
                break
            t.v[(vx, yy, vz)] = ('vine', 'y')
    # glow lichen in patches on the bark: on the side of a free cell that touches wood
    surface = {}
    for (x, y, z), (b, _) in t.v.items():
        if b != WOOD:
            continue
        for face, (dx, dy, dz) in FACES.items():
            p = (x + dx, y + dy, z + dz)
            if p[1] >= 0 and free(p):
                surface.setdefault(p, {'west': 'east', 'east': 'west', 'down': 'up', 'up': 'down', 'north': 'south',
                                       'south': 'north'}[face])
    cells = sorted(surface)
    for _ in range(val('lichen')):
        c = r.choice(cells)
        rad = r.uniform(1.5, 3.5)
        for p in cells:
            if abs(p[0] - c[0]) <= rad and abs(p[1] - c[1]) <= rad and abs(p[2] - c[2]) <= rad and \
                    math.dist(p, c) <= rad and free(p) and r.random() < 0.8:
                t.v[p] = ('glow_lichen', surface[p])
    t.crowns = crowns
    t.ground(max(math.hypot(x - 1.5, z - 1.5) for x, _, z in t.v) + 1)
    return t
