# ADR 0005 — Palette hex freeze and contrast method

**Status:** accepted  
**Date:** 19 October 2026

## Context

ADR 0004 reserved eight named palettes and froze only `arden`. The theme sprint needs real hex in one module so plotnine, Great Tables, and Shiny cannot drift. Guessed hex without WCAG maths would violate the house refusal of “pretty first”.

## Options

1. Keep reserved names and invent hex inside each theme helper.
2. Copy ColorBrewer / Tableau / viridis stops into the registry.
3. **Hand-curate eight token sets, measure WCAG 2.2 contrast in `aesth.contrast`, freeze in `aesth.palettes`.**

## Choice

Option 3.

Relative luminance and contrast ratio follow WCAG 2.2 definitions (S13): sRGB linearisation at 0.03928, ratio `(L1 + 0.05) / (L2 + 0.05)`. The freeze script `scripts/freeze_palettes.py` prints every required pair.

Targets:

- `ink` on `paper` ≥ 7:1
- `mute` on `paper` ≥ 4.5:1
- white on `ink` ≥ 7:1
- white on `accent_deep` ≥ 4.5:1

White on `accent` is reported, not required. When it misses AA, `Palette.chip_fill` is `accent_deep`. When that also misses — historically frozen `arden` tiffany-deep at 2.90:1 — chips use `ink`. Accent stays a fill and stroke.

`arden` hex is unchanged from the COM7021 visual guide (S10). The other seven names were designed as distinct hue families (graphite-brass, bone-oxide, glacial, mineral red, olive, iodine stain, ivory-on-grey), not as restyles of midnight/tiffany.

## Consequences

- `aesth.use("name")` is process-wide. Default remains `arden`.
- Geometry does not change when the palette changes.
- Proofs live in `studies/`. A later ninth palette needs the same contrast table and a poster row.
- Identity chrome (`#151515` / `#F1F0EB` / `#989898`) is still not a data series.

## Links

[0004-palettes.md](0004-palettes.md) · [palettes/README.md](../design/palettes/README.md) · [SOURCES.md](../SOURCES.md) S10, S13
