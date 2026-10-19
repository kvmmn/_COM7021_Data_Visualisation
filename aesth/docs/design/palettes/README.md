# Palette registry

A palette is a **complete semantic token set**, not a mood board of hex codes. plotnine, Great Tables, Shiny, and SVG diagrams all read the same roles. See [ADR 0004](../../decisions/0004-palettes.md) and [ADR 0005](../../decisions/0005-freeze.md).

## Contract

Every named palette documents:

1. Roles filled: `ink`, `accent`, `accent_deep`, `ink_soft`, `support`, `mist`, `paper`, `white`, `mute`, `grid`, `line`, `series` (five).
2. Contrast: `ink` on `paper` ≥ 7:1; `mute` on `paper` ≥ 4.5:1; white on `ink` ≥ 7:1; white on `accent_deep` ≥ 4.5:1 (except historically frozen `arden`).
3. Colour psychology: what the highlight is allowed to mean; what it must not mean.
4. Sequential / categorical / diverging notes. Categorical stops at five.
5. Refusals (no extra hue family, no rainbow).
6. A rendered proof. Hex is frozen in `src/aesth/palettes.py`.

If white-on-accent misses AA, chips use `accent_deep`, or `ink` when that also misses. Accent remains a fill and stroke.

## Named set (frozen)

| Name | Intent | Hex status |
|---|---|---|
| [`arden`](arden.md) | COM7021 / assignment default. Midnight structure, tiffany claim. | Frozen |
| [`carbon`](carbon.md) | Graphite and warm white; oxidised-brass accent. | Frozen |
| [`vellum`](vellum.md) | Archival paper, oxide, bone. | Frozen |
| [`obsidian`](obsidian.md) | Cool black, glacial claim, museum. | Frozen |
| [`cinnabar`](cinnabar.md) | Graphite with a rare earth-red claim. | Frozen |
| [`chloris`](chloris.md) | Olive / moss, not “eco green”. | Frozen |
| [`iodine`](iodine.md) | Scientific brown-violet. No purple glow. | Frozen |
| [`noir`](noir.md) | Near-monochrome, one ivory highlight. | Frozen |

Do not add a ninth name until these eight have more than a poster proof. Hand-curated, not ColorBrewer dumped.

## API

```python
import aesth

aesth.use("arden")
from plotnine import ggplot, aes, geom_line

ggplot(df, aes("x", "y")) + geom_line() + aesth.theme_aesth()
aesth.GT_aesth(df)
print(aesth.css_aesth())
```

COM7021 EcoMove uses `arden` unless a later assignment note says otherwise.
