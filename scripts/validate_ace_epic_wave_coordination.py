#!/usr/bin/env python3
"""Validate the ACE epic wave coordination artifact."""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


EXPECTED_CHILD_ISSUES = set(range(51, 64))
DOWNSTREAM_WAVES = set(range(52, 61))
PUBLICATION_GATE_ISSUES = DOWNSTREAM_WAVES | {61, 63}
MANIFEST_GATE_ISSUES = DOWNSTREAM_WAVES
NON_SAMPLING_MANIFEST_GATE_ISSUES = {51, 61, 62, 63}
CONTROL_SUCCESS_SENTINEL_ISSUES = NON_SAMPLING_MANIFEST_GATE_ISSUES
CROSS_WAVE_GATE_ISSUES = {61, 62, 63}
EXPECTED_WAVE_CLASS = {
    51: "control_plane",
    **{issue: "ingestion_wave" for issue in range(52, 61)},
    61: "storage_lifecycle_gate",
    62: "manifest_freshness_gate",
    63: "public_canary_gate",
}
EXPECTED_REQUIRES_MANIFEST_SNAPSHOT_ID = {issue: issue in MANIFEST_GATE_ISSUES for issue in EXPECTED_CHILD_ISSUES}
PARENT_ISSUE = 50
PARENT_PLAN_PATH = "docs/plans/2026-06-29-issue-50-ace-share-raw-to-knowledge-ingestion-waves-epic.md"
REVIEW_ARTIFACT_ROOT = Path("scripts/review/results")
ALLOWED_METHOD_GAP_DISPOSITIONS = {"doc-update", "skill-eval-update", "follow-on-issue"}
EXPECTED_METHOD_ISSUES = {
    51: {"#1", "#12"},
    52: {"#1", "#12"},
    53: {"#5", "#6", "#12", "#33"},
    54: {"#2", "#3", "#7", "#12", "#33"},
    55: {"#8", "#12", "#33"},
    56: {"#3", "#4", "#12"},
    57: {"#1", "#12"},
    58: {"#9", "#10", "#12"},
    59: {"#6", "#12"},
    60: {"#12"},
    61: {"#1", "#12"},
    62: {"#12"},
    63: {"#12"},
}
EXPECTED_EXECUTABLE_BINDINGS = {
    51: {"scripts/validate_ace_wave0_control_plane.py"},
    52: {"scripts/validate_ace_wave1_text_json.py"},
    53: {"scripts/validate_ace_wave2_spreadsheet_csv.py"},
    54: {"scripts/validate_ace_wave3_document_lane.py"},
    55: {"scripts/validate_ace_wave4_decks_email.py"},
    56: {"scripts/validate_ace_wave5_images.py"},
    57: {"scripts/validate_ace_wave6_cad.py"},
    58: {"examples/simulation-engineering-lane/check.py"},
    59: {"examples/database-geospatial-index-lane/check.py"},
    60: {"scripts/validate_ace_wave9_media_archive_noise.py"},
    61: {"scripts/validate_ace_knowledge_store_contract.py", "scripts/validate_ace_ingested_success_metric.py"},
    62: {"scripts/validate_ace_manifest_freshness.py"},
    63: {"scripts/validate_ace_public_artifacts.py"},
}
VALID_LANES = {"lane:claude", "lane:codex"}
VALID_COMPLEXITIES = {"T2", "T3"}
VALID_PLAN_STATUSES = {"draft", "plan-review", "plan-approved", "completed"}
REVIEW_VERDICTS = {"APPROVE", "MINOR", "MAJOR"}
REVIEW_HISTORY_VERDICTS = REVIEW_VERDICTS | {"UNAVAILABLE"}
EXPECTED_CHILD_LEDGER_HEADERS = [
    "issue",
    "plan",
    "lane",
    "complexity",
    "plan status",
    "status snapshot",
    "implementation ready",
    "method issues",
    "skill groups and executable tests",
    "review artifacts",
    "dependencies",
    "expected useful ingestion / success metric / difficulty",
    "manifest gate",
    "public canary gate",
    "method gap disposition",
    "publication exposure",
]
EXPECTED_STRUCTURAL_WAVE_GATE_HEADERS = [
    "issue",
    "wave_class",
    "requires_manifest_snapshot_id",
    "success_numerator_field",
    "success_denominator_field",
]
CONFIDENTIAL_TERMS = [
    "proprietary " + "confidential",
    "confidential " + "proprietary",
    "do not " + "distribute",
]
EVIDENCE_PLACEHOLDER_TERMS = (
    "not run",
    "expected",
    "todo",
    "tbd",
    "pending",
    "without",
    "does not require",
    "not require",
)
PRIVATE_LEAK_PATTERNS = [
    re.escape("/mnt") + r"/(?:ace|[^`\s|)]*ace[^`\s|)]*)(?:/|\b)",
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    r"(?i)\b(?:client|customer|project)[-_ ]?(?:id|name)\s*[:=]\s*[A-Za-z0-9_-]+",
    r"(?i)\b(?:" + "|".join(re.escape(term) for term in CONFIDENTIAL_TERMS) + r")\b",
    r"\b\d{3}-\d{2}-\d{4}\b",
    r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b",
]
PRIVATE_SOURCE_FIELD_ASSIGNMENT_PATTERNS = [
    r"(?i)[\"']?\b(?:source_id|source_sha256|private_lookup_key|private_lookup_map|share_relative_path_private_only)\b[\"']?\s*[:=]\s*[^`\s,}\]]+",
    r"(?i)[\"']?\bpublic_source_token\b[\"']?\s*[:=]\s*[\"']?pst_[0-9a-f]{32}\b",
]
SOURCE_LIKE_RAW_DIGEST_PATTERNS = [
    r"(?i)\b(?:source\s+hash|source_hash|source_sha256|provenance\s+pointer)\b\s*[:=]\s*[\"']?[0-9a-f]{32,128}\b",
    r"(?i)\|\s*(?:source\s+hash|source_hash|source_sha256|provenance\s+pointer)\s*\|\s*[\"']?[0-9a-f]{32,128}\b",
]
MANIFEST_PATH_PATTERN = r"(?:\$?\{?ACE_SHARE_ROOT\}?|ACE_SHARE_ROOT|assets\.json|master-index\.jsonl|index\.db|_cad-index)"
DENIED_TRAVERSAL_PATTERNS = [
    rf"\bfind\s+[^\n`]*{MANIFEST_PATH_PATTERN}",
    r"\bls\s+-R\b",
    rf"\bdu\s+[^\n`]*{MANIFEST_PATH_PATTERN}",
    rf"\brg\s+[^\n`]*{MANIFEST_PATH_PATTERN}",
    rf"\bfd\s+[^\n`]*{MANIFEST_PATH_PATTERN}",
    rf"\bgrep\s+(?:-[A-Za-z]*[rR][A-Za-z]*|--recursive)\b[^\n`]*{MANIFEST_PATH_PATTERN}",
    r"\bos\.walk\s*\(",
    r"\.rglob\s*\(",
    rf"\bjq\b[^\n`]*{MANIFEST_PATH_PATTERN}",
    rf"\bcat\b[^\n`]*{MANIFEST_PATH_PATTERN}",
    rf"\bwc(?:\s+-[A-Za-z]*[clmw][A-Za-z]*\b)?[^\n`]*{MANIFEST_PATH_PATTERN}",
    rf"\bsha256sum\b[^\n`]*{MANIFEST_PATH_PATTERN}",
]
INTERNAL_TRAVERSAL_SENTINEL = "public-artifact-scan-internal-directory-walk-ok"
DENIED_TRAVERSAL_POLICY_PROSE_TERMS = (
    "Denied traversal patterns",
    "unbounded traversal",
    "unbounded crawls",
    "Sampling firewall deny fixtures",
    "denied-command prose",
    "patterns fail validation",
)
REQUIRED_APPROVAL_MARKER_FIELDS = [
    "Approved by:",
    "Approval date:",
    "Issue:",
    "Plan path:",
    "Reviewed commit:",
    "Review artifacts:",
]


