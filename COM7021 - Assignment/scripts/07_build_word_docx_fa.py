#!/usr/bin/env python3
"""Step 7-FA: Build a Persian (Farsi) Microsoft Word (.docx) & Review Document
tailored for Google Docs import, paragraph-by-paragraph manual editing,
clear screenshot placeholders, and explicit AI image generation attribution.
"""

from __future__ import annotations

import base64
import html
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from PIL import Image
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
TABLES_DIR = BASE_DIR / "output" / "tables"
FIG_DIR = BASE_DIR / "output" / "figures"
OUT_DOCX_FA = BASE_DIR / "COM7021_Assessment_25199053_FA.docx"
OUT_MD_FA = BASE_DIR / "COM7021_Assessment_25199053_FA_Review.md"

PAGE_WIDTH_DXA = 9638

def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

def parse_inline_html_to_runs_rtl(
    html_text: str,
    base_size_half_pt: int = 22,  # 11pt
    base_color: str = "1C2D37",
    base_italic: bool = False,
    base_bold: bool = False,
    code_bg: str | None = "F0F5F7",
) -> str:
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
            rpr.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>')
            sz = max(16, base_size_half_pt - 2)
            rpr.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
            if code_bg:
                rpr.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{code_bg}"/>')
        else:
            rpr.append('<w:rFonts w:ascii="Vazirmatn" w:hAnsi="Vazirmatn" w:cs="Vazirmatn"/>')
            rpr.append(f'<w:sz w:val="{base_size_half_pt}"/><w:szCs w:val="{base_size_half_pt}"/>')
            rpr.append('<w:rtl/>')
            
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

