# Palette: `carbon`

**Status:** frozen  
**Proofs:** `studies/palette_poster.png`, `studies/anscombe_carbon.png`

Graphite structure on warm paper; one oxidised-brass claim. Closest data analogue to the æsth identity chrome without copying `#151515` / `#F1F0EB`.

## Tokens

| Role | Hex | Job |
|---|---|---|
| `ink` | `#1B1916` | Warm graphite titles, axes, dark headers |
| `accent` | `#C4A36A` | Brass highlight fill and stroke |
| `accent_deep` | `#6F5324` | Oxidised brass; white-text chips |
| `ink_soft` | `#3A3530` | Alternate series |
| `support` | `#5C554C` | Pewter; third categorical |
| `mist` | `#EFEAE2` | Zebra / lane |
| `paper` | `#F5F2EB` | Warm canvas |
| `white` | `#FFFFFF` | Cards, bar edges |
| `mute` | `#5C564E` | Ticks |
| `grid` | `#DDD7CD` | Chart grid |
| `line` | `#CFC8BC` | Diagram strokes |
| `series` | `ink`, `accent_deep`, `support`, `ink_soft`, `accent` | Accent last |
| `chip_fill` | `#6F5324` | `accent_deep` |

## Contrast (WCAG 2.2, measured)

| Pair | Ratio | Target | Result |
|---|---|---|---|
| ink on paper | 15.69:1 | 7:1 | pass |
| mute on paper | 6.49:1 | 4.5:1 | pass |
| white on ink | 17.54:1 | 7:1 | pass |
| white on accent_deep | 7.15:1 | 4.5:1 | pass |
| white on accent | 2.39:1 | 4.5:1 | fail (optional) |

Brass `accent` is a fill and a 2 px stroke, not a chip. White text sits on `accent_deep` or `ink`.

## Psychology

- Near-black graphite: print, instrument, archival ink.
- Warm paper: avoids the cold dashboard of pure `#FFFFFF`.
- Brass is metal, not notification-gold and not SaaS amber. It marks the claimed series the way a tooled line marks a plate.

## Sequential / categorical

Categorical stops at five: dark graphite, oxidised brass, pewter, mid graphite, bright brass. Sequential work should stay inside the graphite–mist ramp; do not invent a sixth metal.

## Refusals

Cyan, purple glow, polished chrome gradients, copying brand `#151515` onto every bar. Identity chrome stays on the docs mark; data uses this warmer graphite.
