#!/usr/bin/env python3
"""Validate the ACE ingested-success metric contract for issue 61."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = Path("config/ace-ingested-success-metric-contract.json")
SCHEMA_PATH = Path("artifacts/ace-wave0-ledger-schema.json")
FIXTURE_ROOT = Path("tests/fixtures/ace-knowledge-store-contract")
EXPECTED_STATUSES = {
    "measured",
    "no_eligible_candidates",
    "no_classified_items",
    "not_applicable_control_plane",
    "invalid_metric",
}
CONTROL_GATE_CLASSES = {
    "control_plane",
    "storage_lifecycle_gate",
    "manifest_freshness_gate",
    "public_canary_gate",
}


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def load_json(path: Path) -> dict:
    return json.loads(_repo_path(path).read_text())


def known_wave_classes(schema_path: Path = SCHEMA_PATH) -> set[str]:
    schema = load_json(schema_path)
    return {row.get("wave_class") for row in schema.get("canonical_wave_registry", [])}


def public_scan_paths() -> list[Path]:
    return [
        Path("docs/plans/2026-06-29-issue-61-ace-cross-wave-knowledge-store-retrieval-evaluation-lifecycle-contract.md"),
        Path("docs/plans/README.md"),
        Path("docs/plans/ace-share-ingestion-wave-coordination.md"),
        Path(".planning/plan-approved/61.md"),
        Path("config/ace-ingested-success-metric-contract.json"),
        Path("scripts/validate_ace_ingested_success_metric.py"),
        Path("tests/test_validate_ace_ingested_success_metric.py"),
        Path("tests/fixtures/ace-knowledge-store-contract/valid-ingestion-metric.json"),
        Path("tests/fixtures/ace-knowledge-store-contract/valid-control-metric.json"),
        Path("tests/fixtures/ace-knowledge-store-contract/valid-no-eligible-metric.json"),
        Path("tests/fixtures/ace-knowledge-store-contract/valid-no-classified-metric.json"),
        Path(".github/workflows/validate.yml"),
    ]


def validate_metric_contract_file(path: Path = CONTRACT_PATH) -> list[str]:
    try:
        contract = load_json(path)
    except FileNotFoundError:
        return [f"missing metric contract: {path}"]
    except json.JSONDecodeError as exc:
        return [f"metric contract JSON is invalid: {exc}"]
    return validate_metric_contract(contract)


def validate_metric_contract(contract: dict, schema_path: Path = SCHEMA_PATH) -> list[str]:
    errors: list[str] = []
    if contract.get("contract_id") != "ace-ingested-success-metric-contract":
        errors.append("metric contract_id must be ace-ingested-success-metric-contract")
    if contract.get("owner_issue") != 61:
        errors.append("metric contract owner_issue must be 61")
    if contract.get("imports_success_fields_from_issue") != 65:
        errors.append("metric contract must import success fields from issue 65")
    statuses = set(contract.get("metric_status_values", []))
    if statuses != EXPECTED_STATUSES:
        errors.append("metric status vocabulary must be the closed #61 set")
    metric = contract.get("success_metric", {})
    if metric.get("numerator_field") != "successful_routed_items":
        errors.append("success numerator must be successful_routed_items")
    if metric.get("denominator_field") != "eligible_candidate_items":
        errors.append("success denominator must be eligible_candidate_items")
    exclusion = contract.get("exclusion_metric", {})
    if exclusion.get("numerator_field") != "hard_excluded_items":
        errors.append("exclusion numerator must be hard_excluded_items")
    if exclusion.get("denominator_field") != "total_classified_items":
        errors.append("exclusion denominator must be total_classified_items")
    if exclusion.get("formula") != "hard_excluded_items / total_classified_items * 100":
        errors.append("exclusion formula must be hard_excluded_items / total_classified_items * 100")
    errors.extend(_validate_schema_fields(metric, schema_path))
    return errors


def _validate_schema_fields(metric: dict, schema_path: Path) -> list[str]:
    try:
        schema = load_json(schema_path)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return [f"cannot load #65 schema for metric fields: {exc}"]
    success_fields = set(schema.get("ledger_field_groups", {}).get("success", []))
    required = {metric.get("numerator_field"), metric.get("denominator_field")}
    if not required <= success_fields:
        return ["metric fields must be imported from #65 success vocabulary"]
    return []


def validate_metric_record(record: dict) -> list[str]:
    errors: list[str] = []
    status = record.get("metric_status")
    if status not in EXPECTED_STATUSES - {"invalid_metric"}:
        errors.append("metric_status must be a valid committed status")
    wave_class = record.get("wave_class")
    if wave_class not in known_wave_classes():
        errors.append("wave_class must be imported from the #65 canonical registry")
        return errors
    if wave_class in CONTROL_GATE_CLASSES:
        return errors + _validate_control_record(record)
    if status == "measured":
        errors.extend(_validate_measured_record(record))
    elif status == "no_eligible_candidates":
        errors.extend(_validate_no_eligible_record(record))
    elif status == "no_classified_items":
        errors.extend(_validate_no_classified_record(record))
    return errors


def _count(record: dict, key: str) -> int:
    value = record.get(key)
    return value if isinstance(value, int) else -1


def _validate_base_counts(record: dict) -> tuple[int, int, int, int, list[str]]:
    total = _count(record, "total_classified_items")
    excluded = _count(record, "hard_excluded_items")
    eligible = _count(record, "eligible_candidate_items")
    successful = _count(record, "successful_routed_items")
    errors: list[str] = []
    if min(total, excluded, eligible, successful) < 0:
        errors.append("metric counts must be non-negative integers")
    if eligible != total - excluded:
        errors.append("eligible_candidate_items must equal total_classified_items minus hard exclusions")
    if excluded > total:
        errors.append("hard exclusions cannot exceed total_classified_items")
    if successful > eligible:
        errors.append("successful_routed_items cannot exceed eligible_candidate_items")
    return total, excluded, eligible, successful, errors


def _validate_measured_record(record: dict) -> list[str]:
    total, excluded, eligible, successful, errors = _validate_base_counts(record)
    if eligible <= 0:
        errors.append("measured metric requires eligible_candidate_items > 0")
        return errors
    expected_success = successful / eligible * 100
    expected_excluded = excluded / total * 100 if total else 0.0
    if not _matches(record.get("ingested_success_percent"), expected_success):
        errors.append("ingested success percent must match successful_routed_items / eligible_candidate_items * 100")
    if total > 0 and not _matches(record.get("excluded_percent"), expected_excluded):
        errors.append("hard exclusions must be reported separately as excluded_percent")
    return errors


def _validate_no_eligible_record(record: dict) -> list[str]:
    total, excluded, eligible, successful, errors = _validate_base_counts(record)
    if total <= 0 or eligible != 0 or successful != 0:
        errors.append("no_eligible_candidates requires classified rows but zero eligible candidates")
    if "ingested_success_percent" in record:
        errors.append("no_eligible_candidates must not emit ingested_success_percent")
    expected_excluded = excluded / total * 100 if total else None
    if expected_excluded is not None and not _matches(record.get("excluded_percent"), expected_excluded):
        errors.append("no_eligible_candidates must still report exclusion percent when classified rows exist")
    return errors


def _validate_no_classified_record(record: dict) -> list[str]:
    total, excluded, eligible, successful, errors = _validate_base_counts(record)
    if any(value != 0 for value in [total, excluded, eligible, successful]):
        errors.append("no_classified_items requires zero counts")
    if "excluded_percent" in record or "ingested_success_percent" in record:
        errors.append("no_classified_items must not emit percentages")
    return errors


def _validate_control_record(record: dict) -> list[str]:
    errors: list[str] = []
    if record.get("metric_status") != "not_applicable_control_plane":
        errors.append("control plane rows require not_applicable_control_plane status")
    for key in ["total_classified_items", "hard_excluded_items", "eligible_candidate_items", "successful_routed_items"]:
        if record.get(key, 0) != 0:
            errors.append("control plane sentinel requires zero counts")
    for key in ["measured_success_numerator", "measured_success_denominator", "success_threshold"]:
        if record.get(key) != 0:
            errors.append(f"control plane sentinel requires {key}=0")
    for key in ["ingested_success_percent", "excluded_percent"]:
        if key in record:
            errors.append("control plane sentinel must not emit percentages")
    return errors


def _matches(actual, expected: float) -> bool:
    return isinstance(actual, (int, float)) and math.isclose(float(actual), expected, rel_tol=0, abs_tol=1e-9)


def validate_public_surfaces(paths: list[Path] | None = None) -> list[str]:
    script_dir = Path(__file__).resolve().parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))
    import ace_public_surface_scan

    scan_paths = [_repo_path(path) for path in (paths or public_scan_paths())]
    return ace_public_surface_scan.validate_public_artifact_paths(scan_paths)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=str(CONTRACT_PATH), help="metric contract JSON path")
    parser.add_argument("--record", action="append", default=[], help="metric record JSON path")
    args = parser.parse_args(argv)
    errors = validate_metric_contract_file(Path(args.contract))
    for record_path in args.record:
        try:
            errors.extend(validate_metric_record(load_json(Path(record_path))))
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            errors.append(f"metric record is invalid: {record_path}: {exc}")
    errors.extend(validate_public_surfaces())
    if errors:
        for error in errors:
            print(f"DENY  {error}", file=sys.stderr)
        print(f"\nFAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: ACE ingested-success metric contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
