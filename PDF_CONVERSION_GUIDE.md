# PDF Conversion Guide

## Option 1: Python Script

```bash
pip install markdown2 weasyprint
python convert_to_pdf.py
```

## Option 2: Pandoc (Better Quality)

```bash
pandoc docs/PDF_DOCUMENTATION_TEMPLATE.md -o PROJECT_DOCUMENTATION.pdf --pdf-engine=xelatex --toc
```

## Option 3: VS Code

Install "Markdown PDF" extension, then right-click on `docs/PDF_DOCUMENTATION_TEMPLATE.md` → "Markdown PDF: Export (pdf)"

## Option 4: Online

Upload `docs/PDF_DOCUMENTATION_TEMPLATE.md` to https://www.markdowntopdf.com/
