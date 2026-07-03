"""Public-output certification helpers for ACE issue 63."""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_CONTRACT_PATH = Path("config/ace-public-output-contract.json")
TOKEN_CONTRACT_PATH = Path("config/ace-public-token-fixture-contract.json")
PUBLIC_SURFACE_CONTRACT_PATH = Path("config/ace-public-surface-self-scan-contract.json")
LEGAL_CONFIG_PATH = Path(".legal-deny-list.yaml")
DENY_LIST_PATH = Path("config/ace-public-surface-deny-list.json")
SOURCE_HASH_SWEEP_PATH = Path("artifacts/ace-source-hash-policy-sweep.md")
PUBLIC_SURFACE_HELPER_DIR = REPO_ROOT / "scripts"
if str(PUBLIC_SURFACE_HELPER_DIR) not in sys.path:
    sys.path.insert(0, str(PUBLIC_SURFACE_HELPER_DIR))
LEGAL_HELPER_DIR = REPO_ROOT / "scripts" / "legal"
if str(LEGAL_HELPER_DIR) not in sys.path:
    sys.path.insert(0, str(LEGAL_HELPER_DIR))

from ace_public_surface_contract import (  # noqa: E402
    CONTRACT_PATH as ISSUE_68_CONTRACT_PATH,
    MANIFEST_CONTRACT_PATH,
    TABLE_ASSIGNMENT_RE,
    TEXT_ASSIGNMENT_RE,
    _imported_token_values,
    load_json as load_issue_68_json,
)
from ace_public_surface_rules import (  # noqa: E402
    _allowed_metadata_evidence_paths,
    _scan_line,
    validate_public_artifact_paths as validate_issue_68_public_paths,
)
import legal_sanity_scan  # noqa: E402


SEMVER_RE = re.compile(r"^1\.0\.\d+$")
RAW_DIGEST_RE = re.compile(r"\b[0-9a-f]{32,128}\b", re.IGNORECASE)
GIT_SHA_RE = re.compile(r"\b[0-9a-f]{40}\b", re.IGNORECASE)
MEDIA_METADATA_RE = re.compile(r"(?i)\b(?:exif|gps[_ -]?(?:latitude|longitude)?|gpslatitude|gpslongitude)\b")
ENGINEERING_METADATA_RE = re.compile(r"(?i)\b(?:title[_ -]?block|bom[_ -]?table|bill of materials|unsafe[_ -]?(?:field|table))\b")
COPIED_PRIVATE_SNIPPET_RE = re.compile(r"(?i)\b(?:copied[_ -]?private[_ -]?snippet|private[_ -]?snippet)\b")
SOURCE_HASH_POLICY_HIT_RE = re.compile(
    r"(?i)\b(?:source[-_ ]?(?:hash|digest|provenance)|source_like|source-like|raw digest|"
    r"raw source digest|provenance[_ -]?pointer|source_sha256|source_hash)\b"
)
PUBLICATION_TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".txt", ".csv", ".tsv", ".py", ".sh"}
SOURCE_HASH_SWEEP_ROOTS = (Path("docs"), Path("skills"))
SOURCE_HASH_SWEEP_EXCLUDED_PARTS = {"plans"}
GOVERNANCE_SHA_FIELDS = {"reviewed_commit_sha", "commit_sha", "git_commit_sha"}
FORBIDDEN_INVENTORY_KEYS = {
    "client_names",
    "project_names",
    "customer_names",
    "private_roots",
    "real_values",
    "literal_values",
    "literal_identifier_inventory",
    "private_hostnames",
    "examples",
}
REQUIRED_PUBLIC_SURFACES = {
    "docs",
    "skills",
    "review_artifacts",
    "issue_comment_bodies",
    "closeout_summaries",
    "mkdocs_nav",
    "llm_wiki_outputs",
    "external_publication_summaries",
}
REQUIRED_EVIDENCE_FIELDS = {
    "canary_command",
    "exit_code",
    "scanned_paths",
    "contract_version",
    "timestamp_utc",
}
REQUIRED_DENY_CLASSES = {
    "media-metadata",
    "engineering-metadata",
    "copied-private-snippet",
    "issue-comment-body",
    "external-publication-summary",
}
SWEEP_CLASSIFICATIONS = {
    "modify_public_safe_hash_claim",
    "no_change_private_context",
    "no_change_git_governance_sha",
}


