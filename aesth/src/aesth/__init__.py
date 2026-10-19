"""aesth — the aesthetics of data.

A thin visual language over plotnine, Great Tables, and Shiny.
Plotnine and Great Tables are imported only when their helpers are used.
"""

from __future__ import annotations

from aesth.palettes import PALETTES, get_palette, palette, use

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "use",
    "palette",
    "get_palette",
    "PALETTES",
    "theme_aesth",
    "scale_colour_aesth",
    "scale_fill_aesth",
    "scale_color_aesth",
    "GT_aesth",
    "css_aesth",
    "highlight_column",
    "page_css",
]


def __getattr__(name: str):
    if name in {
        "theme_aesth",
        "scale_colour_aesth",
        "scale_fill_aesth",
        "scale_color_aesth",
    }:
        from aesth import theme as _theme

        return getattr(_theme, name)
    if name == "GT_aesth":
        from aesth.tables import GT_aesth

        return GT_aesth
    if name == "highlight_column":
        from aesth.tables import highlight_column

        return highlight_column
    if name == "css_aesth":
        from aesth.shiny import css_aesth

        return css_aesth
    if name == "page_css":
        from aesth.shiny import page_css

        return page_css
    raise AttributeError(f"module 'aesth' has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__)
