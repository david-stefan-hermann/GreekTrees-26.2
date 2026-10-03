"""Concepts for a more organic date cluster model. The user picked a mix of B and C, which is now the mod's model
(tools/date_cluster.py); A-D stay here as the record of the choice.

Each concept builds the three ripeness stages from tilted boxes (the 26.x model format takes any rotation angle):
a curved stalk out of the trunk, strands, and dates that hang at their own small angle and never overlap each
other (checked as oriented boxes). python tools/date_concepts.py -> art/date_concepts/sheet.png
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import date_cluster  # noqa: E402
import raycast  # noqa: E402
from date_cluster import DATE_SIZE, GROWTH, Cluster, grown, stage_texture  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'concept'))
OUT = os.path.join(ROOT, 'art', 'date_concepts')

# ---------------------------------------------------------------- the concepts (g = growth 0.55 / 0.8 / 1)

def concept_arch(stage, seed=3):
    """A: arched stalk, a fan of strands from its end, dates along the strands like a hanging tassel."""
    g, size = GROWTH[stage], DATE_SIZE[stage]
    c = Cluster(seed + stage)
    arch = [grown(p, g) for p in ((8, 13.5, 16), (8, 14.2, 12.5), (8, 13, 9.5), (8, 10.5, 7.5))]
    c.path(arch, [0.8, 1.0, 1.25][stage])
    n = [5, 7, 10][stage]
    for i in range(n):
        k = i / max(1, n - 1)
        start = arch[2] + (arch[3] - arch[2]) * (0.3 + 0.7 * c.rng.random())
        spread = (k - 0.5) * 1.6
        d = np.array([spread, -1.0, -0.35 + 0.5 * c.rng.random()])
        length = (6 + 3 * c.rng.random()) * g
        end = start + d / np.linalg.norm(d) * length
        c.path([start, end], 0.6)
        steps = int(length / 1.1)
        for s in range(1, steps + 1):
            p = start + (end - start) * (s / steps)
            c.date_near(p, size, 18, 1.2, lean=(d[2] * 20, -d[0] * 20))
    return c


def concept_bunch(stage, seed=11):
    """B: a short stalk and a dense, heavy bunch like a bunch of grapes, wide at the top and pointed below."""
    g, size = GROWTH[stage], DATE_SIZE[stage]
    c = Cluster(seed + stage)
    arch = [grown(p, g) for p in ((8, 13.5, 16), (8, 14, 12.5), (8, 12.5, 10))]
    c.path(arch, [1.0, 1.5, 2.0][stage])
    top, bottom = arch[-1][1] - 0.5, arch[-1][1] - 12 * g
    centre = arch[-1] + np.array([0, 0, -1.5 * g])
    for _ in range(3000):
        y = c.rng.uniform(bottom, top)
        f = (y - bottom) / (top - bottom)
        radius = (1.2 + 5.3 * math.sin(f * math.pi * 0.62)) * g
        a, rr = c.rng.uniform(0, 2 * math.pi), radius * math.sqrt(c.rng.random())
        p = centre + np.array([math.cos(a) * rr, y - centre[1], math.sin(a) * rr * 0.8])
        c.try_date(p, size, 28)
        if len(c.dates) >= [10, 24, 40][stage]:
            break
    for x in (-2.5, 0, 2.5):  # a few strands peeking out under the stalk
        c.path([arch[-1], arch[-1] + np.array([x, -3.5, -1]) * g], 0.6)
    return c


def concept_strings(stage, seed=21):
    """C: long thin strands hanging well below the block with dates on their lower half (the real date palm look).
    Needs the cluster below to stay free, so only the top ring of clusters would remain."""
    g, size = GROWTH[stage], (np.array(DATE_SIZE[stage]) * 0.9)
    c = Cluster(seed + stage)
    arch = [grown(p, g) for p in ((8, 13.5, 16), (8, 14.8, 11.5), (8, 13.5, 7.5), (8, 11, 5.5))]
    c.path(arch, [1.0, 1.5, 2.0][stage])
    n = [5, 8, 12][stage]
    for i in range(n):
        start = arch[2] + (arch[3] - arch[2]) * c.rng.random() + np.array([c.rng.uniform(-1, 1), 0, 0])
        d = np.array([c.rng.uniform(-0.25, 0.25) + (i / (n - 1) - 0.5) * 0.5, -1, c.rng.uniform(-0.3, 0.15)])
        length = (13 + 6 * c.rng.random()) * g
        end = start + d / np.linalg.norm(d) * length
        c.path([start, end], 0.5)
        s = 0.4
        while s <= 1.0:
            c.date_near(start + (end - start) * s, size, 12, 1.0)
            s += 1.5 / length
    return c


def concept_twin(stage, seed=31):
    """D: the stalk forks into two bunches of different size at different heights, turned against each other."""
    g, size = GROWTH[stage], DATE_SIZE[stage]
    c = Cluster(seed + stage)
    trunk = [grown(p, g) for p in ((8, 13.5, 16), (8, 14, 12.5), (8, 13, 10.5))]
    c.path(trunk, [1.0, 1.5, 2.0][stage])
    fork = trunk[-1]
    for (dx, dy, dz), radius, height, count in (((-3.5, -2.5, -2), 4.2, 10, [6, 14, 22][stage]),
                                                ((3.5, -1.0, -1), 3.0, 7, [4, 9, 14][stage])):
        end = fork + np.array([dx, dy, dz]) * g
        c.path([fork, end], [0.8, 1.2, 1.5][stage])
        top, bottom = end[1] - 0.3, end[1] - height * g
        placed, tries = 0, 0
        while placed < count and tries < 2000:
            tries += 1
            y = c.rng.uniform(bottom, top)
            f = (y - bottom) / (top - bottom)
            r = (0.8 + radius * math.sin(f * math.pi * 0.62)) * g
            a, rr = c.rng.uniform(0, 2 * math.pi), r * math.sqrt(c.rng.random())
            p = np.array([end[0] + math.cos(a) * rr, y, end[2] + math.sin(a) * rr * 0.8])
            placed += c.try_date(p, size, 25)
    return c


CONCEPTS = [
    ('B+C', 'gewählt: Mischung aus B und C', date_cluster.build),
    ('A', 'Bogen mit Quaste', concept_arch),
    ('B', 'Dichte Traube', concept_bunch),
    ('C', 'Lange Fäden', concept_strings),
    ('D', 'Zwei Büschel', concept_twin),
]


# ---------------------------------------------------------------- scenes

def cluster_boxes(cluster, stage, offset_blocks, turn=0):
    tex = stage_texture(stage)
    R = raycast.rot_y(turn)
    boxes = []
    for e in cluster.elements():
        faces = {f: (tex, e.uv(f)) for f in ('north', 'south', 'east', 'west', 'up', 'down')}
        b = raycast.Box(e.lo, e.hi, faces, rot=e.M, origin=e.origin)
        if turn:
            b = b.turned(R, np.array([8.0, 8.0, 8.0]))
        b.offset = b.offset + np.array(offset_blocks, float) * 16
        boxes.append(b)
    return boxes


def palm_top():
    """Trunk with crown leaves above the clusters: the trunk top at block (0, 0, 0)."""
    import voxel
    wood = np.array(voxel.face_texture('jungle_wood', 'south', 'y').convert('RGBA'))
    leaves = np.array(voxel.face_texture('jungle_leaves', 'top', 'y').convert('RGBA'))
    boxes = [raycast.full_block(wood, (0, y, 0)) for y in range(-4, 2)]
    cells = {(0, 2, 0)}
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        cells |= {(dx, 1, dz), (2 * dx, 2, 2 * dz), (3 * dx, 1, 3 * dz), (4 * dx, 0, 4 * dz)}
    for dx in (-1, 1):
        for dz in (-1, 1):
            cells |= {(dx, 1, dz), (dx, 2, dz), (2 * dx, 1, 2 * dz), (2 * dx, 0, 2 * dz)}
    boxes += [raycast.full_block(leaves, c) for c in sorted(cells)]
    return boxes


VIEW = (0.55, 0.32, 1.0)   # from the north-west and a little below, looking up at the clusters like a player


def scene_image(concept, stage, size=(440, 520), context=True):
    c = concept(stage)
    boxes = cluster_boxes(c, stage, (0, 0, -1))
    if context:
        # the frame fits the front cluster with room around it: trunk top, crown above, the second cluster
        centre, scale = raycast.fit(boxes, VIEW, size, margin=2.3)
        centre = centre + np.array([0, 3, 0])
        boxes += cluster_boxes(concept(stage), stage, (-1, 0, 0), turn=90)
        boxes += palm_top()
        return raycast.render(boxes, VIEW, centre, scale, size)
    centre, scale = raycast.fit(boxes, VIEW, size)
    return raycast.render(boxes, VIEW, centre, scale, size)


def main():
    from make_sheet import F_LABEL, F_TEXT, F_TITLE
    os.makedirs(OUT, exist_ok=True)
    col_w, big_h, small = 440, 520, 146
    sheet = Image.new('RGB', (len(CONCEPTS) * (col_w + 16) + 16, 110 + big_h + 30 + small + 70), (244, 240, 232))
    d = ImageDraw.Draw(sheet)
    d.text((18, 14), 'Dattelrispe: Vorschläge für ein organischeres Modell', font=F_TITLE, fill=(30, 50, 80))
    d.text((20, 62), 'Oben reif an der Palme (zwei Rispen unter der Krone, Blick von unten wie im Spiel), darunter '
                     'die drei Reifestufen. Gekippte Elemente, keine überlappenden Datteln.', font=F_TEXT,
           fill=(110, 110, 110))
    for i, (key, title, concept) in enumerate(CONCEPTS):
        x = 16 + i * (col_w + 16)
        big = scene_image(concept, 2)
        sheet.paste(big, (x, 100))
        for s in range(3):
            img = scene_image(concept, s, (small, small), context=False)
            sheet.paste(img, (x + s * (small + 1), 100 + big_h + 8))
        n = len(concept(2).elements())
        d.text((x + 4, 100 + big_h + small + 16), f'{key}: {title}', font=F_LABEL, fill=(30, 50, 80))
        d.text((x + 4, 100 + big_h + small + 46), f'{len(concept(2).dates)} Datteln, {n} Elemente (reif)', font=F_TEXT,
               fill=(110, 110, 110))
        big.save(os.path.join(OUT, f'{key}_ripe.png'))
    sheet.save(os.path.join(OUT, 'sheet.png'))
    print(os.path.join(OUT, 'sheet.png'), sheet.size)


def final():
    """The chosen model: ripe at the palm, the three stages close up, and a palm top with clusters on three sides
    at mixed stages, the way a grown palm carries them."""
    from make_sheet import F_LABEL, F_TEXT, F_TITLE
    os.makedirs(OUT, exist_ok=True)
    sheet = Image.new('RGB', (16 + 2 * 456, 110 + 520 + 30 + 300 + 50), (244, 240, 232))
    d = ImageDraw.Draw(sheet)
    d.text((18, 14), 'Dattelrispe: Mischung aus B und C', font=F_TITLE, fill=(30, 50, 80))
    d.text((20, 62), 'Lange Fäden wie C, dicht besetzt wie B. Reif hängt sie fast einen halben Block tiefer.',
           font=F_TEXT, fill=(110, 110, 110))
    sheet.paste(scene_image(date_cluster.build, 2), (16, 100))
    # a palm top seen from further away: clusters north (ripe), west (half ripe) and east (young)
    boxes = cluster_boxes(date_cluster.build(2), 2, (0, 0, -1))
    boxes += cluster_boxes(date_cluster.build(1), 1, (-1, 0, 0), turn=90)
    boxes += cluster_boxes(date_cluster.build(0), 0, (1, 0, 0), turn=-90)
    centre, scale = raycast.fit(boxes, VIEW, (440, 520), margin=2.6)
    boxes += palm_top()
    sheet.paste(raycast.render(boxes, VIEW, centre + np.array([0, 4, 0]), scale, (440, 520)), (16 + 456, 100))
    # the three stages at the same scale (fitted to the ripe one), so the growth shows
    centre, scale = raycast.fit(cluster_boxes(date_cluster.build(2), 2, (0, 0, -1)), VIEW, (300, 300))
    for s in range(3):
        img = raycast.render(cluster_boxes(date_cluster.build(s), s, (0, 0, -1)), VIEW, centre, scale, (300, 300))
        sheet.paste(img, (16 + s * 304, 100 + 520 + 30))
    labels = ['grün (Stufe 0)', 'gelb (Stufe 1)', 'reif (Stufe 2)']
    for s in range(3):
        n = len(date_cluster.STAGES[s].dates)
        d.text((20 + s * 304, 100 + 520 + 30 + 304), f'{labels[s]}: {n} Datteln', font=F_LABEL, fill=(30, 50, 80))
    sheet.save(os.path.join(OUT, 'BC_final.png'))
    print(os.path.join(OUT, 'BC_final.png'), sheet.size)


if __name__ == '__main__':
    if 'final' in sys.argv:
        final()
    else:
        main()
