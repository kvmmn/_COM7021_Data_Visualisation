#!/usr/bin/env python3
"""Step 6: Craft a publication-grade, standard-compliant Microsoft Word (.docx) report:
COM7021_Assessment_25199053.docx

Engineered for Arden University COM7021 Assessment submission and Tutor Review (Ahmed Hassan):
- Formal Arden University Cover Page (Page 1) with Student ID 25199053, Assessment Control Table,
  Word Count Compliance Breakdown, Executive KPI Strip (Figure 0), and Academic Integrity Declaration.
- Structured Table of Contents & Inventory of Figures (Figures 0, A, 1–10) and Tables (Tables 1–3) on Page 2.
- Proper WordprocessingML named styles (Normal, Heading1, Heading2, Heading3, Caption, Bibliography, CodeBlock)
  with <w:outlineLvl> so Microsoft Word's Navigation Pane populates automatically.
- Different First Page (<w:titlePg/>) running headers and footers with live PAGE of NUMPAGES fields.
- Explicit <w:tblGrid> and cell widths (<w:tcW>), repeating table headers (<w:tblHeader/>), and row <w:cantSplit/>.
- Non-breaking figure + caption pairing (<w:keepNext/> + <w:keepLines/>) so no caption is ever orphaned.
- Full Arden University Harvard (AU Harvard) referencing standard with hanging indents, DOIs/URLs, and access dates.
- Complete reproducible Python source code in the Appendix.
"""

from __future__ import annotations

import importlib
import re
import sys
import zipfile
from pathlib import Path
from PIL import Image
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
TABLES_DIR = BASE_DIR / "output" / "tables"
FIG_DIR = BASE_DIR / "output" / "figures"
OUT_DOCX = BASE_DIR / "COM7021_Assessment_25199053.docx"

sys.path.insert(0, str(Path(__file__).resolve().parent))
html_builder = importlib.import_module("05_build_review_html")

# Printable width on A4 (11906 dxa width - 2 * 1134 dxa margins = 9638 dxa = 17.0 cm)
PAGE_WIDTH_DXA = 9638


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def parse_inline_html_to_runs(
    html_text: str,
    base_size_half_pt: int = 21,
    base_color: str = "002B49",
    base_italic: bool = False,
    base_bold: bool = False,
    code_bg: str | None = "F0F5F7",
) -> str:
    """Convert inline HTML (<strong>, <em>, <code>, <sub>, entities) into WordprocessingML <w:r> runs."""
    s = html_text.strip()
    s = (
        s.replace("&minus;", "−")
        .replace("&ndash;", "–")
        .replace("&mdash;", "—")
        .replace("&times;", "×")
        .replace("&amp;", "&")
    )
    token_pattern = re.compile(
        r"(<strong>.*?</strong>|<em>.*?</em>|<code>.*?</code>|<sub>.*?</sub>)",
        re.DOTALL,
    )
    tokens = token_pattern.split(s)
    runs_xml: list[str] = []

    def make_run(
        txt: str,
        bold: bool = False,
        italic: bool = False,
        code: bool = False,
        sub: bool = False,
    ) -> str:
        clean = re.sub(r"<[^>]+>", "", txt)
        if not clean:
            return ""
        rpr: list[str] = []
        if code:
            rpr.append(
                '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
            )
            sz = max(16, base_size_half_pt - 2)
            rpr.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
            if code_bg:
                rpr.append(
                    f'<w:shd w:val="clear" w:color="auto" w:fill="{code_bg}"/>'
                )
        else:
            rpr.append('<w:rFonts w:ascii="Aptos" w:hAnsi="Aptos" w:cs="Aptos"/>')
            rpr.append(
                f'<w:sz w:val="{base_size_half_pt}"/><w:szCs w:val="{base_size_half_pt}"/>'
            )
        if bold or base_bold:
            rpr.append("<w:b/><w:bCs/>")
        if italic or base_italic:
            rpr.append("<w:i/><w:iCs/>")
        if sub:
            rpr.append('<w:vertAlign w:val="subscript"/>')
        rpr.append(f'<w:color w:val="{base_color}"/>')
        return f'<w:r><w:rPr>{"".join(rpr)}</w:rPr><w:t xml:space="preserve">{xml_escape(clean)}</w:t></w:r>'

    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("<strong>") and tok.endswith("</strong>"):
            runs_xml.append(make_run(tok[8:-9], bold=True))
        elif tok.startswith("<em>") and tok.endswith("</em>"):
            runs_xml.append(make_run(tok[4:-5], italic=True))
        elif tok.startswith("<code>") and tok.endswith("</code>"):
            runs_xml.append(make_run(tok[6:-7], code=True))
        elif tok.startswith("<sub>") and tok.endswith("</sub>"):
            runs_xml.append(make_run(tok[5:-6], sub=True))
        else:
            runs_xml.append(make_run(tok))
    return "".join(runs_xml)


