"""Arden Midnight / Tiffany figure style for COM7021 Assessment.
Follows COM7021 - Assignment/VISUAL_DESIGN_GUIDE.md.
"""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap

MIDNIGHT = "#002B49"
TIFFANY = "#66C9BA"
TIFFANY_DEEP = "#3AA89A"
MIDNIGHT_SOFT = "#1A4A6B"
TEAL = "#0E7C8B"
MIST = "#E6F5F2"
PAPER = "#F7FAFB"
MUTE = "#5A6B75"
GRID = "#D5DEE3"
LINE = "#C9D5DD"
WHITE = "#FFFFFF"

# Five-series order. Tiffany stays last so it can still be the highlight.
SERIES = [MIDNIGHT, TIFFANY_DEEP, TEAL, MIDNIGHT_SOFT, TIFFANY]

# House heatmap colormap: mist -> tiffany -> tiffany_deep -> midnight_soft -> midnight
ARDEN_CMAP = LinearSegmentedColormap.from_list(
    "arden_heatmap",
    [MIST, TIFFANY, TIFFANY_DEEP, MIDNIGHT_SOFT, MIDNIGHT],
    N=256,
)


def _resolve_font_family() -> str:
    """Use Microsoft Aptos when available, with clean sans-serif fallback."""
    available = {f.name for f in font_manager.fontManager.ttflist}
    for candidate in ("Aptos", "Helvetica Neue", "Arial", "DejaVu Sans"):
        if candidate in available:
            return candidate
    return "sans-serif"


FONT_FAMILY = _resolve_font_family()


def apply_rcparams() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Aptos", "Helvetica Neue", "Arial", "DejaVu Sans"],
            "axes.titleweight": "bold",
            "axes.labelweight": "semibold",
            "figure.facecolor": WHITE,
            "axes.facecolor": PAPER,
            "text.color": MIDNIGHT,
            "axes.labelcolor": MIDNIGHT,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 9,
            "figure.dpi": 160,
            "savefig.dpi": 220,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.25,
        }
    )


def style_axes(ax, grid_axis: str = "y") -> None:
    ax.set_facecolor(PAPER)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTE, labelsize=10)
    ax.yaxis.label.set_color(MIDNIGHT)
    ax.xaxis.label.set_color(MIDNIGHT)
    ax.yaxis.label.set_fontweight("semibold")
    ax.xaxis.label.set_fontweight("semibold")
    ax.title.set_color(MIDNIGHT)
    ax.title.set_fontweight("bold")
    ax.grid(False)
    if grid_axis in ("x", "y", "both"):
        ax.grid(True, axis=grid_axis, color=GRID, linewidth=1.0)
    ax.set_axisbelow(True)


def save(fig, path: str | Path) -> Path:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved figure: {out_path}")
    return out_path
