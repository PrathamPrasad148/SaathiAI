---
name: pptx
description: "Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations as PowerPoint (.pptx) files; reading, parsing, or extracting text from any .pptx or .potx file (even if the extracted content will be used elsewhere, like in an email, summary, or creating a different type of slide deck); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates (.potx), layouts, speaker notes, or comments. Trigger whenever the user asks for a PowerPoint or .pptx file, or references a .pptx or .potx filename, regardless of what they plan to do with the content afterward. However, when the user asks for a deck, slides, a slide deck, or a presentation without naming a file format, default to using a dedicated slide-deck artifact type or a separate slides skill if this session offers one; otherwise, use this skill."
license: Proprietary
---

# PPTX Creation, Editing, and Analysis Skill

Use this skill whenever a PowerPoint presentation (`.pptx` or `.potx`) is referenced, created, analyzed, modified, or extracted.

A `.pptx` file is a ZIP archive of XML files. Choose the appropriate approach based on the target task:

| Task | Recommended Approach |
| :--- | :--- |
| **Create a new deck** | Write a `pptxgenjs` script or use `python-pptx` |
| **Edit an existing deck or template** | Unpack ZIP $\rightarrow$ edit `ppt/slides/slideN.xml` $\rightarrow$ repack ZIP |
| **Read content / extract text** | `markitdown deck.pptx` (one block per slide under `<!-- Slide number: N -->` markers) |

---

## 1. Creating Decks with `pptxgenjs` — Gotchas & Best Practices

If using Node.js `pptxgenjs` (`require('pptxgenjs')`):

1. **Set canvas dimensions**: Set `pres.layout` before adding slides. The default canvas is `LAYOUT_16x9` (10" × 5.625"). For widescreen 16:9 13.3" × 7.5", use `LAYOUT_WIDE`.
2. **Hex Colors**: Never include `#` and never use 8 digits (e.g., use `color: "FF0000"`). For translucency, use `transparency: 0-100` on fills/images, and `opacity: 0.0-1.0` on shadows.
3. **Immutability**: `pptxgenjs` mutates option objects in place. Never share one options/shadow object across two `add*` calls — create a fresh object each time.
4. **Shadow Offsets**: Shadow offset must be $\ge 0$. To cast a shadow upward, use `angle: 270` with a positive offset.
5. **Character Spacing**: `letterSpacing` is silently ignored; use `charSpacing`.
6. **Lists**: Set `bullet: true` on each item. Never insert a literal bullet character (`•`). Set `breakLine: true` on every array item except the last.
7. **New Instances**: Instantiate `new pptxgen()` per output file; never reuse an instance.
8. **Text Boxes**: Every `addText` call needs `isTextBox: true` for accessibility. Set `margin: 0` when text must align with shapes/lines.
9. **Speaker Notes**: Speaker notes go in `slide.addNotes("...")` (plain text), never in a slide body text box.
10. **Native Charts**: Use `addChart()` for native PowerPoint charts. On stacked bar or column charts, `dataLabelPosition` must be `ctr`, `inEnd`, or `inBase`.

---

## 2. Design Rules & Color Palettes

Don't create boring slides. Plain bullets on a white background won't impress anyone.

### Dominance Over Equality
- **Primary Color**: Dominates 60–70% of visual weight.
- **Supporting Tones**: 1–2 supporting colors.
- **Accent Tone**: 1 sharp accent for key highlights.
- **Visual Motif**: Pick ONE distinctive element and repeat it across slides (e.g. rounded image frames, icons in colored circles).

### Color Palettes
| Theme | Primary | Secondary | Accent |
| :--- | :--- | :--- | :--- |
| **Midnight Executive** | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` (white) |
| **Forest & Moss** | `2C5F2D` (forest) | `97BC62` (moss) | `F5F5F5` (cream) |
| **Coral Energy** | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) |
| **Warm Terracotta** | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) |
| **Ocean Gradient** | `065A82` (deep blue) | `1C7293` (teal) | `21295C` (midnight) |
| **Teal Trust** | `028090` (teal) | `00A896` (seafoam) | `02C39A` (mint) |

### Typography Hierarchy
- **Slide Title**: 36–44pt bold
- **Section Header**: 20–24pt bold
- **Body Text**: 14–16pt
- **Captions**: 10–12pt muted
- **Safe Fonts**: Arial, Calibri, Cambria, Times New Roman, Courier New, Bookman Old Style, Century Schoolbook.

### Avoid List (Common Mistakes)
- **NEVER** use accent lines under titles.
- **NEVER** add decorative color bars or accent stripes (header/footer bars spanning slide width, vertical sidebar stripes).
- **NEVER** default to cream/beige backgrounds (`F5F5DC`, `FAF0E6`). Use white (`FFFFFF`) or topic palette.
- **NEVER** create text-only slides — add images, icons, charts, or visual card layouts.
- **NEVER** center body text — left-align paragraphs and lists; center only main slide titles.

---

## 3. Scripts & Tools Reference

| Script | Function |
| :--- | :--- |
| `scripts/thumbnail.py deck.pptx [prefix]` | Generates labeled grid images of every slide for template analysis. |
| `scripts/add_slide.py unpacked/ slide2.xml [--after slideN.xml]` | Duplicates a slide with package bookkeeping. |
| `scripts/clean.py unpacked/` | Removes orphaned slides, media, and rels. |
| `scripts/office/validate.py deck.pptx [--original src.pptx]` | Validates OOXML schema and chart relationships. |
| `scripts/office/soffice.py --headless --convert-to pdf deck.pptx` | Headless LibreOffice wrapper for PDF conversion. |

---

## 4. Visual QA & Verification Process

1. **Content QA**:
   ```bash
   markitdown output.pptx
   ```
   Check for missing content, typos, or leftover placeholder text (`TODO`, `Lorem Ipsum`).

2. **File Schema Validation**:
   ```bash
   python scripts/office/validate.py output.pptx
   ```

3. **Visual Inspection**:
   Convert slides to JPEG images via headless PDF conversion:
   ```bash
   python scripts/office/soffice.py --headless --convert-to pdf output.pptx
   pdftoppm -jpeg -r 150 output.pdf slide
   ```
