#!/usr/bin/env python3
"""Step 3: Generate Structural & KPI Diagrams (SVG + PNG via rsvg-convert).
Strictly follows COM7021 - Assignment/VISUAL_DESIGN_GUIDE.md and _studies/design_guide/render_studies.py.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUT = BASE_DIR / "output" / "figures"
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


def _fontconfig_env() -> dict[str, str]:
    import os
    env = dict(os.environ)
    cache_dir = Path("/tmp/rsvg_fontconfig_cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    conf_path = Path("/tmp/rsvg_fonts.conf")
    if not conf_path.exists():
        conf_path.write_text(
            f"""<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <dir>/System/Library/Fonts</dir>
  <dir>/System/Library/Fonts/Supplemental</dir>
  <dir>/Library/Fonts</dir>
  <cachedir>{cache_dir}</cachedir>
</fontconfig>
""",
            encoding="utf-8",
        )
    env["FONTCONFIG_FILE"] = str(conf_path)
    env["XDG_CACHE_HOME"] = str(cache_dir)
    env["PANGOCAIRO_BACKEND"] = "fc"
    return env


def render(svg_text: str, stem: str, width: int = 1600) -> Path:
    svg_path = OUT / f"{stem}.svg"
    png_path = OUT / f"{stem}.png"
    svg_path.write_text(svg_text, encoding="utf-8")
    subprocess.run(
        ["rsvg-convert", "-w", str(width), "-o", str(png_path), str(svg_path)],
        check=True,
        env=_fontconfig_env(),
    )
    print(f"Rendered SVG + PNG: {png_path.name}")
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
      .lab {{ font: 600 14px Aptos, 'Helvetica Neue', sans-serif; fill: {MIDNIGHT}; }}
      .labw {{ font: 600 13px Aptos, 'Helvetica Neue', sans-serif; fill: {WHITE}; }}
      .small {{ font: 400 11px Aptos, 'Helvetica Neue', sans-serif; fill: {MUTE}; }}
      .tiny {{ font: 400 10px Aptos, 'Helvetica Neue', sans-serif; fill: {MUTE}; }}
      .chip {{ font: 700 10px Aptos, 'Helvetica Neue', sans-serif; fill: {WHITE}; }}
      .zone {{ font: 700 12px Aptos, 'Helvetica Neue', sans-serif; fill: {MIDNIGHT}; }}
      .num {{ font: 700 12px Aptos, 'Helvetica Neue', sans-serif; fill: {WHITE}; }}
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


def fig00_executive_kpi_strip() -> str:
    """Recipe 6.6 KPI strip: 6 tiles across 1040 px canvas."""
    cards = [
        (32, "Passengers", "40.91M", "12 EU cities", False),
        (196, "On-time rate", "82.1%", "mean service", False),
        (360, "Mean delay", "4.35m", "Bus: 6.58m", True),
        (524, "Cost recovery", "99.6%", "Bike: 5.2%", True),
        (688, "CO2 saved", "4,482t", "Metro: 70.3%", False),
        (852, "Satisfaction", "4.01", "1 to 5 scale", False),
    ]
    parts = []
    for x, title, value, cap, hi in cards:
        fill = MIST if hi else WHITE
        stroke = TIFFANY if hi else LINE
        sw = 2.0 if hi else 1.5
        parts.append(
            f"""
        <g filter="url(#shadow)">
          <rect x="{x}" y="35" width="152" height="112" rx="14"
                fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>
          <text x="{x + 76}" y="63" text-anchor="middle" class="small">{esc(title)}</text>
          <text x="{x + 76}" y="101" text-anchor="middle"
                style="font:700 25px Aptos, 'Helvetica Neue', sans-serif; fill:{MIDNIGHT};">{esc(value)}</text>
          <text x="{x + 76}" y="126" text-anchor="middle" class="tiny">{esc(cap)}</text>
        </g>"""
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="182" viewBox="0 0 1040 182">
  <rect width="1040" height="182" fill="{PAPER}"/>
  {defs()}
  {"".join(parts)}
</svg>"""


def fig08_methodology_pipeline() -> str:
    """Recipe 6.6 Numbered procedure: 5-stage Python data visualisation workflow."""
    parts = [
        step(110, 58, "01"),
        step(310, 58, "02"),
        step(510, 58, "03"),
        step(710, 58, "04"),
        step(910, 58, "05"),
        box(40, 86, 140, 82, "Ingest xlsx", sub=["5,000 rows", "18 columns"]),
        box(240, 86, 140, 82, "Type hygiene", sub=["serial Date", "ISO 2024–25"]),
        box(
            440,
            86,
            140,
            82,
            "Derived ratios",
            sub=["cost recovery", "rate / 10k pax"],
            fill=MIST,
            stroke=TIFFANY,
            sw=2.0,
        ),
        box(640, 86, 140, 82, "Seven charts", sub=["matplotlib", "220 dpi PNG"]),
        box(
            840,
            86,
            140,
            82,
            "Dashboard",
            sub=["multi-filter", "decision view"],
            fill=MIST,
            stroke=MIDNIGHT,
            sw=1.5,
        ),
        arrow(184, 127, 236, 127),
        arrow(384, 127, 436, 127, tiffany=True),
        arrow(584, 127, 636, 127, tiffany=True),
        arrow(784, 127, 836, 127, tiffany=True),
        pill(260, 196, 130, 24, "pandas 3.0", MIDNIGHT),
        pill(410, 196, 160, 24, "normalised metrics", TIFFANY_DEEP),
        pill(590, 196, 150, 24, "Arden palette", MIDNIGHT_SOFT),
    ]
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1020" height="248" viewBox="0 0 1020 248">
  <rect width="1020" height="248" fill="{PAPER}"/>
  {defs()}
  {"".join(parts)}
