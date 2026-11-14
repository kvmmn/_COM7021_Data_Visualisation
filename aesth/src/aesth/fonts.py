"""Resolve a grotesk. Never silently fall back to DejaVu."""

from __future__ import annotations

from pathlib import Path

# Documented public-build substitutes if Microsoft Aptos is absent.
GROTESK_FALLBACKS: tuple[str, ...] = (
    "IBM Plex Sans",
    "Inter",
    "Source Sans 3",
    "Source Sans Pro",
    "Helvetica Neue",
)

_FORBIDDEN_SILENT = frozenset({"DejaVu Sans", "DejaVu Serif", "DejaVu Sans Mono"})


def available_families() -> set[str]:
    from matplotlib import font_manager

    return {face.name for face in font_manager.fontManager.ttflist}


def _drop_display_aliases(family: str) -> None:
    """Keep the text cut when a display face is also registered under ``family``.

    Aptos Display ships with the family name Aptos as well as Aptos Display.
    Matplotlib's matcher treats those as a tie and can return Aptos Display
    for regular text. Drop only the display files that claim the text family.
    Aptos Display remains available under its own name.
    """
    from matplotlib import font_manager

    manager = font_manager.fontManager
    kept = []
    dropped = False
    for face in manager.ttflist:
        stem = Path(face.fname).name.lower()
        if face.name == family and "display" in stem:
            dropped = True
            continue
        kept.append(face)
    if not dropped:
        return
    manager.ttflist[:] = kept
    manager._findfont_cached.cache_clear()


def resolve_sans() -> tuple[str, str]:
    """Return ``(family, note)``.

    Aptos if installed. Otherwise a documented grotesk. Raises if the only
    available faces would be a silent DejaVu substitution.

    Matplotlib's SVG path converter can double the last Aptos glyph. Proof
    posters therefore go through ``rsvg-convert`` with live SVG text. Plotnine
    PNG output uses matplotlib's raster text path and is fine.
    """
    names = available_families()
    if "Aptos" in names:
        _drop_display_aliases("Aptos")
        return "Aptos", "Aptos"
    for family in GROTESK_FALLBACKS:
        if family in names:
            _drop_display_aliases(family)
            note = (
                f"Aptos is not installed; using documented grotesk {family!r}. "
                "Install Microsoft Aptos (Microsoft 365) for the preferred grotesk."
            )
            return family, note
    raise RuntimeError(
        "Aptos is not installed and no documented grotesk was found "
        f"({', '.join(GROTESK_FALLBACKS)}). Silent DejaVu fallback is not allowed."
    )


def font_stack() -> list[str]:
    family, _note = resolve_sans()
    stack = [family, *GROTESK_FALLBACKS, "system-ui", "sans-serif"]
    seen: list[str] = []
    for item in stack:
        if item not in seen and item not in _FORBIDDEN_SILENT:
            seen.append(item)
    return seen
