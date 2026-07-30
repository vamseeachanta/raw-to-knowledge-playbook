#!/usr/bin/env python3
"""Validate the ACE wave-1 text/markup/code/small-JSON bootstrap."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

CONTRACT_PATH = Path("config/ace-wave1-text-json-contract.json")
SCHEMA_PATH = Path("artifacts/ace-wave0-ledger-schema.json")
FIXTURE_ROOT = Path("tests/fixtures/ace-wave1-text-json")
WORKFLOW_PATH = Path(".github/workflows/validate.yml")
PLAN_PATH = Path("docs/plans/2026-06-29-issue-52-ace-wave-1-llm-native-text-markup-code-small-json-bootstrap.md")
CASE_STUDY_PATH = Path("docs/case-studies/ace-wave-1-text-markup-code-json-bootstrap.md")
APPROVAL_MARKER_PATH = Path(".planning/plan-approved/52.md")
HELPER_PATH = Path("skills/content-triage-and-exclusion/resources/text_json_triage.py")
EXPECTED_CLASSES = {
    "hand_authored_markup",
    "small_config_json",
    "generated_repetitive_json",
    "generated_lockfile_like_json",
    "code_documentation",
    "source_tree_noise",
    "hard_excluded_material",
}

from ace_bounded_sampling_firewall import validate_sampling_request as firewall_validate_sampling_request  # noqa: E402
from validate_ace_ingested_success_metric import validate_metric_record as issue61_validate_metric_record  # noqa: E402


def repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def load_json(path: Path) -> Any:
    return json.loads(repo_path(path).read_text())


def validate_contract_file(path: Path = CONTRACT_PATH) -> list[str]:
    try:
        return validate_contract(load_json(path))
    except FileNotFoundError:
        return [f"missing wave-1 contract: {path}"]
    except json.JSONDecodeError as exc:
        return [f"wave-1 contract JSON is invalid: {exc}"]


def validate_contract(contract: dict) -> list[str]:
    schema = load_json(SCHEMA_PATH)
    errors: list[str] = []
    if contract.get("contract_id") != "ace-wave1-text-json-contract":
        errors.append("contract_id must be ace-wave1-text-json-contract")
    if contract.get("owner_issue") != 52:
        errors.append("owner_issue must be 52")
    if contract.get("imports_route_targets_from_issue") != 65:
        errors.append("route targets must be imported from issue 65")
    if contract.get("route_targets") != schema.get("route_targets"):
        errors.append("route targets must match #65 route_targets exactly")
    for field_name in ["kept_row_required_fields", "excluded_row_required_fields"]:
        if "logical_target_store" not in contract.get(field_name, []):
            errors.append(f"{field_name} must require logical_target_store")
    metric = contract.get("success_metric", {})
    if metric.get("numerator_field") != "successful_routed_items":
        errors.append("success numerator must be successful_routed_items")
    if metric.get("denominator_field") != "eligible_candidate_items":
        errors.append("success denominator must be eligible_candidate_items")
    if set(contract.get("candidate_classes", [])) != EXPECTED_CLASSES:
        errors.append("candidate_classes must match the closed wave-1 set")
    errors.extend(_validate_sampling_gate(contract.get("sampling_gate", {}), schema))
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
        return ["committed #52 sample manifest must fail closed without trusted #70 evidence"]
    return errors


def validate_candidate_record(row: dict) -> list[str]:
    contract = load_json(CONTRACT_PATH)
    errors: list[str] = []
    route = row.get("route_target")
    if route not in set(contract["route_targets"]):
        errors.append("candidate route_target must use the closed route enum")
        return errors
    if row.get("candidate_class") not in set(contract["candidate_classes"]):
        errors.append("candidate_class must use the closed wave-1 set")
    errors.extend(_validate_route_compatibility(row, contract))
    errors.extend(_validate_row_shape(row, contract))
    errors.extend(_validate_route_store(row, route))
    if row.get("hard_exclusion_reason") and route != "excluded_no_ingest":
        errors.append("hard exclusions must route excluded_no_ingest before value ranking")
    required = _required_fields_for_route(route, contract)
    missing = [field for field in required if field not in row]
    if missing:
        errors.append(f"candidate row missing required field(s): {', '.join(missing)}")
    if route == "public_llm_wiki":
        errors.extend(_validate_public_route_evidence(row))
    if _has_durable_output_without_gate(row, contract):
        errors.append("durable output fields are outside #52 and require a separate #61-backed implementation gate")
    return errors


def validate_routing_payload(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["routing payload must be a JSON object"]
    candidates = payload.get("candidates")
    if not isinstance(candidates, list):
        return ["routing payload must include candidates list"]
    valid_candidates: list[dict] = []
    for row in candidates:
        if not isinstance(row, dict):
            errors.append("candidate rows must be JSON objects")
            continue
        valid_candidates.append(row)
        errors.extend(validate_candidate_record(row))
    metric = payload.get("metric", {})
    errors.extend(validate_metric_record(metric))
    if isinstance(metric, dict):
        errors.extend(_validate_metric_matches_candidates(metric, valid_candidates))
    return errors


def validate_metric_record(record: Any) -> list[str]:
    if not isinstance(record, dict):
        return ["metric record must be a JSON object"]
    errors = issue61_validate_metric_record(record)
    if record.get("metric_status") not in {"measured", "no_eligible_candidates", "no_classified_items"}:
        errors.append("metric_status must be an ingestion-wave status")
    if record.get("wave_class") != "ingestion_wave":
        errors.append("wave_class must be ingestion_wave for #52")
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
        CASE_STUDY_PATH,
        CONTRACT_PATH,
        HELPER_PATH,
        Path("scripts/validate_ace_wave1_text_json.py"),
        Path("tests/test_validate_ace_wave1_text_json.py"),
        Path("tests/fixtures/ace-wave1-text-json/"),
        Path("docs/01-document-taxonomy.md"),
        Path("docs/10-structured-data-and-model-files.md"),
        Path("docs/14-chunking-and-embedding.md"),
        Path("docs/15-retrieval-evaluation.md"),
        Path("docs/16-corpus-lifecycle.md"),
        Path("skills/content-triage-and-exclusion/SKILL.md"),
        Path("skills/content-triage-and-exclusion/evals/evals.json"),
        Path("skills/source-extraction-coverage/SKILL.md"),
        Path("skills/source-extraction-coverage/evals/evals.json"),
        Path("skills/source-extract-fidelity/SKILL.md"),
        Path("skills/source-extract-fidelity/evals/evals.json"),
        Path("skills/page-shape-contract/SKILL.md"),
        Path("skills/page-shape-contract/evals/evals.json"),
        Path("skills/public-private-routing/SKILL.md"),
        Path("skills/public-private-routing/evals/evals.json"),
        WORKFLOW_PATH,
    ]


def _validate_sampling_gate(gate: dict, schema: dict) -> list[str]:
    row = {entry["issue"]: entry for entry in schema["canonical_wave_registry"]}[52]
    errors: list[str] = []
    expected = {
        "target_issue": 52,
        "target_wave_class": row["wave_class"],
        "request_class": "downstream_manifest_backed_sampling",
        "requires_manifest_snapshot_id": row["requires_manifest_snapshot_id"],
    }
    for key, value in expected.items():
        if gate.get(key) != value:
            errors.append(f"sampling_gate must set {key} to {value!r}")
    return errors


def _required_fields_for_route(route: str, contract: dict) -> list[str]:
    if route == "excluded_no_ingest":
        return contract["excluded_row_required_fields"]
    return contract["kept_row_required_fields"]


def _validate_route_compatibility(row: dict, contract: dict) -> list[str]:
    candidate_class = row.get("candidate_class")
    route = row.get("route_target")
    allowed = contract.get("class_route_targets", {}).get(candidate_class, [])
    if route not in allowed:
        return [f"route compatibility violation for {candidate_class}: {route}"]
    return []


def _validate_row_shape(row: dict, contract: dict) -> list[str]:
    errors: list[str] = []
    if row.get("parse_status") not in contract.get("parse_status_values", []):
        errors.append("parse_status must use the wave-1 closed set")
    if row.get("visibility") not in contract.get("visibility_values", []):
        errors.append("visibility must use the wave-1 closed set")
    route = row.get("route_target")
    if route == "public_llm_wiki" and row.get("visibility") != "public":
        errors.append("public route requires visibility=public")
    if route == "private_sidecar" and row.get("visibility") != "private":
        errors.append("private_sidecar route requires visibility=private")
    if route == "metadata_only" and row.get("visibility") != "private":
        errors.append("metadata_only route requires visibility=private")
    if route == "excluded_no_ingest" and row.get("visibility") != "none":
        errors.append("excluded_no_ingest route requires visibility=none")
    if not isinstance(row.get("signals"), list) or not row.get("signals"):
        errors.append("signals must be a non-empty list")
    if route != "excluded_no_ingest":
        for field_name in ["extraction_estimate", "extraction_yield"]:
            value = row.get(field_name)
            if not isinstance(value, dict) or not value:
                errors.append(f"{field_name} must be a non-empty object")
    return errors


def _validate_route_store(row: dict, route: str) -> list[str]:
    store = row.get("logical_target_store")
    expected = load_json(SCHEMA_PATH).get("route_store_matrix", {}).get(route)
    if store != expected:
        return [f"logical_target_store must be {expected} for route_target={route}"]
    return []


def _has_durable_output_without_gate(row: dict, contract: dict) -> bool:
    fields = set(contract["durable_output_gate"]["field_names"])
    return bool(fields & set(row))


def _validate_public_route_evidence(row: dict) -> list[str]:
    errors: list[str] = []
    if row.get("public_clearance") is not True:
        errors.append("public_clearance is required before public_llm_wiki route")
        return errors
    evidence = row.get("public_clearance_evidence")
    if not isinstance(evidence, dict):
        return ["#63 public-output canary evidence is required before public_llm_wiki route"]
    required = set(load_json(Path("config/ace-public-output-contract.json"))["required_certification_evidence"])
    if set(evidence) != required:
        errors.append("#63 public-output certification evidence must use the closed evidence field set")
        return errors
    if evidence.get("exit_code") != 0:
        errors.append("#63 public-output canary evidence requires exit_code=0")
    if evidence.get("contract_version") != load_json(Path("config/ace-public-output-contract.json"))["contract_version"]:
        errors.append("#63 public-output canary evidence contract_version must match the #63 contract")
    if not isinstance(evidence.get("canary_command"), str) or "validate_ace_public_artifacts.py" not in evidence["canary_command"]:
        errors.append("#63 public-output canary evidence must name the public-output validator command")
    if not isinstance(evidence.get("timestamp_utc"), str) or not evidence["timestamp_utc"]:
        errors.append("#63 public-output canary evidence requires timestamp_utc")
    paths = evidence.get("scanned_paths")
    if not isinstance(paths, list) or not paths:
        errors.append("#63 public-output canary evidence must include scan_public_paths")
    else:
        output_path = row.get("public_output_path")
        if not isinstance(output_path, str) or not output_path:
            errors.append("exact public surface requires public_output_path")
        elif set(paths) != {output_path}:
            errors.append("#63 public-output canary evidence must scan the exact public surface")
        from validate_ace_public_artifacts import collect_errors  # noqa: WPS433

        errors.extend(collect_errors(scan_public_paths=[Path(path) for path in paths]))
    return errors


def _validate_metric_matches_candidates(metric: dict, candidates: list[dict]) -> list[str]:
    errors: list[str] = []
    if metric.get("metric_scope") != "synthetic_fixture":
        errors.append("metric_scope must be synthetic_fixture for committed wave-1 routing fixtures")
    total = len(candidates)
    excluded = sum(1 for row in candidates if row.get("route_target") == "excluded_no_ingest")
    eligible = total - excluded
    successful = sum(1 for row in candidates if row.get("route_target") != "excluded_no_ingest")
    expected = {
        "total_classified_items": total,
        "hard_excluded_items": excluded,
        "eligible_candidate_items": eligible,
        "successful_routed_items": successful,
    }
    for key, value in expected.items():
        if metric.get(key) != value:
            errors.append(f"{key} must match candidate rows")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=str(CONTRACT_PATH), help="wave-1 contract JSON path")
    parser.add_argument("--manifest", action="append", default=[], help="wave-1 sampling manifest JSON path")
    parser.add_argument("--routing", action="append", default=[], help="candidate routing JSON path")
    args = parser.parse_args(argv)
    errors = validate_contract_file(Path(args.contract))
    if args.manifest:
        for path in args.manifest:
            errors.extend(validate_sampling_request(load_json(Path(path))))
    else:
        errors.extend(validate_committed_sampling_fixture(FIXTURE_ROOT / "sample-manifest.json"))
    for path in args.routing or [str(FIXTURE_ROOT / "expected-routing.json")]:
        payload = load_json(Path(path))
        errors.extend(validate_routing_payload(payload))
    errors.extend(validate_public_surfaces())
    if errors:
        for error in errors:
            print(f"DENY  {error}", file=sys.stderr)
        print(f"\nFAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: ACE wave-1 text/JSON bootstrap valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
