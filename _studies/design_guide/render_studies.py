#!/usr/bin/env python3
"""COM7021 design-guide studies — short labels only, locked Arden palette."""

from __future__ import annotations

import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

MIDNIGHT = "#002B49"
TIFFANY = "#66C9BA"
TIFFANY_DEEP = "#3AA89A"
MIDNIGHT_SOFT = "#1A4A6B"
TEAL = "#0E7C8B"
MIST = "#E6F5F2"
PAPER = "#F7FAFB"
MUTE = "#5A6B75"
LINE = "#C9D5DD"
WHITE = "#FFFFFF"


def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render(svg_text: str, stem: str, width: int = 1500) -> Path:
    svg_path = OUT / f"{stem}.svg"
    png_path = OUT / f"{stem}.png"
    svg_path.write_text(svg_text)
    subprocess.run(
        ["rsvg-convert", "-w", str(width), "-o", str(png_path), str(svg_path)],
        check=True,
    )
    print("Wrote", png_path.name)
    return png_path


def defs() -> str:
    return f"""
  <defs>
    <filter id="shadow" x="-6%" y="-6%" width="118%" height="118%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.4"
                    flood-color="{MIDNIGHT}" flood-opacity="0.10"/>
    </filter>
    <marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6 Z" fill="{MUTE}"/>
    </marker>
    <marker id="arrowT" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6 Z" fill="{TIFFANY_DEEP}"/>
    </marker>
    <style>
      .lab {{ font: 600 14px Aptos, sans-serif; fill: {MIDNIGHT}; }}
      .labw {{ font: 600 13px Aptos, sans-serif; fill: {WHITE}; }}
      .small {{ font: 400 11px Aptos, sans-serif; fill: {MUTE}; }}
      .tiny {{ font: 400 10px Aptos, sans-serif; fill: {MUTE}; }}
      .chip {{ font: 700 10px Aptos, sans-serif; fill: {WHITE}; }}
      .zone {{ font: 700 12px Aptos, sans-serif; fill: {MIDNIGHT}; }}
      .num {{ font: 700 12px Aptos, sans-serif; fill: {WHITE}; }}
    </style>
  </defs>
"""


def box(x, y, w, h, label, fill=WHITE, stroke=LINE, sub=None, sw=1.5):
    sub_svg = ""
    if sub:
        if isinstance(sub, str):
            sub = [sub]
        sub_svg = "".join(
            f'<text x="{x + w/2}" y="{y + h/2 + 8 + i*14}" text-anchor="middle" class="tiny">{esc(s)}</text>'
            for i, s in enumerate(sub)
        )
    ty = y + h / 2 + (4 if not sub else -8)
    return f"""
    <g filter="url(#shadow)">
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"
            fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>
      <text x="{x + w/2}" y="{ty}" text-anchor="middle" class="lab">{esc(label)}</text>
      {sub_svg}
    </g>"""


def pill(x, y, w, h, label, fill=MIDNIGHT):
    return f"""
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}"/>
    <text x="{x + w/2}" y="{y + h/2 + 4}" text-anchor="middle" class="chip">{esc(label)}</text>"""


def step(cx, cy, n):
    return f"""
    <circle cx="{cx}" cy="{cy}" r="16" fill="{MIDNIGHT}"/>
    <text x="{cx}" y="{cy + 5}" text-anchor="middle" class="num">{esc(n)}</text>"""


def arrow(x1, y1, x2, y2, tiffany=False):
    m = "url(#arrowT)" if tiffany else "url(#arrow)"
    c = TIFFANY_DEEP if tiffany else MUTE
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{c}" stroke-width="2" marker-end="{m}"/>'
    )


def lane(x, y, w, h, title):
    return f"""
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18"
          fill="{MIST}" stroke="{LINE}" stroke-width="1"/>
    <text x="{x + 16}" y="{y + 22}" class="zone">{esc(title)}</text>"""


def study_01_pipeline() -> str:
    """Linear ML pipeline: one emphasised path, short noun labels."""
    parts = [
        step(110, 70, "01"),
        step(310, 70, "02"),
        step(510, 70, "03"),
        step(710, 70, "04"),
        step(910, 70, "05"),
        box(40, 100, 140, 78, "Raw data", sub=["CSV / API"]),
        box(240, 100, 140, 78, "Clean", sub=["validate"]),
        box(440, 100, 140, 78, "Features", sub=["encode / scale"], fill=MIST, stroke=TIFFANY, sw=2),
        box(640, 100, 140, 78, "Model", sub=["train / select"]),
        box(840, 100, 140, 78, "Evaluate", sub=["hold-out"], fill=MIST, stroke=MIDNIGHT, sw=1.5),
        arrow(180, 139, 240, 139),
        arrow(380, 139, 440, 139),
        arrow(580, 139, 640, 139, tiffany=True),
        arrow(780, 139, 840, 139, tiffany=True),
        # quiet footer chips
        pill(320, 220, 110, 24, "batch", MIDNIGHT),
        pill(450, 220, 130, 24, "supervised", TIFFANY_DEEP),
        pill(600, 220, 120, 24, "reportable", MIDNIGHT_SOFT),
    ]
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1020" height="280" viewBox="0 0 1020 280">
  <rect width="1020" height="280" fill="{PAPER}"/>
  {defs()}
  {"".join(parts)}
