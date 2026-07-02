"""Public artifact scanning rules for ACE issue 68."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

try:
    from .ace_public_surface_contract import (
        ACE_ROOT, ALLOW_CONTEXTS, ALLOW_END_RE, ALLOW_MARKER, ALLOW_START_RE,
        CONTRACT_PATH, DENIED_TRAVERSAL_POLICY_TERMS, FIXED_METADATA_EVIDENCE_PATHS,
        FIXED_METADATA_EVIDENCE_RE, GENERIC_PRIVATE_PATTERNS, CONFIDENTIALITY_PATTERNS,
        MANIFEST_CONTRACT_PATH, MANIFEST_PATH_RE, PERSONAL_IDENTIFIER_PATTERNS,
        PRIVATE_HOST_PATTERNS, SIDECAR_SUFFIXES, SOURCE_DIGEST_LABELS,
        SOURCE_DIGEST_VALUE_RE, TABLE_ASSIGNMENT_RE, TEXT_ASSIGNMENT_RE, TOKEN_LITERAL_RE,
        UNBOUNDED_TRAVERSAL_PATTERNS, REPO_ROOT, _imported_token_values, load_json,
        repo_path, validate_contract_file,
    )
except ImportError:
    from ace_public_surface_contract import (
        ACE_ROOT, ALLOW_CONTEXTS, ALLOW_END_RE, ALLOW_MARKER, ALLOW_START_RE,
        CONTRACT_PATH, DENIED_TRAVERSAL_POLICY_TERMS, FIXED_METADATA_EVIDENCE_PATHS,
        FIXED_METADATA_EVIDENCE_RE, GENERIC_PRIVATE_PATTERNS, CONFIDENTIALITY_PATTERNS,
        MANIFEST_CONTRACT_PATH, MANIFEST_PATH_RE, PERSONAL_IDENTIFIER_PATTERNS,
        PRIVATE_HOST_PATTERNS, SIDECAR_SUFFIXES, SOURCE_DIGEST_LABELS,
        SOURCE_DIGEST_VALUE_RE, TABLE_ASSIGNMENT_RE, TEXT_ASSIGNMENT_RE, TOKEN_LITERAL_RE,
        UNBOUNDED_TRAVERSAL_PATTERNS, REPO_ROOT, _imported_token_values, load_json,
        repo_path, validate_contract_file,
    )


def validate_public_artifact_paths(
    paths: Iterable[Path],
    contract_path: Path = CONTRACT_PATH,
    manifest_contract_path: Path = MANIFEST_CONTRACT_PATH,
    allow_external_paths: bool = False,
) -> list[str]:
    errors: list[str] = []
    contract_errors = validate_contract_file(contract_path)
    if contract_errors:
        return contract_errors
    contract = load_json(contract_path)
    token_contract = _imported_token_values(contract)
    metadata_paths = _allowed_metadata_evidence_paths(manifest_contract_path)
    for root in paths:
        errors.extend(_scan_path(root, token_contract, metadata_paths, allow_external_paths))
    return errors


def _bounded_scan_root(root: Path, allow_external_paths: bool) -> tuple[Path, list[str]]:
    if allow_external_paths:
        return repo_path(root), []
    if root.is_absolute() and not _is_under_repo(root):
        return root, [f"scan-path-absolute: outside repo path is not allowed: {root}"]
    if any(part == ".." for part in root.parts):
        return root, [f"scan-path-traversal: parent traversal is not allowed: {root}"]
    path = repo_path(root)
    if path.is_symlink():
        return path, [f"scan-path-symlink: symlink scan path is not allowed: {root}"]
    if path.exists() and not _is_under_repo(path):
        return path, [f"scan-path-symlink: symlink ancestor escapes repo: {root}"]
    return path, []


def _is_under_repo(path: Path) -> bool:
    try:
        path.resolve().relative_to(REPO_ROOT.resolve())
    except ValueError:
        return False
    return True


def _scan_path(
    root: Path,
    token_contract: dict,
    metadata_paths: dict[str, str],
    allow_external_paths: bool,
) -> list[str]:
    path, path_errors = _bounded_scan_root(root, allow_external_paths)
    if path_errors:
        return path_errors
    if not path.exists():
        return [f"missing public artifact scan path: {root}"]
    candidates = [path]
    if path.is_dir():
        candidates = [item for item in path.glob("**/*") if item.is_file()]
    errors: list[str] = []
    for candidate in candidates:
        if candidate.suffix == ".pyc":
            continue
        if candidate.is_symlink():
            errors.append(_error(candidate, 1, "scan-path-symlink", "scan path symlink"))
            continue
        if not allow_external_paths and not _is_under_repo(candidate):
            errors.append(_error(candidate, 1, "scan-path-symlink", "scan path escapes repo"))
            continue
        errors.extend(_scan_file(candidate, token_contract, metadata_paths))
    return errors


def _scan_file(path: Path, token_contract: dict, metadata_paths: dict[str, str]) -> list[str]:
    text = path.read_text(errors="replace")
    errors = _scan_json_keys(path, text, token_contract)
    allowed_rules, allow_errors = _allow_context_rules(path, text)
    errors.extend(allow_errors)
    for line_number, line in enumerate(text.splitlines(), start=1):
        line_errors = _scan_line(path, line_number, line, token_contract, metadata_paths)
        errors.extend(_filter_allowed_line_errors(line_errors, allowed_rules.get(line_number, set())))
    return errors


def _scan_line(
    path: Path,
    line_number: int,
    line: str,
    token_contract: dict,
    metadata_paths: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    if _is_unbounded_traversal(line) and not _allowed_denied_traversal_policy_prose(line):
        errors.append(_error(path, line_number, "unbounded-traversal-command", "unbounded traversal"))
    if (ACE_ROOT + "/") in line and not _is_allowed_metadata_evidence_line(line, metadata_paths):
        errors.append(_error(path, line_number, "metadata-evidence-path", "unlisted ACE metadata evidence path"))
    sidecar = path.suffix in SIDECAR_SUFFIXES
    if sidecar and _matches_any(PRIVATE_HOST_PATTERNS, line):
        errors.append(_error(path, line_number, "provider-sidecar-leak", "public artifact leak"))
    elif _matches_any(PRIVATE_HOST_PATTERNS, line):
        errors.append(_error(path, line_number, "raw-host-path", "public artifact leak"))
    for pattern in PERSONAL_IDENTIFIER_PATTERNS:
        if pattern.search(line):
            errors.append(_error(path, line_number, "personal-identifier", "public artifact leak"))
            break
    for pattern in GENERIC_PRIVATE_PATTERNS:
        if pattern.search(line):
            errors.append(_error(path, line_number, "generic-private-identifier", "public artifact leak"))
            break
    for pattern in CONFIDENTIALITY_PATTERNS:
        if pattern.search(line):
            errors.append(_error(path, line_number, "confidentiality-marker", "public artifact leak"))
            break
    errors.extend(_scan_line_terms(path, line_number, line, token_contract))
    return errors


def _scan_line_terms(path: Path, line_number: int, line: str, token_contract: dict) -> list[str]:
    errors: list[str] = []
    for field in token_contract["private_source_terms"]:
        if _line_assigns_field(line, field):
            errors.append(_error(path, line_number, "private-source-key", "private source field assignment"))
    for field in token_contract["source_like_raw_digest_terms"]:
        if _line_assigns_field(line, field) and SOURCE_DIGEST_VALUE_RE.search(line):
            errors.append(_error(path, line_number, "source-like-digest-assignment", "source-like raw digest"))
    for field in token_contract["forbidden_request_keys"]:
        if _line_assigns_field(line, field) and not _allowed_python_loop_variable(path, line, field):
            errors.append(_error(path, line_number, "forbidden-request-key", "forbidden request key"))
    if _line_assigns_source_digest(line) and SOURCE_DIGEST_VALUE_RE.search(line):
        errors.append(_error(path, line_number, "source-like-digest-assignment", "source-like raw digest"))
    token_field = re.escape(token_contract["public_token_field_name"])
    if re.search(TEXT_ASSIGNMENT_RE.format(field=token_field), line) and TOKEN_LITERAL_RE.search(line):
        errors.append(_error(path, line_number, "public-token-assignment", "private source field assignment"))
    return errors


def _scan_json_keys(path: Path, text: str, token_contract: dict) -> list[str]:
    if path.suffix.lower() != ".json":
        return []
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return []
    keys = set(_collect_json_keys(payload))
    return _deny_key_errors(path, keys, token_contract)


def _deny_key_errors(path: Path, keys: set[str], token_contract: dict) -> list[str]:
    errors: list[str] = []
    line_number = 1
    for key in sorted(keys & set(token_contract["private_source_terms"])):
        errors.append(_error(path, line_number, "private-source-key", "private source field assignment", key))
    for key in sorted(keys & set(token_contract["source_like_raw_digest_terms"])):
        errors.append(_error(path, line_number, "source-like-key", "source-like raw digest", key))
    for key in sorted(keys & set(token_contract["forbidden_request_keys"])):
        errors.append(_error(path, line_number, "forbidden-request-key", "forbidden request key", key))
    return errors


def _collect_json_keys(value) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _collect_json_keys(child)
    elif isinstance(value, list):
        for item in value:
            yield from _collect_json_keys(item)


def _matches_any(patterns: Iterable[re.Pattern], line: str) -> bool:
    return any(pattern.search(line) for pattern in patterns)


def _line_assigns_field(line: str, field: str) -> bool:
    escaped = re.escape(field)
    if re.search(TEXT_ASSIGNMENT_RE.format(field=escaped), line):
        return True
    return line.lstrip().startswith("|") and bool(re.search(TABLE_ASSIGNMENT_RE.format(field=escaped), line))


def _line_assigns_source_digest(line: str) -> bool:
    return any(_line_assigns_field(line, field) for field in SOURCE_DIGEST_LABELS)


def _allowed_python_loop_variable(path: Path, line: str, field: str) -> bool:
    return path.suffix == ".py" and f"for {field} in" in line


def _allowed_denied_traversal_policy_prose(line: str) -> bool:
    return not re.search(MANIFEST_PATH_RE, line) and any(term in line for term in DENIED_TRAVERSAL_POLICY_TERMS)


def _filter_allowed_line_errors(errors: list[str], allowed_rules: set[str]) -> list[str]:
    return [error for error in errors if _rule_id(error) not in allowed_rules]


def _rule_id(error: str) -> str:
    return error.split(":", 1)[0]


def _allow_context_rules(path: Path, text: str) -> tuple[dict[int, set[str]], list[str]]:
    if ALLOW_MARKER not in text:
        return {}, []
    if path.suffix in {".json", ".py"}:
        return {}, [_error(path, 1, "allow-context-forbidden-filetype", "HTML allow sentinel forbidden")]
    return _parse_allow_contexts(path, text.splitlines())


def _parse_allow_contexts(path: Path, lines: list[str]) -> tuple[dict[int, set[str]], list[str]]:
    errors: list[str] = []
    allowed: dict[int, set[str]] = {}
    open_block: dict | None = None
    current_heading = ""
    for line_number, line in enumerate(lines, start=1):
        current_heading = _updated_heading(current_heading, line)
        start = ALLOW_START_RE.fullmatch(line.strip())
        end = ALLOW_END_RE.fullmatch(line.strip())
        if start:
            open_block = _open_allow_block(path, line_number, start, current_heading, open_block, errors)
            continue
        if end:
            open_block = _close_allow_block(path, line_number, end, open_block, errors)
            continue
        if open_block is not None:
            _record_allow_line(path, line_number, line, open_block, allowed, errors)
    if open_block is not None:
        errors.append(_error(path, open_block["start"], "allow-context-eof", "missing allow end sentinel"))
    return allowed, errors


def _updated_heading(current_heading: str, line: str) -> str:
    if not line.startswith("#"):
        return current_heading
    return line.lstrip("#").strip()


def _open_allow_block(
    path: Path,
    line_number: int,
    start: re.Match,
    heading: str,
    open_block: dict | None,
    errors: list[str],
) -> dict:
    if open_block is not None:
        errors.append(_error(path, line_number, "allow-context-nested", "nested allow context"))
    context_id = start.group("context")
    token_class = start.group("token")
    block = {"id": context_id, "token": token_class, "start": line_number, "lines": 0, "valid": True}
    block["valid"] = _validate_allow_block_start(path, line_number, context_id, token_class, heading, errors)
    return block


def _close_allow_block(
    path: Path,
    line_number: int,
    end: re.Match,
    open_block: dict | None,
    errors: list[str],
) -> dict | None:
    if open_block is None:
        errors.append(_error(path, line_number, "allow-context-stray-end", "allow end without start"))
        return None
    if end.group("context") != open_block["id"]:
        errors.append(_error(path, line_number, "allow-context-overlap", "allow context mismatch"))
    return None


def _record_allow_line(
    path: Path,
    line_number: int,
    line: str,
    open_block: dict,
    allowed: dict[int, set[str]],
    errors: list[str],
) -> None:
    open_block["lines"] += 1
    context = ALLOW_CONTEXTS.get(open_block["id"], {})
    if open_block["lines"] > context.get("max_lines", 0):
        errors.append(_error(path, line_number, "allow-context-line-budget", "allow context line budget exceeded"))
        open_block["valid"] = False
    if open_block["valid"] and _allow_line_is_reference_only(line):
        allowed[line_number] = _allowed_rule_ids(open_block["token"])


def _allow_line_is_reference_only(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    return ":" not in stripped and "=" not in stripped and not stripped.startswith("|")


def _allowed_rule_ids(token_class: str) -> set[str]:
    if token_class in {"schema_term", "placeholder_value", "public_token_grammar", "rule_id"}:
        return {"private-source-key", "source-like-key", "forbidden-request-key"}
    return set()


def _validate_allow_block_start(
    path: Path,
    line_number: int,
    context_id: str,
    token_class: str,
    heading: str,
    errors: list[str],
) -> bool:
    context = ALLOW_CONTEXTS.get(context_id)
    if context is None:
        errors.append(_error(path, line_number, "allow-context-unknown", "unknown allow context"))
        return False
    valid = _validate_allow_path(path, line_number, context_id, errors)
    if token_class not in context["token_classes"]:
        errors.append(_error(path, line_number, "allow-context-token-class", "unknown allow token class"))
        valid = False
    headings = context["headings"]
    if headings is not None and heading not in headings:
        errors.append(_error(path, line_number, "allow-context-heading", "allow heading mismatch"))
        valid = False
    return valid


def _validate_allow_path(path: Path, line_number: int, context_id: str, errors: list[str]) -> bool:
    normalized = path.as_posix()
    valid = False
    if context_id == "schema-term-policy-prose":
        valid = path.suffix == ".md" and "issue-68" in path.name and (
            "/docs/plans/" in normalized or "/scripts/review/results/" in normalized
        )
    if context_id == "review-artifact-forensics":
        valid = "/scripts/review/results/" in normalized and "plan-68" in path.name
    if not valid:
        errors.append(_error(path, line_number, "allow-context-path", "allow path mismatch"))
    return valid


def _allowed_metadata_evidence_paths(manifest_contract_path: Path) -> dict[str, str]:
    paths = dict(FIXED_METADATA_EVIDENCE_PATHS)
    try:
        contract = load_json(manifest_contract_path)
    except (FileNotFoundError, json.JSONDecodeError):
        return paths
    for source_key in contract.get("manifest_source_keys", []):
        paths[str(source_key)] = "file"
    return paths


def _is_allowed_metadata_evidence_line(line: str, allowed_paths: dict[str, str]) -> bool:
    match = FIXED_METADATA_EVIDENCE_RE.fullmatch(line.strip())
    if not match:
        return False
    return allowed_paths.get(match.group("path")) == match.group("kind")


def _is_unbounded_traversal(line: str) -> bool:
    return _matches_any(UNBOUNDED_TRAVERSAL_PATTERNS, line)


def _error(path: Path, line_number: int, rule_id: str, summary: str, key: str | None = None) -> str:
    suffix = f" key={key}" if key else ""
    return f"{rule_id}: {summary} at {path}:{line_number}{suffix}; match=REDACTED"
