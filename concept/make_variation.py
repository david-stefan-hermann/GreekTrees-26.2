"""Explains how growth variation works, one image per picked species:
left an annotated anatomy (side view), right eight random growths with their rolled values, below the dice table.

python make_variation.py  ->  variation/NN_<key>.png
"""
import os
import random

from PIL import Image, ImageDraw, ImageFont

import species
import voxel
from make_sheet import BLUE, F_LABEL, F_SMALL, F_TEXT, F_TITLE, GREY, INK, PAPER, sky

F_NOTE = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 15)
F_CAP = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
NOTE = (190, 30, 45, 255)

PICKED = [
    ('cypress', '01', 'Zypresse', [
        ('Höhe', '20–23', 'zuerst gewürfelt wie bei deinen 32 Bäumen: 22 zu 65 %, 23 zu 25 %'),
        ('Stamm', '4', 'immer 4, wie bei allen gebauten; 8 % ein einzelnes Blatt am Stamm darunter'),
        ('Fuß', 'Kreuz + Kreuz mit Ecken', '85 %; sonst zweimal Kreuz (10 %) oder nur eine Kreuzschicht (5 %)'),
        ('Körper', '5–8, meist 6–7', 'volles 3×3, nimmt den Rest der Höhe auf'),
        ('Leisten', 'je Seite und Schicht', 'Block zwei vor der Seitenmitte: 86 % in der Körpermitte, 70 % unten, 55 % oben'),
        ('Übergang', '0–2, meist 1', 'Kreuz mit 1–3 Ecken'),
        ('Kreuz', '2–4, meist 3', '3×3 ohne Ecken; der Stamm endet in der obersten Kreuzschicht'),
        ('Kappe', '0–2, meist 1', 'Mitte plus 1–3 Seiten, die obere hat nie mehr als die untere'),
        ('Spitze', '4–5', 'einzelne Säule; Kappe + Spitze höchstens 6, sonst zerfiele die Spitze'),
    ]),
    ('olive', '02', 'Olivenbaum', [
        ('Stämme', '2 (⅔) oder 3 (⅓)', 'gleichmäßig verteilt, je ±17° Abweichung'),
        ('Drehung', '0–360°', 'Ausrichtung des ganzen Baums, stufenlos'),
        ('Stammhöhe', '5–6', 'je Stamm'),
        ('Neigung', '1,6–2,2', 'wie weit die Stammspitze nach außen geht'),
        ('Ast', '±34°', 'kurzer Ast in die Krone, Richtung um den Stamm gestreut'),
        ('Krone', 'r 3,2–3,8 · h 1,7–2,1', 'eine Laubwolke pro Stamm'),
        ('Zusatzwolken', '2–3', 'kleine Wolken r 2,2 am Kronenrand, 2–2,8 versetzt'),
    ]),
    ('fig', '06', 'Feigenbaum', [
        ('Stämme', '4–5', 'gleichmäßig verteilt, je ±20° Abweichung'),
        ('Drehung', '0–360°', 'stufenlos'),
        ('Knie', 'weit 2–3 · hoch 1–2', 'erster Knick, flach aus dem Boden'),
        ('Spitze', 'weit 3,2–4,2 · hoch 3–4', 'Ende des Stamms'),
        ('Krone', 'r 2,5–3,0', 'Laubwolke je Stammspitze, dazu eine feste Kappe in der Mitte'),
    ]),
    ('strawberry_tree', '09', 'Erdbeerbaum', [
        ('Stamm', '2–3', 'gemeinsamer gerader Fuß'),
        ('Stämme', '2 oder 3', '2: genau gegenüber; 3: drei der vier Himmelsrichtungen'),
        ('Stammhöhe', '6–8', 'je Stamm'),
        ('Weite', '2–4', 'Blöcke nach außen; die ersten zwei Schritte gehen immer nach außen'),
        ('Drall', 'links / rechts / keiner', 'ein Schritt seitlich an zufälliger Höhe'),
        ('Seitenast', '1–2 lang', '2–3 unter der Spitze, nach links oder rechts'),
        ('Krone', 'r 2,0–2,6 · Ast r 1,6–2,0', 'eine Wolke auf Stamm und Seitenast'),
        ('Stammform', 'fest', 'wie bei Vanilla-Akazien: jeder Schritt ein Block hoch und höchstens einer zur Seite, keine Füllblöcke'),
    ]),
    ('date_palm', '10', 'Kretische Dattelpalme', [
        ('Stämme', '2 oder 3', 'je 50 %'),
        ('Höhen', '9–11 · 6–7 · 4–5', 'Hauptstamm, zweiter, dritter'),
        ('Drehung', '0–360°', 'Richtung, in die sich der Horst öffnet'),
        ('Neigung', 'fest', 'Hauptstamm ¼ seiner Höhe, Nebenstämme 0,6'),
        ('Hängende Wedel', 'je 70 %', 'jeder der vier langen Wedel bekommt eine hängende Spitze'),
        ('Datteln', '2 von 4 Seiten', 'Kakao am Hauptstamm unter der Krone'),
    ]),
]


