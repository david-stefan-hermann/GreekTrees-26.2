"""Tiny isometric voxel renderer that draws vanilla block textures straight from the 26.2 client jar.

Concept-art only: a tree is a dict {(x, y, z): (block, axis)} and render() turns it into a PNG that looks close
to the game with fancy leaves. Visible faces are top, east (+x) and south (+z); blocks are painted back to front.
"""
import io
import os
import zipfile
from collections import deque

from PIL import Image, ImageDraw, ImageFont

JAR = os.path.expanduser('~/.gradle/caches/fabric-loom/26.2/minecraft-client.jar')
_zip = zipfile.ZipFile(JAR)

A, H, V = 16, 8, 18  # half width of a block, half rise of its top, height of its side (pixels)

SHADE = {'top': 1.0, 'south': 0.8, 'east': 0.6}


def _png(path):
    im = Image.open(io.BytesIO(_zip.read(path))).convert('RGBA')
    if im.height > im.width:  # animated strip: first frame
        im = im.crop((0, 0, im.width, im.width))
    return im


def block_tex(name):
    return _png(f'assets/minecraft/textures/block/{name}.png')


def _colormap(name, temp, downfall):
    cm = _png(f'assets/minecraft/textures/colormap/{name}.png')
    temp = max(0.0, min(1.0, temp))
    downfall = max(0.0, min(1.0, downfall)) * temp
    x = int((1 - temp) * 255)
    y = int((1 - downfall) * 255)
    return cm.getpixel((x, y))[:3]


# Plains climate (temperature 0.8, downfall 0.4), the tint most of the Greek build sits in.
FOLIAGE = _colormap('foliage', 0.8, 0.4)
GRASS = _colormap('grass', 0.8, 0.4)
DRY_FOLIAGE = _colormap('dry_foliage', 0.8, 0.4)
FIXED_TINT = {'birch_leaves': (0x80, 0xA7, 0x55), 'spruce_leaves': (0x61, 0x99, 0x61)}
FOLIAGE_TINTED = {'oak_leaves', 'jungle_leaves', 'acacia_leaves', 'dark_oak_leaves', 'mangrove_leaves', 'vine'}


