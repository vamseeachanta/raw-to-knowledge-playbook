#!/usr/bin/env python3
"""Validate the ACE wave-2 spreadsheet/CSV ingestion lane."""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

CSV_HELPER_DIR = REPO_ROOT / "skills" / "format-coverage-ledger" / "resources"
if str(CSV_HELPER_DIR) not in sys.path:
    sys.path.insert(0, str(CSV_HELPER_DIR))

from ace_bounded_sampling_firewall import validate_sampling_request as firewall_validate_sampling_request  # noqa: E402
from validate_ace_ingested_success_metric import validate_metric_record as issue61_validate_metric_record  # noqa: E402
from csv_dialect_probe import validate_convention_sidecar  # noqa: E402


SCHEMA_PATH = Path("artifacts/ace-wave0-ledger-schema.json")
FIXTURE_ROOT = Path("tests/fixtures/ace-wave2-spreadsheet-csv")
PLAN_PATH = Path("docs/plans/2026-06-29-issue-53-ace-wave-2-spreadsheets-csv-calculation-workbook-ingestion-lane.md")
APPROVAL_MARKER_PATH = Path(".planning/plan-approved/53.md")
WORKFLOW_PATH = Path(".github/workflows/validate.yml")
WORKBOOK_CLASSES = {"data_workbook", "calculation_workbook", "report_workbook", "excluded_workbook"}
ORIGINAL_CANARY_CLASSES = {"data", "calculation", "mixed", "guarded", "unsupported"}
DELIMITED_CLASSES = {"csv_table", "delimited_table", "ragged_delimited"}
RAW_WORKBOOK_SUFFIXES = {".xls", ".xlsx", ".xlsm", ".xlsb", ".ods"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
OLE_CF_HEADER = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
DURABLE_FIELDS = {
    "target_path",
    "retrieval_metadata",
    "lifecycle_state",
    "persistent_metric",
    "private_measured_sidecar",
    "private_sidecar",
    "private_sidecar_path",
}


def repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def load_json(path: Path) -> Any:
    return json.loads(repo_path(path).read_text())


def route_store(route: str) -> str | None:
    return load_json(SCHEMA_PATH).get("route_store_matrix", {}).get(route)


def validate_workbook_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    route = record.get("route_target")
    if record.get("workbook_class") not in WORKBOOK_CLASSES:
        errors.append("workbook_class must use the closed ACE wave-2 workbook enum")
    if record.get("original_canary_class") not in ORIGINAL_CANARY_CLASSES:
        errors.append("original_canary_class must preserve the existing canary class")
    errors.extend(_validate_route_fields(record))
    if record.get("workbook_class") == "calculation_workbook":
        triplet = record.get("calculation_triplet")
        if record.get("cached_values_only"):
            errors.append("cached values are evidence only, not verification")
        if not isinstance(triplet, dict) or not all(triplet.get(key) for key in ["input_contract", "code_artifact", "output_proof"]):
            errors.append("calculation triplet requires input_contract, code_artifact, and output_proof")
    if record.get("workbook_class") == "excluded_workbook":
        if route not in {"metadata_only", "excluded_no_ingest"}:
            errors.append("excluded_workbook must route metadata_only or excluded_no_ingest")
        if route == "metadata_only":
            if record.get("content_eligible") is not False:
                errors.append("metadata-only excluded_workbook must set content_eligible=false")
            if not isinstance(record.get("deferral_reasons"), list) or not record["deferral_reasons"]:
                errors.append("metadata-only excluded_workbook must record deferral_reasons")
    if DURABLE_FIELDS & set(record):
        errors.append("durable output fields are outside #53 classifier rows")
    if route == "public_llm_wiki":
        errors.append("#63 public-output canary evidence is required before public_llm_wiki route")
    if not isinstance(record.get("known_losses"), list) or not record["known_losses"]:
        errors.append("known_losses must record spreadsheet/data extraction losses")
    if route != "excluded_no_ingest":
        for field in ["extraction_estimate", "extraction_yield"]:
            if not isinstance(record.get(field), dict) or not record[field]:
                errors.append(f"{field} must be a non-empty object")
    return errors


def validate_csv_probe(probe: dict[str, Any], sidecar: dict[str, Any] | None) -> list[str]:
    errors: list[str] = []
    if probe.get("delimiter") not in {",", ";", "\t", "|"}:
        errors.append("CSV delimiter must be detected from the closed delimiter set")
    errors.extend(_validate_probe_shape(probe))
    if probe.get("ragged_rows"):
        errors.append("ragged rows must route excluded_no_ingest")
    if not isinstance(probe.get("content_digest"), str) or not SHA256_RE.fullmatch(probe["content_digest"]):
        errors.append("content_digest must be a sha256 hex digest")
    errors.extend(validate_convention_sidecar(probe, sidecar))
    return errors


def validate_ledger_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    records = payload.get("records")
    if not isinstance(records, list):
        return ["ledger payload must include records list"]
    valid_records: list[dict[str, Any]] = []
    for record in records:
        if not isinstance(record, dict):
            errors.append("ledger records must be JSON objects")
            continue
        valid_records.append(record)
        if record.get("source_kind") == "workbook":
            errors.extend(validate_workbook_record(record))
        elif record.get("source_kind") == "delimited":
            errors.extend(validate_delimited_record(record))
        else:
            errors.append("source_kind must be workbook or delimited")
    metric = payload.get("metric", {})
    errors.extend(validate_metric_record(metric))
    if isinstance(metric, dict):
        errors.extend(_validate_metric_matches_records(metric, valid_records))
    return errors


def validate_delimited_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if record.get("delimited_class") not in DELIMITED_CLASSES:
        errors.append("delimited_class must use the closed wave-2 delimited enum")
    errors.extend(_validate_route_fields(record))
    probe = record.get("dialect_probe")
    if not isinstance(probe, dict):
        errors.append("dialect probe is required for delimited rows")
    else:
        for field in ["delimiter", "header", "row_count", "expected_field_count", "field_counts", "ragged_rows", "content_digest", "numeric_columns"]:
            if field not in probe:
                errors.append(f"dialect probe missing {field}")
        sidecar = record.get("convention_sidecar")
        if not isinstance(sidecar, dict):
            errors.append("convention sidecar is required for delimited rows")
        elif not sidecar.get("producer"):
            errors.append("convention sidecar missing producer")
        probe_errors = validate_csv_probe(probe, record.get("convention_sidecar"))
        if record.get("delimited_class") == "ragged_delimited" and record.get("route_target") == "excluded_no_ingest":
            probe_errors = [error for error in probe_errors if not error.startswith("ragged rows")]
        errors.extend(probe_errors)
    if record.get("delimited_class") == "ragged_delimited" and record.get("route_target") != "excluded_no_ingest":
        errors.append("ragged delimited rows must route excluded_no_ingest")
    if not isinstance(record.get("known_losses"), list) or not record["known_losses"]:
        errors.append("known_losses must record CSV/delimited extraction losses")
    return errors


def validate_metric_record(record: Any) -> list[str]:
    if not isinstance(record, dict):
        return ["metric record must be a JSON object"]
    errors = issue61_validate_metric_record(record)
    if record.get("metric_status") not in {"measured", "no_eligible_candidates", "no_classified_items"}:
        errors.append("metric_status must be an ingestion-wave status")
    if record.get("wave_class") != "ingestion_wave":
        errors.append("wave_class must be ingestion_wave for #53")
    return errors


def validate_sampling_request(request: Any) -> list[str]:
    if not isinstance(request, dict):
        return ["sampling request must be a JSON object"]
    result = firewall_validate_sampling_request(request)
    if result.authorized:
        return []
    return [item for item in [result.reason_code, *result.errors] if item]


def validate_committed_sampling_fixture(path: Path) -> list[str]:
    errors = validate_sampling_request(load_json(path))
    allowed_fail_closed = {
        "MISSING_62_EVIDENCE_POINTER",
        "SELF_ATTESTED_62_EVIDENCE",
        "FIXTURE_62_EVIDENCE_NOT_OPERATIONAL",
        "UNTRUSTED_62_EVIDENCE",
        "62_EVIDENCE_NOT_AUTHORIZING",
    }
    if any(error in allowed_fail_closed for error in errors):
        return []
    if not errors:
        return ["committed #53 sample manifest must fail closed without trusted #70 evidence"]
    return errors


def validate_no_raw_workbook_bytes(root: Path = FIXTURE_ROOT) -> list[str]:
    base = repo_path(root)
    errors: list[str] = []
    for path in _fixture_files(base):
        try:
            rel = path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            rel = path.as_posix()
        if path.is_symlink():
            errors.append(f"fixture symlink is not allowed: {rel}")
        elif _looks_like_raw_workbook(path):
            errors.append(f"raw workbook fixture is not allowed: {rel}")
    return errors


def validate_public_surfaces(paths: list[Path] | None = None) -> list[str]:
    import ace_public_surface_scan
    import validate_ace_public_artifacts

    scan_paths = [repo_path(path) for path in (paths or public_scan_paths())]
    errors = ace_public_surface_scan.validate_public_artifact_paths(scan_paths)
    errors.extend(validate_ace_public_artifacts.collect_errors(scan_public_paths=scan_paths))
    return errors


def public_scan_paths() -> list[Path]:
    return [
        PLAN_PATH,
        Path("docs/plans/README.md"),
        Path("docs/plans/ace-share-ingestion-wave-coordination.md"),
        APPROVAL_MARKER_PATH,
        Path("scripts/validate_ace_wave2_spreadsheet_csv.py"),
        Path("tests/test_validate_ace_wave2_spreadsheet_csv.py"),
        FIXTURE_ROOT,
        Path("skills/xlsx-input-code-output-canary/SKILL.md"),
        Path("skills/xlsx-input-code-output-canary/resources/xlsx_canary.py"),
        Path("skills/xlsx-input-code-output-canary/evals/evals.json"),
        Path("skills/format-coverage-ledger/SKILL.md"),
        Path("skills/format-coverage-ledger/resources/csv_dialect_probe.py"),
        Path("skills/format-coverage-ledger/evals/evals.json"),
        Path("docs/09-office-formats.md"),
        Path("docs/10-structured-data-and-model-files.md"),
        Path("scripts/review/results/2026-07-03-implementation-53-runtime-r4.md"),
        Path("scripts/review/results/2026-07-03-implementation-53-public-legal-r4.md"),
        Path("scripts/review/results/2026-07-03-implementation-53-docs-skills-r4.md"),
        WORKFLOW_PATH,
    ]


def _validate_route_fields(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    route = record.get("route_target")
    if route not in set(load_json(SCHEMA_PATH)["route_targets"]):
        errors.append("route_target must use the #65 closed route enum")
    expected_store = route_store(route)
    if record.get("logical_target_store") != expected_store:
        errors.append(f"logical_target_store must be {expected_store} for route_target={route}")
    expected_visibility = {
        "public_llm_wiki": "public",
        "private_sidecar": "private",
        "metadata_only": "private",
        "excluded_no_ingest": "none",
    }.get(route)
    if record.get("visibility") != expected_visibility:
        errors.append(f"visibility must be {expected_visibility} for route_target={route}")
    if route == "private_sidecar":
        errors.append("durable output fields are outside #53 classifier rows")
    return errors


def _validate_probe_shape(probe: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    header = probe.get("header")
    row_count = probe.get("row_count")
    expected_field_count = probe.get("expected_field_count")
    field_counts = probe.get("field_counts")
    ragged_rows = probe.get("ragged_rows")
    numeric_columns = probe.get("numeric_columns")
    if not isinstance(header, list) or not header or not all(isinstance(column, str) and column for column in header):
        errors.append("dialect probe header must be a non-empty array of column names")
    if not isinstance(row_count, int) or row_count < 0:
        errors.append("dialect probe row_count must be a non-negative integer")
    if not isinstance(expected_field_count, int) or expected_field_count <= 0:
        errors.append("dialect probe expected_field_count must be a positive integer")
    if not isinstance(field_counts, list) or not field_counts or not all(isinstance(count, int) and count > 0 for count in field_counts):
        errors.append("dialect probe field_counts must be a non-empty array of positive integers")
    if not isinstance(ragged_rows, list):
        errors.append("dialect probe ragged_rows must be an array")
    if not isinstance(numeric_columns, list) or not all(isinstance(column, str) and column for column in numeric_columns):
        errors.append("dialect probe numeric_columns must be an array of column names")
    if isinstance(header, list) and isinstance(expected_field_count, int) and len(header) != expected_field_count:
        errors.append("dialect probe header must match expected_field_count")
    if isinstance(header, list) and isinstance(numeric_columns, list):
        unknown_columns = sorted(set(numeric_columns) - set(header))
        if unknown_columns:
            errors.append(f"dialect probe numeric_columns must reference header columns: {', '.join(unknown_columns)}")
    if isinstance(row_count, int) and isinstance(field_counts, list) and field_counts and len(field_counts) != row_count + 1:
        errors.append("dialect probe row_count must match field_counts excluding the header")
    if isinstance(expected_field_count, int) and isinstance(field_counts, list) and field_counts:
        if field_counts[0] != expected_field_count:
            errors.append("dialect probe header field_count must match expected_field_count")
        observed_ragged_rows = [
            {"row_number": row_number, "field_count": count, "expected_field_count": expected_field_count}
            for row_number, count in enumerate(field_counts[1:], start=2)
            if count != expected_field_count
        ]
        if isinstance(ragged_rows, list):
            valid_shape = all(
                isinstance(item, dict)
                and set(item) == {"row_number", "field_count", "expected_field_count"}
                and all(isinstance(item[key], int) for key in ["row_number", "field_count", "expected_field_count"])
                for item in ragged_rows
            )
            if not valid_shape:
                errors.append("dialect probe ragged_rows entries must use row_number, field_count, and expected_field_count integers")
            elif ragged_rows != observed_ragged_rows:
                errors.append("dialect probe ragged_rows must match field_counts")
    return errors


def _looks_like_raw_workbook(path: Path) -> bool:
    if path.suffix.lower() in RAW_WORKBOOK_SUFFIXES:
        return True
    try:
        with path.open("rb") as handle:
            header = handle.read(512)
    except OSError:
        return False
    if header.startswith(OLE_CF_HEADER):
        return True
    if not zipfile.is_zipfile(path):
        return False
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            lowered = {name.lower() for name in names}
            if "[content_types].xml" in lowered and any(name.startswith("xl/") for name in lowered):
                return True
            if any(name.startswith("xl/worksheets/") for name in lowered):
                return True
            if "mimetype" in names:
                mimetype = archive.read("mimetype").decode("utf-8", errors="replace")
                return "spreadsheet" in mimetype
    except (OSError, zipfile.BadZipFile):
        return False
    return False


def _fixture_files(root: Path) -> list[Path]:
    pending = [root]
    files: list[Path] = []
    while pending:
        current = pending.pop()
        if current.is_symlink() or current.is_file():
            files.append(current)
        elif current.is_dir():
            pending.extend(sorted(current.iterdir(), reverse=True))
    return files


def _validate_metric_matches_records(metric: dict[str, Any], records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if metric.get("metric_scope") != "synthetic_fixture":
        errors.append("metric_scope must be synthetic_fixture for committed wave-2 fixtures")
    total = len(records)
    excluded = sum(1 for record in records if record.get("route_target") == "excluded_no_ingest")
    eligible = total - excluded
    successful = eligible
    expected = {
        "total_classified_items": total,
        "hard_excluded_items": excluded,
        "eligible_candidate_items": eligible,
        "successful_routed_items": successful,
    }
    for key, value in expected.items():
        if metric.get(key) != value:
            errors.append(f"{key} must match ledger records")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", action="append", default=[], help="wave-2 ledger JSON path")
    parser.add_argument("--manifest", action="append", default=[], help="wave-2 sampling manifest JSON path")
    args = parser.parse_args(argv)
    errors: list[str] = []
    errors.extend(validate_no_raw_workbook_bytes())
    for path in args.ledger or [str(FIXTURE_ROOT / "valid-ledger.json")]:
        errors.extend(validate_ledger_payload(load_json(Path(path))))
    if args.manifest:
        for path in args.manifest:
            errors.extend(validate_sampling_request(load_json(Path(path))))
    else:
        errors.extend(validate_committed_sampling_fixture(FIXTURE_ROOT / "sample-manifest.json"))
    errors.extend(validate_public_surfaces())
    if errors:
        for error in errors:
            print(f"DENY  {error}", file=sys.stderr)
        print(f"\nFAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: ACE wave-2 spreadsheet/CSV lane valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
