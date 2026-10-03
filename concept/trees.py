"""Procedural concept generators for Greek trees, vanilla blocks only.

Round 1 archive: helpers plus the species that were not picked. The five picked species live in species.py.

Every generator takes a seed and returns a Tree whose voxels dict maps (x, y, z) -> (block, axis). y = 0 is the
first block above the ground; the trunk base sits at x = z = 0. The shapes are meant to be ported to Java features
later, so they stay rule based (heights, radii, branch counts) rather than hand placed.

A block argument may be a name or a zero-argument function returning a name (mottled bark, mixed leaves).
"""
import math
import random

from voxel import decay_report, is_log

TAU = math.tau
CARDINALS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def ip(p):
    return tuple(math.floor(c + 0.5) for c in p)


def polar(angle, r):
    return math.cos(angle) * r, math.sin(angle) * r


class Tree:
    def __init__(self, seed):
        self.v = {}
        self.rng = seed if isinstance(seed, random.Random) else random.Random(seed)
        self.notes = []  # annotations for the anatomy figures, world coordinates

    @staticmethod
    def _name(block):
        return block() if callable(block) else block

    # -- placement -------------------------------------------------------------------------------------------
    def log(self, p, block, axis='y'):
        p = ip(p)
        old = self.v.get(p)
        if old is None or not is_log(old[0]):
            self.v[p] = (self._name(block), axis)
        elif axis == 'y' and old[1] != 'y':
            self.v[p] = (old[0], 'y')

    def leaf(self, p, block):
        p = ip(p)
        if p not in self.v:
            self.v[p] = (self._name(block), 'y')

    def put(self, p, block):
        self.v[ip(p)] = (self._name(block), 'y')

    def branch(self, a, b, block, axis=None):
        """Face-connected log line from a to b. Axis follows the dominant direction unless given."""
        d = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        if axis is None:
            axis = 'xyz'[max(range(3), key=lambda i: abs(d[i]))]
        return self._line(a, b, lambda p: self.log(p, block, axis))

    def leaf_line(self, a, b, block):
        return self._line(a, b, lambda p: self.leaf(p, block))

    @staticmethod
    def _line(a, b, put):
        d = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        steps = max(1, int(math.ceil(max(abs(c) for c in d) * 3)))
        prev = None
        for i in range(steps + 1):
            t = i / steps
            p = ip((a[0] + d[0] * t, a[1] + d[1] * t, a[2] + d[2] * t))
            if prev is not None and p != prev:
                cur = list(prev)
                for k in (1, 0, 2):  # fill diagonal moves so the chain stays face connected
                    if cur[k] != p[k]:
                        cur[k] = p[k]
                        if tuple(cur) != p:
                            put(tuple(cur))
            put(p)
            prev = p
        return prev

    def stem(self, points, block):
        """Log line that steps diagonally like a vanilla acacia, without filler blocks: bends stay one block thick.
        Leaf decay does not care whether logs touch each other, only how far leaves are from any log."""
        for a, b in zip(points, points[1:]):
            d = [b[i] - a[i] for i in range(3)]
            n = max(1, math.ceil(max(abs(c) for c in d)))
            for i in range(n + 1):
                self.log((a[0] + d[0] * i / n, a[1] + d[1] * i / n, a[2] + d[2] * i / n), block)

    def path(self, points, block, axis=None):
        for a, b in zip(points, points[1:]):
            self.branch(a, b, block, axis)

    def blob(self, c, rx, ry, rz, block, erode=0.15, floor=None, ceil=None, hollow=None):
        """Ellipsoid of leaves. erode removes random rim blocks, floor/ceil cut by y level,
        hollow=(r, ytop) keeps a cylinder of radius r around the trunk axis free below ytop."""
        cx, cy, cz = c
        for x in range(math.floor(cx - rx), math.ceil(cx + rx) + 1):
            for y in range(math.floor(cy - ry), math.ceil(cy + ry) + 1):
                if (floor is not None and y < floor) or (ceil is not None and y > ceil):
                    continue
                for z in range(math.floor(cz - rz), math.ceil(cz + rz) + 1):
                    d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + ((z - cz) / rz) ** 2
                    if d > 1:
                        continue
                    if hollow and y < hollow[1] and x * x + z * z < hollow[0] ** 2:
                        continue
                    if d > 0.5 and self.rng.random() < erode * (d - 0.35) * 2:
                        continue
                    self.leaf((x, y, z), block)

    # -- surroundings ----------------------------------------------------------------------------------------
    def ground(self, radius, top='grass_block', patches=(('coarse_dirt', 0.12),)):
        rng = random.Random(7)
        r = int(math.ceil(radius))
        for x in range(-r, r + 1):
            for z in range(-r, r + 1):
                if x * x + z * z > radius * radius:
                    continue
                b = top
                roll = rng.random()
                for name, p in patches:
                    if roll < p:
                        b = name
                        break
                    roll -= p
                self.v[(x, -1, z)] = (b, 'y')

    def scatter(self, radius, block, chance, rng_seed=11):
        """Carpets (petals, leaf litter) on free ground cells."""
        rng = random.Random(rng_seed)
        r = int(math.ceil(radius))
        for x in range(-r, r + 1):
            for z in range(-r, r + 1):
                if x * x + z * z <= radius * radius and (x, 0, z) not in self.v and rng.random() < chance:
                    self.v[(x, 0, z)] = (block, 'y')

    def finish(self):
        """Branches show bark all round: sideways logs become wood, and so do trunk logs whose open top
        would show rings where the trunk steps sideways."""
        for p, (b, axis) in list(self.v.items()):
            if not b.endswith('_log'):
                continue
            wood = b[:-4] + '_wood'
            if axis != 'y':
                self.v[p] = (wood, 'y')
                continue
            x, y, z = p
            above = self.v.get((x, y + 1, z))
            if above is None or not is_log(above[0]):
                stepped = any(is_log(self.v.get((x + dx, y + 1, z + dz), ('', ''))[0])
                              for dx in (-1, 0, 1) for dz in (-1, 0, 1) if dx or dz)
                if stepped:
                    self.v[p] = (wood, 'y')
        # Leaves the game would let decay (distance 7) are never placed; the Java feature can do the same pass.
        self.pruned = decay_report(self.v)
        for p in self.pruned:
            del self.v[p]
        return self

    def extent(self):
        pts = [p for p in self.v if p[1] >= 0]
        xs = [p[0] for p in pts]
        zs = [p[2] for p in pts]
        return min(xs), max(xs), min(zs), max(zs), max(p[1] for p in pts)