def _tint(im, rgb):
    r, g, b, a = im.split()
    r = r.point(lambda v: v * rgb[0] // 255)
    g = g.point(lambda v: v * rgb[1] // 255)
    b = b.point(lambda v: v * rgb[2] // 255)
    return Image.merge('RGBA', (r, g, b, a))


def _shade(im, f):
    if f >= 0.999:
        return im
    r, g, b, a = im.split()
    lut = [min(255, int(v * f)) for v in range(256)]
    return Image.merge('RGBA', (r.point(lut), g.point(lut), b.point(lut), a))


BOX_BLOCKS = {
    # name: (x0, y0, z0, w, h, d) inside the cell, colour (or a list of such pairs); drawn as flat shaded boxes
    'cocoa': ((0.25, 0.2, 0.25, 0.5, 0.6, 0.5), (156, 92, 40)),
    'date_cluster': ((0.15, -0.45, 0.1, 0.75, 1.4, 0.8), (150, 84, 34)),
    'olive_twig': ((0.25, 0.25, 0.25, 0.5, 0.75, 0.5), (62, 44, 74)),
    'arbutus_twig': ((0.25, 0.25, 0.25, 0.5, 0.75, 0.5), (200, 40, 30)),
    'fig_twig': ((0.25, 0.25, 0.25, 0.5, 0.75, 0.5), (110, 56, 96)),
    'mulberry_twig': ((0.25, 0.25, 0.25, 0.5, 0.75, 0.5), (48, 18, 44)),
    'black_mulberry_twig': ((0.25, 0.25, 0.25, 0.5, 0.75, 0.5), (48, 18, 44)),
    'white_mulberry_twig': ((0.25, 0.25, 0.25, 0.5, 0.75, 0.5), (236, 230, 214)),
    'red_mulberry_twig': ((0.25, 0.25, 0.25, 0.5, 0.75, 0.5), (150, 24, 44)),
}


def box_parts(block):
    entry = BOX_BLOCKS[block]
    return entry if isinstance(entry, list) else [entry]


def kind(block):
    if block in BOX_BLOCKS:
        return 'box'
    if block.endswith('_leaves'):
        return 'leaves'
    if block in ('pink_petals', 'leaf_litter', 'moss_carpet', 'wildflowers'):
        return 'carpet'
    return 'solid'


def is_log(block):
    return block.endswith('_log') or block.endswith('_wood')


_face_tex_cache = {}


def face_texture(block, face, axis):
    """16x16 texture for one face of a block, tinted, rotated for horizontal logs."""
    key = (block, face, axis)
    if key in _face_tex_cache:
        return _face_tex_cache[key]
    rot = False
    if block.endswith('_log'):
        end = {'y': 'top', 'x': 'east', 'z': 'south'}[axis]
        im = block_tex(block + '_top' if face == end else block)
        # Grain runs along the log axis: turn the side texture when the axis lies in the face's u direction.
        rot = (axis == 'x' and face in ('top', 'south')) or (axis == 'z' and face == 'east')
    elif block.endswith('_wood'):
        im = block_tex(block.replace('_wood', '_log'))
    elif block == 'grass_block':
        if face == 'top':
            im = _tint(block_tex('grass_block_top'), GRASS)
        else:
            im = block_tex('grass_block_side').copy()
            im.alpha_composite(_tint(block_tex('grass_block_side_overlay'), GRASS))
    elif block == 'podzol':
        im = block_tex('podzol_top' if face == 'top' else 'podzol_side')
    elif block in ('sandstone',):
        im = block_tex('sandstone_top' if face == 'top' else 'sandstone')
    elif face == 'top' and f'assets/minecraft/textures/block/{block}_top.png' in _zip.namelist():
        im = block_tex(block + '_top')  # pillars and other blocks with their own top face
    elif f'assets/minecraft/textures/block/{block}.png' not in _zip.namelist():
        im = block_tex(block + '_side')
    else:
        im = block_tex(block)
    if block in FOLIAGE_TINTED:
        im = _tint(im, FOLIAGE)
    elif block in FIXED_TINT:
        im = _tint(im, FIXED_TINT[block])
    elif block == 'leaf_litter':
        im = _tint(im, DRY_FOLIAGE)
    if rot:
        im = im.transpose(Image.Transpose.ROTATE_90)
    _face_tex_cache[key] = im
    return im


def _padded(tex):
    """18x18 copy with a replicated 1-texel border so adjacent faces overlap instead of leaving seams."""
    t = tex.resize((16, 16), Image.NEAREST)
    p = Image.new('RGBA', (18, 18))
    p.paste(t, (1, 1))
    p.paste(t.crop((0, 0, 1, 16)), (0, 1))
    p.paste(t.crop((15, 0, 16, 16)), (17, 1))
    p.paste(p.crop((0, 1, 18, 2)), (0, 0))
    p.paste(p.crop((0, 16, 18, 17)), (0, 17))
    return p


# Face geometry: local origin, u edge, v edge and image size (see module docstring for the projection).
GEOM = {
    'top': ((A, 0), (A, H), (-A, H), (2 * A, 2 * H)),
    'east': ((0, H), (A, -H), (0, V), (A, V + H)),
    'south': ((0, 0), (A, H), (0, V), (A, V + H)),
}


def _warp(tex, face):
    (ox, oy), (ux, uy), (vx, vy), size = GEOM[face]
    det = ux * vy - vx * uy
    a, b = 16 * vy / det, -16 * vx / det
    d, e = -16 * uy / det, 16 * ux / det
    c = -(a * ox + b * oy) + 1
    f = -(d * ox + e * oy) + 1
    return _padded(tex).transform(size, Image.AFFINE, (a, b, c, d, e, f), resample=Image.NEAREST)


_face_img_cache = {}


def face_image(block, face, axis, light):
    key = (block, face, axis, light)
    img = _face_img_cache.get(key)
    if img is None:
        img = _shade(_warp(face_texture(block, face, axis), face), SHADE[face] * light / 20)
        if kind(block) == 'leaves':
            # Fancy leaves: keep the holes, the warp padding would otherwise fill the rim.
            mask = _warp(face_texture(block, face, axis), face).split()[3]
            img.putalpha(mask)
        _face_img_cache[key] = img
    return img


def screen(x, y, z):
    return (x - z) * A, (x + z) * H - y * V


def sky_light(voxels):
    """Darken faces under a canopy: count solid blocks above each position (cheap stand-in for shadows)."""
    cols = {}
    for (x, y, z), (b, _) in voxels.items():
        if kind(b) != 'carpet':
            cols.setdefault((x, z), []).append(y)
    light = {}
    for (x, y, z) in voxels:
        above = sum(1 for yy in cols.get((x, z), ()) if yy > y)
        light[(x, y, z)] = max(12, 20 - round(1.5 * above))  # 20 = full light, quantised for the cache
    return light


def _box_polys(x0, y0, z0, w, h, d):
    """Screen polygons (top, east, south) of an axis-aligned box in block units."""
    def P(x, y, z):
        return screen(x, y, z)
    x1, y1, z1 = x0 + w, y0 + h, z0 + d
    top = [P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)]
    east = [P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1), P(x1, y0, z0)]
    south = [P(x0, y1, z1), P(x1, y1, z1), P(x1, y0, z1), P(x0, y0, z1)]
    return top, east, south


def steve_boxes(x, z):
    """A 1.8 block tall player figure standing on block (x, 0, z), built from Steve's 32 px model."""
    px = 1.8 / 32
    cx, cz = x + 0.5, z + 0.5
    parts = [
        ((cx - 4 * px, 0, cz - 2 * px, 4 * px, 12 * px, 4 * px), (59, 60, 140)),      # left leg
        ((cx, 0, cz - 2 * px, 4 * px, 12 * px, 4 * px), (52, 53, 128)),               # right leg
        ((cx - 4 * px, 12 * px, cz - 2 * px, 8 * px, 12 * px, 4 * px), (0, 168, 168)),  # body
        ((cx - 8 * px, 12 * px, cz - 2 * px, 4 * px, 12 * px, 4 * px), (190, 140, 105)),  # arm
        ((cx + 4 * px, 12 * px, cz - 2 * px, 4 * px, 12 * px, 4 * px), (190, 140, 105)),  # arm
        ((cx - 4 * px, 24 * px, cz - 4 * px, 8 * px, 8 * px, 8 * px), (180, 128, 95)),   # head
    ]
    return parts


def render(voxels, steve=None, margin=24, bg=None):
    """Render voxels to an RGBA image. steve=(x, z) adds a player figure for scale."""
    light = sky_light(voxels)
    xs = [screen(x, y, z) for (x, y, z) in voxels]
    minx = min(p[0] for p in xs) - A - margin
    maxx = max(p[0] for p in xs) + A + margin
    miny = min(p[1] for p in xs) - V - margin
    maxy = max(p[1] for p in xs) + 2 * H + margin
    w, h = int(maxx - minx), int(maxy - miny)
    img = Image.new('RGBA', (w, h), bg or (0, 0, 0, 0))

    def opaque(p):
        v = voxels.get(p)
        return v is not None and kind(v[0]) == 'solid'

    order = sorted(voxels, key=lambda p: (p[0] + p[1] + p[2], p[1], p[0]))
    steve_key = None
    if steve:
        sx, sz = steve
        steve_key = (sx + sz + 1, 1, sx)
    drawn_steve = False
    for p in order:
        key = (p[0] + p[1] + p[2], p[1], p[0])
        if steve_key and not drawn_steve and key > steve_key:
            _draw_steve(img, steve, minx, miny)
            drawn_steve = True
        x, y, z = p
        block, axis = voxels[p]
        k = kind(block)
        if k == 'carpet':
            ox, oy = screen(x, y + 1 / 16, z)
            fi = face_image(block, 'top', axis, light[p])
            img.alpha_composite(fi, (int(ox - A - minx), int(oy - miny)))
            continue
        if k == 'box':
            _draw_boxes(img, [((x + bx, y + by, z + bz, bw, bh, bd), col)
                              for (bx, by, bz, bw, bh, bd), col in box_parts(block)], minx, miny)
            continue
        for face, n in (('top', (x, y + 1, z)), ('east', (x + 1, y, z)), ('south', (x, y, z + 1))):
            if opaque(n):
                continue  # fancy leaves keep their faces against other leaves, like the game
            fi = face_image(block, face, axis, light[p])
            if face == 'top':
                ox, oy = screen(x, y + 1, z)
                ox -= A
            elif face == 'east':
                ox, oy = screen(x + 1, y + 1, z + 1)
                oy -= H
            else:
                ox, oy = screen(x, y + 1, z + 1)
            img.alpha_composite(fi, (int(ox - minx), int(oy - miny)))
    if steve and not drawn_steve:
        _draw_steve(img, steve, minx, miny)
    return img


def _draw_steve(img, steve, minx, miny):
    _draw_boxes(img, steve_boxes(*steve), minx, miny)


def _draw_boxes(img, boxes, minx, miny):
    d = ImageDraw.Draw(img)
    for (x0, y0, z0, w, h, dd), col in sorted(boxes, key=lambda b: (b[0][0] + b[0][2], b[0][1])):
        top, east, south = _box_polys(x0, y0, z0, w, h, dd)
        for poly, f in ((south, 0.8), (east, 0.6), (top, 1.0)):
            c = tuple(int(v * f) for v in col)
            d.polygon([(px - minx, py - miny) for px, py in poly], fill=c + (255,))


# ---------------------------------------------------------------- side view at eye level

def render_side(voxels, s=12, steve=None, margin=16):
    """Orthographic elevation looking north (south faces visible). Farther blocks fade a little,
    so the leaf holes read as depth. steve=(x, z) draws a player silhouette for scale."""
    light = sky_light(voxels)
    xs = [p[0] for p in voxels] + ([steve[0]] if steve else [])
    ys = [p[1] for p in voxels] + ([1] if steve else [])  # the player is two blocks tall
    zs = [p[2] for p in voxels]
    minx, maxx, maxy = min(xs), max(xs), max(ys)
    zmin, zmax = min(zs), max(zs)
    w = (maxx - minx + 1) * s + 2 * margin
    h = (maxy - min(ys) + 1) * s + 2 * margin
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    def opaque(p):
        v = voxels.get(p)
        return v is not None and kind(v[0]) == 'solid'

    cache = {}
    steve_drawn = False
    for p in sorted(voxels, key=lambda q: (q[2], q[1])):
        x, y, z = p
        if steve and not steve_drawn and z > steve[1]:
            _side_steve(img, steve, s, minx, maxy, margin)
            steve_drawn = True
        block, axis = voxels[p]
        k = kind(block)
        if opaque((x, y, z + 1)) or k == 'carpet':
            continue
        depth = 1.0 if zmax == zmin else 0.72 + 0.28 * (z - zmin) / (zmax - zmin)
        f = SHADE['south'] * light[p] / 20 * depth
        key = (block, axis, round(f, 2))
        if k == 'box':
            d = ImageDraw.Draw(img)
            for (bx, by, bz, bw, bh, bd), col in box_parts(block):
                x0 = margin + (x - minx + bx) * s
                y0 = margin + (maxy - y + 1 - by - bh) * s
                d.rectangle([x0, y0, x0 + max(1, bw * s) - 1, y0 + max(1, bh * s) - 1],
                            fill=tuple(int(c * f) for c in col) + (255,))
            continue
        tile = cache.get(key)
        if tile is None:
            tile = _shade(face_texture(block, 'south', axis).resize((s, s), Image.NEAREST), f)
            cache[key] = tile
        img.alpha_composite(tile, (margin + (x - minx) * s, margin + (maxy - y) * s))
    if steve and not steve_drawn:
        _side_steve(img, steve, s, minx, maxy, margin)
    return img


def _side_steve(img, steve, s, minx, maxy, margin):
    d = ImageDraw.Draw(img)
    px = 1.8 / 32 * s
    cx = margin + (steve[0] - minx + 0.5) * s
    base = margin + (maxy + 1) * s

    def rect(x0, y0, w, h, col):
        d.rectangle([cx + x0 * px, base - (y0 + h) * px, cx + (x0 + w) * px - 1, base - y0 * px - 1], fill=col)
    rect(-4, 0, 8, 12, (59, 60, 140))
    rect(-4, 12, 8, 12, (0, 168, 168))
    rect(-8, 12, 4, 12, (190, 140, 105))
    rect(4, 12, 4, 12, (190, 140, 105))
    rect(-4, 24, 8, 8, (180, 128, 95))


# ---------------------------------------------------------------- leaf decay check

def decay_report(voxels):
    """Vanilla leaf distance: BFS from logs through leaves, 1..7. Returns leaves that would decay (distance 7)."""
    dist = {}
    q = deque()
    for p, (b, _) in voxels.items():
        if is_log(b):
            dist[p] = 0
            q.append(p)
    while q:
        p = q.popleft()
        if dist[p] >= 6:
            continue
        x, y, z = p
        for n in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
            v = voxels.get(n)
            if v and kind(v[0]) == 'leaves' and n not in dist:
                dist[n] = dist[p] + 1
                q.append(n)
    return [p for p, (b, _) in voxels.items() if kind(b) == 'leaves' and p not in dist]
