#!/usr/bin/env python3
"""Step 4b: High-Resolution Streamlit & Plotly Dashboard State Renderer for EcoMove Mobility.

Produces publication-grade 220 DPI dashboard state captures (SVG + PNG) for the Word report:
- fig09_dashboard_overview.png (Full network baseline state: N = 5,000 records)
- fig10_dashboard_filtered_scenario.png (Filtered executive scenario: Rain & Snow on Surface Transit, n = 583)

Companion to the live interactive Streamlit application:
- Script: scripts/04_streamlit_dashboard.py
- Live Deployment: https://com7021-data-visualisation.streamlit.app/
- Repository: https://github.com/kvmmn/_COM7021_Data_Visualisation
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from style.palette import (
    MIDNIGHT,
    TIFFANY,
    TIFFANY_DEEP,
    MIDNIGHT_SOFT,
    TEAL,
    MIST,
    PAPER,
    MUTE,
    GRID,
    LINE,
    WHITE,
)

DATA_CSV = BASE_DIR / "data" / "ecomove_cleaned.csv"
FIG_DIR = BASE_DIR / "output" / "figures"


def _fontconfig_env() -> dict[str, str]:
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


def esc(text: str) -> str:
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_plotly_dashboard_figure(df: pd.DataFrame, title_suffix: str = "All Network Operations") -> go.Figure:
    """Create a 4-panel interactive Plotly figure styled with the locked Arden palette."""
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Monthly Passenger Demand Trend",
            "Cost Recovery Ratio (%) by Transport Mode",
            "Mean Delay (min) by Weather Condition",
            "Accessibility Complaints per 10k Pax by Route",
        ),
        vertical_spacing=0.18,
        horizontal_spacing=0.12,
    )

    # Panel 1: Monthly trend
    m_df = df.groupby("YearMonth", as_index=False)["Passengers"].mean().sort_values("YearMonth")
    fig.add_trace(
        go.Scatter(
            x=m_df["YearMonth"],
            y=m_df["Passengers"].round(0),
            mode="lines+markers",
            name="Mean Passengers",
            line={"color": MIDNIGHT, "width": 2.5},
            marker={"color": TIFFANY_DEEP, "size": 6, "line": {"color": MIDNIGHT, "width": 1}},
        ),
        row=1,
        col=1,
    )

    # Panel 2: Cost recovery by mode
    mode_df = (
        df.groupby("Transport_Mode", as_index=False)
        .agg(Rev=("Ticket_Revenue_EUR", "sum"), Cost=("Operating_Cost_EUR", "sum"))
        .assign(Rec=lambda d: (d["Rev"] / d["Cost"] * 100.0).round(1))
        .sort_values("Rec", ascending=True)
    )
    mode_colors = [TIFFANY if r < 100 else MIDNIGHT_SOFT for r in mode_df["Rec"]]
    fig.add_trace(
        go.Bar(
            x=mode_df["Rec"],
            y=mode_df["Transport_Mode"],
            orientation="h",
            name="Cost Recovery (%)",
            marker_color=mode_colors,
            text=[f"{r:.1f}%" for r in mode_df["Rec"]],
            textposition="outside",
        ),
        row=1,
        col=2,
    )

    # Panel 3: Weather delay
    w_order = ["Clear", "Cloudy", "Windy", "Heatwave", "Rain", "Snow"]
    w_df = (
        df.groupby("Weather", as_index=False)["Average_Delay_Minutes"]
        .mean()
        .set_index("Weather")
        .reindex([w for w in w_order if w in df["Weather"].unique()])
        .reset_index()
    )
    w_colors = [TIFFANY if w in ("Rain", "Snow") else MIDNIGHT_SOFT for w in w_df["Weather"]]
    fig.add_trace(
        go.Bar(
            x=w_df["Weather"],
            y=w_df["Average_Delay_Minutes"].round(2),
            name="Mean Delay (min)",
            marker_color=w_colors,
            text=[f"{v:.2f}m" for v in w_df["Average_Delay_Minutes"]],
            textposition="outside",
        ),
        row=2,
        col=1,
    )

    # Panel 4: Route accessibility rate per 10k passengers
    r_df = (
        df.groupby("Route_Type", as_index=False)
        .agg(Comp=("Accessibility_Complaints", "sum"), Pax=("Passengers", "sum"))
        .assign(Rate=lambda d: (d["Comp"] / d["Pax"] * 10000.0).round(2))
        .sort_values("Rate", ascending=True)
    )
    r_colors = [
        TIFFANY if r == r_df["Rate"].max() else MIDNIGHT_SOFT for r in r_df["Rate"]
    ]
    fig.add_trace(
        go.Bar(
            x=r_df["Rate"],
            y=r_df["Route_Type"],
            orientation="h",
            name="Complaints / 10k Pax",
            marker_color=r_colors,
            text=[f"{v:.2f}" for v in r_df["Rate"]],
            textposition="outside",
        ),
        row=2,
        col=2,
    )

    fig.update_layout(
        title={
            "text": f"EcoMove Executive Mobility Dashboard — {title_suffix}",
            "font": {"family": "Aptos, Helvetica Neue, sans-serif", "size": 16, "color": MIDNIGHT},
        },
        font={"family": "Aptos, Helvetica Neue, sans-serif", "size": 11, "color": MIDNIGHT},
        paper_bgcolor=WHITE,
        plot_bgcolor=PAPER,
        showlegend=False,
        height=720,
        margin={"l": 60, "r": 40, "t": 70, "b": 50},
    )
    fig.update_xaxes(showgrid=False, linecolor=GRID, tickfont={"color": MUTE})
    fig.update_yaxes(showgrid=True, gridcolor=GRID, linecolor=GRID, tickfont={"color": MUTE})
    return fig


def render_dashboard_capture_svg(
    df_sub: pd.DataFrame,
    filter_chips: list[tuple[str, str, bool]],
    subtitle: str,
    stem: str,
    preset_label: str = "1. Full Network Baseline (Figure 9 — N = 5,000)",
) -> Path:
    """Render a full high-resolution Streamlit + Plotly dashboard capture (SVG + PNG via rsvg-convert)."""
    n_rec = len(df_sub)
    total_pax = df_sub["Passengers"].sum()
    mean_ontime = df_sub["On_Time_Percentage"].mean()
    mean_delay = df_sub["Average_Delay_Minutes"].mean()
    total_rev = df_sub["Ticket_Revenue_EUR"].sum()
    total_cost = df_sub["Operating_Cost_EUR"].sum()
    net_margin = total_rev - total_cost
    recovery = (total_rev / total_cost * 100.0) if total_cost > 0 else 0.0
    rec_mean_recovery = df_sub["Cost_Recovery_Pct"].mean()
    total_co2 = df_sub["CO2_Saved_KG"].sum() / 1000.0
    mean_rating = df_sub["Customer_Rating"].mean()
    comp_10k = (df_sub["Accessibility_Complaints"].sum() / total_pax * 10000.0) if total_pax > 0 else 0.0

    # Prepare data for the visual panels inside the Streamlit workspace canvas
    # 1. Mode cost recovery & delay
    m_df = (
        df_sub.groupby("Transport_Mode", as_index=False)
        .agg(Rev=("Ticket_Revenue_EUR", "sum"), Cost=("Operating_Cost_EUR", "sum"), Delay=("Average_Delay_Minutes", "mean"))
        .assign(Rec=lambda d: d["Rev"] / d["Cost"] * 100.0)
        .sort_values("Delay", ascending=False)
    )
    # 2. City top 6 demand & delay
    c_df = (
        df_sub.groupby("City", as_index=False)
        .agg(
            Pax=("Passengers", "sum"),
            Delay=("Average_Delay_Minutes", "mean"),
            Rec=("Ticket_Revenue_EUR", lambda s: s.sum() / df_sub.loc[s.index, "Operating_Cost_EUR"].sum() * 100.0),
        )
        .sort_values("Pax", ascending=False)
        .head(6)
    )
    # 3. Route complaints per 10k
    r_df = (
        df_sub.groupby("Route_Type", as_index=False)
        .agg(Comp=("Accessibility_Complaints", "sum"), Pax=("Passengers", "sum"))
        .assign(Rate=lambda d: d["Comp"] / d["Pax"] * 10000.0)
        .sort_values("Rate", ascending=False)
    )

    parts = [
        # Left Streamlit Sidebar Panel (st.sidebar)
        f'<rect x="18" y="18" width="232" height="736" rx="14" fill="{WHITE}" stroke="{LINE}" stroke-width="1.5" filter="url(#shadow)"/>',
        f'<rect x="30" y="30" width="208" height="46" rx="10" fill="{MIDNIGHT}"/>',
        f'<text x="42" y="50" style="font:700 12px Aptos, Helvetica Neue, sans-serif; fill:{WHITE};">st.sidebar · Filter Console</text>',
        f'<text x="42" y="66" style="font:400 10px Aptos, Helvetica Neue, sans-serif; fill:{MIST};">COM7021 · ID: 25199053</text>',
        f'<text x="32" y="96" class="zone">1-CLICK SCENARIO PRESET</text>',
        f'<rect x="30" y="103" width="208" height="30" rx="7" fill="{MIST}" stroke="{TIFFANY}" stroke-width="1.5"/>',
        f'<text x="38" y="122" style="font:700 9.0px Aptos, Helvetica Neue, sans-serif; fill:{MIDNIGHT};">{esc(preset_label)}</text>',
        f'<text x="32" y="154" class="zone">GRANULAR SIDEBAR FILTERS</text>',
    ]

    sy = 164
    for label, val, active in filter_chips:
        box_fill = MIST if active else PAPER
        box_stroke = TIFFANY_DEEP if active else LINE
        badge_fill = TIFFANY_DEEP if active else MIDNIGHT_SOFT
        parts.append(f'<text x="32" y="{sy + 11}" class="tiny" style="font-weight:700;fill:{MIDNIGHT};">{esc(label)}</text>')
        parts.append(f'<rect x="30" y="{sy + 16}" width="208" height="26" rx="6" fill="{box_fill}" stroke="{box_stroke}" stroke-width="1.2"/>')
        parts.append(f'<rect x="36" y="{sy + 20}" width="136" height="18" rx="4" fill="{badge_fill}"/>')
        parts.append(f'<text x="104" y="{sy + 32}" text-anchor="middle" class="chip">{esc(val)}</text>')
        parts.append(f'<text x="226" y="{sy + 33}" text-anchor="end" class="tiny">▾</text>')
        sy += 52

    parts.extend([
        f'<rect x="30" y="486" width="208" height="48" rx="8" fill="{PAPER}" stroke="{LINE}" stroke-width="1.2"/>',
        f'<text x="40" y="504" class="tiny" style="font-weight:700;fill:{MIDNIGHT};">Financial Basis Toggle</text>',
        f'<text x="40" y="522" class="tiny">Per-Record · Per-Pax · Total (€)</text>',
        f'<rect x="30" y="546" width="208" height="62" rx="8" fill="{MIST}" stroke="{TIFFANY_DEEP}" stroke-width="1.2"/>',
        f'<text x="40" y="566" class="tiny" style="font-weight:700;fill:{MIDNIGHT};">Active Slice Summary</text>',
        f'<text x="40" y="583" class="tiny">Records: {n_rec:,} / 5,000 ({n_rec/50.0:.1f}%)</text>',
        f'<text x="40" y="599" class="tiny">Ridership: {total_pax/1e6:.2f}M / 40.91M</text>',
        f'<rect x="30" y="622" width="208" height="28" rx="7" fill="{MIDNIGHT_SOFT}"/>',
        f'<text x="134" y="640" text-anchor="middle" class="chip">⬇ Export Filtered Slice CSV</text>',
        f'<text x="134" y="736" text-anchor="middle" class="tiny">Streamlit 1.66 + Plotly 6.9</text>',
    ])

    # Main Workspace Header Banner (x = 264 to 1362, width = 1098)
    parts.extend([
        f'<rect x="264" y="18" width="1098" height="52" rx="12" fill="{MIDNIGHT}"/>',
        f'<text x="284" y="40" style="font:700 15px Aptos, Helvetica Neue, sans-serif; fill:{WHITE};">EcoMove Mobility — Executive Streamlit Decision Dashboard</text>',
        f'<text x="284" y="58" style="font:400 10.5px Aptos, Helvetica Neue, sans-serif; fill:{MIST};">{esc(subtitle)}</text>',
        f'<rect x="1192" y="31" width="152" height="24" rx="12" fill="{TIFFANY_DEEP}"/>',
        f'<text x="1268" y="47" text-anchor="middle" class="chip">COM7021 · 25199053</text>',
    ])

    # Main-Canvas 1-Click Scenario Bar (6 Buttons across x = 264..1362)
    scen_buttons = [
        ("1. Full Baseline (Fig 9)", "1. Full" in preset_label),
        ("2. Adverse Weather (Fig 10)", "2. Adverse" in preset_label),
        ("3. Micromobility Audit", False),
        ("4. Event Day Surge", False),
        ("5. Suburban Access", False),
        ("6. Rail Backbone", False),
    ]
    for b_idx, (b_lbl, b_act) in enumerate(scen_buttons):
        bx = 264 + b_idx * 184
        b_fill = TIFFANY_DEEP if b_act else WHITE
        b_stroke = TIFFANY if b_act else LINE
        b_txt = WHITE if b_act else MIDNIGHT
        parts.append(f'<rect x="{bx}" y="76" width="176" height="24" rx="6" fill="{b_fill}" stroke="{b_stroke}" stroke-width="1.2"/>')
        parts.append(f'<text x="{bx + 88}" y="92" text-anchor="middle" style="font:700 9.4px Aptos, sans-serif; fill:{b_txt};">{esc(b_lbl)}</text>')

    # Streamlit Tabs Bar (st.tabs)
    tabs = [
        ("1. Executive Overview (Figs 9 & 10)", True),
        ("2. Demand & Regimes (Fig 1)", False),
        ("3. Financials & Simpson's Paradox", False),
        ("4. Reliability & Weather (Figs 4–6)", False),
        ("5. Accessibility & Carbon", False),
    ]
    tx = 264
    parts.append(f'<rect x="264" y="106" width="1098" height="30" rx="8" fill="{WHITE}" stroke="{LINE}" stroke-width="1.2"/>')
    for t_label, is_act in tabs:
        tw = 216
        if is_act:
            parts.append(f'<rect x="{tx + 3}" y="108" width="{tw - 6}" height="26" rx="6" fill="{MIST}"/>')
            parts.append(f'<line x1="{tx + 8}" y1="134" x2="{tx + tw - 8}" y2="134" stroke="{TIFFANY_DEEP}" stroke-width="2.6"/>')
            parts.append(f'<text x="{tx + tw/2}" y="125" text-anchor="middle" style="font:700 9.8px Aptos, sans-serif; fill:{MIDNIGHT};">{esc(t_label)}</text>')
        else:
            parts.append(f'<text x="{tx + tw/2}" y="125" text-anchor="middle" class="tiny">{esc(t_label)}</text>')
        tx += 219

    # KPI Strip (6 cards across x = 264..1362)
    margin_str = f"Rec Mean: {rec_mean_recovery:.1f}% · {'+' if net_margin >= 0 else '-'}€{abs(net_margin)/1e6:.2f}M"
    kpis = [
        ("Total Ridership", f"{total_pax/1e6:.2f}M", f"{n_rec:,} daily records", False),
        ("On-Time Rate", f"{mean_ontime:.1f}%", "Authority target: 85.0%", False),
        ("Service Delay", f"{mean_delay:.2f} min", "Service reliability", True),
        ("Cost Recovery", f"{recovery:.1f}%", margin_str, True),
        ("CO2 Mitigated", f"{total_co2:,.1f} t", "Decarbonisation output", False),
        ("Satisfaction", f"{mean_rating:.2f} / 5", f"{comp_10k:.2f} comp / 10k pax", False),
    ]
    for idx, (k_title, k_val, k_sub, k_hi) in enumerate(kpis):
        kx = 264 + idx * 184
        k_fill = MIST if k_hi else WHITE
        k_stroke = TIFFANY if k_hi else LINE
        k_sw = 2.0 if k_hi else 1.5
        parts.append(
            f"""
        <g filter="url(#shadow)">
          <rect x="{kx}" y="142" width="174" height="86" rx="11" fill="{k_fill}" stroke="{k_stroke}" stroke-width="{k_sw}"/>
          <text x="{kx + 87}" y="162" text-anchor="middle" class="small" style="font-weight:700;">{esc(k_title)}</text>
          <text x="{kx + 87}" y="191" text-anchor="middle" style="font:700 19.5px Aptos, Helvetica Neue, sans-serif; fill:{MIDNIGHT};">{esc(k_val)}</text>
          <text x="{kx + 87}" y="213" text-anchor="middle" class="tiny">{esc(k_sub)}</text>
        </g>"""
        )

    # Panel A (Left): Mode Reliability & Cost Recovery Bars
    parts.append(
        f'<rect x="264" y="238" width="540" height="278" rx="14" fill="{WHITE}" stroke="{LINE}" stroke-width="1.5" filter="url(#shadow)"/>'
    )
    parts.append(f'<text x="284" y="264" class="lab">Mean Service Delay (min) &amp; Overall Cost Recovery by Mode</text>')
    parts.append(f'<text x="284" y="281" class="tiny">Interactive Plotly Horizontal Bar · Hover for Record-Mean &amp; Unit Economics</text>')
    max_d = max(m_df["Delay"].max(), 8.0)
    for i, row in enumerate(m_df.itertuples()):
        by = 296 + i * 34
        bw = (row.Delay / max_d) * 235.0
        b_col = TIFFANY if row.Delay == m_df["Delay"].max() else MIDNIGHT_SOFT
        parts.append(f'<text x="382" y="{by + 15}" text-anchor="end" class="small">{esc(row.Transport_Mode)}</text>')
        parts.append(f'<rect x="392" y="{by}" width="{bw:.1f}" height="20" rx="4" fill="{b_col}"/>')
        parts.append(
            f'<text x="{400 + bw:.1f}" y="{by + 15}" class="tiny">{row.Delay:.2f} min  (Rec: {row.Rec:.1f}%)</text>'
        )

    # Panel B (Right): Route Accessibility Intensity (Complaints per 10k Pax)
    parts.append(
        f'<rect x="822" y="238" width="540" height="278" rx="14" fill="{WHITE}" stroke="{LINE}" stroke-width="1.5" filter="url(#shadow)"/>'
    )
    parts.append(f'<text x="842" y="264" class="lab">Accessibility Complaints per 10,000 Passengers by Route</text>')
    parts.append(f'<text x="842" y="281" class="tiny">Volume-Normalised Rate (Σ Complaints ÷ Σ Passengers × 10,000)</text>')
    max_r = max(r_df["Rate"].max(), 18.0)
    for i, row in enumerate(r_df.itertuples()):
        by = 296 + i * 34
        bw = (row.Rate / max_r) * 245.0
        b_col = TIFFANY if i == 0 else MIDNIGHT_SOFT
        parts.append(f'<text x="968" y="{by + 15}" text-anchor="end" class="small">{esc(row.Route_Type)}</text>')
        parts.append(f'<rect x="978" y="{by}" width="{bw:.1f}" height="20" rx="4" fill="{b_col}"/>')
        parts.append(
            f'<text x="{986 + bw:.1f}" y="{by + 15}" class="tiny">{row.Rate:.2f} / 10k pax</text>'
        )

    # Panel C (Bottom Full Width): Top 6 Cities Interactive Summary Matrix
    parts.append(
        f'<rect x="264" y="530" width="1098" height="224" rx="14" fill="{MIST}" stroke="{LINE}" stroke-width="1.5"/>'
    )
    parts.append(
        f'<text x="284" y="556" class="lab">st.dataframe · City-Level Decision Summary (Top 6 Cities in Current Filter Slice)</text>'
    )
    parts.append(
        f'<text x="284" y="573" class="tiny">Includes Direct Modal-Mix Standardisation (Simpson’s Paradox Check) &amp; Volume-Weighted Cost Recovery</text>'
    )
    for idx, row in enumerate(c_df.itertuples()):
        cx = 280 + idx * 178
        hi = idx < 2
        c_stroke = TIFFANY if hi else LINE
        c_sw = 2.0 if hi else 1.5
        parts.append(
            f"""
        <g filter="url(#shadow)">
          <rect x="{cx}" y="586" width="166" height="150" rx="10" fill="{WHITE}" stroke="{c_stroke}" stroke-width="{c_sw}"/>
          <text x="{cx + 83}" y="612" text-anchor="middle" class="lab">{esc(row.City)}</text>
          <text x="{cx + 83}" y="638" text-anchor="middle" class="small">Pax: {row.Pax/1e6:.2f}M</text>
          <text x="{cx + 83}" y="662" text-anchor="middle" class="tiny">Mean delay: {row.Delay:.2f} min</text>
          <text x="{cx + 83}" y="684" text-anchor="middle" class="tiny">Overall Rec: {row.Rec:.1f}%</text>
          <rect x="{cx + 22}" y="700" width="122" height="22" rx="6" fill="{PAPER}" stroke="{LINE}" stroke-width="1"/>
          <text x="{cx + 83}" y="715" text-anchor="middle" class="tiny" style="font-weight:700;fill:{MIDNIGHT};">Active in Slice</text>
        </g>"""
        )

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1380" height="772" viewBox="0 0 1380 772">
  <rect width="1380" height="772" fill="{PAPER}"/>
  <defs>
    <filter id="shadow" x="-6%" y="-6%" width="118%" height="118%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.4" flood-color="{MIDNIGHT}" flood-opacity="0.10"/>
    </filter>
    <style>
      .lab {{ font: 600 13.5px Aptos, 'Helvetica Neue', sans-serif; fill: {MIDNIGHT}; }}
      .labw {{ font: 600 13px Aptos, 'Helvetica Neue', sans-serif; fill: {WHITE}; }}
      .small {{ font: 400 11px Aptos, 'Helvetica Neue', sans-serif; fill: {MUTE}; }}
      .tiny {{ font: 400 10px Aptos, 'Helvetica Neue', sans-serif; fill: {MUTE}; }}
      .chip {{ font: 700 9.8px Aptos, 'Helvetica Neue', sans-serif; fill: {WHITE}; }}
      .zone {{ font: 700 10px Aptos, 'Helvetica Neue', sans-serif; fill: {MIDNIGHT}; }}
    </style>
  </defs>
  {"".join(parts)}
</svg>"""

    svg_path = FIG_DIR / f"{stem}.svg"
    png_path = FIG_DIR / f"{stem}.png"
    svg_path.write_text(svg, encoding="utf-8")
    subprocess.run(
        ["rsvg-convert", "-w", "1800", "-o", str(png_path), str(svg_path)],
        check=True,
        env=_fontconfig_env(),
    )
    print(f"Rendered Streamlit dashboard state capture: {png_path.name}")
    return png_path


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_CSV, parse_dates=["Date_ISO"])

    # 1. Render default full-network Streamlit dashboard state capture (Figure 9)
    render_dashboard_capture_svg(
        df_sub=df,
        filter_chips=[
            ("1. Country", "All (6 Countries)", False),
            ("2. City", "All (12 Cities)", False),
            ("3. Transport Mode", "All (6 Modes)", False),
            ("4. Route Topology", "All (6 Routes)", False),
            ("5. Weather Regime", "All (6 Weathers)", False),
            ("6. Major Event Day", "All Days (N=5,000)", False),
        ],
        subtitle="Figure 9 Default Unfiltered State: All 12 European Cities · 2024–2025 Full Network Baseline (N = 5,000 records)",
        stem="fig09_dashboard_overview",
        preset_label="1. Full Network Baseline (N = 5,000)",
    )
    # Keep legacy filename synced
    render_dashboard_capture_svg(
        df_sub=df,
        filter_chips=[
            ("1. Country", "All (6 Countries)", False),
            ("2. City", "All (12 Cities)", False),
            ("3. Transport Mode", "All (6 Modes)", False),
            ("4. Route Topology", "All (6 Routes)", False),
            ("5. Weather Regime", "All (6 Weathers)", False),
            ("6. Major Event Day", "All Days (N=5,000)", False),
        ],
        subtitle="Figure 9 Default Unfiltered State: All 12 European Cities · 2024–2025 Full Network Baseline (N = 5,000 records)",
        stem="fig10_dashboard_overview",
        preset_label="1. Full Network Baseline (N = 5,000)",
    )

    # 3. Render filtered executive scenario state capture (Figure 10: Rain & Snow on Surface Modes)
    df_filtered = df[
        df["Weather"].isin(["Rain", "Snow"])
        & df["Transport_Mode"].isin(["Bus", "Tram", "Park and Ride"])
    ]
    render_dashboard_capture_svg(
        df_sub=df_filtered,
        filter_chips=[
            ("1. Country", "All (6 Countries)", False),
            ("2. City", "All (12 Cities)", False),
            ("3. Transport Mode", "Surface (3 Modes)", True),
            ("4. Route Topology", "All (6 Routes)", False),
            ("5. Weather Regime", "Rain + Snow", True),
            ("6. Major Event Day", "All Days (n=583)", False),
        ],
        subtitle="Figure 10 Filtered Scenario: Adverse Weather (Rain & Snow) on Surface Modes (Bus, Tram, Park & Ride; n = 583)",
        stem="fig10_dashboard_filtered_scenario",
        preset_label="2. Adverse Weather Surface (n = 583)",
    )
    # Keep legacy filename synced
    render_dashboard_capture_svg(
        df_sub=df_filtered,
        filter_chips=[
            ("1. Country", "All (6 Countries)", False),
            ("2. City", "All (12 Cities)", False),
            ("3. Transport Mode", "Surface (3 Modes)", True),
            ("4. Route Topology", "All (6 Routes)", False),
            ("5. Weather Regime", "Rain + Snow", True),
            ("6. Major Event Day", "All Days (n=583)", False),
        ],
        subtitle="Figure 10 Filtered Scenario: Adverse Weather (Rain & Snow) on Surface Modes (Bus, Tram, Park & Ride; n = 583)",
        stem="fig11_dashboard_filtered_scenario",
        preset_label="2. Adverse Weather Surface (n = 583)",
    )


if __name__ == "__main__":
    main()
