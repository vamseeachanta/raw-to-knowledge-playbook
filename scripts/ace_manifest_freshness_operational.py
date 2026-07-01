"""Operational evidence validation for ACE issue 62."""
from __future__ import annotations

import json
import re
from pathlib import Path

from ace_manifest_freshness_contract import (
    ALLOWED_VALIDATOR_ENV,
    COMMIT_RE,
    EXPECTED_ENUMS,
    EXPECTED_MANIFEST_KEYS,
    EXPECTED_PAIR_IDS,
    EXPECTED_PAIR_SOURCES,
    LEGAL_PAIR_MODES,
    REPO_ROOT,
    RECORD_ID_RE,
    SEMVER_1_RE,
    UTC_RE,
    VALIDATOR_REF,
    is_snapshot_id,
    repo_path,
)


OPERATIONAL_FIELDS = {
    "record_schema_version",
    "record_id",
    "source_issue",
    "evidence_artifact_ref",
    "validator_ref",
    "validator_env",
    "validator_command",
    "validator_exit_status",
    "recorded_at_utc",
    "reviewed_commit",
    "authorization_status",
    "snapshot_ids_by_manifest_source",
    "source_status_by_manifest_source",
    "drift_verdicts_by_manifest_source_pair",
    "reconciliation_refs",
}
REQUEST_POINTER_FIELDS = {"source_issue", "record_id", "evidence_artifact_ref"}
SOURCE_STATUS_FIELDS = {"content_fingerprint_status", "row_count_status", "evidence_mode", "captured_at_utc"}
PAIR_VERDICT_FIELDS = {
    "left_source",
    "right_source",
    "left_snapshot_id",
    "right_snapshot_id",
    "drift_severity",
    "evidence_mode",
    "reconciliation_required",
}
GITHUB_ISSUE_REF_RE = re.compile(
    r"^https://github\.com/vamseeachanta/raw-to-knowledge-playbook/issues/[0-9]+(?:#issuecomment-[0-9]+)?$"
)


def validate_operational_evidence_file(path: Path) -> list[str]:
    artifact = _safe_artifact_path(str(path))
    if artifact is None:
        return [f"operational evidence path is outside allowed roots or missing: {path}"]
    try:
        record = json.loads(artifact.read_text())
    except FileNotFoundError:
        return [f"missing operational evidence file: {path}"]
    except json.JSONDecodeError as exc:
        return [f"operational evidence JSON is invalid: {exc}"]
    return validate_operational_evidence(record)


def validate_request_pointer(pointer: dict) -> list[str]:
    errors: list[str] = []
    if set(pointer) != REQUEST_POINTER_FIELDS:
        errors.append("request freshness evidence must be a minimal pointer")
    if pointer.get("source_issue") != 62:
        errors.append("request pointer source_issue must be 62")
    ref = str(pointer.get("evidence_artifact_ref", ""))
    if not _valid_artifact_ref(ref):
        errors.append("request pointer evidence_artifact_ref is invalid")
        return errors
    errors.extend(_validate_pointer_artifact(pointer, ref))
    return errors


