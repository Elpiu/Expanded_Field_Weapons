"""Minimal DDS reader (DXT1/DXT5/uncompressed 32bit) and RGBA DDS/PNG writer."""
import struct
import sys
import zlib


def _c565(c):
    return ((c >> 11) & 31) * 255 // 31, ((c >> 5) & 63) * 255 // 63, (c & 31) * 255 // 31


def read_dds(path):
    b = open(path, 'rb').read()
    assert b[:4] == b'DDS '
    h, w = struct.unpack('<II', b[12:20])
    pf_flags, fourcc, bits, rm, gm, bm, am = struct.unpack('<I4sIIIII', b[80:108])
    data = b[128:]
    px = [[(0, 0, 0, 0)] * w for _ in range(h)]
    if fourcc in (b'DXT5', b'DXT1'):
        bs = 16 if fourcc == b'DXT5' else 8
        i = 0
        for by in range(0, h, 4):
            for bx in range(0, w, 4):
                blk = data[i:i + bs]
                i += bs
                if fourcc == b'DXT5':
                    a0, a1 = blk[0], blk[1]
                    abits = int.from_bytes(blk[2:8], 'little')
                    al = [a0, a1]
                    if a0 > a1:
                        al += [((6 - k) * a0 + (k - 1) * a1) // 7 for k in range(2, 8)]
                    else:
                        al += [((4 - k) * a0 + (k - 1) * a1) // 5 for k in range(2, 6)] + [0, 255]
                    cb = blk[8:16]
                else:
                    cb = blk
                c0, c1, cbits = struct.unpack('<HHI', cb)
                p0, p1 = _c565(c0), _c565(c1)
                if c0 > c1 or fourcc == b'DXT5':
                    cols = [p0, p1, tuple((2 * x + y) // 3 for x, y in zip(p0, p1)),
                            tuple((x + 2 * y) // 3 for x, y in zip(p0, p1))]
                else:
                    cols = [p0, p1, tuple((x + y) // 2 for x, y in zip(p0, p1)), (0, 0, 0)]
                for k in range(16):
                    x, y = bx + k % 4, by + k // 4
                    if x >= w or y >= h:
                        continue
                    r, g, bl = cols[(cbits >> (2 * k)) & 3]
                    if fourcc == b'DXT5':
                        a = al[(abits >> (3 * k)) & 7]
                    else:
                        a = 0 if (c0 <= c1 and ((cbits >> (2 * k)) & 3) == 3) else 255
                    px[y][x] = (r, g, bl, a)
    else:
        assert bits == 32, (fourcc, bits)

        def ch(v, m):
            if not m:
                return 255
            s = (m & -m).bit_length() - 1
            return (v & m) >> s
        for y in range(h):
            for x in range(w):
                v = struct.unpack_from('<I', data, (y * w + x) * 4)[0]
                px[y][x] = (ch(v, rm), ch(v, gm), ch(v, bm), ch(v, am) if pf_flags & 1 else 255)
    return w, h, px


def write_dds(path, w, h, px):
    """Uncompressed A8R8G8B8, same format as vanilla division icons."""
    hdr = struct.pack('<4sIIIIIII', b'DDS ', 124, 0x1 | 0x2 | 0x4 | 0x1000 | 0x8, h, w, w * 4, 0, 1)
    hdr += b'\0' * 44
    hdr += struct.pack('<II4sIIIII', 32, 0x41, b'\0\0\0\0', 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
    hdr += struct.pack('<IIIII', 0x1000, 0, 0, 0, 0)
    body = bytearray()
    for row in px:
        for r, g, b, a in row:
            body += bytes((b, g, r, a))
    open(path, 'wb').write(hdr + bytes(body))


def write_png(path, w, h, px, scale=1):
    raw = bytearray()
    for row in px:
        for _ in range(scale):
            raw.append(0)
            for p in row:
                raw += bytes(p) * scale
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w * scale, h * scale, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b'')
    open(path, 'wb').write(png)


def bbox(px, x0, x1):
    xs, ys = [], []
    for y, row in enumerate(px):
        for x in range(x0, x1):
            if row[x][3] > 16:
                xs.append(x)
                ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'png':
        w, h, px = read_dds(sys.argv[2])
        write_png(sys.argv[3], w, h, px, int(sys.argv[4]) if len(sys.argv) > 4 else 1)
        print(sys.argv[2], w, h, 'frame bboxes:', bbox(px, 0, w // 2), bbox(px, w // 2, w))
