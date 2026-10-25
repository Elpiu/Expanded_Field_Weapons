"""Find icon blobs (column runs with opaque pixels) in a horizontal strip."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dds_tool import read_dds, write_png


def find_blobs(px, w, h, gap=3):
    cols = [any(px[y][x][3] > 20 for y in range(h)) for x in range(w)]
    blobs, start, empty = [], None, 0
    for x, c in enumerate(cols + [False] * (gap + 1)):
        if c:
            if start is None:
                start = x
            empty = 0
        elif start is not None:
            empty += 1
            if empty > gap:
                blobs.append((start, x - empty))
                start, empty = None, 0
    return blobs


if __name__ == '__main__':
    w, h, px = read_dds(sys.argv[1])
    blobs = find_blobs(px, w, h)
    for i, (a, b) in enumerate(blobs):
        print(i, a, b, b - a + 1)
    if len(sys.argv) > 3:
        idx = [int(x) for x in sys.argv[3].split(',')]
        rows = []
        for y in range(h):
            row = []
            for i in idx:
                a, b = blobs[i]
                row += px[y][a:b + 1] + [(255, 0, 255, 255)] * 2
            rows.append(row)
        write_png(sys.argv[2], len(rows[0]), h, rows, 3)
