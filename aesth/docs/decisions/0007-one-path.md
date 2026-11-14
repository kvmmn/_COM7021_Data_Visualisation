# ADR 0007 — One path across the three libraries

**Status:** accepted  
**Date:** 19 October 2026

## Context

0.2.0 could theme a plotnine figure, a Great Table, and a Shiny page, but the app still pasted `ui.tags.style` by hand, tables left missing values and thousands separators to every caller, and nothing checked that `import aesth` stayed light. The product is still a wrapper. It is not a fourth charting engine.

The palette etude in `studies/palette_etude.py` is a separate approval surface. It is not this decision.

## Options

1. Import plotnine, Great Tables, and Shiny at package import and hang a facade object off `aesth`.
2. Ship a page class that owns layout, geoms, and table drawing.
3. **Keep the three imports lazy. Add `page_aesth` for the Shiny shell, call Great Tables' own `fmt_*` and `sub_missing` from `GT_aesth`, and test that importing aesth does not load the three libraries.**

## Choice

Option 3.

- `page_aesth(palette, title=)` returns `ui.tags.style(css_aesth(...))`. Inside Shiny Express, `title` is passed to `page_opts` (S21). Outside Express, including a headless test, the style tag is still returned. shinyswatch is not imported. Value boxes stay flat: `background-image: none`, with `.aesth-claim` as a solid accent border.
- A plotnine figure and a Great Table share that palette: `@render.plot` plus `theme_aesth` or `dress`, and `ui.HTML(GT_aesth(..., palette=same).as_raw_html())`.
- `GT_aesth(..., quiet=True)` calls `fmt_integer` on integer columns, `fmt_number(decimals=2)` on other numeric columns, and `sub_missing` (default `&mdash;`, S20). `highlight_column` is still the only highlight. No cell heatmap. Heading text stays white through the existing `tab_style` workaround; Great Tables has no `heading_title_font_color`.
- The caller's frame is passed to `GT` as given. CSS is a string built once per call. It is not an attribute that rebuilds on access, and the helpers do not re-run a contrast audit while assembling that string.

## Consequences

- `import aesth` does not import plotnine, great_tables, or shiny. A subprocess test checks `sys.modules`.
- Callers who want raw cell text pass `quiet=False`. A later `fmt_*` still reads the original values, because that is how Great Tables applies formats (S20).
- Etude palettes stay out of `PALETTES` until a later freeze. The registry is still the eight names from ADR 0005.
- No new dependency. Matplotlib remains the raster engine through plotnine.

## Links

[0001-stack.md](0001-stack.md) · [0006-marks.md](0006-marks.md) · [COMPARISON.md](../research/COMPARISON.md) · [SOURCES.md](../SOURCES.md) S04, S08, S20, S21
