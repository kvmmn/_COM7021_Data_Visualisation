"""Geometry invariants: mapping, claim, dress, series limit, save."""

from pathlib import Path

import pandas as pd
import pytest
from matplotlib import font_manager
from plotnine import aes, ggplot

import aesth
from aesth.claim import colour_map
from aesth.fonts import resolve_sans
from aesth.theme import scale_colour_aesth, theme_aesth


def _cities():
    return pd.DataFrame(
        {
            "hour": [1, 2, 1, 2],
            "demand": [10, 12, 8, 9],
            "city": ["Leeds", "Leeds", "York", "York"],
        }
    )


def test_mapped_colour_is_not_stolen():
    frame = _cities()
    plot = ggplot(frame, aes("hour", "demand", color="city")) + aesth.line()
    layer = plot.layers[0]
    assert "color" not in layer.geom.aes_params
    layer._make_layer_mapping(plot.mapping)
    assert layer.mapping["color"] == "city"

    with pytest.raises(ValueError, match="dress"):
        ggplot(frame, aes("hour", "demand", colour="city")) + aesth.line(claim=True)


def test_claim_line_is_accent_when_nothing_is_mapped():
    tokens = aesth.get_palette("carbon")
    layer = aesth.line(claim=True, palette="carbon")
    assert layer.aes_params["color"] == tokens.accent

    frame = _cities().drop(columns="city")
    plot = ggplot(frame, aes("hour", "demand")) + aesth.line(claim=True, palette="carbon")
    assert plot.layers[0].geom.aes_params["color"] == tokens.accent


def test_area_claim_refuses_a_plot_level_fill():
    tokens = aesth.get_palette("arden")
    frame = _cities()
    with pytest.raises(ValueError, match="dress"):
        ggplot(frame, aes("hour", "demand", fill="city")) + aesth.area()

    quiet = ggplot(frame, aes("hour", "demand", fill="city")) + aesth.area(claim=False)
    layer = quiet.layers[0]
    assert "fill" not in layer.geom.aes_params
    assert layer.geom.DEFAULT_AES["fill"] == tokens.ink_soft
    layer._make_layer_mapping(quiet.mapping)
    assert layer.mapping["fill"] == "city"

    plain = ggplot(frame, aes("hour", "demand")) + aesth.area(palette="arden")
    assert plain.layers[0].geom.aes_params["fill"] == tokens.accent


def test_claim_does_not_inherit_when_the_layer_opts_out():
    tokens = aesth.get_palette("arden")
    frame = _cities()
    plot = ggplot(frame, aes("hour", "demand", color="city")) + aesth.line(
        inherit_aes=False, claim=True
    )
    assert plot.layers[0].inherit_aes is False
    assert plot.layers[0].geom.aes_params["color"] == tokens.accent


def test_dress_maps_leeds_to_accent_and_york_to_ink():
    frame = _cities()
    tokens = aesth.get_palette("arden")
    plot = (
        ggplot(frame, aes("hour", "demand", colour="city"))
        + aesth.line()
        + aesth.dress(colour=True, claim="Leeds", levels=["Leeds", "York"])
    )
    scale = plot.scales.get_scales("color")
    assert list(scale.map(["Leeds", "York"])) == [tokens.accent, tokens.ink]


def test_finish_does_not_require_the_caller_to_mutate():
    frame = _cities()
    tokens = aesth.get_palette("arden")
    base = ggplot(frame, aes("hour", "demand", colour="city")) + aesth.line()
    finished = aesth.finish(
        base, colour=True, claim="Leeds", levels=["Leeds", "York"]
    )
    assert base is not finished
    assert base.scales.get_scales("color") is None
    mapped = list(finished.scales.get_scales("color").map(["Leeds", "York"]))
    assert mapped == [tokens.accent, tokens.ink]


def test_six_levels_raise():
    with pytest.raises(ValueError, match="categorical series"):
        colour_map(list("abcdef"), "a")
    with pytest.raises(ValueError, match="categorical series"):
        scale_colour_aesth(values=["#111111"] * 6)

    frame = pd.DataFrame(
        {
            "hour": list(range(6)),
            "demand": list(range(6)),
            "city": list("abcdef"),
        }
    )
    plot = (
        ggplot(frame, aes("hour", "demand", color="city"))
        + aesth.line()
        + scale_colour_aesth()
    )
    with pytest.raises(ValueError, match="categorical series"):
        plot.draw()


def test_empty_levels_and_values_are_refused():
    with pytest.raises(ValueError, match="at least one level"):
        colour_map([], "Leeds")
    with pytest.raises(ValueError, match="at least one"):
        scale_colour_aesth(claim="Leeds", levels=[])
    with pytest.raises(ValueError, match="at least one colour"):
        scale_colour_aesth(values=[])


def test_claim_and_values_cannot_both_be_passed():
    with pytest.raises(ValueError, match="claim or values"):
        scale_colour_aesth(
            values={"Leeds": "#111111"}, claim="Leeds", levels=["Leeds"]
        )


def test_save_sets_dpi_220(monkeypatch, tmp_path: Path):
    frame = _cities()
    plot = ggplot(frame, aes("hour", "demand")) + aesth.line()
    seen: dict = {}

    def fake_save(filename, **kwargs):
        seen["filename"] = filename
        seen["kwargs"] = kwargs
        return "saved"

    monkeypatch.setattr(plot, "save", fake_save)
    target = tmp_path / "figure.png"
    assert aesth.save(plot, target) == "saved"
    assert seen["filename"] == target
    assert seen["kwargs"]["dpi"] == 220
    assert seen["kwargs"]["bbox_inches"] == "tight"
    assert seen["kwargs"]["pad_inches"] == 0.25


def test_theme_figure_size_and_dpi():
    theme = theme_aesth()
    assert theme.getp("figure_size") == (10.5, 5.2)
    assert theme.getp("dpi") == 220


def test_font_resolver_does_not_select_a_display_cut_or_dejavu():
    family, _note = resolve_sans()
    regular = font_manager.findfont(
        font_manager.FontProperties(family=family, weight=400),
        fallback_to_default=False,
    )
    bold = font_manager.findfont(
        font_manager.FontProperties(family=family, weight="bold"),
        fallback_to_default=False,
    )
    for path in (regular, bold):
        name = Path(path).name.lower()
        assert "display" not in name
        assert "dejavu" not in name