</svg>"""


def fig09_mode_performance_matrix() -> str:
    """Recipe 6.6 Comparison matrix: 6 transport modes across 5 core KPIs."""
    headers = [
        (175, "Metro", True),
        (315, "Tram", False),
        (455, "Park & Ride", False),
        (595, "Bus", False),
        (735, "Bike Share", False),
        (875, "E-Scooter", False),
    ]
    rows = [
        (100, "Demand share", ["63.0%", "15.6%", "8.0%", "12.4%", "0.7%", "0.4%"]),
        (164, "Mean delay", ["3.73 min", "4.79 min", "5.17 min", "6.58 min", "1.62 min", "1.94 min"]),
        (228, "Cost recovery", ["106.2%", "117.3%", "121.5%", "100.1%", "5.2%", "7.4%"]),
        (292, "CO2 / kWh", ["2.19 kg", "1.66 kg", "1.72 kg", "1.07 kg", "0 kWh", "7.21 kg"]),
        (356, "Complaints/10k", ["14.85", "15.08", "15.87", "17.46", "17.00", "18.36"]),
    ]
    parts = [
        f'<rect x="30" y="34" width="990" height="404" rx="18" fill="{MIST}" stroke="{LINE}"/>',
        f'<rect x="44" y="50" width="118" height="36" rx="10" fill="{MIDNIGHT}"/>',
        f'<text x="103" y="73" text-anchor="middle" class="labw">Dimension</text>',
    ]
    for x, label, hi in headers:
        fill = TIFFANY_DEEP if hi else MIDNIGHT
        parts.append(f'<rect x="{x}" y="50" width="128" height="36" rx="10" fill="{fill}"/>')
        parts.append(f'<text x="{x + 64}" y="73" text-anchor="middle" class="labw">{esc(label)}</text>')

    for y, label, cells in rows:
        parts.append(f'<text x="103" y="{y + 30}" text-anchor="middle" class="lab">{esc(label)}</text>')
        for i, cell in enumerate(cells):
            x = 175 + i * 140
            hi = i == 0
            stroke = TIFFANY if hi else LINE
            sw = 2.0 if hi else 1.5
            parts.append(
                f"""
            <g filter="url(#shadow)">
              <rect x="{x}" y="{y}" width="128" height="48" rx="8"
                    fill="{WHITE}" stroke="{stroke}" stroke-width="{sw}"/>
              <text x="{x + 64}" y="{y + 29}" text-anchor="middle" class="small">{esc(cell)}</text>
            </g>"""
            )
    parts.append(pill(184, 410, 110, 22, "Core backbone", TIFFANY_DEEP))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="464" viewBox="0 0 1050 464">
  <rect width="1050" height="464" fill="{PAPER}"/>
  {defs()}
  {"".join(parts)}
</svg>"""


def curved_arrow(
    d: str, tiffany: bool = True, dashed: bool = True, label: str = "", lx: float = 0, ly: float = 0
) -> str:
    c = TIFFANY_DEEP if tiffany else MUTE
    dash = 'stroke-dasharray="4,3"' if dashed else ""
    m = "url(#arrowT)" if tiffany else "url(#arrow)"
    label_svg = ""
    if label:
        label_svg = (
            f'<text x="{lx}" y="{ly}" text-anchor="middle" class="tiny" '
            f'style="font-size:9.5px; font-weight:600; fill:{c}; font-style:italic;">{esc(label)}</text>'
        )
    return (
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.8" {dash} '
        f'marker-end="{m}"/>{label_svg}'
    )


