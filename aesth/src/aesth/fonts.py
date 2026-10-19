"""Resolve a grotesk. Never silently fall back to DejaVu."""

from __future__ import annotations

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
        return "Aptos", "Aptos"
    for family in GROTESK_FALLBACKS:
        if family in names:
            note = (
                f"Aptos is not installed; using documented grotesk {family!r}. "
                "Install Microsoft Aptos (Microsoft 365) for COM7021 figures."
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
