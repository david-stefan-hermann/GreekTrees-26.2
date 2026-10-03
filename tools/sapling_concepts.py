"""Five texture proposals each for the Aries oak sapling and the weeping willow sapling (the willow now in pale oak
and azalea). Every proposal is drawn flat and large, as the crossed planes of the block on a grass block, and on the
ground next to the current texture and the vanilla sapling it comes from.

python tools/sapling_concepts.py    -> art/sapling_concepts/aries_oak_sapling.png, weeping_willow_sapling.png
python tools/sapling_concepts.py 2  -> round 2, three variants of each pick (Aries oak A, willow B):
                                       art/sapling_concepts/aries_oak_sapling_v2.png, weeping_willow_sapling_v2.png
python tools/sapling_concepts.py 3  -> round 3, the willow (B) with a curved trunk, five ways:
                                       art/sapling_concepts/weeping_willow_sapling_v3.png
python tools/sapling_concepts.py 4  -> round 4, the willow drawn anew: a domed crown whose strands spring from the
                                       top like a fountain and fall, over a slightly C-curved trunk:
                                       art/sapling_concepts/weeping_willow_sapling_v4.png
python tools/sapling_concepts.py mulberry -> five mulberry saplings after the real tree:
                                       art/sapling_concepts/mulberry_sapling.png
python tools/sapling_concepts.py olive -> five olive saplings after the real tree:
                                       art/sapling_concepts/olive_sapling.png
python tools/sapling_concepts.py olive2 -> five olive saplings after the grown tree of the mod, silvery and in the
                                       azalea greens of its crown: art/sapling_concepts/olive_sapling_v2*.png
python tools/sapling_concepts.py fig -> five fig saplings after the grown tree of the mod:
                                       art/sapling_concepts/fig_sapling.png
python tools/sapling_concepts.py fig2 -> five mixes of fig A and B: art/sapling_concepts/fig_sapling_v2.png
python tools/sapling_concepts.py fig3 -> M3 with one crown per stem, three ways: art/sapling_concepts/fig_sapling_v3.png
python tools/sapling_concepts.py fig4 -> M3 with a hump over every stem, stems closer: fig_sapling_v4.png
python tools/sapling_concepts.py fig5 -> that crown over five branchings that are not a chandelier: fig_sapling_v5.png
python tools/sapling_concepts.py fig6 -> that crown over the wood of five grown figs (side view under each):
                                       fig_sapling_v6.png
python tools/sapling_concepts.py palm / berry -> five date palm / strawberry tree saplings after the grown trees,
                                       the side view of each growth under it: date_palm_sapling.png,
                                       strawberry_tree_sapling.png
python tools/sapling_concepts.py palm2 -> P1 on five curved single trunks: date_palm_sapling_v2.png
python tools/sapling_concepts.py palm3 -> the finished palm under five crowns: date_palm_sapling_v3.png
python tools/sapling_concepts.py cypress -> five cypresses after the grown tree: cypress_sapling.png
python tools/sapling_concepts.py berry2 -> five variations of the current strawberry tree: strawberry_tree_sapling_v2.png
python tools/sapling_concepts.py berry3 -> no root, two stems, crowns at different heights: strawberry_tree_sapling_v3.png
python tools/sapling_concepts.py berry4 -> five variations of berry3 A: strawberry_tree_sapling_v4.png
python tools/sapling_concepts.py berry5 -> those with thicker stems and smooth bark: strawberry_tree_sapling_v5.png
python tools/sapling_concepts.py berry6 -> every stem 2 px: strawberry_tree_sapling_v6.png
python tools/sapling_concepts.py berry7 -> three crowns at different heights: strawberry_tree_sapling_v7.png
python tools/sapling_concepts.py aries3 -> the Aries oak A, bigger: aries_oak_sapling_v3.png
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_textures as mt  # noqa: E402

OUT = os.path.join(mt.ART, 'sapling_concepts')

# ---------------------------------------------------------------- palettes

AZ = {'1': (46, 60, 32), '2': (58, 76, 38), '3': (80, 105, 44), '4': (108, 128, 49), '5': (112, 146, 45)}
# Aries oak: azalea greens, jungle greens (j J), flowering azalea pinks (p f F), dark oak bark (a b c d), stripped
# dark oak (s S), vine greens (v V), glow berries (r o O), moss (m M)
ARIES = {**AZ, 'j': (52, 73, 20), 'J': (98, 128, 26), 'p': (158, 80, 136), 'f': (186, 98, 206), 'F': (208, 123, 227),
         'a': (41, 32, 17), 'b': (51, 39, 21), 'c': (74, 56, 30), 'd': (88, 68, 40), 's': (82, 63, 39),
         'S': (110, 86, 54), 'v': (72, 97, 36), 'V': (80, 114, 51), 'r': (164, 100, 34), 'o': (235, 137, 49),
         'O': (247, 226, 107), 'm': (73, 94, 39), 'M': (100, 114, 51)}
# weeping willow: azalea greens, pale oak bark (a b c d), catkins (k K y)
WILLOW = {**AZ, 'a': (58, 51, 49), 'b': (78, 67, 64), 'c': (94, 83, 80), 'd': (110, 100, 98),
          'k': (186, 184, 160), 'K': (222, 218, 190), 'y': (214, 196, 96)}

ARIES_IDEAS = [
    ('A Kleine Widdereiche', 'das Bild des Baums: Kuppel, zwei Seitenkronen, Stamm mit Wurzelanlauf', [
        '................',
        '.....455454.....',
        '...34f5445543...',
        '..3454J5445f43..',
        '..245JjJ445454..',
        '..2344J454f432..',
        '...1233cb33221..',
        '.454...cb...454.',
        '4f454..bc..45f54',
        '.2332c.cb.c2332.',
        '......ccbc......',
        '.......cb.......',
        '.......bs.......',
        '.......cb.......',
        '......cbsc......',
        '....cdbaabdc....',
    ]),
    ('B Widderhörner', 'zwei gerillte Hörner rollen sich zu beiden Seiten ein, oben ein blühender Schopf', [
        '......4554......',
        '....345f4543....',
        '...345J45f543...',
        '..SddS2432SddS..',
        '.dSddSdbcdSddSd.',
        'S....S.cb.S....S',
        'd..dS..cb..Sd..d',
        'S.S.d..bc..d.S.S',
        'dS..d..cb..d..Sd',
        '.dSSd..bc..dSSd.',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '.......bc.......',
        '......cbsc......',
        '.....cba.bc.....',
    ]),
    ('C Leuchtbeeren', 'runde blühende Krone, drei Leuchtbeerenranken, Moos am Fuß', [
        '................',
        '....3455453.....',
        '..34f5445f543...',
        '.345J4f454J543..',
        '.24JjJ454f45432.',
        '.123443J443321..',
        '..v.1233c3321...',
        '..V..v.cb..V....',
        '..v..V.bc..v....',
        '..o..v.cb..V....',
        '..O..o.bc..o....',
        '.....O.cb..O....',
        '.......bc.......',
        '.......cb.......',
        '.....MmcbmM.....',
        '....mMmMmMmm....',
    ]),
    ('D Knorriger Stamm', 'dicker Stamm mit Rindenstreifen, Knolle und Wurzeln, flache Krone', [
        '................',
        '................',
        '...3454f4543....',
        '.34545J45f4543..',
        '.23J4JjJ445432..',
        '..1223443s3221..',
        '.....bcsdb......',
        '....cbsdcb......',
        '....bcsbcbd.....',
        '...dbcSdcb......',
        '....bcsbcb......',
        '....cbsdbcb.....',
        '...cbcsdcbc.....',
        '..cbdbsbcbdc....',
        '.cb.dbcsbd.bc...',
        'c...cb..bc...c..',
    ]),
    ('E Azaleenbusch', 'dichter Busch voller Blüten mit Dschungel-Flecken auf kurzem Stamm', [
        '................',
        '.....4f54.......',
        '...345F4f54.....',
        '..3f54J45F543...',
        '.345JjJ4f454f3..',
        '.24f4J454F4543..',
        '.12345f45453f2..',
        '..1223F4J45432..',
        '...1123344f21...',
        '.....1223321....',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '.......bs.......',
        '......cbbc......',
        '.....cba.bc.....',
    ]),
]

CURTAIN = [
    '................',
    '......4554......',
    '....34554543....',
    '..345455454543..',
    '.34543.c..34543.',
    '.34.43.c..34.43.',
    '.43.34.c..43.34.',
    '.33.33.cb.33.33.',
    '.32.32.bc.23.23.',
    '.23.2..cb.23.22.',
    '.12.2..bc..2.21.',
    '..2.1..cb..2.1..',
    '..1....bc..1....',
    '.......cb.......',
    '.......bc.......',
    '......cabc......',
]


def leaning(rows):
    """The curtain one block to the left, its trunk replaced by one that leans in steps, a knee at each."""
    grid = [list(('.' + row[1:] + '.')[1:]) for row in rows]  # shifted left by one
    grid = [['.' if ch in 'abcd' else ch for ch in row] for row in grid]
    trunk = {4: {6: 'c'}, 5: {6: 'c'}, 6: {6: 'c', 7: 'b'}, 7: {7: 'c'}, 8: {7: 'c', 8: 'b'}, 9: {7: 'b', 8: 'c'},
             10: {8: 'c', 9: 'b'}, 11: {8: 'b', 9: 'c'}, 12: {8: 'c', 9: 'b'}, 13: {8: 'b', 9: 'c'},
             14: {8: 'c', 9: 'b'}, 15: {7: 'c', 8: 'a', 9: 'b', 10: 'c'}}
    for y, cells in trunk.items():
        for x, ch in cells.items():
            grid[y][x] = ch
    return [''.join(row) for row in grid]


LEANING = leaning(CURTAIN)

WILLOW_IDEAS = [
    ('A Fontäne', 'die bisherige Form, nur in Blasseiche und Azalee: Ruten fallen nach allen Seiten', [
        '................',
        '......545.......',
        '....5443445.....',
        '...44.3c3.44....',
        '..43..3c3..34...',
        '..4..4.c.4..4...',
        '.43..3.c.3..34..',
        '.4..43.c.34..4..',
        '.3..3..cb.3..3..',
        '.3..2..bc.2..3..',
        '.2..2..cb..2.2..',
        '....2..bc.....2.',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '.......ab.......',
    ]),
    ('B Vorhang', 'gewölbte Krone wie beim Baum, Ruten hängen senkrecht als Vorhang', CURTAIN),
    ('C Schiefer Stamm', 'der Vorhang von B, der Stamm lehnt sich in Stufen mit Knie zur Seite', LEANING),
    ('D Bögen', 'Äste steigen aus dem Stamm und biegen sich nach unten, Ruten hängen von den Bögen', [
        '................',
        '...45.4554.54...',
        '...ccc.cb.ccc...',
        '..c4.3ccbc3.4c..',
        '.c34.4.cb.4.43c.',
        '.4.3.3.bc.3.3.4.',
        '.3.4.3.cb.3.4.3.',
        '.3.3.2.bc.2.3.3.',
        '.2.3...cb...3.2.',
        '.2.2...bc...2.2.',
        '.1.2...cb...2.1.',
        '...1...bc...1...',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '......cabc......',
    ]),
    ('E Kätzchen', 'junge, schlanke Rute mit wenigen Zweigen, an den Enden kleine Weidenkätzchen', [
        '................',
        '.......4........',
        '.....45c54......',
        '....4..c..4.....',
        '...4.3.c...4....',
        '..43.3.c..3.4...',
        '..3..2.cb.2.3...',
        '.43..K.bc.2.34..',
        '.2...y.cb.K..3..',
        '.K.....bc.y..2..',
        '.y.....cb....K..',
        '.......bc....y..',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '......cabc......',
    ]),
]

# ---------------------------------------------------------------- round 2: variants of the picks


def strands(rows, cols):
    """Hangs leaf strands into rows: cols maps a column to its first and last row; light at the top, darker down."""
    grid = [list(row) for row in rows]
    for x, (y0, y1) in cols.items():
        n = y1 - y0 + 1
        for k in range(n):
            t = k / max(1, n - 1)
            ch = ('4' if (x + k) % 2 == 0 else '3') if t < 0.3 else '3' if t < 0.55 else '2' if t < 0.85 else '1'
            if grid[y0 + k][x] == '.':
                grid[y0 + k][x] = ch
    return [''.join(row) for row in grid]


ARIES_V2 = [
    ('Jetzt: A', 'die gewählte kleine Widdereiche, zum Vergleich', ARIES_IDEAS[0][2]),
    ('A1 Hochstamm', 'längerer Stamm, kleinere Kuppel, die Seitenkronen auf verschiedenen Höhen wie am Baum', [
        '......4554......',
        '....345f4543....',
        '...3454J45f43...',
        '...245JjJ4543...',
        '....2344f432....',
        '.45...1cb1......',
        '4f54...cb.......',
        '2332c..bc.......',
        '.....cccb...454.',
        '.......bc..45f54',
        '.......cbcc2332.',
        '.......bs.......',
        '.......cb.......',
        '.......bs.......',
        '......cbsc......',
        '...ccdbaabdcc...',
    ]),
    ('A2 Mit Leuchtbeeren', 'A, unter den Seitenkronen hängen Ranken mit Leuchtbeeren', [
        '................',
        '.....455454.....',
        '...34f5445543...',
        '..3454J5445f43..',
        '..245JjJ445454..',
        '..2344J454f432..',
        '...1233cb33221..',
        '.454...cb...454.',
        '4f454..bc..45f54',
        '.2332c.cb.c2332.',
        '..v...ccbc...v..',
        '..V....cb....V..',
        '..o....bs....v..',
        '..O....cb....o..',
        '......cbsc...O..',
        '....cdbaabdc....',
    ]),
    ('A3 Weit ausladend', 'kleinere Kuppel, die Seitenkronen tiefer und bis an den Rand, mehr Dschungel-Flecken', [
        '................',
        '.....455454.....',
        '...34J5445f43...',
        '..3454Jj445J43..',
        '..2f5JJ454f542..',
        '...1233cb33221..',
        '.......cb.......',
        '.45....bc....54.',
        '4554...cb...4f54',
        'f4J54..bc..54J45',
        '23322cccbcc22332',
        '.......cb.......',
        '.......bs.......',
        '......cbbc......',
        '.....cbsdbc.....',
        '...ccdbaabdcc...',
    ]),
]

WILLOW_V2 = [
    ('Jetzt: B', 'der gewählte Vorhang, zum Vergleich', CURTAIN),
    ('B1 Lang und dicht', 'flachere Krone, mehr Ruten, die längsten fast bis zum Boden', strands([
        '................',
        '.....345543.....',
        '...3455445543...',
        '.33454554545433.',
        '3454543c.3454543',
        '.......c........',
        '.......c........',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '.......bc.......',
        '......cabc......',
    ], {0: (5, 9), 1: (5, 13), 3: (5, 12), 4: (5, 10), 5: (5, 7),
        10: (5, 8), 11: (5, 11), 12: (5, 13), 14: (5, 12), 15: (5, 9)})),
    ('B2 Mit Bögen', 'unter der Krone kommen die Äste als Bögen heraus, die Ruten hängen von ihnen', [
        '......4554......',
        '...3455445543...',
        '..345545545543..',
        '..3ccc4cb4ccc3..',
        '.3c34.ccbc.43c3.',
        '.c43.4.cb.4.34c.',
        '.4.3.3.bc.3.3.4.',
        '.3.4.3.cb.3.4.3.',
        '.3.3.2.bc.2.3.3.',
        '.2.3...cb...3.2.',
        '.2.2...bc...2.2.',
        '.1.2...cb...2.1.',
        '...1...bc...1...',
        '.......cb.......',
        '.......bc.......',
        '......cabc......',
    ]),
    ('B3 Mit Knie', 'Stamm mit einem Knie wie die neuen krummen Stämme, Krone und Ruten zur Seite geneigt', strands([
        '................',
        '.....4554.......',
        '...345545543....',
        '..34554554543...',
        '.3454354c.3454..',
        '........c.......',
        '........c.......',
        '.......bc.......',
        '......cb........',
        '......bc........',
        '......cb........',
        '......bc........',
        '......cb........',
        '......bc........',
        '......cb........',
        '.....cabc.......',
    ], {1: (5, 13), 2: (5, 10), 4: (5, 12), 5: (5, 7), 10: (5, 9), 11: (5, 11), 13: (5, 8)})),
]

# ---------------------------------------------------------------- round 3: the willow with a curved trunk

CROWN = ['......4554......', '....34554543....', '..345455454543..', '.34543....34543.']  # rows 1-4 of CURTAIN
CURTAIN_STRANDS = {1: (5, 10), 2: (5, 12), 4: (5, 11), 5: (5, 8), 10: (5, 9), 11: (5, 12), 13: (5, 11), 14: (5, 10)}


def curved(centres, crown_dx=0, extra=None):
    """The curtain willow with its trunk along centres (one function per stem: row -> middle of the stem), one
    pixel wide up to row 6, two below, a flared foot; crown and strands moved by crown_dx, a strand stops above the
    trunk where it would run into it."""
    grid = [['.'] * 16 for _ in range(16)]
    for k, row in enumerate(CROWN):
        for x, ch in enumerate(row):
            if ch != '.' and 0 <= x + crown_dx < 16:
                grid[k + 1][x + crown_dx] = ch
    trunk = {}
    for centre in centres:
        thin = 12 if len(centres) > 1 else 6  # the last row one pixel wide
        xs = {y: math.floor(centre(y)) if y <= thin else math.floor(centre(y) - 0.5) for y in range(4, 16)}
        # the first wide row takes the side that lines up with the row below, so the stem widens without a bump
        xs[thin + 1] = min((xs[thin] - 1, xs[thin]), key=lambda v: abs(v - xs[thin + 2]))
        for y, x in xs.items():
            if y <= thin:
                trunk[(x, y)] = 'c'
            else:
                trunk[(x, y)] = 'd' if y % 3 == 0 else 'c'
                trunk[(x + 1, y)] = 'b'
    foot = sorted(x for x, y in trunk if y == 15)
    trunk[(foot[0] - 1, 15)] = 'c'
    trunk[(foot[-1] + 1, 15)] = 'c'
    trunk[(foot[0], 15)] = 'a'
    cols = {x + crown_dx: span for x, span in CURTAIN_STRANDS.items() if 0 <= x + crown_dx < 16}
    cols.update(extra or {})
    for x, (y0, y1) in list(cols.items()):
        for y in range(y0, y1 + 1):
            if any((x + dx, y) in trunk for dx in (-1, 0, 1)):
                cols[x] = (y0, y - 1)
                break
    rows = strands([''.join(r) for r in grid], {x: span for x, span in cols.items() if span[1] >= span[0]})
    grid = [list(r) for r in rows]
    for (x, y), ch in trunk.items():
        grid[y][x] = ch
    return [''.join(r) for r in grid]


WILLOW_CURVED = [
    ('Jetzt: B', 'der gewählte Vorhang mit geradem Stamm, zum Vergleich', CURTAIN),
    ('K1 Bogen', 'der Stamm wölbt sich in einem weichen Bogen zur Seite', curved(
        [lambda y: 8 - 2.4 * math.sin(math.pi * (y - 4) / 11)])),
    ('K2 S-Kurve', 'der Stamm schwingt erst zur einen, dann zur anderen Seite', curved(
        [lambda y: 8 + 1.5 * math.sin(2 * math.pi * (y - 4) / 11)])),
    ('K3 Schräg aus dem Fuß', 'wie die neuen Stämme: verlässt den Fuß schräg und biegt sich senkrecht in die Krone',
     curved([lambda y: 9 - 3.2 * ((y - 4) / 11) ** 2], crown_dx=1)),
    ('K4 Über dem Wasser', 'stark gekrümmt, fast liegend am Fuß, die Krone hängt weit hinaus', curved(
        [lambda y: 10 - 6.2 * ((y - 4) / 11) ** 2.2], crown_dx=2, extra={15: (5, 12)})),
    ('K5 Zwei Triebe', 'zwei dünne Triebe aus einem Fuß, die sich auseinander- und wieder zusammenbiegen', curved(
        [lambda y: 8 - 1.7 * math.sin(math.pi * min(1, (y - 4) / 9)), lambda y: 8 + 1.7 * math.sin(math.pi * min(1, (y - 4) / 9))])),
]

# ---------------------------------------------------------------- round 4: fountain crown, C-curved trunk


def fountain(strands_, trunk, dome=((6, 9), (4, 11), (3, 12)), fill_gap=2):
    """A weeping willow: strands_ is a list of (column per row from row 1 on, last row); each strand starts near the
    top middle, arches out to its column and falls. Between neighbouring strands the crown is dark down to fill_gap
    rows above the shorter one, the dome on top is light, light comes from the upper left. trunk maps a row to the
    left column of the two-pixel trunk (it shows where the crown is dark or open)."""
    g = [['.'] * 16 for _ in range(16)]
    paths = []
    for xs, end in strands_:
        paths.append({y: xs[y - 1] if y - 1 < len(xs) else xs[-1] for y in range(1, end + 1)})
    paths.sort(key=lambda p: p[min(4, max(p))])
    for a, b in zip(paths, paths[1:]):
        for y in range(1, min(max(a), max(b)) - fill_gap + 1):
            for x in range(min(a[y], b[y]) + 1, max(a[y], b[y])):
                g[y][x] = '2' if y < 6 else '1'
    for y, (x0, x1) in enumerate(dome):
        for x in range(x0, x1 + 1):
            g[y][x] = '5' if x < 8 and (x + y) % 2 == 0 else '4'
    for p in paths:
        end = max(p)
        for y, x in p.items():
            t, left = y / end, x < 8
            g[y][x] = ('5' if left else '4') if t < 0.3 else ('4' if left else '3') if t < 0.7 else '3' if t < 0.92 else '2'
    for y, x0 in trunk.items():
        for k, x in enumerate((x0, x0 + 1)):
            if g[y][x] in '.12' or y >= 12:
                g[y][x] = ('d' if y % 3 == 0 else 'c') if k == 0 else 'b'
    g[15][trunk[15] - 1] = 'c'
    g[15][trunk[15] + 2] = 'c'
    g[15][trunk[15]] = 'a'
    return [''.join(r) for r in g]


C_LEFT = {7: 7, 8: 7, 9: 6, 10: 6, 11: 6, 12: 6, 13: 7, 14: 7, 15: 7}  # bows out to the left, a slight C
C_RIGHT = {7: 7, 8: 7, 9: 8, 10: 8, 11: 8, 12: 8, 13: 7, 14: 7, 15: 7}
INNER = [([7, 6, 5, 4], 11), ([7, 7, 6, 6], 8), ([8, 8, 9, 9], 8), ([8, 9, 10, 11], 11)]

WILLOW_FOUNTAIN = [
    ('Jetzt: B', 'der bisherige Vorhang, zum Vergleich', CURTAIN),
    ('W1 Dicht', 'gewölbte Kuppel, aus der die Ruten wie eine Fontäne nach außen und dann senkrecht fallen; '
                 'außen am längsten, in der Mitte frei für den Stamm mit leichtem C',
     fountain([([5, 3, 1, 0], 11), ([6, 4, 3, 2], 13)] + INNER + [([9, 11, 12, 13], 13), ([10, 12, 14, 15], 11)],
              C_LEFT)),
    ('W2 Lang', 'wie W1, die äußeren Ruten hängen bis fast zum Boden; das C des Stamms zur anderen Seite',
     fountain([([5, 3, 1, 0], 13), ([6, 4, 3, 2], 14)] + INNER + [([9, 11, 12, 13], 14), ([10, 12, 14, 15], 13)],
              C_RIGHT)),
    ('W3 Luftig', 'wie W1, die Ruten enden versetzt und hängen unten frei, der Stamm reicht bis in die Krone',
     fountain([([5, 3, 1, 0], 12), ([6, 4, 3, 2], 10), ([7, 6, 5, 4], 12), ([7, 7, 6, 6], 8), ([8, 8, 9, 9], 8),
               ([8, 9, 10, 11], 12), ([9, 11, 12, 13], 10), ([10, 12, 14, 15], 12)],
              {5: 7, 6: 7, **C_LEFT}, fill_gap=4)),
]

# ---------------------------------------------------------------- mulberry

# the mod's mulberry palette (pale oak bark a b c, jungle greens 1-5) with its fruit colours: white-green (w v),
# red (p r R), black (h k m); plus the orange of white mulberry bark in its furrows (o)
MULB = dict(mt.MULBERRY_FRUIT, o=(140, 94, 58))

MULBERRY_IDEAS = [
    ('A Runde Kuppel', 'kurzer dicker Stamm, tief gegabelt, dichte runde Krone breiter als hoch; Früchte in drei '
     'Reifestufen zugleich (weißgrün, rot, schwarz)', [
        '.....455454.....',
        '...3455455443...',
        '..345545345543..',
        '.34554323455543.',
        '.45543234554354.',
        '.34432123443243.',
        '.23321212332132.',
        '.12211212221121.',
        '..w11cb11cb11...',
        '..v.p.cbcba..h..',
        '....R..cba...k..',
        '.......cba......',
        '.......cba......',
        '.......cba......',
        '......ccbaa.....',
        '.....ccbbbaa....',
    ]),
    ('B Kopfbaum', 'die geschneitelte Maulbeere vom Dorfplatz: knotige Faust, daraus gerade Ruten, flacher Schirm',
     [
        '................',
        '..455455455454..',
        '.34554554545543.',
        '3455435455345543',
        '2343323443233432',
        '.12.b1.c.c1.b.1.',
        '.w..b..c.c..b.h.',
        '.v...b.c.c.b..k.',
        '......cbcb......',
        '.....cbcbba.....',
        '.....cbbaba.....',
        '......cbba......',
        '......cba.......',
        '......cba.......',
        '......cba.......',
        '.....ccbaa......',
    ]),
    ('C Junger Trieb', 'Zickzack-Trieb mit großen Herzblättern, eins gelappt wie ein Fäustling; Beeren in der '
     'Blattachsel', [
        '........45......',
        '.......354.45...',
        '........c.34554.',
        '.45.....cb.34554',
        '345.4..cb.344543',
        '344.45.c...2343.',
        '.34554bc....22..',
        '34554..cb.......',
        '.2343...c..44...',
        '..22....cb3454..',
        '.......cb..3454.',
        '......bc...24553',
        '.....h.c....2343',
        '....pk.cb....23.',
        '....r..cb.....2.',
        '......cbba......',
    ]),
    ('D Fruchtbehang', 'breite, lockere Krone, die Astspitzen hängen; voller Früchte in allen Stufen', [
        '....45545544....',
        '..345545545543..',
        '.34554354554554.',
        '3455432345543543',
        '4543212234432454',
        '3432111c1b112343',
        '232w1.cb.bc.h232',
        '21.v.p.cbcb.k.12',
        '2..h.R.cba..w..2',
        '1..k...cba..v..1',
        '.......cba......',
        '.......cba......',
        '.......cba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbaaa....',
    ]),
    ('E Alte Schwarze Maulbeere', 'knorrig und schief: Stamm mit Knolle und orangen Furchen lehnt sich, die Krone '
     'hängt zur Seite, dunkles raues Laub, Früchte rot und schwarz', [
        '........34543...',
        '.....34454445433',
        '...2344345444543',
        '..23443234544432',
        '..12332123443321',
        '...1221c112332h1',
        '...h..cb.b1.1.k.',
        '...k...cbbc..p..',
        '........cba..R..',
        '.......cboa.....',
        '......ccba......',
        '.....cbob.......',
        '....ccbbaa......',
        '....cboba.......',
        '...ccbbaa.......',
        '..ccbbbaaa......',
    ]),
]

# ---------------------------------------------------------------- olive

# the mod's olive palette: silvery greens 1-5, oak bark a b c, green olives (d g G), purple (h m) and black (k)
OLIV = mt.OLIVE_ITEM_PAL

OLIVE_IDEAS = [
    ('A Offene Vase', 'wie im griechischen Hain geschnitten: kurzer Stamm, drei Leitäste nach außen, Mitte offen, '
     'Wurzeln am Boden', [
        '......4554......',
        '.....354453.....',
        '.45..245342.54..',
        '45543.2332.45545',
        '35425...c..35453',
        '24342...c..24352',
        '.122cb..c..cb21.',
        '.Gd..cb.c.cb.mh.',
        '.g....cbccb..km.',
        '.......ccba.....',
        '.......cba......',
        '.......cba......',
        '.......cba......',
        '......ccbaa.....',
        '....bccbbaab....',
        '...ab..cba..ba..',
    ]),
    ('B Uralter Ölbaum', 'mächtiger, gedrehter Stamm, hohl und in zwei Stränge gespalten, darüber eine kleine '
     'lockere Krone', [
        '...45......45...',
        '..4554....4554..',
        '.345543..354532.',
        '..24342..243421.',
        '...12.c..c.21...',
        '..g..cb..bc..m..',
        '..G..cbc.bc..k..',
        '....ccba.cbba...',
        '...cbba...cbba..',
        '...cba.....cba..',
        '...cbb.....cba..',
        '...ccba...cbba..',
        '....cbba.cbaa...',
        '...ccbbacbbaa...',
        '..ccbcbbabcbaa..',
        '.cbbcabaabbabaa.',
    ]),
    ('C Junger Strauch', 'drei dünne Triebe aus einem Fuß, schmale Blätter paarweise, oben dunkel, unten silbern; '
     'erste Oliven', [
        '.....5.4.5......',
        '......354.......',
        '5.4.524.435.4.5.',
        '.354...c...354..',
        '24.43..c..24.43.',
        '..c..5.c.2..b...',
        '.5.c..3c4..b.5..',
        '..3c...c...b3...',
        '....c2.c.5b.....',
        '....c.4c3.b.....',
        '...G.c.c.b.gm...',
        '...g.c.c.b.dk...',
        '......ccb.......',
        '.......cb.......',
        '.......cb.......',
        '......cbba......',
    ]),
    ('D Silberkugel', 'junger veredelter Baum: gerader schlanker Stamm, runde silbrige Krone, Oliven grün, '
     'violett und schwarz', [
        '.....45545......',
        '...3455445543...',
        '..3455.5544554..',
        '.34552455345543.',
        '.45543345543.54.',
        '.24543234554432.',
        '.234321234.3321.',
        '..232121232321..',
        '...1G21cb121h...',
        '....g..cb.m.m...',
        '.......cb.k.....',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
        '......ccba......',
        '.....cbbbaa.....',
    ]),
    ('E Windgeformt', 'vom Meerwind gebeugt: gedrehter Stamm lehnt sich, die Krone weht zur Seite und zeigt die '
     'silbernen Blattunterseiten', [
        '................',
        '.......34545....',
        '....2345455454..',
        '..12345455455454',
        '...123434545345.',
        '....1221c2343421',
        '.......cb.12.1m.',
        '......cb.c....k.',
        '.....cbc........',
        '.....cba........',
        '....cbca........',
        '....cba.........',
        '...ccba.........',
        '...cbca.........',
        '..ccbbaa........',
        '.abccbbaab......',
    ]),
]

# round 2: the grown tree of the mod (TreeShapes.olive, concept/selftest_olive.png) in small: a wide foot of roots
# on the ground, a narrow neck, a thicker trunk forking into 2-3 kneed stems (sometimes with a hole between them), a
# flat layered crown much wider than tall, olives hanging under its rim
OLIVE_GAME = [
    ('A Zwei Stämme', 'tiefe Gabel, ein Stamm gerade, einer mit Knie; zwei flache Kronen auf verschiedener Höhe', [
        '..455...45545...',
        '.34554.3455454..',
        '3455543345545543',
        '2344332234434432',
        '.k1c2.1121b12k..',
        '.m.cb.....b..m..',
        '....cb....b.....',
        '.....c....b.....',
        '.....cb...b.....',
        '......c..cb.....',
        '......cbcba.....',
        '.......cba......',
        '.......cb.......',
        '.......cb.......',
        '....ccbbbaa.....',
        '...cbbbbbaaa....',
    ]),
    ('B Stamm mit Loch', 'schmaler Hals über dem Wurzelfuß, darüber ein dicker Stamm mit Loch; Krone mit zwei '
     'Buckeln, ein Ast schaut heraus', [
        '..4554....4554..',
        '.34554543455455.',
        '3455454554554543',
        '2345434454543432',
        '.2332k23322cb21.',
        '..1..m.c1ba.....',
        '.....ccbbab.....',
        '.....cb.bab.....',
        '.....cbkba......',
        '.....ccbba......',
        '......cba.......',
        '.......cb.......',
        '.......cb.......',
        '.....ccbbaa.....',
        '....cbbbbbaa....',
        '...cbbbbbbbaa...',
    ]),
    ('C Gedrungen', 'kurzer dicker Stamm, die breite flache Krone hängt auf einer Seite tiefer', [
        '................',
        '......45545545..',
        '....345545454554',
        '..34554545455455',
        '3455454554554543',
        '2344543234433432',
        '34543321.cbb21..',
        '2332k1..cbba....',
        '.12.m..cbbba....',
        '.......cbba.....',
        '.......cbba.....',
        '........cb......',
        '........cb......',
        '......ccbbaa....',
        '.....cbbbbbaa...',
        '....cbbbbbbbaa..',
    ]),
    ('D Drei Stämme', 'drei Stämme aus einer kurzen Gabel, jede Krone auf eigener Höhe, zusammen ein flacher '
     'Schirm', [
        '.....45545......',
        '....34554543....',
        '.....23432.45545',
        '..455.1c1.345454',
        '.345545c.2344332',
        '3455454c..12b1..',
        '2344332c..k.b.m.',
        '.k1c21.c..m.b.k.',
        '.m..c..c...b....',
        '.....c.c..b.....',
        '......ccbb......',
        '.......cba......',
        '.......cb.......',
        '.......cb.......',
        '.....ccbbaa.....',
        '....cbbbbbaa....',
    ]),
    ('E Schräg mit Ast', 'der Stamm knickt schräg zur Seite, ein Ast trägt die Krone, eine kleine Wolke hängt '
     'tiefer daneben', [
        '.......4554.....',
        '....3455455454..',
        '...345545545455.',
        '..34554343454554',
        '.45233211c234332',
        '34554..cb.12.k..',
        '23432.cb.....m..',
        '.k21c.cb........',
        '.m...cb.........',
        '.....cbb........',
        '......cbb.......',
        '.......cba......',
        '.......cb.......',
        '.......cb.......',
        '.....ccbbaa.....',
        '....cbbbbbaa....',
    ]),
]
# the same in the colours the grown tree really has: azalea leaves instead of the silvery greens
OLIV_AZALEA = dict(OLIV, **mt.AZALEA_LEAF)

# ---------------------------------------------------------------- fig

# the grown fig of the mod (TreeShapes.fig, concept/selftest_fig.png) in small: low and wider than tall, a short thick
# grey trunk whose stems spread almost flat with holes between them, a flat mound of leaves, figs under its rim.
# Palette: azalea greens 1-5, grey bark a b c, green figs (G g d), ripe purple (h m k)
FIG_GAME = [
    ('A Kandelaber', 'kurzer Stamm, vier Äste erst flach nach außen, dann gerade hoch; Löcher dazwischen, '
     'darüber ein flacher Laubhügel', [
        '................',
        '.....4554554....',
        '...34554554545..',
        '.34554545545545.',
        '3455454554554543',
        '2345432345434432',
        '.23c21c22b21b21.',
        '.m.c..c..b..b.h.',
        '.k.c..c..b..b.k.',
        '...c..c..b..b...',
        '...ccccbbbbbb...',
        '....abbcbbaaa...',
        '......cbba......',
        '......cbba......',
        '.....ccbbaa.....',
        '....cbbbbbaa....',
    ]),
    ('B Breiter Hügel', 'gewölbter Laubhügel, der Stamm wird nach oben breiter wie ein V, ein kleines Loch darin',
     [
        '......4554......',
        '....34554543....',
        '..345545545543..',
        '.34554545545455.',
        '3455454554554543',
        '3454543454545432',
        '2343323c22343321',
        '.12m1cbbba.1k21.',
        '...k.cbcbba..m..',
        '......cb.ba.....',
        '......cbba......',
        '.......cba......',
        '.......cba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
    ('C Feigenblätter', 'der Hügel aus großen gelappten Feigenblättern wie am echten Baum, drei Stämmchen', [
        '.....4.5.4......',
        '.....45554......',
        '.4.5.445434.5.4.',
        '.45554343.45554.',
        '.34543.22.34543.',
        '3.343334233343.3',
        '3444334443334443',
        '2343223432223432',
        '.232..232..b232.',
        '.m.c...b.h.b.G..',
        '.km.cb.b.kb..g..',
        '.....cbbab......',
        '......cba.......',
        '......cba.......',
        '......cba.......',
        '.....cbbbba.....',
    ]),
    ('D Niedriger Busch', 'ganz flach und breit, das Laub hängt an den Seiten fast bis zum Boden, voller Feigen', [
        '................',
        '................',
        '.....455454.....',
        '...3455455443...',
        '.34554554554543.',
        '3455454554554543',
        '4554543455455454',
        '3454332344343443',
        '2343m11c2b11h342',
        '232.k.cbba..k.21',
        '1G...cbbba....1.',
        '.g....cba.......',
        '......cba.......',
        '......cba.......',
        '.....ccbaa......',
        '....cbbbbaa.....',
    ]),
    ('E Wolken und Kappe', 'wie der Code baut: eine Laubwolke auf jeder Stammspitze, eine Kappe in der Mitte, '
     'Lücken dazwischen', [
        '................',
        '................',
        '......4554......',
        '.....345543.....',
        '.45..344543..54.',
        '4554.234432.4554',
        '34543.1221.34543',
        '23432..cb..23432',
        '.m1c...cb...c1h.',
        '.k.c...cb...c.k.',
        '...c...cb...c...',
        '...ccbbcbbbbc...',
        '....abbcbbaa....',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
]

# round 2: mixes of A (arms flat out, then up, holes between) and B (domed mound, trunk widening like a V, a hole)
FIG_MIX = [
    ('M1 Dreizack', 'Kuppel von B; in der Mitte das V, außen zwei Arme von A erst flach, dann hoch', [
        '......4554......',
        '....34554543....',
        '..345545545543..',
        '.34554545545455.',
        '3455454554554543',
        '3454543454545432',
        '23c3323cb2343b21',
        '.1c.m.cbba.1.bk.',
        '..c.k..cba...b..',
        '..c....cba...b..',
        '..ccbbbcbabbbb..',
        '...abbbcbaaaa...',
        '.......cba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
    ('M2 V mit Fingern', 'der V-Stamm von B teilt sich oben in vier Finger mit Löchern wie bei A, flacher Hügel '
     'von A', [
        '................',
        '.....4554554....',
        '...34554554545..',
        '.34554545545545.',
        '3455454554554543',
        '2345432345434432',
        '.23c2c1221b1b21.',
        '.m.c.c....b.b.h.',
        '.k.ccb....bba.k.',
        '....cbb..bba....',
        '.....cbbbba.....',
        '......cbba......',
        '.......cba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
    ('M3 Kandelaber mit Loch', 'die vier Arme von A, aber aus einem V gewachsen, das Loch von B in der Gabel; '
     'Kuppel von B', [
        '......4554......',
        '....34554543....',
        '..345545545543..',
        '.34554545545455.',
        '3455454554554543',
        '3454543454545432',
        '2c33c232232b32b1',
        '.c.mc......b.kb.',
        '.c.kcb....bb..b.',
        '.cc..cb..bb..bb.',
        '..cccbcb.bbbbb..',
        '....abbcbbaa....',
        '......cbba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
    ('M4 Halb und halb', 'links ein Arm von A flach hinaus und hoch, rechts das V von B mit Loch; Kuppel von B', [
        '.....45545......',
        '...3455455443...',
        '..345545545543..',
        '.34554545545455.',
        '3455454554554543',
        '3454543454545432',
        '2c4332cbbba33321',
        '.c.m..cb.ba.h...',
        '.c.k...cbba.k...',
        '.cc....cba......',
        '..cccbbcba......',
        '....abbcba......',
        '.......cba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
    ('M5 Weite Gabel', 'das V von B weit geöffnet, die Arme laufen schräg bis an den Kronenrand, ein Stämmchen '
     'in der Mitte; Kuppel von B', [
        '......4554......',
        '....34554543....',
        '..345545545543..',
        '.34554545545455.',
        '3455454554554543',
        '3454543454545432',
        '23c2332cb2332b21',
        '.mcc...cb...bbh.',
        '.k.cc..cb..bb.k.',
        '....cc.cb.bb....',
        '.....ccbbba.....',
        '......cbba......',
        '.......cba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
]

# round 3: M3's trunk pulled together (the inner stems one thick trunk, no hole in the middle) with a leaf crown on
# every stem, the crowns running into each other (each light on top with a dark rim underneath, so they stay apart),
# like TreeShapes.fig: a cloud per stem tip and a cap in the middle
FIG_CROWNS = [
    ('M3 (bisher)', 'zum Vergleich: ein durchgehender Laubhügel', FIG_MIX[2][2]),
    ('K1 Vier Kronen', 'eine Krone pro Stamm: die inneren höher und hinten, die äußeren tiefer und davor', [
        '...4434..4344...',
        '..455554455554..',
        '..344443444434..',
        '.55533332333555.',
        '4444322112244434',
        '2333121111213332',
        '12221.cbcb.12221',
        '..1.m.cbcb.h.1..',
        '..c.k.cbcb.k.b..',
        '..cc..cbba..bb..',
        '...cccbbbabbb...',
        '.....cbbbaa.....',
        '......cbba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
    ('K2 Mit Kappe', 'dazu die Kappe in der Mitte obendrauf, wie der Code den Baum baut', [
        '......4444......',
        '....44555543....',
        '..355553455554..',
        '.44344443444434.',
        '4555233112335554',
        '2333322112233332',
        '122211cbcb112221',
        '..c.m.cbcb.h.b..',
        '..c.k.cbcb.k.b..',
        '..cc..cbba..bb..',
        '...cccbbbabbb...',
        '.....cbbbaa.....',
        '......cbba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
    ('K3 Ungleich hoch', 'jede Krone auf eigener Höhe, die rechte innere am höchsten', [
        '.........4554...',
        '....44.4455554..',
        '...55553444434..',
        '..43444413334554',
        '.554233312224434',
        '3444422122113332',
        '123311c11b...11.',
        '.11.m.cbcb.h.b..',
        '..c.k.cbcb.k.b..',
        '..cc..cbba..bb..',
        '...cccbbbabbb...',
        '.....cbbbaa.....',
        '......cbba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
]

# round 4: M3 as it was (bright crown, thin stems), the stems moved closer so the middle has no hole, and the crown
# bulging up over every stem (four humps that run into each other, a shade darker where they meet)
FIG_M3_HUMPS = [
    ('M3 (bisher)', 'zum Vergleich', FIG_MIX[2][2]),
    ('M3 neu', 'Stämme enger zusammen, kein Loch in der Mitte; über jedem Stamm wölbt sich eine eigene Krone, '
     'die Kronen gehen ineinander über', [
        '....454..454....',
        '...4554334554...',
        '.45.55443554.45.',
        '3553454545443543',
        '3454454554554543',
        '3454543454545432',
        '23c323c22b323b31',
        '..c.m.c..b.h.b..',
        '..c.k.cbba.k.b..',
        '..cc...cb...bb..',
        '...ccccbbbbba...',
        '.....cbbbaa.....',
        '......cbba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
]

# round 5: the crown of "M3 neu" unchanged, five branchings under it that are not a chandelier (no arms that go out
# flat and then straight up); the inner stems stay close, so the middle has no hole
_HUMPS = FIG_M3_HUMPS[1][2][:6]
FIG_BRANCHES = [
    ('M3 neu', 'zum Vergleich', FIG_M3_HUMPS[1][2]),
    ('V1 Fächer', 'gerade Stämme fächern aus einer Gabel schräg nach oben, ohne Knick', _HUMPS + [
        '23c223c22c223c31',
        '.m.c..c..c..c.h.',
        '.k..c..cb..c..k.',
        '.....c.cb.c.....',
        '......cbba......',
        '......cbba......',
        '......cbba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
    ('V2 Ungleich', 'ein langer Ast zweigt tief nach links ab, rechts einer weiter oben, die Mitte teilt sich '
     'spät', _HUMPS + [
        '23c23c222c223c31',
        '..c.m.c..c..c.h.',
        '...ck..cb..c..k.',
        '...c...cb.c.....',
        '....c..cbb......',
        '.....c.cba......',
        '......cbba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
    ('V3 Gebogen', 'die Stämme kommen oben senkrecht aus der Krone und biegen sich weich zur Gabel', _HUMPS + [
        '23c223c22c223c31',
        '..c.m.c..c.h.c..',
        '...ck..cb..kc...',
        '....c..cb..c....',
        '.....c.cb.c.....',
        '......cbba......',
        '......cbba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
    ('V4 Astgabel', 'wie ein Baum: der Stamm gabelt sich in zwei Äste, jeder teilt sich unter der Krone noch '
     'einmal', _HUMPS + [
        '233c23c22c22c331',
        '..m.c.c..c.c.h..',
        '..k..cb..cb..k..',
        '......cbcb......',
        '......cbba......',
        '......cbba......',
        '......cbba......',
        '.......cba......',
        '......ccbaa.....',
        '.....cbbbbaa....',
    ]),
    ('V5 Schief', 'der Stamm wächst schräg nach rechts oben, die Äste zweigen auf verschiedenen Höhen ab, '
     'der längste tief nach links', _HUMPS + [
        '23c223c223c22c31',
        '.m.c..c..cb.c.h.',
        '.k.c...cbb.c..k.',
        '....c...cbb.....',
        '.....c.cb.......',
        '......cbb.......',
        '......cba.......',
        '.....cba........',
        '....ccbaa.......',
        '...cbbbbaa......',
    ]),
]

# round 6: the wood as the grown fig really has it (run/greektrees-selftest/fig_*.json, side views): a short broad
# fan, 2-3 blocks wide at the ground, 6-7 under the crown, the stems parting only in the crown's lower edge; the crown
# low and wide on top of it, the figs at its rim next to the stems. Crown of "M3 neu" kept. Each after one growth.
_CROWN = _HUMPS + ['3455454554554543', '2343323443233432']  # the crown of "M3 neu", two rows deeper
FIG_GROWN = [
    ('F1 nach Wuchs 2', 'gleichmäßig: das Holz wird gleich über dem Boden breit, die Stämme trennen sich erst im '
     'unteren Rand der Krone', _CROWN + [
        '.1m1c1cbcb1c1h1.',
        '..k.cbcbcbcb.k..',
        '....cbcbcbcb....',
        '....cbcbcbba....',
        '.....cbcbba.....',
        '.....cbcbba.....',
        '......cbba......',
        '......cbba......',
    ], 1),
    ('F2 nach Wuchs 1', 'die Krone hängt links tiefer, darunter ein Büschel Feigen; im Holz ein kleines Loch',
     _CROWN + [
        '3442cb1121c111h1',
        '2m21cbbb.cb...k.',
        '.km.cbcbcbba....',
        '..k.cbcbcbba....',
        '.....cbcbba.....',
        '......cbcba.....',
        '......cbba......',
        '......cbba......',
    ], 0),
    ('F3 nach Wuchs 3', 'links steigt ein eigener Stamm senkrecht aus dem Fuß bis in die Krone, im Fächer Lücken',
     _CROWN + [
        '1mc21121cb121h21',
        '.kc..c..cb.cb.k.',
        '..c..cbcb.cb....',
        '..c..cbcbcba....',
        '..cbcbcbcbba....',
        '...cbcbcbba.....',
        '.....cbcba......',
        '.....cbcba......',
    ], 2),
    ('F4 nach Wuchs 5', 'gedrungen: kleine Kuppe oben, die Krone hängt tief, die Feigen ganz unten am Holz', [
        '................',
        '......454.......',
        '...4554554554...',
        '.34554545545455.',
        '3455454554554543',
        '3454543454545432',
        '3455454554554543',
        '3454454554554543',
        '2343323c43233432',
        '.21cb11c111cb12.',
        '..m..cbcb.cb.h..',
        '..k...cbcbcb.k..',
        '......cbcba.....',
        '.......cba......',
        '.......cba......',
        '......ccbaa.....',
    ], 4),
    ('F5 nach Wuchs 6', 'gespiegelt: rechts ein eigener Stamm, zwischen ihm und dem Fächer hängt eine Feige',
     _CROWN + [
        '1m2c12cb211c1c21',
        '.kcb..cbcb.h.c..',
        '...cb.cbcb.k.c..',
        '....cbcbcba..c..',
        '.....cbcbcbbba..',
        '......cbcbba....',
        '......cbba......',
        '......cbba......',
    ], 5),
]


def grown_sheet():
    """FIG_GROWN with the side view of the growth each one follows (concept/selftest_fig.png) under it."""
    sheet('Feigen-Setzling · nach dem Wuchs im Spiel', [i[:3] for i in FIG_GROWN], mt.FIG_FRUIT,
          mt.draw(*mt.SAPLINGS['fig_sapling']), 'acacia_sapling', 'fig_sapling_v6.png')
    path = os.path.join(OUT, 'fig_sapling_v6.png')
    img = Image.open(path)
    ref = Image.open(os.path.join(mt.ROOT, 'concept', 'selftest_fig.png'))
    xs = [180, 680, 1210, 1730, 2250, 2770]  # the side views of Wuchs 1-6 in selftest_fig.png
    out = Image.new('RGBA', (img.width, img.height + 300), img.getpixel((0, 0)))
    out.alpha_composite(img)
    d = ImageDraw.Draw(out)
    d.text((20, img.height - 70), 'Darunter: der Wuchs aus dem Dev-Server, nach dem die Variante gezeichnet ist '
           '(Seitenansicht)', font=font(18), fill=(90, 100, 120, 255))
    for i, (*_, n) in enumerate(FIG_GROWN):
        side = ref.crop((xs[n], 450, xs[n] + 170, 555)).resize((320, 198), Image.NEAREST)
        out.alpha_composite(side, (20 + i * 340, img.height - 40))
    out.save(path)


# ---------------------------------------------------------------- date palm and strawberry tree

# after the grown trees (run/greektrees-selftest/*.json): the date palm a slim ringed trunk, 8-10 blocks, stepping
# sideways once, under a compact umbrella crown with drooping ends, the dates beside the trunk under it; sometimes a
# second, shorter trunk with its own crown. Palette PALM.
PALM_GAME = [
    ('P1 Gerade',
     'ein schlanker Stamm, gerade bis oben; die Krone ein Schirm mit hängenden Enden, darunter die Datteln', [
        '.....455454.....',
        '...3455445543...',
        '..345545445543..',
        '.34554322345543.',
        '.3.32.obao.23.3.',
        '.2..2.rcbr.2..2.',
        '.1.....ba.....1.',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
    ], 'date_palm_10'),
    ('P2 Versatz unten', 'der Stamm springt tief unten einen Schritt zur Seite', [
        '.....455454.....',
        '...3455445543...',
        '..345545445543..',
        '.34554322345543.',
        '.3.32.obao.23.3.',
        '.2..2.rcbr.2..2.',
        '.1.....ba.....1.',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
        '.......ba.......',
        '......cb........',
        '......ba........',
        '......cb........',
        '......ba........',
        '......cb........',
    ], 'date_palm_7'),
    ('P3 Versatz Mitte', 'der Sprung auf halber Höhe, die Krone steht neben dem Fuß', [
        '......455454....',
        '....3455445543..',
        '...345545445543.',
        '..34554322345543',
        '..3.32.obao.23.3',
        '..2..2.rcbr.2..2',
        '..1.....ba.....1',
        '........cb......',
        '........ba......',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
    ], 'date_palm_4'),
    ('P4 Zwei Stämme', 'ein hoher und ein kurzer Stamm aus einem Fuß, jeder mit eigener Krone', [
        '........4554....',
        '......34554543..',
        '.....3455445543.',
        '.....2.3ocbo3.2.',
        '.....1..rbar..1.',
        '.........cb.....',
        '...4554..ba.....',
        '.34554543cb.....',
        '3455445543a.....',
        '2.3ocbo3.2b.....',
        '1..rbar..1a.....',
        '....cb...cb.....',
        '.....ba..ba.....',
        '.....cb.cb......',
        '......baba......',
        '......cbcb......',
    ], 'date_palm_9'),
    ('P5 Doppelkrone', 'zwei Stämme dicht nebeneinander, die Krone des kurzen unter der des hohen', [
        '.....455454.....',
        '...3455445543...',
        '..345545445543..',
        '.34554322345543.',
        '.3.32.obao.23.3.',
        '.2..2.rcbr.2..2.',
        '.1..4554a.....1.',
        '..34554543......',
        '.3455445543.....',
        '.2.3ocbo3.2.....',
        '.1..rbara.1.....',
        '.....cbcb.......',
        '.....baba.......',
        '.....cbcb.......',
        '.....baba.......',
        '.....cbcb.......',
    ], 'date_palm_8'),
]

# the strawberry tree: a short trunk, then 2-3 thin orange stems climbing outwards a step at a time, a small round
# crown of dark leaves on each, at different heights, berries under the crowns. Palette ARBUTUS.
BERRY_GAME = [
    ('S1 V-Form', 'zwei dünne Stämme steigen stufenweise auseinander, die Kronen auf gleicher Höhe', [
        '................',
        '................',
        '................',
        '..454.....454...',
        '.34543...34543..',
        '3454543.3454543.',
        '2343432.2343432.',
        '.12221...12221..',
        '.r.c.o...s.c.R..',
        '....c.....c.....',
        '....c.....c.....',
        '.....c...c......',
        '......c.c.......',
        '.......c........',
        '.......c........',
        '.......c........',
    ], 'strawberry_tree_0'),
    ('S2 Ungleich hoch', 'der rechte Stamm steigt höher, seine Krone über der linken', [
        '..........454...',
        '.........34543..',
        '........3454543.',
        '........2343432.',
        '.........12221..',
        '..454....r.c.s..',
        '.34543.....c....',
        '3454543...c.....',
        '2343432...c.....',
        '.12221...c......',
        '.R..co...c......',
        '.....c..c.......',
        '......c.c.......',
        '.......c........',
        '.......c........',
        '.......c........',
    ], 'strawberry_tree_5'),
    ('S3 Drei Stämme', 'drei Stämme, zwei Kronen laufen ineinander, die dritte weiter rechts', [
        '................',
        '...........454..',
        '..........34543.',
        '.......453454543',
        '...4543452343432',
        '..3453454512221.',
        '.345423434R2c.s.',
        '.2343412221.c...',
        '..1222o....c....',
        '..r.c..c..c.....',
        '.....c.c..c.....',
        '.....c.c.c......',
        '......cbb.......',
        '.......c........',
        '.......c........',
        '.......c........',
    ], 'strawberry_tree_3'),
    ('S4 Eine Wolke', 'die Stämme dicht beisammen, die Kronen eine Wolke, Beeren darunter entlang', [
        '................',
        '......454.......',
        '.....3454354....',
        '...4345454343...',
        '..342343432543..',
        '.3454122213432..',
        '.234343212221...',
        '..12221.r.o.r...',
        '..s.R.....c.....',
        '.....c...c......',
        '.....c...c......',
        '......c.c.......',
        '......c.c.......',
        '.......c........',
        '.......c........',
        '.......c........',
    ], 'strawberry_tree_7'),
    ('S5 Hoher Stamm', 'ein hoher Stamm, die Äste zeigen zu dir, eine runde Krone obendrauf', [
        '................',
        '......454.......',
        '.....345543.....',
        '....34545543....',
        '.....34543......',
        '....34545433....',
        '....23434322....',
        '.....12221......',
        '.....rcb.os.....',
        '......Rcb.......',
        '.......c........',
        '.......c........',
        '.......c........',
        '.......c........',
        '.......c........',
        '.......c........',
    ], 'strawberry_tree_6'),
]


# round 2: P1's crown and dates on a single trunk that curves; the trunk a ringed 2 px band that moves at most a
# pixel a row
PALM_CURVED = [
    (PALM_GAME[0][0].split()[0] + ' (Runde 1)', 'zum Vergleich', PALM_GAME[0][2]),
    ('C1 Bauch links', 'der Stamm wölbt sich nach links, Fuß und Krone übereinander', [
        '.....455454.....',
        '...3455445543...',
        '..345545445543..',
        '.34554322345543.',
        '.3.32.obao.23.3.',
        '.2..2.rcbr.2..2.',
        '.1....ba......1.',
        '......cb........',
        '.....ba.........',
        '.....cb.........',
        '.....ba.........',
        '.....cb.........',
        '......ba........',
        '......cb........',
        '.......ba.......',
        '.......cb.......',
    ]),
    ('C2 Schräg rechts', 'lehnt sich von einem Fuß links herüber, oben richtet er sich auf', [
        '......455454....',
        '....3455445543..',
        '...345545445543.',
        '..34554322345543',
        '..3.32.obao.23.3',
        '..2..2.rcbr.2..2',
        '..1.....ba.....1',
        '........cb......',
        '........ba......',
        '.......cb.......',
        '.......ba.......',
        '......cb........',
        '.....ba.........',
        '....cb..........',
        '...ba...........',
        '...cb...........',
    ]),
    ('C3 S-Kurve', 'oben nach rechts gebogen, unten nach links', [
        '.....455454.....',
        '...3455445543...',
        '..345545445543..',
        '.34554322345543.',
        '.3.32.obao.23.3.',
        '.2..2.rcbr.2..2.',
        '.1......ba....1.',
        '........cb......',
        '.........ba.....',
        '.........cb.....',
        '.........ba.....',
        '........cb......',
        '.......ba.......',
        '......cb........',
        '......ba........',
        '.......cb.......',
    ]),
    ('C4 Weit gelehnt', 'lehnt sich weit von einem Fuß rechts herüber, wie am Strand', [
        '....455454......',
        '..3455445543....',
        '.345545445543...',
        '34554322345543..',
        '3.32.obao.23.3..',
        '2..2.rcbr.2..2..',
        '1.....ba.....1..',
        '.......cb.......',
        '.......ba.......',
        '........cb......',
        '.........ba.....',
        '..........cb....',
        '...........ba...',
        '...........cb...',
        '............ba..',
        '............cb..',
    ]),
    ('C5 Liegender Fuß', 'der Fuß läuft schräg zur Seite, dann geht der Stamm gerade hoch', [
        '.....455454.....',
        '...3455445543...',
        '..345545445543..',
        '.34554322345543.',
        '.3.32.obao.23.3.',
        '.2..2.rcbr.2..2.',
        '.1.....ba.....1.',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
        '........ba......',
        '.........cb.....',
        '..........ba....',
        '..........cb....',
    ]),
]


# round 3: the finished date palm (make_textures.SAPLINGS, trunk and dates kept pixel for pixel) under five crowns
PALM_LEAVES = [
    ('jetzt', 'die übernommene Textur', None),
    ('L1 Wedelfächer', 'einzelne Wedel fächern mit Lücken aus: zwei kurz nach oben, zwei im Bogen, zwei hängen bis an den Rand', [
        '....55....55....',
        '...3355..5533...',
        '...4444554444...',
        '.44223455432244.',
        '342..333333..243',
        '32.331ocbo133.23',
        '...31.rbar.13...',
        '..31...cb...13..',
        '.23...ba.....32.',
        '.21...cb.....12.',
        '......ba........',
        '......cb........',
        '......ba........',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
    ]),
    ('L2 Dichter Schirm', 'ein runder, geschlossener Schirm, die Enden hängen drei Reihen tief', [
        '................',
        '.....455454.....',
        '...3455445543...',
        '..345545445543..',
        '.34554322345543.',
        '3453.2ocbo2.3543',
        '342..2rbar2..243',
        '23....1cb..1..32',
        '2.....ba.......2',
        '1.....cb.......1',
        '......ba........',
        '......cb........',
        '......ba........',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
    ]),
    ('L3 Flacher Schirm', 'flach und breit, die Enden hängen nur kurz', [
        '................',
        '................',
        '....45545545....',
        '.3455454454554..',
        '3455432112345543',
        '342.2.ocbo.2.243',
        '2.....rbar.....2',
        '.......cb.......',
        '......ba........',
        '......cb........',
        '......ba........',
        '......cb........',
        '......ba........',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
    ]),
    ('L4 Gefiedert', 'die Wedel im Bogen, darunter einzelne Fiederblättchen wie ein Kamm', [
        '....335..533....',
        '......3555......',
        '.44444445444444.',
        '343.3.34433.3.43',
        '33..33333333...3',
        '...33.ocbo233...',
        '..32..rbar.2.3..',
        '.3.....cb....23.',
        '23....ba......32',
        '2.....cb......22',
        '......ba........',
        '......cb........',
        '......ba........',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
    ]),
    ('L5 Junge Wedel', 'in der Mitte stehen junge Wedel aufrecht, die alten hängen ringsum', [
        '......5..5......',
        '.....45..54.....',
        '..44.4544544.44.',
        '.45545455454554.',
        '3455432112345543',
        '3.32..ocbo..23.3',
        '2..2..rbar..2..2',
        '1..1...cb...1..1',
        '......ba........',
        '......cb........',
        '......ba........',
        '......cb........',
        '......ba........',
        '.......cb.......',
        '.......ba.......',
        '.......cb.......',
    ]),
]


# ---------------------------------------------------------------- cypress and strawberry tree, round 2

# the cypress after the grown tree (22 tall, 5 wide: a 4-block trunk, a narrow foot, widest in the lower third,
# tapering, a thin spire 4-5 blocks long); the side view of a grown cypress under each for comparison. Palette CYPRESS.
CYPRESS_IDEAS = [
    ('Z1 Nach dem Wuchs',
     'dünne lange Spitze, schmaler Oberkörper, im unteren Drittel am breitesten, schmaler Fuß, grauer Stamm', [
        '.......3........',
        '.......4........',
        '.......4........',
        '.......43.......',
        '......431.......',
        '......5421......',
        '......5421......',
        '......4321......',
        '.....544321.....',
        '.....544321.....',
        '.....434321.....',
        '.....544221.....',
        '......5421......',
        '.......cb.......',
        '.......cb.......',
        '.......ba.......',
    ], 'cypress_0'),
    ('Z2 Schlanke Säule',
     'noch schlanker, höchstens vier breit, die Spitze länger', [
        '.......3........',
        '.......4........',
        '.......4........',
        '.......4........',
        '.......42.......',
        '.......43.......',
        '......531.......',
        '......421.......',
        '......531.......',
        '......5421......',
        '......4421......',
        '......5421......',
        '.......43.......',
        '.......cb.......',
        '.......cb.......',
        '.......ba.......',
    ], 'cypress_1'),
    ('Z3 Flamme mit Spitze',
     'die Flamme des jetzigen Setzlings, weich gerundet, mit der langen Spitze obendrauf', [
        '.......3........',
        '.......4........',
        '.......4........',
        '.......43.......',
        '......431.......',
        '......531.......',
        '......5421......',
        '.....44221......',
        '.....544321.....',
        '....4443221.....',
        '....4433221.....',
        '.....544221.....',
        '......5421......',
        '.......cb.......',
        '.......cb.......',
        '.......ba.......',
    ], 'cypress_2'),
    ('Z4 Gestuft',
     'in Bändern gestuft wie die Lagen im Spiel, das breiteste Band mit Knubbeln an den Seiten', [
        '.......3........',
        '.......4........',
        '.......4........',
        '.......4........',
        '.......42.......',
        '......5421......',
        '......5421......',
        '......4321......',
        '.....544321.....',
        '....45433221....',
        '....44333221....',
        '.....544221.....',
        '......5421......',
        '.......cb.......',
        '.......cb.......',
        '.......ba.......',
    ], 'cypress_3'),
    ('Z5 Geneigte Spitze',
     'wie Z1, die Spitze biegt sich oben nach rechts', [
        '.........4......',
        '........4.......',
        '........4.......',
        '.......43.......',
        '......431.......',
        '......5421......',
        '......5421......',
        '......4321......',
        '.....544321.....',
        '.....544321.....',
        '.....434321.....',
        '.....544221.....',
        '......5421......',
        '.......cb.......',
        '.......cb.......',
        '.......ba.......',
    ], 'cypress_4'),
]

# the strawberry tree as variations of its current texture (the round after the grown tree did not please).
# Palette ARBUTUS.
BERRY_VARIANTS = [
    ('jetzt', 'die bisherige Textur', None),
    ('E1 Blüten und Früchte',
     'die jetzige, dazu wie am echten Baum Blüten und Früchte zugleich: weiß, gelb, orange, rot', [
        '................',
        '...343....454...',
        '..34543..34543..',
        '..2w443..344r2..',
        '..23y32..2oR32..',
        '...22c....c22...',
        '...45c....b54...',
        '..3443c..c443...',
        '...2r.c..b.w2...',
        '......cbcb......',
        '.......cb.......',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '......bab.......',
        '......aba.......',
    ]),
    ('E2 Weiter offen',
     'die Arme weiter auseinander, die Kronen größer', [
        '..343......454..',
        '.34543....34543.',
        '3454543..3454543',
        '2s4443r..3443r42',
        '.23r32c..c2ro32.',
        '..22.c....c.22..',
        '..45.c....c.54..',
        '.3443c....c443..',
        '..2r..c..c..r2..',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '......bab.......',
        '......aba.......',
    ]),
    ('E3 Drei Arme',
     'ein dritter Stamm in der Mitte mit einer kleinen Krone obendrauf', [
        '.......454......',
        '...3..34543.4...',
        '..343.3r443.54..',
        '.34543.2o2.34543',
        '.2s443..c..344r2',
        '.23r32..c..2ro32',
        '..22c...c...c22.',
        '..45c...c...b54.',
        '.3443c..c..c443.',
        '..2r.c..c..b.r2.',
        '......cbcb......',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '......bab.......',
        '......aba.......',
    ]),
    ('E4 Ungleich',
     'der rechte Arm steigt höher, seine Krone über der linken', [
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '.........2ro32..',
        '...343....c22...',
        '..34543...b54...',
        '..2s443..c443...',
        '..23r32..b.r2...',
        '...22c...c......',
        '...45c..c.......',
        '..3443cbc.......',
        '...2r..cb.......',
        '.......bc.......',
        '.......cb.......',
        '......bab.......',
        '......aba.......',
    ]),
    ('E5 Eine Krone',
     'die beiden Kronen zu einer runden Krone über dem Y verwachsen, Beeren hängen darunter', [
        '................',
        '....3434545.....',
        '...345434543....',
        '..34s4434344r2..',
        '..234r324ro332..',
        '..1223c2c2221...',
        '...r.2c..c2.r...',
        '...s..c..b..o...',
        '......c..c......',
        '......cbcb......',
        '.......cb.......',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '......bab.......',
        '......aba.......',
    ]),
]


# round 3: no root foot, two stems, the crowns at different heights; in the current style (palette STRAWBERRY)
BERRY_TWO = [
    ('jetzt', 'die bisherige Textur', None),
    ('A Ein Fuß, zwei Arme', 'E4 ohne Wurzel: ein dünner Stamm teilt sich tief in zwei Arme, die rechte Krone höher', [
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '.........2ro32..',
        '...343....c22...',
        '..34543...b54...',
        '..2s443..c443...',
        '..23r32..b.r2...',
        '...22c...c......',
        '...45c..c.......',
        '..3443cbc.......',
        '...2r..cb.......',
        '.......bc.......',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
    ]),
    ('B Zwei Stämme', 'zwei getrennte Stämme direkt aus dem Boden, der rechte länger, seine Krone höher', [
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '.........2ro32..',
        '...343....c22...',
        '..34543...b54...',
        '..2s443..c443...',
        '..23r32..b.r2...',
        '...22c...c......',
        '...45c...b......',
        '..3443c..c......',
        '...2r.c..b......',
        '.......c.c......',
        '.......c.b......',
        '.......cb.......',
        '.......cb.......',
    ]),
]


# round 4: five variations of A from berry3 (one foot, two arms, the right crown higher), palette STRAWBERRY
BERRY_A = [
    ('A (Runde 3)', 'zum Vergleich', BERRY_TWO[1][2]),
    ('A1 Klar', 'nur die zwei Kronen, keine Blattbüschel an den Armen, eine Beere hängt unter jeder Krone', [
        '................',
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '.........2ro32..',
        '..343.....c22r..',
        '.34543....b.....',
        '.2s443...c......',
        '.23r32...b......',
        '.r22c...c.......',
        '....c...b.......',
        '.....c.cb.......',
        '......cbb.......',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
    ]),
    ('A2 Weit offen', 'die Arme spreizen weiter, die Kronen sitzen an den Rändern, zwei Reihen Höhenunterschied', [
        '................',
        '...........454..',
        '..........34543.',
        '.343......344r2.',
        '34543.....2ro32.',
        '2s443......c22r.',
        '23r32......b....',
        '.22c......c.....',
        '...c.....b......',
        '....c...c.......',
        '.....c..b.......',
        '......cbb.......',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '.......bc.......',
    ]),
    ('A3 Große Kronen', 'beide Kronen größer und runder, sie füllen die Kachel', [
        '...........454..',
        '..........34543.',
        '.........3454543',
        '..343....344r443',
        '.34543...2ro3432',
        '3454543....22.2.',
        '2s44r43....c....',
        '23r3432...b.....',
        '.22.2.....c.....',
        '....c....b......',
        '.....c...c......',
        '......c.b.......',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '.......bc.......',
    ]),
    ('A4 Mit Blattpaaren', 'wie die bisherige Textur ein Blattbüschel an jedem Arm, die Kronen auf verschiedener Höhe',
     [
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '...343...2ro32..',
        '..34543...c22...',
        '..2s443...b54...',
        '..23r32..c443...',
        '...22c...b.r2...',
        '...45c...c......',
        '..3443c.c.......',
        '...2r.cb........',
        '......bc........',
        '......cb........',
        '......bc........',
        '......cb........',
        '......bc........',
    ]),
    ('A5 Gebogene Arme', 'die Arme laufen in weichen Bögen statt in Stufen zu den Kronen', [
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '..343....2ro32..',
        '.34543....c22...',
        '.2s443....c.....',
        '.23r32....b.....',
        '..22c.....c.....',
        '...c......b.....',
        '...c.....c......',
        '....cc...b......',
        '......c.c.......',
        '.......cb.......',
        '.......bc.......',
        '.......cb.......',
        '.......bc.......',
    ]),
]


# round 5: the same six with thicker stems (arms 2 px, the trunk 3) and smooth bark instead of the checkers: light
# left edge, dark right edge, now and then a lighter spot where the bark peels
BERRY_THICK = [
    ('A (Runde 3) dicker', '', [
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '.........2ro32..',
        '...343....c22...',
        '..34543...c54...',
        '..2s443..c443...',
        '..23r32..cbr2...',
        '...22cb..cb.....',
        '...45cb.cb......',
        '..3443cbba......',
        '...2r..cba......',
        '.......cba......',
        '.......cca......',
        '.......cba......',
        '.......cba......',
    ]),
    ('A1 Klar dicker', '', [
        '................',
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '.........2ro32..',
        '..343.....c22r..',
        '.34543....cb....',
        '.2s443...cb.....',
        '.23r32...cb.....',
        '.r22cb..cb......',
        '....cb..cb......',
        '.....cbbba......',
        '......cbba......',
        '.......cca......',
        '.......cba......',
        '.......cba......',
    ]),
    ('A2 Weit offen dicker', '', [
        '................',
        '...........454..',
        '..........34543.',
        '.343......344r2.',
        '34543.....2ro32.',
        '2s443......c22r.',
        '23r32......cb...',
        '.22cb.....cb....',
        '...cb....cb.....',
        '....cb..cb......',
        '.....cb.cb......',
        '......cbba......',
        '.......cba......',
        '.......cca......',
        '.......cba......',
        '.......cba......',
    ]),
    ('A3 Große Kronen dicker', '', [
        '...........454..',
        '..........34543.',
        '.........3454543',
        '..343....344r443',
        '.34543...2ro3432',
        '3454543....22.2.',
        '2s44r43....cb...',
        '23r3432...cb....',
        '.22.2.....cb....',
        '....cb...cb.....',
        '.....cb..cb.....',
        '......cbba......',
        '.......cba......',
        '.......cca......',
        '.......cba......',
        '.......cba......',
    ]),
    ('A4 Mit Blattpaaren dicker', '', [
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '...343...2ro32..',
        '..34543...c22...',
        '..2s443...c54...',
        '..23r32..c443...',
        '...22cb..cbr2...',
        '...45cb..cb.....',
        '..3443ccba......',
        '...2r.cba.......',
        '......cba.......',
        '......cba.......',
        '......cca.......',
        '......cba.......',
        '......cba.......',
    ]),
    ('A5 Gebogene Arme dicker', '', [
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '..343....2ro32..',
        '.34543....c22...',
        '.2s443....cb....',
        '.23r32....cb....',
        '..22cb....cb....',
        '...cb.....cb....',
        '...cb....cb.....',
        '....cba..cb.....',
        '......cbba......',
        '.......cba......',
        '.......cca......',
        '.......cba......',
        '.......cba......',
    ]),
]


# round 6: every stem 2 px (the arms thickened, the trunk as it was), smooth bark: light left, darker right
BERRY_2PX = [
    ('A (Runde 3)', '', [
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '.........2ro32..',
        '...343....c22...',
        '..34543...c54...',
        '..2s443..c443...',
        '..23r32..cbr2...',
        '...22cb..cb.....',
        '...45cb.cb......',
        '..3443cbc.......',
        '...2r..cb.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
    ]),
    ('A1 Klar', '', [
        '................',
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '.........2ro32..',
        '..343.....c22r..',
        '.34543....cb....',
        '.2s443...cb.....',
        '.23r32...cb.....',
        '.r22cb..cb......',
        '....cb..cb......',
        '.....cbcb.......',
        '......cbc.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
    ]),
    ('A2 Weit offen', '', [
        '................',
        '...........454..',
        '..........34543.',
        '.343......344r2.',
        '34543.....2ro32.',
        '2s443......c22r.',
        '23r32......cb...',
        '.22cb.....cb....',
        '...cb....cb.....',
        '....cb..cb......',
        '.....cb.cb......',
        '......cbc.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
    ]),
    ('A3 Große Kronen', '', [
        '...........454..',
        '..........34543.',
        '.........3454543',
        '..343....344r443',
        '.34543...2ro3432',
        '3454543....22.2.',
        '2s44r43....cb...',
        '23r3432...cb....',
        '.22.2.....cb....',
        '....cb...cb.....',
        '.....cb..cb.....',
        '......cbcb......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
    ]),
    ('A4 Mit Blattpaaren', '', [
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '...343...2ro32..',
        '..34543...c22...',
        '..2s443...c54...',
        '..23r32..c443...',
        '...22cb..cbr2...',
        '...45cb..cb.....',
        '..3443cbcb......',
        '...2r.cb........',
        '......cb........',
        '......cb........',
        '......cb........',
        '......cb........',
        '......cb........',
    ]),
    ('A5 Gebogene Arme', '', [
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '..343....2ro32..',
        '.34543....c22...',
        '.2s443....cb....',
        '.23r32....cb....',
        '..22cb....cb....',
        '...cb.....cb....',
        '...cb....cb.....',
        '....cb...cb.....',
        '......cbcb......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
    ]),
]


# round 7: three crowns at different heights, 2 px stems lit from the top left, no root (palette STRAWBERRY)
BERRY_THREE = [
    ('T1 Fächer', 'die mittlere Krone am höchsten, die linke am tiefsten, die rechte dazwischen', [
        '......454.......',
        '.....34543......',
        '.....34r43......',
        '.....2o432..454.',
        '......2c2..34543',
        '.......cb..344r2',
        '.343...cb..2ro32',
        '34543..cb..cc22.',
        '2s443..cb.cbb...',
        '23r32..cbcb.....',
        '.22.cc.cbb......',
        '.....ccbb.......',
        '......cbb.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
    ]),
    ('T2 Treppe', 'die Kronen steigen von links nach rechts an', [
        '............454.',
        '...........34543',
        '...........344r2',
        '......454..2ro32',
        '.....34543..c22.',
        '.....34r43.cb...',
        '.343.2o432cb....',
        '34543.2c2cb.....',
        '2s443..cbb......',
        '23r32..cb.......',
        '.22.cc.cb.......',
        '.....ccbb.......',
        '......cbb.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
    ]),
    ('T3 Mitte tief', 'die mittlere Krone sitzt tief zwischen zwei hohen äußeren', [
        '................',
        '.343............',
        '34543.......454.',
        '2s443......34543',
        '23r32......344r2',
        '.22c..454..2ro32',
        '..cbc34543..c22.',
        '....c34r43.cb...',
        '....c2o432cbb...',
        '......2b2cbb....',
        '......cbbbb.....',
        '.......cbb......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
    ]),
    ('T4 Einseitig', 'links eine tiefe Krone, rechts zwei übereinander am selben Arm', [
        '..........454...',
        '.........34543..',
        '.........344r2..',
        '.........2ro32..',
        '..........c22...',
        '..........cb454.',
        '.343......c34543',
        '34543....cb344r2',
        '2s443...cbb2ro32',
        '23r32...cb...22.',
        '.22.cc.cb.......',
        '.....ccbb.......',
        '......cbb.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
    ]),
    ('T5 Verzweigt', 'der Stamm gabelt sich, der rechte Arm teilt sich noch einmal in die mittlere und rechte Krone', [
        '.......454......',
        '......34543.....',
        '......34r43.....',
        '......2o432.454.',
        '.343...2c2.34543',
        '34543...cb.344r2',
        '2s443...cbc2ro32',
        '23r32....cbbb22.',
        '.22bcc..cbbb....',
        '....cb..cb......',
        '....cbccbb......',
        '......cbb.......',
        '......cbb.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
    ]),
]


ARIES_BIG = [
    ('G1 A ausgefüllt', 'wie A, die Kuppel bis an den oberen Rand und 14 breit, größere Seitenkronen, Stamm 2 px', [
        '.....455454.....',
        '...345f5445543..',
        '..3454J5445f543.',
        '.3454JjJ4454543.',
        '.245JjJ445f4543.',
        '.2344J454f45432.',
        '.112233cb332211.',
        '.3454..cb..4543.',
        '34f545.bc.545f43',
        '245J54.cb.45f542',
        '.1232c.cb.c2321.',
        '......ccbc......',
        '.......cb.......',
        '.......bs.......',
        '......cbsc......',
        '....cdbaabdc....',
    ]),
    ('G2 Eine Kuppel', 'eine Krone bis an beide Ränder wie der gewachsene Baum, Stamm 3 px', [
        '....34554543....',
        '..345f54455f43..',
        '.3454J544554543.',
        '345f4JjJ4454f543',
        '3454JjJ445454f43',
        '245J4f4454454542',
        '2344J45444f45432',
        '1233454f43354321',
        '.12233cbb322321.',
        '......cbb.......',
        '......cbb.......',
        '......csb.......',
        '......cbb.......',
        '......csb.......',
        '.....ccbbc......',
        '...cdbbaabdc....',
    ]),
    ('G3 Dicker Stamm', 'G1 mit 3 px Stamm und breiterem Fuß', [
        '.....455454.....',
        '...345f5445543..',
        '..3454J5445f543.',
        '.3454JjJ4454543.',
        '.245JjJ445f4543.',
        '.2344J454f45432.',
        '.11223cbb332211.',
        '.3454.cbb..4543.',
        '34f54.csb.545f43',
        '245J4.cbb.45f542',
        '.1232ccbbcc2321.',
        '......cbb.......',
        '......csb.......',
        '......cbb.......',
        '.....ccbbc......',
        '...cdbbaabbdc...',
    ]),
    ('G4 Hohe Kuppel', 'Seitenkronen und Stamm von A, die Kuppel darüber höher und breiter', [
        '.....455454.....',
        '...345f5445543..',
        '..3454J5445f543.',
        '.3454JjJ4454543.',
        '.345JjJ445f4543.',
        '.2454J454f45442.',
        '.2344J4544f5432.',
        '.12344544544321.',
        '..12233cb332211.',
        '.454...cb...454.',
        '4f454..bc..45f54',
        '.2332c.cb.c2332.',
        '......ccbc......',
        '.......cb.......',
        '......cbsc......',
        '....cdbaabdc....',
    ]),
    ('G5 Wolke', 'Kuppel von G1, die Seitenkronen seitlich hoch davor: eine breite Wolke, langer Stamm', [
        '.....455454.....',
        '...345f5445543..',
        '..3454J5445f543.',
        '.3454JjJ4454543.',
        '.4554jJ445f4554.',
        '34f543454f345f43',
        '3454523cb3344542',
        '234432.cb.234321',
        '.1221..cb..1221.',
        '.....c.bc.c.....',
        '......ccbc......',
        '.......cb.......',
        '.......bs.......',
        '.......cb.......',
        '......cbsc......',
        '....cdbaabdc....',
    ]),
]


def growth_sheet(title, ideas, palette, current, vanilla_name, out,
                 caption='der Wuchs aus dem Dev-Server, nach dem die Variante gezeichnet ist'):
    """sheet() with the side view of the grown tree each idea follows under it. The growths are read from
    run/greektrees-selftest, which every self-test grows anew: render right after drawing."""
    sheet(title, [i[:3] for i in ideas], palette, current, vanilla_name, out)
    sys.path.insert(0, os.path.join(mt.ROOT, 'concept'))
    cwd = os.getcwd()
    os.chdir(os.path.join(mt.ROOT, 'concept'))  # render_selftest reads the growths relative to concept/
    try:
        import render_selftest
        import voxel
        sides = [voxel.render_side(render_selftest.load(i[3]), s=12, margin=6) for i in ideas]
    finally:
        os.chdir(cwd)
    path = os.path.join(OUT, out)
    img = Image.open(path)
    h = max(sd.height for sd in sides)
    res = Image.new('RGBA', (img.width, img.height + h + 30), img.getpixel((0, 0)))
    res.alpha_composite(img)
    ImageDraw.Draw(res).text((20, img.height - 70), f'Darunter: {caption} (Seitenansicht)', font=font(18),
                             fill=(90, 100, 120, 255))
    for i, sd in enumerate(sides):
        panel = Image.new('RGBA', (320, h + 10), (190, 214, 236, 255))
        panel.alpha_composite(sd, ((320 - sd.width) // 2, h + 10 - sd.height))
        res.alpha_composite(panel, (20 + i * 340, img.height - 40))
    res.save(path)


# ---------------------------------------------------------------- the crossed planes on a grass block


def project(p, yaw, pitch):
    x, y, z = p
    u = x * math.cos(yaw) - z * math.sin(yaw)
    d = x * math.sin(yaw) + z * math.cos(yaw)
    v = -y * math.cos(pitch) + d * math.sin(pitch)
    return u, v, d


def face(canvas, tex, origin, eu, ev, yaw, pitch, scale, offset):
    """Draws tex on the parallelogram origin + s*eu + t*ev (s, t in 0..1, texture left->right, top->bottom)."""
    o = project(origin, yaw, pitch)
    a = project([origin[i] + eu[i] for i in range(3)], yaw, pitch)
    b = project([origin[i] + ev[i] for i in range(3)], yaw, pitch)
    ox, oy = o[0] * scale + offset[0], o[1] * scale + offset[1]
    ux, uy = (a[0] - o[0]) * scale, (a[1] - o[1]) * scale
    vx, vy = (b[0] - o[0]) * scale, (b[1] - o[1]) * scale
    det = ux * vy - uy * vx
    w, h = tex.size
    # output X, Y -> s, t -> texture pixel
    ia, ib = vy / det * w, -vx / det * w
    id_, ie = -uy / det * h, ux / det * h
    data = (ia, ib, -(ia * ox + ib * oy), id_, ie, -(id_ * ox + ie * oy))
    canvas.alpha_composite(tex.transform(canvas.size, Image.AFFINE, data, resample=Image.NEAREST))


def shade(img, k):
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            px[x, y] = (int(r * k), int(g * k), int(b * k), a)
    return out


def block_view(tile, size=300):
    yaw, pitch, scale = math.radians(32), math.radians(28), 112
    canvas = Image.new('RGBA', (size, size), (150, 190, 230, 255))
    off = (size / 2, size * 0.42)
    top = mt._tint(mt.vanilla('grass_block_top'), (124, 189, 107))
    side = mt.vanilla('grass_block_side')
    side.alpha_composite(mt._tint(mt.vanilla('grass_block_side_overlay'), (124, 189, 107)))
    # grass block from -0.5..0.5 (x, z), -1..0 (y): the two visible sides, then the top
    face(canvas, shade(side, 0.62), (0.5, 0, 0.5), (0, 0, -1), (0, -1, 0), yaw, pitch, scale, off)
    face(canvas, shade(side, 0.8), (-0.5, 0, 0.5), (1, 0, 0), (0, -1, 0), yaw, pitch, scale, off)
    face(canvas, top, (-0.5, 0, -0.5), (1, 0, 0), (0, 0, 1), yaw, pitch, scale, off)
    # the sapling: two planes along the diagonals, each cut in two at the crossing, drawn far to near
    left, right = tile.crop((0, 0, 8, 16)), tile.crop((8, 0, 16, 16))
    r = 0.5
    halves = []
    for (x0, z0), (x1, z1) in (((-r, -r), (r, r)), ((-r, r), (r, -r))):
        mx, mz = (x0 + x1) / 2, (z0 + z1) / 2
        halves.append((left, (x0, 1, z0), (mx - x0, 0, mz - z0)))
        halves.append((right, (mx, 1, mz), (x1 - mx, 0, z1 - mz)))
    halves.sort(key=lambda h: project((h[1][0] + h[2][0] / 2, 0.5, h[1][2] + h[2][2] / 2), yaw, pitch)[2])
    for tex, origin, eu in halves:
        face(canvas, tex, origin, eu, (0, -1, 0), yaw, pitch, scale, off)
    return canvas


def ground_row(tiles, size=64):
    ctx = Image.new('RGBA', (16 * len(tiles), 32), (150, 190, 230, 255))
    side = mt.vanilla('grass_block_side')
    side.alpha_composite(mt._tint(mt.vanilla('grass_block_side_overlay'), (124, 189, 107)))
    for k, t in enumerate(tiles):
        ctx.alpha_composite(side, (16 * k, 16))
        ctx.alpha_composite(t, (16 * k, 0))
    return ctx.resize((ctx.width * size // 16, ctx.height * size // 16), Image.NEAREST)


def font(px):
    for name in ('segoeuib.ttf', 'arialbd.ttf'):
        try:
            return ImageFont.truetype(name, px)
        except OSError:
            continue
    return ImageFont.load_default()


def sheet(title, ideas, palette, current, vanilla_name, out):
    ink, grey, paper = (30, 50, 80, 255), (90, 100, 120, 255), (244, 240, 232, 255)
    cell, pad = 340, 20
    img = Image.new('RGBA', (pad + cell * len(ideas) + pad, 1210), paper)
    d = ImageDraw.Draw(img)
    d.text((pad, 14), title, font=font(34), fill=ink)
    d.text((pad + 2, 60), 'Oben 16×16 groß, darunter im Spiel als Kreuz auf Gras, unten auf dem Boden: '
           'Vorschlag ×2, bisherige Textur, Vanilla-' + vanilla_name.replace('_', ' ') + '.', font=font(18), fill=grey)
    ref = mt.vanilla(vanilla_name)
    for i, (name, note, rows) in enumerate(ideas):
        tile = mt.draw(palette, rows)
        x = pad + i * cell
        big = Image.new('RGBA', (320, 320), (150, 190, 230, 255))
        big.alpha_composite(tile.resize((320, 320), Image.NEAREST))
        img.alpha_composite(big, (x, 100))
        img.alpha_composite(block_view(tile, 320), (x, 440))
        img.alpha_composite(ground_row([tile, tile, current, ref], 80).resize((320, 160), Image.NEAREST), (x, 780))
        d.text((x, 960), name, font=font(24), fill=ink)
        words, line, y = note.split(), '', 996
        for w in words:
            if d.textlength(line + ' ' + w, font=font(18)) > 320:
                d.text((x, y), line.strip(), font=font(18), fill=grey)
                line, y = '', y + 26
            line += ' ' + w
        d.text((x, y), line.strip(), font=font(18), fill=grey)
    os.makedirs(OUT, exist_ok=True)
    img.save(os.path.join(OUT, out))
    print(out, img.size)


def main():
    if 'aries3' in sys.argv[1:]:
        sheet('Widdereichen-Setzling · A größer', ARIES_BIG, mt.ARIES, mt.draw(*mt.SAPLINGS['aries_oak_sapling']),
              'dark_oak_sapling', 'aries_oak_sapling_v3.png')
        return
    if 'cypress' in sys.argv[1:]:
        growth_sheet('Zypressen-Setzling · 5 Vorschläge nach dem Wuchs im Spiel', CYPRESS_IDEAS, mt.CYPRESS,
                     mt.draw(*mt.SAPLINGS['cypress_sapling']), 'spruce_sapling', 'cypress_sapling.png',
                     'eine gewachsene Zypresse aus dem Dev-Server zum Vergleich')
        return
    if 'berry7' in sys.argv[1:]:
        sheet('Erdbeerbaum-Setzling · drei Kronen', BERRY_THREE, mt.STRAWBERRY,
              mt.draw(*mt.SAPLINGS['strawberry_tree_sapling']), 'acacia_sapling', 'strawberry_tree_sapling_v7.png')
        return
    if 'berry6' in sys.argv[1:]:
        sheet('Erdbeerbaum-Setzling · alle Stämme 2 Pixel', BERRY_2PX, mt.STRAWBERRY,
              mt.draw(*mt.SAPLINGS['strawberry_tree_sapling']), 'acacia_sapling', 'strawberry_tree_sapling_v6.png')
        return
    if 'berry5' in sys.argv[1:]:
        sheet('Erdbeerbaum-Setzling · dickere Stämme, glatte Rinde', BERRY_THICK, mt.STRAWBERRY,
              mt.draw(*mt.SAPLINGS['strawberry_tree_sapling']), 'acacia_sapling', 'strawberry_tree_sapling_v5.png')
        return
    if 'berry4' in sys.argv[1:]:
        sheet('Erdbeerbaum-Setzling · 5 Varianten von A', BERRY_A, mt.STRAWBERRY,
              mt.draw(*mt.SAPLINGS['strawberry_tree_sapling']), 'acacia_sapling', 'strawberry_tree_sapling_v4.png')
        return
    if 'berry3' in sys.argv[1:]:
        current = mt.SAPLINGS['strawberry_tree_sapling'][1]
        sheet('Erdbeerbaum-Setzling · zwei Stämme, ohne Wurzel',
              [(n, note, rows or current) for n, note, rows in BERRY_TWO], mt.STRAWBERRY,
              mt.draw(mt.STRAWBERRY, current), 'acacia_sapling', 'strawberry_tree_sapling_v3.png')
        return
    if 'berry2' in sys.argv[1:]:
        current = mt.SAPLINGS['strawberry_tree_sapling'][1]
        sheet('Erdbeerbaum-Setzling · 5 Varianten der jetzigen Textur',
              [(n, note, rows or current) for n, note, rows in BERRY_VARIANTS], mt.ARBUTUS,
              mt.draw(mt.ARBUTUS, current), 'acacia_sapling', 'strawberry_tree_sapling_v2.png')
        return
    if 'palm3' in sys.argv[1:]:
        current = mt.SAPLINGS['date_palm_sapling'][1]
        sheet('Dattelpalmen-Setzling · 5 Kronen', [(n, note, rows or current) for n, note, rows in PALM_LEAVES],
              mt.PALM, mt.draw(mt.PALM, current), 'jungle_sapling', 'date_palm_sapling_v3.png')
        return
    if 'palm2' in sys.argv[1:]:
        sheet('Dattelpalmen-Setzling · ein Stamm, gebogen', PALM_CURVED, mt.PALM,
              mt.draw(*mt.SAPLINGS['date_palm_sapling']), 'jungle_sapling', 'date_palm_sapling_v2.png')
        return
    if 'palm' in sys.argv[1:]:
        growth_sheet('Dattelpalmen-Setzling · nach dem Wuchs im Spiel', PALM_GAME, mt.PALM,
                     mt.draw(*mt.SAPLINGS['date_palm_sapling']), 'jungle_sapling', 'date_palm_sapling.png')
        return
    if 'berry' in sys.argv[1:]:
        growth_sheet('Erdbeerbaum-Setzling · nach dem Wuchs im Spiel', BERRY_GAME, mt.ARBUTUS,
                     mt.draw(*mt.SAPLINGS['strawberry_tree_sapling']), 'acacia_sapling',
                     'strawberry_tree_sapling.png')
        return
    if 'fig6' in sys.argv[1:]:
        grown_sheet()
        return
    if 'fig5' in sys.argv[1:]:
        sheet('Feigen-Setzling · 5 Verzweigungen unter der Krone', FIG_BRANCHES, mt.FIG_FRUIT,
              mt.draw(*mt.SAPLINGS['fig_sapling']), 'acacia_sapling', 'fig_sapling_v5.png')
        return
    if 'fig4' in sys.argv[1:]:
        sheet('Feige · M3 neu', FIG_M3_HUMPS, mt.FIG_FRUIT,
              mt.draw(*mt.SAPLINGS['fig_sapling']), 'acacia_sapling', 'fig_sapling_v4.png')
        return
    if 'fig3' in sys.argv[1:]:
        sheet('Feigen-Setzling · M3 mit einer Krone pro Stamm', FIG_CROWNS, mt.FIG_FRUIT,
              mt.draw(*mt.SAPLINGS['fig_sapling']), 'acacia_sapling', 'fig_sapling_v3.png')
        return
    if 'fig2' in sys.argv[1:]:
        sheet('Feigen-Setzling · 5 Mischungen aus A und B', FIG_MIX, mt.FIG_FRUIT,
              mt.draw(*mt.SAPLINGS['fig_sapling']), 'acacia_sapling', 'fig_sapling_v2.png')
        return
    if 'fig' in sys.argv[1:]:
        sheet('Feigen-Setzling · 5 Vorschläge nach dem Wuchs im Spiel', FIG_GAME, mt.FIG_FRUIT,
              mt.draw(*mt.SAPLINGS['fig_sapling']), 'acacia_sapling', 'fig_sapling.png')
        return
    if 'olive2' in sys.argv[1:]:
        current = mt.draw(*mt.SAPLINGS['olive_sapling'])
        sheet('Oliven-Setzling · 5 Vorschläge nach dem Wuchs im Spiel', OLIVE_GAME, OLIV, current, 'oak_sapling',
              'olive_sapling_v2.png')
        sheet('Oliven-Setzling · dieselben 5 in Azaleengrün wie die Krone im Spiel', OLIVE_GAME, OLIV_AZALEA, current,
              'oak_sapling', 'olive_sapling_v2_azalea.png')
        return
    if 'olive' in sys.argv[1:]:
        sheet('Oliven-Setzling · 5 Vorschläge nach dem echten Baum', OLIVE_IDEAS, OLIV,
              mt.draw(*mt.SAPLINGS['olive_sapling']), 'oak_sapling', 'olive_sapling.png')
        return
    if 'mulberry' in sys.argv[1:]:
        sheet('Maulbeer-Setzling · 5 Vorschläge nach dem echten Baum', MULBERRY_IDEAS, MULB,
              mt.draw(*mt.SAPLINGS['mulberry_sapling']), 'pale_oak_sapling', 'mulberry_sapling.png')
        return
    if '4' in sys.argv[1:]:
        sheet('Trauerweiden-Setzling · neu gezeichnet: Fontänenkrone, Stamm mit leichtem C', WILLOW_FOUNTAIN, WILLOW,
              mt.draw(*mt.SAPLINGS['weeping_willow_sapling']), 'pale_oak_sapling', 'weeping_willow_sapling_v4.png')
        return
    if '3' in sys.argv[1:]:
        sheet('Trauerweiden-Setzling · gekrümmter Stamm, 5 Varianten von B', WILLOW_CURVED, WILLOW,
              mt.draw(*mt.SAPLINGS['weeping_willow_sapling']), 'pale_oak_sapling', 'weeping_willow_sapling_v3.png')
        return
    if '2' in sys.argv[1:]:
        sheet('Widdereichen-Setzling · 3 Varianten von A', ARIES_V2, ARIES,
              mt.draw(*mt.SAPLINGS['aries_oak_sapling']), 'dark_oak_sapling', 'aries_oak_sapling_v2.png')
        sheet('Trauerweiden-Setzling · 3 Varianten von B', WILLOW_V2, WILLOW,
              mt.draw(*mt.SAPLINGS['weeping_willow_sapling']), 'pale_oak_sapling', 'weeping_willow_sapling_v2.png')
        return
    sheet('Widdereichen-Setzling · 5 Vorschläge', ARIES_IDEAS, ARIES, mt.draw(*mt.SAPLINGS['aries_oak_sapling']),
          'dark_oak_sapling', 'aries_oak_sapling.png')
    sheet('Trauerweiden-Setzling · 5 Vorschläge (Blasseiche + Azalee)', WILLOW_IDEAS, WILLOW,
          mt.draw(*mt.SAPLINGS['weeping_willow_sapling']), 'pale_oak_sapling', 'weeping_willow_sapling.png')


if __name__ == '__main__':
    main()
