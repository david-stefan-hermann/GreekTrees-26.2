"""Round 5 concept (2026-10-02): the Aries oak (Widdereiche, Quercus arietina), fifth shape, after the user's notes
on the fourth: "der Stamm muss rund sein und organisch, unten breiter und nach oben schmaler werdend, die seitlichen
kronen größer und weiter aus dem baum herausragend", as a full design plus five variations that each push one
feature (VARIANTS).

The design:

- trunk: round, a disc of wood per layer whose radius narrows from the foot to the dome (about 11 wide at the
  ground, 7 at a quarter of the height, 4-5 under the dome). The foot flares out over the first blocks, with four
  or five buttresses that end in short roots. Shallow ridges run up the bark and turn slowly with height, and a few
  burls sit on it. The middle line sways in smooth curves, as in the fourth shape.
- side crowns: five to seven limbs leave the trunk at staggered heights between 40 and 62 % of the height. Each one
  is thick at the trunk and thin at the end, rises out of the trunk, arcs outward and lifts at the tip. It ends in
  a big crown, a cloud of three to five puffs, which sticks out beyond the dome's edge, and carries a smaller puff
  half way.
- main dome: the build's hollow dome of a single leaf, radius 13.5-15, its wall over 80 % of the height, bumpy and
  with an uneven lower edge. Ribs under the shell keep every leaf within six of wood, as in the fourth shape.
- hangings: vines from the dome's rim and the crowns' outer edges (some to the ground, most shorter), glow berries
  from moss blocks in the dome and the crowns.

Grown leaves decay more than six steps from wood, so every puff gets twigs inside it and finish() drops what is
still out of reach.
"""
import math

from trees import TAU, Tree, ip, polar

WOOD = 'dark_oak_wood'

# Each value is a range (uniform between the two) or a fixed number.
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
    roots=(1.5, 2.8),      # how far the roots run out beyond the foot
    # side crowns
    limbs=(5, 7),
    limb_y=(0.40, 0.62),   # heights the limbs leave the trunk at, shares of H
    reach=(1.10, 1.35),    # where the crown's middle lies, a share of the dome's radius
    lift=(4, 7),           # how much the limb climbs on its way out
    limb_r=(1.5, 1.9),     # limb radius at the trunk
    crown=(5.0, 6.2),      # crown radius
    crown_h=(3.0, 3.6),    # crown half height
    puffs=(3, 5),
    crown_erode=0.35,
    mid_puff=True,
    # main dome
    R=(13.5, 15.0),
    wall=0.80,             # where the dome's wall starts, a share of H
    cap=0,                 # extra height of the cap above the trunk
    bumps=(0.04, 0.08),
    # hangings and colour
    vines=0.25,            # chance a rim leaf gets a vine
    long_vines=0.35,       # chance a vine runs to the ground (or onto what is below)
    moss=0.02,
    berries=0.09,          # glow berries on a cave vine
    flowering=0.32,
    forks=0,               # side branches per limb, each with a small crown (variation "Geäst")
)