class DocxBuilder:
    def __init__(self) -> None:
        self.body_elements: list[str] = []
        self.images: list[tuple[str, Path]] = []
        self.doc_pr_id = 1

    def add_page_break(self) -> None:
        self.body_elements.append(
            '<w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr><w:r><w:br w:type="page"/></w:r></w:p>'
        )

    def add_banner_box(self, top_line: str, main_title: str, subtitle: str) -> None:
        """Create a formal Arden Midnight cover banner with Tiffany accent border."""
        p1_runs = parse_inline_html_to_runs(
            top_line, base_size_half_pt=19, base_color="66C9BA", base_bold=True
        )
        p2_runs = parse_inline_html_to_runs(
            main_title, base_size_half_pt=32, base_color="FFFFFF", base_bold=True
        )
        p3_runs = parse_inline_html_to_runs(
            subtitle, base_size_half_pt=20, base_color="E6F5F2", base_italic=False
        )
        tbl = f"""
        <w:tbl>
          <w:tblPr>
            <w:tblW w:w="{PAGE_WIDTH_DXA}" w:type="dxa"/>
            <w:tblBorders>
              <w:top w:val="single" w:sz="24" w:space="0" w:color="66C9BA"/>
              <w:bottom w:val="single" w:sz="18" w:space="0" w:color="3AA89A"/>
              <w:left w:val="none"/><w:right w:val="none"/>
            </w:tblBorders>
            <w:tblCellMar>
              <w:top w:w="180" w:type="dxa"/>
              <w:left w:w="220" w:type="dxa"/>
              <w:bottom w:w="180" w:type="dxa"/>
              <w:right w:w="220" w:type="dxa"/>
            </w:tblCellMar>
          </w:tblPr>
          <w:tblGrid><w:gridCol w:w="{PAGE_WIDTH_DXA}"/></w:tblGrid>
          <w:tr>
            <w:tc>
              <w:tcPr>
                <w:tcW w:w="{PAGE_WIDTH_DXA}" w:type="dxa"/>
                <w:shd w:val="clear" w:color="auto" w:fill="002B49"/>
              </w:tcPr>
              <w:p>
                <w:pPr><w:spacing w:before="0" w:after="80"/></w:pPr>
                {p1_runs}
              </w:p>
              <w:p>
                <w:pPr><w:spacing w:before="0" w:after="80" w:line="260" w:lineRule="auto"/></w:pPr>
                {p2_runs}
              </w:p>
              <w:p>
                <w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr>
                {p3_runs}
              </w:p>
            </w:tc>
          </w:tr>
        </w:tbl>"""
        self.body_elements.append(tbl)

    def add_heading(self, text: str, level: int = 1) -> None:
        style_id = f"Heading{level}"
        outline_lvl = max(0, min(2, level - 1))
        if level == 1:
            sz = 28  # 14pt
            color = "002B49"
            before = 240
            after = 110
            bdr = '<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="3AA89A"/></w:pBdr>'
        elif level == 2:
            sz = 24  # 12pt
            color = "002B49"
            before = 200
            after = 80
            bdr = '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="3" w:color="C9D5DD"/></w:pBdr>'
        else:
            sz = 22  # 11pt
            color = "1A4A6B"
            before = 160
            after = 60
            bdr = '<w:pBdr><w:left w:val="single" w:sz="18" w:space="6" w:color="66C9BA"/></w:pBdr>'
        runs = parse_inline_html_to_runs(
            text, base_size_half_pt=sz, base_color=color, base_bold=True
        )
        p = f"""
        <w:p>
          <w:pPr>
            <w:pStyle w:val="{style_id}"/>
            <w:keepNext/>
            <w:keepLines/>
            <w:outlineLvl w:val="{outline_lvl}"/>
            <w:spacing w:before="{before}" w:after="{after}" w:line="260" w:lineRule="auto"/>
            {bdr}
          </w:pPr>
          {runs}
        </w:p>"""
        self.body_elements.append(p)

    def add_paragraph_html(
        self,
        html_p: str,
        align: str = "both",
        space_before: int = 0,
        space_after: int = 115,
        size_half_pt: int = 21,
        color: str = "002B49",
        italic: bool = False,
        hanging_twips: int = 0,
        left_twips: int = 0,
        keep_next: bool = False,
        keep_lines: bool = False,
        style_id: str = "Normal",
        left_border_color: str | None = None,
        fill_color: str | None = None,
    ) -> None:
        inner = re.sub(
            r"^\s*<p[^>]*>|</p>\s*$", "", html_p.strip(), flags=re.DOTALL
        )
        runs = parse_inline_html_to_runs(
            inner,
            base_size_half_pt=size_half_pt,
            base_color=color,
            base_italic=italic,
        )
        ind_xml = ""
        if hanging_twips or left_twips:
            ind_xml = f'<w:ind w:left="{left_twips}" w:hanging="{hanging_twips}"/>'
        kn_xml = "<w:keepNext/>" if keep_next else ""
        kl_xml = "<w:keepLines/>" if keep_lines else ""
        bdr_xml = (
            f'<w:pBdr><w:left w:val="single" w:sz="12" w:space="8" w:color="{left_border_color}"/></w:pBdr>'
            if left_border_color
            else ""
        )
        shd_xml = (
            f'<w:shd w:val="clear" w:color="auto" w:fill="{fill_color}"/>'
            if fill_color
            else ""
        )
        p = f"""
        <w:p>
          <w:pPr>
            <w:pStyle w:val="{style_id}"/>
            {kn_xml}
            {kl_xml}
            {bdr_xml}
            {shd_xml}
            <w:jc w:val="{align}"/>
            <w:spacing w:before="{space_before}" w:after="{space_after}" w:line="276" w:lineRule="auto"/>
            {ind_xml}
          </w:pPr>
          {runs}
        </w:p>"""
        self.body_elements.append(p)

    def add_html_block(self, block: str) -> None:
        """Convert an HTML fragment containing <h3>, <p>, <ol>/<li> into styled Word paragraphs."""
        token_re = re.compile(
            r"(<h3[^>]*>.*?</h3>|<p[^>]*>.*?</p>|<li[^>]*>.*?</li>)", re.DOTALL
        )
        item_idx = 0
        for m in token_re.finditer(block):
            chunk = m.group(0)
            if chunk.startswith("<h3"):
                item_idx = 0
                txt = re.sub(
                    r"^<h3[^>]*>|</h3>$", "", chunk.strip(), flags=re.DOTALL
                )
                self.add_heading(txt, level=3)
            elif chunk.startswith("<p"):
                item_idx = 0
                self.add_paragraph_html(chunk)
            elif chunk.startswith("<li"):
                item_idx += 1
                inner = re.sub(
                    r"^<li[^>]*>|</li>$", "", chunk.strip(), flags=re.DOTALL
                )
                numbered = f"<strong>{item_idx}.</strong> {inner}"
                self.add_paragraph_html(
                    numbered,
                    left_twips=360,
                    hanging_twips=240,
                    space_after=105,
                )

    def add_image(
        self, filename: str, caption_html: str, max_width_cm: float = 16.2
    ) -> None:
        img_path = FIG_DIR / filename
        r_id = f"rIdImg{len(self.images) + 1}"
        self.images.append((r_id, img_path))
        with Image.open(img_path) as im:
            w_px, h_px = im.size
        cx = int(max_width_cm * 360000)
        cy = int(cx * (h_px / w_px))
        doc_id = self.doc_pr_id
        self.doc_pr_id += 1

        img_p = f"""
        <w:p>
          <w:pPr>
            <w:jc w:val="center"/>
            <w:keepNext/>
            <w:keepLines/>
            <w:spacing w:before="120" w:after="40"/>
          </w:pPr>
          <w:r>
            <w:drawing>
              <wp:inline distT="0" distB="0" distL="0" distR="0">
                <wp:extent cx="{cx}" cy="{cy}"/>
                <wp:docPr id="{doc_id}" name="Figure_{doc_id}" descr="{xml_escape(filename)}"/>
                <wp:cNvGraphicFramePr>
                  <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
                </wp:cNvGraphicFramePr>
                <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                  <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
                    <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
                      <pic:nvPicPr>
                        <pic:cNvPr id="{doc_id}" name="{xml_escape(filename)}"/>
                        <pic:cNvPicPr/>
                      </pic:nvPicPr>
                      <pic:blipFill>
                        <a:blip r:embed="{r_id}"/>
                        <a:stretch><a:fillRect/></a:stretch>
                      </pic:blipFill>
                      <pic:spPr>
                        <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
                        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                      </pic:spPr>
                    </pic:pic>
                  </a:graphicData>
                </a:graphic>
              </wp:inline>
            </w:drawing>
          </w:r>
        </w:p>"""
        self.body_elements.append(img_p)
        self.add_paragraph_html(
            caption_html,
            align="both",
            space_before=20,
            space_after=160,
            size_half_pt=18,
            color="1A4A6B",
            keep_lines=True,
            style_id="Caption",
            left_border_color="3AA89A",
            fill_color="F7FAFB",
        )

    def add_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        col_widths_pct: list[float] | None = None,
        col_aligns: list[str] | None = None,
        highlight_rows: set[int] | None = None,
        caption_html: str | None = None,
        font_half_pt: int = 17,
    ) -> None:
        n_cols = len(headers)
        if col_aligns is None:
            col_aligns = ["left"] * n_cols
        if highlight_rows is None:
            highlight_rows = set()
        if col_widths_pct is None:
            col_widths_pct = [100.0 / n_cols] * n_cols

        col_dxa = [int(round(PAGE_WIDTH_DXA * (p / 100.0))) for p in col_widths_pct]
        col_dxa[-1] += PAGE_WIDTH_DXA - sum(col_dxa)

        grid_xml = "".join(f'<w:gridCol w:w="{w}"/>' for w in col_dxa)

        header_cells = []
        for idx, h in enumerate(headers):
            al = col_aligns[idx]
            w = col_dxa[idx]
            runs = parse_inline_html_to_runs(
                h,
                base_size_half_pt=font_half_pt,
                base_color="FFFFFF",
                base_bold=True,
                code_bg=None,
            )
            header_cells.append(f"""
            <w:tc>
              <w:tcPr>
                <w:tcW w:w="{w}" w:type="dxa"/>
                <w:shd w:val="clear" w:color="auto" w:fill="002B49"/>
                <w:vAlign w:val="center"/>
              </w:tcPr>
              <w:p>
                <w:pPr><w:jc w:val="{al}"/><w:spacing w:before="40" w:after="40" w:line="220" w:lineRule="auto"/></w:pPr>
                {runs}
              </w:p>
            </w:tc>""")

        body_rows_xml = [
            f"<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>{''.join(header_cells)}</w:tr>"
        ]

        for r_idx, row in enumerate(rows):
            if r_idx in highlight_rows:
                fill = "E6F5F2"
            elif r_idx % 2 == 1:
                fill = "F7FAFB"
            else:
                fill = "FFFFFF"
            row_cells = []
            for c_idx, cell_val in enumerate(row):
                al = col_aligns[c_idx]
                w = col_dxa[c_idx]
                runs = parse_inline_html_to_runs(
                    cell_val,
                    base_size_half_pt=font_half_pt,
                    base_color="002B49",
                    base_bold=(r_idx in highlight_rows and c_idx == 0),
                    code_bg=None,
                )
                row_cells.append(f"""
                <w:tc>
                  <w:tcPr>
                    <w:tcW w:w="{w}" w:type="dxa"/>
                    <w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>
                    <w:vAlign w:val="center"/>
                  </w:tcPr>
                  <w:p>
                    <w:pPr><w:jc w:val="{al}"/><w:spacing w:before="30" w:after="30" w:line="220" w:lineRule="auto"/></w:pPr>
                    {runs}
                  </w:p>
                </w:tc>""")
            body_rows_xml.append(
                f"<w:tr><w:trPr><w:cantSplit/></w:trPr>{''.join(row_cells)}</w:tr>"
            )

        tbl_xml = f"""
        <w:tbl>
          <w:tblPr>
            <w:tblW w:w="{PAGE_WIDTH_DXA}" w:type="dxa"/>
            <w:tblBorders>
              <w:top w:val="single" w:sz="10" w:space="0" w:color="002B49"/>
              <w:bottom w:val="single" w:sz="10" w:space="0" w:color="002B49"/>
              <w:insideH w:val="single" w:sz="4" w:space="0" w:color="D5DEE3"/>
              <w:left w:val="none"/>
              <w:right w:val="none"/>
              <w:insideV w:val="none"/>
            </w:tblBorders>
            <w:tblCellMar>
              <w:top w:w="45" w:type="dxa"/>
              <w:left w:w="75" w:type="dxa"/>
              <w:bottom w:w="45" w:type="dxa"/>
              <w:right w:w="75" w:type="dxa"/>
            </w:tblCellMar>
          </w:tblPr>
          <w:tblGrid>{grid_xml}</w:tblGrid>
          {''.join(body_rows_xml)}
        </w:tbl>"""
        self.body_elements.append(tbl_xml)
        if caption_html:
            self.add_paragraph_html(
                caption_html,
                align="both",
                space_before=40,
                space_after=150,
                size_half_pt=18,
                color="1A4A6B",
                keep_lines=True,
                style_id="Caption",
                left_border_color="3AA89A",
                fill_color="F7FAFB",
            )

    def add_code_listing(self, title: str, code_text: str) -> None:
        self.add_heading(f"Module Listing: <code>{title}</code>", level=3)
        lines = code_text.splitlines()
        run_lines = []
        for idx, line in enumerate(lines):
            br = "<w:br/>" if idx < len(lines) - 1 else ""
            run_lines.append(
                f'<w:t xml:space="preserve">{xml_escape(line)}</w:t>{br}'
            )
        p = f"""
        <w:p>
          <w:pPr>
            <w:pStyle w:val="CodeBlock"/>
            <w:shd w:val="clear" w:color="auto" w:fill="F4F8FA"/>
            <w:pBdr>
              <w:top w:val="single" w:sz="4" w:space="4" w:color="C9D5DD"/>
              <w:left w:val="single" w:sz="16" w:space="6" w:color="3AA89A"/>
              <w:bottom w:val="single" w:sz="4" w:space="4" w:color="C9D5DD"/>
              <w:right w:val="single" w:sz="4" w:space="4" w:color="C9D5DD"/>
            </w:pBdr>
            <w:spacing w:before="60" w:after="140" w:line="210" w:lineRule="auto"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>
              <w:sz w:val="15"/>
              <w:szCs w:val="15"/>
              <w:color w:val="002B49"/>
            </w:rPr>
            {''.join(run_lines)}
          </w:r>
        </w:p>"""
        self.body_elements.append(p)

    def save(self, out_path: Path) -> None:
        content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
  <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
  <Override PartName="/word/header2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
  <Override PartName="/word/footer2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""

        root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rIdCore" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rIdApp" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""

        core_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>COM7021 Data Visualisation Assessment Report — Student ID 25199053</dc:title>
  <dc:subject>Sustainable Urban Mobility Performance Across European Cities ([5442] EcoMoveMobility.xlsx)</dc:subject>
  <dc:creator>Student ID: 25199053 (Arden University Berlin)</dc:creator>
  <cp:keywords>COM7021, Data Visualisation, Python, EcoMove, Arden University, 25199053</cp:keywords>
  <dc:description>COM7021 Assessment Submission (Task 1 Data Visualisation Investigation in Python &amp; Task 2 Critical Report)</dc:description>
  <cp:revision>2</cp:revision>
