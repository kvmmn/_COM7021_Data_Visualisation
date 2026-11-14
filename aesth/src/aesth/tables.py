"""Great Tables chrome bound to the active aesth palette.

The caller's frame is passed straight to ``GT``. aesth does not copy it.
Quiet formatting calls Great Tables' own ``fmt_integer``, ``fmt_number``,
and ``sub_missing``. There is no cell heatmap.
"""

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


def _numeric_kind(dtype: object) -> str | None:
    """``int``, ``float``, or ``None``. Reads the dtype label only."""
    kind = getattr(dtype, "kind", None)
    if kind in {"i", "u"}:
        return "int"
    if kind == "f":
        return "float"
    if kind in {"b", "O", "M", "m", "S", "U"}:
        return None
    text = str(dtype).lower()
    if "bool" in text:
        return None
    if "int" in text or "uint" in text:
        return "int"
    if "float" in text or "double" in text or "decimal" in text:
        return "float"
    return None


def _numeric_columns(df) -> tuple[list, list]:
    """Column names by numeric dtype. Does not copy the frame."""
    columns = getattr(df, "columns", None)
    if columns is None:
        return [], []
    integers: list = []
    floats: list = []
    dtypes = getattr(df, "dtypes", None)
    schema = getattr(df, "schema", None)
    for name in list(columns):
        dtype = None
        if dtypes is not None:
            try:
                dtype = dtypes[name]
            except (KeyError, TypeError, IndexError):
                dtype = None
        if dtype is None and schema is not None:
            try:
                dtype = schema[name]
            except (KeyError, TypeError):
                dtype = None
        kind = _numeric_kind(dtype) if dtype is not None else None
        if kind == "int":
            integers.append(name)
        elif kind == "float":
            floats.append(name)
    return integers, floats


def _quiet_formats(table, df):
    """GT ``fmt_*`` and ``sub_missing`` only. No second table engine."""
    integers, floats = _numeric_columns(df)
    if integers:
        table = table.fmt_integer(columns=integers)
    if floats:
        table = table.fmt_number(columns=floats, decimals=2)
    # Default missing text is GT's em dash (``&mdash;``). Substitutions
    # leave already-formatted numbers alone.
    return table.sub_missing()


def GT_aesth(
    df,
    palette: str | Palette | None = None,
    *,
    stripe: bool = False,
    quiet: bool = True,
    **kwargs,
):
    """Wrap ``GT(df)`` with ink headers, paper body, and quiet rules.

    ``quiet=True`` formats integer columns with ``fmt_integer``, other
    numeric columns with ``fmt_number(decimals=2)``, and missing cells
    with ``sub_missing``. ``quiet=False`` leaves cell text to the caller.
    ``df`` is not copied.
    """
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
    if quiet:
        table = _quiet_formats(table, df)
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
