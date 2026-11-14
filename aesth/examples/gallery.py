"""Proof gallery for the public aesth API.

One job per figure. Toy cities only.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))

import pandas as pd
from plotnine import aes, ggplot, labs, scale_x_discrete

import aesth

OUT = ROOT / "studies"

HOURS = list(range(8, 16))
LEEDS = [42, 48, 55, 61, 58, 63, 70, 66]
YORK = [30, 33, 36, 40, 39, 44, 47, 45]


def _cities() -> pd.DataFrame:
    """Two contiguous series, so a line is a line and not a join between cities."""
    return pd.DataFrame(
        {
            "hour": HOURS + HOURS,
            "demand": LEEDS + YORK,
            "city": ["Leeds"] * len(HOURS) + ["York"] * len(HOURS),
        }
    )


def _leeds() -> pd.DataFrame:
    return pd.DataFrame({"hour": HOURS, "demand": LEEDS})


def line_chart():
    """Carbon: Leeds is accent, York is ink."""
    frame = _cities()
    return (
        ggplot(frame, aes("hour", "demand", color="city", group="city"))
        + aesth.line(palette="carbon")
        + labs(title="Morning demand by city", x="Hour", y="Passengers")
        + aesth.dress(
            "carbon",
            colour=True,
            claim="Leeds",
            levels=["Leeds", "York"],
        )
    )


def bar_chart():
    """One claimed bar. The other cities stay the quiet default fill."""
    frame = pd.DataFrame(
        {
            "city": ["York", "Leeds", "Hull", "Ripon"],
            "boardings": [960, 1840, 720, 310],
        }
    )
    claimed = frame[frame["city"] == "Leeds"]
    quiet = frame[frame["city"] != "Leeds"]
    return (
        ggplot(frame, aes("city", "boardings"))
        + aesth.col(data=quiet, palette="arden")
        + aesth.col(data=claimed, claim=True, palette="arden")
        + scale_x_discrete(limits=["York", "Leeds", "Hull", "Ripon"])
        + labs(title="Weekday boardings by city", x="City", y="Boardings")
        + aesth.dress("arden")
    )


def area_chart():
    return (
        ggplot(_leeds(), aes("hour", "demand"))
        + aesth.area(palette="arden")
        + labs(title="Hourly demand in Leeds", x="Hour", y="Passengers")
        + aesth.dress("arden")
    )


def band_chart():
    """A short accent window behind one ink line."""
    series = _leeds()
    ceiling = float(max(LEEDS))
    window = pd.DataFrame(
        {
            "hour": [11, 13],
            "low": [0, 0],
            "high": [ceiling, ceiling],
        }
    )
    return (
        ggplot(series, aes("hour", "demand"))
        + aesth.band(
            aes("hour", ymin="low", ymax="high"),
            data=window,
            inherit_aes=False,
            palette="arden",
        )
        + aesth.line(palette="arden")
        + labs(title="Peak window on weekday demand", x="Hour", y="Passengers")
        + aesth.dress("arden")
    )


def table():
    frame = pd.DataFrame(
        {
            "city": ["Leeds", "York", "Hull", "Ripon"],
            "boardings": [1840, 960, 720, 310],
            "share": [0.48, 0.25, 0.19, 0.08],
        }
    )
    built = (
        aesth.GT_aesth(frame, palette="arden", stripe=True)
        .tab_header(title="Morning boardings", subtitle="Toy cities")
        .fmt_number(columns="share", decimals=2)
    )
    return aesth.highlight_column(built, "boardings", palette="arden")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = {
        "gallery_line.png": line_chart(),
        "gallery_bars.png": bar_chart(),
        "gallery_area.png": area_chart(),
        "gallery_band.png": band_chart(),
    }
    for name, plot in jobs.items():
        path = OUT / name
        aesth.save(plot, path)
        print(path)

    built = table()
    html_path = OUT / "gallery_table.html"
    html_path.write_text(built.as_raw_html(), encoding="utf-8")
    print(html_path)

    png_path = OUT / "gallery_table.png"
    # GT.save needs selenium, which this venv does not have.
    # gtsave is the installed path (nokap) and writes PNG.
    if not hasattr(built, "gtsave"):
        print("table png skipped: GT.gtsave is not available")
        return
    built.gtsave(png_path)
    print(png_path)


if __name__ == "__main__":
    main()
