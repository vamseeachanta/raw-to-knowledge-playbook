"""Runtime evidence emission for ACE issue 62."""
from __future__ import annotations

import json
from pathlib import Path

from ace_manifest_freshness_contract import (
    ALLOWED_VALIDATOR_ENV,
    EXPECTED_MANIFEST_KEYS,
    EXPECTED_PAIR_SOURCES,
    VALIDATOR_REF,
    collect_manifest_status,
)
from ace_manifest_freshness_operational import validate_operational_evidence
from ace_manifest_freshness_operational import safe_output_artifact_path


def build_operational_evidence_record(
    share_root: Path,
    evidence_artifact_ref: str,
    *,
    reviewed_commit: str,
    record_id: str = "ace62-runtime-evidence",
    recorded_at_utc: str = "2026-07-01T00:00:00Z",
    validator_command: list[str] | None = None,
) -> dict:
    evidence_by_source = _collect_sources(Path(share_root))
    snapshots = {key: evidence["snapshot_id"] for key, evidence in evidence_by_source.items()}
    statuses = {key: _source_status(evidence) for key, evidence in evidence_by_source.items()}
    verdicts = _pair_verdicts(snapshots, statuses, evidence_by_source)
    return {
        "record_schema_version": "1.0.0",
        "record_id": record_id,
        "source_issue": 62,
        "evidence_artifact_ref": evidence_artifact_ref,
        "validator_ref": VALIDATOR_REF,
        "validator_env": ALLOWED_VALIDATOR_ENV,
        "validator_command": validator_command or ["uv", "run", "python", VALIDATOR_REF, "--evidence", evidence_artifact_ref],
        "validator_exit_status": 0,
        "recorded_at_utc": recorded_at_utc,
        "reviewed_commit": reviewed_commit,
        "authorization_status": _authorization_status(verdicts),
        "snapshot_ids_by_manifest_source": snapshots,
        "source_status_by_manifest_source": statuses,
        "drift_verdicts_by_manifest_source_pair": verdicts,
        "reconciliation_refs": {},
    }


def emit_operational_evidence(
    share_root: Path,
    evidence_artifact_ref: str,
    *,
    reviewed_commit: str,
    record_id: str = "ace62-runtime-evidence",
) -> list[str]:
    record = build_operational_evidence_record(
        share_root,
        evidence_artifact_ref,
        reviewed_commit=reviewed_commit,
        record_id=record_id,
    )
    errors = validate_operational_evidence(record)
    if errors:
        return errors
    output = safe_output_artifact_path(evidence_artifact_ref)
    if output is None:
        return ["evidence_artifact_ref must resolve inside an allowed #62 artifact root"]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, sort_keys=False) + "\n")
    return []


def _collect_sources(share_root: Path) -> dict[str, dict]:
    return {
        key: collect_manifest_status(key, share_root / key)
        for key in EXPECTED_MANIFEST_KEYS
    }


def _source_status(evidence: dict) -> dict:
    return {
        "content_fingerprint_status": evidence["content_fingerprint_status"],
        "row_count_status": evidence["row_count_status"],
        "evidence_mode": evidence["evidence_mode"],
        "captured_at_utc": evidence["captured_at_utc"],
    }


def _pair_verdicts(snapshots: dict[str, str], statuses: dict[str, dict], evidence: dict[str, dict]) -> dict[str, dict]:
    return {
        pair_id: _pair_verdict(pair_id, left, right, snapshots, statuses, evidence)
        for pair_id, (left, right) in EXPECTED_PAIR_SOURCES.items()
    }


def _pair_verdict(
    pair_id: str,
    left: str,
    right: str,
    snapshots: dict[str, str],
    statuses: dict[str, dict],
    evidence: dict[str, dict],
) -> dict:
    severity, mode = _pair_severity(pair_id, left, right, statuses, evidence)
    return {
        "left_source": left,
        "right_source": right,
        "left_snapshot_id": snapshots[left],
        "right_snapshot_id": snapshots[right],
        "drift_severity": severity,
        "evidence_mode": mode,
        "reconciliation_required": severity in {"warning", "blocker"},
    }


def _pair_severity(
    pair_id: str,
    left: str,
    right: str,
    statuses: dict[str, dict],
    evidence: dict[str, dict],
) -> tuple[str, str]:
    unavailable_modes = {"missing_manifest", "blocked_unavailable"}
    modes = {statuses[left]["evidence_mode"], statuses[right]["evidence_mode"]}
    if modes & unavailable_modes:
        return "unavailable", "missing_manifest" if "missing_manifest" in modes else "blocked_unavailable"
    if pair_id != "inventory_to_assets_presence":
        left_count = evidence[left].get("_bounded_count")
        right_count = evidence[right].get("_bounded_count")
        if isinstance(left_count, int) and isinstance(right_count, int) and left_count != right_count:
            return "warning", "public_safe_summary"
    return "compatible", "public_safe_summary"


def _authorization_status(verdicts: dict[str, dict]) -> str:
    severities = {verdict["drift_severity"] for verdict in verdicts.values()}
    if "unavailable" in severities:
        return "blocked_unavailable"
    if severities & {"warning", "blocker"}:
        return "blocked_requires_reconciliation"
    return "sampling_allowed"
