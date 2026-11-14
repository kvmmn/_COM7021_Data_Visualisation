# æsth

**The aesthetics of data.**

Aesth is a small Python layer that makes [plotnine](https://plotnine.org/), [Great Tables](https://posit-dev.github.io/great-tables/), and [Shiny for Python](https://shiny.posit.co/py/) speak one visual language. It is not a new charting engine. It does not reimplement ggplot, GT, or Shiny.

Product name: **Aesth**. Package: `aesth`. Mark: **æsth**.

## Usage

```python
import pandas as pd
from plotnine import ggplot, aes, facet_wrap, labs

import aesth

aesth.use("arden")          # process-wide; default is arden
print(aesth.palette().ink)  # '#002B49'

from plotnine.data import anscombe_quartet

plot = (
    ggplot(anscombe_quartet, aes("x", "y", color="dataset"))
    + aesth.line()
    + facet_wrap("dataset")
    + labs(title="Anscombe's quartet")
    + aesth.dress(colour=True, claim="I", levels=["I", "II", "III", "IV"])
)
aesth.save(plot, "anscombe.png")

table = aesth.GT_aesth(pd.DataFrame({"city": ["Leeds"], "index": [112]}))
css = aesth.css_aesth()     # Bootstrap variables; no shinyswatch

# Shiny Express. Same palette on the page, the plot, and the table.
# aesth.page_aesth("arden", title="æsth")
# @render.plot  -> ggplot(...) + aesth.theme_aesth("arden")
# @render.ui    -> ui.HTML(aesth.GT_aesth(frame, palette="arden").as_raw_html())
```

Eight frozen palettes share the same roles: `arden`, `carbon`, `vellum`, `obsidian`, `cinnabar`, `chloris`, `iodine`, `noir`. Switch with `aesth.use("carbon")` or pass `palette=` to a helper.

## What this package owns

| Layer | Job |
|---|---|
| Palettes | Named token sets in `src/aesth/palettes.py` |
| Marks | `line`, `point`, `col`, `area`, `band` — plotnine geoms with house geometry |
| Claim | `dress(colour=True, claim=, levels=)` puts accent on one category |
| Themes | `theme_aesth`, `GT_aesth` (quiet `fmt_*`), `page_aesth` |
| Diagrams | Hand SVG for structure that is not a data geom |

## What this package refuses

- Forking or vendoring plotnine, Great Tables, or Shiny
- Rainbow categorical palettes, 3D, glow, dual y-axes, pie charts
- Guessing hex values without contrast notes and a rendered proof
- Putting private datasets, lecture notes, or unrelated project files in this tree

## Install

```text
pip install -e ".[charts,tables]"   # plotnine + Great Tables
pip install -e ".[all]"             # plus Shiny
```

Core `import aesth` does not require the extras. Theme helpers raise a clear error if the matching extra is missing.

## Status

0.3.0 — one palette path for a plotnine figure, a Great Table, and a Shiny page (`page_aesth`). `import aesth` does not load those three libraries. Proofs in `studies/`. Read [`docs/INDEX.md`](docs/INDEX.md). Brand brief: [`aesth — Creative Direction Brief.md`](<aesth — Creative Direction Brief.md>).

## Layout

```text
aesth/
  aesth — Creative Direction Brief.md  # locked brand brief (original filename)
  src/aesth/           # contrast, tokens, palettes, marks, theme, tables, shiny
  docs/                # research, decisions, palettes, brand pointer
  examples/            # anscombe.py, table.py, app.py
  studies/             # rendered PNG/SVG proofs
  scripts/             # freeze_palettes.py
```

## What it is for

aesth is an open-source wrapper. plotnine draws, Great Tables sets type, and Shiny hosts the page. aesth supplies shorter commands: one palette, one highlight, house geometry, and a page that uses the same tokens. It does not reimplement those libraries, and it does not carry a dataset of its own.
