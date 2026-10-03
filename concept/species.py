"""The five picked Greek trees: cypress, olive, fig, strawberry tree, Cretan date palm.

Each species is split into two steps, the same split the Java feature will use:

    roll(rng)        draws every random choice once and returns it as a plain dict of named values
    build(p, rng)    turns those values into blocks; the only randomness left here is the ragged rim of
                     leaf clouds (each rim block is kept or dropped on its own)

grow(key, seed, **override) runs both; override pins single values (used for the anatomy figures).
Angles are in degrees, lengths in blocks. Coordinates: y = 0 is the sapling's block, trunk base at x = z = 0.
"""
import math
import random

from trees import CARDINALS, Tree, ip, polar

R = math.radians


def _note(t, kind, label, **kw):
    t.notes.append(dict(kind=kind, label=label, **kw))


# ==================================================================================== 01 cypress

SIDE4 = [(1, 0), (0, 1), (-1, 0), (0, -1)]
CORNER4 = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
ARM4 = [(2, 0), (0, 2), (-2, 0), (0, -2)]


def cypress_roll(r):
    """Rules measured on the 32 hand-built cypresses of the Greek city (MC5 backup, built/trees.json).
    Layers above the 4-block trunk, bottom to top:
      Fuß      P = plus (3x3 without corners), T = plus with 1-3 corners
      Körper   B = full 3x3, plus 'Leisten': single blocks two out from the centre of a side
      Übergang T layers
      Kreuz    P layers
      Kappe    S = centre plus 1-3 sides
      Spitze   centre only
    """
    # The builds keep their height tight (20-23, mostly 22): roll the height first, then the bands, and let
    # the body take up the rest. Bands are re-rolled until the body fits its measured spread.
    hoehe = r.choices([20, 21, 22, 23], weights=[3, 7, 65, 25])[0]
    while True:
        fuss = r.choices(['PT', 'PP', 'P'], weights=[85, 10, 5])[0]
        uebergang = r.choices([0, 1, 2], weights=[1, 8, 1])[0]
        kreuz = r.choices([2, 3, 4], weights=[3, 5, 2])[0]
        kappe = r.choices([0, 1, 2], weights=[15, 50, 35])[0]
        spitze = r.choice([4, 5])
        koerper = hoehe - 4 - len(fuss) - uebergang - kreuz - kappe - spitze
        if kappe + spitze > 6:
            continue  # the tip must stay within leaf distance 6 of the log, which ends in the top plus layer
        if r.random() < {5: 0.12, 6: 1.0, 7: 0.75, 8: 0.12}.get(koerper, 0):  # measured: mostly 6-7
            break

    def t_layer():
        return dict(art='T', ecken=sorted(r.sample(range(4), r.randint(1, 3))))

    layers = [t_layer() if k == 'T' else dict(art='P') for k in fuss]
    for i in range(koerper):
        p_arm = 0.7 if i == 0 else 0.55 if i == koerper - 1 else 0.86  # Leisten thin out at both ends
        layers.append(dict(art='B', leisten=[n for n in range(4) if r.random() < p_arm]))
    layers += [t_layer() for _ in range(uebergang)]
    layers += [dict(art='P') for _ in range(kreuz)]
    n_sides = 4
    for _ in range(kappe):
        n_sides = r.randint(1, min(3, n_sides))
        layers.append(dict(art='S', seiten=sorted(r.sample(range(4), n_sides))))
    layers += [dict(art='O') for _ in range(spitze)]
    return dict(stamm=4, fuss=fuss, koerper=koerper, uebergang=uebergang, kreuz=kreuz, kappe=kappe, spitze=spitze,
                tropfen=r.randrange(4) if r.random() < 0.08 else None,  # lone leaf on the trunk below the crown
                schichten=layers, hoehe=4 + len(layers))


