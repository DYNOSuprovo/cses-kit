#!/usr/bin/env python3
"""Fetch a CSES problem page and emit a Markdown statement + sample tests.

Usage:
    fetch.py <cses-task-url> <problem-dir>

Writes:
    <problem-dir>/statement.md
    <problem-dir>/tests/1.in , 1.out , 2.in , 2.out , ...

Stdlib only (plus curl) — nothing to install.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cses_lib import fetch_problem


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: fetch.py <cses-task-url> <problem-dir>", file=sys.stderr)
        return 2
    url, out_dir = sys.argv[1], sys.argv[2]
    try:
        title, n = fetch_problem(url, out_dir)
    except Exception as e:  # noqa: BLE001
        print(f"error: could not fetch {url}: {e}", file=sys.stderr)
        return 1
    if n:
        print(f"fetched: {title}  ({n} sample test(s))")
    else:
        print(f"fetched: {title}  (no sample tests found — left tests/ as-is or empty 1.in/1.out)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
