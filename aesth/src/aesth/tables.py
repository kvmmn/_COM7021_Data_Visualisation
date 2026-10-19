"""Great Tables chrome bound to the active aesth palette."""

from __future__ import annotations

from aesth.fonts import font_stack
from aesth.palettes import get_palette
from aesth.tokens import Palette


def _gt():
    try:
        from great_tables import GT, loc, style
    except ImportError as exc:
        raise ImportError(
            "GT_aesth requires great-tables. Install with: pip install 'aesth[tables]'"
        ) from exc
    return GT, loc, style


def _resolve(palette: str | Palette | None) -> Palette:
    if isinstance(palette, Palette):
        return palette
    return get_palette(palette)


def GT_aesth(df, palette: str | Palette | None = None, *, stripe: bool = False, **kwargs):
    """Wrap ``GT(df)`` with ink headers, paper body, and quiet rules."""
    GT, loc, style = _gt()
    tokens = _resolve(palette)
    table = GT(df, **kwargs)
    table = table.tab_options(
        table_font_names=font_stack(),
        table_font_size="13px",
        table_font_color=tokens.ink,
        table_font_color_light=tokens.white,
        table_background_color=tokens.paper,
        heading_background_color=tokens.ink,
        heading_title_font_weight="bold",
        heading_border_bottom_color=tokens.ink,
        heading_border_lr_style="none",
        column_labels_background_color=tokens.ink,
        column_labels_font_weight=600,
        column_labels_border_top_style="none",
        column_labels_border_bottom_color=tokens.ink,
        column_labels_vlines_style="none",
        table_body_hlines_color=tokens.grid,
        table_body_hlines_width="1px",
        table_body_vlines_style="none",
        table_border_top_color=tokens.ink,
        table_border_top_width="2px",
        table_border_bottom_color=tokens.line,
        table_border_bottom_width="1px",
        table_border_left_style="none",
        table_border_right_style="none",
        row_striping_background_color=tokens.mist,
        row_striping_include_table_body=stripe,
        table_additional_css=[
            f".gt_title, .gt_subtitle, .gt_heading {{ color: {tokens.white} !important; }}",
            f".gt_col_heading, .gt_column_spanner {{ color: {tokens.white} !important; }}",
            f".gt_table {{ border-collapse: collapse; }}",
        ],
    )
    table = table.tab_style(
        style=style.text(color=tokens.white),
        locations=loc.column_labels(),
    )
    try:
        table = table.tab_style(
            style=style.text(color=tokens.white),
            locations=loc.header(),
        )
    except (TypeError, ValueError, AttributeError):
        pass
    return table


def highlight_column(gt, col, palette: str | Palette | None = None):
    """Accent stroke on one claimed column."""
    _GT, loc, style = _gt()
    tokens = _resolve(palette)
    return gt.tab_style(
        style=style.borders(
            sides=["left", "right"],
            color=tokens.accent,
            style="solid",
            weight="2px",
        ),
        locations=loc.body(columns=col),
    )
