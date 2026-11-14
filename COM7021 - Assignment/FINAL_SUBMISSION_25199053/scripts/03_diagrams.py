from pathlib import Path
import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from style.palette import (
    LINE, MIDNIGHT, MIDNIGHT_SOFT, MIST, MUTE, PAPER,
    TIFFANY, TIFFANY_DEEP, WHITE, apply_rcparams, save,
)

OUT = ROOT / "output" / "figures"


def _canvas(w_in, h_in, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w_in, h_in))
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    ax.set_xlim(0, xlim)
    ax.set_ylim(0, ylim)
    ax.axis("off")
    return fig, ax


def _card(ax, x, y, w, h, fc=WHITE, ec=LINE, lw=1.4, pad=0.04, r=0.14):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={pad},rounding_size={min(r, h * 0.48):.3f}", facecolor=fc, edgecolor=ec, linewidth=lw))


def draw_kpi_strip():
    cards = [
        ("Passengers", "40.91M", "12 EU cities", False),
        ("On-time rate", "82.1%", "mean service", False),
        ("Mean delay", "4.35m", "Bus: 6.58m", True),
        ("Cost recovery", "99.6%", "Bike: 5.2%", True),
        ("CO2 saved", "4,482t", "Metro: 70.3%", False),
        ("Satisfaction", "4.01", "1 to 5 scale", False),
    ]
    fig, ax = _canvas(10.4, 1.85, 10.4, 1.85)
    for i, (label, metric, sub, hi) in enumerate(cards):
        x = 0.25 + i * 1.67
        _card(ax, x, 0.25, 1.48, 1.32, fc=MIST if hi else WHITE, ec=TIFFANY if hi else LINE, lw=2.0 if hi else 1.4)
        cx = x + 0.74
        ax.text(cx, 1.32, label, ha="center", va="center", fontsize=9.5, color=MUTE)
        ax.text(cx, 0.89, metric, ha="center", va="center", fontsize=17.5, fontweight="bold", color=MIDNIGHT)
        ax.text(cx, 0.48, sub, ha="center", va="center", fontsize=8.5, color=MUTE)
    save(fig, OUT / "fig00_executive_kpi_strip.png")


def draw_pipeline_diagram() -> None:
    stages = [
        ("01", "Ingest xlsx", "5,000 rows\n18 columns", False, False),
        ("02", "Type hygiene", "serial Date\nISO 2024–25", False, False),
        ("03", "Derived ratios", "cost recovery\nrate / 10k pax", True, False),
        ("04", "Seven charts", "matplotlib\n220 dpi PNG", False, False),
        ("05", "Dashboard", "multi-filter\ndecision view", True, True),
    ]
    fig, ax = _canvas(10.2, 2.5, 10.2, 2.5)
    for i, (num, title, sub, hi, dark_edge) in enumerate(stages):
        x = 0.35 + i * 2.0
        cx = x + 0.72
        ax.add_patch(Circle((cx, 1.98), 0.17, facecolor=MIDNIGHT, edgecolor="none"))
        ax.text(cx, 1.98, num, ha="center", va="center", fontsize=9.5, fontweight="bold", color=WHITE)
        ec = MIDNIGHT if dark_edge else (TIFFANY if hi else LINE)
        _card(ax, x, 0.85, 1.44, 0.88, fc=MIST if hi else WHITE, ec=ec, lw=1.9 if hi else 1.4)
        ax.text(cx, 1.44, title, ha="center", va="center", fontsize=10.5, fontweight="bold", color=MIDNIGHT)
        ax.text(cx, 1.08, sub, ha="center", va="center", fontsize=8.5, color=MUTE, linespacing=1.25)
        if i < 4:
            col = TIFFANY_DEEP if i >= 1 else MUTE
            ax.annotate("", xy=(x + 1.92, 1.29), xytext=(x + 1.52, 1.29), arrowprops=dict(arrowstyle="-|>,head_width=0.22,head_length=0.35", color=col, lw=1.8))

    for px, w, tag, fill in (
        (2.4, 1.45, "pandas 3.0", MIDNIGHT),
        (4.15, 1.85, "normalised metrics", TIFFANY_DEEP),
        (6.3, 1.6, "Arden palette", MIDNIGHT_SOFT),
    ):
        _card(ax, px, 0.22, w, 0.28, fc=fill, ec="none", pad=0.04)
        ax.text(px + w / 2, 0.36, tag, ha="center", va="center", fontsize=8.5, fontweight="bold", color=WHITE)
    save(fig, OUT / "fig00_methodology_pipeline.png")


def draw_mode_matrix() -> None:
    modes = ["Metro", "Tram", "Park & Ride", "Bus", "Bike Share", "E-Scooter"]
    rows = [
        ("Demand share", ["63.0%", "15.6%", "8.0%", "12.4%", "0.7%", "0.4%"]),
        ("Mean delay", ["3.73 min", "4.79 min", "5.17 min", "6.58 min", "1.62 min", "1.94 min"]),
        ("Cost recovery", ["106.2%", "117.3%", "121.5%", "100.1%", "5.2%", "7.4%"]),
        ("CO2 / kWh", ["2.19 kg", "1.66 kg", "1.72 kg", "1.07 kg", "0 kWh", "7.21 kg"]),
        ("Complaints/10k", ["14.85", "15.08", "15.87", "17.46", "17.00", "18.36"]),
    ]
    fig, ax = _canvas(10.5, 4.65, 10.5, 4.65)
    _card(ax, 0.25, 0.22, 10.0, 4.15, fc=MIST, ec=LINE, lw=1.2, pad=0.06)

    _card(ax, 0.42, 3.72, 1.25, 0.42, fc=MIDNIGHT, ec="none", pad=0.04)
    ax.text(1.045, 3.93, "Dimension", ha="center", va="center", fontsize=10, fontweight="bold", color=WHITE)
    for i, m in enumerate(modes):
        mx = 1.82 + i * 1.38
        _card(ax, mx, 3.72, 1.24, 0.42, fc=TIFFANY_DEEP if i == 0 else MIDNIGHT, ec="none", pad=0.04)
        ax.text(mx + 0.62, 3.93, m, ha="center", va="center", fontsize=10, fontweight="bold", color=WHITE)

    for r_idx, (metric, vals) in enumerate(rows):
        ry = 3.05 - r_idx * 0.62
        ax.text(1.045, ry + 0.24, metric, ha="center", va="center", fontsize=10, fontweight="bold", color=MIDNIGHT)
        for c_idx, val in enumerate(vals):
            cx = 1.82 + c_idx * 1.38
            _card(ax, cx, ry, 1.24, 0.46, fc=WHITE, ec=TIFFANY if c_idx == 0 else LINE, lw=1.9 if c_idx == 0 else 1.2, pad=0.04)
            ax.text(cx + 0.62, ry + 0.23, val, ha="center", va="center", fontsize=9.5, color=MUTE if c_idx else MIDNIGHT)

    _card(ax, 1.9, 0.25, 1.08, 0.23, fc=TIFFANY_DEEP, ec="none", pad=0.02, r=0.11)
    ax.text(2.44, 0.365, "Core backbone", ha="center", va="center", fontsize=8, fontweight="bold", color=WHITE)
    save(fig, OUT / "fig08_mode_performance_matrix.png")


def main() -> None:
    apply_rcparams()
    draw_kpi_strip()
    draw_pipeline_diagram()
    draw_mode_matrix()
    print("Generated fig00 KPI strip, methodology pipeline, and fig08 mode matrix cleanly.")


if __name__ == "__main__":
    main()