def cypress_build(p, rng):
    t = Tree(rng)
    LOG, LEAF = 'acacia_log', 'azalea_leaves'
    h = p['hoehe']
    y_body = p['stamm'] + len(p['fuss'])
    # Like the builds near the temple: the log runs up through the top plus layer, cap and spire are leaves only.
    log_top = h - p['spitze'] - p['kappe'] - 1
    for y in range(log_top + 1):
        t.log((0, y, 0), LOG)
    for i, layer in enumerate(p['schichten']):
        y = p['stamm'] + i
        cells = [(0, 0)]
        art = layer['art']
        if art in 'PTB':
            cells += SIDE4
        if art == 'T':
            cells += [CORNER4[n] for n in layer['ecken']]
        if art == 'B':
            cells += CORNER4 + [ARM4[n] for n in layer['leisten']]
        if art == 'S':
            cells += [SIDE4[n] for n in layer['seiten']]
        for x, z in cells:
            t.leaf((x, y, z), LEAF)
    if p['tropfen'] is not None:
        x, z = SIDE4[p['tropfen']]
        t.leaf((x, p['stamm'] - 1, z), LEAF)
    y = p['stamm']
    for name, n in (('Fuß', len(p['fuss'])), ('Körper', p['koerper']), ('Übergang', p['uebergang']),
                    ('Kreuz', p['kreuz']), ('Kappe', p['kappe']), ('Spitze', p['spitze'])):
        if n:
            _note(t, 'vbar', f'{name} {n}', y0=y, y1=y + n - 1)
        y += n
    _note(t, 'vbar', 'Stamm 4', y0=0, y1=p['stamm'] - 1)
    body = p['schichten'][len(p['fuss']):len(p['fuss']) + p['koerper']]
    for n, x in ((0, 2), (2, -2)):  # east and west Leisten show in the side view
        ys = [y_body + i for i, layer in enumerate(body) if n in layer['leisten']]
        if ys:
            _note(t, 'dot', 'Leiste', x=x, y=sum(ys) / len(ys))
    t.ground(3.5)
    return t


def cypress_summary(p):
    leisten = sum(len(layer.get('leisten', [])) for layer in p['schichten'])
    return [f'Höhe {p["hoehe"]} = 4+{len(p["fuss"])}+{p["koerper"]}+{p["uebergang"]}+{p["kreuz"]}+{p["kappe"]}+{p["spitze"]}',
            f'{leisten} Leistenblöcke' + (' · Tropfen' if p['tropfen'] is not None else '')]


# ==================================================================================== 02 olive

def olive_roll(r):
    n = r.choice([2, 2, 3])
    a0 = r.uniform(0, 360)
    staemme = []
    for i in range(n):
        w = a0 + i * 360 / n + r.uniform(-17, 17)
        staemme.append(dict(
            winkel=w,                           # direction the stem leans to
            hoehe=r.randint(5, 6),              # height of the stem top
            neigung=r.uniform(1.6, 2.2),        # how far the top leans out
            ast=w + r.uniform(-34, 34),         # short limb into the crown
            krone_r=r.uniform(3.2, 3.8),        # crown cloud radius, horizontal
            krone_h=r.uniform(1.7, 2.1),        # crown cloud radius, vertical
        ))
    extra = [dict(stamm=r.randrange(n), winkel=r.uniform(0, 360), abstand=r.uniform(2.0, 2.8))
             for _ in range(r.randint(2, 3))]
    return dict(drehung=a0, staemme=staemme, extra=extra)


