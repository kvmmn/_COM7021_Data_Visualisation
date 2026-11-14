#!/usr/bin/env python3
"""Approval etude: complementary palettes plus a documented Arden raven.

Does not touch the frozen registry. Color Hunt is a mood reference
(https://colorhunt.co/), not a hex source. Renders two posters for review.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from aesth.contrast import contrast_ratio, ratio  # noqa: E402

OUT = Path(__file__).resolve().parent

# Complementary pairs. Accent is the claim colour (often too light for white text).
# accent_deep carries chips. Paper is the wall.
# raven uses the documented Arden tokens exactly (visual design guide / palettes/arden.md).
# Other rows are original interior translations of Color Hunt moods, not copied boards.
ETUDE = [
    {
        "name": "raven",
        "pair": "Midnight  ·  tiffany",
        "room": "University",
        "note": "Codename for the Arden crow. Documented colours only.",
        "ink": "#002B49",
        "accent": "#66C9BA",
        "accent_deep": "#3AA89A",
        "ink_soft": "#1A4A6B",
        "support": "#0E7C8B",
        "mist": "#E6F5F2",
        "paper": "#F7FAFB",
        "white": "#FFFFFF",
        "mute": "#5A6B75",
        "grid": "#D5DEE3",
        "line": "#C9D5DD",
    },
    {
        "name": "salon",
        "pair": "Aubergine  ·  chartreuse",
        "room": "Drawing room",
        "note": "Violet against yellow-green. Plaster wall, one theatrical cushion.",
        "ink": "#3A243C",
        "accent": "#C6B423",
        "accent_deep": "#6E6414",
        "ink_soft": "#5C4860",
        "support": "#A08A68",
        "mist": "#F3EBD0",
        "paper": "#F5F0E8",
        "white": "#FFFCF8",
        "mute": "#6E655C",
        "grid": "#E6DDD0",
        "line": "#D8CFC2",
    },
    {
        "name": "veranda",
        "pair": "Teal  ·  coral",
        "room": "Loggia",
        "note": "Sea against fired clay. Cool structure, one warm object.",
        "ink": "#0E3C42",
        "accent": "#E57A56",
        "accent_deep": "#8E3C28",
        "ink_soft": "#3A5C60",
        "support": "#C4A06A",
        "mist": "#F7E6DC",
        "paper": "#F4EFE8",
        "white": "#FFFCF8",
        "mute": "#6A635C",
        "grid": "#E4DCD2",
        "line": "#D6CEC4",
    },
    {
        "name": "nocturne",
        "pair": "Ink  ·  malachite",
        "room": "Night room",
        "note": "Near-black architecture. One mineral green, no second neon.",
        "ink": "#161616",
        "accent": "#3E8F72",
        "accent_deep": "#1E5C48",
        "ink_soft": "#3A3A3A",
        "support": "#8A8174",
        "mist": "#E7E4DE",
        "paper": "#F2F0EB",
        "white": "#FFFFFF",
        "mute": "#5E5A54",
        "grid": "#DDD8D0",
        "line": "#CFC9C0",
    },
    {
        "name": "hague",
        "pair": "Blue  ·  orange",
        "room": "Study",
        "note": "Navy structure, one lacquered orange chair.",
        "ink": "#143044",
        "accent": "#E25C22",
        "accent_deep": "#8C3412",
        "ink_soft": "#3C5568",
        "support": "#7C8E9A",
        "mist": "#F6E3D2",
        "paper": "#F3EEE6",
        "white": "#FFFCF8",
        "mute": "#6A6258",
        "grid": "#E4DACD",
        "line": "#D5CBBE",
    },
    {
        "name": "hearth",
        "pair": "Wine  ·  amber",
        "room": "Sunset",
        "note": "After Color Hunt sunsets: warmth without a traffic-light red.",
        "ink": "#6A242C",
        "accent": "#E39B2B",
        "accent_deep": "#8A5410",
        "ink_soft": "#8A4A42",
        "support": "#C47A58",
        "mist": "#F6E4CC",
        "paper": "#F8F0E4",
        "white": "#FFFCF6",
        "mute": "#6E5E52",
        "grid": "#E8D8C4",
        "line": "#D9C8B2",
    },
    {
        "name": "cabaret",
        "pair": "Charcoal  ·  magenta",
        "room": "Foyer",
        "note": "After Color Hunt hot pink: one fuchsia object, not a neon field.",
        "ink": "#1C1418",
        "accent": "#E23D78",
        "accent_deep": "#8E2048",
        "ink_soft": "#4A343C",
        "support": "#C4A0A8",
        "mist": "#F6E4EA",
        "paper": "#F7F1F2",
        "white": "#FFFCFC",
        "mute": "#6A5A5E",
        "grid": "#E6D6DA",
        "line": "#D8C6CC",
    },
    {
        "name": "grove",
        "pair": "Olive  ·  clay",
        "room": "Garden",
        "note": "Earth board: cultivated green, one fired-clay pot.",
        "ink": "#3A442C",
        "accent": "#C4623A",
        "accent_deep": "#7A341C",
        "ink_soft": "#5C6848",
        "support": "#A89468",
        "mist": "#EFE6D2",
        "paper": "#F4F1E6",
        "white": "#FFFCF6",
        "mute": "#686258",
        "grid": "#E2DACA",
        "line": "#D4CCBA",
    },
    {
        "name": "glacier",
        "pair": "Slate  ·  ice",
        "room": "Winter",
        "note": "Cold, not tiffany. A pale blue claim on a stone wall.",
        "ink": "#243848",
        "accent": "#7EB4D4",
        "accent_deep": "#2E6484",
        "ink_soft": "#4A6274",
        "support": "#8AA0AE",
        "mist": "#E4EEF4",
        "paper": "#F4F7F8",
        "white": "#FFFFFF",
        "mute": "#5C6A72",
        "grid": "#D5E0E6",
        "line": "#C6D2D8",
    },
    {
        "name": "gild",
        "pair": "Espresso  ·  brass",
        "room": "Ceremony",
        "need": "Luxury mark",
        "note": "After Color Hunt gold boards. One brass object, not a yellow dashboard.",
        "ink": "#2A1C12",
        "accent": "#C8963E",
        "accent_deep": "#7A5418",
        "ink_soft": "#5A4636",
        "support": "#A68462",
        "mist": "#F3E6CC",
        "paper": "#F7F1E4",
        "white": "#FFFCF6",
        "mute": "#6E6256",
        "grid": "#E6D8C4",
        "line": "#D8C8B0",
    },
    {
        "name": "espresso",
        "pair": "Roast  ·  cream",
        "room": "Cafe",
        "need": "Warm reading",
        "note": "Coffee browns for a long page. Cognac is the only claim.",
        "ink": "#3A2A22",
        "accent": "#C4844A",
        "accent_deep": "#7A4A24",
        "ink_soft": "#6A5346",
        "support": "#A89078",
        "mist": "#EFE4D6",
        "paper": "#F6F1E8",
        "white": "#FFFCF8",
        "mute": "#6A5E54",
        "grid": "#E4D8CC",
        "line": "#D6C8BA",
    },
    {
        "name": "blossom",
        "pair": "Sage  ·  blush",
        "room": "Clinic",
        "need": "Soft editorial",
        "note": "Pastel spring. Quiet enough to read, pink enough to be remembered.",
        "ink": "#3E5344",
        "accent": "#E4A8B4",
        "accent_deep": "#8A5460",
        "ink_soft": "#6A7A68",
        "support": "#C4B09A",
        "mist": "#F6E8EA",
        "paper": "#F7F4EF",
        "white": "#FFFCFA",
        "mute": "#6A645E",
        "grid": "#E4DED6",
        "line": "#D6D0C8",
    },
    {
        "name": "vesper",
        "pair": "Night  ·  candle",
        "room": "After dark",
        "need": "Dark UI",
        "note": "The wall is the dark. Text and sofa are the light. One candle accent.",
        "ink": "#F3EFE6",
        "accent": "#E2B15A",
        "accent_deep": "#7A5014",
        "ink_soft": "#C8C2B4",
        "support": "#8E8678",
        "mist": "#2A2C30",
        "paper": "#17181B",
        "white": "#FFFFFF",
        "mute": "#B7B1A4",
        "grid": "#3A3C40",
        "line": "#4A4C52",
    },
    {
        "name": "archive",
        "pair": "Faded navy  ·  rose",
        "room": "Museum",
        "need": "Vintage print",
        "note": "Aged paper and a dusty rose. History, not cabaret.",
        "ink": "#2C3A55",
        "accent": "#C9898E",
        "accent_deep": "#7A454C",
        "ink_soft": "#5A6880",
        "support": "#A89880",
        "mist": "#F0E4D8",
        "paper": "#F3EBDD",
        "white": "#FFFCF8",
        "mute": "#6A6258",
        "grid": "#E4D8C8",
        "line": "#D6C8B6",
    },
    {
        "name": "marina",
        "pair": "Harbour  ·  signal",
        "room": "Chart desk",
        "need": "Maps and distance",
        "note": "Deeper than veranda, colder than raven. One signal blue.",
        "ink": "#0E1C38",
        "accent": "#3D7AD4",
        "accent_deep": "#1E4E92",
        "ink_soft": "#3A4E68",
        "support": "#8AA0B4",
        "mist": "#E4EAF2",
        "paper": "#F4F6F8",
        "white": "#FFFFFF",
        "mute": "#5C6A76",
        "grid": "#D4DEE6",
        "line": "#C6D0D8",
    },
]

ROLES = [
    "ink",
    "accent",
    "accent_deep",
    "ink_soft",
    "support",
    "mist",
    "paper",
    "mute",
    "grid",
    "line",
]


def check() -> None:
    print(f"{'name':10} ink/paper  mute/paper  white/deep  accent/paper")
    for item in ETUDE:
        print(
            f"{item['name']:10} "
            f"{ratio(item['ink'], item['paper']):8.2f}  "
            f"{ratio(item['mute'], item['paper']):10.2f}  "
            f"{ratio('#FFFFFF', item['accent_deep']):10.2f}  "
            f"{ratio(item['accent'], item['paper']):11.2f}"
        )


def poster() -> str:
    n = len(ETUDE)
    width, row_h, header = 1480, 246, 120
    height = header + n * row_h + 24
    margin = 40
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        "text { font-family: Aptos, 'Helvetica Neue', sans-serif; }",
        ".title { font-size: 28px; font-weight: 700; fill: #151515; }",
        ".lede { font-size: 14px; fill: #5A564E; }",
        ".name { font-size: 22px; font-weight: 700; }",
        ".pair { font-size: 13px; font-weight: 600; }",
        ".note { font-size: 13px; }",
        ".role { font-size: 10px; font-weight: 600; }",
        ".hex { font-size: 9px; }",
        ".chip { font-size: 11px; font-weight: 700; fill: #FFFFFF; }",
        "</style>",
        '<rect width="100%" height="100%" fill="#EFEAE3"/>',
        '<text class="title" x="48" y="52">æsth — palette etude</text>',
        '<text class="lede" x="48" y="78">Fifteen rooms. raven is the documented Arden crow. New rows cover needs the first nine did not. Hexes are ours; moods after Color Hunt.</text>',
    ]
    for i, item in enumerate(ETUDE):
        y = header + i * row_h
        parts.append(
            f'<rect x="{margin}" y="{y}" width="{width - 2 * margin}" height="{row_h - 18}" '
            f'rx="16" fill="{item["paper"]}" stroke="{item["line"]}"/>'
        )
        parts.append(
            f'<text class="name" x="{margin + 24}" y="{y + 36}" fill="{item["ink"]}">{item["name"]}</text>'
        )
        parts.append(
            f'<text class="pair" x="{margin + 160}" y="{y + 36}" fill="{item["accent_deep"]}">{item["pair"]}</text>'
        )
        parts.append(
            f'<rect x="{margin + 520}" y="{y + 16}" width="78" height="26" rx="13" fill="{item["accent_deep"]}"/>'
        )
        parts.append(
            f'<text class="chip" x="{margin + 559}" y="{y + 34}" text-anchor="middle">{item["room"]}</text>'
        )
        # two large complementary masses
        parts.append(
            f'<rect x="{margin + 24}" y="{y + 52}" width="220" height="72" rx="10" fill="{item["ink"]}"/>'
        )
        ink_label = item["white"] if contrast_ratio("#FFFFFF", item["ink"]) >= 4.5 else item["paper"]
        parts.append(
            f'<text x="{margin + 134}" y="{y + 94}" text-anchor="middle" fill="{ink_label}" '
            f'font-size="13" font-weight="600">ink</text>'
        )
        parts.append(
            f'<rect x="{margin + 256}" y="{y + 52}" width="220" height="72" rx="10" fill="{item["accent"]}"/>'
        )
        parts.append(
            f'<text x="{margin + 366}" y="{y + 94}" text-anchor="middle" fill="{item["ink"]}" '
            f'font-size="13" font-weight="600">accent</text>'
        )
        parts.append(
            f'<text class="note" x="{margin + 500}" y="{y + 78}" fill="{item["ink_soft"]}">{item["note"]}</text>'
        )
        # role row
        for j, role in enumerate(ROLES):
            x = margin + 24 + j * 132
            parts.append(
                f'<rect x="{x}" y="{y + 142}" width="118" height="36" rx="6" fill="{item[role]}" '
                f'stroke="{item["line"]}" stroke-width="1"/>'
            )
            parts.append(
                f'<text class="role" x="{x + 8}" y="{y + 198}" fill="{item["mute"]}">{role}</text>'
            )
            parts.append(
                f'<text class="hex" x="{x + 8}" y="{y + 212}" fill="{item["mute"]}">{item[role]}</text>'
            )
    parts.append("</svg>")
    return "\n".join(parts)


def rooms() -> str:
    """Each palette as a shallow interior: wall, floor, sofa, one cushion."""
    rows = (len(ETUDE) + 2) // 3
    width, height = 1480, 110 + rows * 460 + 24
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text { font-family: Aptos, 'Helvetica Neue', sans-serif; }</style>",
        '<rect width="100%" height="100%" fill="#EFEAE3"/>',
        '<text x="48" y="52" font-size="28" font-weight="700" fill="#151515">Rooms</text>',
        '<text x="48" y="78" font-size="14" fill="#5A564E">One accent object. Added: ceremony, cafe, clinic, dark UI, museum, chart desk.</text>',
    ]
    for i, item in enumerate(ETUDE):
        col, row = i % 3, i // 3
        x, y = 48 + col * 470, 110 + row * 460
        w, h = 440, 420
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{item["paper"]}" stroke="{item["line"]}"/>')
        # floor
        parts.append(f'<rect x="{x}" y="{y + 280}" width="{w}" height="140" fill="{item["ink_soft"]}"/>')
        parts.append(f'<rect x="{x}" y="{y + 400}" width="{w}" height="20" rx="0" fill="{item["ink"]}"/>')
        # window / picture
        parts.append(
            f'<rect x="{x + 250}" y="{y + 48}" width="140" height="110" rx="4" fill="{item["mist"]}" stroke="{item["line"]}"/>'
        )
        parts.append(
            f'<rect x="{x + 268}" y="{y + 66}" width="104" height="74" fill="{item["accent"]}"/>'
        )
        # sofa
        parts.append(f'<rect x="{x + 36}" y="{y + 210}" width="250" height="92" rx="12" fill="{item["ink"]}"/>')
        parts.append(f'<rect x="{x + 36}" y="{y + 188}" width="70" height="48" rx="10" fill="{item["ink"]}"/>')
        parts.append(f'<rect x="{x + 210}" y="{y + 188}" width="76" height="48" rx="10" fill="{item["ink"]}"/>')
        # the one cushion — the claim
        parts.append(f'<rect x="{x + 118}" y="{y + 198}" width="78" height="62" rx="8" fill="{item["accent"]}"/>')
        # side table + object
        parts.append(f'<rect x="{x + 310}" y="{y + 248}" width="72" height="54" rx="4" fill="{item["support"]}"/>')
        parts.append(f'<circle cx="{x + 346}" cy="{y + 236}" r="14" fill="{item["accent_deep"]}"/>')
        name_fill = item["white"] if contrast_ratio(item["white"], item["ink_soft"]) >= 4.5 else item["paper"]
        pair_fill = item["mist"] if contrast_ratio(item["mist"], item["ink_soft"]) >= 3 else item["paper"]
        parts.append(
            f'<text x="{x + 24}" y="{y + 392}" font-size="20" font-weight="700" fill="{name_fill}">{item["name"]}</text>'
        )
        parts.append(
            f'<text x="{x + 24}" y="{y + 412}" font-size="12" fill="{pair_fill}">{item["pair"]}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def render(svg: str, stem: str) -> None:
    svg_path = OUT / f"{stem}.svg"
    png_path = OUT / f"{stem}.png"
    svg_path.write_text(svg)
    subprocess.run(["rsvg-convert", "-w", "1600", "-o", str(png_path), str(svg_path)], check=True)
    print("Wrote", png_path.name)


def main() -> None:
    check()
    render(poster(), "etude_palettes")
    render(rooms(), "etude_rooms")


if __name__ == "__main__":
    main()
