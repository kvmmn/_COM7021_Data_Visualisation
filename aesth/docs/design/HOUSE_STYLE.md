# House style

Geometry and reduction. Colour lives in the [palette registry](palettes/README.md). Brand chrome lives in [CREATIVE_DIRECTION.md](../brand/CREATIVE_DIRECTION.md).

Derived from the COM7021 visual design guide (S10) and the æsth brief (S11). Where they conflict on **hue**, palettes win. Where they conflict on **reduction**, this page wins.

## Principles

- The prose carries the argument. The figure carries one visual job.
- Short labels inside the artwork. Interpretation sits in the caption.
- One highlight. `accent` marks the claim. `ink` is structure. Everything else stays quiet.
- British English in labels when the audience is this module (`visualisation`, `colour`).
- Refuse: purple glow, rainbow categorical palettes, 3D, heavy gradients, dual y-axes, pie/donut/radar, chartjunk.

## Semantic tokens (every palette must fill these)

| Role | Job |
|---|---|
| `ink` | Titles, axes, primary series, dark headers |
| `accent` | The claim: highlight series, emphasis stroke |
| `accent_deep` | Secondary emphasis, recommended headers, markers |
| `ink_soft` | Alternate series |
| `support` | Third categorical only |
| `mist` | Lane / zebra / soft fill |
| `paper` | Plot canvas |
| `white` | Cards, bar edges |
| `mute` | Ticks, secondary text |
| `grid` | Chart grid |
| `line` | Diagram strokes |
| `series` | Five categorical colours; `accent` last so it can still highlight |

Identity-only (docs, mark, monochrome icon — not a data series): `#151515`, `#F1F0EB`, `#989898`.

## Type

Charts and diagrams share one grotesk. COM7021 figures use **Microsoft Aptos** (Regular 400, SemiBold 600, Bold 700). Public builds may substitute a documented neo-grotesk later; silent fallback to DejaVu is a fail. Matplotlib’s SVG path converter can double the last Aptos glyph — raster plotnine PNGs are fine; posters go through live SVG text and `rsvg-convert`.

Chart scale: title 13 pt bold `ink`; axis 11 pt semibold `ink`; ticks 10 pt `mute`; legend 9 pt, no frame.

Diagram scale: card title 14 px 600; dark header 13 px 600 white; qualifier 10–11 px `mute`; chips 10–12 px 700 white; lane title 12 px 700 `ink`.

Titles are noun phrases: “Mean half-hourly demand by region”. Not a sentence that restates the axes.

## Chart geometry

- Figure about `(10.5, 5.2)` for lines, `(10.5, 5.0)` for bars.
- Face white; axes `paper`; top and right spines off; remaining spines `grid`.
- Horizontal grid only, behind the data.
- `savefig` 220 dpi, tight bbox, 0.25 in pad.
- Line width ~2.4, round caps. No markers on a line unless a second encoding (e.g. weekend points).
- Bars: width 0.85, white edges; default `ink_soft`; highlight `accent`; labels only on highlighted bars.
- Area: fill `accent` at alpha 0.35, line `ink` on top. Highlight band: `accent` at alpha 0.12.
- Max five series. A sixth means facet or split.

## Diagram geometry

- Canvas `paper`. No title inside the SVG; the caption is the title.
- Corner radii: lane 18, card 12, KPI 14, inner cell 8, pills fully round.
- Shadow: 2 px drop, `ink` at 10% opacity. Not a glow. Lanes take no shadow.
- Default card stroke `line` 1.5; claim path `accent` 1.5–2; structural emphasis `ink` 1.5.
- Default arrows `mute`; claimed flow `accent_deep`.

## Recipes (engine-agnostic)

1. Multi-series line + optional accent window.
2. Single line + point encoding on a subset.
3. Bar with one highlighted state.
4. Line with area fill (magnitude under the curve).
5. Comparison matrix: `ink` headers, one `accent_deep` column, `accent` stroke on claimed cells.
6. KPI strip: one or two tiles with `accent` stroke; the rest quiet.

## Toolchain

| Job | Tool |
|---|---|
| Charts | plotnine → matplotlib PNG |
| Tables | Great Tables → HTML and PNG |
| App | Shiny Express, CSS from the active palette |
| Diagrams | Python SVG → `rsvg-convert` |

No seaborn theme. No Plotly unless a later brief forces hover that plotnine cannot give.
