#!/usr/bin/env python3
"""Create the simple, single-column Word reference used by Pandoc exports.

Requires python-docx. Run from any directory; output is templates/reference.docx.
The reference is committed so normal resume builds only require Pandoc.
"""

from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


def main():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = section.bottom_margin = Inches(0.6)
    section.left_margin = section.right_margin = Inches(0.7)

    for style_name in ("Normal", "Body Text", "First Paragraph", "Compact"):
        if style_name not in doc.styles:
            doc.styles.add_style(style_name, 1)
        style = doc.styles[style_name]
        style.font.name = "Arial"
        style.font.size = Pt(11)
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_after = Pt(4)
        style.paragraph_format.line_spacing = 1.02
        style.paragraph_format.widow_control = True

    for name, size, before, after in (
        ("Title", 22, 0, 3),
        ("Heading 1", 22, 0, 3),
        ("Heading 2", 12, 9, 4),
        ("Heading 3", 11, 6, 3),
        ("Entry Heading", 11, 4, 3),
    ):
        if name not in doc.styles:
            doc.styles.add_style(name, 1)
        style = doc.styles[name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = name != "Entry Heading"
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True
        # Remove theme colors and title-rule residue in default Word styles.
        props = style.element.get_or_add_rPr()
        for color in props.findall(qn("w:color")):
            props.remove(color)
        color = OxmlElement("w:color")
        color.set(qn("w:val"), "000000")
        props.append(color)
        ppr = style.element.find(qn("w:pPr"))
        if ppr is not None:
            for border in ppr.findall(qn("w:pBdr")):
                ppr.remove(border)

    # Pandoc uses this style for links; keep the application readable in print.
    if "Hyperlink" not in doc.styles:
        doc.styles.add_style("Hyperlink", 2)
    doc.styles["Hyperlink"].font.color.rgb = RGBColor(0, 0, 0)
    doc.styles["Hyperlink"].font.underline = True
    doc.core_properties.author = "Marco Del Fava"
    doc.core_properties.title = "Resume reference"
    doc.add_paragraph("Resume reference", style="Title")
    target = Path(__file__).resolve().parent.parent / "templates" / "reference.docx"
    doc.save(target)
    print(target)


if __name__ == "__main__":
    main()
