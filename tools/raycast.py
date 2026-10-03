"""Small ray caster for block models: boxes in model units (16 per block), each with an optional rotation (as in
the game's model format, around an origin) and a texture region per face. Orthographic camera, the game's face
shading, cut-out textures (leaves). Used for the date cluster concepts (tools/date_concepts.py)."""
import math

import numpy as np
from PIL import Image

FACE_NAMES = (('west', 'east'), ('down', 'up'), ('north', 'south'))


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
    """The game's Euler rotation of a model element ("rotation": {"x", "y", "z"} in degrees): CuboidRotation builds
    it with JOML rotationZYX, i.e. Rz * Ry * Rx, so a vector is turned about x first, then y, then z."""
    return rot_z(z) @ rot_y(y) @ rot_x(x)


class Box:
    """lo/hi: element from/to; faces: {name: (texture array HxWx4, (u1, v1, u2, v2))}, a missing face is not drawn;
    rot: 3x3 matrix around origin; offset: where the block sits (model units)."""

    def __init__(self, lo, hi, faces, rot=None, origin=(8, 8, 8), offset=(0, 0, 0)):
        self.lo = np.array(lo, float)
        self.hi = np.array(hi, float)
        self.faces = faces
        self.M = np.eye(3) if rot is None else np.array(rot, float)
        self.origin = np.array(origin, float)
        self.offset = np.array(offset, float)

    def turned(self, R, origin):
        """The same box with a block rotation R around origin applied after its own (like a blockstate y)."""
        b = Box(self.lo, self.hi, self.faces)
        # world = R (M (p - o) + o - O) + O + offset
        b.M = R @ self.M
        b.origin = self.origin
        b.offset = self.offset + (R @ (self.origin - origin) + origin - self.origin)
        return b


def _uv(face, p, lo, hi):
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    sx = (x - lo[0]) / max(hi[0] - lo[0], 1e-6)
    sy = (hi[1] - y) / max(hi[1] - lo[1], 1e-6)
    sz = (z - lo[2]) / max(hi[2] - lo[2], 1e-6)
    return {
        'north': (1 - sx, sy), 'south': (sx, sy), 'west': (sz, sy), 'east': (1 - sz, sy),
        'up': (sx, sz), 'down': (sx, 1 - sz),
    }[face]


def render(boxes, direction, center, scale, size, bg_top=(118, 168, 222), bg_bottom=(196, 222, 240)):
    """Orthographic view along direction (from the camera into the scene) centred on center, scale pixels per
    model unit, size (w, h)."""
    w, h = size
    d = np.array(direction, float)
    d /= np.linalg.norm(d)
    right = np.cross(d, [0, 1, 0])
    right /= np.linalg.norm(right)
    up = np.cross(right, d)
    jj, ii = np.mgrid[0:h, 0:w]
    plane = (np.array(center, float)[None, :]
             + ((ii.ravel() - w / 2 + 0.5) / scale)[:, None] * right[None, :]
             - ((jj.ravel() - h / 2 + 0.5) / scale)[:, None] * up[None, :])
    origin = plane - d[None, :] * 1000
    depth = np.full(w * h, np.inf)
    colour = np.zeros((w * h, 3))
    for b in boxes:
        ol = (origin - b.origin - b.offset) @ b.M + b.origin
        dl = d @ b.M
        dl = np.where(np.abs(dl) < 1e-9, 1e-9, dl)
        t1 = (b.lo[None, :] - ol) / dl
        t2 = (b.hi[None, :] - ol) / dl
        tmin, tmax = np.minimum(t1, t2), np.maximum(t1, t2)
        tnear, tfar = tmin.max(1), tmax.min(1)
        hit = (tnear <= tfar) & (tfar > 0) & (tnear < depth)
        if not hit.any():
            continue
        idx = np.nonzero(hit)[0]
        axis = tmin[idx].argmax(1)
        p = ol[idx] + tnear[idx, None] * dl[None, :]
        for a in range(3):
            face = FACE_NAMES[a][0 if dl[a] > 0 else 1]
            sel = axis == a
            if not sel.any() or face not in b.faces:
                continue
            tex, (u1, v1, u2, v2) = b.faces[face]
            s, t = _uv(face, p[sel], b.lo, b.hi)
            u = u1 + np.clip(s, 0, 0.9999) * (u2 - u1)
            v = v1 + np.clip(t, 0, 0.9999) * (v2 - v1)
            th, tw = tex.shape[:2]
            px = tex[np.clip((v * th / 16).astype(int), 0, th - 1), np.clip((u * tw / 16).astype(int), 0, tw - 1)]
            opaque = px[:, 3] > 0
            n = np.zeros(3)
            n[a] = -1 if dl[a] > 0 else 1
            nw = b.M @ n
            shade = min(nw[0] ** 2 * 0.6 + nw[1] ** 2 * (3 + nw[1]) / 4 + nw[2] ** 2 * 0.8, 1.0)
            target = idx[sel][opaque]
            colour[target] = px[opaque, :3] * shade
            depth[target] = tnear[target]
    sky = np.linspace(0, 1, h)[:, None, None] * (np.array(bg_bottom) - np.array(bg_top))[None, None, :] + np.array(bg_top)
    img = np.broadcast_to(sky, (h, w, 3)).copy().reshape(-1, 3)
    drawn = np.isfinite(depth)
    img[drawn] = colour[drawn]
    return Image.fromarray(img.reshape(h, w, 3).clip(0, 255).astype(np.uint8), 'RGB')


def corners(box):
    pts = np.array([[x, y, z] for x in (box.lo[0], box.hi[0]) for y in (box.lo[1], box.hi[1])
                    for z in (box.lo[2], box.hi[2])])
    return (pts - box.origin) @ box.M.T + box.origin + box.offset


def fit(boxes, direction, size, margin=1.15):
    """Centre and scale so that the boxes fill the picture."""
    d = np.array(direction, float)
    d /= np.linalg.norm(d)
    right = np.cross(d, [0, 1, 0])
    right /= np.linalg.norm(right)
    up = np.cross(right, d)
    pts = np.vstack([corners(b) for b in boxes])
    r, u = pts @ right, pts @ up
    centre = pts.mean(0)
    centre += right * ((r.max() + r.min()) / 2 - centre @ right) + up * ((u.max() + u.min()) / 2 - centre @ up)
    scale = min(size[0] / ((r.max() - r.min()) * margin), size[1] / ((u.max() - u.min()) * margin))
    return centre, scale


def full_block(texture, offset):
    """A whole block with one texture on every face, at block offset (in blocks)."""
    faces = {f: (texture, (0, 0, 16, 16)) for pair in FACE_NAMES for f in pair}
    return Box((0, 0, 0), (16, 16, 16), faces, offset=np.array(offset, float) * 16)
