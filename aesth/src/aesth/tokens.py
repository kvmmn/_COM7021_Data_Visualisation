"""Semantic colour tokens shared by plotnine, Great Tables, and Shiny."""

from __future__ import annotations

from dataclasses import dataclass, field

from aesth.contrast import chip_fill as _chip_fill
from aesth.contrast import passes_aa


@dataclass(frozen=True)
class Palette:
    """One complete aesth token set.

    ``series`` is always ``(ink, accent_deep, support, ink_soft, accent)``
    so the highlight stays last and can still mark a claim.
    """

    name: str
    ink: str
    accent: str
    accent_deep: str
    ink_soft: str
    support: str
    mist: str
    paper: str
    white: str
    mute: str
    grid: str
    line: str
    series: tuple[str, str, str, str, str] = field(init=False, repr=True)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "series",
            (self.ink, self.accent_deep, self.support, self.ink_soft, self.accent),
        )

    def as_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "ink": self.ink,
            "accent": self.accent,
            "accent_deep": self.accent_deep,
            "ink_soft": self.ink_soft,
            "support": self.support,
            "mist": self.mist,
            "paper": self.paper,
            "white": self.white,
            "mute": self.mute,
            "grid": self.grid,
            "line": self.line,
        }

    @property
    def roles(self) -> dict[str, str]:
        data = self.as_dict()
        data.pop("name")
        return data

    @property
    def accent_holds_white_text(self) -> bool:
        return passes_aa(self.white, self.accent)

    @property
    def chip_fill(self) -> str:
        """Fill for white-text chips and pills."""
        return _chip_fill(self.roles)

    @property
    def highlight_alpha_band(self) -> float:
        return 0.12

    @property
    def highlight_alpha_area(self) -> float:
        return 0.35