def olive_build(p, rng):
    t = Tree(rng)
    LOG, LEAF = 'oak_log', 'oak_leaves'
    for q in ((0, 0, 0), (0, 1, 0), (1, 0, 0)):
        t.log(q, LOG)
    t.log((-1, 0, 0), LOG, 'x')  # root lying on the ground
    _note(t, 'dot', 'Wurzel', x=-1, y=0)
    tops = []
    for i, s in enumerate(p['staemme']):
        dx, dz = polar(R(s['winkel']), s['neigung'])
        knee = (dx * 0.6, 2.6, dz * 0.6)
        top = (dx, s['hoehe'], dz)
        t.path([(0, 1, 0), knee, top], LOG, 'y')
        ox, oz = polar(R(s['ast']), 2)
        t.branch(top, (dx + ox, s['hoehe'] + 1, dz + oz), LOG)
        c = (dx + ox * 0.5, s['hoehe'], dz + oz * 0.5)
        tops.append(c)
        t.blob((c[0], c[1] + 1.6, c[2]), s['krone_r'], s['krone_h'], s['krone_r'], LEAF, erode=0.25, floor=c[1])
        _note(t, 'ellipse', f'Krone {s["krone_r"]:.1f}', x=c[0], y=c[1] + 1.6, z=c[2], rx=s['krone_r'], ry=s['krone_h'])
        if i == 0:
            _note(t, 'vbar', f'Stamm {s["hoehe"]}', y0=0, y1=s['hoehe'] - 1)
    for e in p['extra']:
        x, y, z = tops[e['stamm']]
        ox, oz = polar(R(e['winkel']), e['abstand'])
        t.blob((x + ox, y + 1, z + oz), 2.2, 1.3, 2.2, LEAF, erode=0.3, floor=y)
    t.ground(5.5)
    return t


def olive_summary(p):
    s = p['staemme']
    return [f'{len(s)} Stämme · Höhe {"/".join(str(q["hoehe"]) for q in s)}',
            f'Kronen r {"/".join(f"{q["krone_r"]:.1f}" for q in s)} · {len(p["extra"])} Zusatzwolken']


# ==================================================================================== 06 fig

def fig_roll(r):
    n = r.randint(4, 5)
    a0 = r.uniform(0, 360)
    staemme = [dict(
        winkel=a0 + i * 360 / n + r.uniform(-20, 20),
        knie_weite=r.uniform(2.0, 3.0),     # first bend: how far out ...
        knie_hoehe=r.randint(1, 2),         # ... and how high
        weite=r.uniform(3.2, 4.2),          # stem tip distance from the base
        hoehe=r.randint(3, 4),              # stem tip height
        krone_r=r.uniform(2.5, 3.0),        # leaf cloud on the tip
    ) for i in range(n)]
    return dict(drehung=a0, staemme=staemme)


def fig_build(p, rng):
    t = Tree(rng)
    LOG, LEAF = 'acacia_wood', 'azalea_leaves'
    for q in ((0, 0, 0), (1, 0, 0), (0, 0, 1)):
        t.log(q, LOG)
    for s in p['staemme']:
        kx, kz = polar(R(s['winkel']), s['knie_weite'])
        fx, fz = polar(R(s['winkel']), s['weite'])
        tip = (fx, s['hoehe'], fz)
        t.path([(0.3, 0, 0.3), (kx, s['knie_hoehe'], kz), tip], LOG)
        t.blob((fx, s['hoehe'] + 0.6, fz), s['krone_r'], 1.7, s['krone_r'], LEAF, erode=0.25, floor=2)
        _note(t, 'ellipse', f'Krone {s["krone_r"]:.1f}', x=fx, y=s['hoehe'] + 0.6, z=fz, rx=s['krone_r'], ry=1.7)
    t.blob((0.3, 4.6, 0.3), 3.0, 1.6, 3.0, LEAF, erode=0.2, floor=3)
    _note(t, 'ellipse', 'Kappe 3.0', x=0.3, y=4.6, z=0.3, rx=3.0, ry=1.6)
    t.ground(7.5)
    return t


def fig_summary(p):
    s = p['staemme']
    return [f'{len(s)} Stämme · Spitzen {"/".join(str(q["hoehe"]) for q in s)} hoch',
            f'Weite {min(q["weite"] for q in s):.1f}–{max(q["weite"] for q in s):.1f}']


# ==================================================================================== 09 strawberry tree

