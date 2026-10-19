"""WCAG 2 relative luminance and contrast ratio.

Math follows WCAG 2.2 Success Criterion 1.4.3 / 1.4.6 relative-luminance
definition (sRGB, threshold 0.03928). See docs/SOURCES.md S13.
"""

from __future__ import annotations

from typing import Iterable

# WCAG 2.x official linearisation threshold (not the sRGB 0.04045 knee).
_SRGB_THRESHOLD = 0.03928
_AAA_NORMAL = 7.0
_AA_NORMAL = 4.5


def parse_hex(hex_color: str) -> tuple[int, int, int]:
    """Return ``(r, g, b)`` in 0–255 from ``#RRGGBB``."""
    if not isinstance(hex_color, str):
        raise TypeError(f"hex colour must be a string, got {type(hex_color)!r}")
    value = hex_color.strip()
    if value.startswith("#"):
        value = value[1:]
    if len(value) != 6:
        raise ValueError(f"expected #RRGGBB, got {hex_color!r}")
    try:
        return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
    except ValueError as exc:
        raise ValueError(f"invalid hex colour {hex_color!r}") from exc


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Alias of :func:`parse_hex` for CSS ``r, g, b`` tuples."""
    return parse_hex(hex_color)


def _linearize(channel_8bit: int) -> float:
    srgb = channel_8bit / 255.0
    if srgb <= _SRGB_THRESHOLD:
        return srgb / 12.92
    return ((srgb + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    """WCAG relative luminance of an sRGB hex colour, 0–1."""
    red, green, blue = parse_hex(hex_color)
    return (
        0.2126 * _linearize(red)
        + 0.7152 * _linearize(green)
        + 0.0722 * _linearize(blue)
    )


def contrast_ratio(foreground: str, background: str) -> float:
    """WCAG contrast ratio of two hex colours (order-independent)."""
    lighter, darker = sorted(
        (relative_luminance(foreground), relative_luminance(background)),
        reverse=True,
    )
    return (lighter + 0.05) / (darker + 0.05)


def ratio(foreground: str, background: str) -> float:
    """Rounded contrast ratio to two decimals, for tables and freeze logs."""
    return round(contrast_ratio(foreground, background), 2)


def passes_aaa(foreground: str, background: str) -> bool:
    return contrast_ratio(foreground, background) >= _AAA_NORMAL


def passes_aa(foreground: str, background: str) -> bool:
    return contrast_ratio(foreground, background) >= _AA_NORMAL


def format_ratio(value: float) -> str:
    return f"{value:.2f}:1"


def required_pairs(tokens: dict[str, str]) -> list[tuple[str, str, str, float]]:
    """Named pair, fg, bg, minimum ratio.

    ``white`` on ``accent`` is reported but not required: chips fall back
    to ``accent_deep`` when that pair misses AA.
    """
    return [
        ("ink on paper", tokens["ink"], tokens["paper"], _AAA_NORMAL),
        ("mute on paper", tokens["mute"], tokens["paper"], _AA_NORMAL),
        ("white on ink", tokens["white"], tokens["ink"], _AAA_NORMAL),
        ("white on accent_deep", tokens["white"], tokens["accent_deep"], _AA_NORMAL),
        ("white on accent", tokens["white"], tokens["accent"], _AA_NORMAL),
    ]


def audit(tokens: dict[str, str]) -> list[dict[str, object]]:
    """Measure every required pairing. ``required`` is False for accent chips."""
    rows: list[dict[str, object]] = []
    for name, foreground, background, minimum in required_pairs(tokens):
        value = contrast_ratio(foreground, background)
        required = name != "white on accent"
        rows.append(
            {
                "pair": name,
                "foreground": foreground,
                "background": background,
                "ratio": round(value, 2),
                "minimum": minimum,
                "pass": value >= minimum,
                "required": required,
            }
        )
    return rows


def failures(tokens: dict[str, str]) -> list[dict[str, object]]:
    return [row for row in audit(tokens) if row["required"] and not row["pass"]]


def chip_fill(tokens: dict[str, str]) -> str:
    """Fill behind white chip text.

    Prefer ``accent``, then ``accent_deep``, then ``ink``. Frozen ``arden``
    keeps its historical tiffany hex; both accent stops miss AA for white
    text, so chips use midnight ink.
    """
    if passes_aa(tokens["white"], tokens["accent"]):
        return tokens["accent"]
    if passes_aa(tokens["white"], tokens["accent_deep"]):
        return tokens["accent_deep"]
    return tokens["ink"]


def assert_required(tokens: dict[str, str], name: str = "palette") -> None:
    missed = failures(tokens)
    if missed:
        detail = "; ".join(
            f"{row['pair']} {row['ratio']}:1 < {row['minimum']}:1" for row in missed
        )
        raise ValueError(f"{name} misses required contrast: {detail}")


def summarise(tokens: dict[str, str]) -> str:
    lines: list[str] = []
    for row in audit(tokens):
        flag = "ok" if row["pass"] else ("optional-fail" if not row["required"] else "FAIL")
        lines.append(f"{row['pair']:<22} {format_ratio(row['ratio']):>8}  {flag}")
    return "\n".join(lines)


def rgb_css(hex_color: str) -> str:
    red, green, blue = parse_hex(hex_color)
    return f"{red}, {green}, {blue}"


def walk_roles(tokens: Iterable[str]) -> list[str]:
    return list(tokens)