@dataclass
class ValidationResult:
    errors: list[str]


def _parse_child_issues(text: str) -> set[int]:
    issues: set[int] = set()
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        first_cell = line.split("|", 2)[1].strip()
        match = re.fullmatch(r"(?:#(\d+)|\[#(\d+)\]\([^)]+\))", first_cell)
        if match:
            issues.add(int(match.group(1) or match.group(2)))
    return issues


def _split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _normalise_header(header: str) -> str:
    return re.sub(r"\s+", " ", header.strip().lower())


def _parse_child_rows(text: str) -> tuple[dict[int, dict[str, str]], list[str]]:
    rows: dict[int, dict[str, str]] = {}
    errors: list[str] = []
    headers: list[str] | None = None
    in_child_table = False
    in_child_section = False
    saw_child_section = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            in_child_section = stripped == "## Child Wave Ledger"
            saw_child_section = saw_child_section or in_child_section
            in_child_table = False
            headers = None
            continue
        if not in_child_section:
            continue
        if line.startswith("| Issue | Plan | Lane | Complexity |"):
            headers = [_normalise_header(header) for header in _split_markdown_row(line)]
            if headers != EXPECTED_CHILD_LEDGER_HEADERS:
                errors.append("child wave ledger header must match canonical schema")
            in_child_table = True
            continue
        if not in_child_table:
            continue
        if not line.startswith("|"):
            in_child_table = False
            continue
        if re.fullmatch(r"\|\s*-+.*", line):
            continue
        cells = _split_markdown_row(line)
        if not cells:
            continue
        match = re.fullmatch(r"(?:#(\d+)|\[#(\d+)\]\([^)]+\))", cells[0])
        if not match:
            continue
        issue = int(match.group(1) or match.group(2))
        if headers is None:
            continue
        if len(cells) != len(headers):
            errors.append(f"#{issue} row has {len(cells)} cells; expected {len(headers)}")
            continue
        padded = cells + [""] * max(0, len(headers) - len(cells))
        if issue in rows:
            errors.append(f"duplicate child issue row for #{issue}")
            continue
        rows[issue] = dict(zip(headers, padded))
    if not saw_child_section:
        errors.append("missing ## Child Wave Ledger section")
    return rows, errors


