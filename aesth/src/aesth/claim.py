"""One highlight inside a categorical scale.

plotnine still draws the marks. This module only decides which level
receives ``accent`` and which stay quiet.
"""

from __future__ import annotations

from collections.abc import Sequence

from aesth.palettes import get_palette
from aesth.tokens import Palette

_SERIES_LIMIT = 5


def _refuse_series_count(count: int) -> None:
    """A sixth categorical series is a facet, not another hue."""
    if count > _SERIES_LIMIT:
        raise ValueError(
            f"aesth allows {_SERIES_LIMIT} categorical series; facet or split the figure"
        )


def _resolve(palette: str | Palette | None) -> Palette:
    if isinstance(palette, Palette):
        return palette
    return get_palette(palette)


def colour_map(
    levels: Sequence[object],
    claim: object,
    palette: str | Palette | None = None,
) -> dict[object, str]:
    """Map category levels to hex. ``claim`` is ``accent``; the rest walk the quiet series.

    At most five levels. A sixth means facet or split, not a new hue.
    """
    tokens = _resolve(palette)
    ordered = list(levels)
    if not ordered:
        raise ValueError("colour_map requires at least one level")
    if len(ordered) != len(set(ordered)):
        raise ValueError("colour_map levels must be unique")
    _refuse_series_count(len(ordered))
    if claim not in ordered:
        raise ValueError(f"claim {claim!r} is not in levels {ordered!r}")

    quiet = (tokens.ink, tokens.accent_deep, tokens.support, tokens.ink_soft)
    mapping: dict[object, str] = {}
    quiet_index = 0
    for level in ordered:
        if level == claim:
            mapping[level] = tokens.accent
        else:
            mapping[level] = quiet[quiet_index]
            quiet_index += 1
    return mapping


fill_map = colour_map
