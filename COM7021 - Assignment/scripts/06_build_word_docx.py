#!/usr/bin/env python3
"""Step 6: Build the final publication-grade Microsoft Word (.docx) submission file:
COM7021_Assessment_25199053.docx

This pure-Python OpenXML (.docx) generator embeds all high-resolution figures (Figure 0, Figure A,
and Figures 1 to 10), styled Arden tables (Tables 1, 2, and 3), the exact Task 1 (~600w) and Task 2 (~900w)
academic prose incorporating all formative feedback from Tutor Ahmed Hassan, Harvard references, and the
complete reproducible Python code in the Appendix.
"""

from __future__ import annotations

import html
import re
import zipfile
from pathlib import Path
from PIL import Image
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
TABLES_DIR = BASE_DIR / "output" / "tables"
FIG_DIR = BASE_DIR / "output" / "figures"
OUT_DOCX = BASE_DIR / "COM7021_Assessment_25199053.docx"

# Import prose directly from 05_build_review_html.py to guarantee 100% single-source synchronisation
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib
html_builder = importlib.import_module("05_build_review_html")


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def parse_inline_html_to_runs(html_text: str, base_size_half_pt: int = 21, base_color: str = "002B49", base_italic: bool = False, base_bold: bool = False) -> str:
    """Convert simple inline HTML (<strong>, <em>, <code>, <sub>, &amp;, &minus;) into WordprocessingML <w:r> runs."""
    s = html_text.strip()
    s = s.replace("&minus;", "−").replace("&ndash;", "–").replace("&mdash;", "—").replace("&amp;", "&")
    # Tokenise by inline tags
    token_pattern = re.compile(r"(<strong>.*?</strong>|<em>.*?</em>|<code>.*?</code>|<sub>.*?</sub>)", re.DOTALL)
    tokens = token_pattern.split(s)
    runs_xml = []

    def make_run(txt: str, bold: bool = False, italic: bool = False, code: bool = False, sub: bool = False) -> str:
        # Strip any residual tags
        clean = re.sub(r"<[^>]+>", "", txt)
        if not clean:
            return ""
        rpr = []
        if code:
            rpr.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>')
            rpr.append(f'<w:sz w:val="{max(16, base_size_half_pt - 2)}"/>')
            rpr.append(f'<w:szCs w:val="{max(16, base_size_half_pt - 2)}"/>')
            rpr.append('<w:shd w:val="clear" w:color="auto" w:fill="F0F5F7"/>')
        else:
            rpr.append('<w:rFonts w:ascii="Aptos" w:hAnsi="Aptos" w:cs="Aptos"/>')
            rpr.append(f'<w:sz w:val="{base_size_half_pt}"/>')
            rpr.append(f'<w:szCs w:val="{base_size_half_pt}"/>')
        if bold or base_bold:
            rpr.append("<w:b/>")
        if italic or base_italic:
            rpr.append("<w:i/>")
        if sub:
            rpr.append('<w:vertAlign w:val="subscript"/>')
        rpr.append(f'<w:color w:val="{base_color}"/>')
        rpr_str = "".join(rpr)
        return f'<w:r><w:rPr>{rpr_str}</w:rPr><w:t xml:space="preserve">{xml_escape(clean)}</w:t></w:r>'

    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("<strong>") and tok.endswith("</strong>"):
            inner = tok[8:-9]
            runs_xml.append(make_run(inner, bold=True))
        elif tok.startswith("<em>") and tok.endswith("</em>"):
            inner = tok[4:-5]
            runs_xml.append(make_run(inner, italic=True))
        elif tok.startswith("<code>") and tok.endswith("</code>"):
            inner = tok[6:-7]
            runs_xml.append(make_run(inner, code=True))
        elif tok.startswith("<sub>") and tok.endswith("</sub>"):
            inner = tok[5:-6]
            runs_xml.append(make_run(inner, sub=True))
        else:
            runs_xml.append(make_run(tok))
    return "".join(runs_xml)