def _parse_structural_wave_gate_rows(text: str) -> tuple[dict[int, dict[str, str]], list[str]]:
    rows: dict[int, dict[str, str]] = {}
    errors: list[str] = []
    headers: list[str] | None = None
    in_registry = False
    in_table = False
    saw_registry = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            in_registry = stripped == "## Structural Wave Gate Registry"
            saw_registry = saw_registry or in_registry
            in_table = False
            headers = None
            continue
        if not in_registry:
            continue
        if line.startswith("| Issue | wave_class | requires_manifest_snapshot_id |"):
            headers = [_normalise_header(header) for header in _split_markdown_row(line)]
            if headers != EXPECTED_STRUCTURAL_WAVE_GATE_HEADERS:
                errors.append("Structural Wave Gate Registry header must match canonical schema")
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            in_table = False
            continue
        if re.fullmatch(r"\|\s*-+.*", line):
            continue
        cells = _split_markdown_row(line)
        match = re.fullmatch(r"(?:#(\d+)|\[#(\d+)\]\([^)]+\))", cells[0] if cells else "")
        if not match:
            continue
        issue = int(match.group(1) or match.group(2))
        if headers is None:
            continue
        if len(cells) != len(headers):
            errors.append(f"#{issue} structural wave gate row has {len(cells)} cells; expected {len(headers)}")
            continue
        if issue in rows:
            errors.append(f"duplicate structural wave gate row for #{issue}")
            continue
        rows[issue] = dict(zip(headers, cells))
    if not saw_registry:
        errors.append("missing ## Structural Wave Gate Registry section")
    return rows, errors


def _has_all(text: str, required_terms: list[str]) -> bool:
    lower = text.lower()
    return all(term.lower() in lower for term in required_terms)


def _has_forbidden_negation(text: str) -> bool:
    lower = text.lower()
    return "does not require" in lower or "not require" in lower or "without " in lower


def _has_gate_phrase(text: str, issue: int, phrase: str) -> bool:
    return f"#{issue} {phrase}".lower() in text.lower() and not _has_forbidden_negation(text)


def _contains_method_issue(issue: int, cell: str) -> bool:
    anchors = set(re.findall(r"#\d+", cell))
    return EXPECTED_METHOD_ISSUES.get(issue, set()).issubset(anchors)


def _contains_executable_binding(issue: int, cell: str) -> bool:
    lower = cell.lower()
    if "tbd" in lower or "todo" in lower:
        return False
    required = EXPECTED_EXECUTABLE_BINDINGS.get(issue, set())
    return bool(required) and all(binding.lower() in lower for binding in required)


def _contains_control_success_sentinel(issue: int, cell: str) -> bool:
    lower = cell.lower()
    required_terms = [
        "0%",
        "success_metric_applicability=not_applicable_control_plane",
        "expected_yield=0",
        "measured_success_numerator=0",
        "measured_success_denominator=0",
        "success_threshold=0",
        "validation_command=",
        "difficulty",
    ]
    if not all(term in lower for term in required_terms):
        return False
    required_paths = EXPECTED_EXECUTABLE_BINDINGS.get(issue, set())
    return bool(required_paths) and all(path.lower() in lower for path in required_paths)


