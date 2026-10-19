# Research: plotnine

**Role in aesth:** the chart grammar. We wrap theme and scales. We do not wrap every geom.

Canonical pages: [plotnine.org](https://plotnine.org/) (S01), [Overview](https://plotnine.org/guide/overview.html) (S02).

## Purpose

Plotnine is a Python implementation of the grammar of graphics, with syntax close to ggplot2. Plots are declared as data + aesthetic mappings + layers, not as a sequence of matplotlib artist calls. That is the point: a house theme can sit at the end of the chain and restyle any geom the same way.

## Install (documented)

```text
pip install plotnine
```

Overview notes pandas **and** polars DataFrames, in tidy (longer) form (S02).

## API we will actually use

| Piece | Why |
|---|---|
| `ggplot(data)` + `aes(...)` | Single entry point |
| `geom_line`, `geom_point`, `geom_col` / `geom_bar`, `geom_area`, `geom_histogram`, `geom_boxplot`, `geom_violin`, `geom_smooth`, `geom_tile` | Covers the six COM7021 visualisation *types* without a new engine |
| `facet_wrap` / `facet_grid` | Split instead of a sixth categorical colour |
| `scale_colour_*` / `scale_fill_*` | Bind the active aesth palette |
| `labs`, `coord_*` | Titles as noun phrases; no dual axes |
| `theme_minimal()` as a **base**, then `theme(...)` + `element_line` / `element_text` / `element_rect` / `element_blank` | House chrome: paper canvas, mute ticks, hidden extra spines |
| `ggsave` / `.save()` | PNG for the Word report; Shiny forwards kwargs to `save()` (S07) |

The homepage itself shows the intended path from a one-liner to a branded figure: defaults first, then override colour/size, then `theme_tufte(...)` + `theme(...)` for organisation brand (S01). aesth occupies that last step.

## API we will not wrap

- A parallel matplotlib helper that restyles the same chart a second way
- Seaborn (would fight the theme)
- Plotly traces (assignment does not require them; Shiny already rasterises plotnine)
- Custom geom classes in v0
- Dual y-axis coordinate helpers

## Fit to æsth

Plotnine draws on matplotlib, so Aptos (or a documented grotesk) and PNG export already work. The house geometry in `HOUSE_STYLE.md` maps cleanly:

- Horizontal grid only → `panel_grid_major_x=element_blank()`, y-grid in `grid` token
- Paper axes face → `panel_background=element_rect(fill=paper)`
- Series order of five → `scale_colour_manual(values=palette.series)`
- One highlight → map a boolean or a rule to `accent`, leave the rest on `ink` / `ink_soft`

The homepage Anscombe example is the first proof candidate: four facets, one accent for points, ink for the smooth, no rainbow legend once faceted (S01).

## Risks

- Default palettes are not ours. Forgetting `scale_*` after `theme_aesth()` would leak viridis / default hues onto a “house” figure.
- `theme_tufte` is a reference, not a dependency of our look. We start from `theme_minimal` plus explicit elements so paper/mist/grid stay exact.
- Font: if Aptos is missing, plotnine will silently substitute. That is a fail, not a fallback, until a documented grotesk is chosen for public builds.

## Worked example (prose, before code)

Anscombe quartet, lesson file already in the parent repo. One `ggplot` + `geom_point` + `geom_smooth(method="lm")` + `facet_wrap("dataset")` + `theme_aesth("arden")`. Title: “Anscombe’s quartet”. No in-plot essay. The report caption carries the statistical joke.
