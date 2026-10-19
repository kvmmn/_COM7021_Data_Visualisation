# Who owns which job

aesth is a **language layer**. The three libraries keep their engines. This page is the ownership map so we do not rebuild what already exists.

| Job | Owner | aesth adds | We refuse |
|---|---|---|---|
| Grammar of charts (layers, facets, scales) | [plotnine](https://plotnine.org/) | `theme_aesth(palette)`, `scale_*_aesth` | A second matplotlib style path; seaborn; Plotly traces |
| Publication tables | [Great Tables](https://posit-dev.github.io/great-tables/) | `GT_aesth(df, palette=...)` chrome, highlight column, fmt defaults | DataGrid as the manager table; rainbow cell heatmaps |
| Reactive dashboard | [Shiny for Python](https://shiny.posit.co/py/) | CSS variables + value-box theme from the active palette | shinyswatch / Bootswatch; indigo–purple gradients |
| Structural diagrams (lanes, matrices, KPI strips that are not geoms) | Hand SVG (existing COM7021 studies) | Same semantic tokens as the active palette | Drawing architecture in plotnine |
| Colour | aesth palette registry | Named token sets the user can switch | One locked hue family for the whole product |
| Argument / caption | The report, not the figure | Noun-phrase titles only | Sentences baked into PNG |

## Why this split

- Plotnine already sits on matplotlib, and Shiny’s `@render.plot` already accepts plotnine ([overview](https://shiny.posit.co/py/docs/overview.html)). No adapter library is required.
- Great Tables already exports HTML (for the app) and images (for Word). That is the report + dashboard table path.
- Shiny is a permitted “other suitable Python framework” in the COM7021 brief. Dash/Streamlit/Panel/Bokeh are alternatives, not requirements.
- Identity chrome (`#151515` / `#F1F0EB`) is brand, not data. Data marks come from the **active palette**.

## Default path for COM7021 EcoMove

`palette="arden"` on charts, tables, and the Shiny page, so the assignment screenshots match the existing visual guide. Other palettes are for the public gallery and later work.

## Sources

See [SOURCES.md](../SOURCES.md) S01–S12.
