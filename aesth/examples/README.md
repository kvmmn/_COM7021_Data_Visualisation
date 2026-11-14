# Examples

Run from `aesth/` with the local venv so `src/` is on the path.

```bash
.venv/bin/python examples/anscombe.py
.venv/bin/python examples/recipes.py
.venv/bin/python examples/table.py
.venv/bin/shiny run examples/app.py
```

`app.py` opens with `aesth.page_aesth("arden", title="æsth")`. The select input restyles the plotnine facet and the Great Table through `page_css` and the same palette name. Value boxes stay flat.

Toy frames only. The package does not ship a dataset.