def strawberry_tree_roll(r):
    """Thin stems like the branches of a vanilla acacia: each rise moves at most one block along one axis, so
    neighbouring logs always share an edge and no filler blocks thicken the bends (no knobs)."""
    n = r.randint(2, 3)
    if n == 2:
        d = r.randrange(4)
        dirs = [d, (d + 2) % 4]
    else:
        dirs = r.sample(range(4), 3)
    stamm = r.randint(2, 3)
    staemme = []
    for d in dirs:
        hoehe = r.randint(6, 8)
        steps = hoehe - stamm + 1                      # rises from the trunk top to the stem tip
        weite = r.randint(2, min(4, steps - 1))
        # the first two rises always move outwards, so the stems part at once instead of forming a block
        aussen = sorted({0, 1} | set(r.sample(range(2, steps), weite - 2)))
        frei = [k for k in range(1, steps) if k not in aussen]
        drall = r.choice([-1, 0, 1]) if frei else 0
        staemme.append(dict(
            richtung=d,                                # N/E/S/W the stem leans to
            hoehe=hoehe,                               # height of the stem tip
            weite=weite,                               # blocks it moves outwards
            aussen=aussen,                             # which rises move outwards
            drall=drall,                               # one sideways step left/right, or none
            drall_bei=r.choice(frei) if drall else None,
            ast=r.choice([-1, 1]),                     # side branch to the left or right
            ast_laenge=r.randint(1, 2),
            ast_ab=r.randint(2, 3),                    # starts this many blocks below the tip
            krone_r=r.uniform(2.0, 2.6),
            ast_krone_r=r.uniform(1.6, 2.0),
        ))
    return dict(stamm=stamm, staemme=staemme)


def strawberry_tree_build(p, rng):
    t = Tree(rng)
    LOG, LEAF = 'stripped_acacia_log', 'mangrove_leaves'
    st = p['stamm']
    for y in range(st):
        t.log((0, y, 0), LOG)
    _note(t, 'vbar', f'Stamm {st}', y0=0, y1=st - 1)
    for i, s in enumerate(p['staemme']):
        dx, dz = SIDE4[s['richtung']]
        px, pz = SIDE4[(s['richtung'] + 1) % 4]
        x, y, z = 0, st - 1, 0
        pts = []
        for k in range(s['hoehe'] - st + 1):
            y += 1
            if k in s['aussen']:
                x, z = x + dx, z + dz
            elif k == s['drall_bei']:
                x, z = x + px * s['drall'], z + pz * s['drall']
                if i == 0 and dz == 0:
                    _note(t, 'dot', 'Drall', x=x, y=y)
            t.log((x, y, z), LOG)
            pts.append((x, y, z))
        bx, by, bz = pts[-s['ast_ab']]
        for _ in range(s['ast_laenge']):
            bx, by, bz = bx + px * s['ast'], by + 1, bz + pz * s['ast']
            t.log((bx, by, bz), LOG)
        t.blob((x, y + 0.9, z), s['krone_r'], 1.4, s['krone_r'], LEAF, erode=0.35, floor=y)
        t.blob((bx, by + 0.8, bz), s['ast_krone_r'], 1.2, s['ast_krone_r'], LEAF, erode=0.35, floor=by)
        _note(t, 'ellipse', f'Krone {s["krone_r"]:.1f}', x=x, y=y + 0.9, z=z, rx=s['krone_r'], ry=1.4)
    t.ground(6)
    return t


def strawberry_tree_summary(p):
    s = p['staemme']
    drall = sum(1 for q in s if q['drall'])
    return [f'{len(s)} Stämme · Höhe {"/".join(str(q["hoehe"]) for q in s)} · Stamm {p["stamm"]}',
            f'Weite {"/".join(str(q["weite"]) for q in s)} · {drall}× Drall']


# ==================================================================================== 10 Cretan date palm