class DocxBuilder:
    def __init__(self) -> None:
        self.body_elements: list[str] = []
        self.images: list[tuple[str, Path]] = []  # (rId, path)
        self.doc_pr_id = 1

    def add_heading(self, text: str, level: int = 1) -> None:
        if level == 1:
            sz = 30  # 15pt
            color = "002B49"
            before = 280
            after = 120
            bdr = '<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="66C9BA"/></w:pBdr>'
        elif level == 2:
            sz = 25  # 12.5pt
            color = "002B49"
            before = 220
            after = 90
            bdr = '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="3" w:color="E6F5F2"/></w:pBdr>'
        else:
            sz = 22  # 11pt
            color = "1A4A6B"
            before = 180
            after = 70
            bdr = ""
        runs = parse_inline_html_to_runs(text, base_size_half_pt=sz, base_color=color, base_bold=True)
        p = f"""
        <w:p>
          <w:pPr>
            <w:keepNext/>
            <w:spacing w:before="{before}" w:after="{after}" w:line="276" w:lineRule="auto"/>
            {bdr}
          </w:pPr>
          {runs}
        </w:p>"""
        self.body_elements.append(p)

    def add_paragraph_html(self, html_p: str, align: str = "both", space_before: int = 0, space_after: int = 120, size_half_pt: int = 21, color: str = "002B49", italic: bool = False, hanging_twips: int = 0, left_twips: int = 0) -> None:
        inner = re.sub(r"^\s*<p[^>]*>|</p>\s*$", "", html_p.strip(), flags=re.DOTALL)
        runs = parse_inline_html_to_runs(inner, base_size_half_pt=size_half_pt, base_color=color, base_italic=italic)
        ind_xml = ""
        if hanging_twips or left_twips:
            ind_xml = f'<w:ind w:left="{left_twips}" w:hanging="{hanging_twips}"/>'
        p = f"""
        <w:p>
          <w:pPr>
            <w:jc w:val="{align}"/>
            <w:spacing w:before="{space_before}" w:after="{space_after}" w:line="276" w:lineRule="auto"/>
            {ind_xml}
          </w:pPr>
          {runs}
        </w:p>"""
        self.body_elements.append(p)

    def add_html_block(self, block: str) -> None:
        """Parse an HTML fragment containing <h3>, <p>, <ol>/<li> into Word paragraphs."""
        token_re = re.compile(r"(<h3[^>]*>.*?</h3>|<p[^>]*>.*?</p>|<li[^>]*>.*?</li>)", re.DOTALL)
        item_idx = 0
        for m in token_re.finditer(block):
            chunk = m.group(0)
            if chunk.startswith("<h3"):
                item_idx = 0
                txt = re.sub(r"^<h3[^>]*>|</h3>$", "", chunk.strip(), flags=re.DOTALL)
                self.add_heading(txt, level=3)
            elif chunk.startswith("<p"):
                item_idx = 0
                self.add_paragraph_html(chunk)
            elif chunk.startswith("<li"):
                item_idx += 1
                inner = re.sub(r"^<li[^>]*>|</li>$", "", chunk.strip(), flags=re.DOTALL)
                numbered = f"<strong>{item_idx}.</strong> {inner}"
                self.add_paragraph_html(numbered, left_twips=360, hanging_twips=240, space_after=100)

    def add_image(self, filename: str, caption_html: str, max_width_cm: float = 16.5) -> None:
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
            <w:spacing w:before="140" w:after="60"/>
          </w:pPr>
          <w:r>
            <w:drawing>
              <wp:inline distT="0" distB="0" distL="0" distR="0">
                <wp:extent cx="{cx}" cy="{cy}"/>
                <wp:docPr id="{doc_id}" name="Picture {doc_id}" descr="{xml_escape(filename)}"/>
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
        self.add_paragraph_html(caption_html, align="both", space_before=20, space_after=180, size_half_pt=18, color="5A6B75")

    def add_table(self, headers: list[str], rows: list[list[str]], col_aligns: list[str] | None = None, highlight_rows: set[int] | None = None, caption_html: str | None = None) -> None:
        if col_aligns is None:
            col_aligns = ["left"] * len(headers)
        if highlight_rows is None:
            highlight_rows = set()

        header_cells = []
        for idx, h in enumerate(headers):
            al = col_aligns[idx]
            runs = parse_inline_html_to_runs(h, base_size_half_pt=17, base_color="FFFFFF", base_bold=True)
            header_cells.append(f"""
            <w:tc>
              <w:tcPr>
                <w:shd w:val="clear" w:color="auto" w:fill="002B49"/>
                <w:vAlign w:val="center"/>
              </w:tcPr>
              <w:p>
                <w:pPr><w:jc w:val="{al}"/><w:spacing w:before="40" w:after="40"/></w:pPr>
                {runs}
              </w:p>
            </w:tc>""")

        body_rows_xml = [f"<w:tr><w:trPr><w:tblHeader/></w:trPr>{''.join(header_cells)}</w:tr>"]

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
                runs = parse_inline_html_to_runs(cell_val, base_size_half_pt=17, base_color="002B49", base_bold=(r_idx in highlight_rows and c_idx <= 1))
                row_cells.append(f"""
                <w:tc>
                  <w:tcPr>
                    <w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>
                    <w:vAlign w:val="center"/>
                  </w:tcPr>
                  <w:p>
                    <w:pPr><w:jc w:val="{al}"/><w:spacing w:before="30" w:after="30"/></w:pPr>
                    {runs}
                  </w:p>
                </w:tc>""")
            body_rows_xml.append(f"<w:tr>{''.join(row_cells)}</w:tr>")

        tbl_xml = f"""
        <w:tbl>
          <w:tblPr>
            <w:tblW w:w="5000" w:type="pct"/>
            <w:tblBorders>
              <w:top w:val="single" w:sz="8" w:space="0" w:color="002B49"/>
              <w:bottom w:val="single" w:sz="8" w:space="0" w:color="002B49"/>
              <w:insideH w:val="single" w:sz="4" w:space="0" w:color="D5DEE3"/>
              <w:left w:val="none"/>
              <w:right w:val="none"/>
              <w:insideV w:val="none"/>
            </w:tblBorders>
            <w:tblCellMar>
              <w:top w:w="50" w:type="dxa"/>
              <w:left w:w="80" w:type="dxa"/>
              <w:bottom w:w="50" w:type="dxa"/>
              <w:right w:w="80" w:type="dxa"/>
            </w:tblCellMar>
          </w:tblPr>
          {''.join(body_rows_xml)}
        </w:tbl>"""
        self.body_elements.append(tbl_xml)
        if caption_html:
            self.add_paragraph_html(caption_html, align="both", space_before=40, space_after=160, size_half_pt=18, color="5A6B75")

    def add_code_listing(self, title: str, code_text: str) -> None:
        self.add_heading(f"Appendix File: <code>{title}</code>", level=3)
        lines = code_text.splitlines()
        run_lines = []
        for idx, line in enumerate(lines):
            br = "<w:br/>" if idx < len(lines) - 1 else ""
            run_lines.append(f'<w:t xml:space="preserve">{xml_escape(line)}</w:t>{br}')
        p = f"""
        <w:p>
          <w:pPr>
            <w:shd w:val="clear" w:color="auto" w:fill="F4F8FA"/>
            <w:pBdr>
              <w:top w:val="single" w:sz="4" w:space="4" w:color="C9D5DD"/>
              <w:left w:val="single" w:sz="12" w:space="6" w:color="3AA89A"/>
              <w:bottom w:val="single" w:sz="4" w:space="4" w:color="C9D5DD"/>
              <w:right w:val="single" w:sz="4" w:space="4" w:color="C9D5DD"/>
            </w:pBdr>
            <w:spacing w:before="60" w:after="140" w:line="220" w:lineRule="auto"/>
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
  <Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
  <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
</Types>"""

        root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

        doc_rel_items = [
            '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rIdHeader1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>',
            '<Relationship Id="rIdFooter1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>',
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
  </w:docDefaults>
</w:styles>"""

        header_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:jc w:val="right"/>
      <w:pBdr><w:bottom w:val="single" w:sz="4" w:space="2" w:color="D5DEE3"/></w:pBdr>
    </w:pPr>
    <w:r>
      <w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="17"/><w:color w:val="5A6B75"/></w:rPr>
      <w:t>COM7021SCC Data Visualisation · Assessment Submission · Student ID: 25199053</w:t>
    </w:r>
  </w:p>
</w:hdr>"""

        footer_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:jc w:val="center"/>
      <w:pBdr><w:top w:val="single" w:sz="4" w:space="2" w:color="D5DEE3"/></w:pBdr>
    </w:pPr>
    <w:r>
      <w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="17"/><w:color w:val="5A6B75"/></w:rPr>
      <w:t xml:space="preserve">Arden University · Student ID: 25199053 · Page </w:t>
    </w:r>
    <w:fldSimple w:instr="PAGE"/>
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
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""

        with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", content_types)
            zf.writestr("_rels/.rels", root_rels)
            zf.writestr("word/_rels/document.xml.rels", doc_rels)
            zf.writestr("word/styles.xml", styles_xml)
            zf.writestr("word/header1.xml", header_xml)
            zf.writestr("word/footer1.xml", footer_xml)
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

    # Title & Cover Metadata Block
    doc.add_heading(
        "Sustainable Urban Mobility Performance Across European Cities: A Python Data Visualisation Investigation and Critical Report",
        level=1,
    )
    doc.add_paragraph_html(
        "<p><strong>COM7021SCC Data Visualisation Assessment Submission</strong> · Dataset: <code>[5442] EcoMoveMobility.xlsx</code> (EcoMove City Transport Authority, 2024–2025)</p>",
        space_after=100,
    )

    meta_headers = ["Assessment Field", "Submission Specification", "Word Count & Weighting", "Compliance Metric"]
    meta_rows = [
        ["Student ID", "25199053", "Task 1 Written Prose", f"{t1_words} words (Target: ~600 words)"],
        ["Module & Programme", "COM7021SCC · MSc Data Science", "Task 1 Practical Equivalent", "1,500 words equivalent (70 Marks)"],
        ["Module Tutor", "Ahmed Hassan", "Task 2 Critical Report", f"{t2_words} words (Target: ~900 words; 30 Marks)"],
        ["Interactive Web View", "Live Dashboard (index.html)", "Total Written Prose", f"{t1_words + t2_words} words (Target: ~1,500 words)"],
    ]
    doc.add_table(meta_headers, meta_rows, col_aligns=["left", "left", "left", "left"])

    doc.add_image(
        "fig00_executive_kpi_strip.png",
        "<strong>Figure 0 (Executive Summary Strip):</strong> Baseline 2024–2025 operational metrics across 5,000 daily records in 12 European cities. Tiffany-bordered tiles highlight surface delay bottlenecks (mean 4.35 min; Bus 6.58 min) and aggregate vs modal cost-recovery divergence (99.6% overall network recovery vs 84.1% unweighted record average; Bike Share 5.2%).",
    )

    # ==========================================================================
    # TASK 1
    # ==========================================================================
    doc.add_heading("Task 1 — Data Visualisation Investigation in Python (LO1 & LO2 · 70 Marks)", level=1)

    doc.add_heading("1.1 Data Importing, Hygiene Audit, and Feature Engineering", level=2)
    doc.add_html_block(html_builder.TASK1_SEC_1_1)
    doc.add_image(
        "fig00_methodology_pipeline.png",
        "<strong>Figure A (Investigation Workflow):</strong> Five-stage Python analytical pipeline from raw Excel ingestion and serial-date conversion (<code>origin='1899-12-30'</code>) to normalised feature engineering, static 220 DPI chart generation, and interactive multi-filter dashboard deployment.",
    )

    doc.add_heading("1.2 Initial Descriptive Statistics and Financial Aggregation Basis", level=2)
    doc.add_html_block(html_builder.TASK1_SEC_1_2)

    stats_df = pd.read_csv(TABLES_DIR / "table01_initial_statistics.csv")
    t1_headers = ["Variable", "Count", "Miss", "Mean", "SD", "Median", "Q25", "Q75", "IQR", "Min", "Max", "Skew"]
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
        col_aligns=["left"] + ["right"] * 11,
        highlight_rows={9, 10, 13},
        caption_html="<strong>Table 1:</strong> Initial parametric and non-parametric descriptive statistics for raw and derived numerical variables across all <code>N = 5,000</code> daily records (generated via <code>scripts/01_data_prep_and_eda.py</code>). Note that <code>Cost_Recovery_Pct</code> mean (84.12%) reflects the unweighted average of daily record ratios, whereas volume-weighted overall cost recovery (<code>Sum Revenue / Sum Cost</code>) is 99.58%.",
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

    doc.add_heading("1.4 Interactive Python Decision Dashboard (Figures 9 & 10)", level=2)
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

    # ==========================================================================
    # TASK 2
    # ==========================================================================
    doc.add_heading("Task 2 — Critical Report on Visualisation and Decision-Making (LO1–LO4 · 30 Marks)", level=1)

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
        col_aligns=["left", "left"] + ["right"] * 10,
        highlight_rows=t2_hi,
        caption_html="<strong>Table 2:</strong> Comparative multi-metric performance across all 12 European cities (<code>N = 5,000</code> records). Both cumulative 2-year net margin (<code>Total Margin</code>) and per-record mean net margin (<code>Margin/Rec</code>) are reported alongside volume-weighted overall cost recovery (<code>Sum Revenue / Sum Cost</code>) and unweighted record-mean cost recovery in parentheses.",
    )

    doc.add_html_block(html_builder.TASK2_SEC_2_3)
    doc.add_html_block(html_builder.TASK2_SEC_2_4)

    t3_headers = [
        "Policy Domain",
        "Target Mode / City Scope",
        "Empirical Visual Evidence",
        "Proposed Intervention for Pilot Evaluation & Feasibility Appraisal",
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
        col_aligns=["left", "left", "left", "left"],
        highlight_rows={0, 2},
        caption_html="<strong>Table 3:</strong> Evidence-supported policy appraisal framework linking empirical findings to candidate interventions for pilot evaluation across commercial, environmental, public-sector, and social dimensions.",
    )

    # ==========================================================================
    # REFERENCES
    # ==========================================================================
    doc.add_heading("References (Harvard Format)", level=1)
    refs = [
        "Banister, D. (2008) ‘The sustainable mobility paradigm’, <em>Transport Policy</em>, 15(2), pp. 73–80.",
        "Cleveland, W.S. and McGill, R. (1984) ‘Graphical perception: Theory, experimentation, and application to the development of graphical methods’, <em>Journal of the American Statistical Association</em>, 79(387), pp. 531–554.",
        "European Commission (2021) <em>The New EU Urban Mobility Framework</em> (COM(2021) 811 final). Brussels: European Commission.",
        "Few, S. (2012) <em>Show Me the Numbers: Designing Tables and Graphs to Enlighten</em>. 2nd edn. Burlingame, CA: Analytics Press.",
        "Few, S. (2013) <em>Information Dashboard Design: Displaying Data for At-a-Glance Monitoring</em>. 2nd edn. Burlingame, CA: Analytics Press.",
        "Munzner, T. (2014) <em>Visualization Analysis and Design</em>. Boca Raton, FL: CRC Press.",
        "Shneiderman, B. (1996) ‘The eyes have it: A task by data type taxonomy for information visualizations’, <em>Proceedings of the IEEE Symposium on Visual Languages</em>, Boulder, CO, 3–6 September, pp. 336–343.",
        "Tufte, E.R. (2001) <em>The Visual Display of Quantitative Information</em>. 2nd edn. Cheshire, CT: Graphics Press.",
        "Ware, C. (2021) <em>Information Visualization: Perception for Design</em>. 4th edn. Cambridge, MA: Morgan Kaufmann.",
        "Wertheimer, M. (1923) ‘Untersuchungen zur Lehre von der Gestalt II’, <em>Psychologische Forschung</em>, 4(1), pp. 301–350.",
    ]
    for ref in refs:
        doc.add_paragraph_html(f"<p>{ref}</p>", left_twips=420, hanging_twips=420, space_after=80, size_half_pt=19)

    # ==========================================================================
    # APPENDIX
    # ==========================================================================
    doc.add_heading("Appendix — Reproducible Python Source Code", level=1)
    doc.add_paragraph_html(
        "<p>Complete, self-contained Python scripts used to audit the dataset, compute descriptive and standardised statistics, render the static 220 DPI visualisation suite, and build the interactive Plotly dashboard.</p>"
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
    print(f"Built Word submission file: {OUT_DOCX} ({OUT_DOCX.stat().st_size / (1024*1024):.2f} MB)")


if __name__ == "__main__":
    build_word_document()