def _review_artifacts_recorded(cell: str) -> bool:
    provider_status: dict[str, str] = {}
    for part in [part.strip() for part in cell.split(";") if part.strip()]:
        match = re.fullmatch(r"(Claude|Codex|Gemini):\s*(.+)", part, flags=re.IGNORECASE)
        if not match:
            return False
        provider_status[match.group(1).lower()] = match.group(2).strip().lower()
    if set(provider_status) != {"claude", "codex", "gemini"}:
        return False
    return all(_review_status_valid(status) for status in provider_status.values())


def _review_status_valid(status: str) -> bool:
    if status in {"pending", "not-run"}:
        return True
    if status.startswith("unavailable"):
        return status == "unavailable" or status.startswith("unavailable:")
    return _review_artifact_path_valid(status)


def _review_artifact_path_valid(path_text: str, *, allow_unavailable: bool = False) -> bool:
    path = Path(path_text)
    if path.is_absolute() or ".." in path.parts or path.suffix != ".md":
        return False
    try:
        root = REVIEW_ARTIFACT_ROOT.resolve(strict=True)
        resolved = path.resolve(strict=True)
    except FileNotFoundError:
        return False
    try:
        resolved.relative_to(root)
    except ValueError:
        return False
    if resolved.stat().st_size == 0:
        return False
    try:
        text = resolved.read_text(errors="replace")
    except OSError:
        return False
    verdict = _extract_review_verdict(text)
    allowed = REVIEW_HISTORY_VERDICTS if allow_unavailable else REVIEW_VERDICTS
    return verdict in allowed


def _extract_review_verdict(text: str) -> str | None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        heading_match = re.match(r"(?i)^\s*(?:##\s+)?Verdict\s*:?\s*(.*)$", line)
        bullet_match = re.match(r"(?i)^\s*-\s+\*\*Verdict:\*\*\s*(.*)$", line)
        value = ""
        if bullet_match:
            value = bullet_match.group(1)
        elif heading_match:
            value = heading_match.group(1)
            if not value:
                for next_line in lines[index + 1 :]:
                    value = next_line.strip()
                    if value:
                        break
        else:
            continue
        candidate = re.sub(r"^[\s`*_]+", "", value.strip())
        match = re.match(r"(APPROVE|MINOR|MAJOR|UNAVAILABLE)(?:\b|[^A-Za-z0-9_])", candidate, flags=re.IGNORECASE)
        if match:
            return match.group(1).upper()
        return None
    return None


def _method_gap_disposition_closed(cell: str) -> bool:
    found = {token for token in ALLOWED_METHOD_GAP_DISPOSITIONS if token in cell}
    if cell.strip().lower().startswith("closed-set:"):
        return found == ALLOWED_METHOD_GAP_DISPOSITIONS
    if found == {"follow-on-issue"}:
        return bool(re.search(r"#\d+", cell))
    if found == {"doc-update"}:
        return "docs/" in cell
    if found == {"skill-eval-update"}:
        return "skills/" in cell or "evals/evals.json" in cell
    return False


def validate_approval_marker(marker_path: Path, issue: int, expected_plan: str) -> list[str]:
    errors: list[str] = []
    if not marker_path.exists():
        return [f"missing approval marker for #{issue}: {marker_path}"]
    text = marker_path.read_text()
    fields: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[f"{key.strip()}:"] = value.strip()
    for field in REQUIRED_APPROVAL_MARKER_FIELDS:
        if field not in fields:
            errors.append(f"#{issue} approval marker missing {field}")
        elif field != "Review artifacts:" and not fields[field]:
            errors.append(f"#{issue} approval marker has empty {field}")
    if f"/issues/{issue}" not in fields.get("Issue:", ""):
        errors.append(f"#{issue} approval marker issue URL must match issue")
    if fields.get("Plan path:", "") != expected_plan.strip("`"):
        errors.append(f"#{issue} approval marker plan path must match {expected_plan}")
    if not re.fullmatch(r"[0-9a-f]{40}", fields.get("Reviewed commit:", "")):
        errors.append(f"#{issue} approval marker reviewed commit must be a 40-character SHA")
    artifact_paths = _approval_marker_artifact_paths(text)
    if not artifact_paths:
        errors.append(f"#{issue} approval marker must include review artifact bullet paths")
    for path in artifact_paths:
        if not _review_artifact_path_valid(path, allow_unavailable=True):
            errors.append(f"#{issue} approval marker review artifact must be an existing scripts/review/results/*.md path: {path}")
    return errors


