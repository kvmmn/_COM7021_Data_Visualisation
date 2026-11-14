"""Lazy import, Shiny page shell, and Great Tables quiet formatting."""

import os
import subprocess
import sys
from pathlib import Path

import pandas as pd

import aesth

_SRC = Path(__file__).resolve().parents[1] / "src"


def _fresh(code: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(_SRC) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_import_aesth_does_not_load_the_three_engines():
    result = _fresh(
        "import sys\n"
        "import aesth\n"
        "blocked = {'plotnine', 'great_tables', 'shiny'}\n"
        "loaded = sorted(name for name in sys.modules if name.split('.')[0] in blocked)\n"
        "assert loaded == [], loaded\n"
        "assert aesth.__version__ == '0.3.0'\n"
    )
    assert result.returncode == 0, result.stderr


def test_css_build_does_not_load_the_three_engines():
    result = _fresh(
        "import sys\n"
        "import aesth\n"
        "css = aesth.css_aesth('arden')\n"
        "assert '--aesth-paper' in css\n"
        "assert 'background-image: none' in css\n"
        "blocked = {'plotnine', 'great_tables', 'shiny', 'shinyswatch'}\n"
        "loaded = sorted(name for name in sys.modules if name.split('.')[0] in blocked)\n"
        "assert loaded == [], loaded\n"
    )
    assert result.returncode == 0, result.stderr


def test_page_aesth_returns_a_style_tag_without_a_server():
    tag = aesth.page_aesth("carbon", title="æsth")
    assert tag.name == "style"
    text = str(tag)
    assert "background-image: none" in text
    assert "aesth-claim" in text
    assert "bg-gradient" not in text
    assert "indigo" not in text
    assert "shinyswatch" not in sys.modules
    assert "plotnine" not in text


def test_page_css_matches_the_shell_sheet():
    sheet = str(aesth.page_css("noir"))
    assert "aesth palette: noir" in sheet
    assert sheet == str(aesth.page_aesth("noir"))


def test_gt_quiet_formats_and_keeps_the_callers_frame():
    frame = pd.DataFrame(
        {
            "city": ["Leeds", None],
            "index": [1120, 79],
            "share": [0.2, None],
        }
    )
    table = aesth.GT_aesth(frame, palette="arden")
    assert table._tbl_data is frame
    html = table.as_raw_html()
    assert "1,120" in html
    assert "0.20" in html
    assert "&mdash;" in html
    assert "#FFFFFF" in html or "#ffffff" in html.lower()
    assert "gt_title" in html

    plain = aesth.GT_aesth(frame, palette="arden", quiet=False).as_raw_html()
    assert "1,120" not in plain
    assert "&mdash;" not in plain


def test_highlight_column_still_uses_one_accent():
    frame = pd.DataFrame({"city": ["Leeds"], "index": [112]})
    table = aesth.GT_aesth(frame, palette="arden", quiet=False)
    marked = aesth.highlight_column(table, "index", palette="arden")
    html = marked.as_raw_html().lower()
    assert "#66c9ba" in html
