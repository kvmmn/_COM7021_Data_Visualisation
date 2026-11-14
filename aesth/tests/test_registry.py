"""Contrast contract for the frozen registry. Etude palettes are not in here."""

from aesth.contrast import failures
from aesth.palettes import PALETTES


def test_registry_has_the_frozen_eight():
    assert list(PALETTES) == [
        "arden",
        "carbon",
        "vellum",
        "obsidian",
        "cinnabar",
        "chloris",
        "iodine",
        "noir",
    ]


def test_series_keeps_accent_last():
    for name, tokens in PALETTES.items():
        assert len(tokens.series) == 5, name
        assert tokens.series[-1] == tokens.accent
        assert tokens.series[0] == tokens.ink


def test_required_contrast_except_historical_arden():
    for name, tokens in PALETTES.items():
        missed = failures(tokens.roles)
        if name == "arden":
            pairs = {row["pair"] for row in missed}
            assert pairs == {"white on accent_deep"}
            assert tokens.chip_fill == tokens.ink
        else:
            assert missed == [], name
