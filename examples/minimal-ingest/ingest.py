#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["pdfplumber>=0.11"]
# ///
"""Minimal raw-to-knowledge loop on ONE table — the playbook in ~120 lines.

    EXTRACT (deterministic)  →  PROVISIONAL  →  VERIFY (vision)  →  PROMOTE

This is the smallest honest slice of the pipeline (docs 02/03). It uses only an
ADOPT-tier permissive extractor (pdfplumber, MIT) and the Python stdlib.

WHAT IS REAL vs STUBBED
- REAL: deterministic text/table extraction; the provisional-by-default gate;
  the doc-03 verdict decision tree; the binary-faithful, closed-set verdict.
- STUBBED: the *vision* comparator. In production a VLM compares a rendered page
  PNG against the CSV cell-by-cell. Offline/CI can't call a VLM, so here the
  comparator diffs the extracted CSV against a committed ground_truth.csv that
  stands in for "what the rendered page actually says." Swap `vision_compare()`
  for a real VLM call to go live — the surrounding gate is unchanged.

Usage:
    uv run ingest.py                 # happy path  → VERIFIED
    uv run ingest.py --inject-defect # simulate an A7 OCR digit-substitution → DEFERRED
    uv run ingest.py --check         # run, then assert outputs == expected/ fixtures (CI)
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, sys
from pathlib import Path

import pdfplumber

HERE = Path(__file__).parent
PDF = HERE / "sample" / "allowable_stress.pdf"
GROUND_TRUTH = HERE / "ground_truth" / "allowable_stress.csv"
OUT = HERE / "out"
TABLE_ID = "EX-001-table-3"
SOURCE_PAGE = 1

# Closed sets (doc 03) — the agent/script may write ONLY these.
PARSE_STATUS = {"provisional-unverified", "verified", "rejected", "deferred"}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows_to_csv(rows: list[list[str]]) -> str:
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(rows)
    return buf.getvalue()


def csv_to_rows(text: str) -> list[list[str]]:
    return [r for r in csv.reader(io.StringIO(text))]


# 1. EXTRACT — deterministic, not an LLM ------------------------------------
def extract(pdf: Path) -> list[list[str]]:
    with pdfplumber.open(pdf) as doc:
        table = doc.pages[SOURCE_PAGE - 1].extract_table()
    if not table:
        return []
    return [[("" if c is None else c.strip()) for c in row] for row in table]


# 2. VERIFY — the vision step (STUBBED by ground-truth diff) -----------------
def vision_compare(extracted: list[list[str]], truth: list[list[str]]) -> dict:
    """Stand-in for a VLM comparing the rendered page to the CSV, cell-by-cell.

    Returns a verdict from the closed set with a *specific, falsifiable* evidence
    string when it rejects/defers (doc 03: "prefer the review citing a specific
    falsifiable defect").
    """
    if not extracted:
        return {"verdict": "rejected", "defect": "not-a-data-table",
                "evidence": "extractor produced no table region"}
    if len(extracted) != len(truth) or any(len(r) != len(truth[0]) for r in extracted):
        return {"verdict": "deferred", "defect": "A5-truncated/shape-mismatch",
                "evidence": f"shape {len(extracted)}x{len(extracted[0]) if extracted else 0} "
                            f"!= source {len(truth)}x{len(truth[0])}"}
    header_noise = []
    for ri, (er, tr) in enumerate(zip(extracted, truth)):
        for ci, (ev, tv) in enumerate(zip(er, tr)):
            if ev == tv:
                continue
            if ri == 0:  # OCR noise in HEADER only → verified-with-note (doc 03)
                header_noise.append(f"r0c{ci}: '{ev}'~'{tv}'")
                continue
            # value mismatch in a DATA cell → defect; classify digit-substitution
            defect = "A7-ocr-digit-substitution" if (ev.isdigit() and tv.isdigit()) else "A6-value-mismatch"
            return {"verdict": "deferred", "defect": defect,
                    "evidence": f"cell (row {ri}, col {ci}): page shows '{tv}', CSV has '{ev}'"}
    note = f"header OCR noise: {'; '.join(header_noise)}" if header_noise else "all cells match source"
    return {"verdict": "verified", "defect": None, "evidence": note}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inject-defect", action="store_true",
                    help="perturb one extracted cell to demonstrate the gate catching an A7 defect")
    ap.add_argument("--check", action="store_true", help="assert outputs match expected/ fixtures")
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)

    # --- EXTRACT ---
    extracted = extract(PDF)
    if args.inject_defect and len(extracted) > 4:
        # simulate failure-class A7: '565' misread as '585' in a data cell
        extracted[4] = [c if c != "565" else "585" for c in extracted[4]]

    provisional_csv = rows_to_csv(extracted)
    (OUT / "provisional.csv").write_text(provisional_csv)

    # --- PROVISIONAL page + queue row (trust nothing by default) ---
    src_hash = sha256(PDF)
    page_md = (
        f"---\n"
        f"table_id: {TABLE_ID}\n"
        f"publisher: Example (synthetic)\n"
        f"source_page: {SOURCE_PAGE}\n"
        f"sources: sha256:{src_hash}\n"
        f"parse_status: provisional-unverified\n"
        f"visibility: public\n"
        f"---\n\n"
        f"# Allowable Stress by Material Grade (Example Spec EX-001)\n\n"
        f"> Auto-extracted. **provisional-unverified** — do not cite values until the vision pass promotes it.\n\n"
        f"```csv\n{provisional_csv}```\n"
    )

    # --- VERIFY ---
    truth = csv_to_rows(GROUND_TRUTH.read_text())
    verdict = vision_compare(extracted, truth)
    assert verdict["verdict"] in PARSE_STATUS, "verdict escaped the closed set"

    queue_row = {
        "table_id": TABLE_ID, "csv_path": "out/provisional.csv", "source_page": SOURCE_PAGE,
        "parse_status": verdict["verdict"], "defect_class": verdict["defect"],
        "verifier": "vision-stub (ground-truth diff)", "verification_notes": verdict["evidence"],
    }
    (OUT / "queue_row.json").write_text(json.dumps(queue_row, indent=2) + "\n")

    # --- PROMOTE (only on verified) ---
    if verdict["verdict"] == "verified":
        page_md = page_md.replace("parse_status: provisional-unverified", "parse_status: verified")
        page_md = page_md.replace(
            "> Auto-extracted. **provisional-unverified** — do not cite values until the vision pass promotes it.",
            f"> **verified** — vision pass confirmed cell-by-cell ({verdict['evidence']}). Safe to cite.")
        (OUT / "verified.csv").write_text(provisional_csv)
    (OUT / "page.md").write_text(page_md)

    # --- REPORT ---
    print(f"EXTRACT  : {len(extracted)} rows via pdfplumber (deterministic)")
    print(f"PROVISIONAL: out/provisional.csv  (sha256 source pinned: {src_hash[:12]}…)")
    print(f"VERIFY   : {verdict['verdict'].upper()}"
          + (f"  [{verdict['defect']}]  {verdict['evidence']}" if verdict["defect"] else f"  ({verdict['evidence']})"))
    print(f"PROMOTE  : {'out/verified.csv + page.md(verified)' if verdict['verdict']=='verified' else 'held provisional; defect queued for re-extract'}")

    if args.check:
        return run_checks(args.inject_defect)
    return 0


def run_checks(defect_mode: bool) -> int:
    """Assert the run reproduced the committed fixtures."""
    fixtures = "expected_defect" if defect_mode else "expected"
    exp = HERE / fixtures
    ok = True
    for name in ["provisional.csv", "queue_row.json", "page.md"]:
        got = (OUT / name).read_text()
        want = (exp / name).read_text()
        if got != want:
            ok = False
            print(f"  MISMATCH {name}", file=sys.stderr)
    print("CHECK    :", "PASS — outputs match fixtures" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
