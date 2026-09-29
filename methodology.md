# pdf-annotation-tools

Small utilities for extracting and structuring text from PDF documents
so it can be reviewed and annotated in downstream NLP workflows.

## What's here

| Path | Purpose |
|---|---|
| `scripts/extract_pdf_text.py` | Extracts text blocks from a PDF with page numbers, block order, and bounding boxes, and writes them to JSONL. |
| `scripts/validate_json.py` | Validates JSON/JSONL records against a JSON Schema and reports errors per record. |
| `scripts/export_figures.py` | Builds a simple pipeline diagram and exports it as SVG and high-DPI PNG. |
| `examples/` | Fake sample data and an example schema for trying the scripts. |
| `docs/setup.md` | Installation and usage instructions. |

## Quick start

```bash
pip install -r requirements.txt
python scripts/validate_json.py examples/sample_schema.json examples/sample.jsonl
python scripts/export_figures.py --out outputs/
python scripts/extract_pdf_text.py path/to/any.pdf --out outputs/blocks.jsonl
```

See `docs/setup.md` for details.

## Notes

All example data in this repository is synthetic.