def rotate(p, delta):
    """Turn a rolled tree so its first stem points along +x (side view = east-west)."""
    q = dict(p)
    if 'staemme' in q:
        q['staemme'] = [dict(s, winkel=s['winkel'] + delta, **({'ast': s['ast'] + delta} if 'ast' in s else {}))
                        for s in q['staemme']]
    q['drehung'] = q.get('drehung', 0) + delta
    return q


def anatomy_tree(key):
    rng = random.Random(4)
    p = species.roll(key, rng)
    if key == 'cypress':
        pass  # seed 4 as rolled
    elif key == 'strawberry_tree':
        p['staemme'] = [dict(s, richtung=d) for s, d in zip(p['staemme'][:2], (0, 2))]
    elif key == 'date_palm':
        p.update(drehung=0, hoehen=[10, 6], haengend=[True, True, False, True], datteln=[0, 2])
    elif 'staemme' in p:
        p = rotate(p, -p['staemme'][0]['winkel'])
    rng = random.Random(4)
    t = getattr(species, key + '_build')(p, rng).finish()
    t.params = p
    return t


def with_player(t):
    """Ground strip and player figure two blocks east of the tree, like the concept cards."""
    x0, x1, z0, z1, top = t.extent()
    sx = x1 + 2
    for gx in range(sx - 1, sx + 2):
        t.v.setdefault((gx, -1, 0), ('grass_block', 'y'))
    return (sx, 0)


def extent_blocks(t, steve):
    xs = [q[0] for q in t.v] + [steve[0]]
    ys = [q[1] for q in t.v] + [1]
    return min(xs), max(xs), min(ys), max(ys)


def side_with_notes(t, s, left, right=100, top=56):
    steve = with_player(t)
    img = voxel.render_side(t.v, s=s, steve=steve, margin=0)
    minx, _, _, maxy = extent_blocks(t, steve)
    canvas = Image.new('RGBA', (img.width + left + right, img.height + top + 10), (0, 0, 0, 0))
    canvas.alpha_composite(img, (left, top))
    d = ImageDraw.Draw(canvas)

    def P(x, y):  # continuous world coords -> pixels
        return left + (x - minx) * s, top + (maxy + 1 - y) * s

    bars = [n for n in t.notes if n['kind'] == 'vbar']
    cols = []
    for n in bars:  # overlapping height ranges go into separate columns, further left
        c = 0
        while any(cc == c and not (n['y1'] < a or n['y0'] > b) for cc, a, b, _ in cols):
            c += 1
        cols.append((c, n['y0'], n['y1'], n))
    widths = {}
    for c, _, _, n in cols:
        widths[c] = max(widths.get(c, 0), d.textlength(n['label'], font=F_NOTE))
    xcol = {0: left - 14}
    for c in range(1, len(widths)):
        xcol[c] = xcol[c - 1] - widths[c - 1] - 30
    for c, _, _, n in cols:
        x = xcol[c]
        _, ya = P(0, n['y1'] + 1)
        _, yb = P(0, n['y0'])
        d.line([(x, ya + 2), (x, yb - 2)], fill=NOTE, width=3)
        d.line([(x, ya + 2), (x + 7, ya + 2)], fill=NOTE, width=3)
        d.line([(x, yb - 2), (x + 7, yb - 2)], fill=NOTE, width=3)
        tw = d.textlength(n['label'], font=F_NOTE)
        d.text((x - tw - 6, (ya + yb) / 2 - 10), n['label'], font=F_NOTE, fill=NOTE)
    k = 0
    used = []
    for n in t.notes:
        if n['kind'] == 'ellipse':
            if abs(n.get('z', 0)) > 1.5:
                continue  # in front of or behind the trunk, not part of the outline
            cx, cy = P(n['x'] + 0.5, n['y'] + 0.5)
            rx, ry = (n['rx'] + 0.5) * s, (n['ry'] + 0.5) * s
            d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=(255, 255, 255, 230), width=2)
            tw = d.textlength(n['label'], font=F_NOTE)
            lx = cx + rx * 0.55 if k % 2 == 0 else cx - rx * 0.55 - tw
            d.text((lx, cy - ry - 20), n['label'], font=F_NOTE, fill=(255, 255, 255, 255),
                   stroke_width=2, stroke_fill=(40, 60, 90, 255))
            k += 1
        elif n['kind'] == 'dot':
            cx, cy = P(n['x'] + 0.5, n['y'] + 0.5)
            d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=NOTE, width=3)
            lx = canvas.width - right + 12
            ly = cy
            while any(abs(ly - u) < 22 for u in used):  # keep labels from stacking on each other
                ly += 22
            used.append(ly)
            d.line([(cx + 5, cy), (lx - 4, ly)], fill=NOTE, width=1)
            d.text((lx, ly - 10), n['label'], font=F_NOTE, fill=NOTE)
    return canvas


