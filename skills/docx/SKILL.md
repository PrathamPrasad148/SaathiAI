---
name: docx
description: "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx) or Word templates (.dotx). Triggers include: any mention of 'Word doc', 'word document', '.docx', '.dotx', or requests to produce professional documents with formatting like tables of contents, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx or .dotx files, inserting or replacing images in documents, find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file (to download, email or print), use this skill. However, if they ask for a document, page, report, memo, or notes WITHOUT naming a file format and the session offers a dedicated document or page skill or connector, use that instead. Do NOT use for PDFs, spreadsheets, Google Docs, or coding unrelated to document generation."
license: Proprietary
---

# DOCX Creation, Editing, and Analysis Skill

A `.docx` file is a ZIP archive of XML files. Choose the appropriate approach based on the target task:

| Task | Recommended Approach |
| :--- | :--- |
| **Create** a new document | Write a `docx` (npm) script — see gotchas below |
| **Edit** an existing document | `unzip` $\rightarrow$ edit `word/document.xml` $\rightarrow$ `zip` (`docx-js` cannot open existing files) |
| **Read** content | `pandoc -t markdown file.docx` |

---

## 1. Creating with `docx-js` — Gotchas & Best Practices

`docx` is preinstalled — write scripts using `require('docx')` directly. Only run `npm install docx` if that require fails.

- **Page size**: Defaults to A4. For US Letter, set `page: { size: { width: 12240, height: 15840 } }` (DXA; 1440 = 1″).
- **Landscape**: Pass portrait dimensions and `orientation: PageOrientation.LANDSCAPE` — `docx-js` swaps width/height internally.
- **Tables need dual widths**: Set `columnWidths` on the table AND `width` on every cell, both in `WidthType.DXA` (PERCENTAGE breaks in Google Docs). Column widths must sum to the table width.
- **Table shading**: Use `ShadingType.CLEAR`, never `SOLID` (renders black).
- **Lists**: Never insert `•` literally; use a `numbering` config with `LevelFormat.BULLET`.
- **`ImageRun` requires `type:`** (`"png"`, `"jpg"`, …).
- **`PageBreak` must be inside a `Paragraph`.**
- **Never use `\n`** — use separate `Paragraph` elements.
- **TOC**: Headings must use built-in `HeadingLevel.*`; custom heading styles need `outlineLevel` set or they won't appear.
- **Horizontal Rules**: Don't use a table as a horizontal rule — use a paragraph bottom border instead.
- **Right Alignment on Same Line**: Use `PositionalTab` (`alignment: PositionalTabAlignment.RIGHT`, `leader: PositionalTabLeader.DOT`) inside a `TextRun`, not literal `.` or space padding.

---

## 2. Editing Existing Documents

Legacy `.doc` files must be converted first: `python scripts/office/soffice.py --headless --convert-to docx file.doc`.

```bash
unzip -q doc.docx -d unpacked/
find unpacked -type l -delete   # strip symlink entries
python scripts/merge_runs.py unpacked/   # coalesce fragmented runs so text is findable
# edit unpacked/word/document.xml in place — do NOT reformat or pretty-print
(cd unpacked && rm -f ../out.docx && zip -Xr ../out.docx .)
python scripts/office/validate.py out.docx --original doc.docx   # XSD checks
```

### Tracked Changes & Redlining
- When redlining, validate with `--author "<the name you redlined under>"` (needs `--original`).
- Wrap runs in `<w:ins>` / `<w:del>` with `w:id`, `w:author`, `w:date` attributes.
- Inside `<w:del>`, the text element is `<w:delText>`, not `<w:t>`.
- To produce a clean copy with all tracked changes accepted: `python scripts/accept_changes.py in.docx out.docx`.

---

## 3. Comments Engine

Comments require six cross-linked files. Use the helper script:

```bash
# Against an already-unpacked directory
python scripts/comment.py unpacked/ "Fees & expenses cap is too low"
python scripts/comment.py unpacked/ "Agreed" --parent 0

# Against a .docx directly
python scripts/comment.py contract.docx "This cap is too low" -o annotated.docx
```

---

## 4. Visual Verification & Output Inspection

After writing a `.docx`, render it to verify typography and formatting:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.docx
pdftoppm -jpeg -r 100 output.pdf page
ls page-*.jpg
```
