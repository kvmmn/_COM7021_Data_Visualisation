#!/usr/bin/env python3
"""Render aesth palette poster, Anscombe charts, and a Great Tables proof.

    PYTHONPATH=src python studies/render_proofs.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OUT = Path(__file__).resolve().parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))

from aesth.fonts import resolve_sans  # noqa: E402
from aesth.palettes import PALETTES, get_palette  # noqa: E402
from aesth.theme import scale_colour_aesth, theme_aesth  # noqa: E402


ROLE_ORDER = [
    "ink",
    "accent",
    "accent_deep",
    "ink_soft",
    "support",
    "mist",
    "paper",
    "white",
    "mute",
    "grid",
    "line",
]


def render_poster() -> list[Path]:
    """Hand SVG + rsvg-convert. Matplotlib path-converts Aptos and doubles glyphs."""
    import shutil
    import subprocess

    family, note = resolve_sans()
    print(f"typeface: {note} (poster via rsvg-convert)")
    width, height = 1480, 1960
    margin = 48
    row_h = 214
    header = 118
    sw_w, sw_h = 78, 46
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        f"text {{ font-family: '{family}', 'IBM Plex Sans', sans-serif; font-feature-settings: 'liga' 0, 'calt' 0; }}",
        ".title { font-size: 28px; font-weight: 700; fill: #151515; }",
        ".lede { font-size: 13px; font-weight: 400; fill: #989898; }",
        ".name { font-size: 16px; font-weight: 700; }",
        ".meta { font-size: 11px; font-weight: 400; }",
        ".role { font-size: 10px; font-weight: 600; }",
        ".hex { font-size: 9px; font-weight: 400; }",
        ".chip { font-size: 10px; font-weight: 700; fill: #FFFFFF; }",
        "</style>",
        '<rect width="100%" height="100%" fill="#F1F0EB"/>',
        '<text class="title" x="48" y="52">æsth palettes</text>',
        '<text class="lede" x="48" y="78">Frozen token rows. Accent last in series. Brand chrome is not a data hue.</text>',
    ]
    for i, name in enumerate(PALETTES):
        palette = PALETTES[name]
        y = header + i * row_h
        parts.append(
            f'<rect x="{margin}" y="{y}" width="{width - 2 * margin}" height="{row_h - 16}" '
            f'rx="14" fill="{palette.paper}" stroke="{palette.line}" stroke-width="1.5"/>'
        )
        parts.append(
            f'<text class="name" x="{margin + 20}" y="{y + 28}" fill="{palette.ink}">{name}</text>'
        )
        parts.append(
            f'<rect x="{margin + 118}" y="{y + 12}" width="52" height="20" rx="10" fill="{palette.chip_fill}"/>'
        )
        parts.append(
            f'<text class="chip" x="{margin + 144}" y="{y + 26}" text-anchor="middle">chip</text>'
        )
        parts.append(
            f'<text class="meta" x="{width - margin - 20}" y="{y + 26}" text-anchor="end" fill="{palette.mute}">series</text>'
        )
        for j, hex_value in enumerate(palette.series):
            sx = width - margin - 20 - (5 - j) * 36
            parts.append(f'<rect x="{sx}" y="{y + 12}" width="32" height="18" fill="{hex_value}"/>')
        for j, role in enumerate(ROLE_ORDER):
            x = margin + 20 + j * (sw_w + 10)
            hex_value = getattr(palette, role)
            parts.append(
                f'<rect x="{x}" y="{y + 52}" width="{sw_w}" height="{sw_h}" fill="{hex_value}" '
                f'stroke="{palette.line}" stroke-width="0.75"/>'
            )
            parts.append(
                f'<text class="role" x="{x + sw_w / 2}" y="{y + 118}" text-anchor="middle" fill="{palette.ink}">{role}</text>'
            )
            parts.append(
                f'<text class="hex" x="{x + sw_w / 2}" y="{y + 134}" text-anchor="middle" fill="{palette.mute}">{hex_value}</text>'
            )
    parts.append("</svg>")
    svg = OUT / "palette_poster.svg"
    png = OUT / "palette_poster.png"
    svg.write_text("\n".join(parts), encoding="utf-8")
    converter = shutil.which("rsvg-convert")
    if converter is None:
        raise RuntimeError("rsvg-convert is required to rasterise the palette poster")
    subprocess.run(
        [converter, "-d", "220", "-p", "220", "-o", str(png), str(svg)],
        check=True,
    )
    return [png, svg]


def _anscombe_frame():
    try:
        from plotnine.data import anscombe_quartet

        return anscombe_quartet
    except Exception:
        pass
    try:
        import pandas as pd

        from plotnine.data import anscombe

        return anscombe
    except Exception:
        import pandas as pd

        rows = []
        sets = {
            "I": [
                (10, 8.04),
                (8, 6.95),
                (13, 7.58),
                (9, 8.81),
                (11, 8.33),
                (14, 9.96),
                (6, 7.24),
                (4, 4.26),
                (12, 10.84),
                (7, 4.82),
                (5, 5.68),
            ],
            "II": [
                (10, 9.14),
                (8, 8.14),
                (13, 8.74),
                (9, 8.77),
                (11, 9.26),
                (14, 8.10),
                (6, 6.13),
                (4, 3.10),
                (12, 9.13),
                (7, 7.26),
                (5, 4.74),
            ],
            "III": [
                (10, 7.46),
                (8, 6.77),
                (13, 12.74),
                (9, 7.11),
                (11, 7.81),
                (14, 8.84),
                (6, 6.08),
                (4, 5.39),
                (12, 8.15),
                (7, 6.42),
                (5, 5.73),
            ],
            "IV": [
                (8, 6.58),
                (8, 5.76),
                (8, 7.71),
                (8, 8.84),
                (8, 8.47),
                (8, 7.04),
                (8, 5.25),
                (19, 12.50),
                (8, 5.56),
                (8, 7.91),
                (8, 6.89),
            ],
        }
        for name, pairs in sets.items():
            for x, y in pairs:
                rows.append({"dataset": name, "x": x, "y": y})
        return pd.DataFrame(rows)


def _dataset_col(frame) -> str:
    for candidate in ("dataset", "group", "set"):
        if candidate in frame.columns:
            return candidate
    raise KeyError(f"no dataset column in {list(frame.columns)}")


def render_anscombe(names: tuple[str, ...] = ("arden", "carbon", "cinnabar")) -> list[Path]:
    from plotnine import aes, facet_wrap, geom_point, geom_smooth, ggplot, labs, theme

    frame = _anscombe_frame()
    facet = _dataset_col(frame)
    written: list[Path] = []
    for name in names:
        tokens = get_palette(name)
        plot = (
            ggplot(frame, aes("x", "y"))
            + geom_point(color=tokens.accent, size=2.8, stroke=0)
            + geom_smooth(method="lm", se=False, color=tokens.ink, size=1.05)
            + facet_wrap(facet, ncol=2)
            + labs(title="Anscombe's quartet", x="x", y="y")
            + theme_aesth(name, figure_size=(10.5, 7.2))
            + theme(legend_position="none")
        )
        path = OUT / f"anscombe_{name}.png"
        plot.save(str(path), dpi=220, verbose=False, limitsize=False)
        written.append(path)
        # Touch scale constructors so they stay import-tested.
        _ = scale_colour_aesth(name)
    return written


def render_table() -> list[Path]:
    import pandas as pd

    from aesth.tables import GT_aesth, highlight_column

    frame = pd.DataFrame(
        {
            "city": ["Leeds", "Bristol", "Glasgow", "Cardiff", "Belfast"],
            "index": [112, 101, 97, 88, 79],
            "share": [0.24, 0.21, 0.20, 0.18, 0.17],
        }
    )
    table = GT_aesth(frame, "arden", stripe=True)
    table = table.tab_header(
        title="Regional index",
        subtitle="Toy frame for the arden table theme",
    )
    table = highlight_column(table, "index", "arden")
    html_path = OUT / "arden_table.html"
    html_path.write_text(table.as_raw_html(), encoding="utf-8")
    written = [html_path]
    png_path = OUT / "arden_table.png"
    try:
        saver = getattr(table, "gtsave", None) or table.save
        saver(str(png_path))
        written.append(png_path)
    except Exception as exc:
        print(f"GT PNG export skipped: {exc}")
    return written


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    written.extend(render_poster())
    written.extend(render_anscombe())
    written.extend(render_table())
    print("wrote:")
    for path in written:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
