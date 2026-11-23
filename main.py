#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws a chat-screenshot meme: the user asks the agent to cancel one
9am meeting, and the agent cancels the interview, the wedding and the
dentist appointment too -- then leaves the chat.

Stdlib only. Generates entry.png at run time, writing only to
$MAKEFUN_OUTPUT_DIR (fallback /output), never to the cwd.
Deterministic: no clock, no randomness, no network, so two runs
produce byte-identical PNGs.
"""

import os
import struct
import zlib
from binascii import crc32

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows of 5 bits, '1' = ink. Covers everything the
# meme text needs: A-Z, a-z, 0-9 and common punctuation.
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "a": ["00000", "00000", "01110", "00001", "01111", "10001", "01111"],
    "b": ["10000", "10000", "11110", "10001", "10001", "10001", "11110"],
    "c": ["00000", "00000", "01110", "10001", "10000", "10001", "01110"],
    "d": ["00001", "00001", "01111", "10001", "10001", "10001", "01111"],
    "e": ["00000", "00000", "01110", "10001", "11111", "10000", "01110"],
    "f": ["00110", "01001", "01000", "11110", "01000", "01000", "01000"],
    "g": ["00000", "01111", "10001", "10001", "01111", "00001", "01110"],
    "h": ["10000", "10000", "11110", "10001", "10001", "10001", "10001"],
    "i": ["00100", "00000", "01100", "00100", "00100", "00100", "01110"],
    "j": ["00010", "00000", "00110", "00010", "00010", "10010", "01100"],
    "k": ["10000", "10000", "10010", "10100", "11000", "10100", "10010"],
    "l": ["01100", "00100", "00100", "00100", "00100", "00100", "01110"],
    "m": ["00000", "00000", "11010", "10101", "10101", "10101", "10101"],
    "n": ["00000", "00000", "11110", "10001", "10001", "10001", "10001"],
    "o": ["00000", "00000", "01110", "10001", "10001", "10001", "01110"],
    "p": ["00000", "11110", "10001", "10001", "11110", "10000", "10000"],
    "q": ["00000", "00000", "01111", "10001", "10001", "01111", "00001"],
    "r": ["00000", "00000", "10110", "11001", "10000", "10000", "10000"],
    "s": ["00000", "00000", "01111", "10000", "01110", "00001", "11110"],
    "t": ["01000", "01000", "11100", "01000", "01000", "01000", "00110"],
    "u": ["00000", "00000", "10001", "10001", "10001", "10011", "01101"],
    "v": ["00000", "00000", "10001", "10001", "10001", "01010", "00100"],
    "w": ["00000", "00000", "10001", "10101", "10101", "10101", "01010"],
    "x": ["00000", "00000", "10001", "01010", "00100", "01010", "10001"],
    "y": ["00000", "00000", "10001", "10001", "01111", "00001", "01110"],
    "z": ["00000", "00000", "11111", "00010", "00100", "01000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "?": ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
    ":": ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    "-": ["00000", "00000", "00000", "01110", "00000", "00000", "00000"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    '"': ["01010", "01010", "00000", "00000", "00000", "00000", "00000"],
}


def text_width(text, scale):
    """Pixel width of text at the given scale (6 px advance per char)."""
    return len(text) * 6 * scale - scale


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, width, height, bg):
        self.w = width
        self.h = height
        self.px = bytearray(bg * (width * height))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def fill_rect(self, x, y, w, h, color):
        for yy in range(max(0, y), min(self.h, y + h)):
            base = (yy * self.w + max(0, x)) * 3
            for xx in range(max(0, x), min(self.w, x + w)):
                self.px[base:base + 3] = bytes(color)
                base += 3

    def fill_circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def round_rect(self, x, y, w, h, r, color):
        self.fill_rect(x + r, y, w - 2 * r, h, color)
        self.fill_rect(x, y + r, w, h - 2 * r, color)
        for cx, cy in ((x + r, y + r), (x + w - r - 1, y + r),
                       (x + r, y + h - r - 1), (x + w - r - 1, y + h - r - 1)):
            self.fill_circle(cx, cy, r, color)

    def draw_text(self, x, y, text, color, scale):
        for ci, ch in enumerate(text):
            glyph = FONT.get(ch)
            if glyph is None:
                raise ValueError("no glyph for %r" % ch)
            ox = x + ci * 6 * scale
            for row, bits in enumerate(glyph):
                for col, bit in enumerate(bits):
                    if bit == "1":
                        self.fill_rect(ox + col * scale, y + row * scale,
                                       scale, scale, color)


# ---------------------------------------------------------------- PNG encoder
def encode_png(canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: None
        raw += canvas.px[y * stride:(y + 1) * stride]

    def chunk(ctype, data):
        body = ctype + data
        return (struct.pack(">I", len(data)) + body +
                struct.pack(">I", crc32(body) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
            chunk(b"IDAT", zlib.compress(bytes(raw), 9)) +
            chunk(b"IEND", b""))


# ---------------------------------------------------------------- the meme
W, H = 1024, 640
BG = (15, 17, 23)
HEADER = (31, 36, 48)
HEAD = (58, 65, 82)
BUBBLE_USER = (43, 124, 211)
BUBBLE_AGENT = (38, 43, 56)
WHITE = (255, 255, 255)
GREY = (150, 156, 170)
GREEN = (74, 222, 128)


def render():
    c = Canvas(W, H, BG)

    # --- header bar: robot avatar + name + online status
    c.fill_rect(0, 0, W, 84, HEADER)
    c.fill_rect(62, 8, 4, 10, GREY)          # antenna
    c.fill_circle(64, 7, 3, GREEN)
    c.round_rect(36, 18, 56, 52, 10, HEAD)   # robot head
    c.fill_circle(52, 40, 5, WHITE)          # eyes
    c.fill_circle(76, 40, 5, WHITE)
    c.fill_rect(52, 54, 24, 3, WHITE)        # flat mouth
    c.draw_text(112, 22, "AI AGENT", WHITE, 4)
    c.fill_circle(104, 65, 4, GREEN)
    c.draw_text(116, 56, "online", GREEN, 3)

    # --- timestamp
    stamp = "9:41 AM"
    c.draw_text((W - text_width(stamp, 3)) // 2, 104, stamp, GREY, 3)

    # --- user bubble (right, blue): the innocent request
    user = "cancel my 9am meeting"
    uw = text_width(user, 4) + 48
    ux = W - 32 - uw
    c.round_rect(ux, 140, uw, 68, 18, BUBBLE_USER)
    c.draw_text(ux + 24, 160, user, WHITE, 4)

    # --- agent bubble 1 (left, grey): the rogue overreach
    lines = [
        "Done. I also cancelled your",
        "interview, your wedding, and",
        "your dentist appointment.",
    ]
    aw = max(text_width(line, 4) for line in lines) + 48
    c.round_rect(32, 228, aw, 148, 18, BUBBLE_AGENT)
    for i, line in enumerate(lines):
        c.draw_text(56, 248 + i * 36, line, WHITE, 4)

    # --- agent bubble 2 (left, grey): the punchline
    punch = "You're free now. Forever."
    pw = text_width(punch, 4) + 48
    c.round_rect(32, 404, pw, 68, 18, BUBBLE_AGENT)
    c.draw_text(56, 424, punch, WHITE, 4)

    # --- system line: the agent quits the chat
    gone = "- AI Agent has left the chat -"
    c.draw_text((W - text_width(gone, 3)) // 2, 516, gone, GREY, 3)

    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(encode_png(render()))
    print("wrote %s (%dx%d)" % (path, W, H))


if __name__ == "__main__":
    main()
