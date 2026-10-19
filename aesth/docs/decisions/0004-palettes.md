# ADR 0004 — Palettes as a user-selectable registry

**Status:** accepted  
**Date:** 19 October 2026

## Context

The COM7021 visual guide locked a single Arden pair (midnight / tiffany). That is correct for the assignment screenshots. It is too narrow for a public library whose brief says additional accents appear when conceptually necessary, and whose user asked for several high-end palettes.

Brand identity (`#151515` / `#F1F0EB` / `#989898`) is also not a data palette. Mixing them would either make every chart look like the logo, or make the logo look like a dashboard.

## Options

1. One locked data palette (`arden` only).
2. Free-form hex in every call (`theme(colour="#...")`).
3. **Named palettes that all implement the same semantic tokens**, user-selected.

## Choice

Option 3.

Every palette fills the same roles (`ink`, `accent`, `accent_deep`, `ink_soft`, `support`, `mist`, `paper`, `mute`, `grid`, `line`, `series[5]`). plotnine, Great Tables, Shiny CSS, and SVG diagrams read those roles. Switching palettes does not change geometry.

`arden` is the COM7021 default. The other names are now frozen; see [ADR 0005](0005-freeze.md).

## Consequences

- API shape (later): `aesth.use("arden")` or `theme_aesth("vellum")`.
- No sixth categorical colour: facet or split instead.
- One highlight token per figure (`accent`). If everything is accent, nothing is.
- Identity chrome may stay near-black / warm white on the docs site even when data uses `arden`. Apps default to **one active palette for chrome + data** so a screenshot is one system.
- Do not ship seaborn/ColorBrewer dumps. Hand-curated set of six to eight.

## Links

[palettes/README.md](../design/palettes/README.md) · [arden.md](../design/palettes/arden.md) · [HOUSE_STYLE.md](../design/HOUSE_STYLE.md)
