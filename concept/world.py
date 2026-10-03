"""Minimal Anvil reader: enough to pull block states out of a 1.18+ world without extra packages.

    for (x, y, z), name, props in blocks_in_region(path, wanted={'minecraft:azalea_leaves'}): ...
"""
import io
import math
import os
import struct
import zlib


# ---------------------------------------------------------------- NBT

def _read(f, t):
    if t == 1:
        return struct.unpack('>b', f.read(1))[0]
    if t == 2:
        return struct.unpack('>h', f.read(2))[0]
    if t == 3:
        return struct.unpack('>i', f.read(4))[0]
    if t == 4:
        return struct.unpack('>q', f.read(8))[0]
    if t == 5:
        return struct.unpack('>f', f.read(4))[0]
    if t == 6:
        return struct.unpack('>d', f.read(8))[0]
    if t == 7:
        n = struct.unpack('>i', f.read(4))[0]
        return f.read(n)
    if t == 8:
        n = struct.unpack('>H', f.read(2))[0]
        return f.read(n).decode('utf-8', 'replace')
    if t == 9:
        et = f.read(1)[0]
        n = struct.unpack('>i', f.read(4))[0]
        return [_read(f, et) for _ in range(n)]
    if t == 10:
        out = {}
        while True:
            tt = f.read(1)[0]
            if tt == 0:
                return out
            n = struct.unpack('>H', f.read(2))[0]
            name = f.read(n).decode('utf-8', 'replace')
            out[name] = _read(f, tt)
    if t == 11:
        n = struct.unpack('>i', f.read(4))[0]
        return struct.unpack(f'>{n}i', f.read(4 * n))
    if t == 12:
        n = struct.unpack('>i', f.read(4))[0]
        return struct.unpack(f'>{n}q', f.read(8 * n))
    raise ValueError(f'bad tag {t}')


def nbt(data):
    f = io.BytesIO(data)
    t = f.read(1)[0]
    n = struct.unpack('>H', f.read(2))[0]
    f.read(n)
    return _read(f, t)


# ---------------------------------------------------------------- region

def chunks(path):
    """Yield (chunk_x, chunk_z, nbt) for every chunk stored in a region file."""
    with open(path, 'rb') as fh:
        data = fh.read()
    for i in range(1024):
        off = int.from_bytes(data[i * 4:i * 4 + 3], 'big')
        if off == 0:
            continue
        pos = off * 4096
        length = struct.unpack('>i', data[pos:pos + 4])[0]
        comp = data[pos + 4]
        raw = data[pos + 5:pos + 4 + length]
        if comp == 2:
            raw = zlib.decompress(raw)
        elif comp == 1:
            import gzip
            raw = gzip.decompress(raw)
        elif comp != 3:
            continue  # LZ4 or external chunk, not needed here
        tag = nbt(raw)
        yield tag.get('xPos'), tag.get('zPos'), tag


def _indices(longs, bits, count=4096):
    per = 64 // bits
    mask = (1 << bits) - 1
    out = []
    for v in longs:
        v &= 0xFFFFFFFFFFFFFFFF
        for k in range(per):
            out.append((v >> (k * bits)) & mask)
            if len(out) == count:
                return out
    return out


def blocks_in_region(path, wanted, area=None):
    """Yield ((x, y, z), name, props) for blocks whose name is in wanted.
    area=(x0, z0, x1, z1) skips chunks outside that block rectangle."""
    for cx, cz, tag in chunks(path):
        if area and not (area[0] - 16 < cx * 16 <= area[2] and area[1] - 16 < cz * 16 <= area[3]):
            continue
        for sec in tag.get('sections', []):
            bs = sec.get('block_states')
            if not bs:
                continue
            pal = bs['palette']
            hits = [i for i, p in enumerate(pal) if p['Name'] in wanted]
            if not hits:
                continue
            sy = sec['Y']
            if len(pal) == 1:
                idx = [0] * 4096
            else:
                bits = max(4, math.ceil(math.log2(len(pal))))
                idx = _indices(bs['data'], bits)
            hit = set(hits)
            for n, k in enumerate(idx):
                if k in hit:
                    x = n & 15
                    z = (n >> 4) & 15
                    y = n >> 8
                    p = pal[k]
                    yield (cx * 16 + x, sy * 16 + y, cz * 16 + z), p['Name'], p.get('Properties', {})


def region_file(world, x, z):
    return os.path.join(world, 'dimensions', 'minecraft', 'overworld', 'region', f'r.{x >> 9}.{z >> 9}.mca')