</cp:coreProperties>"""

        app_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
  <Application>Microsoft Office Word</Application>
  <Company>Arden University</Company>
</Properties>"""

        settings_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:zoom w:percent="100"/>
  <w:MirrorMargins w:val="false"/>
  <w:updateFields w:val="true"/>
</w:settings>"""

        doc_rel_items = [
            '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>',
            '<Relationship Id="rIdHeader1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>',
            '<Relationship Id="rIdFooter1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>',
            '<Relationship Id="rIdHeader2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header2.xml"/>',
            '<Relationship Id="rIdFooter2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer2.xml"/>',
        ]
        for r_id, img_path in self.images:
            doc_rel_items.append(
                f'<Relationship Id="{r_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{img_path.name}"/>'
            )
        doc_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {''.join(doc_rel_items)}
</Relationships>"""

        styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Aptos" w:hAnsi="Aptos" w:cs="Aptos"/>
        <w:sz w:val="21"/>
        <w:szCs w:val="21"/>
        <w:color w:val="002B49"/>
        <w:lang w:val="en-GB"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="115" w:line="276" w:lineRule="auto"/>
        <w:jc w:val="both"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:spacing w:before="240" w:after="110"/>
      <w:outlineLvl w:val="0"/>
    </w:pPr>
    <w:rPr>
      <w:b/><w:bCs/>
      <w:color w:val="002B49"/>
      <w:sz w:val="28"/><w:szCs w:val="28"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:spacing w:before="200" w:after="80"/>
      <w:outlineLvl w:val="1"/>
    </w:pPr>
    <w:rPr>
      <w:b/><w:bCs/>
      <w:color w:val="002B49"/>
      <w:sz w:val="24"/><w:szCs w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:spacing w:before="160" w:after="60"/>
      <w:outlineLvl w:val="2"/>
    </w:pPr>
    <w:rPr>
      <w:b/><w:bCs/>
      <w:color w:val="1A4A6B"/>
      <w:sz w:val="22"/><w:szCs w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="caption"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepLines/>
      <w:spacing w:before="20" w:after="150"/>
    </w:pPr>
    <w:rPr>
      <w:color w:val="1A4A6B"/>
      <w:sz w:val="18"/><w:szCs w:val="18"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Bibliography">
    <w:name w:val="Bibliography"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:ind w:left="420" w:hanging="420"/>
      <w:spacing w:before="0" w:after="90" w:line="260" w:lineRule="auto"/>
    </w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="CodeBlock">
    <w:name w:val="Code Block"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:jc w:val="left"/>
      <w:spacing w:before="60" w:after="140" w:line="210" w:lineRule="auto"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>
      <w:sz w:val="15"/><w:szCs w:val="15"/>
    </w:rPr>
  </w:style>
