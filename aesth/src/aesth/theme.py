"""plotnine theme and scales bound to the active aesth palette."""

from __future__ import annotations

from collections.abc import Sequence

from aesth.claim import _SERIES_LIMIT, _refuse_series_count, colour_map
from aesth.fonts import resolve_sans
from aesth.palettes import get_palette
from aesth.tokens import Palette


def _plotnine():
    try:
        from plotnine import (
            element_blank,
            element_line,
            element_rect,
            element_text,
            scale_color_manual,
            scale_colour_manual,
            scale_fill_manual,
            theme,
            theme_minimal,
        )
    except ImportError as exc:
        raise ImportError(
            "theme_aesth requires plotnine. Install with: pip install 'aesth[charts]'"
        ) from exc
    return {
        "element_blank": element_blank,
        "element_line": element_line,
        "element_rect": element_rect,
        "element_text": element_text,
        "scale_color_manual": scale_color_manual,
        "scale_colour_manual": scale_colour_manual,
        "scale_fill_manual": scale_fill_manual,
        "theme": theme,
        "theme_minimal": theme_minimal,
    }


def _resolve(palette: str | Palette | None) -> Palette:
    if isinstance(palette, Palette):
        return palette
    return get_palette(palette)


def theme_aesth(palette: str | Palette | None = None, *, figure_size: tuple[float, float] = (10.5, 5.2)):
    """House theme: paper panel, horizontal grid, mute ticks, ink titles."""
    pn = _plotnine()
    tokens = _resolve(palette)
    family, _note = resolve_sans()

    return (
        pn["theme_minimal"](base_size=11, base_family=family)
        + pn["theme"](
            figure_size=figure_size,
            dpi=220,
            text=pn["element_text"](family=family, color=tokens.ink),
            plot_title=pn["element_text"](
                family=family,
                weight="bold",
                size=13,
                color=tokens.ink,
                margin={"b": 14, "unit": "pt"},
            ),
            plot_subtitle=pn["element_text"](
                family=family,
                size=10,
                color=tokens.mute,
            ),
            plot_caption=pn["element_text"](
                family=family,
                size=9,
                color=tokens.mute,
            ),
            axis_title=pn["element_text"](
                family=family,
                weight=600,
                size=11,
                color=tokens.ink,
            ),
            axis_text=pn["element_text"](
                family=family,
                size=10,
                color=tokens.mute,
            ),
            legend_title=pn["element_text"](
                family=family,
                size=9,
                color=tokens.ink,
            ),
            legend_text=pn["element_text"](
                family=family,
                size=9,
                color=tokens.ink,
            ),
            legend_background=pn["element_blank"](),
            legend_key=pn["element_blank"](),
            legend_frame=pn["element_blank"](),
            plot_background=pn["element_rect"](fill=tokens.white, color="none"),
            panel_background=pn["element_rect"](fill=tokens.paper, color="none"),
            panel_border=pn["element_blank"](),
            panel_grid_major_x=pn["element_blank"](),
            panel_grid_minor_x=pn["element_blank"](),
            panel_grid_minor_y=pn["element_blank"](),
            panel_grid_major_y=pn["element_line"](color=tokens.grid, size=0.4),
            axis_ticks=pn["element_line"](color=tokens.mute, size=0.4),
            axis_line=pn["element_line"](color=tokens.grid, size=0.6),
            strip_background=pn["element_rect"](fill=tokens.mist, color="none"),
            strip_text=pn["element_text"](
                family=family,
                size=10,
                color=tokens.ink,
                weight="bold",
            ),
        )
    )


def _value_count(values) -> int | None:
    if values is None or isinstance(values, (str, bytes, bool)) or callable(values):
        return None
    try:
        return len(values)
    except TypeError:
        return None


def _scale_values(
    tokens: Palette,
    *,
    claim: object | None,
    levels: Sequence[object] | None,
    kwargs: dict,
) -> dict:
    if claim is not None and "values" in kwargs:
        raise ValueError("pass claim or values, not both")
    kwargs = dict(kwargs)
    if claim is not None:
        if levels is None:
            raise ValueError("claim requires levels")
        kwargs["values"] = colour_map(levels, claim, tokens)
        kwargs.setdefault("limits", list(levels))
    else:
        kwargs.setdefault("values", list(tokens.series))
    count = _value_count(kwargs.get("values"))
    if count == 0:
        raise ValueError("aesth scale requires at least one colour")
    if count is not None:
        _refuse_series_count(count)
    for key in ("limits", "breaks"):
        width = _value_count(kwargs.get(key))
        if width is not None:
            _refuse_series_count(width)
    return kwargs


def _cap_palette(scale):
    """Raise when a manual scale is asked for a sixth series.

    plotnine only warns, then paints the extra level with the missing-value
    colour. The house rule is to facet or split.
    """
    original = scale.palette

    def palette(n: int):
        if n > _SERIES_LIMIT:
            _refuse_series_count(n)
        return original(n)

    scale.palette = palette
    return scale


def scale_colour_aesth(
    palette: str | Palette | None = None,
    *,
    claim: object | None = None,
    levels: Sequence[object] | None = None,
    **kwargs,
):
    pn = _plotnine()
    tokens = _resolve(palette)
    kwargs = _scale_values(tokens, claim=claim, levels=levels, kwargs=kwargs)
    return _cap_palette(pn["scale_colour_manual"](**kwargs))


def scale_fill_aesth(
    palette: str | Palette | None = None,
    *,
    claim: object | None = None,
    levels: Sequence[object] | None = None,
    **kwargs,
):
    pn = _plotnine()
    tokens = _resolve(palette)
    kwargs = _scale_values(tokens, claim=claim, levels=levels, kwargs=kwargs)
    return _cap_palette(pn["scale_fill_manual"](**kwargs))


scale_color_aesth = scale_colour_aesth
