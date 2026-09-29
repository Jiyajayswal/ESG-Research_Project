"""Extract text blocks from a PDF into JSONL.

Each output line is one text block with its page number, order on the page,
bounding box, and text. Useful as a first pass before manual review.

Usage:
    python scripts/extract_pdf_text.py input.pdf --out outputs/blocks.jsonl
    python scripts/extract_pdf_text.py input.pdf --pages 1-5 --min-chars 20
"""
import argparse
import json
import re
import sys
from pathlib import Path

import pymupdf


def parse_pages(spec, page_count):
    """Turn '1-3,7' into a sorted list of 0-based page indexes."""
    if not spec:
        return list(range(page_count))
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            pages.update(range(int(start) - 1, int(end)))
        else:
            pages.add(int(part) - 1)
    return sorted(p for p in pages if 0 <= p < page_count)


def clean_text(text):
    """Join hyphenated line breaks and collapse whitespace."""
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    return re.sub(r"\s+", " ", text).strip()


def extract(pdf_path, pages_spec=None, min_chars=1):
    doc = pymupdf.open(pdf_path)
    doc_id = Path(pdf_path).stem
    for page_index in parse_pages(pages_spec, doc.page_count):
        page = doc[page_index]
        blocks = page.get_text("blocks", sort=True)
        if not any(b[6] == 0 and b[4].strip() for b in blocks):
            print(f"Warning: page {page_index + 1} has no text layer "
                  "(scanned image?). Run OCR first.", file=sys.stderr)
            continue
        order = 0
        for x0, y0, x1, y1, text, _block_no, block_type in blocks:
            if block_type != 0:  # skip image blocks
                continue
            cleaned = clean_text(text)
            if len(cleaned) < min_chars:
                continue
            order += 1
            yield {
                "doc_id": doc_id,
                "page": page_index + 1,
                "block": order,
                "bbox": [round(v, 2) for v in (x0, y0, x1, y1)],
                "raw_text": text,
                "text": cleaned,
            }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pdf", help="Path to a PDF file")
    parser.add_argument("--out", default="outputs/blocks.jsonl", help="Output JSONL path")
    parser.add_argument("--pages", help="Pages to extract, e.g. '1-3,7' (1-based)")
    parser.add_argument("--min-chars", type=int, default=1, help="Skip blocks shorter than this")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with out_path.open("w", encoding="utf-8") as f:
        for record in extract(args.pdf, args.pages, args.min_chars):
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    print(f"Wrote {count} blocks to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
