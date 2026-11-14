# ADR 0008 — Geometry refuses a stolen mapping and a sixth series

**Status:** accepted  
**Date:** 19 October 2026

## Context

ADR 0006 put house colour on `DEFAULT_AES` so a mapped series stays a mapping. `claim=True` still wrote a constant into `aes_params`. plotnine then deletes that aesthetic from an inherited plot mapping, so two cities become one polyline. A manual scale of five colours only warned when a sixth level appeared, and painted the extra level with the missing-value colour. On this machine Aptos Display is also registered as the family Aptos, and matplotlib's tie-break returned the display cut for regular text.

## Options

1. Leave the warnings and the constant claim colour. Document that callers must not combine them.
2. Subclass plotnine's geoms and scales.
3. **Keep ordinary plotnine objects. Refuse the combination when the plot mapping becomes visible, and refuse a sixth series when the scale is built or asked to map.**

## Choice

Option 3.

- `line(claim=True)`, `point(claim=True)`, and `col(claim=True)` still store accent on the geom. Adding one of them to a plot that already maps the same aesthetic raises the same error as a mapping on the geom itself. `inherit_aes=False` keeps the fixed accent, because the plot mapping is not inherited.
- `colour_map` and `scale_colour_aesth` / `scale_fill_aesth` raise above five series. An explicit `values` or `limits` longer than five raises at construction. A default five-colour scale raises when drawing asks for a sixth level, instead of warning.
- `resolve_sans` drops display files that claim the text family name, so Aptos resolves to the text cut. Aptos Display stays available under its own name. DejaVu is still not a silent fallback.
- `dress` and `finish` already return a new plot: plotnine copies on `+`. `save` already passes 220 dpi, a tight bbox, and a 0.25 in pad. Those paths are now locked by tests.

## Consequences

- A multi-series claim still goes through `dress(claim=, levels=)`, not `line(claim=True)`.
- A sixth category fails the figure instead of leaking a grey series.
- Figures that asked for Aptos and received Aptos Display now get the text face. The font list for the process is filtered once.

## Links

[0006-marks.md](0006-marks.md) · [HOUSE_STYLE.md](../design/HOUSE_STYLE.md)