def lerp_path(points, y):
    """x, z of a polyline at height y (points sorted by y)."""
    for a, b in zip(points, points[1:]):
        if a[1] <= y <= b[1]:
            t = 0 if b[1] == a[1] else (y - a[1]) / (b[1] - a[1])
            return a[0] + (b[0] - a[0]) * t, a[2] + (b[2] - a[2]) * t
    return points[-1][0], points[-1][2]


# ==================================================================================== new: stone pine

def stone_pine(seed):
    """Pinus pinea (Schirmpinie): tall bare trunk, slightly leaning, splitting high up into a flat umbrella."""
    t = Tree(seed)
    r = t.rng
    LOG, LEAF = 'spruce_log', 'spruce_leaves'
    h = r.randint(11, 14)
    lx, lz = polar(r.uniform(0, TAU), r.uniform(0.8, 1.6))
    trunk = [(0, 0, 0), (lx * 0.25, h * 0.55, lz * 0.25), (lx, h, lz)]
    t.path(trunk, LOG, 'y')
    n = r.randint(5, 7)
    a0 = r.uniform(0, TAU)
    tips = []
    for i in range(n):
        ang = a0 + i * TAU / n + r.uniform(-0.25, 0.25)
        y0 = h - r.randint(1, 3)
        sx, sz = lerp_path(trunk, y0)
        ex, ez = polar(ang, r.uniform(3.2, 4.6))
        tip = (sx + ex, y0 + r.randint(1, 2), sz + ez)
        t.branch((sx, y0, sz), tip, LOG)
        tips.append(tip)
    for (x, y, z) in tips:
        t.blob((x, y + 0.9, z), r.uniform(2.6, 3.2), 1.35, r.uniform(2.6, 3.2), LEAF, erode=0.3, floor=round(y))
    t.blob((lx, h + 1, lz), 3.6, 1.4, 3.6, LEAF, erode=0.2, floor=h)
    t.ground(7)
    return t


