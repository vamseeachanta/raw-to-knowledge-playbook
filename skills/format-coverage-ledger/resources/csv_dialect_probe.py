"""CSV/delimited dialect and row-integrity probe for ACE wave 2."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


COMMON_DELIMITERS = [",", ";", "\t", "|"]


def probe_csv(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    data = source.read_bytes()
    text = data.decode("utf-8", errors="replace")
    delimiter = _detect_delimiter(text)
    rows = list(csv.reader(text.splitlines(), delimiter=delimiter))
    header = rows[0] if rows else []
    expected_width = len(header)
    ragged_rows = [
        {"row_number": index + 1, "field_count": len(row), "expected_field_count": expected_width}
        for index, row in enumerate(rows[1:], start=1)
        if len(row) != expected_width
    ]
    return {
        "path": source.name,
        "delimiter": delimiter,
        "quotechar": '"',
        "encoding": "utf-8",
        "line_ending": _line_ending(text),
        "header": header,
        "row_count": max(0, len(rows) - 1),
        "expected_field_count": expected_width,
        "field_counts": [len(row) for row in rows],
        "ragged_rows": ragged_rows,
        "content_digest": hashlib.sha256(data).hexdigest(),
        "numeric_columns": _numeric_columns(header, rows[1:]),
    }


def validate_convention_sidecar(probe: dict[str, Any], sidecar: dict[str, Any] | None) -> list[str]:
    if not probe.get("numeric_columns"):
        return []
    if not isinstance(sidecar, dict):
        return ["convention sidecar is required for numeric delimited data"]
    errors: list[str] = []
    for field in ["units", "sign_conventions", "coordinate_frames", "producer"]:
        if field not in sidecar:
            errors.append(f"convention sidecar missing {field}")
    for column in probe["numeric_columns"]:
        for field in ["units", "sign_conventions", "coordinate_frames"]:
            values = sidecar.get(field, {})
            if not isinstance(values, dict) or column not in values:
                errors.append(f"convention sidecar missing {field}.{column}")
    return errors


def _detect_delimiter(text: str) -> str:
    sample = "\n".join(text.splitlines()[:10])
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters="".join(COMMON_DELIMITERS))
        if dialect.delimiter in COMMON_DELIMITERS:
            return dialect.delimiter
    except csv.Error:
        pass
    scores = {delimiter: _delimiter_score(sample, delimiter) for delimiter in COMMON_DELIMITERS}
    return max(scores, key=scores.get)


def _delimiter_score(text: str, delimiter: str) -> tuple[int, int, int]:
    rows = list(csv.reader(text.splitlines(), delimiter=delimiter))
    widths = [len(row) for row in rows if row]
    if not widths:
        return (0, 0, 0)
    width_counts = {width: widths.count(width) for width in set(widths)}
    dominant_width = max(width_counts, key=width_counts.get)
    multi_column_rows = sum(1 for width in widths if width > 1)
    return (multi_column_rows, width_counts[dominant_width], dominant_width)


def _line_ending(text: str) -> str:
    if "\r\n" in text:
        return "CRLF"
    if "\r" in text:
        return "CR"
    return "LF"


def _numeric_columns(header: list[str], data_rows: list[list[str]]) -> list[str]:
    numeric: list[str] = []
    for index, name in enumerate(header):
        values = [row[index] for row in data_rows if index < len(row) and row[index] != ""]
        if values and all(_is_number(value) for value in values):
            numeric.append(name)
    return numeric


def _is_number(value: str) -> bool:
    try:
        float(value)
    except ValueError:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    print(json.dumps(probe_csv(args.path), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