def _approval_marker_artifact_paths(text: str) -> list[str]:
    artifact_paths: list[str] = []
    in_artifacts = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "Review artifacts:":
            in_artifacts = True
            continue
        if not in_artifacts:
            continue
        if stripped.startswith("-"):
            artifact_paths.append(stripped.removeprefix("-").strip())
            continue
        if stripped and re.match(r"^[A-Za-z][A-Za-z ]+:", stripped):
            break
    return artifact_paths


def _approval_marker_valid(marker_path: Path, issue: int, expected_plan: str) -> bool:
    return not validate_approval_marker(marker_path, issue, expected_plan)


def _validate_global_contract(text: str, errors: list[str]) -> None:
    bounded_terms = [
        "ACE_SHARE_ROOT",
        "Named manifest sources",
        "Seed/sort rule",
        "Row caps",
        "maximum files touched",
        "maximum bytes touched",
        "Denied traversal patterns",
    ]
    if not _has_all(text, bounded_terms):
        errors.append("bounded read contract must declare ACE_SHARE_ROOT, named manifests, seed/sort, row caps, file/byte caps, and denied traversal patterns")

    if not _has_all(text, ["Branch publication rule", "dedicated planning branch", "stacked-branch note"]):
        errors.append("branch publication rule must require a dedicated planning branch or explicit stacked-branch note")

    if not _has_all(text, ["Public artifact safety gate", "path-tokenization", "public_source_token", "raw source id/hash denial", "generic private-like identifier", "personal identifier", "proprietary snippet", "deny-list certification", "#63 gate", "docs nav", "mkdocs", "llm-wiki"]):
        errors.append("public artifact safety gate must cover path-tokenization, opaque public_source_token use, raw source id/hash denial, generic private-like/personal/proprietary checks, #63 deny-list certification, docs nav, mkdocs, and llm-wiki publication")

    if "successful_routed_items / eligible_candidate_items * 100" not in text:
        errors.append("ingested success metric must be `successful_routed_items / eligible_candidate_items * 100`")

    if not _has_all(text, sorted(ALLOWED_METHOD_GAP_DISPOSITIONS)):
        errors.append("method gap disposition closed set must be doc-update, skill-eval-update, or follow-on-issue")

    for line_number, line in enumerate(text.splitlines(), start=1):
        policy_catalog_line = "Denied traversal patterns" in line and not re.search(
            MANIFEST_PATH_PATTERN, line
        )
        for pattern in DENIED_TRAVERSAL_PATTERNS:
            if not policy_catalog_line and re.search(pattern, line):
                errors.append(f"unbounded traversal command is not allowed at line {line_number}: {line.strip()}")
                break
        for pattern in PRIVATE_LEAK_PATTERNS:
            if re.search(pattern, line):
                errors.append(f"public artifact leak is not allowed at line {line_number}: {line.strip()}")
                break


def _row_ready(row: dict[str, str], issue: int, approval_root: Path | None) -> bool:
    ready = row.get("implementation ready", "").strip().lower() in {"true", "yes"}
    snapshot = row.get("status snapshot", "")
    plan = row.get("plan", "").strip("`")
    marker_valid = False
    if approval_root is not None:
        marker_valid = _approval_marker_valid(approval_root / f"{issue}.md", issue, plan)
    gate_evidence_ready = issue not in CROSS_WAVE_GATE_ISSUES or not _gate_readiness_errors(row, issue)
    return ready and "status:plan-approved" in snapshot and marker_valid and gate_evidence_ready


def _gate_readiness_errors(row: dict[str, str], issue: int) -> list[str]:
    if issue not in CROSS_WAVE_GATE_ISSUES:
        return []
    errors: list[str] = []
    evidence = _parse_status_snapshot_evidence(row.get("status snapshot", ""))
    implemented_key = "implemented-canary" if issue == 63 else "implemented-validator"
    implemented = evidence.get(implemented_key, "")
    command = evidence.get("passing-command", "")
    exit_code = evidence.get("exit-code", "")
    required_paths = EXPECTED_EXECUTABLE_BINDINGS.get(issue, set())
    missing_paths = sorted(path for path in required_paths if not Path(path).exists())
    if missing_paths:
        errors.append(f"#{issue} gate readiness requires implemented executable binding(s): {', '.join(missing_paths)}")
    if not implemented or any(path not in implemented for path in required_paths):
        errors.append(f"#{issue} gate readiness requires {implemented_key}: evidence for expected executable binding(s)")
    if not command or not any(path in command for path in required_paths):
        errors.append(f"#{issue} gate readiness requires passing-command: to invoke an expected executable binding")
    if exit_code != "0":
        errors.append(f"#{issue} gate readiness requires exact exit-code:0 evidence")
    if any(_has_placeholder_evidence(value) for value in [implemented, command, exit_code]):
        errors.append(f"#{issue} gate readiness rejects placeholder, negated, pending, or expected evidence")
    return errors


