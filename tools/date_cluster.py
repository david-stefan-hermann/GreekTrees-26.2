"""The hanging date cluster model (model units, 16 per block), shared by make_dates.py (block models), make_textures.py
(textures and preview), date_concepts.py (the concept sheet) and the hit boxes in DateClusterBlock.

Modelled for facing=south: the palm trunk is on the +z side; the other facings are y rotations in the blockstate,
like vanilla cocoa. Design (the user's pick from art/date_concepts: a mix of B and C): a stalk arches out of the
trunk just under the crown, a fan of long thin strands hangs from it, and the strands are packed with dates like a
heavy bunch of grapes. The ripe cluster hangs about a third of a block below its own block. Every stalk piece,
strand and date is a box at its own angle (the 26.x model format takes any Euler rotation); the stages grow from
small and green to big and brown.

Two faces that lie in the same plane, face the same way and overlap flicker in the game (z-fighting, the
"Texturüberlappungen" of 0.2.0). Dates never share volume with each other; check() also tests every pair of faces
of the whole model for that case and refuses the model otherwise.

python tools/date_cluster.py  checks all stages and prints their element counts and hit boxes.
"""
import math
import random

import numpy as np

# ---------------------------------------------------------------- texture (16x16 per stage)

UV_STALK = (0, 0, 4, 4)
UV_STRAND = (0, 0, 1, 4)
UV_SIDE = [(4 + 2 * k, 0, 6 + 2 * k, 3) for k in range(3)]   # three date shades: side 2x3
UV_END = [(4 + 2 * k, 3, 6 + 2 * k, 5) for k in range(3)]    # and their ends 2x2
# per stage: stalk, stalk shadow, then three date shades as (base, light, dark)
PALETTE = [
    ((150, 172, 72), (118, 140, 52), [((104, 146, 56), (150, 190, 88), (74, 108, 38)),
                                      ((122, 158, 60), (168, 198, 96), (88, 118, 42)),
                                      ((92, 132, 50), (132, 172, 76), (64, 96, 34))]),
    ((214, 150, 52), (176, 116, 38), [((232, 176, 44), (252, 218, 104), (196, 124, 26)),
                                      ((236, 150, 40), (252, 196, 92), (190, 104, 24)),
                                      ((224, 190, 62), (250, 228, 128), (184, 140, 36))]),
    ((206, 138, 56), (164, 104, 40), [((122, 62, 28), (184, 110, 58), (74, 34, 16)),
                                      ((100, 48, 22), (160, 92, 48), (62, 28, 12)),
                                      ((140, 76, 36), (198, 128, 70), (86, 42, 20))]),
]


def stage_texture(stage):
    """RGBA array 16x16x4: stalk swatch, then three date swatches (side above, end below)."""
    stalk, shadow, dates = PALETTE[stage]
    t = np.zeros((16, 16, 4), np.uint8)
    t[0:4, 0:4] = stalk + (255,)
    t[1, 1] = t[3, 2] = t[2, 0] = shadow + (255,)
    for k, (base, light, dark) in enumerate(dates):
        u = 4 + 2 * k
        t[0:3, u:u + 2] = base + (255,)
        t[0, u] = light + (255,)
        t[2, u + 1] = dark + (255,)
        t[3:5, u:u + 2] = dark + (255,)
        t[3, u] = base + (255,)
    return t


# ---------------------------------------------------------------- elements

def rot_x(a):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_y(a):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_z(a):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def euler(x, y, z):
    """The game's element rotation: CuboidRotation uses JOML rotationZYX, i.e. Rz * Ry * Rx."""
    return rot_z(z) @ rot_y(y) @ rot_x(x)


FACES = {'west': (0, -1), 'east': (0, 1), 'down': (1, -1), 'up': (1, 1), 'north': (2, -1), 'south': (2, 1)}


class Element:
    """A box of the model: from/to, Euler rotation (x, y, z degrees) around origin, kind (stalk, strand, date)."""

    def __init__(self, lo, hi, angles=(0, 0, 0), origin=None, kind='stalk', shade=0):
        self.lo = np.round(np.array(lo, float), 3)
        self.hi = np.round(np.array(hi, float), 3)
        self.angles = tuple(round(a, 1) for a in angles)
        self.origin = np.round(np.array(origin if origin is not None else (self.lo + self.hi) / 2, float), 3)
        self.kind = kind
        self.shade = shade

    @property
    def M(self):
        return euler(*self.angles)

    def obb(self):
        c = (self.lo + self.hi) / 2
        return self.M @ (c - self.origin) + self.origin, self.M, (self.hi - self.lo) / 2

    def corners(self):
        pts = np.array([[x, y, z] for x in (self.lo[0], self.hi[0]) for y in (self.lo[1], self.hi[1])
                        for z in (self.lo[2], self.hi[2])])
        return (pts - self.origin) @ self.M.T + self.origin

    def face_polygon(self, name):
        """World normal, plane offset and the four corners of one face."""
        axis, sign = FACES[name]
        pts = self.corners()
        local = np.array([[x, y, z] for x in (self.lo[0], self.hi[0]) for y in (self.lo[1], self.hi[1])
                          for z in (self.lo[2], self.hi[2])])
        bound = self.hi[axis] if sign > 0 else self.lo[axis]
        poly = pts[np.isclose(local[:, axis], bound)]
        n = np.zeros(3)
        n[axis] = sign
        n = self.M @ n
        return n, float(n @ poly[0]), poly

    def uv(self, name):
        if self.kind == 'stalk':
            return UV_STALK
        if self.kind == 'strand':
            return UV_STRAND
        return UV_END[self.shade] if name in ('up', 'down') else UV_SIDE[self.shade]