</svg>"""


def study_02_data_zones() -> str:
    """Lake zones as swimlanes — mist lanes, cards on top, one claim path."""
    parts = [
        lane(40, 40, 940, 100, "Landing"),
        lane(40, 160, 940, 100, "Curated"),
        lane(40, 280, 940, 100, "Serving"),
        box(70, 70, 160, 52, "Ingest", sub=["immutable"]),
        box(280, 70, 160, 52, "Staging", sub=["raw files"]),
        box(490, 70, 160, 52, "Quarantine", sub=["failed rows"]),
        box(70, 190, 180, 52, "Clean tables", sub=["typed"], fill=MIST, stroke=TIFFANY, sw=2),
        box(300, 190, 180, 52, "Feature store", sub=["versioned"], fill=MIST, stroke=TIFFANY, sw=2),
        box(530, 190, 160, 52, "Quality", sub=["checks"]),
        box(70, 310, 180, 52, "Dashboard", sub=["aggregates"]),
        box(300, 310, 180, 52, "API layer", sub=["read models"], fill=MIST, stroke=MIDNIGHT),
        box(530, 310, 160, 52, "Export", sub=["CSV / Parquet"]),
        arrow(230, 96, 280, 96),
        arrow(440, 96, 490, 96),
        arrow(150, 122, 150, 190, tiffany=True),
        arrow(250, 216, 300, 216, tiffany=True),
        arrow(390, 242, 390, 310, tiffany=True),
        # governance footer
        f'<rect x="40" y="410" width="940" height="44" rx="14" fill="{MIDNIGHT}"/>',
        pill(70, 420, 120, 24, "lineage", TIFFANY_DEEP),
        pill(210, 420, 140, 24, "access control", MIDNIGHT_SOFT),
        pill(370, 420, 110, 24, "audit", TIFFANY_DEEP),
        pill(500, 420, 150, 24, "retention rules", MIDNIGHT_SOFT),
    ]
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1020" height="480" viewBox="0 0 1020 480">
  <rect width="1020" height="480" fill="{PAPER}"/>
  {defs()}
  {"".join(parts)}
</svg>"""


def study_03_kpi_strip() -> str:
    """KPI strip — one tiffany highlight, short captions, no essay text."""
    cards = [
        (40, "Rows", "128k", "cleaned", False),
        (230, "Features", "24", "selected", False),
        (420, "MAE", "3.1%", "hold-out", True),
        (610, "Peak hour", "17:00", "UTC", False),
        (800, "Coverage", "98%", "valid rows", False),
    ]
    parts = []
    for x, title, value, cap, hi in cards:
        fill = MIST if hi else WHITE
        stroke = TIFFANY if hi else LINE
        sw = 2 if hi else 1.5
        parts.append(f"""
        <g filter="url(#shadow)">
          <rect x="{x}" y="50" width="170" height="110" rx="14"
                fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>
          <text x="{x + 85}" y="80" text-anchor="middle" class="small">{esc(title)}</text>
          <text x="{x + 85}" y="118" text-anchor="middle"
                style="font:700 28px Aptos, sans-serif; fill:{MIDNIGHT};">{esc(value)}</text>
          <text x="{x + 85}" y="142" text-anchor="middle" class="tiny">{esc(cap)}</text>
        </g>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="210" viewBox="0 0 1040 210">
  <rect width="1040" height="210" fill="{PAPER}"/>
  {defs()}
  {"".join(parts)}
</svg>"""


def study_04_role_matrix() -> str:
    """Who sees what — matrix with one recommended column."""
    headers = [
        (160, "Analyst", False),
        (360, "Manager", True),
        (560, "Engineer", False),
        (760, "Auditor", False),
    ]
    rows = [
        (100, "Trend chart", ["read", "read", "build", "—"]),
        (170, "Exception strip", ["read", "act", "build", "read"]),
        (240, "Feature table", ["explore", "—", "own", "sample"]),
        (310, "Lineage log", ["—", "—", "own", "review"]),
    ]
    parts = [
        f'<rect x="40" y="40" width="940" height="340" rx="18" fill="{MIST}" stroke="{LINE}"/>',
        # stub column for row labels
        f'<rect x="50" y="55" width="90" height="36" rx="10" fill="{MIDNIGHT}"/>',
        f'<text x="95" y="78" text-anchor="middle" class="labw">View</text>',
    ]
    for x, label, hi in headers:
        fill = TIFFANY_DEEP if hi else MIDNIGHT
        parts.append(f'<rect x="{x}" y="55" width="180" height="36" rx="10" fill="{fill}"/>')
        parts.append(
            f'<text x="{x + 90}" y="78" text-anchor="middle" class="labw">{esc(label)}</text>'
        )
    for y, label, cells in rows:
        parts.append(
            f'<text x="95" y="{y + 28}" text-anchor="middle" class="lab">{esc(label)}</text>'
        )
        for i, cell in enumerate(cells):
            x = 160 + i * 200
            hi = i == 1
            fill = WHITE
            stroke = TIFFANY if hi else LINE
            sw = 2 if hi else 1.5
            parts.append(f"""
            <g filter="url(#shadow)">
              <rect x="{x}" y="{y}" width="180" height="52" rx="8"
                    fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>
              <text x="{x + 90}" y="{y + 32}" text-anchor="middle" class="small">{esc(cell)}</text>
            </g>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1020" height="420" viewBox="0 0 1020 420">
  <rect width="1020" height="420" fill="{PAPER}"/>
  {defs()}
  {"".join(parts)}
</svg>"""


def main() -> None:
    render(study_01_pipeline(), "study_01_ml_pipeline", width=1500)
    render(study_02_data_zones(), "study_02_data_zones", width=1600)
    render(study_03_kpi_strip(), "study_03_kpi_strip", width=1600)
    render(study_04_role_matrix(), "study_04_role_matrix", width=1600)


if __name__ == "__main__":
    main()
