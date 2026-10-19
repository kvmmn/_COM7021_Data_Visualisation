# ADR 0001 — Three-library stack

**Status:** accepted  
**Date:** 19 October 2026

## Context

COM7021 requires Python visualisations, at least six distinct chart types, and one interactive dashboard. The course visual guide already locks geometry (one job per figure, one highlight, quiet chrome). We need engines that can carry that geometry into print (Word screenshots) and into a reactive app, without writing a new grammar.

## Options

1. Matplotlib + custom SVG + Streamlit (closest to the old COM7020 toolchain; dashboard listed in the brief).
2. Plotly Dash for charts and app (listed in the brief; interactive, but fights the house refusal of default “AI chart” chrome).
3. **plotnine + Great Tables + Shiny** (grammar + display tables + reactive shell).
4. Build geoms ourselves on matplotlib.

## Choice

Option 3.

- Plotnine is the grammar; themes and scales are the wrap points ([plotnine.org](https://plotnine.org/)).
- Great Tables is display output, not a DataFrame ([Great Tables](https://posit-dev.github.io/great-tables/)).
- Shiny `@render.plot` already rasterises plotnine ([overview](https://shiny.posit.co/py/docs/overview.html)); CSS variables can carry the active palette ([UI customise](https://shiny.posit.co/py/docs/ui-customize.html)).
- The brief’s named frameworks are examples; “another suitable Python-based visualisation framework” covers Shiny.

## Consequences

- We depend on three upstream APIs. Pin versions in `pyproject.toml` when theme code lands.
- We do not vendor or fork them.
- Shinyswatch is available and rejected (generic Bootswatch).
- Matplotlib remains the raster engine *through* plotnine, not as a parallel house API.
- Hand SVG remains for non-data diagrams.

## Links

[COMPARISON.md](../research/COMPARISON.md) · [SOURCES.md](../SOURCES.md) S01–S09, S12
