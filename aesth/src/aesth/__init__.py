"""aesth — the aesthetics of data.

A thin visual language over plotnine, Great Tables, and Shiny.
Those three libraries are imported only when a helper asks for them.
Importing aesth does not load them, copy a frame, or build CSS.
"""

from __future__ import annotations

from aesth.palettes import PALETTES, get_palette, palette, use

__version__ = "0.3.0"

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
    "colour_map",
    "line",
    "point",
    "col",
    "area",
    "band",
    "dress",
    "finish",
    "save",
    "GT_aesth",
    "css_aesth",
    "highlight_column",
    "page_css",
    "page_aesth",
]


def __getattr__(name: str):
    if name == "colour_map":
        from aesth.claim import colour_map

        return colour_map
    if name in {
        "theme_aesth",
        "scale_colour_aesth",
        "scale_fill_aesth",
        "scale_color_aesth",
    }:
        from aesth import theme as _theme

        return getattr(_theme, name)
    if name in {"line", "point", "col", "area", "band"}:
        from aesth import marks as _marks

        return getattr(_marks, name)
    if name in {"dress", "finish", "save"}:
        from aesth import compose as _compose

        return getattr(_compose, name)
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
    if name == "page_aesth":
        from aesth.shiny import page_aesth

        return page_aesth
    raise AttributeError(f"module 'aesth' has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__)