# ==================================================================================== new: Aleppo pine

def aleppo_pine(seed):
    """Pinus halepensis (Aleppo-Kiefer): leaning, kinked trunk, crown broken into separate cloud pads."""
    t = Tree(seed)
    r = t.rng
    LOG, LEAF = 'spruce_log', 'acacia_leaves'
    h = r.randint(10, 13)
    ang = r.uniform(0, TAU)
    lx, lz = polar(ang, r.uniform(3.0, 4.0))
    px, pz = polar(ang + TAU / 4, 1.0)
    trunk = [(0, 0, 0), (lx * 0.15 + px, h * 0.35, lz * 0.15 + pz), (lx * 0.6 - px * 0.6, h * 0.7, lz * 0.6 - pz * 0.6),
             (lx, h, lz)]
    t.path(trunk, LOG, 'y')
    pads = [((lx, h, lz), 3.0, 1.2)]
    for i in range(r.randint(3, 4)):
        y0 = int(h * r.uniform(0.45, 0.85))
        sx, sz = lerp_path(trunk, y0)
        bang = ang + r.choice([-1, 1]) * r.uniform(0.9, 2.4)
        ex, ez = polar(bang, r.uniform(2.5, 4.0))
        tip = (sx + ex, y0 + r.randint(1, 2), sz + ez)
        t.branch((sx, y0, sz), tip, LOG)
        pads.append((tip, r.uniform(2.0, 2.7), 1.0))
    for (x, y, z), rad, ry in pads:
        t.blob((x, y + 0.7, z), rad, ry, rad, LEAF, erode=0.4, floor=round(y))
    t.ground(6)
    return t


# ==================================================================================== new: oriental plane

def plane(seed):
    """Platanus orientalis (Platane): the giant of the village square. 2x2 mottled trunk with root flare,
    thick limbs, huge dome. Mottled bark = pale oak wood mixed with stripped pale oak and stripped birch."""
    t = Tree(seed)
    r = t.rng

    def bark():
        x = r.random()
        return 'stripped_pale_oak_wood' if x < 0.55 else 'stripped_birch_wood' if x < 0.85 else 'pale_oak_wood'

    LEAF = 'jungle_leaves'
    th = r.randint(5, 6)
    for y in range(th + 1):
        for x in (0, 1):
            for z in (0, 1):
                t.log((x, y, z), bark)
    for x, z in ((-1, 0), (-1, 1), (2, 0), (2, 1), (0, -1), (1, -1), (0, 2), (1, 2)):
        if r.random() < 0.6:
            t.log((x, 0, z), bark)
    for dx, dz in r.sample(CARDINALS, 3):
        bx, bz = (2 if dx > 0 else -1 if dx < 0 else r.randint(0, 1)), (2 if dz > 0 else -1 if dz < 0 else r.randint(0, 1))
        t.log((bx + dx, 0, bz + dz), bark, 'x' if dx else 'z')
    c = (0.5, th, 0.5)
    n = r.randint(4, 5)
    a0 = r.uniform(0, TAU)
    tips = []
    for i in range(n):
        ang = a0 + i * TAU / n + r.uniform(-0.3, 0.3)
        ex, ez = polar(ang, r.uniform(5.0, 6.5))
        mid = (c[0] + ex * 0.45, th + r.randint(2, 3), c[2] + ez * 0.45)
        tip = (c[0] + ex, th + r.randint(4, 6), c[2] + ez)
        t.branch(c, mid, bark)
        t.branch(mid, tip, bark)
        tips.append((tip, r.uniform(3.4, 3.9), 2.3))
        for side in (-1, 1):  # twigs into the crown so every leaf stays within reach of wood
            sx, sz = polar(ang + side * r.uniform(0.7, 1.1), 2.5)
            sub = (mid[0] + sx, mid[1] + r.randint(2, 4), mid[2] + sz)
            t.branch(mid, sub, bark)
            tips.append((sub, r.uniform(2.6, 3.0), 2.0))
    top_y = max(p[0][1] for p in tips)
    t.branch(c, (c[0], top_y, c[2]), bark, 'y')
    for (x, y, z), rad, ry in tips:
        t.blob((x, y + 0.5, z), rad, ry, rad, LEAF, erode=0.3, floor=th + 2)
    t.blob((c[0], top_y + 1.2, c[2]), 3.6, 2.2, 3.6, LEAF, erode=0.3)
    t.ground(10)
    return t


