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


def fig00_workflow_roadmap() -> str:
    """Recipe 6.6 & Custom: End-to-End Assignment R&D Workflow & Execution Roadmap.
    Shows 6 sequential stages, detailed deliverables, and completed vs remaining milestones.
    """
    stages = [
        {
            "num": "01",
            "title": "Data Hygiene",
            "subtitle": "Ingestion & Audit",
            "bullets": ["5,000 rows x 18 cols", "Excel serial to ISO", "Zero missing/anomalies"],
            "status": "COMPLETED",
            "status_color": MIDNIGHT,
            "hi": False,
            "dashed": False,
        },
        {
            "num": "02",
            "title": "First Principles",
            "subtitle": "Feature Engineering",
            "bullets": ["Net margin & recovery", "Rate / 10k pax metrics", "OLS cost decomposition"],
            "status": "COMPLETED",
            "status_color": MIDNIGHT,
            "hi": False,
            "dashed": False,
        },
        {
            "num": "03",
            "title": "Visualisation Suite",
            "subtitle": "7 Advanced Figures",
            "bullets": ["Raincloud & Dumbbell", "Joint OLS + KDE strips", "220 DPI Arden palette"],
            "status": "COMPLETED",
            "status_color": MIDNIGHT,
            "hi": False,
            "dashed": False,
        },
        {
            "num": "04",
            "title": "Interactive Dash",
            "subtitle": "Decision Engine",
            "bullets": ["Plotly 6-slicer engine", "6 real-time KPI tiles", "Scenario stress testing"],
            "status": "COMPLETED",
            "status_color": MIDNIGHT,
            "hi": False,
            "dashed": False,
        },
        {
            "num": "05",
            "title": "Critical Synthesis",
            "subtitle": "Rubric Alignment",
            "bullets": ["Task 1 (~680w explanation)", "Task 2 (~980w report)", "LO1–LO4 & Harvard refs"],
            "status": "IN REVIEW",
            "status_color": TIFFANY_DEEP,
            "hi": True,
            "dashed": False,
        },
        {
            "num": "06",
            "title": "Final Submission",
            "subtitle": "Packaging & Word",
            "bullets": ["Incorporate tutor notes", "Format official .docx", "Band 90–100 rubric check"],
            "status": "PENDING",
            "status_color": MUTE,
            "hi": False,
            "dashed": True,
        },
    ]

    parts = []
    # Header title inside diagram
    parts.append(
        f'<text x="40" y="30" class="lab" style="font-size:16px; font-weight:700; fill:{MIDNIGHT};">'
        f'COM7021 ASSESSMENT R&amp;D WORKFLOW &amp; EXECUTION ROADMAP'
        f'</text>'
    )
    parts.append(
        f'<text x="40" y="48" class="small" style="fill:{MUTE};">'
        f'Progress Tracker: 85% Completed (Stages 01–05 active/built) · Next: Stage 06 Final Word Packaging post-feedback'
        f'</text>'
    )

    y_top = 66
    card_w = 158
    card_h = 210

    for i, s in enumerate(stages):
        x = 24 + i * 178
        fill = MIST if s["hi"] else WHITE
        stroke = TIFFANY_DEEP if s["hi"] else (LINE if not s["dashed"] else "#98AAB5")
        sw = "2.5" if s["hi"] else ("1.5" if not s["dashed"] else "1.5")
        dash_attr = 'stroke-dasharray="4,3"' if s["dashed"] else ""

        # Connecting arrow to next stage
        if i < len(stages) - 1:
            arr_x1 = x + card_w + 3
            arr_x2 = arr_x1 + 14
            arr_y = y_top + card_h / 2
            is_arr_tiffany = (i >= 3)
            parts.append(arrow(arr_x1, arr_y, arr_x2, arr_y, tiffany=is_arr_tiffany))

        # Card container
        parts.append(f"""
        <g filter="url(#shadow)">
          <rect x="{x}" y="{y_top}" width="{card_w}" height="{card_h}" rx="12"
                fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {dash_attr}/>
          <!-- Step circle -->
          <circle cx="{x + 26}" cy="{y_top + 26}" r="15" fill="{s['status_color']}"/>
          <text x="{x + 26}" y="{y_top + 31}" text-anchor="middle" class="num" style="font-size:11px;">{s['num']}</text>
          <!-- Stage badge -->
          <rect x="{x + 48}" y="{y_top + 15}" width="{card_w - 56}" height="22" rx="11" fill="{s['status_color']}"/>
          <text x="{x + 48 + (card_w - 56)/2}" y="{y_top + 29}" text-anchor="middle" class="chip" style="font-size:9.5px; font-weight:700;">{s['status']}</text>
          <!-- Title & Subtitle -->
          <text x="{x + 14}" y="{y_top + 62}" class="lab" style="font-size:12.5px; font-weight:700; fill:{MIDNIGHT};">{esc(s['title'])}</text>
          <text x="{x + 14}" y="{y_top + 78}" class="tiny" style="font-size:10px; font-weight:600; fill:{TEAL if s['hi'] else MUTE};">{esc(s['subtitle'])}</text>
          <line x1="{x + 14}" y1="{y_top + 87}" x2="{x + card_w - 14}" y2="{y_top + 87}" stroke="{LINE}" stroke-width="1"/>
          <!-- Bullets -->
          <circle cx="{x + 18}" cy="{y_top + 106}" r="2.5" fill="{TIFFANY_DEEP if s['hi'] else MUTE}"/>
          <text x="{x + 26}" y="{y_top + 110}" class="tiny" style="font-size:9.5px; fill:{MIDNIGHT};">{esc(s['bullets'][0])}</text>
          <circle cx="{x + 18}" cy="{y_top + 128}" r="2.5" fill="{TIFFANY_DEEP if s['hi'] else MUTE}"/>
          <text x="{x + 26}" y="{y_top + 132}" class="tiny" style="font-size:9.5px; fill:{MIDNIGHT};">{esc(s['bullets'][1])}</text>
          <circle cx="{x + 18}" cy="{y_top + 150}" r="2.5" fill="{TIFFANY_DEEP if s['hi'] else MUTE}"/>
          <text x="{x + 26}" y="{y_top + 154}" class="tiny" style="font-size:9.5px; fill:{MIDNIGHT};">{esc(s['bullets'][2])}</text>
          <!-- Footer micro-label -->
          <rect x="{x + 12}" y="{y_top + 172}" width="{card_w - 24}" height="26" rx="6" fill="{WHITE if s['hi'] else PAPER}" stroke="{LINE}" stroke-width="1"/>
          <text x="{x + card_w / 2}" y="{y_top + 189}" text-anchor="middle" class="tiny" style="font-size:9px; font-weight:600; fill:{MIDNIGHT};">
            {'Active Focus' if s['hi'] else ('Next Step' if s['dashed'] else 'Verified Artifact')}
          </text>
        </g>""")

    # Bottom Progress Bar Strip
    bar_y = 296
    parts.append(f"""
    <g filter="url(#shadow)">
      <rect x="24" y="{bar_y}" width="1072" height="46" rx="10" fill="{WHITE}" stroke="{LINE}" stroke-width="1.5"/>
      <!-- Track -->
      <rect x="40" y="{bar_y + 16}" width="420" height="14" rx="7" fill="{MIST}"/>
      <!-- Fill 85% -->
      <rect x="40" y="{bar_y + 16}" width="357" height="14" rx="7" fill="{TIFFANY}"/>
      <!-- 85% text -->
      <text x="495" y="{bar_y + 27}" text-anchor="middle" class="chip" style="fill:{MIDNIGHT}; font-weight:700; font-size:10px;">85% Done</text>
      <!-- Milestone text -->
      <text x="545" y="{bar_y + 28}" class="small" style="font-weight:700; fill:{MIDNIGHT}; font-size:11.5px;">
        Milestone: <tspan fill="{TIFFANY_DEEP}">Tutor Review Draft Online</tspan> · <tspan fill="{MUTE}">Next: Feedback &amp; Word Docx</tspan>
      </text>
    </g>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="360" viewBox="0 0 1120 360">
  <rect width="1120" height="360" fill="{PAPER}"/>
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

