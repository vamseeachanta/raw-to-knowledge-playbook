"""Repo-local public-surface scanner helpers for ACE issue 68."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = Path("config/ace-public-surface-self-scan-contract.json")
TOKEN_CONTRACT_PATH = Path("config/ace-public-token-fixture-contract.json")
MANIFEST_CONTRACT_PATH = Path("config/ace-manifest-evidence-contract.json")
REVIEW_ROOT = Path("scripts/review/results")
SEMVER_RE = re.compile(r"^1\.0\.\d+$")
CONFIDENTIAL_TERMS = [
    "proprietary " + "confidential",
    "confidential " + "proprietary",
    "do not " + "distribute",
]
SIDECAR_SUFFIXES = {".err", ".stderr", ".stdout", ".json", ".log", ".trace"}
TEXT_ASSIGNMENT_RE = r"(?i)[\"']?\b{field}\b[\"']?\s*[:=]\s*[^`\s,}}\]]+"
TABLE_ASSIGNMENT_RE = r"(?i)\|\s*{field}\s*\|\s*[^|\s][^|]*\|"
TOKEN_LITERAL_RE = re.compile(r"\bpst_[0-9a-f]{32}\b")
SOURCE_DIGEST_VALUE_RE = re.compile(r"\b[0-9a-f]{32,128}\b", re.IGNORECASE)
ALLOW_MARKER = "ace-public-scan-" + "allow:"
ALLOW_START_RE = re.compile(
    rf"^<!-- {ALLOW_MARKER}start context_id=(?P<context>[A-Za-z0-9_-]+) "
    r"token_class=(?P<token>[A-Za-z0-9_-]+) -->$"
)
ALLOW_END_RE = re.compile(rf"^<!-- {ALLOW_MARKER}end context_id=(?P<context>[A-Za-z0-9_-]+) -->$")
PERSONAL_IDENTIFIER_PATTERNS = [
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b"),
]
PRIVATE_HOST_PATTERNS = [
    re.compile(re.escape("/mnt") + r"/(?:ace|[^`\s|)]*ace[^`\s|)]*)(?:/|\b)"),
    re.compile(r"(?:file://)?" + re.escape("/" + "home") + r"/[A-Za-z0-9._-]+/[^\s`|)]*"),
]
GENERIC_PRIVATE_PATTERNS = [
    re.compile(r"(?i)\b(?:client|customer|project)[-_ ]?(?:id|name)\s*[:=]\s*[A-Za-z0-9_-]+"),
]
CONFIDENTIALITY_PATTERNS = [
    re.compile(r"(?i)\b(?:" + "|".join(re.escape(term) for term in CONFIDENTIAL_TERMS) + r")\b"),
]
FIXED_METADATA_EVIDENCE_PATHS = {"llm-wiki": "directory"}
ACE_ROOT = "ACE" + "_SHARE_ROOT"
FIXED_METADATA_EVIDENCE_RE = re.compile(
    rf"^EXISTS {ACE_ROOT}/(?P<path>[^`\s|]+) type=(?P<kind>file|directory) details=withheld_public$"
)
MANIFEST_PATH_RE = r"(?:\$?\{?ACE_SHARE_ROOT\}?|ACE_SHARE_ROOT|assets\.json|master-index\.jsonl|index\.db|_cad-index)"
UNBOUNDED_TRAVERSAL_PATTERNS = [
    re.compile(rf"\bfind\s+[^\n`]*{MANIFEST_PATH_RE}", re.IGNORECASE),
    re.compile(r"\bls\s+-R\b", re.IGNORECASE),
    re.compile(rf"\bdu\s+[^\n`]*{MANIFEST_PATH_RE}", re.IGNORECASE),
    re.compile(rf"\brg\s+[^\n`]*{MANIFEST_PATH_RE}", re.IGNORECASE),
    re.compile(rf"\bfd\s+[^\n`]*{MANIFEST_PATH_RE}", re.IGNORECASE),
    re.compile(rf"\bgrep\s+(?:-[A-Za-z]*[rR][A-Za-z]*\b|--recursive\b)[^\n`]*{MANIFEST_PATH_RE}", re.IGNORECASE),
    re.compile(r"\bos\.walk\s*\("),
    re.compile(r"\.rglob\s*\("),
    re.compile(rf"\bjq\b[^\n`]*{MANIFEST_PATH_RE}", re.IGNORECASE),
    re.compile(rf"\bcat\b[^\n`]*{MANIFEST_PATH_RE}", re.IGNORECASE),
    re.compile(rf"\bwc(?:\s+-[A-Za-z]*[clmw][A-Za-z]*\b)?[^\n`]*{MANIFEST_PATH_RE}", re.IGNORECASE),
    re.compile(rf"\bsha256sum\b[^\n`]*{MANIFEST_PATH_RE}", re.IGNORECASE),
]
DENIED_TRAVERSAL_POLICY_TERMS = (
    "Denied traversal patterns",
    "unbounded traversal",
    "unbounded crawls",
    "Sampling firewall deny fixtures",
    "denied-command prose",
    "patterns fail validation",
)
ALLOW_CONTEXTS = {
    "schema-term-policy-prose": {
        "token_classes": {"schema_term", "placeholder_value", "public_token_grammar", "rule_id"},
        "headings": {"Pseudocode", "Contract Details Required Before Implementation", "TDD Test List", "Acceptance Criteria"},
        "max_lines": 40,
    },
    "review-artifact-forensics": {
        "token_classes": {"review_finding_excerpt", "redacted_path_token", "rule_id"},
        "headings": None,
        "max_lines": 30,
    },
}
EXPECTED_DENY_CLASSES = {
    "raw-host-path",
    "personal-identifier",
    "confidentiality-marker",
    "generic-private-identifier",
    "private-source-key",
    "source-like-key",
    "forbidden-request-key",
    "source-like-digest-assignment",
    "public-token-assignment",
    "provider-sidecar-leak",
    "unbounded-traversal-command",
    "metadata-evidence-path",
}
EXPECTED_PROVIDERS = {
    "claude",
    "codex",
    "gemini",
    "subagent-boundary",
    "subagent-scanner",
    "subagent-workflow",
}
SNAPSHOT_KEYS = [
    "schema_version",
    "issue_number",
    "comment_id",
    "url",
    "source_kind",
    "phase",
    "fetched_at",
    "body_sha256",
    "body",
]
REVIEW_PHASES = {"plan", "implementation"}
ROUND_RE = re.compile(r"^r[0-9]+$")
REVIEW_ARTIFACT_RE = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}-(?P<phase>plan|implementation)-68-"
    r"(?P<provider>claude|codex|gemini|subagent-boundary|subagent-scanner|subagent-workflow)-"
    r"(?P<round>r[0-9]+)\.md$"
)
SNAPSHOT_SOURCE_KINDS = {"issue_body", "planned_comment", "issue_comment"}
SNAPSHOT_PHASES = {"pre_post", "post_refetch"}
SNAPSHOT_PAIRINGS = {("planned_comment", "issue_comment"), ("issue_body", "issue_body")}
SOURCE_DIGEST_LABELS = ("source hash", "source_hash", "source_sha256", "provenance pointer", "provenance_pointer")


def repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def load_json(path: Path) -> dict:
    return json.loads(repo_path(path).read_text())


def validate_contract_file(path: Path = CONTRACT_PATH) -> list[str]:
    try:
        contract = load_json(path)
    except FileNotFoundError:
        return [f"missing public-surface scan contract: {path}"]
    except json.JSONDecodeError as exc:
        return [f"public-surface scan contract JSON is invalid: {exc}"]
    return validate_contract(contract)


def validate_contract(contract: dict) -> list[str]:
    errors: list[str] = []
    _validate_contract_metadata(contract, errors)
    _validate_token_contract_import(contract, errors)
    _validate_scan_policy_contract(contract, errors)
    return errors


def _imported_token_values(contract: dict) -> dict:
    return contract["upstream_contracts"]["public_token_fixture_contract"]["imported_values"]


def _validate_contract_metadata(contract: dict, errors: list[str]) -> None:
    expected = {
        "contract_id": "ace-public-surface-self-scan-contract",
        "owner_issue": 68,
        "mode": "repo_local_public_surface_self_scan",
        "private_deny_list_owner_issue": 63,
        "stock_ci_live_github_dependency": False,
    }
    for key, value in expected.items():
        if contract.get(key) != value:
            errors.append(f"public-surface scan contract must set {key} to {value!r}")
    if not SEMVER_RE.fullmatch(str(contract.get("contract_version", ""))):
        errors.append("public-surface scan contract_version must use 1.0.x semver")
    if set(contract.get("boundary_owner_issues", {})) != {"65", "66", "69"}:
        errors.append("public-surface scan contract must record #65, #66, and #69 boundaries")


def _validate_token_contract_import(contract: dict, errors: list[str]) -> None:
    imported = contract.get("upstream_contracts", {}).get("public_token_fixture_contract")
    if not isinstance(imported, dict):
        errors.append("public-surface scan contract must import #66 fixture contract")
        return
    if imported.get("path") != TOKEN_CONTRACT_PATH.as_posix():
        errors.append("public-surface scan contract must reference the #66 contract path")
    if imported.get("owner_issue") != 66:
        errors.append("public-surface scan contract must preserve #66 owner issue")
    token_contract = load_json(TOKEN_CONTRACT_PATH)
    if imported.get("contract_id") != token_contract.get("contract_id"):
        errors.append("public-surface scan contract must preserve #66 contract id")
    if imported.get("contract_version") != token_contract.get("contract_version"):
        errors.append("public-surface scan contract must preserve #66 contract version")
    _validate_imported_values(imported, token_contract, errors)


def _validate_imported_values(imported: dict, token_contract: dict, errors: list[str]) -> None:
    fields = imported.get("imported_fields", [])
    values = imported.get("imported_values", {})
    if not isinstance(fields, list) or not fields:
        errors.append("public-surface scan contract must list imported #66 fields")
        return
    if not isinstance(values, dict):
        errors.append("public-surface scan contract imported_values must be an object")
        return
    for field in fields:
        if field not in token_contract:
            errors.append(f"imported #66 field does not exist: {field}")
        elif values.get(field) != token_contract[field]:
            errors.append(f"imported #66 field drifted: {field}")


def _validate_scan_policy_contract(contract: dict, errors: list[str]) -> None:
    deny_ids = {item.get("id") for item in contract.get("deny_classes", []) if isinstance(item, dict)}
    if deny_ids != EXPECTED_DENY_CLASSES:
        errors.append("public-surface deny class set must stay closed")
    contexts = contract.get("allow_contexts", [])
    context_ids = {item.get("id") for item in contexts if isinstance(item, dict)}
    if context_ids != set(ALLOW_CONTEXTS):
        errors.append("public-surface allow context set must stay closed")
    _validate_allow_context_contract(contexts, errors)
    if set(contract.get("sidecar_selector", {}).get("suffixes", [])) != SIDECAR_SUFFIXES:
        errors.append("public-surface sidecar suffix set must stay closed")
    selector = contract.get("review_artifact_selector", {})
    if set(selector.get("provider_enum", [])) != EXPECTED_PROVIDERS:
        errors.append("review artifact provider enum must stay closed")
    snapshot = contract.get("issue_comment_snapshot_schema", {})
    if snapshot.get("top_level_keys") != SNAPSHOT_KEYS:
        errors.append("issue/comment snapshot keys must stay closed")
    for forbidden in ("whole_file_exemptions", "whole_directory_exemptions"):
        if forbidden in contract:
            errors.append(f"blanket exemption is not allowed: {forbidden}")


def _validate_allow_context_contract(contexts: list, errors: list[str]) -> None:
    for item in contexts:
        if not isinstance(item, dict) or item.get("id") not in ALLOW_CONTEXTS:
            continue
        expected = ALLOW_CONTEXTS[item["id"]]
        if set(item.get("token_classes", [])) != expected["token_classes"]:
            errors.append(f"allow context token class set drifted: {item['id']}")
        if item.get("max_lines") != expected["max_lines"]:
            errors.append(f"allow context max_lines drifted: {item['id']}")
        for forbidden in ("whole_file_exemptions", "whole_directory_exemptions"):
            if item.get(forbidden):
                errors.append(f"allow context blanket exemption is not allowed: {item['id']}")
