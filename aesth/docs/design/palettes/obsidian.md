# Palette: `obsidian`

**Status:** frozen  
**Proofs:** `studies/palette_poster.png`

Cool black, glacial claim, museum vitrine. Night seriousness on a print-safe light canvas.

## Tokens

| Role | Hex | Job |
|---|---|---|
| `ink` | `#14181E` | Cool black structure |
| `accent` | `#8BB8C8` | Glacial ice fill and stroke |
| `accent_deep` | `#2F5C6C` | Deep ice; chips |
| `ink_soft` | `#2C3540` | Alternate series |
| `support` | `#4A5864` | Slate |
| `mist` | `#E6EDF1` | Cool lane |
| `paper` | `#F3F5F7` | Museum white |
| `white` | `#FFFFFF` | Cards |
| `mute` | `#54606A` | Ticks |
| `grid` | `#D3DBE1` | Chart grid |
| `line` | `#C4CDD4` | Diagram strokes |
| `series` | `ink`, `accent_deep`, `support`, `ink_soft`, `accent` | Accent last |
| `chip_fill` | `#2F5C6C` | `accent_deep` |

Apps using `obsidian` may darken chrome later; this freeze keeps `paper` light so Word figures remain readable. Docs-site identity can stay warm white.

## Contrast (WCAG 2.2, measured)

| Pair | Ratio | Target | Result |
|---|---|---|---|
| ink on paper | 16.30:1 | 7:1 | pass |
| mute on paper | 5.90:1 | 4.5:1 | pass |
| white on ink | 17.81:1 | 7:1 | pass |
| white on accent_deep | 7.32:1 | 4.5:1 | pass |
| white on accent | 2.15:1 | 4.5:1 | fail (optional) |

Ice `accent` is a fill. White text uses `accent_deep` or `ink`.

## Psychology

- Obsidian: density, cut stone, seriousness.
- Glacial accent: distance, climate, precision — not “tech cyan”.
- Mist stays cool. A warm mist would break the stone.

## Sequential / categorical

Alternate cool black and slate, keep ice last. Do not add a neon second highlight.

## Refusals

Glow, electric cyan, dark-mode neon on black UI, aurora gradients. Museum glass, not a nightclub.