def _parse_status_snapshot_evidence(snapshot: str) -> dict[str, str]:
    evidence: dict[str, str] = {}
    for part in snapshot.split(";"):
        if ":" not in part:
            continue
        key, value = part.split(":", 1)
        evidence[key.strip().lower()] = value.strip()
    return evidence


def _has_placeholder_evidence(value: str) -> bool:
    lower = value.lower()
    normalised = re.sub(r"[^a-z0-9]+", " ", lower).strip()
    compact = re.sub(r"[^a-z0-9]+", "", lower)
    return any(term in normalised for term in EVIDENCE_PLACEHOLDER_TERMS) or "notrun" in compact


def _validate_row(issue: int, row: dict[str, str], approval_root: Path | None, errors: list[str]) -> None:
    plan = row.get("plan", "").strip("`")
    if not plan or f"issue-{issue}" not in plan or not plan.endswith(".md"):
        errors.append(f"#{issue} plan must name an issue-specific markdown plan file")
    if row.get("lane", "") not in VALID_LANES:
        errors.append(f"#{issue} lane must be one of {sorted(VALID_LANES)}")
    if row.get("complexity", "") not in VALID_COMPLEXITIES:
        errors.append(f"#{issue} complexity must be one of {sorted(VALID_COMPLEXITIES)}")
    plan_status = row.get("plan status", "")
    if plan_status not in VALID_PLAN_STATUSES:
        errors.append(f"#{issue} plan status must be one of {sorted(VALID_PLAN_STATUSES)}")
    if not row.get("status snapshot", "").strip():
        errors.append(f"#{issue} status snapshot must be recorded")

    method_issues = row.get("method issues", "")
    if not _contains_method_issue(issue, method_issues):
        expected = ", ".join(sorted(EXPECTED_METHOD_ISSUES.get(issue, set())))
        errors.append(f"#{issue} method issues must include expected anchors: {expected}")

    skill_groups = row.get("skill groups and executable tests", "")
    if not _contains_executable_binding(issue, skill_groups):
        expected = ", ".join(sorted(EXPECTED_EXECUTABLE_BINDINGS.get(issue, set())))
        errors.append(f"#{issue} skill groups must include expected executable binding(s): {expected}")

    review_artifacts = row.get("review artifacts", "")
    if not _review_artifacts_recorded(review_artifacts):
        errors.append(f"#{issue} review artifacts must record Claude, Codex, and Gemini paths/statuses")

    ready = row.get("implementation ready", "").strip().lower() in {"true", "yes"}
    snapshot = row.get("status snapshot", "")
    marker_valid = False
    if approval_root is not None:
        marker_valid = _approval_marker_valid(approval_root / f"{issue}.md", issue, plan)
    if plan_status in {"plan-approved", "completed"} and ("status:plan-approved" not in snapshot or not marker_valid):
        errors.append(f"#{issue} plan-approved status requires status:plan-approved snapshot and local approval marker")
    if ready and ("status:plan-approved" not in snapshot or not marker_valid):
        errors.append(f"#{issue} implementation ready requires status:plan-approved snapshot and local approval marker")
        if approval_root is not None and (approval_root / f"{issue}.md").exists() and not marker_valid:
            errors.append(f"#{issue} approval marker must include required approval fields")
    if ready:
        errors.extend(_gate_readiness_errors(row, issue))

    dependencies = row.get("dependencies", "")
    if issue in DOWNSTREAM_WAVES and "#51" not in dependencies:
        errors.append(f"#{issue} dependencies must include #51 wave-0 control-plane gate")
    if issue in PUBLICATION_GATE_ISSUES and "#61" not in dependencies:
        errors.append(f"#{issue} dependencies must include #61 durable-output lifecycle gate")
    if issue in PUBLICATION_GATE_ISSUES:
        lifecycle_phrase = "status:plan-approved + approval marker + implemented validator + recorded passing-command"
        if not _has_gate_phrase(dependencies, 61, lifecycle_phrase):
            errors.append(f"#{issue} #61 gate must require status:plan-approved, approval marker, implemented validator, and recorded passing-command")

    metric = row.get("expected useful ingestion / success metric / difficulty", "")
    if issue in CONTROL_SUCCESS_SENTINEL_ISSUES:
        if not _contains_control_success_sentinel(issue, metric):
            errors.append(f"#{issue} ingestion metric must use the non-computing zero success sentinel with validation_command and difficulty rank")
    elif (
        "%" not in metric
        or "successful_routed_items / eligible_candidate_items * 100" not in metric
        or "difficulty" not in metric.lower()
        or "success_metric_applicability=not_applicable_control_plane" in metric.lower()
    ):
        errors.append(f"#{issue} ingestion metric must include expected %, success formula, and difficulty rank")

    manifest_gate = row.get("manifest gate", "")
    manifest_phrase = "status:plan-approved+approval marker+implemented validator+recorded passing-command+snapshot_id"
    if issue in MANIFEST_GATE_ISSUES:
        if not _has_gate_phrase(manifest_gate, 62, manifest_phrase):
            errors.append(f"#{issue} manifest gate must require #62 status:plan-approved+approval marker+implemented validator+recorded passing-command+snapshot_id before sampling")
    elif issue in NON_SAMPLING_MANIFEST_GATE_ISSUES:
        if "not applicable for own sampling" not in manifest_gate.lower() or "#62 gate applies to downstream sampling" not in manifest_gate:
            errors.append(f"#{issue} manifest gate must state not applicable for own sampling while preserving #62 downstream sampling gate")

    public_gate = row.get("public canary gate", "")
    public_phrase = "status:plan-approved+approval marker+implemented canary+recorded passing-command"
    if not _has_gate_phrase(public_gate, 63, public_phrase):
        errors.append(f"#{issue} public canary gate must require #63 status:plan-approved+approval marker+implemented canary+recorded passing-command before publication")

    method_gap = row.get("method gap disposition", "")
    if not _method_gap_disposition_closed(method_gap):
        errors.append(f"#{issue} method gap disposition must be the closed set doc-update, skill-eval-update, follow-on-issue")

    exposure = row.get("publication exposure", "").strip().lower()
    if exposure not in {"true", "false"}:
        errors.append(f"#{issue} publication exposure must be true or false")