@dataclass(frozen=True)
class SourceHashPolicyHit:
    key: str
    rel_path: Path
    line_number: int


def repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def load_json(path: Path) -> dict:
    return json.loads(repo_path(path).read_text())


def validate_public_output_contract_file(path: Path = OUTPUT_CONTRACT_PATH) -> list[str]:
    try:
        contract = load_json(path)
    except FileNotFoundError:
        return [f"missing public output contract: {path}"]
    except json.JSONDecodeError as exc:
        return [f"public output contract JSON is invalid: {exc}"]
    return validate_public_output_contract(contract, token_contract=load_json(TOKEN_CONTRACT_PATH))


def validate_public_output_contract(contract: dict, *, token_contract: dict) -> list[str]:
    errors: list[str] = []
    errors.extend(_forbidden_inventory_errors(contract))
    expected = {
        "contract_id": "ace-public-output-contract",
        "owner_issue": 63,
        "mode": "publication_certification",
        "stock_ci_live_github_dependency": False,
    }
    for key, expected_value in expected.items():
        if contract.get(key) != expected_value:
            errors.append(f"public output contract must set {key} to {expected_value!r}")
    if not SEMVER_RE.fullmatch(str(contract.get("contract_version", ""))):
        errors.append("public output contract_version must use 1.0.x semver")
    upstream = contract.get("upstream_contracts", {})
    _validate_upstream(upstream, "public_token_fixture_contract", TOKEN_CONTRACT_PATH, 66, errors)
    _validate_upstream(upstream, "public_surface_self_scan_contract", PUBLIC_SURFACE_CONTRACT_PATH, 68, errors)
    _validate_upstream(upstream, "legal_security_scan", LEGAL_CONFIG_PATH, 69, errors)
    if contract.get("public_token_field_name") != token_contract.get("public_token_field_name"):
        errors.append("public output contract must import #66 public token field")
    if contract.get("public_token_grammar") != token_contract.get("public_token_grammar"):
        errors.append("public output contract token grammar must match #66")
    if contract.get("public_safe_source_reference_fields") != [token_contract.get("public_token_field_name")]:
        errors.append("public output contract must allow only public_source_token references")
    for key in ["private_only_provenance_fields", "private_only_fields", "banned_public_fields"]:
        if contract.get(key) != token_contract.get("private_source_terms"):
            errors.append(f"public output contract {key} must match #66 private terms")
    for key in ["source_like_raw_digest_terms", "source_hash_private_terms"]:
        if contract.get(key) != token_contract.get("source_like_raw_digest_terms"):
            errors.append(f"public output contract {key} must match #66 digest terms")
    if set(contract.get("git_governance_sha_fields", [])) != GOVERNANCE_SHA_FIELDS:
        errors.append("git governance SHA fields must stay closed")
    if set(contract.get("public_output_surfaces", [])) != REQUIRED_PUBLIC_SURFACES:
        errors.append("public output surfaces must stay closed")
    if set(contract.get("required_certification_evidence", [])) != REQUIRED_EVIDENCE_FIELDS:
        errors.append("required certification evidence fields must stay closed")
    policy = contract.get("allowed_public_reference_policy", {})
    if policy.get("raw_source_digest_public_reference") is not False or policy.get("raw_private_lookup_public_reference") is not False:
        errors.append("public output contract must reject raw source digest and private lookup public references")
    return errors


def _validate_upstream(upstream: dict, key: str, path: Path, owner_issue: int, errors: list[str]) -> None:
    record = upstream.get(key)
    if not isinstance(record, dict):
        errors.append(f"public output contract must declare upstream {key}")
        return
    if record.get("path") != path.as_posix() or record.get("owner_issue") != owner_issue:
        errors.append(f"public output contract upstream {key} path/owner drifted")


def validate_deny_list_file(path: Path = DENY_LIST_PATH) -> list[str]:
    try:
        record = load_json(path)
    except FileNotFoundError:
        return [f"missing public deny-list supplement: {path}"]
    except json.JSONDecodeError as exc:
        return [f"public deny-list supplement JSON is invalid: {exc}"]
    return validate_deny_list_supplement(record)


