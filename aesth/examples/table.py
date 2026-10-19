"""One Great Tables display with arden chrome."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import aesth

frame = pd.DataFrame(
    {
        "city": ["Leeds", "Bristol", "Glasgow", "Cardiff", "Belfast"],
        "index": [112, 101, 97, 88, 79],
        "share": [0.24, 0.21, 0.20, 0.18, 0.17],
    }
)

table = (
    aesth.GT_aesth(frame, palette="arden", stripe=True)
    .tab_header(title="Regional index", subtitle="Toy frame for the arden table theme")
    .fmt_number(columns="share", decimals=2)
)
table = aesth.highlight_column(table, "index", palette="arden")

html_path = Path(__file__).with_name("table.html")
html_path.write_text(table.as_raw_html())
print(html_path)
