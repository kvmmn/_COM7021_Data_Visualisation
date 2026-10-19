# Palette: `arden`

**Status:** frozen (assignment default)  
**Proofs:** COM7020 MES figures; COM7021 design-guide studies; `studies/anscombe_arden.png`, `studies/arden_table.html`

Midnight is structure. Tiffany is the claim. Nothing else joins the hue family.

## Tokens

| Role | Hex | Job |
|---|---|---|
| `ink` | `#002B49` | Titles, axes, primary series, dark headers |
| `accent` | `#66C9BA` | Highlight series, emphasis stroke, highlighted bars |
| `accent_deep` | `#3AA89A` | Recommended markers, claimed arrows |
| `ink_soft` | `#1A4A6B` | Alternate series, quieter bars |
| `support` | `#0E7C8B` | Third categorical only |
| `mist` | `#E6F5F2` | Lanes, zebra, highlighted card fill |
| `paper` | `#F7FAFB` | Axes / canvas |
| `white` | `#FFFFFF` | Cards, bar edges |
| `mute` | `#5A6B75` | Ticks, secondary text |
| `grid` | `#D5DEE3` | Chart grid |
| `line` | `#C9D5DD` | Diagram strokes |
| `series` | `ink`, `accent_deep`, `support`, `ink_soft`, `accent` | Categorical order; accent last |
| `chip_fill` | `#002B49` (`ink`) | White-text chips; see contrast |

Alpha: highlight band 0.12; area fill 0.35. Stronger washes muddy tiffany.

## Contrast (WCAG 2.2, measured)

| Pair | Ratio | Target | Result |
|---|---|---|---|
| ink on paper | 13.89:1 | 7:1 | pass |
| mute on paper | 5.28:1 | 4.5:1 | pass |
| white on ink | 14.57:1 | 7:1 | pass |
| white on accent_deep | 2.90:1 | 4.5:1 | **fail — hex frozen** |
| white on accent | 1.98:1 | 4.5:1 | fail (optional) |

`accent` and `accent_deep` are fills and strokes, not chip backgrounds. White-text chips use `ink`. Do not put `ink` body text on `accent`. Do not put white text on `mist` or `paper`.

## Psychology

- Navy (`ink`) reads as institutional, stable, structural — suitable for axes and “the world as it is”.
- Tiffany (`accent`) is reserved for **the decision**: the peak, the recommended column, the exception. It is not “pretty teal everywhere”.
- A third teal (`support`) exists only so a five-series line can alternate dark navy and mid teal. It is not a second highlight.

## Refusals

Orange, purple, red, rainbow, glow. If an exception needs alarm, that is a different palette (`cinnabar`), not a one-off hue in `arden`.

## Source

COM7021 `VISUAL_DESIGN_GUIDE.md` (S10). Arden logo pair plus the derived working set from the COM7020 portfolio. Contrast method: S13.
