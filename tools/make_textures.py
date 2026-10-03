"""Pixel art for the Greek Trees mod: saplings, fruit items, fruit twigs and date cluster swatches (the icon:
tools/make_icons.py).

python tools/make_textures.py            writes the textures into src/main/resources
python tools/make_textures.py --preview  also writes art/preview_saplings.png and art/preview_fruit.png
"""
import io
import os
import sys
import zipfile

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import date_cluster  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(ROOT, 'src', 'main', 'resources', 'assets', 'greektrees', 'textures', 'block')
ITEM_TEX = os.path.join(ROOT, 'src', 'main', 'resources', 'assets', 'greektrees', 'textures', 'item')
ART = os.path.join(ROOT, 'art')

# ---------------------------------------------------------------- palettes (shared keys per sapling)

CYPRESS = {
    '1': (34, 60, 28), '2': (48, 82, 34), '3': (66, 106, 42), '4': (90, 132, 52), '5': (120, 160, 70),
    'a': (70, 66, 60), 'b': (100, 94, 86), 'c': (128, 121, 110),
}
OLIVE = {
    '1': (70, 86, 58), '2': (96, 114, 78), '3': (128, 146, 104), '4': (164, 178, 136), '5': (198, 208, 174),
    'a': (66, 50, 34), 'b': (96, 74, 48), 'c': (128, 102, 68),
    'k': (40, 30, 44), 'm': (78, 58, 86),
}
# the four greens of vanilla azalea_leaves (the fig tree's leaves), with one darker shade under them for edges
AZALEA_LEAF = {'1': (46, 60, 32), '2': (58, 76, 38), '3': (80, 105, 44), '4': (108, 128, 49), '5': (112, 146, 45)}
FIG = {
    **AZALEA_LEAF,
    'a': (92, 88, 80), 'b': (122, 116, 104), 'c': (150, 144, 130),
    'k': (86, 42, 80), 'm': (128, 70, 112),
}
STRAWBERRY = {
    '1': (30, 54, 24), '2': (44, 76, 30), '3': (62, 100, 38), '4': (86, 128, 48), '5': (112, 154, 62),
    'a': (130, 52, 30), 'b': (172, 78, 44), 'c': (210, 112, 66),
    'r': (180, 30, 30), 's': (230, 76, 52), 'o': (236, 150, 52),
}
PALM = {
    '1': (44, 84, 30), '2': (66, 116, 40), '3': (96, 150, 54), '4': (130, 182, 74), '5': (164, 206, 100),
    'a': (84, 60, 34), 'b': (116, 86, 50), 'c': (148, 114, 70),
    'o': (204, 128, 42), 'r': (150, 80, 30),
}
DATE = {
    'o': (62, 30, 16), 'd': (98, 50, 24), 'm': (132, 72, 34), 'h': (182, 118, 64), 'w': (226, 178, 120),
    's': (196, 150, 70), 'S': (150, 108, 48),
}

# mulberry: the grey-brown pale oak bark and the jungle leaves of its crown (plains tint), black fruit (k m h)
MULBERRY = {
    '1': (40, 58, 16), '2': (52, 73, 20), '3': (70, 102, 28), '4': (98, 128, 26), '5': (110, 147, 30),
    'a': (58, 51, 49), 'b': (78, 67, 64), 'c': (110, 100, 98),
    'k': (34, 10, 30), 'm': (72, 22, 62), 'h': (130, 62, 112),
}
# weeping willow: pale oak bark and the azalea greens of its curtain
WILLOW = {**AZALEA_LEAF, 'a': (58, 51, 49), 'b': (78, 67, 64), 'c': (94, 83, 80), 'd': (110, 100, 98)}

# Aries oak: the azalea greens with pink flowers (f), jungle leaf patches (j J), dark oak bark (a b c d), a streak of
# stripped dark oak (s)
ARIES = {**AZALEA_LEAF, 'f': (186, 98, 206), 'j': (52, 73, 20), 'J': (98, 128, 26), 'a': (41, 32, 17),
         'b': (51, 39, 21), 'c': (74, 56, 30), 'd': (88, 68, 40), 's': (82, 63, 39)}

