"""Attach the house theme, and optionally the categorical scales, to a plotnine plot."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from aesth.palettes import get_palette
from aesth.theme import scale_colour_aesth, scale_fill_aesth, theme_aesth
from aesth.tokens import Palette


class dress:
    """Object that plotnine can add with ``+``.

    ``colour`` and ``fill`` turn on the aesth categorical scales.
    ``claim`` plus ``levels`` puts accent on one category.
    """

    def __init__(
        self,
        palette: str | Palette | None = None,
        *,
        colour: bool = False,
        fill: bool = False,
        claim: object | None = None,
        levels: Sequence[object] | None = None,
    ) -> None:
        if claim is not None and not (colour or fill):
            raise ValueError("dress(claim=...) needs colour=True or fill=True")
        if claim is not None and levels is None:
            raise ValueError("dress(claim=...) needs levels")
        self.palette = palette
        self.colour = colour
        self.fill = fill
        self.claim = claim
        self.levels = levels

    def __radd__(self, plot):
        plot += theme_aesth(self.palette)
        if self.colour:
            plot += scale_colour_aesth(
                self.palette, claim=self.claim, levels=self.levels
            )
        if self.fill:
            plot += scale_fill_aesth(
                self.palette, claim=self.claim, levels=self.levels
            )
        return plot

    def __repr__(self) -> str:
        name = self.palette if isinstance(self.palette, str) or self.palette is None else self.palette.name
        if name is None:
            name = get_palette().name
        return f"dress({name!r}, colour={self.colour}, fill={self.fill}, claim={self.claim!r})"


def finish(
    plot,
    palette: str | Palette | None = None,
    *,
    colour: bool = False,
    fill: bool = False,
    claim: object | None = None,
    levels: Sequence[object] | None = None,
):
    """Return a copy of ``plot`` with the house theme and optional scales."""
    return plot + dress(
        palette,
        colour=colour,
        fill=fill,
        claim=claim,
        levels=levels,
    )


def save(plot, filename: str | Path, **kwargs):
    """Save through plotnine at 220 dpi, tight bbox, 0.25 in pad."""
    kwargs.setdefault("dpi", 220)
    kwargs.setdefault("verbose", False)
    kwargs.setdefault("bbox_inches", "tight")
    kwargs.setdefault("pad_inches", 0.25)
    return plot.save(filename, **kwargs)


__all__ = ["dress", "finish", "save"]
