# æsth

**The aesthetics of data.**

Aesth is a small Python layer that makes [plotnine](https://plotnine.org/), [Great Tables](https://posit-dev.github.io/great-tables/), and [Shiny for Python](https://shiny.posit.co/py/) speak one visual language. It is not a new charting engine. It does not reimplement ggplot, GT, or Shiny.

Product name: **Aesth**. Package: `aesth`. Mark: **æsth**.

## Usage

```python
import pandas as pd
from plotnine import ggplot, aes, geom_point, geom_smooth, facet_wrap, labs

import aesth

aesth.use("arden")          # process-wide; default is arden
print(aesth.palette().ink)  # '#002B49'

from plotnine.data import anscombe_quartet

plot = (
    ggplot(anscombe_quartet, aes("x", "y"))
    + geom_point()
    + geom_smooth(method="lm", se=False)
    + facet_wrap("dataset")
    + labs(title="Anscombe's quartet")
    + aesth.theme_aesth()
    + aesth.scale_colour_aesth()
)
plot.save("anscombe.png", dpi=220)

table = aesth.GT_aesth(pd.DataFrame({"city": ["Leeds"], "index": [112]}))
css = aesth.css_aesth()     # Bootstrap variables; no shinyswatch
```

Eight frozen palettes share the same roles: `arden`, `carbon`, `vellum`, `obsidian`, `cinnabar`, `chloris`, `iodine`, `noir`. Switch with `aesth.use("carbon")` or pass `palette=` to a helper.

## What this package owns

| Layer | Job |
|---|---|
| Palettes | Named token sets in `src/aesth/palettes.py` |
| Geometry | One job per figure, one highlight, five categorical series maximum |
| Themes | `theme_aesth`, `GT_aesth`, `css_aesth` |
| Diagrams | Hand SVG for structure that is not a data geom |

## What this package refuses

- Forking or vendoring plotnine, Great Tables, or Shiny
- Rainbow categorical palettes, 3D, glow, dual y-axes, pie charts
- Guessing hex values without contrast notes and a rendered proof
- Putting university course files, lecture PDFs, or assignment datasets in this tree

## Install

```text
pip install -e ".[charts,tables]"   # plotnine + Great Tables
pip install -e ".[all]"             # plus Shiny
```

Core `import aesth` does not require the extras. Theme helpers raise a clear error if the matching extra is missing.

## Status

0.1.0 — palettes frozen, themes importable, proofs in `studies/`. Read [`docs/INDEX.md`](docs/INDEX.md). Brand brief: [`aesth — Creative Direction Brief.md`](<aesth — Creative Direction Brief.md>).

## Layout

```text
aesth/
  aesth — Creative Direction Brief.md  # locked brand brief (original filename)
  src/aesth/           # contrast, tokens, palettes, theme, tables, shiny
  docs/                # research, decisions, palettes, brand pointer
  examples/            # anscombe.py, table.py, app.py
  studies/             # rendered PNG/SVG proofs
  scripts/             # freeze_palettes.py
```

## Course context

This folder is a subproject of the COM7021 Data Visualisation working repo. Assessed writing still lives in `COM7021 - Assignment/`. EcoMove analysis will *import* aesth; it will not live inside this package.
