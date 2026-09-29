"""Validate JSON or JSONL records against a JSON Schema.

Usage:
    python scripts/validate_json.py schema.json data.jsonl
    python scripts/validate_json.py schema.json a.json b.json --quiet

Exit code is 0 if every record is valid, 1 otherwise.
"""
import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def load_records(path):
    """Yield (label, record) pairs from a .json or .jsonl file."""
    path = Path(path)
    if path.suffix == ".jsonl":
        with path.open(encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if line.strip():
                    yield f"{path.name}:{line_no}", json.loads(line)
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else [data]
        for i, item in enumerate(items, 1):
            yield f"{path.name}[{i}]", item


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("schema", help="Path to a JSON Schema file")
    parser.add_argument("files", nargs="+", help="JSON or JSONL files to check")
    parser.add_argument("--quiet", action="store_true", help="Only print the summary")
    args = parser.parse_args()

    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    total, bad = 0, 0
    for file in args.files:
        for label, record in load_records(file):
            total += 1
            errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
            if errors:
                bad += 1
                if not args.quiet:
                    for err in errors:
                        where = "/".join(str(p) for p in err.path) or "(root)"
                        print(f"FAIL {label} at {where}: {err.message}")

    print(f"\n{total - bad}/{total} records valid")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
