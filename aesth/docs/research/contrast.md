# Research: contrast method

**Role in aesth:** the only allowed way to freeze a hex pair.

Canonical pages: [WCAG 2.2 relative luminance](https://www.w3.org/TR/WCAG22/#dfn-relative-luminance) (S13), [contrast ratio](https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio) (S14).

## Purpose

Named palettes are a design claim. Contrast maths is the check that the claim can still be read. `src/aesth/contrast.py` implements the WCAG 2.2 formulae; `scripts/freeze_palettes.py` prints them.

## Formulae we actually use

- sRGB channel → linear: divide by 12.92 if ≤ 0.03928, else `((c + 0.055) / 1.055) ** 2.4`
- Relative luminance: `0.2126 R + 0.7152 G + 0.0722 B`
- Contrast: `(L_lighter + 0.05) / (L_darker + 0.05)`

Targets for every palette: ink-on-paper ≥ 7:1; mute-on-paper ≥ 4.5:1; white-on-ink ≥ 7:1; white-on-accent_deep ≥ 4.5:1. White-on-accent is reported, not required.

## Workarounds

- Light accents (arden tiffany, carbon brass, vellum oxide, obsidian ice, chloris olive, noir ivory) fail white-text AA. Chips use `accent_deep`, or `ink` when that also fails.
- `arden` hex is historically frozen. White on `#3AA89A` is 2.90:1. Chips use midnight.

## Refusals

Online contrast pickers as the source of truth. The package must be able to reprint the ratios from the hex in `palettes.py`.
