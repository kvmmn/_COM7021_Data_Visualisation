"""plotnine geoms with house geometry already set.

These return ordinary plotnine layers. They do not invent a grammar.
A fixed colour is applied only when the layer is not already mapped:
a mapped ``color`` or ``fill`` stays free for ``dress(claim=...)``.
"""

from __future__ import annotations

from aesth.palettes import get_palette
from aesth.tokens import Palette

LINE_SIZE = 2.4
POINT_SIZE = 2.2
BAR_WIDTH = 0.85
BAR_EDGE = 0.4
AREA_ALPHA = 0.35
BAND_ALPHA = 0.12
AREA_LINE = 1.2


def _resolve(palette: str | Palette | None) -> Palette:
    if isinstance(palette, Palette):
        return palette
    return get_palette(palette)


def _mapped(mapping, *names: str) -> bool:
    if mapping is None:
        return False
    return any(name in mapping for name in names)


_CLAIM_MAPPING = (
    "claim=True paints one mark. Drop the colour or fill mapping, "
    "or pass the categories to dress(claim=..., levels=...)."
)


def _refuse_fixed_claim(mapping, claim: bool, *names: str) -> None:
    if claim and _mapped(mapping, *names):
        raise ValueError(_CLAIM_MAPPING)


def _has_param(geom, *names: str) -> bool:
    return any(name in geom.aes_params for name in names)


def _guard_plot_mapping(geom, *names: str):
    """Refuse claim once the plot mapping is known.

    A fixed colour lives in ``aes_params``. plotnine then deletes the same
    aesthetic from an inherited plot mapping, which collapses two series
    into one polyline. The layer mapping is checked at construction; the
    plot mapping only exists when the geom is added.
    """
    original = geom.__radd__

    def __radd__(plot):
        inherit = geom._kwargs.get("inherit_aes", True)
        if inherit and _mapped(getattr(plot, "mapping", None), *names):
            raise ValueError(_CLAIM_MAPPING)
        return original(plot)

    geom.__radd__ = __radd__  # type: ignore[method-assign]
    return geom


def _with_defaults(geom, **updates):
    """Instance defaults. A mapped aesthetic still wins; a fixed one does not."""
    geom.DEFAULT_AES = {**geom.DEFAULT_AES, **updates}
    return geom


def line(mapping=None, data=None, *, palette: str | Palette | None = None, claim: bool = False, **kwargs):
    """Line, width 2.4, round caps. ``claim`` uses accent; otherwise ink.

    House ink sits on ``DEFAULT_AES``, so a mapped colour still wins.
    ``claim=True`` is a constant accent and raises if the geom or the plot
    already maps colour.
    """
    from plotnine import geom_line

    tokens = _resolve(palette)
    _refuse_fixed_claim(mapping, claim, "color", "colour")
    if claim:
        kwargs.setdefault("color", tokens.accent)
    kwargs.setdefault("lineend", "round")
    geom = geom_line(mapping=mapping, data=data, **kwargs)
    defaults = {"size": LINE_SIZE}
    if not claim and not _has_param(geom, "color", "colour"):
        defaults["color"] = tokens.ink
    geom = _with_defaults(geom, **defaults)
    if claim:
        _guard_plot_mapping(geom, "color", "colour")
    return geom


def point(mapping=None, data=None, *, palette: str | Palette | None = None, claim: bool = False, **kwargs):
    """Point for a second encoding, such as weekend markers on a line."""
    from plotnine import geom_point

    tokens = _resolve(palette)
    _refuse_fixed_claim(mapping, claim, "color", "colour")
    if claim:
        kwargs.setdefault("color", tokens.accent)
    geom = geom_point(mapping=mapping, data=data, **kwargs)
    defaults = {"size": POINT_SIZE}
    if not claim and not _has_param(geom, "color", "colour"):
        defaults["color"] = tokens.ink
    geom = _with_defaults(geom, **defaults)
    if claim:
        _guard_plot_mapping(geom, "color", "colour")
    return geom


def col(mapping=None, data=None, *, palette: str | Palette | None = None, claim: bool = False, **kwargs):
    """Bar of width 0.85 with a white edge. Default fill is ink_soft; claim is accent."""
    from plotnine import geom_col

    tokens = _resolve(palette)
    _refuse_fixed_claim(mapping, claim, "fill")
    if claim:
        kwargs.setdefault("fill", tokens.accent)
    kwargs.setdefault("width", BAR_WIDTH)
    geom = geom_col(mapping=mapping, data=data, **kwargs)
    defaults = {"size": BAR_EDGE}
    if not claim and not _has_param(geom, "fill"):
        defaults["fill"] = tokens.ink_soft
    if not _has_param(geom, "color", "colour"):
        defaults["color"] = tokens.white
    geom = _with_defaults(geom, **defaults)
    if claim:
        _guard_plot_mapping(geom, "fill")
    return geom


def area(mapping=None, data=None, *, palette: str | Palette | None = None, claim: bool = True, **kwargs):
    """Magnitude under a curve: accent fill at 0.35, ink line on top.

    ``claim=True`` (the default) is a fixed accent and raises if the geom or
    the plot already maps fill. ``claim=False`` leaves a mapped fill alone.
    """
    from plotnine import geom_area

    tokens = _resolve(palette)
    _refuse_fixed_claim(mapping, claim, "fill")
    if claim:
        kwargs.setdefault("fill", tokens.accent)
    geom = geom_area(mapping=mapping, data=data, **kwargs)
    defaults = {"alpha": AREA_ALPHA, "size": AREA_LINE}
    if not claim and not _has_param(geom, "fill"):
        defaults["fill"] = tokens.ink_soft
    if not _has_param(geom, "color", "colour"):
        defaults["color"] = tokens.ink
    geom = _with_defaults(geom, **defaults)
    if claim:
        _guard_plot_mapping(geom, "fill")
    return geom


def band(mapping=None, data=None, *, palette: str | Palette | None = None, **kwargs):
    """Highlight window. Accent at alpha 0.12, no stroke."""
    from plotnine import geom_ribbon

    tokens = _resolve(palette)
    geom = geom_ribbon(mapping=mapping, data=data, **kwargs)
    defaults = {"alpha": BAND_ALPHA}
    if not _has_param(geom, "fill"):
        defaults["fill"] = tokens.accent
    if not _has_param(geom, "color", "colour"):
        defaults["color"] = "none"
    return _with_defaults(geom, **defaults)
