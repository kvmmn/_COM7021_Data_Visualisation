from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
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

SERIES = [MIDNIGHT, TIFFANY_DEEP, TEAL, MIDNIGHT_SOFT, TIFFANY]
ARDEN_CMAP = LinearSegmentedColormap.from_list(
    "arden_heatmap", [MIST, TIFFANY, TIFFANY_DEEP, MIDNIGHT_SOFT, MIDNIGHT], N=256
)
FONT_FAMILY = "Aptos, Calibri, Helvetica Neue, Arial, sans-serif"


def apply_rcparams():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Aptos", "Calibri", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 10.0,
        "figure.facecolor": WHITE,
        "figure.dpi": 220,
        "axes.facecolor": WHITE,
        "axes.edgecolor": LINE,
        "axes.titlesize": 12.5,
        "axes.titleweight": "bold",
        "axes.labelsize": 10.0,
        "axes.labelweight": "semibold",
        "axes.labelcolor": MIDNIGHT,
        "xtick.labelsize": 9.0,
        "xtick.color": MUTE,
        "ytick.labelsize": 9.0,
        "ytick.color": MUTE,
        "grid.color": GRID,
        "grid.linestyle": "--",
        "grid.linewidth": 0.7,
        "legend.frameon": False,
        "legend.fontsize": 9.0,
    })


def style_axes(ax, grid_axis="y"):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(LINE)
    ax.tick_params(colors=MUTE, which="both")
    ax.xaxis.label.set_color(MIDNIGHT)
    ax.yaxis.label.set_color(MIDNIGHT)
    if grid_axis in ("x", "y", "both"):
        ax.grid(axis=grid_axis, color=GRID, alpha=0.75)
        ax.set_axisbelow(True)
    else:
        ax.grid(False)


def save(fig, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
