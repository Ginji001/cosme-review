#!/usr/bin/env python3
# アイコン生成（外部ライブラリなし）。背景＋ボトル形のPNGを書き出す。
import zlib, struct

BG   = (0x0F, 0x1A, 0x20)
TEAL = (0x1C, 0x6E, 0x68)
INK  = (0xE8, 0xF2, 0xF0)

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
            if rr(u, v, 40, 40, 472, 472, 96): c = TEAL
            if rr(u, v, 224, 92, 288, 170, 14): c = INK          # キャップ
            if rr(u, v, 186, 170, 326, 420, 40): c = INK         # ボトル
            if rr(u, v, 214, 232, 298, 250, 8): c = TEAL         # ラベルの線
            if rr(u, v, 214, 272, 272, 290, 8): c = TEAL
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