def validate_deny_list_supplement(record: dict) -> list[str]:
    errors: list[str] = []
    errors.extend(_forbidden_inventory_errors(record))
    expected = {
        "contract_id": "ace-public-surface-deny-list",
        "owner_issue": 63,
        "mode": "publication_supplement",
    }
    for key, expected_value in expected.items():
        if record.get(key) != expected_value:
            errors.append(f"deny-list supplement must set {key} to {expected_value!r}")
    if not SEMVER_RE.fullmatch(str(record.get("contract_version", ""))):
        errors.append("deny-list supplement contract_version must use 1.0.x semver")
    owners = record.get("upstream_rule_owners", {})
    if owners != {"public_surface_self_scan": 68, "legal_security_scan": 69}:
        errors.append("deny-list supplement must reference #68 and #69 rule owners")
    deny_ids = {item.get("id") for item in record.get("publication_deny_classes", []) if isinstance(item, dict)}
    if deny_ids != REQUIRED_DENY_CLASSES:
        errors.append("publication deny class set must stay closed")
    private_inputs = record.get("optional_private_deny_inputs", {})
    if private_inputs.get("runtime_only") is not True or private_inputs.get("committed_config_allowed") is not False:
        errors.append("private deny-list inputs must be runtime-only and uncommitted")
    return errors


def validate_source_hash_policy_sweep_file(path: Path = SOURCE_HASH_SWEEP_PATH) -> list[str]:
    try:
        text = repo_path(path).read_text()
    except FileNotFoundError:
        return [f"missing source-hash policy sweep: {path}"]
    return validate_source_hash_policy_sweep_text(text)


def validate_source_hash_policy_sweep_text(text: str) -> list[str]:
    errors: list[str] = []
    if RAW_DIGEST_RE.search(text):
        errors.append("source-hash policy sweep must not publish raw digest values")
    if "reject_unclassified" in text:
        errors.append("source-hash policy sweep has unclassified hit")
    rows = _source_hash_sweep_rows(text)
    if not rows:
        errors.append("source-hash policy sweep must classify at least one hit")
    row_keys: set[str] = set()
    for row in rows:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if cells:
            row_keys.add(cells[0])
        if len(cells) < 4 or cells[2] not in SWEEP_CLASSIFICATIONS:
            errors.append(f"source-hash policy sweep row has invalid classification: {cells[0] if cells else 'unknown'}")
    expected_keys = {hit.key for hit in iter_source_hash_policy_hits()}
    missing_keys = sorted(expected_keys - row_keys)
    stale_keys = sorted(row_keys - expected_keys)
    if missing_keys:
        errors.append(f"source-hash policy sweep missing live hit classification: {missing_keys[0]}")
    if stale_keys:
        errors.append(f"source-hash policy sweep contains stale hit classification: {stale_keys[0]}")
    return errors


def _source_hash_sweep_rows(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith("|") and not line.startswith("|---") and "Hit key" not in line]


def iter_source_hash_policy_hits(root: Path = REPO_ROOT) -> list[SourceHashPolicyHit]:
    hits: list[SourceHashPolicyHit] = []
    for scan_root in SOURCE_HASH_SWEEP_ROOTS:
        base = root / scan_root
        if not base.exists():
            continue
        for path in sorted(item for item in base.glob("**/*") if item.is_file()):
            if path.suffix.lower() not in PUBLICATION_TEXT_SUFFIXES:
                continue
            rel_path = path.relative_to(root)
            if scan_root == Path("docs") and rel_path.parts[1:2] and rel_path.parts[1] in SOURCE_HASH_SWEEP_EXCLUDED_PARTS:
                continue
            for line_number, line in enumerate(path.read_text(errors="replace").splitlines(), start=1):
                if SOURCE_HASH_POLICY_HIT_RE.search(line):
                    hits.append(SourceHashPolicyHit(key=_source_hash_hit_key(rel_path, line_number), rel_path=rel_path, line_number=line_number))
    return hits


def _source_hash_hit_key(rel_path: Path, line_number: int) -> str:
    stem = re.sub(r"[^a-z0-9]+", "-", rel_path.as_posix().lower()).strip("-")
    return f"{stem}-l{line_number}"


def validate_public_output_paths(paths: Iterable[Path]) -> list[str]:
    path_list = [Path(path) for path in paths]
    errors = validate_issue_68_public_paths(path_list, contract_path=ISSUE_68_CONTRACT_PATH)
    errors.extend(_validate_legal_public_paths(path_list))
    for path in path_list:
        resolved = repo_path(path)
        if resolved.is_dir():
            for child in sorted(item for item in resolved.glob("**/*") if item.is_file()):
                if _uses_publication_text_scan(child):
                    errors.extend(validate_public_output_text(child.as_posix(), child.read_text(errors="replace")))
        elif resolved.exists():
            if _uses_publication_text_scan(resolved):
                errors.extend(validate_public_output_text(resolved.as_posix(), resolved.read_text(errors="replace")))
    return errors