def date_palm_roll(r):
    n = r.randint(2, 3)
    hoehen = [r.randint(9, 11), r.randint(6, 7), r.randint(4, 5)][:n]
    return dict(
        drehung=r.uniform(0, 360),
        hoehen=hoehen,                                       # main trunk, second, third
        haengend=[r.random() < 0.7 for _ in range(4)],       # long fronds that get a hanging tip
        datteln=r.sample(range(4), 2),                       # sides of the main crown with cocoa
    )


def date_palm_build(p, rng):
    t = Tree(rng)
    LOG, LEAF = 'jungle_log', 'jungle_leaves'
    bases = [(0, 0, 0), (1, 0, 0), (0, 0, 1)]
    n = len(p['hoehen'])
    for i, h in enumerate(p['hoehen']):
        lx, lz = polar(R(p['drehung'] + i * 360 / n), (0.25 if i == 0 else 0.6) * h)
        bx, _, bz = bases[i]
        trunk = [(bx, 0, bz), (bx + lx * 0.2, h * 0.5, bz + lz * 0.2), (bx + lx, h, bz + lz)]
        t.path(trunk, LOG, 'y')
        top = ip(trunk[-1])
        _palm_crown(t, top, LOG, LEAF, p['haengend'])
        _note(t, 'vbar', f'Stamm {i + 1}: {h}', y0=0, y1=h - 1)
        if i == 0:
            for side in p['datteln']:
                dx, dz = CARDINALS[side]
                t.put((top[0] + dx, top[1], top[2] + dz), 'cocoa')
            _note(t, 'dot', 'Datteln', x=top[0] + 1, y=top[1])
    t.ground(6, top='sand', patches=(('grass_block', 0.25),))
    return t


def _palm_crown(t, top, log, leaf, hanging):
    """Hidden core log one above the trunk top, a leaf cap, four long arching fronds and four short
    diagonal ones. Frond tips sit at leaf distance 6, the most vanilla decay allows."""
    x, y, z = top
    c = y + 1
    t.log((x, c, z), log)
    t.leaf((x, c + 1, z), leaf)
    for dx, dz in CARDINALS:
        t.leaf((x + dx, c, z + dz), leaf)
    for k, (dx, dz) in enumerate(CARDINALS):
        pts = [(x + dx * i, c + dy, z + dz * i) for i, dy in ((1, 1), (2, 1), (3, 0), (4, -1))]
        if hanging[k]:
            pts.append((x + dx * 4, c - 2, z + dz * 4))
        for a, b in zip(pts, pts[1:]):
            t.leaf_line(a, b, leaf)
    for dx in (-1, 1):
        for dz in (-1, 1):
            t.leaf((x + dx, c, z + dz), leaf)
            t.leaf((x + dx, c + 1, z + dz), leaf)
            t.leaf((x + 2 * dx, c, z + 2 * dz), leaf)
            t.leaf((x + 2 * dx, c, z + dz), leaf)
            t.leaf((x + 2 * dx, c - 1, z + 2 * dz), leaf)


def date_palm_summary(p):
    return [f'{len(p["hoehen"])} Stämme · Höhe {"/".join(map(str, p["hoehen"]))}',
            f'{sum(p["haengend"])} von 4 Wedeln hängen']


# ==================================================================================== registry

PICKED = ['cypress', 'olive', 'fig', 'strawberry_tree', 'date_palm']


def roll(key, rng):
    return globals()[key + '_roll'](rng)


def grow(key, seed, **override):
    """One growth: roll every value with the seed, pin the overrides, build, then the shared finishing pass."""
    rng = random.Random(seed)
    p = roll(key, rng)
    p.update(override)
    t = globals()[key + '_build'](p, rng).finish()
    t.params = p
    return t


def summary(key, p):
    return globals()[key + '_summary'](p)


# Plain generator functions so make_sheet.py and preview.py keep working.
def _plain(key):
    return lambda seed: grow(key, seed)


for _k in PICKED:
    globals()[_k] = _plain(_k)