def _validate_structural_wave_gate_row(issue: int, row: dict[str, str], errors: list[str]) -> None:
    expected_class = EXPECTED_WAVE_CLASS[issue]
    if row.get("wave_class", "") != expected_class:
        errors.append(f"#{issue} wave_class must be {expected_class}")
    expected_requires_snapshot = "true" if EXPECTED_REQUIRES_MANIFEST_SNAPSHOT_ID[issue] else "false"
    if row.get("requires_manifest_snapshot_id", "").lower() != expected_requires_snapshot:
        errors.append(f"#{issue} requires_manifest_snapshot_id must be {expected_requires_snapshot}")
    expected_numerator = "successful_routed_items" if issue in DOWNSTREAM_WAVES else "measured_success_numerator"
    expected_denominator = "eligible_candidate_items" if issue in DOWNSTREAM_WAVES else "measured_success_denominator"
    if row.get("success_numerator_field", "") != expected_numerator:
        errors.append(f"#{issue} success_numerator_field must be {expected_numerator}")
    if row.get("success_denominator_field", "") != expected_denominator:
        errors.append(f"#{issue} success_denominator_field must be {expected_denominator}")


def validate_text(text: str, approval_root: Path | None = None) -> ValidationResult:
    errors: list[str] = []
    _validate_global_contract(text, errors)
    structural_rows, structural_parse_errors = _parse_structural_wave_gate_rows(text)
    errors.extend(structural_parse_errors)
    rows, parse_errors = _parse_child_rows(text)
    errors.extend(parse_errors)
    structural_issues = set(structural_rows)
    child_issues = set(rows)
    missing_structural = sorted(EXPECTED_CHILD_ISSUES - structural_issues)
    extra_structural = sorted(issue for issue in structural_issues if issue not in EXPECTED_CHILD_ISSUES)
    if missing_structural:
        errors.append(f"Structural Wave Gate Registry missing parsable child issues: {', '.join(f'#{issue}' for issue in missing_structural)}")
    if extra_structural:
        errors.append(f"unexpected structural wave gate issues: {', '.join(f'#{issue}' for issue in extra_structural)}")
    for issue in sorted(EXPECTED_CHILD_ISSUES & structural_issues):
        _validate_structural_wave_gate_row(issue, structural_rows[issue], errors)
    missing = sorted(EXPECTED_CHILD_ISSUES - child_issues)
    extra = sorted(issue for issue in child_issues if issue not in EXPECTED_CHILD_ISSUES)
    if missing:
        errors.append(f"child wave ledger missing parsable child issues: {', '.join(f'#{issue}' for issue in missing)}")
    if extra:
        errors.append(f"unexpected child issues: {', '.join(f'#{issue}' for issue in extra)}")
    for issue in sorted(EXPECTED_CHILD_ISSUES & set(rows)):
        _validate_row(issue, rows[issue], approval_root, errors)
    if 61 in rows:
        issue_61_ready = _row_ready(rows[61], 61, approval_root)
        for issue, row in sorted(rows.items()):
            if issue in DOWNSTREAM_WAVES and row.get("implementation ready", "").strip().lower() in {"true", "yes"} and not issue_61_ready:
                errors.append(f"#{issue} #61 dependency must be implementation-ready before downstream durable output is ready")
    issue_63_ready = 63 in rows and _row_ready(rows[63], 63, approval_root)
    for issue, row in sorted(rows.items()):
        if row.get("publication exposure", "").strip().lower() == "true" and not issue_63_ready:
            errors.append(f"#{issue} publication exposure requires #63 implementation-ready approval marker and canary evidence")
    return ValidationResult(errors)