def _validate_legal_public_paths(paths: list[Path]) -> list[str]:
    try:
        repo = legal_sanity_scan.git_root()
        rules, allow_contexts = legal_sanity_scan.load_config(repo, None)
        candidates = legal_sanity_scan.collect_explicit_candidates(repo, [str(path) for path in paths])
        return legal_sanity_scan.scan_candidates(candidates, rules, allow_contexts)
    except legal_sanity_scan.ScanError as exc:
        return [legal_sanity_scan.redact(str(exc))]


def _uses_publication_text_scan(path: Path) -> bool:
    return path.suffix.lower() in PUBLICATION_TEXT_SUFFIXES


def validate_public_output_text(label: str, text: str) -> list[str]:
    issue_68_contract = load_issue_68_json(ISSUE_68_CONTRACT_PATH)
    token_contract = _imported_token_values(issue_68_contract)
    metadata_paths = _allowed_metadata_evidence_paths(MANIFEST_CONTRACT_PATH)
    path = Path(label)
    errors: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        errors.extend(_scan_line(path, line_number, line, token_contract, metadata_paths))
        errors.extend(_scan_issue_63_line(path, line_number, line))
    return _dedupe_errors(errors)


def _scan_issue_63_line(path: Path, line_number: int, line: str) -> list[str]:
    errors: list[str] = []
    if _line_assigns_any(line, MEDIA_METADATA_RE):
        errors.append(_error(path, line_number, "media-metadata", "media metadata leak"))
    if _line_assigns_any(line, ENGINEERING_METADATA_RE):
        errors.append(_error(path, line_number, "engineering-metadata", "engineering metadata leak"))
    if _line_assigns_any(line, COPIED_PRIVATE_SNIPPET_RE):
        errors.append(_error(path, line_number, "copied-private-snippet", "copied private snippet"))
    if GIT_SHA_RE.search(line) and not _allowed_git_governance_sha(line):
        errors.append(_error(path, line_number, "source-like-digest-assignment", "source-like raw digest"))
    return errors


def _line_assigns_any(line: str, pattern: re.Pattern[str]) -> bool:
    for match in pattern.finditer(line):
        if match.start() > 0 and line[match.start() - 1] in {"-", "/"}:
            continue
        field = re.escape(match.group(0))
        if re.search(TEXT_ASSIGNMENT_RE.format(field=field), line):
            return True
        if line.lstrip().startswith("|") and re.search(TABLE_ASSIGNMENT_RE.format(field=field), line):
            return True
    return False


def validate_public_output_body_text(label: str, text: str) -> list[str]:
    errors = validate_public_output_text(label, text)
    errors.extend(_validate_legal_public_text(label, text))
    return _dedupe_errors(errors)


def _validate_legal_public_text(label: str, text: str) -> list[str]:
    try:
        repo = legal_sanity_scan.git_root()
        rules, allow_contexts = legal_sanity_scan.load_config(repo, None)
        candidate = legal_sanity_scan.Candidate(rel_path=Path(label), source_kind="issue-comment-body", content=text)
        return legal_sanity_scan.scan_candidates([candidate], rules, allow_contexts)
    except legal_sanity_scan.ScanError as exc:
        return [legal_sanity_scan.redact(str(exc))]


def _allowed_git_governance_sha(line: str) -> bool:
    lowered = line.lower()
    return any(field in lowered for field in GOVERNANCE_SHA_FIELDS)


def _forbidden_inventory_errors(value, path: str = "root") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_str = str(key)
            if key_str in FORBIDDEN_INVENTORY_KEYS:
                errors.append(f"forbidden inventory key at {path}: {key_str}")
            errors.extend(_forbidden_inventory_errors(nested, f"{path}.{key_str}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_forbidden_inventory_errors(nested, f"{path}[{index}]"))
    return errors


def _error(path: Path, line_number: int, rule_id: str, summary: str) -> str:
    safe_path = legal_sanity_scan.redact(path.as_posix())
    return f"{rule_id}: {summary} at {safe_path}:{line_number}; match=REDACTED"


def _dedupe_errors(errors: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for error in errors:
        if error not in seen:
            seen.add(error)
            unique.append(error)
    return unique