def validate_operational_evidence(record: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["operational evidence must be a JSON object"]
    _validate_operational_shape(record, errors)
    _validate_operational_metadata(record, errors)
    snapshots = record.get("snapshot_ids_by_manifest_source", {})
    statuses = record.get("source_status_by_manifest_source", {})
    verdicts = record.get("drift_verdicts_by_manifest_source_pair", {})
    _validate_snapshot_map(snapshots, errors)
    _validate_source_statuses(statuses, errors)
    if not isinstance(verdicts, dict):
        errors.append("drift verdicts must use the exact closed pair IDs")
    if isinstance(statuses, dict) and not all(isinstance(value, dict) for value in statuses.values()):
        return errors
    if not all(isinstance(value, dict) for value in [snapshots, statuses, verdicts]):
        return errors
    _validate_pair_verdicts(verdicts, snapshots, statuses, record, errors)
    _validate_authorization(record, verdicts, errors)
    return errors


def _validate_pointer_artifact(pointer: dict, ref: str) -> list[str]:
    artifact = _safe_artifact_path(ref)
    if artifact is None:
        return [f"referenced artifact is outside allowed roots: {ref}"]
    try:
        record = json.loads(artifact.read_text())
    except FileNotFoundError:
        return [f"referenced artifact is missing: {ref}"]
    errors = validate_operational_evidence(record)
    if errors:
        return errors
    if record.get("source_issue") != pointer.get("source_issue"):
        errors.append("referenced artifact source_issue does not match request pointer")
    if record.get("record_id") != pointer.get("record_id"):
        errors.append("referenced artifact record_id does not match request pointer")
    if record.get("evidence_artifact_ref") != ref:
        errors.append("referenced artifact evidence_artifact_ref does not match request pointer")
    return errors


def _validate_operational_shape(record: dict, errors: list[str]) -> None:
    if set(record) != OPERATIONAL_FIELDS:
        errors.append("operational evidence must be a closed root object for #70")
    for key in OPERATIONAL_FIELDS:
        if key not in record:
            errors.append(f"operational evidence missing required field: {key}")


def _validate_operational_metadata(record: dict, errors: list[str]) -> None:
    if not SEMVER_1_RE.fullmatch(str(record.get("record_schema_version", ""))):
        errors.append("record_schema_version must use 1.0.x semver")
    if not RECORD_ID_RE.fullmatch(str(record.get("record_id", ""))):
        errors.append("record_id must start with ace62- and use safe characters")
    if record.get("source_issue") != 62:
        errors.append("source_issue must be 62")
    if not _valid_artifact_ref(str(record.get("evidence_artifact_ref", ""))):
        errors.append("evidence_artifact_ref must be a repo-relative #62 JSON artifact ref")
    _validate_validator_execution(record, errors)
    if not UTC_RE.fullmatch(str(record.get("recorded_at_utc", ""))):
        errors.append("recorded_at_utc must be a UTC timestamp ending in Z")
    if not COMMIT_RE.fullmatch(str(record.get("reviewed_commit", ""))):
        errors.append("reviewed_commit must be a 40-character lowercase SHA")


def _validate_validator_execution(record: dict, errors: list[str]) -> None:
    if record.get("validator_ref") != VALIDATOR_REF:
        errors.append(f"validator_ref must be {VALIDATOR_REF}")
    if record.get("validator_env") != ALLOWED_VALIDATOR_ENV:
        errors.append("validator_env must be the closed UV_CACHE_DIR object")
    command = record.get("validator_command", [])
    if not isinstance(command, list) or not all(isinstance(token, str) for token in command):
        errors.append("validator_command must be argv-style string tokens")
        return
    if any("UV_CACHE_DIR" in token or "=" in token for token in command):
        errors.append("validator_env values must not be embedded in validator_command argv")
    ref = str(record.get("evidence_artifact_ref", ""))
    allowed = [["uv", "run", "python", VALIDATOR_REF, "--evidence", ref]]
    if command not in allowed:
        errors.append("validator_command must exactly invoke the #62 validator evidence command")
    if record.get("validator_exit_status") != 0:
        errors.append("validator_exit_status must be exactly 0")


def _valid_artifact_ref(value: str) -> bool:
    path = Path(value)
    allowed_roots = (Path("artifacts/ace-manifest-freshness"), Path("tests/fixtures/ace-manifest-freshness"))
    if path.is_absolute() or ".." in path.parts or path.suffix != ".json":
        return False
    return any(path == root or root in path.parents for root in allowed_roots)


def _safe_artifact_path(value: str) -> Path | None:
    if not _valid_artifact_ref(value):
        return None
    candidate = repo_path(Path(value))
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError:
        return None
    allowed_roots = [root.resolve() for root in _allowed_artifact_roots()]
    return resolved if any(_is_relative_to(resolved, root) for root in allowed_roots) else None


def safe_output_artifact_path(value: str) -> Path | None:
    if not _valid_artifact_ref(value):
        return None
    candidate = repo_path(Path(value))
    allowed_root = _matching_allowed_root(candidate)
    if allowed_root is None:
        return None
    try:
        parent = candidate.parent.resolve(strict=True)
    except FileNotFoundError:
        if candidate.parent != allowed_root:
            return None
        parent = allowed_root.parent.resolve(strict=True) / allowed_root.name
    else:
        if not _is_relative_to(parent, allowed_root.resolve()):
            return None
    if candidate.is_symlink():
        return None
    if candidate.exists():
        try:
            resolved = candidate.resolve(strict=True)
        except FileNotFoundError:
            return None
        if not any(_is_relative_to(resolved, root.resolve()) for root in _allowed_artifact_roots()):
            return None
    return candidate


def _matching_allowed_root(candidate: Path) -> Path | None:
    for root in _allowed_artifact_roots():
        if candidate == root or root in candidate.parents:
            return root
    return None


def _allowed_artifact_roots() -> list[Path]:
    return [
        REPO_ROOT / "artifacts" / "ace-manifest-freshness",
        REPO_ROOT / "tests" / "fixtures" / "ace-manifest-freshness",
    ]


def _validate_snapshot_map(snapshots: object, errors: list[str]) -> None:
    if not isinstance(snapshots, dict) or list(snapshots) != EXPECTED_MANIFEST_KEYS:
        errors.append("snapshot_ids_by_manifest_source must use the exact six manifest keys")
        return
    for key, snapshot_id in snapshots.items():
        if not is_snapshot_id(snapshot_id):
            errors.append(f"snapshot ID for {key} must be opaque ams_ plus 32 lowercase hex characters")


def _validate_source_statuses(statuses: object, errors: list[str]) -> None:
    if not isinstance(statuses, dict) or set(statuses) != set(EXPECTED_MANIFEST_KEYS):
        errors.append("source_status_by_manifest_source must use the exact six manifest keys")
        return
    for key, status in statuses.items():
        if not isinstance(status, dict):
            errors.append(f"source status for {key} must be a closed object")
            continue
        if set(status) != SOURCE_STATUS_FIELDS:
            errors.append(f"source status for {key} must be a closed object")
            continue
        _validate_source_status_values(key, status, errors)


def _validate_source_status_values(key: str, status: dict, errors: list[str]) -> None:
    for field in ["content_fingerprint_status", "row_count_status"]:
        if status.get(field) not in EXPECTED_ENUMS[field]:
            errors.append(f"source status for {key} has invalid {field}")
    if status.get("evidence_mode") not in EXPECTED_ENUMS["evidence_mode"]:
        errors.append(f"source status for {key} has invalid evidence_mode")
    if not UTC_RE.fullmatch(str(status.get("captured_at_utc", ""))):
        errors.append(f"source status for {key} must include UTC captured_at_utc")


def _validate_pair_verdicts(verdicts: object, snapshots: dict, statuses: dict, record: dict, errors: list[str]) -> None:
    if not isinstance(verdicts, dict) or set(verdicts) != EXPECTED_PAIR_IDS:
        errors.append("drift verdicts must use the exact closed pair IDs")
        return
    noncompatible: set[str] = set()
    for pair_id, verdict in verdicts.items():
        if not isinstance(verdict, dict):
            errors.append(f"pair verdict for {pair_id} must be a closed object")
            continue
        if set(verdict) != PAIR_VERDICT_FIELDS:
            errors.append(f"pair verdict for {pair_id} must be a closed object")
            continue
        _validate_pair_source_and_snapshot(pair_id, verdict, snapshots, errors)
        _validate_pair_severity_mode(pair_id, verdict, errors)
        if verdict.get("drift_severity") in {"warning", "blocker"}:
            noncompatible.add(pair_id)
        _validate_compatible_pair_support(pair_id, verdict, statuses, errors)
    _validate_reconciliation_refs(noncompatible, record, errors)


def _validate_pair_source_and_snapshot(pair_id: str, verdict: dict, snapshots: dict, errors: list[str]) -> None:
    left, right = EXPECTED_PAIR_SOURCES[pair_id]
    if verdict.get("left_source") != left or verdict.get("right_source") != right:
        errors.append(f"pair verdict for {pair_id} must use the configured source pair")
    if verdict.get("left_snapshot_id") != snapshots.get(left):
        errors.append(f"left snapshot for {pair_id} must match snapshot_ids_by_manifest_source")
    if verdict.get("right_snapshot_id") != snapshots.get(right):
        errors.append(f"right snapshot for {pair_id} must match snapshot_ids_by_manifest_source")


def _validate_pair_severity_mode(pair_id: str, verdict: dict, errors: list[str]) -> None:
    severity = verdict.get("drift_severity")
    mode = verdict.get("evidence_mode")
    if severity not in EXPECTED_ENUMS["drift_severity"]:
        errors.append(f"pair verdict for {pair_id} has invalid drift_severity")
        return
    if mode not in LEGAL_PAIR_MODES[severity]:
        errors.append(f"pair verdict for {pair_id} uses illegal severity/evidence_mode combination")
    expected_reconciliation = severity in {"warning", "blocker"}
    if verdict.get("reconciliation_required") is not expected_reconciliation:
        errors.append(f"pair verdict for {pair_id} has inconsistent reconciliation_required")


def _validate_compatible_pair_support(pair_id: str, verdict: dict, statuses: dict, errors: list[str]) -> None:
    if verdict.get("drift_severity") != "compatible":
        return
    supported = {"available_sidecar", "available_under_cap"}
    left = statuses.get(verdict.get("left_source"), {})
    right = statuses.get(verdict.get("right_source"), {})
    required = [left.get("content_fingerprint_status"), left.get("row_count_status")]
    required.extend([right.get("content_fingerprint_status"), right.get("row_count_status")])
    if not all(value in supported for value in required):
        errors.append(f"compatible pair {pair_id} requires sidecar or under-cap evidence")


def _validate_reconciliation_refs(noncompatible: set[str], record: dict, errors: list[str]) -> None:
    refs = record.get("reconciliation_refs", {})
    if not isinstance(refs, dict):
        errors.append("reconciliation_refs must be an object")
        return
    if set(refs) - noncompatible:
        errors.append("reconciliation_refs may only name warning or blocker pair IDs")
    for pair_id in noncompatible:
        values = refs.get(pair_id)
        if not isinstance(values, list) or not values:
            errors.append(f"reconciliation_refs must name non-empty refs for {pair_id}")
            continue
        for value in values:
            if not _valid_reconciliation_ref(value):
                errors.append(f"reconciliation_refs contains invalid ref for {pair_id}")


def _validate_authorization(record: dict, verdicts: object, errors: list[str]) -> None:
    if not isinstance(verdicts, dict):
        return
    severities = {verdict.get("drift_severity") for verdict in verdicts.values() if isinstance(verdict, dict)}
    expected = "sampling_allowed"
    if "unavailable" in severities:
        expected = "blocked_unavailable"
    elif severities & {"warning", "blocker"}:
        expected = "blocked_requires_reconciliation"
    if record.get("authorization_status") != expected:
        errors.append(f"authorization_status must be {expected} for the drift verdict set")


def _valid_reconciliation_ref(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if GITHUB_ISSUE_REF_RE.fullmatch(value):
        return True
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return False
    if not path.parts or path.parts[0] not in {"artifacts", "docs", "scripts", "tests", ".planning"}:
        return False
    try:
        resolved = repo_path(path).resolve(strict=True)
    except FileNotFoundError:
        return False
    return _is_relative_to(resolved, REPO_ROOT)


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True