def fig00_workflow_roadmap() -> str:
    """Minimal, symbolic R&D network topology.
    Clean, lightweight visual showing high-level project status and iterative feedback loops.
    """
    nodes = [
        # Top row: Forward discovery
        {"id": "01", "name": "Ingestion & Hygiene", "sub": "Verified 5k Clean Dataset", "status": "Done ✓", "x": 40, "y": 55, "w": 260, "h": 50, "hi": False, "dashed": False},
        {"id": "02", "name": "Feature Engineering", "sub": "Unit Economics & Ratios", "status": "Done ✓", "x": 350, "y": 55, "w": 260, "h": 50, "hi": False, "dashed": False},
        {"id": "03", "name": "Visual Analytics", "sub": "7 Distributional Figures", "status": "Done ✓", "x": 660, "y": 55, "w": 260, "h": 50, "hi": False, "dashed": False},
        # Bottom row: Interactive & Synthesis
        {"id": "06", "name": "Formative Review & Word", "sub": "Tutor Feedback & Final .docx", "status": "Pending", "x": 40, "y": 145, "w": 260, "h": 50, "hi": False, "dashed": True},
        {"id": "05", "name": "Academic Synthesis", "sub": "Task 1 & 2 Critical Report", "status": "In Review", "x": 350, "y": 145, "w": 260, "h": 50, "hi": True, "dashed": False},
        {"id": "04", "name": "Decision Dashboard", "sub": "Multi-Filter Scenario App", "status": "Done ✓", "x": 660, "y": 145, "w": 260, "h": 50, "hi": False, "dashed": False},
    ]

    parts = []
    # Minimal top banner title
    parts.append(
        f'<text x="40" y="20" class="lab" style="font-size:12px; font-weight:700; fill:{MIDNIGHT}; letter-spacing:0.3px;">'
        f'PROJECT WORKFLOW &amp; WORKING TOPOLOGY · <tspan font-weight="400" fill="{MUTE};">Iterative research with recursive feedback loops</tspan>'
        f'</text>'
    )

    # 1. Forward flow arrows
    parts.append(arrow(300, 80, 345, 80))
    parts.append(arrow(610, 80, 655, 80, tiffany=True))
    parts.append(arrow(790, 105, 790, 140))
    parts.append(arrow(660, 170, 615, 170, tiffany=True))
    parts.append(arrow(350, 170, 305, 170))

    # 2. Subtle, minimal dashed feedback loops
    # Loop 02 -> 01
    parts.append(
        curved_arrow("M 380 55 C 340 32, 290 32, 240 52", tiffany=True, dashed=True,
                     label="anomaly audit", lx=310, ly=34)
    )
    # Loop 03 -> 02
    parts.append(
        curved_arrow("M 690 55 C 650 32, 600 32, 550 52", tiffany=True, dashed=True,
                     label="Simpson's loop", lx=620, ly=34)
    )
    # Loop 04 -> 03 (right)
    parts.append(
        curved_arrow("M 920 160 C 948 138, 948 108, 920 88", tiffany=True, dashed=True,
                     label="stress-test", lx=946, ly=125)
    )
    # Loop 05 <-> 02 (center vertical)
    parts.append(
        curved_arrow("M 465 142 L 465 109", tiffany=True, dashed=True,
                     label="model feedback", lx=425, ly=127)
    )
    # Loop 06 -> 05 (bottom)
    parts.append(
        curved_arrow("M 260 195 C 300 215, 350 215, 390 195", tiffany=True, dashed=True,
                     label="tutor review loop", lx=325, ly=214)
    )

    # 3. Draw clean, minimal symbolic node pills
    for n in nodes:
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        fill = MIST if n["hi"] else WHITE
        stroke = TIFFANY_DEEP if n["hi"] else (LINE if not n["dashed"] else "#98AAB5")
        sw = "2" if n["hi"] else ("1.2" if not n["dashed"] else "1.2")
        dash_attr = 'stroke-dasharray="3,3"' if n["dashed"] else ""
        badge_bg = TIFFANY_DEEP if n["hi"] else (MIDNIGHT if not n["dashed"] else MUTE)

        parts.append(f"""
        <g filter="url(#shadow)">
          <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"
                fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {dash_attr}/>
          <!-- Circle number -->
          <circle cx="{x + 22}" cy="{y + h/2}" r="12" fill="{badge_bg}"/>
          <text x="{x + 22}" y="{y + h/2 + 4}" text-anchor="middle" class="num" style="font-size:10px;">{n['id']}</text>
          <!-- Title & Sub -->
          <text x="{x + 42}" y="{y + 22}" class="lab" style="font-size:11.5px; font-weight:700; fill:{MIDNIGHT};">{esc(n['name'])}</text>
          <text x="{x + 42}" y="{y + 36}" class="tiny" style="font-size:9px; fill:{MUTE};">{esc(n['sub'])}</text>
          <!-- Status pill -->
          <rect x="{x + w - 62}" y="{y + 16}" width="54" height="18" rx="9" fill="{WHITE if n['hi'] else PAPER}" stroke="{stroke}" stroke-width="1"/>
          <text x="{x + w - 35}" y="{y + 28}" text-anchor="middle" class="tiny" style="font-size:8.5px; font-weight:700; fill:{TIFFANY_DEEP if n['hi'] else (MIDNIGHT if not n['dashed'] else MUTE)};">
            {esc(n['status'])}
          </text>
        </g>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="970" height="235" viewBox="0 0 970 235">
  <rect width="970" height="235" fill="{PAPER}"/>
  {defs()}
  {"".join(parts)}
</svg>"""


def main() -> None:
    render(fig00_executive_kpi_strip(), "fig00_executive_kpi_strip", width=1600)
    render(fig00_workflow_roadmap(), "fig00_workflow_roadmap", width=1600)
    render(fig08_methodology_pipeline(), "fig08_methodology_pipeline", width=1600)
    render(fig09_mode_performance_matrix(), "fig09_mode_performance_matrix", width=1600)


if __name__ == "__main__":
    main()

