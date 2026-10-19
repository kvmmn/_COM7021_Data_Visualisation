# Source ledger

Fetched 19 October 2026 unless noted. Do not cite a URL that is not in this file.

| ID | URL | What was extracted | Used in |
|---|---|---|---|
| S01 | https://plotnine.org/ | Grammar of graphics for Python; ggplot2-like syntax; layers, facets, defaults, `theme()` / `theme_tufte` brand override; Anscombe walkthrough | research/plotnine.md, COMPARISON.md |
| S02 | https://plotnine.org/guide/overview.html | `ggplot()` + tidy frames; `aes()`; `geom_*`; `scale_*`; `facet_*`; `coord_*`; `theme_*` vs `theme()` + `element_*`; pandas and polars | research/plotnine.md |
| S03 | https://posit-dev.github.io/great-tables/ | Display tables vs DataFrames; chain from `GT()`; header, format, style; HTML / LaTeX / image export; `pip install great_tables`; Python >= 3.10 | research/great-tables.md |
| S04 | https://posit-dev.github.io/great-tables/reference/ | `tab_header`, stub, spanners, footnotes, source notes, `tab_style`, `tab_style_body`, `tab_options`, `opt_stylize`, `fmt_*` | research/great-tables.md |
| S05 | https://shiny.posit.co/py/ | Reactive Python apps; Starlette + asyncio; CSS/JS customisation; `uv pip install shiny` | research/shiny.md |
| S06 | https://shiny.posit.co/py/docs/overview.html | `shiny.express`; `@render.plot` accepts matplotlib **and plotnine**; `@render.data_frame` / DataGrid; inputs `ui.input_*` | research/shiny.md, 0001-stack.md |
| S07 | https://shiny.posit.co/py/api/core/render.plot.html | Plot rendered as HTML image; kwargs forwarded to matplotlib `savefig` or plotnine `save` | research/shiny.md |
| S08 | https://shiny.posit.co/py/docs/ui-customize.html | shinyswatch Bootswatch themes; `ui.tags.style`; `ui.include_css`; inline styles; Bootstrap utilities; **CSS variables** (`--bs-primary-rgb`) | research/shiny.md, 0001-stack.md |
| S09 | https://shiny.posit.co/py/components/outputs/value-box/ | Value box: title, value, showcase, theme; sample uses `bg-gradient-indigo-purple` (rejected for aesth) | research/shiny.md |
| S10 | COM7021 visual design guide (local) `COM7021 - Assignment/VISUAL_DESIGN_GUIDE.md` | Geometry, Aptos, midnight/tiffany tokens, chart and diagram recipes | HOUSE_STYLE.md, palettes/arden.md |
| S11 | `aesth/aesth — Creative Direction Brief.md` | Name, ligature, identity colours `#151515` / `#F1F0EB` / `#989898`, philosophy | 0002-name.md, HOUSE_STYLE.md |
| S12 | COM7021 assessment statement (local PDF, not redistributed) | Six visualisation types + interactive dashboard; Python; frameworks listed including “another suitable” option | 0001-stack.md |

| S13 | https://www.w3.org/TR/WCAG22/#dfn-relative-luminance | WCAG 2.2 relative luminance (sRGB, 0.03928) and contrast-ratio formula | contrast.py, 0005-freeze.md |
| S14 | https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio | Contrast ratio `(L1 + 0.05) / (L2 + 0.05)` | contrast.py |
| S15 | https://plotnine.org/reference/theme.html | plotnine 0.15 `theme()` themeables | theme.py |
| S16 | https://plotnine.org/reference/theme_minimal.html | `theme_minimal(base_size, base_family)` | theme.py |
| S17 | https://posit-dev.github.io/great-tables/reference/GT.tab_options.html | Live `tab_options` field names (heading/column/body/stripe) | tables.py |
| S18 | https://posit-dev.github.io/great-tables/user-guide/table-theme-options.html | Worked `tab_options` examples | tables.py |

Pages requested but not found on 19 Oct 2026: `plotnine.org/guide/themes.html`, `posit-dev.github.io/great-tables/get-started/table-styling.html`. `user-guide/table-theme-options.html` resolved later the same day (S18).
