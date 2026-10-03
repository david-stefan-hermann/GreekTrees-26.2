"""Mod icon concepts for Greek Trees, round 2 (round 1 was rejected; its images are in art/icon_concepts/round1).

python tools/make_icons.py -> art/icon_concepts/round2/{E_item,F_five,G_sunset,H_mosaic}.png and preview.png
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'art', 'icon_concepts', 'round2')
TEX = os.path.join(ROOT, 'src', 'main', 'resources', 'assets', 'greektrees', 'textures', 'block')


def sapling(name):
    return Image.open(os.path.join(TEX, name + '_sapling.png')).convert('RGBA')


def rounded_mask(size, radius):
    m = Image.new('L', (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return m


def framed(img, radius, outline=None, width=0):
    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), rounded_mask(img.width, radius))
    if outline:
        ImageDraw.Draw(out).rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=radius,
                                              outline=outline, width=width)
    return out


def gradient(size, top, bottom):
    img = Image.new('RGBA', (size, size))
    d = ImageDraw.Draw(img)
    for y in range(size):
        t = y / (size - 1)
        d.line([(0, y), (size - 1, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)) + (255,))
    return img


def with_shadow(base, sprite, pos, offset=(4, 6), blur=4, alpha=110):
    mask = sprite.split()[3]
    shadow = Image.new('RGBA', sprite.size, (10, 20, 40, 0))
    shadow.putalpha(mask.point(lambda v: alpha if v else 0))
    pad = Image.new('RGBA', (sprite.width + 4 * blur, sprite.height + 4 * blur), (0, 0, 0, 0))
    pad.alpha_composite(shadow, (2 * blur, 2 * blur))
    pad = pad.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(pad, (pos[0] + offset[0] - 2 * blur, pos[1] + offset[1] - 2 * blur))
    base.alpha_composite(sprite, pos)


# ================================================================ E: the sapling as a big item

def icon_item():
    img = gradient(128, (132, 190, 240), (30, 92, 172))
    glow = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([22, 16, 106, 100], fill=(255, 238, 186, 150))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(14)))
    with_shadow(img, sapling('olive').resize((96, 96), Image.NEAREST), (16, 14), offset=(3, 4), blur=2, alpha=70)
    return framed(img, 22, (246, 242, 230, 255), 3)


# ================================================================ F: all five saplings on marble

def icon_five():
    rng = random.Random(5)
    img = Image.new('RGBA', (128, 128), (244, 241, 233, 255))
    veins = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veins)
    for _ in range(5):  # faint marble veins
        x, y = rng.uniform(-20, 128), rng.uniform(-20, 40)
        pts = []
        for _ in range(8):
            pts.append((x, y))
            x += rng.uniform(8, 22)
            y += rng.uniform(6, 20)
        vd.line(pts, fill=(200, 196, 190, 70), width=1, joint='curve')
    img.alpha_composite(veins.filter(ImageFilter.GaussianBlur(1)))
    with_shadow(img, sapling('cypress').resize((64, 64), Image.NEAREST), (32, 28), offset=(3, 4), blur=3, alpha=90)
    for name, pos in (('olive', (12, 10)), ('fig', (84, 10)), ('strawberry_tree', (12, 84)), ('date_palm', (84, 84))):
        with_shadow(img, sapling(name).resize((32, 32), Image.NEAREST), pos, offset=(2, 3), blur=2, alpha=90)
    return framed(img, 18, (28, 86, 166, 255), 6)


# ================================================================ G: blocky cypresses against a sunset (64 grid, x2)

def icon_sunset():
    s = Image.new('RGBA', (64, 64))
    d = ImageDraw.Draw(s)
    bands = [(44, 40, 104), (78, 52, 124), (128, 62, 128), (184, 80, 116), (226, 112, 92), (244, 150, 76),
             (250, 190, 92), (252, 220, 132)]
    for y in range(40):
        i = min(len(bands) - 1, y * len(bands) // 40)
        c = bands[i]
        nxt = bands[min(len(bands) - 1, i + 1)]
        for x in range(64):  # dither one row at every band edge
            edge = (y + 1) * len(bands) // 40 != i and (x + y) % 2
            s.putpixel((x, y), (nxt if edge else c) + (255,))
    d.ellipse([33, 26, 53, 46], fill=(255, 226, 150, 255))  # sun sinking into the sea
    d.ellipse([36, 29, 50, 43], fill=(255, 244, 196, 255))
    d.rectangle([0, 40, 63, 63], fill=(36, 34, 86, 255))
    for y in range(41, 64):
        t = (y - 41) / 23
        d.line([(0, y), (63, y)], fill=(int(54 - 24 * t), int(48 - 20 * t), int(110 - 30 * t), 255))
    for y, x0, x1 in ((41, 34, 52), (43, 37, 49), (45, 39, 47), (48, 40, 46), (51, 41, 45), (55, 42, 44)):
        d.line([(x0, y), (x1, y)], fill=(250, 170, 96, 255))  # reflection
    ink = (24, 16, 40, 255)
    d.polygon([(0, 44), (0, 38), (8, 35), (20, 34), (30, 36), (38, 40), (40, 44)], fill=ink)  # hill
    d.rectangle([0, 44, 40, 47], fill=ink)
    d.rectangle([0, 47, 26, 63], fill=ink)
    d.polygon([(26, 47), (40, 47), (30, 63), (26, 63)], fill=ink)

    def cypress(x, base, h, seed):
        """Silhouette of the built cypresses: 3-block trunk, 3-wide body with strips that stick out to 5,
        a narrower plus band and a single spire."""
        r = random.Random(seed)
        d.rectangle([x, base - 2, x, base], fill=ink)
        crown = h - 3
        for k in range(crown):
            y = base - 3 - k
            f = k / crown
            if f < 0.08:
                half = 1
            elif f < 0.5:
                half = 2 if r.random() < 0.6 else 1
            elif f < 0.72:
                half = 1
            else:
                half = 0
            d.line([(x - half, y), (x + half, y)], fill=ink)

    cypress(8, 36, 24, 1)
    cypress(15, 35, 31, 2)
    cypress(22, 35, 22, 3)
    # small temple on the hill's end
    d.polygon([(27, 30), (33, 27), (39, 30)], fill=ink)
    d.rectangle([27, 30, 39, 31], fill=ink)
    for x in (28, 30, 32, 34, 36, 38):
        d.line([(x, 32), (x, 36)], fill=ink)
    d.rectangle([26, 37, 40, 38], fill=ink)
    return framed(s.resize((128, 128), Image.NEAREST), 18, (24, 16, 40, 255), 3)


# ================================================================ H: olive tree mosaic

def icon_mosaic():
    N = 21
    rng = random.Random(9)
    cream, ochre, blue, dblue = (240, 232, 212), (206, 168, 104), (44, 96, 170), (26, 60, 120)
    grid = [[cream for _ in range(N)] for _ in range(N)]
    for i in range(N):  # border: dark blue ring, light blue ring
        for j in range(N):
            ring = min(i, j, N - 1 - i, N - 1 - j)
            if ring == 0:
                grid[j][i] = dblue
            elif ring == 1:
                grid[j][i] = blue if (i + j) % 2 else (226, 232, 240)
    for i in range(2, N - 2):  # a single row of ground, the rest is air
        grid[18][i] = ochre
    trunk = (74, 48, 30)
    for y, xs in ((17, (9, 10, 11)), (16, (9, 10, 11)), (15, (9, 11)), (14, (8, 9, 11, 12)), (13, (8, 12)),
                  (12, (8, 12)), (11, (8, 12))):
        for x in xs:
            grid[y][x] = trunk
    greens = [(40, 72, 34), (58, 98, 44), (84, 128, 58), (122, 160, 84)]
    for cx, cy, rx, ry in ((6, 11, 3.2, 2.6), (14, 11, 3.2, 2.6), (10, 8, 3.6, 2.4), (8, 13, 2.4, 1.8),
                           (12, 13, 2.4, 1.8)):
        for y in range(N):
            for x in range(N):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1 and 2 <= x < N - 2 and 2 <= y < 17:
                    shade = 1 if y > cy else 2
                    if ((x - cx + 1) / rx) ** 2 + ((y - cy + 1) / ry) ** 2 <= 0.35:
                        shade = 3
                    grid[y][x] = greens[shade] if rng.random() > 0.15 else greens[shade - 1]
    for x, y in ((5, 12), (14, 10), (11, 7), (8, 10), (16, 12)):  # olives
        grid[y][x] = (64, 40, 76)
    tile = 6
    img = Image.new('RGBA', (N * tile + 2, N * tile + 2), (176, 164, 146, 255))  # grout
    d = ImageDraw.Draw(img)
    for y in range(N):
        for x in range(N):
            c = tuple(max(0, min(255, v + rng.randint(-10, 10))) for v in grid[y][x])
            x0 = 1 + x * tile + rng.randint(0, 1)
            y0 = 1 + y * tile + rng.randint(0, 1)
            d.rectangle([x0, y0, x0 + tile - 2, y0 + tile - 2], fill=c + (255,))
    img = img.resize((128, 128), Image.LANCZOS)
    return framed(img, 14)


# ================================================================ preview

CONCEPTS = [
    ('E_item', 'E · Setzling pur', icon_item),
    ('F_five', 'F · Die fünf Setzlinge', icon_five),
    ('G_sunset', 'G · Zypressen im Abendlicht', icon_sunset),
    ('H_mosaic', 'H · Mosaik', icon_mosaic),
]


ICON = os.path.join(ROOT, 'src', 'main', 'resources', 'assets', 'greektrees', 'icon.png')


def main():
    os.makedirs(OUT, exist_ok=True)
    icon_mosaic().save(ICON)  # picked by the user on 2026-10-02 (round 2, H)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 26)
    small = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
    col = 420
    sheet = Image.new('RGBA', (col * len(CONCEPTS) + 20, 620), (236, 232, 222, 255))
    d = ImageDraw.Draw(sheet)
    for i, (key, title, fn) in enumerate(CONCEPTS):
        icon = fn()
        icon.save(os.path.join(OUT, key + '.png'))
        x = 20 + i * col
        d.text((x, 14), title, font=font, fill=(29, 53, 87, 255))
        sheet.alpha_composite(icon.resize((384, 384), Image.NEAREST), (x, 56))
        for j, bgc in enumerate(((30, 30, 34, 255), (250, 250, 250, 255))):
            tile = Image.new('RGBA', (180, 90), bgc)
            tile.alpha_composite(icon.resize((64, 64), Image.LANCZOS), (10, 13))
            tile.alpha_composite(icon.resize((32, 32), Image.LANCZOS), (90, 29))
            sheet.alpha_composite(tile, (x + j * 196, 456))
        d.text((x, 556), 'Mod-Liste: 64 px und 32 px', font=small, fill=(90, 96, 110, 255))
    sheet.save(os.path.join(OUT, 'preview.png'))
    print('ok')


if __name__ == '__main__':
    main()
