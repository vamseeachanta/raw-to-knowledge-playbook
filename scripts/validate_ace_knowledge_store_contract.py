#!/usr/bin/env python3
"""Validate the ACE knowledge-store contract for issue 61."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = Path("config/ace-knowledge-store-contract.json")
SCHEMA_PATH = Path("artifacts/ace-wave0-ledger-schema.json")
SCHEMA_VALIDATOR_PATH = Path("scripts/validate_ace_wave0_schema_contract.py")
EXPECTED_STORAGE_FORMS = {"landing_page", "part_file", "dataset_table", "media_descriptor", "geometry_metadata", "private_sidecar_record", "exclusion_record", "retrieval_chunk", "eval_case"}
EXPECTED_METADATA_GROUPS = {"identity", "routing", "lifecycle", "verification", "provenance", "evaluation", "success"}
EXPECTED_LIFECYCLE_STATES = {"candidate", "provisional", "verified", "rejected", "superseded", "stale_requires_rescreen"}
ALLOWED_TRANSITIONS = {
    ("candidate", "provisional"),
    ("candidate", "rejected"),
    ("candidate", "stale_requires_rescreen"),
    ("provisional", "verified"),
    ("provisional", "rejected"),
    ("provisional", "stale_requires_rescreen"),
    ("verified", "superseded"),
    ("verified", "stale_requires_rescreen"),
    ("rejected", "stale_requires_rescreen"),
    ("stale_requires_rescreen", "provisional"),
    ("stale_requires_rescreen", "rejected"),
    ("superseded", "stale_requires_rescreen"),
}
EXPECTED_CHUNK_METADATA = {"citation_id", "logical_document_key", "edition", "revision", "is_current", "as_of_timestamp", "visibility", "lifecycle_state", "parse_status", "hash_reference", "structure_type", "route_target", "logical_target_store"}
EXPECTED_PRIVATE_PROVENANCE_FIELDS = {"private_provenance_bundle_ref"}
ALLOWED_VISIBILITY_VALUES = {"public", "private", "metadata_only"}
HEX_DIGEST_RE = re.compile(r"^[0-9a-f]{32,128}$", re.IGNORECASE)
DRIFT_RESET_FIELDS = {"source_fingerprint_ref", "manifest_snapshot_id", "route_target", "logical_target_store", "visibility", "boundary_policy_ref", "parser_version", "chunker_version"}
PRIVATE_SOURCE_TERMS = {"source_" + "id", "source_" + "sha256", "private_" + "lookup_key", "private_" + "lookup_map", "share_" + "relative_path_private_only"}
SOURCE_DIGEST_TERMS = {"source_" + "hash", "provenance_" + "pointer"}
TOKEN_LITERAL_RE = re.compile(r"\bpst_[0-9a-f]{32}\b")
DENIED_SOURCE_PATTERNS = [
    re.compile(r"\bfi" + r"nd\s+.*ACE_SHARE_ROOT"),
    re.compile(r"\bca" + r"t\s+.*ACE_SHARE_ROOT"),
    re.compile(r"\bsha256" + r"sum\s+(?:docs/master-index|assets|INDEX|_cad-index|\.ace-knowledge)"),
    re.compile(r"\bgrep\s+(?:-[A-Za-z]*[rR][A-Za-z]*\b|--recursive\b).*ACE_SHARE_ROOT"),
    re.compile(r"os" + r"\.walk\s*\("),
    re.compile(r"\." + r"rglob\s*\("),
]
BOUND_SKILL_EVAL_PATHS = [Path(path) for path in ("skills/page-shape-contract/evals/evals.json", "skills/source-extraction-coverage/evals/evals.json", "skills/source-extract-fidelity/evals/evals.json", "skills/verify-batch/evals/evals.json", "skills/independent-oracle-validation/evals/evals.json", "skills/public-private-routing/evals/evals.json", "skills/stacked-batch-prs/evals/evals.json")]


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def load_json(path: Path) -> dict:
    return json.loads(_repo_path(path).read_text())


def load_contract(path: Path = CONTRACT_PATH) -> dict:
    return load_json(path)


def load_wave0_schema(path: Path = SCHEMA_PATH) -> dict:
    return load_json(path)


def _load_schema_validator():
    validator_path = _repo_path(SCHEMA_VALIDATOR_PATH)
    spec = importlib.util.spec_from_file_location("validate_ace_wave0_schema_contract", validator_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def public_scan_paths() -> list[Path]:
    paths = [
        Path("docs/plans/2026-06-29-issue-61-ace-cross-wave-knowledge-store-retrieval-evaluation-lifecycle-contract.md"),
        Path("docs/plans/README.md"),
        Path("docs/plans/ace-share-ingestion-wave-coordination.md"),
        Path(".planning/plan-approved/61.md"),
        Path("docs/case-studies/ace-share-knowledge-store-contract.md"),
        Path("config/ace-knowledge-store-contract.json"),
        Path("config/ace-ingested-success-metric-contract.json"),
        Path("scripts/validate_ace_knowledge_store_contract.py"),
        Path("scripts/validate_ace_ingested_success_metric.py"),
        Path("tests/test_validate_ace_knowledge_store_contract.py"),
        Path("tests/test_validate_ace_ingested_success_metric.py"),
        Path("tests/fixtures/ace-knowledge-store-contract"),
        Path("docs/14-chunking-and-embedding.md"),
        Path("docs/15-retrieval-evaluation.md"),
        Path("docs/16-corpus-lifecycle.md"),
        Path("docs/07-data-governance.md"),
        Path("docs/19-trust-boundary-and-private-mode.md"),
        Path(".github/workflows/validate.yml"),
    ]
    paths.extend(BOUND_SKILL_EVAL_PATHS)
    return paths


def validate_contract_file(path: Path = CONTRACT_PATH) -> list[str]:
    try:
        contract = load_contract(path)
    except FileNotFoundError:
        return [f"missing knowledge-store contract: {path}"]
    except json.JSONDecodeError as exc:
        return [f"knowledge-store contract JSON is invalid: {exc}"]
    return validate_contract(contract)


def validate_contract(contract: dict, schema_path: Path = SCHEMA_PATH) -> list[str]:
    errors: list[str] = []
    _validate_metadata(contract, errors)
    _validate_route_dependency(contract, schema_path, errors)
    _validate_storage_forms(contract, errors)
    _validate_lifecycle(contract, errors)
    _validate_enum_owners(contract, errors)
    _validate_private_boundary(contract, errors)
    _validate_retrieval_and_eval_contract(contract, errors)
    errors.extend(validate_source_read_policy(json.dumps(contract, sort_keys=True)))
    return errors


def _validate_metadata(contract: dict, errors: list[str]) -> None:
    if contract.get("contract_id") != "ace-knowledge-store-contract":
        errors.append("knowledge-store contract_id must be ace-knowledge-store-contract")
    if contract.get("owner_issue") != 61:
        errors.append("knowledge-store contract owner_issue must be 61")
    if contract.get("depends_on_schema_issue") != 65:
        errors.append("knowledge-store contract must depend on #65 schema")
    if contract.get("depends_on_manifest_evidence_issue") != 62:
        errors.append("knowledge-store contract must depend on #62 evidence")
    if contract.get("publication_gate_issue") != 63:
        errors.append("knowledge-store contract must preserve #63 publication gate")
def _validate_route_dependency(contract: dict, schema_path: Path, errors: list[str]) -> None:
    dependency = contract.get("route_store_dependency", {})
    if (
        dependency.get("owner_issue") != 65
        or dependency.get("mode") != "import_only"
        or dependency.get("schema_path") != SCHEMA_PATH.as_posix()
        or dependency.get("validator_path") != SCHEMA_VALIDATOR_PATH.as_posix()
    ):
        errors.append("route/store dependency must import #65 in import_only mode")
    if "route_targets" in contract or "route_store_matrix" in contract:
        errors.append("knowledge-store contract must not redefine #65 route/store values")
    try:
        schema = load_wave0_schema(schema_path)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load #65 route/store schema: {exc}")
        return
    if not schema.get("route_targets") or not schema.get("route_store_matrix"):
        errors.append("#65 route/store schema must expose route_targets and route_store_matrix")
        return
    schema_errors = _load_schema_validator().validate_schema(schema)
    if schema_errors:
        errors.append("#65 route/store schema invalid: " + "; ".join(schema_errors))
def _validate_storage_forms(contract: dict, errors: list[str]) -> None:
    forms = set(contract.get("storage_forms", []))
    if forms != EXPECTED_STORAGE_FORMS:
        errors.append("storage form enum must be the closed #61 set")
    metadata = contract.get("required_metadata_by_storage_form", {})
    if set(metadata) != EXPECTED_STORAGE_FORMS:
        errors.append("metadata map must cover every storage form")
    for form, spec in metadata.items():
        groups = set(spec.get("field_groups", []))
        if not EXPECTED_METADATA_GROUPS <= groups:
            errors.append(f"metadata group coverage incomplete for {form}")
def _validate_lifecycle(contract: dict, errors: list[str]) -> None:
    states = set(contract.get("lifecycle_states", []))
    if states != EXPECTED_LIFECYCLE_STATES:
        errors.append("lifecycle state enum must be the closed #61 set")
    transitions = contract.get("lifecycle_transitions", [])
    pairs = {(item.get("from"), item.get("to")) for item in transitions}
    if pairs != ALLOWED_TRANSITIONS:
        errors.append("lifecycle transition table must match the approved #61 set")
    for item in transitions:
        if not item.get("reason_required"):
            errors.append("lifecycle transition requires reason_required")
def _validate_enum_owners(contract: dict, errors: list[str]) -> None:
    owners = contract.get("enum_owner_map", {})
    expected = {
        "route_target": ("owner_issue", 65),
        "logical_target_store": ("owner_issue", 65),
        "lifecycle_state": ("owner_issue", 61),
        "manifest_freshness_status": ("owner_issue", 62),
        "publication_certification_status": ("owner_issue", 63),
        "page_shape_parse_status": ("owner_skill", "page-shape-contract"),
    }
    for enum_name, (key, value) in expected.items():
        if owners.get(enum_name, {}).get(key) != value:
            errors.append(f"enum owner mismatch for {enum_name}")
def _validate_private_boundary(contract: dict, errors: list[str]) -> None:
    keys = set(_collect_keys(contract))
    if keys & PRIVATE_SOURCE_TERMS:
        errors.append("private source field terms must not appear as public JSON keys")
    if keys & SOURCE_DIGEST_TERMS:
        errors.append("source-like raw digest terms must not appear as public JSON keys")
    text_values = list(_collect_strings(contract))
    for value in text_values:
        if TOKEN_LITERAL_RE.search(value):
            errors.append("literal public token value is not allowed")
        for term in PRIVATE_SOURCE_TERMS:
            if re.search(rf"\b{re.escape(term)}\b\s*[:=]", value):
                errors.append("private source field assignment is not allowed")
    policy = contract.get("private_provenance_policy", {})
    if set(policy.get("allowed_public_fields", [])) != EXPECTED_PRIVATE_PROVENANCE_FIELDS:
        errors.append("private provenance must be exposed only through an opaque bundle reference")
    if policy.get("opaque_reference_required") is not True:
        errors.append("private provenance requires opaque_reference_required true")
    if policy.get("committed_private_lookup_material") is not False:
        errors.append("private provenance must not commit lookup material")
def _validate_retrieval_and_eval_contract(contract: dict, errors: list[str]) -> None:
    if set(contract.get("retrieval_chunk_required_metadata", [])) != EXPECTED_CHUNK_METADATA:
        errors.append("retrieval chunk metadata must be the closed #61 set")
    eval_contract = contract.get("eval_contract", {})
    if eval_contract.get("golden_cases_outside_ingest_path") is not True:
        errors.append("golden eval cases must stay outside ingest paths")
    if eval_contract.get("golden_cases_outside_chunk_store") is not True:
        errors.append("golden eval cases must stay outside chunk stores")
    if contract.get("bulk_scale_gate_requires_61") is not True:
        errors.append("bulk scale gate must require #61 binding")
    gate = contract.get("publication_gate", {})
    if gate.get("owner_issue") != 63 or gate.get("publication_exposure_allowed") is not False:
        errors.append("publication gate must block exposure until #63 canary evidence exists")
    blocked = set(gate.get("blocked_public_surfaces", []))
    required_blocked = {"docs_navigation", "mkdocs_yml", "llm_wiki", "external_publication", "derived_public_summaries"}
    if not required_blocked <= blocked:
        errors.append("publication gate must name docs nav, mkdocs, llm-wiki, external, and summary blocks")
def validate_lifecycle_events(events: list[dict], contract: dict | None = None) -> list[str]:
    reason_map = _transition_reason_map(contract)
    errors: list[str] = []
    for event in events:
        pair = (event.get("from"), event.get("to"))
        if pair not in ALLOWED_TRANSITIONS:
            errors.append(f"lifecycle transition is not allowed: {pair}")
            continue
        reason = event.get("reason", event.get("transition_reason"))
        if reason != reason_map.get(pair):
            errors.append(f"lifecycle transition reason mismatch for {pair}")
        if pair[0] == "stale_requires_rescreen" and not event.get("rescreen_evidence_ref"):
            errors.append("stale rescreen transition requires rescreen evidence")
    return errors
def _transition_reason_map(contract: dict | None = None) -> dict[tuple[str, str], str]:
    contract = contract or load_contract()
    return {
        (item.get("from"), item.get("to")): item.get("reason_required")
        for item in contract.get("lifecycle_transitions", [])
    }


def validate_storage_record_update(previous: dict, current: dict) -> list[str]:
    drifted = sorted(field for field in DRIFT_RESET_FIELDS if previous.get(field) != current.get(field))
    if drifted and current.get("lifecycle_state") != "stale_requires_rescreen":
        return ["storage record drift requires stale_requires_rescreen lifecycle state: " + ", ".join(drifted)]
    return []
def validate_retrieval_chunk_record(record: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(EXPECTED_CHUNK_METADATA - set(record))
    if missing:
        errors.append(f"retrieval chunk metadata missing: {', '.join(missing)}")
        return errors
    if record.get("lifecycle_state") not in EXPECTED_LIFECYCLE_STATES:
        errors.append("retrieval chunk lifecycle_state is invalid")
    if record.get("visibility") not in ALLOWED_VISIBILITY_VALUES:
        errors.append("retrieval chunk visibility is invalid")
    schema = load_wave0_schema()
    parse_values = set(schema.get("external_status_vocabularies", {}).get("page_shape_parse_status_values", {}).get("values", []))
    if record.get("parse_status") not in parse_values:
        errors.append("retrieval chunk parse_status is invalid")
    matrix = schema.get("route_store_matrix", {})
    route = record.get("route_target")
    store = record.get("logical_target_store")
    if route not in matrix or matrix.get(route) != store:
        errors.append("retrieval chunk route-store pair is invalid")
    hash_ref = str(record.get("hash_reference", ""))
    if HEX_DIGEST_RE.fullmatch(hash_ref) or any(term in hash_ref for term in SOURCE_DIGEST_TERMS):
        errors.append("retrieval chunk hash_reference must be an opaque non-raw-digest reference")
    if record.get("structure_type") == "table" and record.get("table_preserved") is not True:
        errors.append("table structure must be preserved for retrieval chunks")
    return errors


def validate_eval_case_record(record: dict) -> list[str]:
    errors: list[str] = []
    if record.get("storage_form") != "eval_case":
        errors.append("eval record must use eval_case storage form")
    if record.get("outside_ingest_path") is not True or record.get("outside_chunk_store") is not True:
        errors.append("eval leakage into ingest path or chunk store is not allowed")
    return errors


def validate_source_read_policy(text: str) -> list[str]:
    errors: list[str] = []
    for pattern in DENIED_SOURCE_PATTERNS:
        if pattern.search(text):
            errors.append("source traversal or raw manifest read is not allowed")
    try:
        import ace_public_surface_contract
    except ImportError:
        return errors
    for pattern in ace_public_surface_contract.UNBOUNDED_TRAVERSAL_PATTERNS:
        if pattern.search(text):
            errors.append("source traversal or raw manifest read is not allowed")
    return errors


def validate_skill_eval_file(path: Path) -> list[str]:
    try:
        payload = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return [f"skill eval JSON is invalid: {path}: {exc}"]
    matching = [case for case in payload.get("evals", []) if case.get("issue") == 61]
    if not matching:
        return [f"skill eval file missing issue 61 case: {path}"]
    errors = []
    for case in matching:
        if not str(case.get("id", "")).startswith("ace-61-"):
            errors.append(f"skill eval issue 61 case id must start with ace-61-: {path}")
    return errors


def validate_public_surfaces(paths: list[Path] | None = None) -> list[str]:
    script_dir = Path(__file__).resolve().parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))
    import ace_public_surface_scan

    scan_paths = [_repo_path(path) for path in (paths or public_scan_paths())]
    return ace_public_surface_scan.validate_public_artifact_paths(scan_paths)


def _collect_keys(value) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            keys.append(str(key))
            keys.extend(_collect_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.extend(_collect_keys(child))
    return keys


def _collect_strings(value) -> list[str]:
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, dict):
        for child in value.values():
            strings.extend(_collect_strings(child))
    elif isinstance(value, list):
        for child in value:
            strings.extend(_collect_strings(child))
    return strings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=str(CONTRACT_PATH), help="knowledge-store contract JSON path")
    parser.add_argument("--chunk-record", action="append", default=[], help="retrieval chunk record JSON path")
    parser.add_argument("--eval-record", action="append", default=[], help="eval case record JSON path")
    args = parser.parse_args(argv)
    errors = validate_contract_file(Path(args.contract))
    for record_path in args.chunk_record:
        try:
            errors.extend(validate_retrieval_chunk_record(load_json(Path(record_path))))
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            errors.append(f"retrieval chunk record is invalid: {record_path}: {exc}")
    for record_path in args.eval_record:
        try:
            errors.extend(validate_eval_case_record(load_json(Path(record_path))))
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            errors.append(f"eval case record is invalid: {record_path}: {exc}")
    for skill_path in BOUND_SKILL_EVAL_PATHS:
        errors.extend(validate_skill_eval_file(_repo_path(skill_path)))
    errors.extend(validate_public_surfaces())
    if errors:
        for error in errors:
            print(f"DENY  {error}", file=sys.stderr)
        print(f"\nFAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: ACE knowledge-store contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
