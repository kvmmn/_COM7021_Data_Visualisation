import pytest

from aesth.claim import colour_map
from aesth.palettes import get_palette


def test_claim_receives_accent_and_order_is_kept():
    tokens = get_palette("cinnabar")
    mapping = colour_map(["York", "Leeds", "Hull"], "Leeds", "cinnabar")
    assert list(mapping) == ["York", "Leeds", "Hull"]
    assert mapping["Leeds"] == tokens.accent
    assert mapping["York"] == tokens.ink
    assert mapping["Hull"] == tokens.accent_deep


def test_sixth_series_is_refused():
    with pytest.raises(ValueError, match="categorical series"):
        colour_map(["a", "b", "c", "d", "e", "f"], "a", "noir")


def test_claim_must_be_one_of_the_levels():
    with pytest.raises(ValueError, match="not in levels"):
        colour_map(["Leeds"], "York", "arden")
