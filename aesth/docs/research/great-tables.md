# Research: Great Tables

**Role in aesth:** publication display tables. We wrap chrome, fonts, and highlight rules. We do not invent a table widget.

Canonical pages: [Great Tables](https://posit-dev.github.io/great-tables/) (S03), [Reference](https://posit-dev.github.io/great-tables/reference/) (S04).

## Purpose

Great Tables distinguishes **display tables** (output for a page, journal, or magazine) from **data tables** (DataFrames you would feed a model). The homepage is explicit: you would not want to use the result as input again (S03). That matches aesth: the table is a figure with type, not a spreadsheet.

## Install (documented)

```text
pip install great_tables
```

Requires Python >= 3.10 (S03).

## API we will actually use

| Piece | Why |
|---|---|
| `GT(df)` | Chain root; optional stub / row groups |
| `tab_header(title, subtitle)` | Noun-phrase title, one-line qualifier |
| `tab_stub` / `tab_stubhead` | Row identity without repeating a first column header badly |
| `tab_spanner` | Group measures (demand / reliability / cost) |
| `fmt_number`, `fmt_integer`, `fmt_percent`, `fmt_currency` | Units in the format, not in every cell as prose |
| `tab_source_note`, `tab_footnote` | Citation and caveats below, not inside cells |
| `tab_style` / `tab_style_body` | One accent column or exception rows |
| `tab_options` / `opt_stylize` | Fonts, header fill, table width — bound to the active palette |
| HTML / LaTeX / image export | HTML inside Shiny; PNG/LaTeX for the Word report (S03) |

Homepage example pattern we will keep: header, stub, integer format, source note, nothing else (S03).

## API we will not wrap

- Using GT as a dataframe API
- Rainbow heatmaps across every cell
- Default `opt_stylize()` looks without remapping to aesth tokens (easy to look like a Bootstrap table)
- Multiple simultaneous highlight hues

Nanoplots (inline sparklines in cells) are **in scope later**, not in the first theme sprint. They are a strength of GT and should inherit `ink` / `accent` once the chrome theme is stable. Recorded here so we do not forget them; not implemented until the table theme exists.

## Fit to æsth

The COM7020/7021 comparison-matrix recipe is already a GT: midnight headers, one recommended column in accent-deep, body cells white, accent stroke on the claimed column. `tab_style` can express that without hand SVG.

Identity chrome (`#151515` / `#F1F0EB`) is for documentation pages. Data tables use the **active palette** (`arden` for EcoMove).

## Risks

- HTML in Shiny is a different colour pipeline from PNG export. Both must read the same tokens.
- Header text on `ink` fill must be white (or paper); mute grey on tiffany-like fills fails contrast.
- Polars vs pandas: homepage uses polars; aesth should accept both, matching plotnine (S02, S03).

## Worked example (prose, before code)

A ten-row country or city ranking: stub = name, one integer column, header + source note, `arden` header fill midnight, body paper, no zebra unless it helps a scan. That is enough to prove the theme before EcoMove KPIs.
