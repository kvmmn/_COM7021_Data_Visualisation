# Documentation map

British English. Every claim that came from the web has a URL in [`SOURCES.md`](SOURCES.md). Every stack choice has a decision record.

| Path | What it is |
|---|---|
| [../README.md](../README.md) | Public pitch and non-goals |
| [../aesth — Creative Direction Brief.md](<../aesth — Creative Direction Brief.md>) | Locked brand brief (æsth), original filename |
| [brand/CREATIVE_DIRECTION.md](brand/CREATIVE_DIRECTION.md) | Docs-tree pointer to that brief |
| [design/HOUSE_STYLE.md](design/HOUSE_STYLE.md) | Geometry, reduction, type, recipes |
| [design/palettes/README.md](design/palettes/README.md) | Palette registry contract |
| [design/palettes/arden.md](design/palettes/arden.md) | Assignment default palette (hex frozen) |
| [design/palettes/](design/palettes/) | Frozen palettes: carbon, vellum, obsidian, cinnabar, chloris, iodine, noir |
| [research/plotnine.md](research/plotnine.md) | What we take from plotnine |
| [research/great-tables.md](research/great-tables.md) | What we take from Great Tables |
| [research/shiny.md](research/shiny.md) | What we take from Shiny for Python |
| [research/contrast.md](research/contrast.md) | WCAG freeze method |
| [research/COMPARISON.md](research/COMPARISON.md) | Who owns which job |
| [decisions/0001-stack.md](decisions/0001-stack.md) | Three-library composition |
| [decisions/0002-name.md](decisions/0002-name.md) | Name: Aesth / `aesth` / æsth |
| [decisions/0003-docs-standard.md](decisions/0003-docs-standard.md) | How this tree is written |
| [decisions/0004-palettes.md](decisions/0004-palettes.md) | Palettes as a user-selectable registry |
| [decisions/0005-freeze.md](decisions/0005-freeze.md) | Hex freeze and WCAG contrast method |
| [SOURCES.md](SOURCES.md) | Living source ledger |

## Reading order

1. README (what aesth is not).
2. Creative direction (who it wants to look like).
3. Comparison (who owns charts, tables, apps).
4. House style + palette contract.
5. The three research notes if you are implementing a theme.

Theme Python lives in `src/aesth/`. Palettes are frozen; see ADR 0005.

The original creative brief lives at [`aesth/aesth — Creative Direction Brief.md`](<../aesth — Creative Direction Brief.md>). [`brand/CREATIVE_DIRECTION.md`](brand/CREATIVE_DIRECTION.md) is a pointer only. Do not keep a copy at the course-repo root.
