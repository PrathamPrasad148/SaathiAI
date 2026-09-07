---
name: pdf
description: "Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill."
license: Proprietary
---

# PDF Processing & Generation Skill Guide

This guide covers essential PDF processing, manipulation, and generation operations using Python libraries (`pypdf`, `pdfplumber`, `reportlab`, `fitz` / `PyMuPDF`, `pytesseract`) and command-line tools (`qpdf`, `pdftotext`, `pdfimages`).

---

## 1. Quick Start & Python Libraries

### Reading & Extracting Text (`pypdf` / `pdfplumber`)
```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
print(f"Total Pages: {len(reader.pages)}")

text = ""
for page in reader.pages:
    text += page.extract_text()
```

### Table Extraction (`pdfplumber` + `pandas`)
```python
import pdfplumber
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

---

## 2. PDF Creation & Generation (`reportlab`)

### Multi-Page Document Creation (`reportlab.platypus`)
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Title & Body
title = Paragraph("Saathi AI Generated Report", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is a formatted PDF document generated programmatically.", styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Section 2", styles['Heading1']))
story.append(Paragraph("Content for page 2.", styles['Normal']))

doc.build(story)
```

### Subscripts & Superscripts Rule in ReportLab
> **CRITICAL**: Never use Unicode subscript/superscript characters (`₀₁₂₃₄₅₆₇₈₉`, `⁰¹²³⁴⁵⁶⁷⁸⁹`) in ReportLab PDFs. Built-in fonts do not include these glyphs, causing them to render as solid black boxes.
> Use ReportLab XML tags inside `Paragraph` objects instead:
> - Subscript: `Paragraph("H<sub>2</sub>O", styles['Normal'])`
> - Superscript: `Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])`

---

## 3. PDF Operations (Merge, Split, Rotate, Encrypt)

### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

### Rotate Pages & Password Protect
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.rotate(90)  # 90° clockwise
    writer.add_page(page)

writer.encrypt("userpassword", "ownerpassword")
with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

---

## 4. OCR on Scanned PDFs

```python
import pytesseract
from pdf2image import convert_from_path

# Convert PDF pages to PIL images
images = convert_from_path('scanned.pdf')

text = ""
for i, image in enumerate(images):
    text += f"--- Page {i+1} ---\n"
    text += pytesseract.image_to_string(image) + "\n\n"

print(text)
```

---

## 5. Command-Line Tools & Quick Reference

| Task | Best Tool | Command / Code |
| :--- | :--- | :--- |
| **Merge PDFs** | `pypdf` / `qpdf` | `qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf` |
| **Split PDFs** | `pypdf` | Separate writer per page |
| **Extract Text** | `pdfplumber` / `pdftotext` | `pdftotext -layout input.pdf output.txt` |
| **Extract Tables** | `pdfplumber` | `page.extract_tables()` |
| **Create PDFs** | `reportlab` | `SimpleDocTemplate` / `canvas` |
| **Extract Images** | `pdfimages` | `pdfimages -j input.pdf output_prefix` |
| **OCR Scanned PDF** | `pytesseract` + `pdf2image` | Image conversion + OCR |