# figs: grey bark and the azalea greens of the crown from FIG; green young figs (g G d), a purple blush (u), ripe
# purple (k m h, p eye)
FIG_FRUIT = {**FIG, 'g': (112, 146, 52), 'G': (152, 186, 84), 'd': (72, 100, 34), 'u': (120, 84, 96),
             'k': (58, 28, 56), 'm': (110, 56, 96), 'h': (164, 104, 146), 'p': (186, 104, 120)}
# mulberries: grey bark and jungle leaves from MULBERRY; every kind starts white-green (w v g). Black: red (p r R),
# then black (k m h H). White: cream (y Y e), then white with a pink blush (W x z, q). Red: pink (s p P), then deep
# red (l r R D).
MULBERRY_FRUIT = dict(MULBERRY, w=(220, 226, 182), v=(184, 202, 132), g=(142, 168, 92), p=(236, 130, 128),
                      r=(198, 50, 62), R=(138, 24, 42), H=(176, 118, 156),
                      y=(234, 228, 164), Y=(208, 202, 130), e=(174, 172, 102),
                      W=(248, 246, 236), x=(226, 220, 206), z=(196, 184, 168), q=(240, 188, 194),
                      s=(246, 172, 164), P=(212, 92, 98), l=(232, 112, 112), D=(96, 12, 32))

# ---------------------------------------------------------------- sapling pixel maps (16 x 16, '.' = clear)