</w:styles>"""

        # Running header & footer for Pages 2+
        header1_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:jc w:val="right"/>
      <w:pBdr><w:bottom w:val="single" w:sz="6" w:space="3" w:color="66C9BA"/></w:pBdr>
    </w:pPr>
    <w:r>
      <w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:b/><w:sz w:val="17"/><w:color w:val="002B49"/></w:rPr>
      <w:t xml:space="preserve">COM7021 Data Visualisation </w:t>
    </w:r>
    <w:r>
      <w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="17"/><w:color w:val="5A6B75"/></w:rPr>
      <w:t xml:space="preserve">· Assessment Submission Report · Student ID: 25199053</w:t>
    </w:r>
  </w:p>
</w:hdr>"""

        footer1_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:jc w:val="center"/>
      <w:pBdr><w:top w:val="single" w:sz="4" w:space="3" w:color="D5DEE3"/></w:pBdr>
    </w:pPr>
    <w:r>
      <w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="17"/><w:color w:val="5A6B75"/></w:rPr>
      <w:t xml:space="preserve">Arden University Berlin · MSc Data Science · Student ID: 25199053 · Page </w:t>
    </w:r>
    <w:fldSimple w:instr="PAGE"/>
    <w:r>
      <w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="17"/><w:color w:val="5A6B75"/></w:rPr>
      <w:t xml:space="preserve"> of </w:t>
    </w:r>
    <w:fldSimple w:instr="NUMPAGES"/>
  </w:p>
</w:ftr>"""

        # Cover page header & footer (minimal / discreet)
        header2_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p/>
</w:hdr>"""

        footer2_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:jc w:val="center"/>
      <w:pBdr><w:top w:val="single" w:sz="4" w:space="3" w:color="D5DEE3"/></w:pBdr>
    </w:pPr>
    <w:r>
      <w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="16"/><w:color w:val="5A6B75"/></w:rPr>
      <w:t>Arden University · COM7021 Data Visualisation Assessment Submission · Student ID: 25199053 · Cover Sheet</w:t>
    </w:r>
  </w:p>
</w:ftr>"""

        document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">
  <w:body>
    {''.join(self.body_elements)}
    <w:sectPr>
      <w:headerReference w:type="default" r:id="rIdHeader1"/>
      <w:footerReference w:type="default" r:id="rIdFooter1"/>
      <w:headerReference w:type="first" r:id="rIdHeader2"/>
      <w:footerReference w:type="first" r:id="rIdFooter2"/>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="680" w:footer="680" w:gutter="0"/>
      <w:titlePg/>
    </w:sectPr>
  </w:body>
</w:document>"""

        with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", content_types)
            zf.writestr("_rels/.rels", root_rels)
            zf.writestr("docProps/core.xml", core_xml)
            zf.writestr("docProps/app.xml", app_xml)
            zf.writestr("word/_rels/document.xml.rels", doc_rels)
            zf.writestr("word/styles.xml", styles_xml)
            zf.writestr("word/settings.xml", settings_xml)
            zf.writestr("word/header1.xml", header1_xml)
            zf.writestr("word/footer1.xml", footer1_xml)
            zf.writestr("word/header2.xml", header2_xml)
            zf.writestr("word/footer2.xml", footer2_xml)
            zf.writestr("word/document.xml", document_xml)
            written_media = set()
            for _, img_path in self.images:
                if img_path.name not in written_media:
                    zf.write(img_path, f"word/media/{img_path.name}")
                    written_media.add(img_path.name)


