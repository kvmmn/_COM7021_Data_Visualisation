"""Tiny Shiny proof: palette switcher, plotnine facet, Great Table, value boxes."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from plotnine import aes, facet_wrap, geom_point, geom_smooth, ggplot, labs
from plotnine.data import anscombe_quartet
from shiny.express import input, render, ui

import aesth

NAMES = list(aesth.PALETTES)

ui.page_opts(title="æsth")
ui.tags.style(aesth.css_aesth("arden"))

with ui.sidebar():
    ui.input_selectize("pal", "Palette", choices=NAMES, selected="arden")
    ui.p("Brand chrome is not a data hue. Switching palettes restyles plot, table, and CSS together.")


@render.ui
def live_css():
    return ui.tags.style(aesth.css_aesth(input.pal()))


with ui.layout_column_wrap(width=1 / 3):
    with ui.value_box():
        "Ink"
        ui.output_text("ink_hex")
        "structure"

    with ui.value_box(class_="aesth-claim"):
        "Accent"
        ui.output_text("accent_hex")
        "the claim"

    with ui.value_box():
        "Chip"
        ui.output_text("chip_hex")
        "AA white text"


@render.text
def ink_hex():
    return aesth.get_palette(input.pal()).ink


@render.text
def accent_hex():
    return aesth.get_palette(input.pal()).accent


@render.text
def chip_hex():
    return aesth.get_palette(input.pal()).chip_fill


@render.plot
def quartet():
    tokens = aesth.get_palette(input.pal())
    return (
        ggplot(anscombe_quartet, aes("x", "y"))
        + geom_point(color=tokens.accent, size=2.2)
        + geom_smooth(method="lm", se=False, color=tokens.ink, size=0.9)
        + facet_wrap("dataset")
        + labs(title="Anscombe's quartet")
        + aesth.theme_aesth(tokens, figure_size=(10.5, 6.2))
    )


@render.ui
def ranking():
    tokens_name = input.pal()
    frame = pd.DataFrame(
        {
            "city": ["Leeds", "Bristol", "Glasgow", "Cardiff", "Belfast"],
            "index": [112, 101, 97, 88, 79],
        }
    )
    table = (
        aesth.GT_aesth(frame, palette=tokens_name)
        .tab_header(title="Regional index", subtitle=tokens_name)
    )
    table = aesth.highlight_column(table, "index", palette=tokens_name)
    return ui.HTML(table.as_raw_html())
