# ADR 0006 — Geometry stays a plotnine layer

**Status:** accepted  
**Date:** 19 October 2026

## Context

0.1.0 wrapped chrome: `theme_aesth`, `GT_aesth`, `css_aesth`. The house rules for marks — line width 2.4, round caps, bar width 0.85, area alpha 0.35, band alpha 0.12, one accent claim, five series — lived only in [HOUSE_STYLE.md](../design/HOUSE_STYLE.md). A caller could add the theme and still draw a default plotnine line.

The palette etude in `studies/palette_etude.py` is a separate approval surface. It is not this decision.

## Options

1. Document the numbers and leave every chart to set them by hand.
2. Ship new geom classes that subclass plotnine.
3. **Return ordinary plotnine geoms with the house defaults already filled, and add the theme plus scales through one `+` object.**

## Choice

Option 3.

- `line`, `point`, `col`, `area`, `band` call `geom_*`. House colour and size sit on the geom's `DEFAULT_AES`, so a colour mapped on the plot still wins. `claim=True` is a fixed accent and overrides that mapping.
- `colour_map` / `scale_*_aesth(claim=, levels=)` put `accent` on one named level. Six levels raise.
- `dress` is added with `+`, the same way a theme is. `finish` is the functional form. `save` calls plotnine `ggplot.save` at 220 dpi with a tight bbox (S19).

## Consequences

- The grammar remains plotnine. There is no second chart engine.
- A mapped colour is not overwritten. The claim for a multi-series figure goes through `dress`, not through `line(claim=True)`.
- Etude palettes (salon, veranda, nocturne, and the rest) stay out of `PALETTES` until a later freeze. The registry is still the eight names from ADR 0005.
- Great Tables and Shiny are unchanged in this step.

## Links

[HOUSE_STYLE.md](../design/HOUSE_STYLE.md) · [0001-stack.md](0001-stack.md) · [0005-freeze.md](0005-freeze.md) · [SOURCES.md](../SOURCES.md) S19