def build_word_document() -> None:
    doc = DocxBuilder()

    t1_words = (
        html_builder.count_words(html_builder.TASK1_SEC_1_1)
        + html_builder.count_words(html_builder.TASK1_SEC_1_2)
        + html_builder.count_words(html_builder.TASK1_FIG1_TEXT)
        + html_builder.count_words(html_builder.TASK1_FIG2_TEXT)
        + html_builder.count_words(html_builder.TASK1_FIG3_TEXT)
        + html_builder.count_words(html_builder.TASK1_FIG4_TEXT)
        + html_builder.count_words(html_builder.TASK1_FIG5_TEXT)
        + html_builder.count_words(html_builder.TASK1_FIG6_8_TEXT)
    )
    t2_words = (
        html_builder.count_words(html_builder.TASK2_SEC_2_1)
        + html_builder.count_words(html_builder.TASK2_SEC_2_2)
        + html_builder.count_words(html_builder.TASK2_SEC_2_3)
        + html_builder.count_words(html_builder.TASK2_SEC_2_4)
    )

    # ==========================================================================
    # PAGE 1: FORMAL ARDEN UNIVERSITY ASSESSMENT COVER PAGE
    # ==========================================================================
    doc.add_banner_box(
        "ARDEN UNIVERSITY BERLIN · SCHOOL OF COMPUTING &amp; DATA SCIENCE · MSc DATA SCIENCE",
        "Sustainable Urban Mobility Performance Across European Cities: A Python Data Visualisation Investigation and Critical Report",
        "COM7021 Data Visualisation Assessment Submission (100% Weighting · LO1–LO4) · Dataset: [5442] EcoMoveMobility.xlsx",
    )

    doc.add_paragraph_html(
        "<p><strong>Assessment Control &amp; Submission Specification</strong></p>",
        space_before=140,
        space_after=60,
        size_half_pt=22,
        keep_next=True,
    )

    cover_headers = ["Submission Parameter", "Details &amp; Verification"]
    cover_rows = [
        ["<strong>Student ID Number</strong>", "<strong>25199053</strong>"],
        ["<strong>Module Code &amp; Title</strong>", "COM7021 (COM7021SCC) — Data Visualisation"],
        ["<strong>Degree Programme</strong>", "MSc Data Science (Arden University Berlin)"],
        ["<strong>Module Tutor</strong>", "Ahmed Hassan"],
        ["<strong>Assignment Format</strong>", "Single Word Report (<code>.docx</code>) with Python Verification Appendix"],
        ["<strong>Authoritative Dataset</strong>", "<code>[5442] EcoMoveMobility.xlsx</code> (5,000 daily records × 18 columns; 12 European cities, 2024–2025)"],
        [
            "<strong>Task 1 Allocation (70 Marks · LO1 &amp; LO2)</strong>",
            f"1,500 words equivalent (Practical Python Investigation, 8 Charts + Interactive Dashboard) + <strong>{t1_words} written words</strong> (Nominal target: ~600 words)",
        ],
        [
            "<strong>Task 2 Allocation (30 Marks · LO3 &amp; LO4)</strong>",
            f"<strong>{t2_words} written words</strong> (Nominal target: ~900 words; Critical Evaluation &amp; Evidence-Supported Recommendations)",
        ],
        [
            "<strong>Total Assessment Word Count</strong>",
            f"<strong>{t1_words + t2_words} written prose words</strong> + 1,500 words equivalent practical work (Total: ~3,000 words equivalent)",
        ],
        ["<strong>Referencing Standard</strong>", "Arden University Harvard Referencing (AU Harvard)"],
    ]
    doc.add_table(
        cover_headers,
        cover_rows,
        col_widths_pct=[32.0, 68.0],
        col_aligns=["left", "left"],
        highlight_rows={0, 6, 7, 8},
        font_half_pt=18,
    )

    doc.add_image(
        "fig00_executive_kpi_strip.png",
        "<strong>Figure 0 (Executive Summary Strip):</strong> Baseline 2024–2025 operational metrics across 5,000 daily records in 12 European cities. Tiffany-bordered tiles highlight surface delay bottlenecks (mean 4.35 min; Bus 6.58 min) and aggregate vs modal cost-recovery divergence (99.6% overall network recovery vs 84.1% unweighted record average; Bike Share 5.2%).",
        max_width_cm=16.2,
    )

    doc.add_paragraph_html(
        "<p><strong>Declaration of Academic Integrity:</strong> I confirm that this assessment submission (Student ID: <code>25199053</code>) is my own original work produced in Python for module <code>COM7021 Data Visualisation</code>, that all external academic and policy sources are acknowledged in accordance with Arden University Harvard Referencing guidelines, and that the complete reproducible Python source code is provided in the Appendix.</p>",
        space_before=40,
        space_after=60,
        size_half_pt=18,
        color="5A6B75",
        left_border_color="002B49",
        fill_color="F7FAFB",
        keep_lines=True,
    )

    doc.add_page_break()

    # ==========================================================================
    # PAGE 2: STRUCTURED TABLE OF CONTENTS & VISUALISATION / TABLE INVENTORY
    # ==========================================================================
    doc.add_heading("Document Structure, Learning Outcomes & Visualisation Inventory", level=1)
    doc.add_paragraph_html(
        "<p>This report is structured as a single connected analytical investigation linking Python data preparation and multi-technique visual exploration (<strong>Task 1</strong>, 70 Marks) to critical perceptual evaluation, methodological reflection, and evidence-supported policy appraisal (<strong>Task 2</strong>, 30 Marks).</p>"
    )

    toc_headers = ["Section", "Report Section Title", "Assessed LOs", "Weight / Allocation"]
    toc_rows = [
        ["<strong>Task 1</strong>", "<strong>Data Visualisation Investigation in Python</strong>", "<strong>LO1, LO2</strong>", "<strong>70 Marks (~600w + 1,500w eq.)</strong>"],
        ["Section 1.1", "Data Importing, Hygiene Audit, and Feature Engineering (Figure A)", "LO2", "Data Preparation Pipeline"],
        ["Section 1.2", "Initial Descriptive Statistics and Financial Aggregation Basis (Table 1)", "LO2", "Parametric &amp; Non-Parametric EDA"],
        ["Section 1.3", "Visualisation Investigation and Decision Justification (Figures 1 to 8)", "LO1, LO2", "8 Distinct Non-Repeating Charts"],
        ["Section 1.4", "Interactive Python Decision Dashboard (Figures 9 and 10)", "LO1, LO2, LO3", "Multi-Filter Plotly Application"],
        ["<strong>Task 2</strong>", "<strong>Critical Report on Visualisation and Decision-Making</strong>", "<strong>LO1, LO2, LO3, LO4</strong>", "<strong>30 Marks (~900 words)</strong>"],
        ["Section 2.1", "Critical Justification of Visualisation Design for Technical &amp; Non-Technical Audiences", "LO1, LO3", "Perceptual Psychology &amp; Encoding"],
        ["Section 2.2", "Critical Synthesis of Findings and Methodological Reflections (Table 2)", "LO2, LO3", "Financial, Compositional &amp; Causal Rigour"],
        ["Section 2.3", "Critical Evaluation of Dashboard Effectiveness and Analytical Limitations", "LO1, LO3", "Shneiderman Mantra &amp; Constraints"],
        ["Section 2.4", "Evidence-Supported Recommendations and Decision-Making Value (Table 3)", "LO3, LO4", "Pilot &amp; Feasibility Appraisal"],
        ["<strong>References</strong>", "<strong>Arden University Harvard (AU Harvard) Reference List</strong>", "<strong>LO1, LO4</strong>", "<strong>12 Peer-Reviewed &amp; Policy Sources</strong>"],
        ["<strong>Appendix</strong>", "<strong>Complete Reproducible Python Source Code (5 Modules)</strong>", "<strong>LO2</strong>", "<strong>Full Verification Code</strong>"],
    ]
    doc.add_table(
        toc_headers,
        toc_rows,
        col_widths_pct=[14.0, 50.0, 14.0, 22.0],
        col_aligns=["left", "left", "left", "left"],
        highlight_rows={0, 5, 10, 11},
        font_half_pt=17,
    )

    doc.add_heading("Inventory of Visualisations (Figures 0, A, and 1 to 10) and Summary Tables", level=2)
    inv_headers = ["Ref", "Visualisation Technique / Table Type", "Analytical Dimension &amp; Brief Requirement Satisfied"]
    inv_rows = [
        ["<strong>Figure 0</strong>", "Executive KPI Summary Strip (SVG/PNG)", "Baseline network KPIs highlighting surface delay and overall vs record-mean cost recovery."],
        ["<strong>Figure A</strong>", "Five-Stage Analytical Workflow Diagram", "Reproducible Python pipeline from Excel serial-date parsing to dashboard deployment."],
        ["<strong>Figure 1</strong>", "Dual-Series Time-Series Line + Shaded Regime Ribbon", "<em>Requirement 1 (Time-Series):</em> Monthly demand (2024–2025), +34.1% weekday premium &amp; Oct trough."],
        ["<strong>Figure 2</strong>", "Connected Dumbbell Plot (Direct Standardisation)", "<em>Requirement 2 (City Comparison):</em> Raw vs modal-mix-adjusted city margins (Simpson's Paradox)."],
        ["<strong>Figure 3</strong>", "Two-Panel Horizontal Bar Chart (Unit Economics)", "<em>Requirement 2 &amp; 5 (Mode Comparison &amp; Financials):</em> Fare vs cost per passenger &amp; €/tCO<sub>2</sub> return."],
        ["<strong>Figure 4</strong>", "Raincloud Plot (Half-Violin KDE + Boxplot + Jitter)", "<em>Requirement 4 (Distribution):</em> Service delay dispersion &amp; tail risk across transport modes."],
        ["<strong>Figure 5</strong>", "Joint Scatter + OLS Regression + Marginal KDEs", "<em>Requirement 3 (Relationship):</em> Observational delay vs rating association (<em>r</em> = &minus;0.821) &amp; Event Days."],
        ["<strong>Figure 6</strong>", "Dual-Encoded 6×6 Interaction Heatmap", "<em>Requirement 3 (Multivariate Interaction):</em> Weather × Mode delay escalation (+119.4% in Snow)."],
        ["<strong>Figure 7</strong>", "Two-Way Normalised Rate Bar + 6×6 Matrix", "<em>Requirement 2 &amp; 5 (Route Accessibility):</em> Volume-weighted complaints per 10,000 passengers."],
        ["<strong>Figure 8</strong>", "Multi-Dimensional Modal Performance Matrix", "<em>Requirement 5 (Performance Indicator):</em> Cross-modal synthesis of demand, delay, recovery &amp; CO<sub>2</sub>/kWh."],
        ["<strong>Figure 9</strong>", "Interactive Dashboard Screenshot (Unfiltered)", "<em>Requirement 6 (Dashboard Overview):</em> Default baseline state (<em>N</em> = 5,000 records across 12 cities)."],
        ["<strong>Figure 10</strong>", "Interactive Dashboard Screenshot (Filtered Scenario)", "<em>Requirement 6 (Dashboard Scenario):</em> Surface modes under Rain &amp; Snow (<em>n</em> = 583 records)."],
        ["<strong>Table 1</strong>", "Parametric &amp; Non-Parametric Summary Table", "Initial descriptive statistics (Mean, SD, Median, Q25, Q75, IQR, Min, Max, Skewness) for 15 variables."],
        ["<strong>Table 2</strong>", "12-City Comparative Performance Table", "Cumulative vs per-record city margins and volume-weighted vs record-mean cost recovery."],
        ["<strong>Table 3</strong>", "Evidence-Supported Policy Appraisal Matrix", "Links empirical visual findings to candidate interventions for pilot evaluation and feasibility appraisal."],
    ]
    doc.add_table(
        inv_headers,
        inv_rows,
        col_widths_pct=[13.0, 37.0, 50.0],
        col_aligns=["left", "left", "left"],
        highlight_rows={2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
        font_half_pt=16,
    )

    doc.add_page_break()

    # ==========================================================================
    # TASK 1: DATA VISUALISATION INVESTIGATION IN PYTHON (70 MARKS)
    # ==========================================================================
    doc.add_heading(
        f"Task 1 — Data Visualisation Investigation in Python (LO1 &amp; LO2 · 70 Marks · {t1_words} Words)",
        level=1,
    )

    doc.add_heading("1.1 Data Importing, Hygiene Audit, and Feature Engineering", level=2)
    doc.add_html_block(html_builder.TASK1_SEC_1_1)
    doc.add_image(
        "fig00_methodology_pipeline.png",
        "<strong>Figure A (Investigation Workflow):</strong> Five-stage Python analytical pipeline from raw Excel ingestion and serial-date conversion (<code>origin='1899-12-30'</code>) to normalised feature engineering, static 220 DPI chart generation, and interactive multi-filter dashboard deployment.",
    )

    doc.add_heading("1.2 Initial Descriptive Statistics and Financial Aggregation Basis", level=2)
    doc.add_html_block(html_builder.TASK1_SEC_1_2)

    stats_df = pd.read_csv(TABLES_DIR / "table01_initial_statistics.csv")
    t1_headers = [
        "Variable",
        "N",
        "Miss",
        "Mean",
        "SD",
        "Median",
        "Q25",
        "Q75",
        "IQR",
        "Min",
        "Max",
        "Skew",
    ]
    t1_rows = []
    for _, r in stats_df.iterrows():
        t1_rows.append([
            f"<code>{r['Variable']}</code>",
            f"{int(r['Count']):,}",
            f"{int(r['Missing'])}",
            f"{r['Mean']:,.2f}",
            f"{r['SD']:,.2f}",
            f"{r['Median']:,.2f}",
            f"{r['Q25']:,.2f}",
            f"{r['Q75']:,.2f}",
            f"{r['IQR']:,.2f}",
            f"{r['Min']:,.2f}",
            f"{r['Max']:,.2f}",
            f"{r['Skewness']:+.2f}",
        ])
    doc.add_table(
        t1_headers,
        t1_rows,
        col_widths_pct=[21.0, 6.0, 5.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 7.0, 8.0, 5.0],
        col_aligns=["left"] + ["right"] * 11,
        highlight_rows={9, 10, 13},
        caption_html="<strong>Table 1:</strong> Initial parametric and non-parametric descriptive statistics for raw and derived numerical variables across all <code>N = 5,000</code> daily records (generated via <code>scripts/01_data_prep_and_eda.py</code>). Note that <code>Cost_Recovery_Pct</code> mean (84.12%) reflects the unweighted average of daily record ratios, whereas volume-weighted overall cost recovery (<code>Sum Revenue / Sum Cost</code>) is 99.58%.",
        font_half_pt=15,
    )

    doc.add_heading("1.3 Visualisation Investigation and Decision Justification (Figures 1 to 8)", level=2)

    doc.add_html_block(html_builder.TASK1_FIG1_TEXT)
    doc.add_image(
        "fig01_monthly_demand_trend.png",
        "<strong>Figure 1 (Time-Series &amp; Regime Decomposition):</strong> Monthly mean daily passenger demand across 2024–2025, decomposing the +34.1% weekday commute premium (shaded ribbon) and contrasting recurring March–April spring peaks with the &minus;27.2% October trough.",
    )

    doc.add_html_block(html_builder.TASK1_FIG2_TEXT)
    doc.add_image(
        "fig02_city_demand_comparison.png",
        "<strong>Figure 2 (Connected Dumbbell Plot — Simpson's Paradox):</strong> Unadjusted raw mean net margin per record versus modal-mix-adjusted net margin per record across the 12 European cities. Direct standardisation controls for modal sampling share (<em>r</em> = &minus;0.795), shifting Berlin from Rank #4 (+€35.65/record) to Rank #11 (&minus;€353.87/record) while Madrid improves from &minus;€702.29 to &minus;€268.04/record.",
    )

    doc.add_html_block(html_builder.TASK1_FIG3_TEXT)
    doc.add_image(
        "fig03_mode_cost_recovery.png",
        "<strong>Figure 3 (Two-Panel Unit Economics &amp; Carbon Abatement Return):</strong> Panel A compares aggregate per-passenger ticket fare against operating cost across modes, illustrating negative per-trip unit margins in Bike Share (&minus;€20.84/trip; 5.25% overall recovery) and E-Scooter (&minus;€19.98/trip; 7.39% recovery). Panel B reports cumulative 2-year net margins (€M) and net public-finance return per tonne of CO<sub>2</sub> saved.",
    )

    doc.add_html_block(html_builder.TASK1_FIG4_TEXT)
    doc.add_image(
        "fig04_delay_distribution_boxplot.png",
        "<strong>Figure 4 (Distribution Visualisation — Raincloud Plot):</strong> Raincloud distribution combining half-violin Gaussian KDE densities, Tukey boxplots (median and IQR), and jittered daily observations across modes. Bus exhibits the widest delay distribution (median 6.50 min, mean 6.58 min, max 12.50 min).",
    )

    doc.add_html_block(html_builder.TASK1_FIG5_TEXT)
    doc.add_image(
        "fig05_delay_rating_relationship.png",
        "<strong>Figure 5 (Joint Bivariate Relationship &amp; Marginal Density Projections):</strong> Observational association between average service delay and customer satisfaction rating (<em>r</em> = &minus;0.821, OLS slope &minus;0.14 pts/min; <em>N</em> = 5,000), with top and right marginal KDE strips comparing Standard Days (<em>n</em> = 4,490) against Major Event Days (<em>n</em> = 510).",
    )

    doc.add_html_block(html_builder.TASK1_FIG6_8_TEXT)
    doc.add_image(
        "fig06_weather_mode_delay_heatmap.png",
        "<strong>Figure 6 (Dual-Encoded Weather × Mode Interaction Heatmap):</strong> Mean service delay (minutes) and percentage escalation relative to Clear weather across transport modes and weather conditions.",
    )
    doc.add_image(
        "fig07_route_accessibility_rate.png",
        "<strong>Figure 7 (Two-Way Accessibility Complaint Rate Matrix):</strong> Volume-weighted aggregate accessibility complaints per 10,000 passengers by route type (Panel A) and across the 6×6 Route × Mode interaction matrix (Panel B), isolating elevated complaint intensity on Suburban Feeder micromobility services (E-Scooter: 54.02/10k aggregate; Bike Share: 49.26/10k aggregate).",
    )
    doc.add_image(
        "fig08_mode_performance_matrix.png",
        "<strong>Figure 8 (Multi-Dimensional Modal Performance Matrix):</strong> Cross-modal summary comparing passenger demand share, mean service delay, overall cost-recovery ratio, environmental efficiency (<code>CO2 / kWh</code>), and aggregate accessibility complaints per 10,000 passengers.",
    )

    doc.add_heading("1.4 Interactive Python Decision Dashboard (Figures 9 &amp; 10)", level=2)
    doc.add_paragraph_html(
        "<p>The interactive Plotly decision dashboard (<code>output/dashboard/ecomove_interactive_dashboard.html</code> and live web report) links six categorical filter dimensions (Country, City, Transport Mode, Route Type, Weather Condition, and Major Event Day) to six KPI cards and four coordinated charts. <strong>Figure 9</strong> (unfiltered network baseline) and <strong>Figure 10</strong> (filtered adverse-weather surface transit scenario) provide the static screenshot evidence below.</p>"
    )
    doc.add_image(
        "fig09_dashboard_overview.png",
        "<strong>Figure 9 (Dashboard Screenshot Evidence — Default Unfiltered View):</strong> Full-network baseline state (<code>N = 5,000</code> records across all 12 European cities), displaying top-level KPIs (40.91M passengers, 82.1% on-time, 4.35 min delay, 99.6% overall cost recovery), modal delay and recovery bars, route-level accessibility complaint rates, and top city summary metrics.",
    )
    doc.add_image(
        "fig10_dashboard_filtered_scenario.png",
        "<strong>Figure 10 (Dashboard Screenshot Evidence — Filtered Adverse Weather Surface Scenario):</strong> Filtered decision state isolating surface transit modes (<code>Bus, Tram, Park &amp; Ride</code>) under <code>Rain &amp; Snow</code> (<code>n = 583</code> records). Mean delay rises to 7.38 min (+69.7% above baseline), on-time performance drops to 72.2%, and customer rating falls to 3.46 / 5.00, while surface cost recovery remains positive at 113.2%.",
    )

    doc.add_page_break()

    # ==========================================================================
    # TASK 2: CRITICAL REPORT ON VISUALISATION AND DECISION-MAKING (30 MARKS)
    # ==========================================================================
    doc.add_heading(
        f"Task 2 — Critical Report on Visualisation and Decision-Making (LO1–LO4 · 30 Marks · {t2_words} Words)",
        level=1,
    )

    doc.add_html_block(html_builder.TASK2_SEC_2_1)
    doc.add_html_block(html_builder.TASK2_SEC_2_2)

    city_df = pd.read_csv(TABLES_DIR / "table03_city_summary.csv")
    t2_headers = [
        "Country",
        "City",
        "Rows",
        "Total Pax",
        "Pax/Rec",
        "Delay",
        "On-Time",
        "Total Margin",
        "Margin/Rec",
        "Overall (Mean) Rec%",
        "Rating",
        "Comp/10k",
    ]
    t2_rows = []
    t2_hi = set()
    for idx, r in city_df.iterrows():
        if r["Net_Margin_EUR"] < 0:
            t2_hi.add(idx)
        t2_rows.append([
            str(r["Country"]),
            f"<strong>{r['City']}</strong>",
            f"{int(r['Records']):,}",
            f"{int(r['Total_Passengers']):,}",
            f"{r['Mean_Passengers']:,.1f}",
            f"{r['Mean_Delay_Min']:.2f}m",
            f"{r['Mean_OnTime_Pct']:.1f}%",
            f"€{r['Net_Margin_EUR']:,.0f}",
            f"€{r['Mean_Margin_EUR']:,.2f}",
            f"{r['Cost_Recovery_Pct']:.2f}% ({r['Mean_Record_Cost_Recovery_Pct']:.1f}%)",
            f"{r['Mean_Rating']:.2f}",
            f"{r['Complaints_per_10k_Pax']:.2f}",
        ])
    doc.add_table(
        t2_headers,
        t2_rows,
        col_widths_pct=[9.5, 9.5, 5.5, 9.5, 7.5, 6.5, 7.0, 9.5, 8.5, 14.0, 6.0, 7.0],
        col_aligns=["left", "left"] + ["right"] * 10,
        highlight_rows=t2_hi,
        caption_html="<strong>Table 2:</strong> Comparative multi-metric performance across all 12 European cities (<code>N = 5,000</code> records). Both cumulative 2-year net margin (<code>Total Margin</code>) and per-record mean net margin (<code>Margin/Rec</code>) are reported alongside volume-weighted overall cost recovery (<code>Sum Revenue / Sum Cost</code>) and unweighted record-mean cost recovery in parentheses.",
        font_half_pt=15,
    )

    doc.add_html_block(html_builder.TASK2_SEC_2_3)
    doc.add_html_block(html_builder.TASK2_SEC_2_4)

    t3_headers = [
        "Policy Domain",
        "Target Mode / City Scope",
        "Empirical Visual Evidence",
        "Proposed Intervention for Pilot Evaluation &amp; Feasibility Appraisal",
    ]
    t3_rows = [
        [
            "<strong>1. Commercial Viability</strong>",
            "Shared Bike &amp; E-Scooter (Madrid, Barcelona, Milan, Berlin)",
            "Overall cost recovery of 5.25% (Bike) and 7.39% (E-Scooter); unit deficits of &minus;€19.98 to &minus;€20.84/trip; compositional confounding across cities (Figures 2 &amp; 3).",
            "Audit vendor rebalancing fee structures, evaluate seasonal fleet scaling during the August–October demand trough (Figure 1), and pilot multimodal fare bundling prior to any fleet expansion.",
        ],
        [
            "<strong>2. Operational &amp; Environmental</strong>",
            "Surface Bus Network (All 12 Cities; high-delay corridors)",
            "Widest delay dispersion (median 6.50 min, mean 6.58 min, max 12.50 min; 74.92% on-time) and lowest motorised carbon efficiency (1.07 kg CO<sub>2</sub>/kWh vs Metro 2.19; Figures 4 &amp; 8).",
            "Conduct corridor feasibility studies for traffic-signal priority or dedicated bus lanes where delays exceed 6.0 min (Figure 5), alongside capital appraisal for phased electric bus renewal.",
        ],
        [
            "<strong>3. Public-Sector Resilience</strong>",
            "Surface Modes in Rain/Snow &amp; Major Event Days",
            "Snow coincides with 8.14 min mean delay (Bus 10.33 min; Figure 6); Event Days (+26.2% pax) coincide with +31.0% higher delay (5.53 vs 4.22 min; Figure 5).",
            "Trial weather-triggered timetable headway buffers (Figure 10) and evaluate the operational feasibility of deploying reserve rail/tram sets during scheduled municipal events.",
        ],
        [
            "<strong>4. Social Equity &amp; Inclusion</strong>",
            "Suburban Feeder Corridors (Micromobility &amp; Bus stops)",
            "Highest volume-weighted accessibility complaint rate (16.79/10k pax overall; E-Scooter 54.02/10k and Bike Share 49.26/10k aggregate; Figure 7).",
            "Prioritise physical site audits on Suburban Feeder corridors to test whether geofenced micromobility parking corrals and step-free kerb upgrades reduce complaint intensity.",
        ],
    ]
    doc.add_table(
        t3_headers,
        t3_rows,
        col_widths_pct=[16.0, 20.0, 31.0, 33.0],
        col_aligns=["left", "left", "left", "left"],
        highlight_rows={0, 2},
        caption_html="<strong>Table 3:</strong> Evidence-supported policy appraisal framework linking empirical findings to candidate interventions for pilot evaluation across commercial, environmental, public-sector, and social dimensions.",
        font_half_pt=16,
    )

    doc.add_page_break()

    # ==========================================================================
    # REFERENCES (ARDEN UNIVERSITY HARVARD STANDARD)
    # ==========================================================================
    doc.add_heading("References (Arden University Harvard Standard)", level=1)
    for ref in html_builder.HARVARD_REFERENCES:
        doc.add_paragraph_html(
            f"<p>{ref}</p>",
            left_twips=420,
            hanging_twips=420,
            space_after=90,
            size_half_pt=19,
            style_id="Bibliography",
            keep_lines=True,
        )

    doc.add_page_break()

    # ==========================================================================
    # APPENDIX — REPRODUCIBLE PYTHON SOURCE CODE
    # ==========================================================================
    doc.add_heading("Appendix — Reproducible Python Source Code", level=1)
    doc.add_paragraph_html(
        "<p>Complete, self-contained Python 3.11 scripts used to ingest and validate <code>[5442] EcoMoveMobility.xlsx</code>, compute parametric, non-parametric, and directly standardised statistics, render the 220 DPI static visualisation suite (Figures 0, A, and 1 to 10), and build the interactive Plotly decision dashboard.</p>"
    )
    code_files = [
        ("style/palette.py", BASE_DIR / "style" / "palette.py"),
        ("scripts/01_data_prep_and_eda.py", BASE_DIR / "scripts" / "01_data_prep_and_eda.py"),
        ("scripts/02_charts.py", BASE_DIR / "scripts" / "02_charts.py"),
        ("scripts/03_diagrams.py", BASE_DIR / "scripts" / "03_diagrams.py"),
        ("scripts/04_dashboard.py", BASE_DIR / "scripts" / "04_dashboard.py"),
    ]
    for title, path in code_files:
        doc.add_code_listing(title, path.read_text(encoding="utf-8"))

    doc.save(OUT_DOCX)
    print(
        f"Built crafted Word submission file: {OUT_DOCX} ({OUT_DOCX.stat().st_size / (1024*1024):.2f} MB)"
    )


if __name__ == "__main__":
    build_word_document()
