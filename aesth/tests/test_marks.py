"""House geoms stay plotnine layers and do not override a mapped colour."""

import pandas as pd
import pytest
from plotnine import aes, ggplot, labs

import aesth
from aesth.marks import AREA_ALPHA, BAND_ALPHA, BAR_WIDTH, LINE_SIZE


def _aes_params(layer):
    return dict(layer.aes_params)


def test_line_uses_house_width_without_stealing_a_mapping():
    layer = aesth.line(aes("hour", "demand", color="city"), palette="arden")
    assert layer.__class__.__name__ == "geom_line"
    assert "color" not in layer.aes_params
    assert layer.DEFAULT_AES["size"] == LINE_SIZE
    assert layer.DEFAULT_AES["color"] == aesth.get_palette("arden").ink
    assert layer.params["lineend"] == "round"


def test_claim_on_a_mapped_line_is_refused():
    with pytest.raises(ValueError, match="dress"):
        aesth.line(aes("hour", "demand", color="city"), claim=True)


def test_unmapped_claim_line_is_accent():
    tokens = aesth.get_palette("carbon")
    layer = aesth.line(claim=True, palette="carbon")
    assert _aes_params(layer)["color"] == tokens.accent


def test_column_defaults():
    tokens = aesth.get_palette("arden")
    layer = aesth.col(palette="arden")
    assert layer.DEFAULT_AES["fill"] == tokens.ink_soft
    assert layer.DEFAULT_AES["color"] == tokens.white
    assert layer.params["width"] == BAR_WIDTH


def test_area_and_band_alphas():
    assert aesth.area().DEFAULT_AES["alpha"] == AREA_ALPHA
    assert aesth.band().DEFAULT_AES["alpha"] == BAND_ALPHA


def test_plot_mapping_is_not_replaced_by_a_fixed_ink():
    frame = pd.DataFrame(
        {
            "hour": [1, 2, 1, 2],
            "demand": [10, 12, 8, 9],
            "city": ["Leeds", "Leeds", "York", "York"],
        }
    )
    plot = ggplot(frame, aes("hour", "demand", color="city")) + aesth.line()
    layer = plot.layers[0]
    assert "color" not in layer.geom.aes_params
    layer._make_layer_mapping(plot.mapping)
    assert "color" in layer.mapping


def test_dress_attaches_theme_and_claim_scale():
    frame = pd.DataFrame(
        {
            "hour": [1, 2, 3, 1, 2, 3],
            "demand": [10, 12, 11, 8, 9, 13],
            "city": ["Leeds", "Leeds", "Leeds", "York", "York", "York"],
        }
    )
    plot = (
        ggplot(frame, aes("hour", "demand", color="city"))
        + aesth.line()
        + labs(title="Mean demand by city")
        + aesth.dress(colour=True, claim="Leeds", levels=["Leeds", "York"])
    )
    assert plot.theme is not None
    scale = plot.scales.get_scales("color")
    assert scale is not None
    tokens = aesth.get_palette("arden")
    mapped = list(scale.map(["Leeds", "York"]))
    assert mapped == [tokens.accent, tokens.ink]


def test_import_does_not_require_plotnine_for_tokens():
    assert aesth.__version__ == "0.3.0"
    assert aesth.palette().name == "arden"