def validate_public_artifact_paths(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for root in paths:
        if not root.exists():
            errors.append(f"missing public artifact scan path: {root}")
            continue
        candidates = [root]
        if root.is_dir():
            candidates = [path for path in root.rglob("*") if path.is_file()]  # public-artifact-scan-internal-directory-walk-ok
        for path in candidates:
            if path.suffix == ".pyc":
                continue
            text = path.read_text(errors="ignore")
            for line_number, line in enumerate(text.splitlines(), start=1):
                for pattern in DENIED_TRAVERSAL_PATTERNS:
                    if re.search(pattern, line):
                        if _allowed_internal_traversal_line(path, line) or _allowed_denied_traversal_policy_prose(line):
                            continue
                        errors.append(f"unbounded traversal command is not allowed at {path}:{line_number}: {line.strip()}")
                        break
                for pattern in PRIVATE_LEAK_PATTERNS:
                    if re.search(pattern, line):
                        errors.append(f"public artifact leak is not allowed at {path}:{line_number}: {line.strip()}")
                        break
                for pattern in PRIVATE_SOURCE_FIELD_ASSIGNMENT_PATTERNS:
                    if re.search(pattern, line):
                        errors.append(f"private source field assignment is not allowed at {path}:{line_number}: {line.strip()}")
                        break
                for pattern in SOURCE_LIKE_RAW_DIGEST_PATTERNS:
                    if re.search(pattern, line):
                        errors.append(f"source-like raw digest is not allowed at {path}:{line_number}: {line.strip()}")
                        break
    return errors


def _allowed_internal_traversal_line(path: Path, line: str) -> bool:
    return (
        path.name == "validate_ace_epic_wave_coordination.py"
        and INTERNAL_TRAVERSAL_SENTINEL in line
        and ("root." + "rglob") in line
        and "path.is_file" in line
    )


def _allowed_denied_traversal_policy_prose(line: str) -> bool:
    return not re.search(MANIFEST_PATH_PATTERN, line) and any(
        term in line for term in DENIED_TRAVERSAL_POLICY_PROSE_TERMS
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        default="docs/plans/ace-share-ingestion-wave-coordination.md",
        help="coordination markdown path",
    )
    parser.add_argument(
        "--scan-public-path",
        action="append",
        default=[],
        help="additional public artifact file/directory to scan for private leakage",
    )
    args = parser.parse_args(argv)

    path = Path(args.path)
    if not path.exists():
        print(f"FAIL: missing coordination artifact: {path}", file=sys.stderr)
        return 1
    approval_root = Path(".planning/plan-approved")
    result = validate_text(path.read_text(), approval_root=approval_root)
    errors = (
        result.errors
        + validate_approval_marker(approval_root / f"{PARENT_ISSUE}.md", PARENT_ISSUE, PARENT_PLAN_PATH)
        + validate_public_artifact_paths([Path(item) for item in args.scan_public_path])
    )
    if errors:
        for error in errors:
            print(f"DENY  {error}", file=sys.stderr)
        print(f"\nFAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: ACE epic wave coordination valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
