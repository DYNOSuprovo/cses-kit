"""ACCEPTED banner. Imported by submit; preview with `cses celebrate`."""
from __future__ import annotations

import os
import random
import shutil
import sys
import time

_HIDE_CUR = "\033[?25l"
_SHOW_CUR = "\033[?25h"
_RST = "\033[0m"
_GREEN = "\033[32m"
_BOLD = "\033[1m"
_CONFETTI = list("*+.:x%o#")
_POPS = ["🎉", "🎊", "✨"]
_CONFETTI_COLORS = ("\033[33m", "\033[93m", "\033[35m", "\033[36m", "\033[91m", "\033[32m")
_BANNER = [
    r"  █████╗  ██████╗ ██████╗███████╗██████╗ ████████╗███████╗██████╗ ",
    r" ██╔══██╗██╔════╝██╔════╝██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗",
    r" ███████║██║     ██║     █████╗  ██████╔╝   ██║   █████╗  ██║  ██║",
    r" ██╔══██║██║     ██║     ██╔══╝  ██╔═══╝    ██║   ██╔══╝  ██║  ██║",
    r" ██║  ██║╚██████╗╚██████╗███████╗██║        ██║   ███████╗██████╔╝",
    r" ╚═╝  ╚═╝ ╚═════╝ ╚═════╝╚══════╝╚═╝        ╚═╝   ╚══════╝╚═════╝",
]


def _cols() -> int:
    try:
        return shutil.get_terminal_size().columns
    except OSError:
        return 80


def static_accept(title: str, extra: str) -> None:
    print()
    print(f"{_GREEN}{_BOLD}  ACCEPTED{extra}{_RST}")
    print(f"{_GREEN}  {(title or 'Problem')} is done.{_RST}")
    print()


def animate_accept(title: str, extra: str) -> None:
    rng = random.Random()
    cols = max(40, min(_cols(), 72))
    wide = cols >= 68
    banner = _BANNER if wide else ["  ***  A C C E P T E D  ***", "      *  *  *  *  *  *"]
    top, bot = 2, 2
    height = top + len(banner) + bot
    bits = [
        {
            "x": rng.uniform(0, cols - 2),
            "y": rng.uniform(0, height - 1),
            "vy": rng.uniform(0.25, 0.7),
            "ch": rng.choice(_CONFETTI),
            "color": rng.choice(_CONFETTI_COLORS),
        }
        for _ in range(22 if wide else 14)
    ]
    subtitle = f"  🎉  {(title or 'Problem')}{extra}  🎉"
    out = sys.stdout
    out.write(_HIDE_CUR)
    out.flush()
    try:
        for f in range(22):
            grid = [[" "] * cols for _ in range(height)]
            color_at: dict[tuple[int, int], str] = {}
            pop = _POPS[f % len(_POPS)]
            corners = f"{pop}{' ' * max(0, cols - 4)}{pop}"
            for b in bits:
                b["y"] = (b["y"] + b["vy"]) % height
                b["x"] = (b["x"] + rng.uniform(-0.4, 0.4)) % (cols - 1)
                xi, yi = int(b["x"]), int(b["y"])
                if grid[yi][xi] == " ":
                    grid[yi][xi] = b["ch"]
                    color_at[(yi, xi)] = b["color"]
            for i, line in enumerate(banner):
                row = top + i
                start = max(0, (cols - len(line)) // 2)
                for j, ch in enumerate(line):
                    x = start + j
                    if 0 <= x < cols:
                        grid[row][x] = ch
                        color_at[(row, x)] = _GREEN + _BOLD
            if f:
                out.write(f"\033[{height + 1}A")
            out.write("\033[2K" + corners + "\n")
            for y in range(1, height):
                row = grid[y]
                out.write("\033[2K")
                prev = ""
                for x, ch in enumerate(row):
                    c = color_at.get((y, x), "")
                    if c != prev:
                        out.write(_RST + c)
                        prev = c
                    out.write(ch)
                out.write(_RST + "\n")
            out.write("\033[2K" + _GREEN + subtitle[:cols] + _RST + "\n")
            out.flush()
            time.sleep(0.055)
    finally:
        out.write(_SHOW_CUR)
        out.flush()
    print()


def play(title: str, score: str = "") -> None:
    extra = f" ({score})" if score else ""
    if not sys.stdout.isatty() or os.environ.get("CSES_NO_ANIM"):
        static_accept(title, extra)
        return
    print()
    try:
        animate_accept(title, extra)
    except (KeyboardInterrupt, OSError):
        sys.stdout.write(_SHOW_CUR)
        sys.stdout.flush()
        static_accept(title, extra)