def fit_scale(trees, w, h, cap):
    """Largest block size in pixels so every tree (with player) fits w x h."""
    best = cap
    for t in trees:
        steve = (t.extent()[1] + 2, 0)
        x0, x1, y0, y1 = extent_blocks(t, steve)
        best = min(best, int(w / (x1 - x0 + 1)), int(h / (y1 - y0 + 1)))
    return max(4, best)


def variant_cell(t, s, w, h, key):
    steve = with_player(t)
    img = voxel.render_side(t.v, s=s, steve=steve, margin=4)
    cell = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    cell.alpha_composite(img, ((w - img.width) // 2, h - 40 - img.height))
    d = ImageDraw.Draw(cell)
    for i, line in enumerate(species.summary(key, t.params)):
        tw = d.textlength(line, font=F_CAP)
        d.text(((w - tw) / 2, h - 38 + i * 17), line, font=F_CAP, fill=INK)
    return cell


def figure(key, num, title, table):
    W = 1700
    cell_w, cell_h = 255, 320
    grid_w = cell_w * 4
    body_h = cell_h * 2 + 20
    left_w = W - grid_w - 60
    at = anatomy_tree(key)
    n_cols = len({(n['y0'], n['y1']) for n in at.notes if n['kind'] == 'vbar'})
    note_left = 150 if key != 'date_palm' else 215
    s_anat = fit_scale([at], left_w - note_left - 100 - 20, body_h - 70, 26)
    anat = side_with_notes(at, s_anat, note_left)
    growths = [species.grow(key, i + 1) for i in range(8)]
    s_var = fit_scale(growths, cell_w - 16, cell_h - 70, 16)

    row_h = 30
    table_h = 50 + row_h * len(table)
    H = 100 + body_h + table_h + 30
    img = Image.new('RGBA', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((28, 16), f'{num}  {title} · wie die Varianten entstehen', font=F_TITLE, fill=INK)
    d.text((32, 62), 'Links: Aufbau mit den gewürfelten Größen. Rechts: 8 zufällige Wüchse (Seed 1–8) mit ihren Würfen. '
           'Seitenansicht, Spielerfigur als Maßstab.', font=F_TEXT, fill=GREY)

    panel = sky(left_w, body_h)
    panel.alpha_composite(anat, ((left_w - anat.width) // 2, body_h - anat.height - 6))
    img.alpha_composite(panel, (20, 100))
    d.text((32, 106), 'Aufbau', font=F_LABEL, fill=INK)

    grid = sky(grid_w + 20, body_h)
    for i, t in enumerate(growths):
        cell = variant_cell(t, s_var, cell_w, cell_h, key)
        grid.alpha_composite(cell, (10 + (i % 4) * cell_w, (i // 4) * cell_h + 10))
    img.alpha_composite(grid, (left_w + 40, 100))
    d.text((left_w + 52, 106), '8 Wüchse', font=F_LABEL, fill=INK)

    y = 100 + body_h + 18
    d.text((28, y), 'Würfel bei jedem Wachsen', font=F_LABEL, fill=BLUE)
    y += 32
    for name, rng_, effect in table:
        d.text((40, y), name, font=F_LABEL, fill=INK)
        d.text((240, y), rng_, font=F_TEXT, fill=INK)
        d.text((520, y), effect, font=F_TEXT, fill=INK)
        y += row_h
    return img.crop((0, 0, W, y + 16))


def main():
    os.makedirs('variation', exist_ok=True)
    for key, num, title, table in PICKED:
        img = figure(key, num, title, table)
        img.save(f'variation/{num}_{key}.png')
        print(key, img.size)


if __name__ == '__main__':
    main()