VARIANTS = [
    ('design', 'Entwurf', 'alles ausgewogen', {}),
    ('trunk', '1  Stamm', 'breiter Fuß, starke Verjüngung, kräftiger Schwung, gedrehte Rippen, Knollen', dict(
        r_base=(7.0, 7.6), r_mid=(4.2, 4.6), r_top=(2.2, 2.5), flare=(9, 11), buttress=0.38, ridges=0.15,
        twist=0.07, sway=(2.8, 3.6), burls=(7, 10), roots=(2.0, 3.0), vines=0.1)),
    ('dome', '2  Hauptkuppel', 'größer, höher, beuliger; die Seitenkronen nur knapp darunter hervor', dict(
        R=(17.0, 18.0), wall=0.72, cap=4, bumps=(0.07, 0.11), reach=(0.95, 1.12), crown=(4.6, 5.4))),
    ('crowns', '3  Seitenkronen', 'mehr, längere Äste, riesige Kronen weit draußen, in zwei Etagen', dict(
        limbs=(8, 9), limb_y=(0.34, 0.64), reach=(1.35, 1.65), crown=(6.4, 7.4), crown_h=(3.4, 4.2),
        puffs=(4, 6), limb_r=(1.8, 2.2), lift=(5, 9), R=(12.5, 13.5))),
    ('limbs', '4  Geäst', 'lockere Kronen, die geschwungenen Äste zeigen sich und gabeln sich', dict(
        limbs=(7, 8), crown=(3.2, 3.8), crown_h=(2.2, 2.6), puffs=(2, 3), crown_erode=0.6, mid_puff=False,
        forks=2, limb_r=(1.8, 2.2), lift=(6, 10), vines=0.08)),
    ('vines', '5  Ranken & Leuchtbeeren', 'dichter Rankenvorhang, viel Moos mit Leuchtbeeren', dict(
        vines=0.85, long_vines=0.7, moss=0.09, berries=0.3)),
]


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

    top = H + P['cap']
    for y in range(top):
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

    def crown(c, rad, half, puffs, erode):
        """A cloud of puffs round c, flat underneath, with twigs from c into every puff."""
        cx, cy, cz = c
        # a wide puff in the middle, a higher one on top of it (the crown arches), smaller ones round the rim
        spots = [(cx, cy, cz, rad, half), (cx + r.uniform(-1, 1), cy + half * 0.9, cz + r.uniform(-1, 1),
                                           rad * r.uniform(0.55, 0.7), half * 0.8)]
        a0 = r.uniform(0, TAU)
        for i in range(puffs - 1):
            a = a0 + i * TAU / (puffs - 1) + r.uniform(-0.4, 0.4)
            d = rad * r.uniform(0.5, 0.8)
            spots.append((cx + math.cos(a) * d, cy + r.uniform(-1.2, 1.5), cz + math.sin(a) * d,
                          rad * r.uniform(0.5, 0.7), half * r.uniform(0.75, 1.0)))
        for x, y, z, s, h in spots:
            t.path([(cx, cy - 1, cz), (x, y - 0.5, z)], WOOD)
            for k in range(3):  # twigs out towards the puff's rim
                a = r.uniform(0, TAU)
                t.path([(x, y - 0.5, z), (x + math.cos(a) * s * 0.55, y, z + math.sin(a) * s * 0.55)], WOOD)
        for x, y, z, s, h in spots:
            t.blob((x, y + 0.6, z), s, h, s, leaf, erode=erode, floor=round(y - h * 0.7))

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
    crown_cells = []
    for i in range(n):
        a = a0 + i * TAU / n + r.uniform(-0.2, 0.2)
        y = round(H * heights[i])
        cx, cz = centre(y)
        rt = radius_at(y, a)
        D = R0 * val('reach')
        lift = val('lift')
        drift = r.uniform(-0.35, 0.35)
        start = (cx + math.cos(a) * (rt - 0.8), y, cz + math.sin(a) * (rt - 0.8))
        # rises out of the trunk, arcs outward, lifts again at the tip
        p1 = (cx + math.cos(a) * D * 0.3, y + lift * 0.7, cz + math.sin(a) * D * 0.3)
        p2 = (cx + math.cos(a + drift) * D * 0.7, y + lift * 0.6, cz + math.sin(a + drift) * D * 0.7)
        tip = (cx + math.cos(a + drift * 0.6) * D, y + lift, cz + math.sin(a + drift * 0.6) * D)
        line = tube([start, p1, p2, tip], val('limb_r'), 0.4)
        before = set(t.v)
        crown((tip[0], tip[1] + 1, tip[2]), val('crown'), val('crown_h'), val('puffs'), P['crown_erode'])
        if P['mid_puff']:
            mx, my, mz = line[len(line) // 2]
            t.blob((mx, my + 1.6, mz), 2.8, 2.0, 2.8, leaf, erode=0.4, floor=round(my))
        for _ in range(P['forks']):
            px, py, pz = line[r.randint(len(line) // 3, 2 * len(line) // 3)]
            fa = a + drift + r.choice((-1, 1)) * r.uniform(0.6, 1.1)
            fl = D * r.uniform(0.3, 0.45)
            ftip = (px + math.cos(fa) * fl, py + r.uniform(2, 5), pz + math.sin(fa) * fl)
            tube([(px, py, pz), (px + math.cos(fa) * fl * 0.5, py + 0.5, pz + math.sin(fa) * fl * 0.5), ftip],
                 0.9, 0.4)
            crown((ftip[0], ftip[1] + 1, ftip[2]), val('crown') * 0.7, val('crown_h') * 0.8, 2, P['crown_erode'])
        crown_cells += [p for p in set(t.v) - before]

    # ------------------------------------------------------------------------------------------------ dome
    bumps = [(val('bumps'), k, r.uniform(0, TAU)) for k in (2, 3, 5)]
    edge = (r.uniform(0.8, 2.0), r.randint(2, 3), r.uniform(0, TAU))  # how much lower the wall hangs, and where
    wall_top = y2 + r.randint(2, 3)
    dome_top = top + 1
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

    ribs = max(12, round(R0 * 0.9))
    a0 = r.uniform(0, TAU)
    for i in range(ribs):
        a = a0 + i * TAU / ribs + r.uniform(-0.08, 0.08)
        y = y2 - 3 + r.randint(-1, 1)
        cx, cz = centre(y)
        rt = radius_at(y, a)
        foot = (ccx + math.cos(a) * (wall_r(a) - 2.0), y2 - 1, ccz + math.sin(a) * (wall_r(a) - 2.0))
        kink = a + r.uniform(-0.25, 0.25)
        tube([(cx + math.cos(a) * (rt - 0.5), y - 1, cz + math.sin(a) * (rt - 0.5)),
              (cx + math.cos(kink) * wall_r(a) * 0.5, y + 1.5, cz + math.sin(kink) * wall_r(a) * 0.5), foot], 1.1, 0.4)
        prev = foot
        for yy in range(y2, dome_top):
            rr = shell_r(yy + 1, a) - 1.6  # under the shell of this layer and the one above, so the shell hides it
            if rr < 2.5:
                break
            nxt = (ccx + math.cos(a) * rr, yy, ccz + math.sin(a) * rr)
            before = set(t.v)
            t.path([prev, nxt], WOOD, 'y')
            # leaves round the rib reach out to the shell a block further out, so the shell is fed from it
            for (bx, by, bz) in set(t.v) - before:
                for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    t.leaf((bx + dx, by, bz + dz), leaf)
            prev = nxt
    moss = []
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
                else:
                    t.leaf((x, y, z), leaf)
    t.finish()  # leaves out of reach of wood go; what hangs is placed on what is left

    # ------------------------------------------------------------------------------------------------ hangings
    def free(p):
        return p not in t.v

    leaves = [p for p, (b, _) in t.v.items() if b.endswith('_leaves')]
    # moss under the canopies: a leaf with air below may turn into moss and grow glow berries
    for p in leaves:
        x, y, z = p
        if free((x, y - 1, z)) and r.random() < P['moss']:
            t.put(p, 'moss_block')
            moss.append(p)
    for p, (b, _) in t.v.items():
        if b == 'moss_block' and p not in moss and free((p[0], p[1] - 1, p[2])):
            moss.append(p)
    for (x, y, z) in moss:
        length = r.randint(3, max(3, min(24, y - 2)))
        for yy in range(y - 1, max(0, y - 1 - length), -1):
            if not free((x, yy, z)):
                break
            t.v[(x, yy, z)] = ('cave_vines_plant_lit' if r.random() < P['berries'] else 'cave_vines_plant', 'y')
    # vines on the outer side of rim leaves (those with air below and outside), hanging down
    for (x, y, z) in leaves:
        if (x, y, z) not in t.v or not t.v[(x, y, z)][0].endswith('_leaves') or not free((x, y - 1, z)):
            continue
        dx, dz = x - ccx, z - ccz
        if math.hypot(dx, dz) < R0 * 0.6:
            continue
        out = (1 if dx > 0 else -1, 0) if abs(dx) >= abs(dz) else (0, 1 if dz > 0 else -1)
        vx, vz = x + out[0], z + out[1]
        if not free((vx, y, vz)) or r.random() > P['vines']:
            continue
        length = y + 1 if r.random() < P['long_vines'] else r.randint(2, 10)
        for yy in range(y, max(-1, y - length), -1):
            if not free((vx, yy, vz)):
                break
            t.v[(vx, yy, vz)] = ('vine', 'y')
    t.ground(max(math.hypot(x - 1.5, z - 1.5) for x, _, z in t.v) + 1)
    return t
