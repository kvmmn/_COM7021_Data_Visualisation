"""Named palette registry. One active palette at a time."""

from __future__ import annotations

from aesth.tokens import Palette

# arden is locked to the COM7021 visual guide. Do not restyle.
_ARDEN = Palette(
    name="arden",
    ink="#002B49",
    accent="#66C9BA",
    accent_deep="#3AA89A",
    ink_soft="#1A4A6B",
    support="#0E7C8B",
    mist="#E6F5F2",
    paper="#F7FAFB",
    white="#FFFFFF",
    mute="#5A6B75",
    grid="#D5DEE3",
    line="#C9D5DD",
)

# Graphite structure, oxidised-brass claim. Near identity chrome, not a copy.
_CARBON = Palette(
    name="carbon",
    ink="#1B1916",
    accent="#C4A36A",
    accent_deep="#6F5324",
    ink_soft="#3A3530",
    support="#5C554C",
    mist="#EFEAE2",
    paper="#F5F2EB",
    white="#FFFFFF",
    mute="#5C564E",
    grid="#DDD7CD",
    line="#CFC8BC",
)

# Archival bone paper, iron-oxide marginalia.
_VELLUM = Palette(
    name="vellum",
    ink="#2A2118",
    accent="#C06A3A",
    accent_deep="#7A3C1E",
    ink_soft="#4A3A28",
    support="#6E5840",
    mist="#F2E8D6",
    paper="#F6F0E2",
    white="#FFFDF8",
    mute="#5C4F3C",
    grid="#E5D9C4",
    line="#D8CBB4",
)

# Cool museum black, glacial claim. Light canvas for print.
_OBSIDIAN = Palette(
    name="obsidian",
    ink="#14181E",
    accent="#8BB8C8",
    accent_deep="#2F5C6C",
    ink_soft="#2C3540",
    support="#4A5864",
    mist="#E6EDF1",
    paper="#F3F5F7",
    white="#FFFFFF",
    mute="#54606A",
    grid="#D3DBE1",
    line="#C4CDD4",
)

# Graphite with a rare mineral-red claim. Not hazard-tape red.
_CINNABAR = Palette(
    name="cinnabar",
    ink="#1C1917",
    accent="#C24732",
    accent_deep="#7A2A1E",
    ink_soft="#3A332E",
    support="#6A5348",
    mist="#F4EBE7",
    paper="#F6F3F0",
    white="#FFFFFF",
    mute="#5A534E",
    grid="#E0D8D2",
    line="#D2C8C1",
)

# Olive and moss. Cultivated landscape, not recycling-bin green.
_CHLORIS = Palette(
    name="chloris",
    ink="#1C2418",
    accent="#8A9648",
    accent_deep="#3E4A1E",
    ink_soft="#33402A",
    support="#5A6840",
    mist="#EEF0E4",
    paper="#F4F5EE",
    white="#FFFFFF",
    mute="#545C4C",
    grid="#DBDFD2",
    line="#CDD2C4",
)

# Dried violet and umber. Laboratory stain, not brand-purple glow.
_IODINE = Palette(
    name="iodine",
    ink="#241C22",
    accent="#8A5A68",
    accent_deep="#4A2E38",
    ink_soft="#3A2C34",
    support="#6A4A40",
    mist="#F0E8EB",
    paper="#F6F2F3",
    white="#FFFFFF",
    mute="#5A5056",
    grid="#E0D6DA",
    line="#D2C6CB",
)

# Near-monochrome. Warm ivory is the only chromatic permission.
_NOIR = Palette(
    name="noir",
    ink="#1A1A1A",
    accent="#C8B896",
    accent_deep="#5C5646",
    ink_soft="#3D3D3D",
    support="#5C5C5C",
    mist="#EEEEEA",
    paper="#F4F4F1",
    white="#FFFFFF",
    mute="#555555",
    grid="#DDDDD8",
    line="#CECEC8",
)

PALETTES: dict[str, Palette] = {
    "arden": _ARDEN,
    "carbon": _CARBON,
    "vellum": _VELLUM,
    "obsidian": _OBSIDIAN,
    "cinnabar": _CINNABAR,
    "chloris": _CHLORIS,
    "iodine": _IODINE,
    "noir": _NOIR,
}

DEFAULT_PALETTE = "arden"
_active_name = DEFAULT_PALETTE


def _require(name: str) -> Palette:
    try:
        return PALETTES[name]
    except KeyError as exc:
        known = ", ".join(PALETTES)
        raise KeyError(f"unknown palette {name!r}; choose from: {known}") from exc


def use(name: str) -> Palette:
    """Set the process-wide active palette. Default is ``arden``."""
    global _active_name
    chosen = _require(name)
    _active_name = chosen.name
    return chosen


def get_palette(name: str | None = None) -> Palette:
    """Return a named palette, or the active one when ``name`` is omitted."""
    if name is None:
        return PALETTES[_active_name]
    return _require(name)


def palette() -> Palette:
    """Return the active palette."""
    return get_palette()
