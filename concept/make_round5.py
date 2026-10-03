"""Concept sheets of the Aries oak, fifth shape (round5.py):

- round5_design.png: the build next to three growths of the design, each seen whole, cut open through the trunk
  and from the side
- round5_variations.png: the design and its five variations (one feature pushed in each), whole and cut open

cd concept && python make_round5.py [design|variations]
"""
import sys

from PIL import Image, ImageDraw

import round5
import voxel
from make_round4 import original
from make_sheet import F_LABEL, F_TEXT, F_TITLE, GREY, INK, PAPER, sky

SEEDS = (1, 2, 3)


def cut(v):
    """Cut open through the middle of the trunk at every height (the trunk sways, a flat cut would miss it)."""
    trunk_z = {}
    for (x, y, z), (b, _) in v.items():
        if b in ('dark_oak_wood', 'dark_oak_log') and abs(x - 1.5) <= 9 and abs(z - 1.5) <= 9:
            trunk_z.setdefault(y, []).append(z)
    mid = {y: sorted(zs)[len(zs) // 2] for y, zs in trunk_z.items()}
    last = 1
    cut_at = {}
    for y in range(min(p[1] for p in v), max(p[1] for p in v) + 1):
        last = mid.get(y, last)
        cut_at[y] = last
    return {p: b for p, b in v.items() if p[2] <= cut_at[p[1]]}


def steve(v):
    return max(p[0] for p in v) + 1, 0


def scaled(im, f):
    return im.resize((int(im.width * f), int(im.height * f)), Image.LANCZOS)


def sheet(cols, title, sub, out):
    """cols: [(label, [image per row])], drawn as a grid of columns, each row bottom aligned."""
    cw = max(im.width for _, ims in cols for im in ims) + 20
    nrows = len(cols[0][1])
    rows = [max(ims[k].height for _, ims in cols) for k in range(nrows)]
    W = cw * len(cols) + 40
    H = 130 + sum(rows) + nrows * 40
    img = Image.new('RGBA', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((24, 14), title, font=F_TITLE, fill=INK)
    d.text((26, 60), sub, font=F_TEXT, fill=GREY)
    panel = sky(W - 40, H - 120)
    pd = ImageDraw.Draw(panel)
    y = 0
    for k in range(nrows):
        for i, (label, ims) in enumerate(cols):
            im = ims[k]
            panel.alpha_composite(im, (i * cw + (cw - im.width) // 2, y + rows[k] - im.height))
            if k == 0:
                pd.text((i * cw + 10, y + 4), label, font=F_LABEL, fill=INK)
        y += rows[k] + 40
    img.alpha_composite(panel, (20, 110))
    img.save(out)
    print(out, img.size)


def design():
    cols = [('Original (Stadt, 1:1)', original())]
    for s in SEEDS:
        cols.append((f'Entwurf, Wuchs {s}', round5.giant(s).v))
    rendered = []
    for label, v in cols:
        rendered.append((label, [scaled(voxel.render(v, steve=steve(v), margin=10), 0.5),
                                 scaled(voxel.render(cut(v), margin=10), 0.5),
                                 voxel.render_side(v, s=6, steve=steve(v), margin=8)]))
    sheet(rendered, 'Widdereiche (Aries Oak), fünfte Form: der Bau eines Mitspielers und drei Wüchse des Entwurfs',
          'oben ganz, Mitte aufgeschnitten durch den Stamm, unten von der Seite; die Ranken sind als Würfel '
          'gezeichnet, im Spiel hängen sie flach an der Seite', 'round5_design.png')


def variations():
    cells = []
    for key, name, what, over in round5.VARIANTS:
        v = round5.giant(1, **over).v
        whole = scaled(voxel.render(v, steve=steve(v), margin=10), 0.42)
        inside = scaled(voxel.render(cut(v), margin=10), 0.42)
        cell = Image.new('RGBA', (whole.width + inside.width + 10, max(whole.height, inside.height) + 34))
        d = ImageDraw.Draw(cell)
        d.text((4, 0), name, font=F_LABEL, fill=INK)
        d.text((4 + d.textlength(name, font=F_LABEL) + 14, 2), what, font=F_TEXT, fill=GREY)
        cell.alpha_composite(whole, (0, cell.height - whole.height))
        cell.alpha_composite(inside, (whole.width + 10, cell.height - inside.height))
        cells.append(cell)
    per_row = 2
    rows = [cells[i:i + per_row] for i in range(0, len(cells), per_row)]
    cw = max(c.width for c in cells) + 30
    rh = [max(c.height for c in row) for row in rows]
    W = cw * per_row + 40
    H = 130 + sum(rh) + len(rows) * 40
    img = Image.new('RGBA', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.text((24, 14), 'Widdereiche, fünfte Form: der Entwurf und fünf Variationen, die je ein Merkmal betonen',
           font=F_TITLE, fill=INK)
    d.text((26, 60), 'je links ganz, rechts aufgeschnitten durch den Stamm; alle aus demselben Samen (Wuchs 1)',
           font=F_TEXT, fill=GREY)
    panel = sky(W - 40, H - 120)
    y = 20
    for row, h in zip(rows, rh):
        for i, c in enumerate(row):
            panel.alpha_composite(c, (i * cw + 10, y + h - c.height))
        y += h + 40
    img.alpha_composite(panel, (20, 110))
    img.save('round5_variations.png')
    print('round5_variations.png', img.size)


if __name__ == '__main__':
    which = sys.argv[1:] or ['design', 'variations']
    if 'design' in which:
        design()
    if 'variations' in which:
        variations()