def obb_overlap(a, b, margin=0.0):
    """Separating axis test for two oriented boxes (centre, axes as columns, half sizes)."""
    ca, ra, ha = a
    cb, rb, hb = b
    t = cb - ca
    axes = [ra[:, i] for i in range(3)] + [rb[:, i] for i in range(3)]
    for i in range(3):
        for j in range(3):
            c = np.cross(ra[:, i], rb[:, j])
            if np.linalg.norm(c) > 1e-6:
                axes.append(c / np.linalg.norm(c))
    for L in axes:
        pa = sum(ha[i] * abs(ra[:, i] @ L) for i in range(3))
        pb = sum(hb[i] * abs(rb[:, i] @ L) for i in range(3))
        if abs(t @ L) > pa + pb + margin:
            return False
    return True


def angles_towards(d):
    """Euler angles (y = 0) that turn the local +y axis onto direction d: Rz(c) Rx(a) (0, 1, 0) = d."""
    d = np.array(d, float) / np.linalg.norm(d)
    return math.degrees(math.asin(max(-1, min(1, d[2])))), 0.0, math.degrees(math.atan2(-d[0], d[1]))


def segment(p0, p1, width, kind='stalk'):
    """A piece from p0 to p1: a box along the local y axis, turned onto the direction. Pieces that point down run
    along local -y, so their unturned box stays inside the model's -16..32 range."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    length = np.linalg.norm(p1 - p0)
    down = p1[1] < p0[1]
    ext = min(width * 0.3, 0.4)
    if down:
        lo = p0 + np.array([-width / 2, -length - ext, -width / 2])
        hi = p0 + np.array([width / 2, ext, width / 2])
        return Element(lo, hi, angles_towards(p0 - p1), origin=p0, kind=kind)
    lo = p0 + np.array([-width / 2, -ext, -width / 2])
    hi = p0 + np.array([width / 2, length + ext, width / 2])
    return Element(lo, hi, angles_towards(p1 - p0), origin=p0, kind=kind)


class Cluster:
    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.stalks = []
        self.dates = []

    def path(self, points, widths, kind='stalk'):
        """Pieces along the points; widths per piece (tapering widths keep the side faces of neighbours apart)."""
        if not isinstance(widths, (list, tuple)):
            widths = [widths] * (len(points) - 1)
        for a, b, w in zip(points, points[1:], widths):
            self.stalks.append(segment(a, b, w, kind))

    def try_date(self, centre, size, tilt_range, lean=(0, 0)):
        r = self.rng
        angles = (lean[0] + r.uniform(-tilt_range, tilt_range), r.uniform(-40, 40),
                  lean[1] + r.uniform(-tilt_range, tilt_range))
        c, s = np.array(centre, float), np.array(size, float)
        e = Element(c - s / 2, c + s / 2, angles, origin=c, kind='date', shade=r.randrange(3))
        pts = e.corners()
        if pts.min() < -15.5 or pts.max() > 31.5 or pts[:, 2].max() > 15.8:
            return False  # outside the model range, or into the trunk
        box = e.obb()
        if any(obb_overlap(box, o.obb(), 0.02) for o in self.dates):
            return False
        self.dates.append(e)
        return True

    def date_near(self, p, size, tilt_range, radius, tries=10, lean=(0, 0)):
        """A date somewhere around p (a point on a strand): the first of a few random spots that is free."""
        for _ in range(tries):
            a = self.rng.uniform(0, 2 * math.pi)
            off = np.array([math.cos(a) * radius, self.rng.uniform(-0.4, 0.4), math.sin(a) * radius])
            if self.try_date(np.array(p) + off, size, tilt_range, lean):
                return True
        return False

    def elements(self):
        return self.stalks + self.dates


# ---------------------------------------------------------------- the model

DATE_SIZE = [(1.25, 2.0, 1.25), (1.6, 2.75, 1.6), (1.85, 3.25, 1.85)]
GROWTH = [0.55, 0.8, 1.0]
ATTACH = np.array([8.0, 13.5, 16.0])
SEED = 41


def grown(p, g):
    return ATTACH + (np.array(p, float) - ATTACH) * g


def build(stage, seed=SEED):
    """Stalk arching out of the trunk, a fan of long strands (the middle ones longest), dense dates along them."""
    g, size = GROWTH[stage], DATE_SIZE[stage]
    c = Cluster(seed + stage)
    arch = [grown(p, g) for p in ((8, 13.5, 16), (8, 14.8, 11.5), (8, 13.5, 7.5), (8, 11, 5.5))]
    c.path(arch, [[1.0, 0.9, 0.8], [1.5, 1.35, 1.2], [2.0, 1.8, 1.6]][stage])
    n = [5, 8, 12][stage]
    strands = []
    for i in range(n):
        k = i / (n - 1)
        start = arch[2] + (arch[3] - arch[2]) * c.rng.uniform(0.2, 1.0) + np.array([c.rng.uniform(-0.6, 0.6), 0, 0])
        d = np.array([(k - 0.5) * 0.9 + c.rng.uniform(-0.1, 0.1), -1, c.rng.uniform(-0.35, 0.15)])
        length = (10 + 7 * (1 - abs(k - 0.5) * 1.6) + c.rng.uniform(-1, 1)) * g
        end = start + d / np.linalg.norm(d) * length
        c.path([start, end], 0.5 + 0.01 * i, kind='strand')  # every strand a hair thicker: no shared planes
        strands.append((start, end, length))
    # first a row of dates down every strand, then the gaps between the strands are filled like a bunch of grapes
    for start, end, length in strands:
        s = 0.12
        while s <= 1.0:
            c.date_near(start + (end - start) * s, size, 15, 1.1, tries=8)
            s += 1.0 / length
    pts = np.array([p for st, en, _ in strands for p in (st, en)])
    lo, hi = pts.min(0) - 1.5, pts.max(0) + 1.5
    target = [16, 32, 50][stage]
    for _ in range(4000):
        if len(c.dates) >= target:
            break
        p = np.array([c.rng.uniform(lo[i], hi[i]) for i in range(3)])
        if min(_distance(p, st, en) for st, en, _ in strands) < 1.7 and p[1] < arch[2][1] - 1:
            c.try_date(p, size, 15)
    return c


def _distance(p, a, b):
    """Distance from p to the segment a-b."""
    ab = b - a
    t = max(0.0, min(1.0, (p - a) @ ab / (ab @ ab)))
    return float(np.linalg.norm(p - (a + ab * t)))


STAGES = [build(s) for s in range(3)]


def bounds(stage):
    """Bounding box of a stage, the cluster's hit box before rotation."""
    pts = np.vstack([e.corners() for e in STAGES[stage].elements()])
    return pts.min(0), pts.max(0)