# ==================================================================================== new: almond in blossom

def almond(seed):
    """Prunus dulcis (Mandelbaum): small vase-shaped tree, airy crown in pale pink blossom, petals below."""
    t = Tree(seed)
    r = t.rng
    LOG, LEAF = 'cherry_log', 'cherry_leaves'
    th = r.randint(2, 3)
    for y in range(th + 1):
        t.log((0, y, 0), LOG)
    n = r.randint(3, 4)
    a0 = r.uniform(0, TAU)
    tips = []
    for i in range(n):
        ang = a0 + i * TAU / n + r.uniform(-0.3, 0.3)
        ex, ez = polar(ang, r.uniform(2.2, 3.0))
        tip = (ex, th + r.randint(3, 4), ez)
        t.branch((0, th, 0), tip, LOG, 'y')
        sx, sz = polar(ang + r.choice([-1, 1]) * 0.5, 1.4)
        tip2 = (ex + sx, tip[1] + 1, ez + sz)
        t.branch(tip, tip2, LOG)
        tips.append(tip2)
    for (x, y, z) in tips:
        t.blob((x, y + 0.3, z), r.uniform(2.1, 2.5), 1.6, r.uniform(2.1, 2.5), LEAF, erode=0.45, floor=th + 2)
    t.ground(5.5)
    t.scatter(4.5, 'pink_petals', 0.35)
    return t


# ==================================================================================== new: oleander

def oleander(seed):
    """Nerium oleander: multi-stemmed shrub tree, pink flowers. Flowering azalea leaves over azalea leaves."""
    t = Tree(seed)
    r = t.rng
    LOG = 'jungle_log'

    def leaf():
        return 'flowering_azalea_leaves' if r.random() < 0.7 else 'azalea_leaves'

    n = r.randint(2, 3)
    a0 = r.uniform(0, TAU)
    tops = []
    for i in range(n):
        dx, dz = polar(a0 + i * TAU / n, 1.0)
        top = (dx, r.randint(1, 2), dz)
        t.branch((0, 0, 0), top, LOG, 'y')
        tops.append(top)
    t.blob((0, 2.4, 0), r.uniform(2.2, 2.6), 1.7, r.uniform(2.2, 2.6), leaf, erode=0.3, floor=1)
    for (x, y, z) in tops:
        t.blob((x * 1.3, y + 1.2, z * 1.3), 1.6, 1.3, 1.6, leaf, erode=0.35, floor=1)
    t.ground(3.5)
    return t


# ==================================================================================== new: carob

def carob(seed):
    """Ceratonia siliqua (Johannisbrotbaum): short dark trunk, very dense dark dome that almost reaches the ground."""
    t = Tree(seed)
    r = t.rng
    LOG, LEAF = 'dark_oak_log', 'dark_oak_leaves'
    th = r.randint(2, 3)
    for y in range(th + 1):
        t.log((0, y, 0), LOG)
    t.log((1, 0, 0), LOG)
    n = r.randint(4, 5)
    a0 = r.uniform(0, TAU)
    tips = []
    for i in range(n):
        ang = a0 + i * TAU / n + r.uniform(-0.3, 0.3)
        ex, ez = polar(ang, r.uniform(2.0, 2.8))
        tip = (ex, th + r.randint(1, 3), ez)
        t.branch((0, th, 0), tip, LOG)
        tips.append(tip)
    t.blob((0, th + 2.2, 0), r.uniform(4.2, 4.7), 3.3, r.uniform(4.2, 4.7), LEAF, erode=0.12, floor=1, hollow=(2.2, th))
    for (x, y, z) in tips:
        t.blob((x * 1.3, y + 1.0, z * 1.3), 2.3, 1.8, 2.3, LEAF, erode=0.3)
    t.ground(6)
    return t


ALL = ['stone_pine', 'aleppo_pine', 'plane', 'almond', 'oleander', 'carob']
