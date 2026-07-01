"""Contract and bounded-read helpers for ACE issue 62."""
from __future__ import annotations

import importlib.util
import json
import re
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = Path("config/ace-manifest-evidence-contract.json")
WAVE0_SCHEMA_PATH = Path("artifacts/ace-wave0-ledger-schema.json")
PARENT_VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_epic_wave_coordination.py"
PLAN_PATH = Path("docs/plans/2026-06-29-issue-62-ace-manifest-freshness-and-drift-sentinel.md")
CASE_STUDY_PATH = Path("docs/case-studies/ace-manifest-freshness-drift-sentinel.md")
LIFECYCLE_PATH = Path("docs/16-corpus-lifecycle.md")
WORKFLOW_PATH = Path(".github/workflows/validate.yml")
APPROVAL_MARKER_PATH = Path(".planning/plan-approved/62.md")
VALIDATOR_REF = "scripts/validate_ace_manifest_freshness.py"

SNAPSHOT_ID_RE = re.compile(r"^ams_[0-9a-f]{32}$")
SEMVER_1_RE = re.compile(r"^1\.0\.\d+$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
RECORD_ID_RE = re.compile(r"^ace62-[a-z0-9.-]+$")

EXPECTED_MANIFEST_KEYS = [
    "INDEX.md",
    "assets.json",
    "docs/master-index.jsonl",
    "_cad-index/index-summary.json",
    "_cad-index/cad-readability-index.tsv",
    ".ace-knowledge/index.db",
]
EXPECTED_MANIFEST_ROLES = {
    "INDEX.md": "root_inventory_index",
    "assets.json": "asset_manifest",
    "docs/master-index.jsonl": "master_record_index",
    "_cad-index/index-summary.json": "cad_summary_index",
    "_cad-index/cad-readability-index.tsv": "cad_readability_index",
    ".ace-knowledge/index.db": "knowledge_store_index",
}
EXPECTED_PAIR_SOURCES = {
    "inventory_to_assets_presence": ("INDEX.md", "assets.json"),
    "assets_to_master_records": ("assets.json", "docs/master-index.jsonl"),
    "master_records_to_cad_summary": ("docs/master-index.jsonl", "_cad-index/index-summary.json"),
    "cad_summary_to_cad_readability": (
        "_cad-index/index-summary.json",
        "_cad-index/cad-readability-index.tsv",
    ),
    "master_records_to_knowledge_store": ("docs/master-index.jsonl", ".ace-knowledge/index.db"),
}
EXPECTED_PAIR_IDS = set(EXPECTED_PAIR_SOURCES)
EXPECTED_ENUMS = {
    "content_fingerprint_status": {"available_sidecar", "available_under_cap", "unavailable", "not_present"},
    "row_count_status": {"available_sidecar", "available_under_cap", "unavailable", "not_present"},
    "drift_severity": {"compatible", "warning", "blocker", "unavailable"},
    "evidence_mode": {"public_safe_summary", "private_sidecar_validated", "missing_manifest", "blocked_unavailable"},
    "authorization_status": {"sampling_allowed", "blocked_requires_reconciliation", "blocked_unavailable"},
}
LEGAL_PAIR_MODES = {
    "compatible": {"public_safe_summary", "private_sidecar_validated"},
    "warning": {"public_safe_summary", "private_sidecar_validated"},
    "blocker": {"public_safe_summary", "private_sidecar_validated"},
    "unavailable": {"missing_manifest", "blocked_unavailable"},
}
ALLOWED_VALIDATOR_ENV = {"UV_CACHE_DIR": ".claude/state/uv-cache"}
MANIFEST_HINTS = tuple(["ACE_" + "SHARE_ROOT", *EXPECTED_MANIFEST_KEYS])
DENIED_COMMAND_TOKENS = ("find", "du", "rg", "fd", "jq", "cat", "wc", "sha256sum")


def load_contract(path: Path = CONTRACT_PATH) -> dict:
    return json.loads(repo_path(path).read_text())


def validate_contract_file(path: Path = CONTRACT_PATH) -> list[str]:
    try:
        contract = load_contract(path)
    except FileNotFoundError:
        return [f"missing contract file: {path}"]
    except json.JSONDecodeError as exc:
        return [f"contract JSON is invalid: {exc}"]
    errors = validate_contract(contract)
    errors.extend(validate_wave0_schema_dependency(contract, WAVE0_SCHEMA_PATH))
    return errors


def validate_contract(contract: dict) -> list[str]:
    errors: list[str] = []
    _validate_metadata(contract, errors)
    _validate_manifest_sources(contract, errors)
    _validate_status_enums(contract, errors)
    _validate_drift_pairs(contract, errors)
    _validate_bounded_caps(contract, errors)
    return errors


def validate_wave0_schema_dependency(contract: dict, schema_path: Path = WAVE0_SCHEMA_PATH) -> list[str]:
    if contract.get("depends_on_schema_issue") != 65:
        return ["contract must depend on issue 65 schema"]
    try:
        schema = json.loads(repo_path(schema_path).read_text())
    except FileNotFoundError:
        return [f"missing #65 schema file: {schema_path}"]
    return _validate_wave0_rows(schema.get("canonical_wave_registry", []))


def is_snapshot_id(value: str) -> bool:
    return bool(SNAPSHOT_ID_RE.fullmatch(str(value)))


def validate_operation_is_bounded(command: str | list[str]) -> list[str]:
    text = command if isinstance(command, str) else " ".join(command)
    lower = text.lower()
    if not any(hint.lower() in lower for hint in MANIFEST_HINTS):
        return []
    if _contains_denied_operation(lower):
        return [f"unbounded manifest operation is not allowed: {text}"]
    return []


def public_scan_paths() -> list[Path]:
    paths = [
        PLAN_PATH,
        Path("docs/plans/README.md"),
        Path("docs/plans/ace-share-ingestion-wave-coordination.md"),
        APPROVAL_MARKER_PATH,
        CONTRACT_PATH,
        Path("scripts/validate_ace_manifest_freshness.py"),
        Path("scripts/ace_manifest_freshness_contract.py"),
        Path("scripts/ace_manifest_freshness_emit.py"),
        Path("scripts/ace_manifest_freshness_operational.py"),
        Path("tests/test_validate_ace_manifest_freshness.py"),
        Path("tests/test_validate_ace_manifest_freshness_runtime.py"),
        Path("tests/test_validate_ace_manifest_freshness_security.py"),
        Path("tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json"),
        CASE_STUDY_PATH,
        LIFECYCLE_PATH,
        WORKFLOW_PATH,
    ]
    paths.extend(_plan_review_artifacts())
    return paths


def validate_public_surfaces(paths: list[Path] | None = None) -> list[str]:
    parent = _load_parent_validator()
    scan_paths = paths or public_scan_paths()
    return parent.validate_public_artifact_paths([repo_path(path) for path in scan_paths])


def collect_manifest_status(
    manifest_key: str,
    manifest_path: Path,
    *,
    caps: dict | None = None,
    snapshot_id: str | None = None,
    captured_at_utc: str | None = None,
    sidecar: dict | None = None,
) -> dict:
    if manifest_key not in EXPECTED_MANIFEST_KEYS:
        raise ValueError(f"unknown manifest source key: {manifest_key}")
    base = _public_evidence_base(manifest_key, snapshot_id or _new_snapshot_id(), captured_at_utc or _utc_now())
    path = Path(manifest_path)
    if not path.exists():
        return {**base, **_status_fields("not_present", "not_present", "missing_manifest")}
    if sidecar:
        return {**base, **_sidecar_status(sidecar)}
    if _is_under_cap(path, _normalise_caps(caps)):
        return {
            **base,
            **_status_fields("available_under_cap", "available_under_cap", "public_safe_summary"),
            "_bounded_count": _bounded_count(path),
        }
    return {**base, **_status_fields("unavailable", "unavailable", "blocked_unavailable")}


def repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def _validate_wave0_rows(rows: list[dict]) -> list[str]:
    errors: list[str] = []
    by_issue = {row.get("issue"): row for row in rows}
    if set(by_issue) != set(range(51, 64)):
        errors.append("#65 canonical wave registry must cover #51-#63 exactly")
    for issue in range(52, 61):
        if by_issue.get(issue, {}).get("requires_manifest_snapshot_id") is not True:
            errors.append(f"#{issue} must require manifest snapshot IDs in #65 schema")
    if by_issue.get(62, {}).get("requires_manifest_snapshot_id") is not False:
        errors.append("#62 must not be classified as a sampling wave in #65 schema")
    return errors


def _validate_metadata(contract: dict, errors: list[str]) -> None:
    expected = {
        "contract_id": "ace-manifest-evidence-contract",
        "owner_issue": 62,
        "depends_on_schema_issue": 65,
        "downstream_consumer_issue": 70,
        "blocked_operational_issue": 67,
        "source_root_env_var": "ACE_SHARE_ROOT",
    }
    for key, value in expected.items():
        if contract.get(key) != value:
            errors.append(f"contract metadata must set {key} to {value!r}")
    if not SEMVER_1_RE.fullmatch(str(contract.get("contract_version", ""))):
        errors.append("contract_version must use 1.0.x semver")


def _validate_manifest_sources(contract: dict, errors: list[str]) -> None:
    if contract.get("manifest_source_keys") != EXPECTED_MANIFEST_KEYS:
        errors.append("manifest source keys must match the closed #62 six-key enum")
    if contract.get("manifest_source_roles") != EXPECTED_MANIFEST_ROLES:
        errors.append("manifest source roles must match the closed #62 role map")


def _validate_status_enums(contract: dict, errors: list[str]) -> None:
    for name, expected_values in EXPECTED_ENUMS.items():
        if set(contract.get("status_enums", {}).get(name, [])) != expected_values:
            errors.append(f"{name} enum must match the closed #62 vocabulary")


def _validate_drift_pairs(contract: dict, errors: list[str]) -> None:
    pairs = contract.get("drift_eligible_pairs", [])
    if {pair.get("pair_id") for pair in pairs if isinstance(pair, dict)} != EXPECTED_PAIR_IDS:
        errors.append("drift eligible pairs must match the closed #62 pair set")
    for pair in pairs:
        pair_id = pair.get("pair_id")
        expected_sources = EXPECTED_PAIR_SOURCES.get(pair_id)
        if expected_sources != (pair.get("left_source"), pair.get("right_source")):
            errors.append(f"drift pair {pair_id} must use the configured source pair")


def _validate_bounded_caps(contract: dict, errors: list[str]) -> None:
    caps = contract.get("bounded_caps", {})
    for key in ["max_header_bytes", "max_under_cap_bytes", "max_under_cap_rows"]:
        if not isinstance(caps.get(key), int) or caps[key] <= 0:
            errors.append(f"bounded cap must be a positive integer: {key}")


def _contains_denied_operation(lower: str) -> bool:
    if "ls -r" in lower or "grep -r" in lower or "grep --recursive" in lower:
        return True
    if ("os." + "walk(") in lower or ("." + "rglob(") in lower:
        return True
    return any(re.search(rf"\b{re.escape(token)}\b", lower) for token in DENIED_COMMAND_TOKENS)


def _plan_review_artifacts() -> list[Path]:
    review_root = REPO_ROOT / "scripts" / "review" / "results"
    if not review_root.exists():
        return []
    artifacts = list(review_root.glob("*plan-62*.md"))
    artifacts.extend(review_root.glob("*implementation-62*.md"))
    return [artifact.relative_to(REPO_ROOT) for artifact in sorted(artifacts) if artifact.is_file()]


def _load_parent_validator():
    spec = importlib.util.spec_from_file_location("validate_ace_epic_wave_coordination_for_62", PARENT_VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _normalise_caps(caps: dict | None) -> dict:
    default = load_contract().get("bounded_caps", {})
    merged = {**default, **(caps or {})}
    return {
        "max_under_cap_bytes": int(merged["max_under_cap_bytes"]),
        "max_under_cap_rows": int(merged["max_under_cap_rows"]),
    }


def _public_evidence_base(manifest_key: str, snapshot_id: str, captured_at_utc: str) -> dict:
    return {
        "snapshot_id": snapshot_id,
        "manifest_source_key": manifest_key,
        "source_root_env_var": "ACE_SHARE_ROOT",
        "captured_at_utc": captured_at_utc,
        "schema_marker_status": "unknown",
        "generated_timestamp_status": "unknown",
        "drift_severity": "unavailable",
        "validator_version": "1.0.0",
    }


def _status_fields(content_status: str, row_status: str, mode: str) -> dict:
    return {"content_fingerprint_status": content_status, "row_count_status": row_status, "evidence_mode": mode}


def _sidecar_status(sidecar: dict) -> dict:
    content = sidecar.get("content_fingerprint_status", "available_sidecar")
    rows = sidecar.get("row_count_status", "available_sidecar")
    status = _status_fields(content, rows, "private_sidecar_validated")
    if isinstance(sidecar.get("comparable_count"), int):
        status["_bounded_count"] = sidecar["comparable_count"]
    return status


def _is_under_cap(path: Path, caps: dict) -> bool:
    if path.stat().st_size > caps["max_under_cap_bytes"]:
        return False
    return len(path.read_text(errors="replace").splitlines()) <= caps["max_under_cap_rows"]


def _bounded_count(path: Path) -> int:
    text = path.read_text(errors="replace")
    if path.suffix == ".json":
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return _nonempty_line_count(text)
        if isinstance(parsed, list):
            return len(parsed)
        if isinstance(parsed, dict):
            return len(parsed)
    return _nonempty_line_count(text)


def _nonempty_line_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def _new_snapshot_id() -> str:
    return "ams_" + secrets.token_hex(16)


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
