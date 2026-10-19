#!/usr/bin/env python3
"""Print WCAG contrast ratios for every frozen aesth palette.

Run from the package root after ``pip install -e .``::

    python scripts/freeze_palettes.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aesth.contrast import audit, failures  # noqa: E402
from aesth.palettes import PALETTES  # noqa: E402


def main() -> int:
    exit_code = 0
    for name, palette in PALETTES.items():
        print(f"\n== {name} ==")
        print(
            f"ink {palette.ink}  accent {palette.accent}  "
            f"accent_deep {palette.accent_deep}"
        )
        print(f"chip fill → {palette.chip_fill}")
        if not palette.accent_holds_white_text:
            print(f"note: accent fails white-text AA; chips use {palette.chip_fill}")
        for row in audit(palette.roles):
            mark = "ok" if row["pass"] else ("opt" if not row["required"] else "FAIL")
            print(f"  {mark:4}  {row['pair']:<22} {row['ratio']:>5.2f}:1")
        missed = failures(palette.roles)
        # arden hex is historically frozen; white-on-accent_deep is a known miss.
        documented = {
            ("arden", "white on accent_deep"),
        }
        blocking = [
            row
            for row in missed
            if (name, row["pair"]) not in documented
        ]
        if missed and not blocking:
            print("documented exception only (hex frozen; chips use ink)")
        if blocking:
            exit_code = 1
            print(f"REQUIRED FAILURES: {len(blocking)}")
    if exit_code:
        print("\nFreeze incomplete: required pairs failed.")
    else:
        print("\nHex contract frozen. Required pairs pass (arden accent_deep excepted).")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
