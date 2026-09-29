# Setup and usage

## Requirements

- Python 3.9+

## Install

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Scripts

### Extract text from a PDF

```bash
python scripts/extract_pdf_text.py path/to/file.pdf --out outputs/blocks.jsonl
```

Options:
- `--pages 1-5,9` extracts only those pages (1-based).
- `--min-chars 20` skips very short blocks such as page numbers.

Each output line contains `doc_id`, `page`, `block`, `bbox`, `raw_text`, and `text`.

### Validate records against a schema

```bash
python scripts/validate_json.py examples/sample_schema.json examples/sample.jsonl
```

Prints each failing record and field, then a summary. Exits with code 1 if anything is invalid, so it can be used in CI.

### Export a diagram

```bash
python scripts/export_figures.py --out outputs/ --dpi 400
```

Writes `pipeline.svg` (editable text) and `pipeline.png`. Edit `STEPS` in the script to change the boxes and colors.

## Data policy

Real source documents and outputs are excluded by `.gitignore`. Only synthetic example data is committed.
