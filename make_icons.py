#!/usr/bin/env python3
# アイコン生成（外部ライブラリなし）。背景＋ボトル形のPNGを書き出す。
import zlib, struct

BG   = (0xFF, 0xFF, 0xFF)
ROSE = (0xD1, 0x47, 0x6C)
SOFT = (0xFD, 0xEB, 0xEF)

def rr(x, y, x0, y0, x1, y1, r):
    if x < x0 or x > x1 or y < y0 or y > y1: return False
    for cx, cy in ((x0+r, y0+r), (x1-r, y0+r), (x0+r, y1-r), (x1-r, y1-r)):
        if (x < x0+r or x > x1-r) and (y < y0+r or y > y1-r):
            if (x-cx)**2 + (y-cy)**2 > r*r: return False
    return True

def png(size, path):
    s = size / 512.0
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            u, v = x/s, y/s
            c = BG
            if rr(u, v, 32, 32, 480, 480, 120): c = SOFT
            if rr(u, v, 226, 96, 286, 168, 18): c = ROSE          # キャップ
            if rr(u, v, 184, 168, 328, 424, 56): c = ROSE         # ボトル
            if rr(u, v, 212, 236, 300, 254, 9): c = SOFT          # ラベルの線
            if rr(u, v, 212, 278, 268, 296, 9): c = SOFT
            row += bytes(c)
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)

    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
    out += chunk(b"IDAT", zlib.compress(raw, 9))
    out += chunk(b"IEND", b"")
    open(path, "wb").write(out)
    print("作成:", path)

png(192, "icon-192.png")
png(512, "icon-512.png")
