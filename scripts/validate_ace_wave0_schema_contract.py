#!/usr/bin/env python3
"""Validate the ACE wave 0 schema contract for issue 65."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = Path("artifacts/ace-wave0-ledger-schema.json")
PARENT_VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_epic_wave_coordination.py"
COORDINATION_PATH = Path("docs/plans/ace-share-ingestion-wave-coordination.md")
PLAN_PATH = Path("docs/plans/2026-06-30-issue-65-ace-wave-0-ledger-schema-route-store-matrix.md")
EXPECTED_ROUTES = {
    "public_llm_wiki": "public_llm_wiki_store",
    "private_sidecar": "private_sidecar_store",
    "metadata_only": "metadata_ledger_store",
    "excluded_no_ingest": "excluded_no_store",
}
EXPECTED_VERIFICATION_STATES = {
    "not_verified",
    "validator_passed",
    "independent_review_passed",
    "verification_rejected",
}
EXPECTED_FIELD_GROUPS = {
    "identity",
    "routing",
    "content",
    "method",
    "validation",
    "success",
    "readiness",
    "downstream_contracts",
}
EXPECTED_SPLIT_DEPENDENCIES = {
    65: [],
    66: [65],
    67: [65],
    68: [65, 66],
    69: [65],
}
EXPECTED_SPLIT_PLAN_PATHS = {
    65: "docs/plans/2026-06-30-issue-65-ace-wave-0-ledger-schema-route-store-matrix.md",
    66: "docs/plans/2026-06-30-issue-66-ace-public-token-fixtures-private-field-placeholders.md",
    67: "docs/plans/2026-06-30-issue-67-ace-wave-0-bounded-sampling-firewall.md",
    68: "docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md",
    69: "docs/plans/2026-07-01-issue-69-repo-local-legal-security-scan-gate.md",
}
ALLOWED_SPLIT_STATUS_SNAPSHOTS = {
    "status:plan-approved",
    "status:plan-review",
    "status:blocked-draft",
    "status:draft",
    "status:plan-required",
}
PRIVATE_SOURCE_TERMS = {
    "source_" + "id",
    "source_" + "sha256",
    "private_" + "lookup_key",
    "private_" + "lookup_map",
    "share_" + "relative_path_private_only",
}
SOURCE_LIKE_DIGEST_TERMS = {
    "source_" + "hash",
    "provenance_" + "pointer",
}
HEX_DIGEST = re.compile(r"^[0-9a-f]{32,128}$", re.IGNORECASE)
FORBIDDEN_STORE_PATH_PARTS = ("/", "\\", ":", "..")


def _load_parent_validator():
    spec = importlib.util.spec_from_file_location("validate_ace_epic_wave_coordination", PARENT_VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_schema(path: Path = SCHEMA_PATH) -> dict:
    schema_path = _repo_path(path)
    return json.loads(schema_path.read_text())


def validate_schema_file(path: Path = SCHEMA_PATH) -> list[str]:
    errors: list[str] = []
    try:
        schema = load_schema(path)
    except FileNotFoundError:
        return [f"missing schema file: {path}"]
    except json.JSONDecodeError as exc:
        return [f"schema JSON is invalid: {exc}"]
    errors.extend(validate_schema(schema))
    errors.extend(validate_coordination_compatibility(schema))
    errors.extend(validate_public_surfaces())
    return errors


def validate_schema(schema: dict, approval_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    approval_root = approval_root or REPO_ROOT / ".planning" / "plan-approved"
    _validate_metadata(schema, errors)
    _validate_routes_and_stores(schema, errors)
    _validate_verification_states(schema, errors)
    _validate_field_groups(schema, errors)
    _validate_private_terms(schema, errors)
    _validate_downstream_contracts(schema, errors)
    _validate_split_registry(schema, approval_root, errors)
    _validate_canonical_wave_registry(schema, errors)
    return errors


def validate_coordination_compatibility(schema: dict) -> list[str]:
    errors: list[str] = []
    text = _repo_path(COORDINATION_PATH).read_text()
    for row in schema.get("canonical_wave_registry", []):
        issue = row.get("issue")
        cells = [
            f"#{issue}",
            row.get("wave_class"),
            str(row.get("requires_manifest_snapshot_id")).lower(),
            row.get("success_numerator_field"),
            row.get("success_denominator_field"),
        ]
        expected_line = "| " + " | ".join(cells) + " |"
        if expected_line not in text:
            errors.append(f"coordination registry missing schema row: {expected_line}")
    if "artifacts/ace-wave0-ledger-schema.json" not in text or "scripts/validate_ace_wave0_schema_contract.py" not in text:
        errors.append("coordination split registry must show #65 schema and validator artifacts")
    return errors


def public_scan_paths() -> list[Path]:
    paths = [
        PLAN_PATH,
        Path("docs/plans/README.md"),
        COORDINATION_PATH,
        SCHEMA_PATH,
        Path("scripts/validate_ace_wave0_schema_contract.py"),
        Path("tests/test_validate_ace_wave0_schema_contract.py"),
        Path(".github/workflows/validate.yml"),
    ]
    review_root = REPO_ROOT / "scripts" / "review" / "results"
    if review_root.exists():
        for artifact in sorted(review_root.glob("*plan-65*.md")):
            paths.append(artifact.relative_to(REPO_ROOT))
    paths.extend(changed_bound_skill_docs())
    return paths


def changed_bound_skill_docs() -> list[Path]:
    return []


def validate_public_surfaces(paths: list[Path] | None = None) -> list[str]:
    parent = _load_parent_validator()
    scan_paths = paths or public_scan_paths()
    return parent.validate_public_artifact_paths([_repo_path(path) for path in scan_paths])


def _validate_metadata(schema: dict, errors: list[str]) -> None:
    if schema.get("schema_id") != "ace-wave0-ledger-schema":
        errors.append("schema metadata must name ace-wave0-ledger-schema")
    if not re.fullmatch(r"1\.0\.\d+", str(schema.get("schema_version", ""))):
        errors.append("schema metadata must use a 1.0.x schema_version")
    if schema.get("owner_issue") != 65:
        errors.append("schema metadata must set owner_issue 65")
    if schema.get("status") != "plan-approved":
        errors.append("schema metadata must reflect plan-approved status")
    if schema.get("route_contract_owner_issue") != 51:
        errors.append("schema metadata must preserve #51 route contract ownership")
    if not schema.get("public_safety_notes"):
        errors.append("schema metadata must include public_safety_notes")


def _validate_routes_and_stores(schema: dict, errors: list[str]) -> None:
    routes = set(schema.get("route_targets", []))
    stores = set(schema.get("logical_target_stores", []))
    matrix = schema.get("route_store_matrix", {})
    if routes != set(EXPECTED_ROUTES):
        errors.append("route target enum must be the closed #65 set")
    if stores != set(EXPECTED_ROUTES.values()):
        errors.append("logical store enum must be the closed #65 set")
    if matrix != EXPECTED_ROUTES:
        errors.append("route-store matrix must map each route to its logical store")
    for store in matrix.values():
        if store not in EXPECTED_ROUTES.values() or any(part in store for part in FORBIDDEN_STORE_PATH_PARTS):
            errors.append(f"logical store must not be a physical, repo, host, or wiki path: {store}")


def _validate_verification_states(schema: dict, errors: list[str]) -> None:
    states = set(schema.get("control_plane_verification_states", []))
    if states != EXPECTED_VERIFICATION_STATES:
        errors.append("verification state enum must be the closed #65 set")
    vocabularies = schema.get("external_status_vocabularies", {})
    for name in ["issue_61_lifecycle_states", "page_shape_parse_status_values"]:
        values = set(vocabularies.get(name, {}).get("values", []))
        if states & values:
            errors.append(f"verification state enum must be disjoint from {name}")


def _validate_field_groups(schema: dict, errors: list[str]) -> None:
    if set(schema.get("required_field_groups", [])) != EXPECTED_FIELD_GROUPS:
        errors.append("required field groups must match the downstream split contract")
    declared = set(schema.get("ledger_field_groups", {}))
    if declared != EXPECTED_FIELD_GROUPS:
        errors.append("ledger field groups must define every required field group")
    if set(schema.get("method_issue_bindings", [])) != {1, 12}:
        errors.append("schema must bind method issues #1 and #12")
    if "public-private-routing" not in set(schema.get("bound_skill_groups", [])):
        errors.append("schema must bind the public-private-routing skill group")


def _validate_private_terms(schema: dict, errors: list[str]) -> None:
    if set(schema.get("private_source_field_terms", [])) != PRIVATE_SOURCE_TERMS:
        errors.append("private source field terms must match the closed schema-term set")
    if set(schema.get("source_like_raw_digest_terms", [])) != SOURCE_LIKE_DIGEST_TERMS:
        errors.append("source-like raw digest terms must match the closed schema-term set")
    keys = _collect_keys(schema)
    for term in PRIVATE_SOURCE_TERMS:
        if term in keys:
            errors.append(f"private source field term must be an array value, not a JSON key: {term}")
    for term in SOURCE_LIKE_DIGEST_TERMS:
        if term in keys:
            errors.append(f"source-like raw digest term must be an array value, not a JSON key: {term}")
    for key, value in _walk_items(schema):
        if key in SOURCE_LIKE_DIGEST_TERMS and isinstance(value, str) and HEX_DIGEST.fullmatch(value):
            errors.append(f"source-like raw digest assignment is not allowed for key: {key}")
        if isinstance(value, str):
            for term in PRIVATE_SOURCE_TERMS:
                if value != term and re.search(rf"\b{re.escape(term)}\b\s*[:=]", value):
                    errors.append(f"private source field assignment is not allowed for value: {term}")
            for term in SOURCE_LIKE_DIGEST_TERMS:
                if re.search(rf"\b{re.escape(term)}\b\s*[:=]\s*[0-9a-f]{{32,128}}\b", value, re.I):
                    errors.append(f"source-like raw digest assignment is not allowed for value: {term}")


def _validate_downstream_contracts(schema: dict, errors: list[str]) -> None:
    contracts = schema.get("downstream_contracts", {})
    token = contracts.get("public_token", {})
    if token.get("owner_issues") != [66, 63]:
        errors.append("public token contract must be owned by #66 and #63")
    if token.get("generation_status") != "delegated_not_implemented_in_65":
        errors.append("public token generation must be delegated outside #65")
    if "grammar" in token:
        errors.append("public token grammar must not be implemented in #65")
    for name, issue in {
        "sampling_firewall": 67,
        "public_surface_scan": 68,
        "legal_security_scan": 69,
        "durable_private_storage": 61,
        "publication_certification": 63,
    }.items():
        if contracts.get(name, {}).get("owner_issue") != issue:
            errors.append(f"{name} downstream contract must be owned by #{issue}")


def _validate_split_registry(schema: dict, approval_root: Path, errors: list[str]) -> None:
    parent = _load_parent_validator()
    rows = {row.get("issue"): row for row in schema.get("wave0_split_registry", [])}
    if set(rows) != set(EXPECTED_SPLIT_DEPENDENCIES):
        errors.append("split registry must list exactly #65-#69")
    for issue, expected_dependencies in EXPECTED_SPLIT_DEPENDENCIES.items():
        row = rows.get(issue, {})
        if row.get("depends_on") != expected_dependencies:
            errors.append(f"#{issue} split dependencies must be {expected_dependencies}")
        if row.get("status_snapshot") not in ALLOWED_SPLIT_STATUS_SNAPSHOTS:
            errors.append(f"#{issue} split status_snapshot must use the canonical status vocabulary")
        expected_plan_path = EXPECTED_SPLIT_PLAN_PATHS[issue]
        if _repo_path(Path(expected_plan_path)).exists():
            if row.get("plan_path") != expected_plan_path:
                errors.append(f"#{issue} split plan_path must be {expected_plan_path}")
        else:
            if row.get("plan_path") != "":
                errors.append(f"#{issue} split plan_path must be empty until expected plan exists")
            if row.get("status_snapshot") != "status:plan-required":
                errors.append(f"#{issue} split status_snapshot must be status:plan-required until expected plan exists")
            if row.get("implementation_ready"):
                errors.append(f"#{issue} split implementation_ready must be false until expected plan exists")
            continue
        status_sources = _split_status_sources(issue, expected_plan_path, approval_root, parent)
        expected_status = status_sources[0][1] if status_sources else None
        if expected_status and row.get("status_snapshot") != expected_status:
            errors.append(f"#{issue} split status_snapshot must match repo-local status {expected_status}")
        _validate_lower_precedence_split_statuses(issue, status_sources, errors)
        if not row.get("implementation_ready"):
            continue
        if "status:plan-approved" not in row.get("status_snapshot", ""):
            errors.append(f"#{issue} implementation_ready requires status:plan-approved")
            continue
        plan_path = row.get("plan_path", "")
        marker_path = approval_root / f"{issue}.md"
        marker_errors = parent.validate_approval_marker(marker_path, issue, plan_path)
        if marker_errors:
            errors.append(f"#{issue} implementation_ready requires valid approval marker")
            errors.extend(marker_errors)


def _split_status_sources(issue: int, plan_path: str, approval_root: Path, parent) -> list[tuple[str, str]]:
    sources: list[tuple[str, str]] = []
    marker_path = approval_root / f"{issue}.md"
    if marker_path.exists() and not parent.validate_approval_marker(marker_path, issue, plan_path):
        sources.append(("approval marker", "status:plan-approved"))
    for name, status in [
        ("coordination", _coordination_split_status(issue)),
        ("plan file", _plan_file_status(plan_path)),
        ("README", _readme_plan_status(issue)),
    ]:
        if status:
            sources.append((name, status))
    return sources


def _validate_lower_precedence_split_statuses(
    issue: int,
    sources: list[tuple[str, str]],
    errors: list[str],
) -> None:
    if not sources:
        return
    expected_status = sources[0][1]
    for source_name, status in sources[1:]:
        if not _compatible_split_status(expected_status, status):
            errors.append(
                f"#{issue} split status_snapshot lower-precedence {source_name} "
                f"contradicts {expected_status}"
            )


def _compatible_split_status(expected_status: str, lower_status: str) -> bool:
    if expected_status == lower_status:
        return True
    return expected_status == "status:blocked-draft" and lower_status == "status:draft"


def _coordination_split_status(issue: int) -> str | None:
    text = _repo_path(COORDINATION_PATH).read_text()
    for line in text.splitlines():
        if f"[#{issue}]" not in line or not line.lstrip().startswith("|"):
            continue
        cells = _markdown_cells(line)
        if len(cells) >= 4 and _markdown_issue_cell_matches(cells[0], issue):
            return _normalize_split_status(cells[3])
    return None


def _plan_file_status(plan_path: str) -> str | None:
    path = _repo_path(Path(plan_path))
    if not path.exists():
        return None
    text = path.read_text()
    blocked_match = re.search(r"(?i)\bOverall result:\s*[*_\s]*BLOCKED-DRAFT\b", text)
    if blocked_match:
        return "status:blocked-draft"
    header_match = re.search(r"(?im)^>\s+\*\*Status:\*\*\s*(.+)$", text)
    return _normalize_split_status(header_match.group(1)) if header_match else None


def _readme_plan_status(issue: int) -> str | None:
    text = _repo_path(Path("docs/plans/README.md")).read_text()
    for line in text.splitlines():
        if f"[#{issue}]" not in line or not line.lstrip().startswith("|"):
            continue
        cells = _markdown_cells(line)
        if len(cells) >= 5 and _markdown_issue_cell_matches(cells[0], issue):
            return _normalize_split_status(cells[4])
    return None


def _markdown_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _markdown_issue_cell_matches(cell: str, issue: int) -> bool:
    match = re.fullmatch(r"(?:#(\d+)|\[#(\d+)\]\([^)]+\))", cell.strip())
    return bool(match and int(match.group(1) or match.group(2)) == issue)


def _normalize_split_status(text: str | None) -> str | None:
    lowered = (text or "").strip().lower()
    for token in ["plan-approved", "plan-review", "blocked-draft", "plan-required", "draft"]:
        if token in lowered:
            return f"status:{token}"
    return None


def _validate_canonical_wave_registry(schema: dict, errors: list[str]) -> None:
    rows = {row.get("issue"): row for row in schema.get("canonical_wave_registry", [])}
    if set(rows) != set(range(51, 64)):
        errors.append("canonical wave registry must cover #51-#63 exactly")
    for issue, row in rows.items():
        is_ingestion = 52 <= issue <= 60
        expected_num = "successful_routed_items" if is_ingestion else "measured_success_numerator"
        expected_den = "eligible_candidate_items" if is_ingestion else "measured_success_denominator"
        if row.get("success_numerator_field") != expected_num:
            errors.append(f"#{issue} success numerator field must be {expected_num}")
        if row.get("success_denominator_field") != expected_den:
            errors.append(f"#{issue} success denominator field must be {expected_den}")


def _collect_keys(value) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key))
            keys.update(_collect_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(_collect_keys(nested))
    return keys


def _walk_items(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield str(key), nested
            yield from _walk_items(nested)
    elif isinstance(value, list):
        for nested in value:
            yield "", nested
            yield from _walk_items(nested)


def _repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--schema",
        default=str(SCHEMA_PATH),
        help="schema JSON path",
    )
    args = parser.parse_args(argv)
    errors = validate_schema_file(Path(args.schema))
    if errors:
        for error in errors:
            print(f"DENY  {error}", file=sys.stderr)
        print(f"\nFAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: ACE wave 0 schema contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