class FaDocxBuilder:
    def __init__(self) -> None:
        self.body_elements: list[str] = []
        self.images: list[tuple[str, Path]] = []
        self.doc_pr_id = 1

    def add_page_break(self) -> None:
        self.body_elements.append(
            '<w:p><w:pPr><w:bidi/><w:spacing w:before="0" w:after="0"/></w:pPr><w:r><w:br w:type="page"/></w:r></w:p>'
        )

    def add_banner_box(self, top_line: str, main_title: str, subtitle: str) -> None:
        p1_runs = parse_inline_html_to_runs_rtl(top_line, base_size_half_pt=20, base_color="66C9BA", base_bold=True)
        p2_runs = parse_inline_html_to_runs_rtl(main_title, base_size_half_pt=34, base_color="FFFFFF", base_bold=True)
        p3_runs = parse_inline_html_to_runs_rtl(subtitle, base_size_half_pt=22, base_color="E6F5F2", base_italic=False)
        tbl = f"""
        <w:tbl>
          <w:tblPr>
            <w:bidiVisual/>
            <w:tblW w:w="{PAGE_WIDTH_DXA}" w:type="dxa"/>
            <w:tblBorders>
              <w:top w:val="single" w:sz="24" w:space="0" w:color="66C9BA"/>
              <w:bottom w:val="single" w:sz="18" w:space="0" w:color="3AA89A"/>
              <w:left w:val="none"/><w:right w:val="none"/>
            </w:tblBorders>
            <w:tblCellMar>
              <w:top w:w="200" w:type="dxa"/>
              <w:left w:w="240" w:type="dxa"/>
              <w:bottom w:w="200" w:type="dxa"/>
              <w:right w:w="240" w:type="dxa"/>
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
                <w:pPr><w:bidi/><w:jc w:val="right"/><w:spacing w:before="0" w:after="80"/></w:pPr>
                {p1_runs}
              </w:p>
              <w:p>
                <w:pPr><w:bidi/><w:jc w:val="right"/><w:spacing w:before="0" w:after="80" w:line="280" w:lineRule="auto"/></w:pPr>
                {p2_runs}
              </w:p>
              <w:p>
                <w:pPr><w:bidi/><w:jc w:val="right"/><w:spacing w:before="0" w:after="0"/></w:pPr>
                {p3_runs}
              </w:p>
            </w:tc>
          </w:tr>
        </w:tbl>"""
        self.body_elements.append(tbl)

    def add_heading(self, text: str, level: int = 1) -> None:
        style_id = f"Heading{level}"
        if level == 1:
            sz = 28
            color = "002B49"
            before = 260
            after = 120
            bdr = '<w:pBdr><w:bottom w:val="single" w:sz="14" w:space="4" w:color="3AA89A"/></w:pBdr>'
        elif level == 2:
            sz = 24
            color = "002B49"
            before = 220
            after = 90
            bdr = '<w:pBdr><w:bottom w:val="single" w:sz="8" w:space="3" w:color="C9D5DD"/></w:pBdr>'
        else:
            sz = 22
            color = "123B5A"
            before = 180
            after = 60
            bdr = ""
        runs = parse_inline_html_to_runs_rtl(text, base_size_half_pt=sz, base_color=color, base_bold=True)
        p = f"""
        <w:p>
          <w:pPr>
            <w:pStyle w:val="{style_id}"/>
            <w:bidi/>
            <w:keepNext/>
            <w:keepLines/>
            {bdr}
            <w:jc w:val="right"/>
            <w:spacing w:before="{before}" w:after="{after}"/>
          </w:pPr>
          {runs}
        </w:p>"""
        self.body_elements.append(p)

    def add_paragraph_html(
        self,
        html_text: str,
        style_id: str = "Normal",
        space_before: int = 0,
        space_after: int = 130,
        align: str = "both",
        left_border_color: str | None = None,
        fill_color: str | None = None,
        keep_next: bool = False,
    ) -> None:
        runs = parse_inline_html_to_runs_rtl(html_text)
        bdr_xml = f'<w:pBdr><w:right w:val="single" w:sz="18" w:space="8" w:color="{left_border_color}"/></w:pBdr>' if left_border_color else ""
        shd_xml = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill_color}"/>' if fill_color else ""
        kn_xml = "<w:keepNext/>" if keep_next else ""
        p = f"""
        <w:p>
          <w:pPr>
            <w:pStyle w:val="{style_id}"/>
            <w:bidi/>
            {kn_xml}
            {bdr_xml}
            {shd_xml}
            <w:jc w:val="{align}"/>
            <w:spacing w:before="{space_before}" w:after="{space_after}" w:line="310" w:lineRule="auto"/>
          </w:pPr>
          {runs}
        </w:p>"""
        self.body_elements.append(p)

    def add_placeholder_box(self, title: str, instructions: str, recommended_specs: str) -> None:
        """Render a prominent, styled callout placeholder for manual user screenshots."""
        t_runs = parse_inline_html_to_runs_rtl(f"<strong>📌 {title}</strong>", base_size_half_pt=22, base_color="856404", base_bold=True)
        i_runs = parse_inline_html_to_runs_rtl(instructions, base_size_half_pt=20, base_color="664D03")
        s_runs = parse_inline_html_to_runs_rtl(f"<em>⚙️ مشخصات و ابعاد پیشنهادی:</em> {recommended_specs}", base_size_half_pt=19, base_color="533F03")
        tbl = f"""
        <w:tbl>
          <w:tblPr>
            <w:bidiVisual/>
            <w:tblW w:w="{PAGE_WIDTH_DXA}" w:type="dxa"/>
            <w:tblBorders>
              <w:top w:val="dashed" w:sz="14" w:space="0" w:color="FFEBAA"/>
              <w:bottom w:val="dashed" w:sz="14" w:space="0" w:color="FFEBAA"/>
              <w:left w:val="dashed" w:sz="14" w:space="0" w:color="FFEBAA"/>
              <w:right w:val="single" w:sz="24" w:space="0" w:color="FFC107"/>
            </w:tblBorders>
            <w:tblCellMar>
              <w:top w:w="160" w:type="dxa"/>
              <w:left w:w="200" w:type="dxa"/>
              <w:bottom w:w="160" w:type="dxa"/>
              <w:right w:w="200" w:type="dxa"/>
            </w:tblCellMar>
          </w:tblPr>
          <w:tblGrid><w:gridCol w:w="{PAGE_WIDTH_DXA}"/></w:tblGrid>
          <w:tr>
            <w:tc>
              <w:tcPr>
                <w:tcW w:w="{PAGE_WIDTH_DXA}" w:type="dxa"/>
                <w:shd w:val="clear" w:color="auto" w:fill="FFF9E6"/>
              </w:tcPr>
              <w:p>
                <w:pPr><w:bidi/><w:jc w:val="right"/><w:spacing w:before="0" w:after="60"/></w:pPr>
                {t_runs}
              </w:p>
              <w:p>
                <w:pPr><w:bidi/><w:jc w:val="right"/><w:spacing w:before="0" w:after="60"/></w:pPr>
                {i_runs}
              </w:p>
              <w:p>
                <w:pPr><w:bidi/><w:jc w:val="right"/><w:spacing w:before="0" w:after="0"/></w:pPr>
                {s_runs}
              </w:p>
            </w:tc>
          </w:tr>
        </w:tbl>"""
        self.body_elements.append(tbl)

    def add_image(
        self,
        filename: str,
        caption_html: str,
        max_width_cm: float = 16.2,
        is_ai_generated: bool = False,
        ai_model_name: str = "Google Imagen 3 (خانواده Google Gemini)",
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
            <w:bidi/>
            <w:jc w:val="center"/>
            <w:keepNext/>
            <w:keepLines/>
            <w:spacing w:before="140" w:after="50"/>
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

        full_caption = caption_html
        if is_ai_generated:
            full_caption += f" — <span style='color:#0E7C8B;'>[تولید تصویر گرافیکی با مدل هوش مصنوعی: <strong>{ai_model_name}</strong>]</span>"
        
        cap_runs = parse_inline_html_to_runs_rtl(full_caption, base_size_half_pt=19, base_color="335266", base_italic=False)
        cap_p = f"""
        <w:p>
          <w:pPr>
            <w:pStyle w:val="Caption"/>
            <w:bidi/>
            <w:jc w:val="center"/>
            <w:spacing w:before="40" w:after="160"/>
          </w:pPr>
          {cap_runs}
        </w:p>"""
        self.body_elements.append(cap_p)

    def add_table_xml(self, tbl_xml: str) -> None:
        self.body_elements.append(tbl_xml)

    def build_docx_bytes(self) -> bytes:
        content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Default Extension="jpeg" ContentType="image/jpeg"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

        root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

        doc_rels_items = [
            '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
        ]
        for r_id, pth in self.images:
            doc_rels_items.append(
                f'<Relationship Id="{r_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{pth.name}"/>'
            )
        doc_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {"".join(doc_rels_items)}
</Relationships>"""

        styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Vazirmatn" w:hAnsi="Vazirmatn" w:cs="Vazirmatn"/>
        <w:sz w:val="22"/><w:szCs w:val="22"/>
        <w:color w:val="1C2D37"/>
        <w:rtl/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:bidi/>
        <w:spacing w:before="0" w:after="120" w:line="300" w:lineRule="auto"/>
        <w:jc w:val="right"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:bidi/><w:outlineLvl w:val="0"/></w:pPr>
    <w:rPr><w:b/><w:bCs/><w:color w:val="002B49"/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rtl/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:bidi/><w:outlineLvl w:val="1"/></w:pPr>
    <w:rPr><w:b/><w:bCs/><w:color w:val="002B49"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:rtl/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:bidi/><w:outlineLvl w:val="2"/></w:pPr>
    <w:rPr><w:b/><w:bCs/><w:color w:val="123B5A"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:rtl/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="caption"/>
    <w:rPr><w:sz w:val="19"/><w:szCs w:val="19"/><w:color w:val="335266"/><w:rtl/></w:rPr>
  </w:style>
</w:styles>"""

        sect_pr = f"""
        <w:sectPr>
          <w:pgSz w:w="11906" w:h="16838"/>
          <w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/>
          <w:bidi/>
        </w:sectPr>"""

        document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>
    {"".join(self.body_elements)}
    {sect_pr}
  </w:body>
</w:document>"""

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", content_types)
            zf.writestr("_rels/.rels", root_rels)
            zf.writestr("word/_rels/document.xml.rels", doc_rels)
            zf.writestr("word/styles.xml", styles)
            zf.writestr("word/document.xml", document)
            for r_id, pth in self.images:
                zf.writestr(f"word/media/{pth.name}", pth.read_bytes())
        return buf.getvalue()


def build_fa_documents() -> None:
    doc = FaDocxBuilder()
    md_lines: list[str] = []

    def md_h(text: str, level: int = 1) -> None:
        md_lines.append(f"\n{'#' * level} {text}\n")

    def md_p(text: str) -> None:
        clean = text.replace("<p>", "").replace("</p>", "").replace("<code>", "`").replace("</code>", "`").replace("<strong>", "**").replace("</strong>", "**").replace("<em>", "*").replace("</em>", "*")
        md_lines.append(clean + "\n")

    def md_placeholder(title: str, instructions: str, specs: str) -> None:
        md_lines.append(f"\n> 📌 **[جایگاه قرارگیری اسکرین‌شات دستی کاربر: {title}]**\n> {instructions}\n> *مشخصات پیشنهادی:* {specs}\n")

    # Cover Banner
    doc.add_banner_box(
        "دانشگاه آردن برلین · دوره کارشناسی ارشد علوم داده (MSc Data Science)",
        "ارزیابی پایداری حمل‌ونقل شهری در اروپا · گزارش تحلیلی (نسخه فارسی)",
        "ماژول: COM7021SCC (مصورسازی داده‌ها) | شناسه دانشجو: 25199053 | استاد راهنما: Ahmed Hassan"
    )
    md_h("ارزیابی پایداری حمل‌ونقل شهری در اروپا · گزارش تحلیلی (نسخه فارسی)", 1)
    md_p("**ماژول:** COM7021SCC (مصورسازی داده‌ها) | **شناسه دانشجو:** 25199053 | **مدرس:** Ahmed Hassan")

    doc.add_paragraph_html(
        "<strong>راهنمای ویرایش:</strong> این سند دقیقاً معادل متن نسخه نهایی گزارش برای سهولت کار و بازبینی پاراگراف به پاراگراف به زبان فارسی آماده شده است. جایگاه تصاویر، فلوچارت‌ها، مدل هوش مصنوعی استفاده‌شده و اسکرین‌شات‌های دستی به وضوح نشانه‌گذاری شده‌اند.",
        fill_color="E6F5F2",
        left_border_color="3AA89A"
    )

    # Figure 0: Executive KPI Strip
    doc.add_image("fig00_executive_kpi_strip.png", "شکل ۰: نوار شاخص‌های کلیدی عملکرد اجرایی شبکه در ۵,۰۰۰ رکورد روزانه (۲۰۲۴–۲۰۲۵)")
    md_p("![شکل ۰](COM7021%20-%20Assignment/output/figures/fig00_executive_kpi_strip.png)\n*شکل ۰: نوار شاخص‌های کلیدی عملکرد اجرایی شبکه در ۵,۰۰۰ رکورد روزانه*")

    # TASK 1
    doc.add_heading("بخش ۱: بررسی اکتشافی، آماده‌سازی داده و مصورسازی (Task 1)", level=1)
    md_h("بخش ۱: بررسی اکتشافی، آماده‌سازی داده و مصورسازی (Task 1)", 1)

    # Paragraph 1-1
    doc.add_heading("۱.۱ پایپ‌لاین تمیزکاری، مبدأ تاریخ و مهندسی ویژگی‌ها (LO2)", level=2)
    doc.add_paragraph_html("<strong>[پاراگراف ۱-۱ · ورود داده و مهندسی شاخص‌ها]</strong>")
    p1_1 = "در این پژوهش، مجموعه داده <code>[5442] EcoMoveMobility.xlsx</code> شامل ۵,۰۰۰ رکورد روزانه و ۱۸ متغیر در ۱۲ شهر اروپایی (۶ کشور) برای سال‌های ۲۰۲۴ و ۲۰۲۵ بررسی شده است (شکل الف). تمامی کلیدهای <code>Record_ID</code> یکتا بوده و هیچ مقدار گمشده یا منفی وجود ندارد. تاریخ‌های سریال اکسل (<code>45292</code> تا <code>46022</code>) با مبدأ <code>1899-12-30</code> به تاریخ استاندارد ISO تبدیل شدند و شش شاخص نرمال‌شده مهندسی گردید: حاشیه سود خالص (<code>Net_Margin_EUR</code>)، درصد پوشش هزینه (<code>Cost_Recovery_Pct</code>)، کرایه و هزینه به ازای هر مسافر (<code>Fare_per_Pax_EUR</code> و <code>Cost_per_Pax_EUR</code>)، شکایات در هر ۱۰,۰۰۰ مسافر (<code>Complaints_per_10k_Pax</code>) و بهره‌وری کربن (<code>CO2_per_kWh</code>)."
    doc.add_paragraph_html(p1_1)
    md_h("۱.۱ پایپ‌لاین تمیزکاری، مبدأ تاریخ و مهندسی ویژگی‌ها (LO2)", 2)
    md_p(f"**[پاراگراف ۱-۱ · ورود داده و مهندسی شاخص‌ها]**\n{p1_1}")

    # Figure A (Methodology Diagram with Python code reference)
    doc.add_image(
        "fig00_methodology_pipeline.png",
        "شکل الف: پایپ‌لاین روش‌شناسی ۵ مرحله‌ای تحلیل داده و پردازش در پایتون (تولیدشده با کد پایتون scripts/03_diagrams.py)"
    )
    md_p("![شکل الف](COM7021%20-%20Assignment/output/figures/fig00_methodology_pipeline.png)\n*شکل الف: پایپ‌لاین روش‌شناسی ۵ مرحله‌ای تحلیل داده و پردازش در پایتون (تولیدشده با کد پایتون `scripts/03_diagrams.py`)*")

    # Paragraph 1-2
    doc.add_heading("۱.۲ آمار توصیفی پایه و حل تناقض تجمیع مالی (LO2)", level=2)
    doc.add_paragraph_html("<strong>[پاراگراف ۱-۲ · آمار توصیفی و تفاوت میانگین ساده با وزنی]</strong>")
    p1_2 = "آمار توصیفی اولیه (جدول ۱) چولگی مثبت شدید را در متغیرهای حجمی—تعداد مسافران (میانگین ۸,۱۸۱.۹۴، میانه ۴,۳۹۸.۰۰، چولگی ۱.۹۰+)، درآمد بلیت (میانگین ۲۲,۳۲۸.۱۲ یورو، میانه ۱۱,۱۹۰.۰۲ یورو) و صرفه‌جویی کربن (میانگین ۸۹۶.۳۹ کیلوگرم، میانه ۳۳۸.۳۰ کیلوگرم)—نشان می‌دهد، زیرا متروی پرظرفیت (میانگین ۲۴,۶۰۱.۲۶ مسافر؛ ۶۲.۹۶٪ کل مسافران) با دوچرخه اشتراکی (۳۵۴.۱۰) و اسکوتر برقی (۳۴۶.۶۰) تجمیع شده است. همچنین در تحلیل مالی، میانگین ساده رکوردها با نسبت وزنی کل شبکه تفاوت دارد: مجموع درآمد کل شبکه (۱۱۱.۶۴ میلیون یورو؛ ۲.۷۳ یورو به ازای هر مسافر) در برابر مجموع هزینه‌ها (۱۱۲.۱۱ میلیون یورو؛ ۲.۷۴ یورو به ازای هر مسافر) پوشش هزینه کلی ۹۹.۵۸٪ (کسری خالص ۰.۴۷- میلیون یورو یا ۹۳.۸۸- یورو در هر رکورد) را نشان می‌دهد، در حالی که میانگین ساده درصد پوشش هزینه روزانه ۸۴.۱۲٪ (میانه ۱۰۲.۲۶٪) است؛ زیرا وسایل خردمقیاس زیان‌ده ۲۴.۶۴٪ رکوردها اما تنها ۱.۰۶٪ مسافران را تشکیل می‌دهند."
    doc.add_paragraph_html(p1_2)
    md_h("۱.۲ آمار توصیفی پایه و حل تناقض تجمیع مالی (LO2)", 2)
    md_p(f"**[پاراگراف ۱-۲ · آمار توصیفی و تفاوت میانگین ساده با وزنی]**\n{p1_2}")

    # Visual Suite Figures 1 to 8
    doc.add_heading("۱.۳ مجموعه مصورسازی تحلیلی (شکل‌های ۱ تا ۸)", level=2)
    md_h("۱.۳ مجموعه مصورسازی تحلیلی (شکل‌های ۱ تا ۸)", 2)

    # Fig 1
    doc.add_paragraph_html("<strong>[پاراگراف ۱-۳ · رژیم فصلی و روزهای کاری - شکل ۱]</strong>")
    p_fig1 = "<strong>۱. رژیم فصلی و روزهای کاری (شکل ۱):</strong> نمودار خطی دوسویه میانگین تقاضای ماهانه را در سال‌های ۲۰۲۴–۲۰۲۵ نشان داده و رژیم روزهای کاری و آخر هفته را تفکیک می‌کند (۳۴.۱٪+ تقاضای بیشتر در روزهای کاری: ۸,۸۰۲.۸۸ در برابر ۶,۵۶۲.۸۶ مسافر). اوج تقاضای بهاره (مارس ۲۰۲۴: ۹,۴۱۲.۲۲؛ آوریل ۲۰۲۵: ۱۰,۲۸۵.۴۷) در برابر افت ۲۷.۲- درصدی در کف ماه اکتبر (۶,۸۰۵.۴۸) قرار دارد که اکتبر را به کم‌اختلال‌ترین بازه برای تعمیرات اساسی تبدیل می‌کند."
    doc.add_paragraph_html(p_fig1)
    doc.add_image("fig01_monthly_demand_trend.png", "شکل ۱: روند ماهانه تقاضای مسافران با تفکیک روزهای کاری و آخر هفته (۲۰۲۴–۲۰۲۵)")
    md_p(f"**[پاراگراف ۱-۳ · رژیم فصلی و روزهای کاری]**\n{p_fig1}\n![شکل ۱](COM7021%20-%20Assignment/output/figures/fig01_monthly_demand_trend.png)")

    # Fig 2
    doc.add_paragraph_html("<strong>[پاراگراف ۱-۴ · تناقض آماری سیمپسون در حاشیه مالی شهرها - شکل ۲]</strong>")
    p_fig2 = "<strong>۲. تناقض آماری سیمپسون در حاشیه مالی شهرها (شکل ۲):</strong> نمودار دمبلی متصل، میانگین سود خالص خام هر رکورد را با سود تعدیل‌شده بر اساس ترکیب وسایل نقلیه مقایسه می‌کند. از آنجا که سهم رکوردهای دوچرخه و اسکوتر بین شهرها متفاوت است (از ۲۲.۱۸٪ در آمستردام تا ۲۸.۶۱٪ در مادرید) و همبستگی منفی قوی با سود خام دارد (<em>r</em> = &minus;0.795)، رتبه‌بندی خام دچار تورش ترکیبی است. استانداردسازی مستقیم وزن وسایل نقلیه، برلین را از رتبه ۴ خام (۳۵.۶۵+ یورو در رکورد؛ ۱۴.۵۴+ هزار یورو کل) به رتبه ۱۱ (۳۵۳.۸۷- یورو تعدیل‌شده) منتقل کرده و کسری هر رکورد مادرید را ۶۲٪ کاهش می‌دهد (از ۷۰۲.۲۹- به ۲۶۸.۰۴- یورو)."
    doc.add_paragraph_html(p_fig2)
    doc.add_image("fig02_city_demand_comparison.png", "شکل ۲: نمودار دمبلی مقایسه حاشیه سود خام در برابر تعدیل‌شده شهرها (حل تناقض سیمپسون)")
    md_p(f"**[پاراگراف ۱-۴ · تناقض آماری سیمپسون]**\n{p_fig2}\n![شکل ۲](COM7021%20-%20Assignment/output/figures/fig02_city_demand_comparison.png)")

    # Fig 3
    doc.add_paragraph_html("<strong>[پاراگراف ۱-۵ · اقتصاد واحد سفر و بازدهی کاهش کربن - شکل ۳]</strong>")
    p_fig3 = "<strong>۳. اقتصاد واحد سفر و بازدهی کاهش کربن (شکل ۳):</strong> نمودار میله‌ای دوپنلی، اقتصاد واحد هر مسافر (پنل الف) را در کنار تراز تجمعی و بازده کربن (پنل ب) نمایش می‌دهد. پارکینگ و سوار (۳.۰۸ یورو کرایه در برابر ۲.۵۴ یورو هزینه؛ ۰.۵۵+ یورو)، تراموا (۲.۴۶ در برابر ۲.۰۹؛ ۰.۳۶+ یورو) و مترو (۲.۸۵ در برابر ۲.۶۸؛ ۰.۱۷+ یورو) حاشیه واحد مثبت دارند و اتوبوس در نقطه سربه‌سر (۲.۳۷ در برابر ۲.۳۶ یورو) قرار دارد. در مقابل، دوچرخه اشتراکی (۱.۱۵ در برابر ۲۲.۰۰ یورو؛ ۲۰.۸۴- یورو، پوشش کلی ۵.۲۵٪) و اسکوتر برقی (۱.۵۹ در برابر ۲۱.۵۷ یورو؛ ۱۹.۹۸- یورو، پوشش ۷.۳۹٪) زیان واحد سنگینی دارند. مترو ضمن کاهش ۳,۱۵۰.۹۲ تن کربن، ۴.۳۰+ میلیون یورو مازاد مالی (۱,۳۶۶+ یورو بر تن کربن) ایجاد می‌کند، در حالی که حمل‌ونقل خرد نیازمند ۱۱۴ تا ۱۵۱ هزار یورو یارانه به ازای هر تن کربن است."
    doc.add_paragraph_html(p_fig3)
    doc.add_image("fig03_mode_cost_recovery.png", "شکل ۳: اقتصاد واحد به ازای هر مسافر در برابر تراز تجمعی و راندمان کاهش کربن")
    md_p(f"**[پاراگراف ۱-۵ · اقتصاد واحد سفر و بازدهی کربن]**\n{p_fig3}\n![شکل ۳](COM7021%20-%20Assignment/output/figures/fig03_mode_cost_recovery.png)")

    # Fig 4
    doc.add_paragraph_html("<strong>[پاراگراف ۱-۶ · توزیع تأخیر خدمات و نمودار باران‌ابری - شکل ۴]</strong>")
    p_fig4 = "<strong>۴. توزیع تأخیر خدمات (شکل ۴):</strong> نمودار باران‌ابری (ترکیب چگالی KDE، باکس‌پلات توکی و نقاط مشاهده‌شده) دنباله ریسک تأخیر را نشان می‌دهد. اتوبوس گسترده‌ترین پراکندگی تأخیر را دارد (میانه ۶.۵۰ دقیقه، دامنه بین‌چارکی ۲.۰۰ دقیقه، میانگین ۶.۵۸ دقیقه، حداکثر ۱۲.۵۰ دقیقه؛ وقت‌شناسی ۷۴.۹۲٪)، در حالی که مترو با خطوط مجزا توزیع فشرده و پایداری دارد (میانه ۳.۶۰ دقیقه، میانگین ۳.۷۳ دقیقه؛ وقت‌شناسی ۸۴.۰۹٪)."
    doc.add_paragraph_html(p_fig4)
    doc.add_image("fig04_delay_distribution_boxplot.png", "شکل ۴: نمودار باران‌ابری توزیع تأخیر خدمات در وسایل مختلف حمل‌ونقل")
    md_p(f"**[پاراگراف ۱-۶ · توزیع تأخیر خدمات]**\n{p_fig4}\n![شکل ۴](COM7021%20-%20Assignment/output/figures/fig04_delay_distribution_boxplot.png)")

    # Fig 5
    doc.add_paragraph_html("<strong>[پاراگراف ۱-۷ · همبستگی تأخیر، رضایت مسافر و روزهای رویداد - شکل ۵]</strong>")
    p_fig5 = "<strong>۵. همبستگی تأخیر، رضایت مسافر و روزهای رویداد (شکل ۵):</strong> نمودار پراکندگی مشترک به همراه رگرسیون OLS و منحنی‌های حاشیه‌ای، رابطه مشاهده‌ای بین تأخیر و امتیاز رضایت را نشان می‌دهد (<em>r</em> = &minus;0.821، شیب ۰.۱۴- امتیاز در دقیقه؛ <em>N</em> = 5,000). از آنجا که همبستگی به تنهایی اثبات‌کننده علیت مستقیم نیست، افت رضایت می‌تواند متأثر از متغیرهای مداخله‌گر هم‌زمان مانند ازدحام واگن‌ها یا دشواری تعویض خط نیز باشد. در روزهای رویداد بزرگ (<em>n</em> = 510)، تقاضا ۲۶.۲٪+ بیشتر بوده و هم‌زمان میانگین تأخیر ۳۱.۰٪+ بالاتر (۵.۵۳ در برابر ۴.۲۲ دقیقه) و رضایت کمتر (۳.۸۷ در برابر ۴.۰۲) ثبت شده است."
    doc.add_paragraph_html(p_fig5)
    doc.add_image("fig05_delay_rating_relationship.png", "شکل ۵: رابطه پراکندگی و رگرسیون بین تأخیر و رضایت مسافران به تفکیک روزهای رویداد")
    md_p(f"**[پاراگراف ۱-۷ · تأخیر و رضایت مسافر]**\n{p_fig5}\n![شکل ۵](COM7021%20-%20Assignment/output/figures/fig05_delay_rating_relationship.png)")

    # Fig 6, 7, 8
    doc.add_paragraph_html("<strong>[پاراگراف ۱-۸ · آب‌وهوا، شکایات دسترسی و ماتریس ارزیابی چندبعدی - شکل‌های ۶ تا ۸]</strong>")
    p_fig68 = "<strong>۶. شرایط جوی، نرخ شکایات دسترسی و ماتریس جامع (شکل‌های ۶ تا ۸):</strong> نقشه حرارتی آب‌وهوا (شکل ۶) نشان می‌دهد بارش برف با ۱۱۹.۴٪+ تأخیر بیشتر نسبت به هوای صاف همراه است (۸.۱۴ در برابر ۳.۷۱ دقیقه؛ اتوبوس ۱۰.۳۳ دقیقه). شکل ۷ خطای مخرج را در شکایات دسترسی اصلاح می‌کند: شمار خام شکایات با حجم مسافر همبستگی دارد (<em>r</em> = 0.866) و مترو را در ظاهر بدترین نشان می‌دهد (۳۶.۵۲ شکایت در رکورد)، اما نرخ نرمال‌شده در هر ۱۰,۰۰۰ مسافر (پنل الف) ثابت می‌کند مترو کمترین نرخ شکایت (۱۴.۸۵) و خطوط حومه‌ای بالاترین نرخ (۱۶.۷۹ در ۱۰ هزار) را دارند؛ به‌ویژه اسکوتر (۵۴.۰۲ وزنی؛ ۶۶.۸۷ میانگین رکورد) و دوچرخه (۴۹.۲۶ وزنی؛ ۵۵.۲۶ میانگین رکورد) در خطوط حومه‌ای (پنل ب). شکل ۸ شاخص‌های کلیدی را جمع‌بندی کرده و شکل‌های ۹ و ۱۰ داشبورد تعاملی را نمایش می‌دهند."
    doc.add_paragraph_html(p_fig68)
    doc.add_image("fig06_weather_mode_delay_heatmap.png", "شکل ۶: نقشه حرارتی تأثیر شرایط جوی بر میانگین تأخیر وسایل نقلیه")
    doc.add_image("fig07_route_accessibility_rate.png", "شکل ۷: ماتریس دوسویه نرخ شکایات دسترسی نرمال‌شده در هر ۱۰,۰۰۰ مسافر")
    doc.add_image("fig08_mode_performance_matrix.png", "شکل ۸: ماتریس ارزیابی جامع چندبعدی عملکرد وسایل نقلیه شهری")
    md_p(f"**[پاراگراف ۱-۸ · آب‌وهوا، شکایات دسترسی و ماتریس جامع]**\n{p_fig68}\n![شکل ۶](COM7021%20-%20Assignment/output/figures/fig06_weather_mode_delay_heatmap.png)\n![شکل ۷](COM7021%20-%20Assignment/output/figures/fig07_route_accessibility_rate.png)\n![شکل ۸](COM7021%20-%20Assignment/output/figures/fig08_mode_performance_matrix.png)")

    # SECTION 1.4: DASHBOARD WITH PLACEHOLDERS
    doc.add_heading("۱.۴ داشبورد تعاملی تحلیلی (Streamlit) و شواهد سناریوها (شکل‌های ۹ و ۱۰)", level=2)
    md_h("۱.۴ داشبورد تعاملی تحلیلی (Streamlit) و شواهد سناریوها (شکل‌های ۹ و ۱۰)", 2)

    doc.add_paragraph_html("<strong>[پاراگراف ۱-۹ · داشبورد تعاملی و پیاده‌سازی فیلترها]</strong>")
    p_dash_desc = "داشبورد تحلیلی تعاملی طراحی‌شده با Streamlit و Plotly (مستقر در آدرس <code>https://com7021-data-visualisation.streamlit.app/</code>) با هدف توانمندسازی مدیران در واکاوی چندبعدی داده‌ها توسعه یافته است. در شکل ۹، نمای پیش‌فرض کل شبکه (N = 5,000) به عنوان خط مبنا ارائه شده است. در شکل ۱۰، سناریوی تنش جوی و ناوگان سطحی (باران و برف برای اتوبوس و تراموا، n = 583) بررسی شده که نشان‌دهنده افزایش شدید تأخیر به ۷.۳۸ دقیقه و افت رضایت به ۳.۴۶ است."
    doc.add_paragraph_html(p_dash_desc)
    md_p(f"**[پاراگراف ۱-۹ · داشبورد تعاملی و پیاده‌سازی فیلترها]**\n{p_dash_desc}")

    # Placeholder for Fig 9
    doc.add_placeholder_box(
        "اسکرین‌شات دستی شکل ۹: نمای کلی داشبورد در حالت پیش‌فرض شبکه (Baseline)",
        "کاربر گرامی، لطفاً اسکرین‌شات باکیفیت و واضحی از نمای تمام‌صفحه داشبورد آنلاین در حالت بدون فیلتر (N=5,000) گرفته و در این جایگاه جایگزین فرمایید.",
        "نسبت تصویر ۱۶:۹، رزولوشن ۱۹۲۰x۱۰۸۰ پیکسل، شامل نوار KPI بالا و تب‌های تحلیلی."
    )
    doc.add_image("fig09_dashboard_overview.png", "شکل ۹: نمای کلی داشبورد تحلیلی تعاملی — خط مبنای کل شبکه بدون فیلتر (N = 5,000)")
    md_placeholder(
        "اسکرین‌شات شکل ۹: داشبورد در حالت پیش‌فرض شبکه",
        "اسکرین‌شات داشبورد در حالت N=5,000 را در این محل قرار دهید.",
        "۱۹۲۰x۱۰۸۰ (۱۶:۹)"
    )

    # Placeholder for Fig 10
    doc.add_placeholder_box(
        "اسکرین‌شات دستی شکل ۱۰: سناریوی فیلترشده ناوگان سطحی در شرایط جوی نامساعد",
        "کاربر گرامی، لطفاً دکمه سناریوی آماده 'Adverse Weather Surface' را در داشبورد کلیک کرده و اسکرین‌شات نمای فیلترشده (n=583) را در این بخش قرار دهید.",
        "نسبت تصویر ۱۶:۹، نمایش دلتاهای قرمز تأخیر و کاهش رضایت در کارت‌های KPI."
    )
    doc.add_image("fig10_dashboard_filtered_scenario.png", "شکل ۱۰: سناریوی فیلترشده ناوگان سطحی در باران و برف (n = 583) در داشبورد تعاملی")
    md_placeholder(
        "اسکرین‌شات شکل ۱۰: سناریوی فیلترشده ناوگان سطحی در باران و برف",
        "اسکرین‌شات حالت فیلترشده (n=583) را در این محل قرار دهید.",
        "۱۹۲۰x۱۰۸۰ (۱۶:۹)"
    )

    # TASK 2
    doc.add_page_break()
    doc.add_heading("بخش ۲: گزارش تفسیری و توصیه‌های سیاستی (Task 2)", level=1)
    md_h("بخش ۲: گزارش تفسیری و توصیه‌های سیاستی (Task 2)", 1)

    # Paragraph 2-1
    doc.add_heading("۲.۱ توجیه ادراکی و روان‌شناختی طراحی بصری برای مخاطبان فنی و غیرفنی (LO1 & LO3)", level=2)
    doc.add_paragraph_html("<strong>[پاراگراف ۲-۱ · روانشناسی ادراک و طراحی برای دو گروه مخاطب]</strong>")
    p2_1 = "انتقال مؤثر یافته‌های عملکرد حمل‌ونقل نیازمند پاسخگویی هم‌زمان به دو گروه مخاطب است: تحلیل‌گران فنی که به دنبال بررسی چولگی توزیع، هم‌پراکندگی و نرخ‌های نرمال‌شده هستند، و مدیران اجرایی غیرفنی که نیازمند تشخیص سریع ناهنجاری‌ها و سبک‌سنگین کردن گزینه‌های سیاستی هستند (Munzner, 2014; Few, 2013). با کنار گذاشتن نمودارهای کم‌دقت مانند نمودار دایره‌ای، اشکال سه‌بعدی یا محورهای دوگانه، این مجموعه بر سلسله‌مراتب ادراکی Cleveland و McGill (1984) تکیه دارد و تمامی مقایسه‌های اصلی (شکل‌های ۲، ۳ و ۷) را روی محورهای مشترک تراز می‌کند."
    doc.add_paragraph_html(p2_1)
    p2_1_b = "برای کاهش بار شناختی، اصول بیشینه‌سازی جوهر داده Tufte (2001) و پردازش پیش‌توجهی Ware (2021) به کار گرفته شده است. پالت رنگی منسجم—سرمه‌ای آردن (<code>#002B49</code>) برای ساختار پایه و فیروزه‌ای تیفانی (<code>#66C9BA</code> / <code>#3AA89A</code>) صرفاً برای نقاط کانونی—کنتراست استاندارد WCAG 4.5:1 را تضمین می‌کند. مدیران غیرفنی از طریق برچسب‌های مستقیم در شکل‌های ۲، ۳ و ۸ به سرعت تغییر رتبه شهرها و کسری مالی وسایل خرد را درمی‌یابند، در حالی که تحلیل‌گران فنی از لایه‌های آماری نمودار باران‌ابری (شکل ۴) و رگرسیون مشترک (شکل ۵) بهره می‌برند."
    doc.add_paragraph_html(p2_1_b)
    md_h("۲.۱ توجیه ادراکی و روان‌شناختی طراحی بصری برای مخاطبان فنی و غیرفنی (LO1 & LO3)", 2)
    md_p(f"**[پاراگراف ۲-۱ · روانشناسی ادراک و طراحی]**\n{p2_1}\n\n{p2_1_b}")

    # Paragraph 2-2
    doc.add_heading("۲.۲ ترکیب انتقادی یافته‌ها و بازاندیشی روش‌شناختی (LO2 & LO3)", level=2)
    doc.add_paragraph_html("<strong>[پاراگراف ۲-۲ · چهار یافته روش‌شناختی کلیدی]</strong>")
    p2_2_lead = "ترکیب شواهد تحلیلی بدون تکرار توصیف‌های خام، چهار نتیجه روش‌شناختی کلیدی را برجسته می‌سازد:"
    doc.add_paragraph_html(p2_2_lead)
    items_2_2 = [
        "<strong>۱. تطبیق ارقام مالی در سطح هر رکورد، هر مسافر و کل شبکه:</strong> مبنای تجمیع، تفسیر مالی را دگرگون می‌کند. در حالی که میانگین ساده درصد پوشش هزینه در ۵,۰۰۰ رکورد روزانه ۸۴.۱۲٪ است (زیرا وسایل خردمقیاس ۲۴.۶۴٪ رکوردها یعنی ۱,۲۳۲ ردیف را تشکیل می‌دهند)، نسبت پوشش هزینه وزنی کل شبکه (<code>Sum Revenue / Sum Cost</code>) برابر با ۹۹.۵۸٪ است (۱۱۱.۶۴ میلیون یورو درآمد در برابر ۱۱۲.۱۱ میلیون یورو هزینه؛ کسری کل ۰.۴۷- میلیون یورو یا ۹۳.۸۸- یورو در هر رکورد). خطوط ثابت—مترو (۴.۳۰+ میلیون یورو کل، ۰.۱۷+ یورو بر مسافر، پوشش کلی ۱۰۶.۲۴٪)، تراموا (۲.۳۱+ میلیون یورو، ۰.۳۶+ یورو بر مسافر، ۱۱۷.۳۰٪) و پارکینگ و سوار (۱.۷۸+ میلیون یورو، ۰.۵۵+ یورو بر مسافر، ۱۲۱.۵۳٪)—زیان دوچرخه اشتراکی (۵.۶۰- میلیون یورو، ۲۰.۸۴- یورو بر مسافر، ۵.۲۵٪) و اسکوتر (۳.۲۸- میلیون یورو، ۱۹.۹۸- یورو بر مسافر، ۷.۳۹٪) را جبران می‌کنند (شکل ۳).",
        "<strong>۲. کنترل اثر ترکیبی در مقایسه شهرها:</strong> ارقام تجمعی خام شهرها (جدول ۲) به دلیل تفاوت سهم رکوردهای حمل‌ونقل خرد و همبستگی منفی آن با سود خام (<em>r</em> = &minus;0.795) دچار تناقض سیمپسون هستند. استانداردسازی مستقیم (شکل ۲) نشان می‌دهد مازاد خام برلین (۱۴.۵۴+ هزار یورو کل؛ ۳۵.۶۵+ یورو در رکورد) زیان روزانه حمل‌ونقل خرد را پنهان کرده است (۳۵۳.۸۷- یورو تعدیل‌شده، رتبه ۱۱)، در حالی که کسری ظاهری مادرید (۲۷۲.۴۹- هزار یورو کل؛ ۷۰۲.۲۹- یورو در رکورد) با وزن‌های برابر ۶۲٪ کاهش می‌یابد (۲۶۸.۰۴- یورو).",
        "<strong>۳. مرزبندی همبستگی و علیت در کیفیت خدمات:</strong> هرچند تأخیرهای سطحی (شکل ۴)، شرایط جوی نامساعد (شکل ۶) و روزهای رویداد (شکل ۵) همبستگی قوی با افت وقت‌شناسی (<em>r</em> = &minus;0.968) و افت رضایت (<em>r</em> = &minus;0.821) دارند، داده‌های مشاهده‌ای به تنهایی علیت تک‌متغیره را اثبات نمی‌کنند و عواملی چون ازدحام، سرمای ایستگاه یا فرسودگی ناوگان نیز در افت رضایت نقش دارند.",
        "<strong>۴. اصلاح تورش حجم مسافر در ارزیابی دسترسی‌پذیری:</strong> شکایات خام دسترسی با حجم مسافر همبستگی دارند (<em>r</em> = 0.866). نرمال‌سازی وزنی به ازای هر ۱۰,۰۰۰ مسافر (شکل ۷) نشان می‌دهد مترو کمترین نرخ شکایت (۱۴.۸۵) و خطوط حومه‌ای بالاترین شدت شکایت (۱۶.۷۹ در ۱۰ هزار) را دارند که در اسکوتر (۵۴.۰۲) و دوچرخه (۴۹.۲۶) متمرکز است."
    ]
    for it in items_2_2:
        doc.add_paragraph_html(it, space_before=40, space_after=100)
    md_h("۲.۲ ترکیب انتقادی یافته‌ها و بازاندیشی روش‌شناختی (LO2 & LO3)", 2)
    md_p(f"**[پاراگراف ۲-۲ · چهار یافته روش‌شناختی کلیدی]**\n{p2_2_lead}\n\n" + "\n\n".join(items_2_2))

    # Paragraph 2-3
    doc.add_heading("۲.۳ ارزیابی اثربخشی داشبورد تعاملی و محدودیت‌های تحلیلی (LO1 & LO3)", level=2)
    doc.add_paragraph_html("<strong>[پاراگراف ۲-۳ · قابلیت‌های داشبورد و محدودیت‌های روش‌شناختی]</strong>")
    p2_3 = "داشبورد تعاملی (بخش ۱.۴؛ شکل‌های ۹ و ۱۰) اصل معروف Shneiderman (1996) (<em>نمای کلی در ابتدا، بزرگ‌نمایی و فیلتر، سپس جزئیات در صورت نیاز</em>) را با اتصال شش فیلتر به شش کارت KPI و چهار نمودار پیاده‌سازی می‌کند. در حالی که نمای پایه بدون فیلتر (شکل ۹، <em>N</em> = 5,000) پوشش هزینه ۹۹.۶٪ و میانگین تأخیر ۴.۳۵ دقیقه را نشان می‌دهد، فیلتر کردن ناوگان سطحی در باران و برف (شکل ۱۰، <em>n</em> = 583) افزایش تأخیر (۷.۳۸ دقیقه)، افت وقت‌شناسی (۷۲.۲٪) و کاهش رضایت (۳.۴۶ از ۵) را در کنار پوشش هزینه مثبت ناوگان سطحی (۱۱۳.۲٪) جداسازی می‌کند. سه محدودیت روش‌شناختی عبارت‌اند از: (۱) حذف قابلیت تعاملی در تصاویر ثابت فایل Word؛ (۲) تجمیع روزانه که پیک ترافیک صبح و عصر را پنهان می‌کند؛ و (۳) عدم شمول استهلاک سرمایه‌ای در هزینه‌های عملیاتی."
    doc.add_paragraph_html(p2_3)
    md_h("۲.۳ ارزیابی اثربخشی داشبورد تعاملی و محدودیت‌های تحلیلی (LO1 & LO3)", 2)
    md_p(f"**[پاراگراف ۲-۳ · قابلیت‌های داشبورد و محدودیت‌ها]**\n{p2_3}")

    # Paragraph 2-4
    doc.add_heading("۲.۴ پیشنهادهای مبتنی بر شواهد برای امکان‌سنجی و اجرای آزمایشی (LO4)", level=2)
    doc.add_paragraph_html("<strong>[پاراگراف ۲-۴ · توصیه‌های سیاستی و اجرایی]</strong>")
    p2_4_lead = "در چارچوب حکمرانی حمل‌ونقل پایدار اروپا (European Commission, 2021; Banister, 2008)، از آنجا که یافته‌ها مبتنی بر داده‌های مشاهده‌ای هستند، چهار مداخله هدفمند به عنوان گزینه‌های پشتوانه‌دار برای ارزیابی آزمایشی (پایلوت) و امکان‌سنجی فنی-اقتصادی پیشنهاد می‌شوند:"
    doc.add_paragraph_html(p2_4_lead)
    items_2_4 = [
        "<strong>۱. بازنگری قراردادهای نگهداری حمل‌ونقل خرد و مقیاس‌دهی فصلی (پایداری تجاری):</strong> با توجه به زیان واحد هر سفر (۱۹.۹۸- تا ۲۰.۸۴- یورو؛ شکل ۳) و اثر ترکیبی بر تراز شهرها (شکل ۲)، پیشنهاد می‌شود در مادرید، بارسلونا، میلان و برلین تعرفه پیمانکاران شارژ و جابه‌جایی بازنگری شده، کاهش فصلی ناوگان در رکود اوت–اکتبر (شکل ۱) و بسته‌های کرایه ترکیبی پیش از هرگونه توسعه ناوگان به صورت آزمایشی ارزیابی شوند.",
        "<strong>۲. امکان‌سنجی اولویت تردد اتوبوس در کریدورهای پرتأخیر (عملیاتی و زیست‌محیطی):</strong> با توجه به پراکندگی بالای تأخیر اتوبوس (میانگین ۶.۵۸ دقیقه؛ شکل ۴) و بهره‌وری کربن پایین‌تر (۱.۰۷ در برابر ۲.۱۹ کیلوگرم بر کیلووات‌ساعت در مترو؛ شکل ۸)، انجام مطالعات امکان‌سنجی برای خطوط ویژه یا اولویت چراغ راهنمایی در مسیرهای با تأخیر بالای ۶ دقیقه (شکل ۵) و ارزیابی مالی نوسازی تدریجی اتوبوس‌های برقی پیشنهاد می‌شود.",
        "<strong>۳. اجرای آزمایشی ضرایب اطمینان جدول زمانی در برف و روزهای رویداد (تاب‌آوری خدمات):</strong> بر پایه افزایش تأخیر در برف (۸.۱۴ دقیقه) و باران (۵.۴۰ دقیقه؛ شکل‌های ۶ و ۱۰) و روزهای رویداد بزرگ (۳۱.۰٪+ تأخیر هم‌زمان با ۲۶.۲٪+ تقاضا؛ شکل ۵)، آزمایش برنامه‌های زمان‌بندی منعطف جوی و ارزیابی اقتصادی اعزام قطارهای ذخیره در رویدادهای از پیش تعیین‌شده توصیه می‌شود.",
        "<strong>۴. ممیزی میدانی ایستگاه‌ها در خطوط ارتباطی حومه‌ای (عدالت اجتماعی):</strong> بر اساس نرخ شکایات نرمال‌شده (شکل ۷)، انجام ممیزی میدانی در خطوط حومه‌ای برای آزمون تأثیر احداث پارکینگ‌های مشخص اسکوتر و دوچرخه و مناسب‌سازی لبه‌های پیاده‌رو بر کاهش نرخ شکایات (۴۹.۳ تا ۵۴.۰ در ۱۰ هزار مسافر) پیشنهاد می‌گردد."
    ]
    for it in items_2_4:
        doc.add_paragraph_html(it, space_before=40, space_after=100)
    md_h("۲.۴ پیشنهادهای مبتنی بر شواهد برای امکان‌سنجی و اجرای آزمایشی (LO4)", 2)
    md_p(f"**[پاراگراف ۲-۴ · توصیه‌های سیاستی]**\n{p2_4_lead}\n\n" + "\n\n".join(items_2_4))

    # Harvard References
    doc.add_heading("منابع و مراجع دانشگاهی (References - Harvard Style)", level=2)
    md_h("منابع و مراجع دانشگاهی (References - Harvard Style)", 2)
    refs = [
        "Banister, D. (2008) 'The sustainable mobility paradigm', <em>Transport Policy</em>, 15(2), pp. 73–80.",
        "Cleveland, W.S. and McGill, R. (1984) 'Graphical perception: Theory, experimentation, and application to the development of graphical methods', <em>Journal of the American Statistical Association</em>, 79(387), pp. 531–554.",
        "European Commission (2021) <em>Sustainable and Smart Mobility Strategy – Putting European transport on track for the future</em>. Brussels: European Commission.",
        "Few, S. (2013) <em>Information Dashboard Design: Displaying data for at-a-glance monitoring</em>. 2nd edn. Burlingame, CA: Analytics Press.",
        "Munzner, T. (2014) <em>Visualization Analysis and Design</em>. Boca Raton, FL: CRC Press / Taylor & Francis Group.",
        "Shneiderman, B. (1996) 'The eyes have it: A task by data type taxonomy for information visualizations', in <em>Proceedings of the IEEE Symposium on Visual Languages</em>. Boulder, CO: IEEE Computer Society Press, pp. 336–343.",
        "Tufte, E.R. (2001) <em>The Visual Display of Quantitative Information</em>. 2nd edn. Cheshire, CT: Graphics Press.",
        "Ware, C. (2021) <em>Information Visualization: Perception for Design</em>. 4th edn. Cambridge, MA: Morgan Kaufmann / Elsevier."
    ]
    for r in refs:
        doc.add_paragraph_html(r, space_after=80, align="left")
        clean_r = r.replace("<em>", "*").replace("</em>", "*")
        md_lines.append(f"- {clean_r}")

    # Build DOCX file
    docx_bytes = doc.build_docx_bytes()
    OUT_DOCX_FA.write_bytes(docx_bytes)
    OUT_MD_FA.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Generated Persian DOCX: {OUT_DOCX_FA} ({len(docx_bytes):,} bytes)")
    print(f"Generated Persian Review Markdown: {OUT_MD_FA}")

if __name__ == "__main__":
    build_fa_documents()
