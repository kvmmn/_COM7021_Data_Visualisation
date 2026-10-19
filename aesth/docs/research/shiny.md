# Research: Shiny for Python

**Role in aesth:** the interactive shell. We wrap CSS variables, value boxes, and layout chrome. We do not wrap a second reactive runtime.

Canonical pages: [Shiny for Python](https://shiny.posit.co/py/) (S05), [Overview](https://shiny.posit.co/py/docs/overview.html) (S06), [`render.plot`](https://shiny.posit.co/py/api/core/render.plot.html) (S07), [UI customise](https://shiny.posit.co/py/docs/ui-customize.html) (S08), [Value box](https://shiny.posit.co/py/components/outputs/value-box/) (S09).

## Purpose

Shiny builds reactive web apps in pure Python. The engine recomputes only outputs whose upstream inputs changed (S05). It sits on Starlette and asyncio, so it is a real web stack, not a notebook slideshow. The COM7021 brief asks for an interactive dashboard and names Dash, Streamlit, Panel, Bokeh, **or another suitable Python framework**. Shiny is that other framework (S12).

## Install (documented)

```text
uv pip install shiny
uvx shiny create --template dashboard-tips
```

aesth will not ship that template’s look. The template is only evidence that dashboard layout is a supported path (S05).

## API we will actually use

| Piece | Why |
|---|---|
| `shiny.express` for the first apps | Less boilerplate while the theme is proven (S06) |
| `ui.input_selectize` / slider / date | Filters for city, mode, date — the brief’s dashboard job |
| `@render.plot` | Plotnine figures as PNG (`save()` kwargs) (S06, S07) |
| `ui.HTML(...)` with GT `as_raw_html()` | Display tables, not DataGrid spreadsheets |
| `ui.value_box` | KPI strip; **custom theme**, not the indigo–purple sample (S09) |
| `ui.include_css` or CSS variables on the page | Map `--bs-primary` and canvas colours to the active palette (S08) |
| `ui.layout_sidebar` / cards / fillable page | Quiet structure, not a dense icon dashboard |

## API we will not wrap

- **shinyswatch / Bootswatch** as the look. Convenient and wrong: Darkly and friends are generic SaaS skins (S08). The creative brief forbids that register.
- Sample value-box theme `bg-gradient-indigo-purple` (S09). Gradients and purple glow are explicit house-style refusals.
- Plotly via `shinywidgets` unless a geom plotnine cannot draw is required. It is not required for the six COM7021 types.
- `@render.data_frame` as the primary table. That is an explorer grid. Managers get Great Tables.

## Fit to æsth

Shiny is HTML. Identity colours (`#151515`, `#F1F0EB`) may clothe the **docs site and app chrome**. Data marks still come from the active palette. A page can be carbon-paper while the charts use `arden` only if we document that split; the default is **one active palette for chrome + data** so a screenshot looks like one system.

`@render.plot` already names plotnine as a first-class matplotlib-compatible source (S06). That is the technical reason the three-library merge is not a fantasy adapter.

## Risks

- Express vs Core: Express is faster to sketch; Core may be needed if we publish a reusable page function. Decision deferred to the Shiny sprint; first proof uses Express.
- CSS variable coverage is not complete for every component. Value boxes and sidebars may need targeted rules, not only `--bs-primary`.
- Raster plots inside a reactive app can feel static. Filters must change the **data**, not fake interactivity with Plotly hover as a substitute for a decision-maker control.

## Worked example (prose, before code)

One sidebar filter (dataset or city), one plotnine facet, one GT HTML table, three value boxes using `ink` / `accent` / `paper`. No Bootswatch. That is the theme proof. EcoMove comes after.