def _overlap_2d(p, q, n):
    """Do two convex polygons in the same plane (normal n) overlap with some area?"""
    u = np.cross(n, [1, 0, 0] if abs(n[0]) < 0.9 else [0, 1, 0])
    u /= np.linalg.norm(u)
    v = np.cross(n, u)
    P, Q = np.c_[p @ u, p @ v], np.c_[q @ u, q @ v]

    def hull(a):
        c = a.mean(0)
        return a[np.argsort(np.arctan2(a[:, 1] - c[1], a[:, 0] - c[0]))]

    P, Q = hull(P), hull(Q)
    for poly in (P, Q):
        for i in range(len(poly)):
            e = poly[(i + 1) % len(poly)] - poly[i]
            axis = np.array([-e[1], e[0]])
            pa, qa = P @ axis, Q @ axis
            if pa.max() <= qa.min() + 1e-4 or qa.max() <= pa.min() + 1e-4:
                return False
    return True


def check():
    """Problems of the model: coordinates out of the game's range, dates sharing volume, flickering faces."""
    problems = []
    for s, cluster in enumerate(STAGES):
        els = cluster.elements()
        for i, e in enumerate(els):
            if e.lo.min() < -16 or e.hi.max() > 32:
                problems.append(f'stage {s}: element {i} outside -16..32')
        for i, a in enumerate(cluster.dates):
            for b in cluster.dates[i + 1:]:
                if obb_overlap(a.obb(), b.obb()):
                    problems.append(f'stage {s}: two dates overlap')
        faces = [(i, f) + e.face_polygon(f) for i, e in enumerate(els) for f in FACES]
        for x in range(len(faces)):
            i, f, n, off, poly = faces[x]
            for y in range(x + 1, len(faces)):
                j, g, m, off2, poly2 = faces[y]
                if i != j and n @ m > 0.9999 and abs(off - off2) < 1e-3 and _overlap_2d(poly, poly2, n):
                    problems.append(f'stage {s}: elements {i} ({f}) and {j} ({g}) share a face plane')
    return problems


if __name__ == '__main__':
    found = check()
    print('\n'.join(found) if found else 'ok: no overlapping dates, no faces sharing a plane')
    for s in range(3):
        lo, hi = bounds(s)
        print(s, len(STAGES[s].dates), 'dates', len(STAGES[s].elements()), 'elements, bounds',
              np.round(lo, 2), np.round(hi, 2))
