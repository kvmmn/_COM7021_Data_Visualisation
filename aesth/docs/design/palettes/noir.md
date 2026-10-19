# Palette: `noir`

**Status:** frozen  
**Proofs:** `studies/palette_poster.png`

Near-monochrome. One warm-ivory highlight. Maximum reduction.

## Tokens

| Role | Hex | Job |
|---|---|---|
| `ink` | `#1A1A1A` | Structure |
| `accent` | `#C8B896` | Warm ivory fill and stroke |
| `accent_deep` | `#5C5646` | Warm stone; chips |
| `ink_soft` | `#3D3D3D` | Alternate series |
| `support` | `#5C5C5C` | Mid grey |
| `mist` | `#EEEEEA` | Quiet zebra |
| `paper` | `#F4F4F1` | Cool newsprint |
| `white` | `#FFFFFF` | Cards |
| `mute` | `#555555` | Ticks |
| `grid` | `#DDDDD8` | Chart grid |
| `line` | `#CECEC8` | Diagram strokes |
| `series` | `ink`, `accent_deep`, `support`, `ink_soft`, `accent` | Accent last |
| `chip_fill` | `#5C5646` | `accent_deep` |

## Contrast (WCAG 2.2, measured)

| Pair | Ratio | Target | Result |
|---|---|---|---|
| ink on paper | 15.79:1 | 7:1 | pass |
| mute on paper | 6.77:1 | 4.5:1 | pass |
| white on ink | 17.40:1 | 7:1 | pass |
| white on accent_deep | 7.31:1 | 4.5:1 | pass |
| white on accent | 1.95:1 | 4.5:1 | fail (optional) |

Ivory `accent` is a bar fill and a 2 px stroke. It is not a chip. The five greys are spaced so a projector still separates them.

## Psychology

- Greyscale is the control condition of the library: if a chart still works in `noir`, the geometry is doing the job.
- Warm ivory is the only permission to be chromatic.
- This palette most closely obeys “remove anything that does not contribute”.

## Sequential / categorical

`ink` → `ink_soft` → `support` → `accent_deep` → `accent`. Do not add a cold blue “just for the highlight”.

## Refusals

A second accent, photographic duotone, film-grain overlays, using ivory on every series.