SAPLINGS = {
    # After the grown tree (TreeShapes.cypress): a thin spire, a narrow upper body, widest in the lower third, a
    # narrow foot over a short grey trunk (proposal Z1 of tools/sapling_concepts.py cypress).
    'cypress_sapling': (CYPRESS, [
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
    ]),
    # After the grown tree (TreeShapes.olive): roots on the ground, a narrow neck, a thick trunk with a hole
    # between its stems, a flat crown with two humps and a branch poking out, olives under its rim (proposal B of
    # round 2, tools/sapling_concepts.py olive2, the widest root row cut off, the root a pixel narrower each side).
    'olive_sapling': (OLIVE, [
        '................',
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
        '......cbba......',
        '.....cbbbba.....',
    ]),
    # After the grown tree (TreeShapes.fig): a short broad fan of grey wood under a low, wide crown that bulges
    # over every stem, figs at its rim (proposal F4 of tools/sapling_concepts.py fig6, after growth 5).
    'fig_sapling': (FIG_FRUIT, [
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
    ]),
    # Smooth orange-red stems 2 px wide: the trunk forks, the right arm forks again; three crowns at different
    # heights with red and orange berries.
    'strawberry_tree_sapling': (STRAWBERRY, [
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
    # After the grown tree (TreeShapes.datePalm): a slim ringed trunk bowing a pixel to the left, fronds fanning
    # out with gaps between them, two short ones up, two arching, two drooping to the edge, the dates beside the
    # trunk under them (trunk: proposal C1 of tools/sapling_concepts.py palm2, a pixel lower, bow 1 px deep in
    # rows 8-12; crown: L1 of palm3).
    'date_palm_sapling': (PALM, [
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
    # A short stout trunk without a root foot, forking low under a dense round dome, mulberries white-green, red and
    # black at once (proposal A of tools/sapling_concepts.py mulberry, a pixel lower, the trunk 2 px thick).
    'mulberry_sapling': (MULBERRY_FRUIT, [
        '................',
        '.....455454.....',
        '...3455455443...',
        '..345545345543..',
        '.34554323455543.',
        '.45543234554354.',
        '.34432123443243.',
        '.23321212332132.',
        '.12211212221121.',
        '..w11cb11cb11h..',
        '..v.p.cbcb...k..',
        '....R..cb.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
        '.......cb.......',
    ]),
    # A domed crown whose strands spring from the top like a fountain and fall, longest at the rim, dark between
    # them, open in the middle over a pale trunk with a slight C (proposal W1 of tools/sapling_concepts.py).
    'weeping_willow_sapling': (WILLOW, [
        '......5444......',
        '....45554444....',
        '...5545544444...',
        '.52525422342424.',
        '4242424223232323',
        '4242424223232323',
        '4141413113131313',
        '41414.3cb3.31313',
        '31413.2cb2.31313',
        '31413.db...31313',
        '3.3.3.cb...3.3.3',
        '2.3.2.cb...2.3.2',
        '..2...db.....2..',
        '..2....cb....2..',
        '.......cb.......',
        '......cabc......',
    ]),
    # The giant in small: a flowering dome with jungle leaf patches, two side crowns on branches, a trunk with a
    # flared foot (proposal A of tools/sapling_concepts.py).
    'aries_oak_sapling': (ARIES, [
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
}

# ---------------------------------------------------------------- fruit: items and the twigs under the leaves

# olive twigs: bark and silvery leaves from OLIVE, then green olives (g G d) and purple-black ones (k m h)
OLIVE_STAGES = [
    dict(OLIVE, g=(110, 140, 50), G=(150, 180, 80), d=(74, 100, 32)),
    dict(OLIVE, g=(150, 156, 58), G=(196, 198, 104), d=(104, 110, 40), k=(84, 46, 66), m=(138, 78, 108),
         h=(182, 130, 152)),
    dict(OLIVE, k=(34, 24, 38), m=(70, 48, 80), h=(124, 96, 136)),
]
OLIVE_ITEM_PAL = dict(OLIVE, h=(130, 104, 140), d=(82, 100, 34), g=(124, 144, 52), G=(170, 188, 96))
PIT = {'o': (96, 66, 40), 'b': (178, 142, 98), 'l': (214, 186, 142), 'r': (140, 104, 66)}
SHARP_PIT = dict(PIT, w=(244, 234, 210))
# arbutus: red bark and dark leaves from STRAWBERRY, white flowers, green, yellow, orange and red berries
ARBUTUS = dict(STRAWBERRY, R=(126, 18, 22), r=(196, 32, 30), s=(232, 76, 56), p=(252, 150, 120), y=(236, 196, 70),
               Y=(252, 232, 140), e=(200, 150, 40), o=(236, 140, 40), q=(252, 186, 92), O=(190, 92, 24),
               g=(130, 160, 60), G=(170, 196, 96), d=(90, 118, 40), w=(236, 232, 216), W=(255, 255, 250),
               P=(230, 168, 168))

ITEMS = {
    # A ripe black olive and a green one on a twig with a narrow silvery leaf.
    'olive': (OLIVE_ITEM_PAL, [
        '................',
        '............ab..',
        '...........ab...',
        '..55443...ab....',
        '.54433221ab.....',
        '..33221.ab......',
        '........ab......',
        '.......b..b.....',
        '......b....b....',
        '....kkk...ddd...',
        '...kmhmk.dGGgd..',
        '...kmmmk.dGggd..',
        '...kmmmk.dgggd..',
        '...kkmmk.ddggd..',
        '....kkk...ddd...',
        '................',
    ]),
    # The ridged stone left over from an olive.
    'olive_pit': (PIT, [
        '................',
        '................',
        '................',
        '.......oo.......',
        '......olbo......',
        '.....olbrbo.....',
        '.....olbrbo.....',
        '.....lbrbbo.....',
        '.....obrbbo.....',
        '.....obbrbo.....',
        '.....obbrbo.....',
        '......obbo......',
        '.......oo.......',
        '................',
        '................',
        '................',
    ]),
    # A filed pit with a bright cutting edge and a sharp tip.
    'sharpened_olive_pit': (SHARP_PIT, [
        '................',
        '................',
        '........w.......',
        '.......wl.......',
        '.......wlo......',
        '......wlbo......',
        '......wlbo......',
        '......lbro......',
        '.....olbrbo.....',
        '.....obrbbo.....',
        '.....obbrbo.....',
        '.....obbrbo.....',
        '......obbo......',
        '.......oo.......',
        '................',
        '................',
    ]),
    # A ripe purple fig under a lobed leaf.
    'fig': (FIG_FRUIT, [
        '................',
        '.........454....',
        '........45554...',
        '........34543...',
        '.......bc232....',
        '.......b........',
        '......kmk.......',
        '.....kmmmk......',
        '....kmhmmmk.....',
        '....kmhmmmk.....',
        '....kmmmmmk.....',
        '....kmmmpmk.....',
        '.....kmppk......',
        '......kkk.......',
        '................',
        '................',
    ]),
    # A red and an orange arbutus berry with their grainy skin, under a dark leaf.
    'arbutus_berry': (ARBUTUS, [
        '................',
        '..........345...',
        '.........34543..',
        '.........2332...',
        '........a.......',
        '.......a........',
        '......a.a.......',
        '.....a...a......',
        '...rsr...oqo....',
        '..rpsrr.oqqoo...',
        '..srysR.qoyqO...',
        '..rsrRR.ooqOO...',
        '...RRR...OOO....',
        '................',
        '................',
        '................',
    ]),
    # A ripe black mulberry, bumpy like a blackberry, on its stalk under a small leaf.
    'black_mulberry': (MULBERRY_FRUIT, [
        '................',
        '........34......',
        '.......3453.....',
        '.......b232.....',
        '.......b........',
        '......hHm.......',
        '.....hmkmk......',
        '.....mkmkm......',
        '.....kmkmk......',
        '.....mkmkm......',
        '.....kmkmk......',
        '......kmk.......',
        '.......k........',
        '................',
        '................',
        '................',
    ]),
    # A ripe white mulberry, cream white with a pink blush.
    'white_mulberry': (MULBERRY_FRUIT, [
        '................',
        '........34......',
        '.......3453.....',
        '.......b232.....',
        '.......b........',
        '......qWx.......',
        '.....qxWxz......',
        '.....xWxWx......',
        '.....WxWxz......',
        '.....xWxWx......',
        '.....zxWxz......',
        '......zxz.......',
        '.......z........',
        '................',
        '................',
        '................',
    ]),
    # A ripe red mulberry, deep red.
    'red_mulberry': (MULBERRY_FRUIT, [
        '................',
        '........34......',
        '.......3453.....',
        '.......b232.....',
        '.......b........',
        '......lrR.......',
        '.....lrRrD......',
        '.....rRrRr......',
        '.....RrRrD......',
        '.....rRrRr......',
        '.....DrRrD......',
        '......DrD.......',
        '.......D........',
        '................',
        '................',
        '................',
    ]),
}

# twig textures for the cross model: the twig starts at the top edge, under the leaf block it hangs from
_OLIVE_TOP = [
    '.......ab.......',
    '.......ba.......',
    '.5443..ab.......',
    '..32211ba.......',
    '.......ab.3445..',
    '.......ba12233..',
    '.......ab.......',
    '......b.b.b.....',
    '.....b..b..b....',
]
_ARBUTUS_TOP = [
    '.......ab.......',
    '..345..ba.......',
    '.23454.ab.454...',
    '..1233.ba34543..',
    '.......ab.2332..',
    '.......ba.......',
    '.......ab.......',
    '......b.b.b.....',
    '.....b..b..b....',
]
_FIG_TOP = [
    '.......cb.......',
    '..454..bc.......',
    '.45554.cb..454..',
    '.34543.bc.45554.',
    '..2.32.cb.34543.',
    '.......bc..232..',
    '......c..b......',
    '.....c....b.....',
]
_MULBERRY_TOP = [
    '.......ab.......',
    '..343..ba..343..',
    '.34543.ab.34543.',
    '.23432.ba.23432.',
    '..2.2.b..a.2.2..',
    '.....b....a.....',
]
TWIGS = {
    # young: a short twig, two leaves, two small green olives
    'olive_twig_stage0': (OLIVE_STAGES[0], [
        '.......ab.......',
        '.......ba.......',
        '..5443.ab.......',
        '...3221ba.3445..',
        '.......ab12233..',
        '......b..b......',
        '.....b....b.....',
        '.....g....g.....',
        '....gGg..gGg....',
        '....ggd..ggd....',
        '.....d....d.....',
        '................',
        '................',
        '................',
        '................',
        '................',
    ]),
    # half ripe: three olives, the outer ones yellowish green, the middle one turning purple
    'olive_twig_stage1': (OLIVE_STAGES[1], _OLIVE_TOP + [
        '....gg..b...gg..',
        '...gGgg.kk.gGgg.',
        '...gggdkmhkgggd.',
        '....dd.kmmk.dd..',
        '.......kmmk.....',
        '........kk......',
        '................',
    ]),
    # ripe: three big purple-black olives
    'olive_twig_stage2': (OLIVE_STAGES[2], _OLIVE_TOP + [
        '....kk..b...kk..',
        '...kmhk.kk.kmhk.',
        '...kmmkkmhkkmmk.',
        '...kmmkkmmkkmmk.',
        '...kkmkkmmkkkmk.',
        '....kk.kkmk.kk..',
        '........kk......',
    ]),
    # young: two small green figs under big lobed leaves
    'fig_twig_stage0': (FIG_FRUIT, [
        '.......cb.......',
        '..454..bc.......',
        '.45554.cb..454..',
        '.34543.bc.45554.',
        '..2.32.cb.34543.',
        '......c.b..232..',
        '.....c...b......',
        '.....d...d......',
        '....gGd.gGd.....',
        '....ggd.ggd.....',
        '.....d...d......',
        '................',
        '................',
        '................',
        '................',
        '................',
    ]),
    # half ripe: bigger green figs with a purple blush
    'fig_twig_stage1': (FIG_FRUIT, _FIG_TOP + [
        '.....dd...dd....',
        '.....gd...gd....',
        '....gGgu.gGgu...',
        '....ggud.ggud...',
        '.....uu...uu....',
        '................',
        '................',
        '................',
    ]),
    # ripe: two fat purple figs
    'fig_twig_stage2': (FIG_FRUIT, _FIG_TOP + [
        '.....k....k.....',
        '....kmk..kmk....',
        '...kmhmkkmhmk...',
        '...kmmmkkmmmk...',
        '...kmmpkkmmpk...',
        '....kkk..kkk....',
        '................',
        '................',
    ]),
    # young: white urn flowers next to a small green berry
    'arbutus_twig_stage0': (ARBUTUS, [
        '.......ab.......',
        '..345..ba.......',
        '.23454.ab.454...',
        '..1233.ba34543..',
        '.......ab.2332..',
        '......b..b......',
        '.....b....b.....',
        '....wWw..gGg....',
        '....wWw..ggd....',
        '.....P....d.....',
        '................',
        '................',
        '................',
        '................',
        '................',
        '................',
    ]),
    # half ripe: yellow and orange berries
    'arbutus_twig_stage1': (ARBUTUS, _ARBUTUS_TOP + [
        '....yy..b...yy..',
        '...yYyy.oo.yYyy.',
        '...yyyeoqooyyye.',
        '....ee.oooO.ee..',
        '........OO......',
        '................',
        '................',
    ]),
    # ripe: three big red berries
    'arbutus_twig_stage2': (ARBUTUS, _ARBUTUS_TOP[:7] + [
        '......b.b.b.....',
        '.....b..b..b....',
        '....b...b...rsr.',
        '..rsr...b..rpsrr',
        '.rpsrr.rsr.srysR',
        '.srysRrpsrrrsrRR',
        '.rsrRRsrysR.RRR.',
        '..RRR.rsrRR.....',
        '.......RRR......',
    ]),
    # black mulberry, young: two small white-green mulberries under broad leaves
    'black_mulberry_twig_stage0': (MULBERRY_FRUIT, _MULBERRY_TOP + [
        '.....v....v.....',
        '....wvg..wvg....',
        '....vgg..vgg....',
        '.....g....g.....',
    ] + ['................'] * 6),
    # half ripe: longer, red
    'black_mulberry_twig_stage1': (MULBERRY_FRUIT, _MULBERRY_TOP + [
        '.....g....g.....',
        '....prR..prR....',
        '....rRr..rRr....',
        '....RrR..RrR....',
        '.....R....R.....',
    ] + ['................'] * 5),
    # ripe: long, black, bumpy
    'black_mulberry_twig_stage2': (MULBERRY_FRUIT, _MULBERRY_TOP + [
        '.....b....b.....',
        '....Hmk..hmk....',
        '....mkm..mkm....',
        '....kmk..kmk....',
        '....mkm..mkm....',
        '.....k....k.....',
    ] + ['................'] * 4),
    # white mulberry: young like the others, then cream, ripe white with a pink blush
    'white_mulberry_twig_stage0': (MULBERRY_FRUIT, _MULBERRY_TOP + [
        '.....v....v.....',
        '....wvg..wvg....',
        '....vgg..vgg....',
        '.....g....g.....',
    ] + ['................'] * 6),
    'white_mulberry_twig_stage1': (MULBERRY_FRUIT, _MULBERRY_TOP + [
        '.....g....g.....',
        '....yYe..yYe....',
        '....YyY..YyY....',
        '....eYy..eYy....',
        '.....e....e.....',
    ] + ['................'] * 5),
    'white_mulberry_twig_stage2': (MULBERRY_FRUIT, _MULBERRY_TOP + [
        '.....b....b.....',
        '....Wxq..Wxz....',
        '....xWx..xWx....',
        '....zxW..zxq....',
        '....xzx..xzx....',
        '.....z....z.....',
    ] + ['................'] * 4),
    # red mulberry: young like the others, then pink, ripe deep red
    'red_mulberry_twig_stage0': (MULBERRY_FRUIT, _MULBERRY_TOP + [
        '.....v....v.....',
        '....wvg..wvg....',
        '....vgg..vgg....',
        '.....g....g.....',
    ] + ['................'] * 6),
    'red_mulberry_twig_stage1': (MULBERRY_FRUIT, _MULBERRY_TOP + [
        '.....g....g.....',
        '....spP..spP....',
        '....pPp..pPp....',
        '....PpP..PpP....',
        '.....P....P.....',
    ] + ['................'] * 5),
    'red_mulberry_twig_stage2': (MULBERRY_FRUIT, _MULBERRY_TOP + [
        '.....b....b.....',
        '....lrR..lrD....',
        '....rRr..rRr....',
        '....RrD..RrR....',
        '....rDR..rDR....',
        '.....D....D.....',
    ] + ['................'] * 4),
}

# Two glossy dates hanging from a short yellow stalk.
DATE_ITEM = [
    '................',
    '...........ss...',
    '..........sS....',
    '.........sS.....',
    '....oo..sSoo....',
    '...ohwoSSohwo...',
    '..ohhmmo.ohmmo..',
    '..ohmmmo.ommmo..',
    '..ommmmdoommmdo.',
    '..ommmmdoommmdo.',
    '..ommmdo..ommdo.',
    '..odmmdo..oddo..',
    '...oddo....oo...',
    '....oo..........',
    '................',
    '................',
]


def draw(palette, rows):
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row)
        for x, ch in enumerate(row):
            if ch != '.':
                img.putpixel((x, y), palette[ch] + (255,))
    return img


def main():
    os.makedirs(TEX, exist_ok=True)
    os.makedirs(ITEM_TEX, exist_ok=True)
    tiles = {}
    for name, (palette, rows) in SAPLINGS.items():
        img = draw(palette, rows)
        img.save(os.path.join(TEX, name + '.png'))
        tiles[name] = img
    date = draw(DATE, DATE_ITEM)
    date.save(os.path.join(ITEM_TEX, 'date.png'))
    for i in range(3):
        Image.fromarray(date_cluster.stage_texture(i), 'RGBA').save(os.path.join(TEX, f'date_cluster_stage{i}.png'))
    items = {'date': date}
    for name, (palette, rows) in ITEMS.items():
        items[name] = draw(palette, rows)
        items[name].save(os.path.join(ITEM_TEX, name + '.png'))
    twigs = {}
    for name, (palette, rows) in TWIGS.items():
        twigs[name] = draw(palette, rows)
        twigs[name].save(os.path.join(TEX, name + '.png'))
    if '--preview' in sys.argv:
        preview(tiles)
        preview_fruit(items, twigs)


def vanilla(name):
    jar = zipfile.ZipFile(os.path.expanduser('~/.gradle/caches/fabric-loom/26.2/minecraft-client.jar'))
    return Image.open(io.BytesIO(jar.read(f'assets/minecraft/textures/block/{name}.png'))).convert('RGBA')


def preview(tiles):
    """Each sapling large, then in context on grass next to a vanilla oak sapling."""
    os.makedirs(ART, exist_ok=True)
    names = list(tiles)
    cell = 200
    sheet = Image.new('RGBA', (cell * (len(names) + 1), cell * 2 + 30), (226, 232, 238, 255))
    d = ImageDraw.Draw(sheet)
    ref = vanilla('oak_sapling')
    for i, name in enumerate(names + ['(vanilla oak)']):
        t = tiles.get(name, ref)
        bg = Image.new('RGBA', (176, 176), (150, 190, 230, 255))
        bg.alpha_composite(t.resize((176, 176), Image.NEAREST))
        sheet.alpha_composite(bg, (i * cell + 12, 10))
        ctx = Image.new('RGBA', (64, 64), (150, 190, 230, 255))
        ctx.alpha_composite(vanilla('grass_block_side').resize((64, 16), Image.NEAREST), (0, 48))
        for k, x in enumerate((0, 16, 32, 48)):
            ctx.alpha_composite(t if k != 3 else ref, (x, 32))
        sheet.alpha_composite(ctx.resize((176, 176), Image.NEAREST), (i * cell + 12, cell + 10))
        d.text((i * cell + 14, cell * 2 + 12), name, fill=(30, 50, 80, 255))
    sheet.save(os.path.join(ART, 'preview_saplings.png'))


def preview_fruit(items, twigs):
    """The fruit items, the twigs hanging under their leaf block at each stage, and the date cluster stages on the
    palm trunk (seen from outside, the trunk behind)."""
    sky, ink = (150, 190, 230, 255), (30, 50, 80, 255)
    sheet = Image.new('RGBA', (12 + 204 * len(twigs), 1010), (226, 232, 238, 255))
    d = ImageDraw.Draw(sheet)
    d.text((14, 8), 'Items', fill=ink)
    for i, name in enumerate(('olive', 'olive_pit', 'sharpened_olive_pit', 'fig', 'arbutus_berry', 'date',
                              'black_mulberry', 'white_mulberry', 'red_mulberry')):
        bg = Image.new('RGBA', (176, 176), sky)
        bg.alpha_composite(items[name].resize((176, 176), Image.NEAREST))
        sheet.alpha_composite(bg, (12 + i * 200, 26))
        d.text((14 + i * 200, 206), name, fill=ink)
    d.text((14, 232), 'Zweige unter dem Laub (im Spiel als Kreuz wie ein Setzling), Stufe 0 / 1 / 2', fill=ink)
    azalea = vanilla('azalea_leaves')
    leaves = {'olive_twig': azalea, 'fig_twig': azalea, 'arbutus_twig': _tint(vanilla('mangrove_leaves'), (146, 192, 76)),
              **{f'{kind}_mulberry_twig': _tint(vanilla('jungle_leaves'), (119, 171, 47))
                 for kind in ('black', 'white', 'red')}}
    for i, name in enumerate(twigs):
        tile = Image.new('RGBA', (16, 32), sky)
        tile.alpha_composite(leaves[name.rsplit('_stage', 1)[0]], (0, 0))
        tile.alpha_composite(twigs[name], (0, 16))
        x = 12 + i * 204
        sheet.alpha_composite(tile.resize((128, 256), Image.NEAREST), (x + 30, 250))
        d.text((x, 512), name, fill=ink)
    d.text((14, 540), 'Dattelrispe Stufe 0 / 1 / 2 (Mischung aus B und C, gleicher Massstab)', fill=ink)
    import date_concepts
    import raycast
    ripe = date_concepts.cluster_boxes(date_cluster.STAGES[2], 2, (0, 0, -1))
    centre, scale = raycast.fit(ripe, date_concepts.VIEW, (400, 400))
    for stage in range(3):
        boxes = date_concepts.cluster_boxes(date_cluster.STAGES[stage], stage, (0, 0, -1))
        img = raycast.render(boxes, date_concepts.VIEW, centre, scale, (400, 400)).convert('RGBA')
        sheet.alpha_composite(img, (12 + stage * 410, 560))
    sheet.save(os.path.join(ART, 'preview_fruit.png'))


def _tint(img, colour):
    """Vanilla leaf textures are grey where the game tints them by biome; azalea leaves come coloured."""
    if colour is None:
        return img
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            px[x, y] = (r * colour[0] // 255, g * colour[1] // 255, b * colour[2] // 255, a)
    return out


if __name__ == '__main__':
    main()
