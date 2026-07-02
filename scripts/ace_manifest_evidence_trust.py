"""Trusted #62 evidence registry checks for ACE issue 70."""
from __future__ import annotations
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ace_manifest_freshness_operational import (  # noqa: E402
    GITHUB_ISSUE_REF_RE,
    REQUEST_POINTER_FIELDS,
    _safe_artifact_path,
    validate_operational_evidence,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
TRUSTED_REGISTRY_PATH = Path("artifacts/ace-manifest-freshness/trusted-evidence-registry.json")
PLAN_70_PATH = Path("docs/plans/2026-07-01-issue-70-ace-67-62-manifest-evidence-contract-integration.md")
APPROVAL_70_PATH = Path(".planning/plan-approved/70.md")
CASE_STUDY_PATH = Path("docs/case-studies/ace-manifest-freshness-drift-sentinel.md")
WORKFLOW_PATH = Path(".github/workflows/validate.yml")
TRUST_SCRIPT_PATH = Path("scripts/ace_manifest_evidence_trust.py")
TRUST_TEST_PATH = Path("tests/test_validate_ace_manifest_evidence_integration.py")
REGISTRY_FIELDS = {
    "registry_schema_version",
    "owner_issue",
    "consumer_issue",
    "evidence_source_issue",
    "trusted_evidence",
}
ROW_FIELDS = {
    "record_id",
    "evidence_artifact_ref",
    "artifact_integrity_digest",
    "reviewed_commit",
    "validator_ref",
    "validator_command",
    "validator_exit_status",
    "issue_evidence_comment_url",
}


@dataclass
class TrustedEvidenceResult:
    authorized: bool = False
    reason_code: str = ""
    errors: list[str] = field(default_factory=list)
    record: dict | None = None


def repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def validate_trusted_62_evidence_pointer(
    pointer: object,
    registry_path: Path = TRUSTED_REGISTRY_PATH,
) -> TrustedEvidenceResult:
    minimal_error = _validate_minimal_pointer(pointer)
    if minimal_error:
        return TrustedEvidenceResult(False, "SELF_ATTESTED_62_EVIDENCE", minimal_error)
    ref = str(pointer["evidence_artifact_ref"])
    if _is_fixture_ref(ref):
        return TrustedEvidenceResult(False, "FIXTURE_62_EVIDENCE_NOT_OPERATIONAL", ["fixture evidence is not operational"])
    if _path_has_symlink(repo_path(Path(ref))):
        return TrustedEvidenceResult(False, "INVALID_62_EVIDENCE_POINTER", [f"referenced artifact path must not contain symlinks: {ref}"])
    artifact = _safe_artifact_path(ref)
    if artifact is None:
        return TrustedEvidenceResult(False, "INVALID_62_EVIDENCE_POINTER", [f"referenced artifact is outside allowed roots: {ref}"])
    raw, record, errors = _read_record_once(artifact)
    if errors:
        return TrustedEvidenceResult(False, "INVALID_62_EVIDENCE_POINTER", errors)
    errors = _validate_record_matches_pointer(record, pointer, ref)
    if errors:
        return TrustedEvidenceResult(False, "INVALID_62_EVIDENCE_POINTER", errors, record)
    registry_errors, rows = _load_registry(registry_path)
    row_errors = _find_registry_match(rows, record, raw)
    if registry_errors or row_errors:
        return TrustedEvidenceResult(False, "UNTRUSTED_62_EVIDENCE", registry_errors + row_errors, record)
    if record.get("authorization_status") != "sampling_allowed":
        return TrustedEvidenceResult(False, "62_EVIDENCE_NOT_AUTHORIZING", ["authorization_status is not sampling_allowed"], record)
    return TrustedEvidenceResult(True, "AUTHORIZED_62_EVIDENCE", [], record)


def issue_70_public_scan_paths() -> list[Path]:
    paths = [
        PLAN_70_PATH,
        Path("docs/plans/README.md"),
        APPROVAL_70_PATH,
        Path("config/ace-manifest-evidence-contract.json"),
        Path("config/ace-bounded-sampling-firewall-contract.json"),
        TRUSTED_REGISTRY_PATH,
        TRUST_SCRIPT_PATH,
        TRUST_TEST_PATH,
        CASE_STUDY_PATH,
        WORKFLOW_PATH,
        Path("tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json"),
    ]
    paths.extend(_review_artifact_paths())
    return paths


def _validate_minimal_pointer(pointer: object) -> list[str]:
    if not isinstance(pointer, dict):
        return ["request freshness evidence must be a minimal pointer"]
    errors: list[str] = []
    if set(pointer) != REQUEST_POINTER_FIELDS:
        errors.append("request freshness evidence must be a minimal pointer")
    if pointer.get("source_issue") != 62:
        errors.append("request pointer source_issue must be 62")
    if not isinstance(pointer.get("record_id"), str) or not pointer.get("record_id"):
        errors.append("request pointer record_id is required")
    if not isinstance(pointer.get("evidence_artifact_ref"), str):
        errors.append("request pointer evidence_artifact_ref is required")
    return errors


def _is_fixture_ref(ref: str) -> bool:
    return Path(ref).parts[:3] == ("tests", "fixtures", "ace-manifest-freshness")


def _path_has_symlink(path: Path) -> bool:
    current = path
    while True:
        if current.is_symlink():
            return True
        if current == REPO_ROOT or current == current.parent:
            return False
        current = current.parent


def _read_record_once(path: Path) -> tuple[bytes, dict, list[str]]:
    try:
        raw = path.read_bytes()
        record = json.loads(raw)
    except FileNotFoundError:
        return b"", {}, [f"referenced artifact is missing: {path}"]
    except json.JSONDecodeError as exc:
        return b"", {}, [f"operational evidence JSON is invalid: {exc}"]
    return raw, record, validate_operational_evidence(record)


def _validate_record_matches_pointer(record: dict, pointer: dict, ref: str) -> list[str]:
    errors: list[str] = []
    if record.get("source_issue") != pointer.get("source_issue"):
        errors.append("referenced artifact source_issue does not match request pointer")
    if record.get("record_id") != pointer.get("record_id"):
        errors.append("referenced artifact record_id does not match request pointer")
    if record.get("evidence_artifact_ref") != ref:
        errors.append("referenced artifact evidence_artifact_ref does not match request pointer")
    return errors


def _load_registry(path: Path) -> tuple[list[str], list[dict]]:
    try:
        registry = json.loads(repo_path(path).read_text())
    except FileNotFoundError:
        return [f"trusted evidence registry is missing: {path}"], []
    except json.JSONDecodeError as exc:
        return [f"trusted evidence registry JSON is invalid: {exc}"], []
    errors = _validate_registry_shape(registry)
    rows = registry.get("trusted_evidence", []) if isinstance(registry, dict) else []
    return errors, rows if isinstance(rows, list) else []


def _validate_registry_shape(registry: object) -> list[str]:
    if not isinstance(registry, dict):
        return ["trusted evidence registry must be a JSON object"]
    errors: list[str] = []
    if set(registry) != REGISTRY_FIELDS:
        errors.append("trusted evidence registry must be a closed root object")
    expected = {"registry_schema_version": "1.0.0", "owner_issue": 70, "consumer_issue": 67, "evidence_source_issue": 62}
    for key, value in expected.items():
        if registry.get(key) != value:
            errors.append(f"trusted evidence registry must set {key} to {value!r}")
    if not isinstance(registry.get("trusted_evidence"), list):
        errors.append("trusted_evidence must be a list")
    return errors


def _find_registry_match(rows: list[dict], record: dict, raw: bytes) -> list[str]:
    digest = hashlib.sha256(raw).hexdigest()
    errors = _validate_rows(rows)
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("record_id") == record.get("record_id") and row.get("evidence_artifact_ref") == record.get("evidence_artifact_ref"):
            errors.extend(_compare_row(row, record, digest))
            return errors
    errors.append("trusted evidence registry has no matching row")
    return errors


def _validate_rows(rows: list[dict]) -> list[str]:
    errors: list[str] = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != ROW_FIELDS:
            errors.append("trusted evidence rows must be closed objects")
            continue
        if not str(row.get("artifact_integrity_digest", "")).isalnum() or len(str(row.get("artifact_integrity_digest", ""))) != 64:
            errors.append("artifact_integrity_digest must be a SHA-256 hex digest")
        url = str(row.get("issue_evidence_comment_url", ""))
        if not GITHUB_ISSUE_REF_RE.fullmatch(url) or "/issues/62#issuecomment-" not in url:
            errors.append("issue_evidence_comment_url must be an issue 62 evidence comment URL")
    return errors


def _compare_row(row: dict, record: dict, digest: str) -> list[str]:
    checks = {
        "artifact_integrity_digest": digest,
        "reviewed_commit": record.get("reviewed_commit"),
        "validator_ref": record.get("validator_ref"),
        "validator_command": record.get("validator_command"),
        "validator_exit_status": record.get("validator_exit_status"),
    }
    return [f"registry {key} does not match evidence artifact" for key, value in checks.items() if row.get(key) != value]


def _review_artifact_paths() -> list[Path]:
    root = REPO_ROOT / "scripts" / "review" / "results"
    if not root.exists():
        return []
    paths = list(root.glob("*plan-70*.md")) + list(root.glob("*implementation-70*.md"))
    return [path.relative_to(REPO_ROOT) for path in sorted(paths) if path.is_file()]
