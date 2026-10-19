"""Shiny / Bootstrap CSS variables from the active aesth palette.

Rejects shinyswatch skins and indigo–purple value-box gradients.
"""

from __future__ import annotations

from aesth.contrast import rgb_css
from aesth.palettes import get_palette
from aesth.tokens import Palette


def _resolve(palette: str | Palette | None) -> Palette:
    if isinstance(palette, Palette):
        return palette
    return get_palette(palette)


def css_aesth(palette: str | Palette | None = None) -> str:
    """Return a CSS string mapping Bootstrap and bslib tokens to the palette."""
    tokens = _resolve(palette)
    ink_rgb = rgb_css(tokens.ink)
    accent_rgb = rgb_css(tokens.accent)
    deep_rgb = rgb_css(tokens.accent_deep)
    paper_rgb = rgb_css(tokens.paper)
    return f"""/* aesth palette: {tokens.name} — no shinyswatch, no gradient value boxes */
:root {{
  --aesth-ink: {tokens.ink};
  --aesth-accent: {tokens.accent};
  --aesth-accent-deep: {tokens.accent_deep};
  --aesth-ink-soft: {tokens.ink_soft};
  --aesth-support: {tokens.support};
  --aesth-mist: {tokens.mist};
  --aesth-paper: {tokens.paper};
  --aesth-white: {tokens.white};
  --aesth-mute: {tokens.mute};
  --aesth-grid: {tokens.grid};
  --aesth-line: {tokens.line};
  --aesth-chip: {tokens.chip_fill};
  --bs-body-bg: {tokens.paper};
  --bs-body-bg-rgb: {paper_rgb};
  --bs-body-color: {tokens.ink};
  --bs-body-color-rgb: {ink_rgb};
  --bs-primary: {tokens.accent_deep};
  --bs-primary-rgb: {deep_rgb};
  --bs-secondary: {tokens.mute};
  --bs-border-color: {tokens.line};
  --bs-link-color: {tokens.accent_deep};
  --bs-link-hover-color: {tokens.ink};
  --bs-emphasis-color: {tokens.ink};
  --bs-tertiary-bg: {tokens.mist};
  --bslib-sidebar-bg: {tokens.mist};
  --bslib-sidebar-fg: {tokens.ink};
}}

html, body {{
  background: {tokens.paper};
  color: {tokens.ink};
}}

.card, .bslib-card {{
  background: {tokens.white};
  border: 1px solid {tokens.line};
  border-radius: 12px;
  box-shadow: 0 2px 0 rgba({ink_rgb}, 0.10);
}}

.bslib-value-box,
.value-box,
.bslib-value-box .value-box-area {{
  background-color: {tokens.paper} !important;
  background-image: none !important;
  color: {tokens.ink};
  border: 1px solid {tokens.line};
  border-radius: 12px;
  box-shadow: none;
}}

.bslib-value-box.aesth-claim,
.value-box.aesth-claim {{
  border-color: {tokens.accent};
  border-width: 2px;
}}

.bslib-value-box .value-box-title,
.value-box .value-box-title {{
  color: {tokens.mute};
}}

.bslib-value-box .value-box-value,
.value-box .value-box-value {{
  color: {tokens.ink};
}}

.navbar, .navbar-default, .bslib-page-navbar {{
  background: {tokens.ink} !important;
  color: {tokens.white};
}}

.form-control, .selectize-input {{
  border-color: {tokens.line};
  color: {tokens.ink};
  background: {tokens.white};
}}

a {{
  color: {tokens.accent_deep};
}}
""".strip()


def page_css(palette: str | Palette | None = None):
    """Return ``ui.tags.style`` when Shiny is installed, else the CSS string."""
    css = css_aesth(palette)
    try:
        from shiny import ui
    except ImportError:
        return css
    return ui.tags.style(css)
