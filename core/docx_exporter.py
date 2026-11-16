"""
Professional Word (.docx) exporter for legal documents.
Generates properly styled, court-ready documents with margins,
headings, indentation, and advocate signature blocks.
"""

import io
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT


def create_legal_docx(markdown_content: str, title: str = "Legal Document") -> io.BytesIO:
    """
    Parses markdown legal text and builds a professional .docx file in memory.
    """
    doc = Document()
    
    # Page setup - Standard Indian legal margins (1 inch all sides)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)   # A4 Width
        section.page_height = Inches(11.69) # A4 Height

    # Base styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(20, 20, 20)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    lines = markdown_content.split('\n')
    
    in_code_block = False
    
    for raw_line in lines:
        line = raw_line.rstrip()
        
        # Skip markdown code fence
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue
            
        if not line:
            # Empty line -> slight spacing
            continue

        # Header 1 (# Title)
        if line.startswith("# "):
            text = line[2:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(12)
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.underline = True
            continue

        # Header 2 (## Subheading)
        if line.startswith("## "):
            text = line[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(13)
            run.font.bold = True
            continue

        # Header 3 (### Sub-section)
        if line.startswith("### "):
            text = line[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
            run.font.bold = True
            continue

        # Horizontal Rule (---)
        if line.strip() in ("---", "***", "___"):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run("―" * 55)
            run.font.color.rgb = RGBColor(180, 180, 180)
            continue

        # Bullet point (* or -)
        if re.match(r"^[\*\-]\s+", line):
            text = re.sub(r"^[\*\-]\s+", "", line)
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(3)
            _add_formatted_runs(p, text)
            continue

        # Numbered list item (1. or a) or (i))
        if re.match(r"^(\d+\.|\([a-z0-9]+\)|[a-z]\))\s+", line):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_after = Pt(4)
            _add_formatted_runs(p, line)
            continue

        # Standard Paragraph
        p = doc.add_paragraph()
        # Justify legal text if length is substantial
        if len(line) > 60:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        _add_formatted_runs(p, line)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def _add_formatted_runs(paragraph, text: str):
    """
    Parses simple inline markdown bold (**bold**) and italics (*italic*).
    """
    tokens = re.split(r'(\*\*.*?\*\*|\*.*?\*)', text)
    for token in tokens:
        if not token:
            continue
        if token.startswith('**') and token.endswith('**'):
            run = paragraph.add_run(token[2:-2])
            run.bold = True
            run.font.name = 'Times New Roman'
        elif token.startswith('*') and token.endswith('*'):
            run = paragraph.add_run(token[1:-1])
            run.italic = True
            run.font.name = 'Times New Roman'
        else:
            run = paragraph.add_run(token)
            run.font.name = 'Times New Roman'
