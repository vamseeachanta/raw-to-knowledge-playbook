#!/usr/bin/env python3
"""Repo-local legal and security public-surface scanner."""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


CONFIG_PATH = Path(".legal-deny-list.yaml")
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".txt", ".csv", ".tsv", ".py", ".sh"}
TOP_LEVEL_TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".toml"}
INCLUDE_PREFIXES = {"docs", "skills", "scripts", "tests", "artifacts", "config", "examples"}
EXCLUDED_PARTS = {"__pycache__", ".git", ".mypy_cache", ".pytest_cache"}
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
TOP_LEVEL_KEYS = {
    "format",
    "owner_issue",
    "private_runtime_config_owner_issue",
    "config_contract",
    "rules",
    "allow_contexts",
}
RULE_KEYS = {"id", "severity", "description", "patterns"}
ALLOW_CONTEXT_KEYS = {"context_id", "path_globs", "rule_ids", "sentinel", "max_lines_per_file", "justification"}
ALLOW_CONTEXT_POLICIES = {
    "test-fixture-forensic-examples": {
        "path_globs": {"tests/fixtures/.tmp-legal-allow-*.md"},
        "rule_ids": {"private-root-shape"},
        "line_pattern": r".*",
    },
}

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
HOST_RE = re.compile(r"\b(?:[A-Za-z0-9-]+\.)+(?:com|net|org|io|ai|dev|co|edu|gov|mil|biz|info|internal)\b")
PRIVATE_PATH_RE = re.compile(r"(?i)(?:/mnt|/home|/tmp)/[^\s`|)]*")
IDENTIFIER_ASSIGNMENT_RE = re.compile(r"(?i)\b(?:client|customer|project)[-_ ]?(?:id|name)\s*[:=]\s*[A-Za-z0-9_-]+")
HEX_DIGEST_RE = re.compile(r"\b[0-9a-f]{32,128}\b", re.I)
SECRET_ASSIGNMENT_RE = re.compile(r"(?i)\b(?:api[_-]?key|api[_-]?token|access[_-]?token|secret|password)\s*[:=]\s*[A-Za-z0-9_./+=-]{8,}")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
PHONE_RE = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b")


@dataclass(frozen=True)
class Rule:
    id: str
    severity: str
    description: str
    patterns: list[re.Pattern[str]]


@dataclass(frozen=True)
class AllowContext:
    context_id: str
    path_globs: list[str]
    rule_ids: set[str]
    sentinel: str
    max_lines_per_file: int
    justification: str


@dataclass(frozen=True)
class Candidate:
    rel_path: Path
    source_kind: str
    content: str


class ScanError(Exception):
    def __init__(self, message: str, code: int = 2) -> None:
        super().__init__(message)
        self.code = code


def git_root() -> Path:
    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise ScanError("not inside a git repository")
    return Path(result.stdout.strip()).resolve()


def run_git(repo: Path, args: list[str]) -> bytes:
    result = subprocess.run(["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise ScanError(f"git command failed: {redact(result.stderr.decode(errors='replace'))}")
    return result.stdout


def git_paths(repo: Path, args: list[str]) -> list[Path]:
    output = run_git(repo, args)
    return [Path(item.decode("utf-8", errors="surrogateescape")) for item in output.split(b"\0") if item]


def load_config(repo: Path, config_arg: str | None) -> tuple[list[Rule], list[AllowContext]]:
    path = Path(config_arg) if config_arg else repo / CONFIG_PATH
    if not path.is_absolute():
        path = repo / path
    try:
        raw = path.read_text()
    except OSError as exc:
        raise ScanError(f"config read failed: {redact(str(exc))}") from exc
    try:
        record = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ScanError(f"config must be strict JSON text despite .yaml extension: {redact(str(exc))}") from exc
    validate_config_record(record)
    return build_rules(record), build_allow_contexts(record.get("allow_contexts", []))


def validate_config_record(record) -> None:
    if not isinstance(record, dict):
        raise ScanError("config root must be an object")
    unknown = set(record) - TOP_LEVEL_KEYS
    if unknown:
        if unknown & FORBIDDEN_INVENTORY_KEYS:
            raise ScanError("config contains forbidden inventory key")
        raise ScanError(f"config contains unknown top-level key: {sorted(unknown)[0]}")
    if record.get("format") != "json-subset-yaml":
        raise ScanError("config format must be json-subset-yaml")
    if record.get("owner_issue") != 69 or record.get("private_runtime_config_owner_issue") != 63:
        raise ScanError("config issue ownership fields are invalid")
    if not isinstance(record.get("rules"), list) or not record["rules"]:
        raise ScanError("config requires non-empty rules")
    for rule in record["rules"]:
        validate_rule_record(rule)
    known_rule_ids = {rule["id"] for rule in record["rules"]}
    if len(known_rule_ids) != len(record["rules"]):
        raise ScanError("rule ids must be unique")
    for context in record.get("allow_contexts", []):
        validate_allow_context(context, known_rule_ids)


def validate_rule_record(rule) -> None:
    if not isinstance(rule, dict):
        raise ScanError("rule must be an object")
    forbidden = set(rule) & FORBIDDEN_INVENTORY_KEYS
    if forbidden:
        raise ScanError("rule contains forbidden inventory key")
    unknown = set(rule) - RULE_KEYS
    if unknown:
        raise ScanError(f"rule contains unknown key: {sorted(unknown)[0]}")
    if not isinstance(rule.get("id"), str) or not rule["id"]:
        raise ScanError("rule requires id")
    if rule.get("severity") not in {"block", "warn"}:
        raise ScanError("rule severity must be block or warn")
    if not isinstance(rule.get("description"), str) or not rule["description"]:
        raise ScanError("rule requires description")
    patterns = rule.get("patterns")
    if not isinstance(patterns, list) or not patterns:
        raise ScanError("rule requires non-empty patterns")
    for pattern in patterns:
        if not isinstance(pattern, str) or not pattern:
            raise ScanError("rule patterns must be non-empty strings")
        validate_policy_pattern(pattern)
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ScanError(f"rule pattern compile failed: {redact(str(exc))}") from exc


def validate_policy_pattern(pattern: str) -> None:
    literal_probe = re.sub(r"\\(.)", r"\1", pattern)
    literal_probe = re.sub(r"\[([A-Za-z0-9._-])\]", r"\1", literal_probe)
    if looks_sensitive(literal_probe):
        raise ScanError("pattern field contains literal sensitive-looking value")


def validate_allow_context(context, known_rule_ids: set[str]) -> None:
    if not isinstance(context, dict):
        raise ScanError("allow context must be an object")
    unknown = set(context) - ALLOW_CONTEXT_KEYS
    if unknown:
        raise ScanError(f"allow context contains unknown key: {sorted(unknown)[0]}")
    if not isinstance(context.get("context_id"), str) or not context["context_id"]:
        raise ScanError("allow context requires context_id")
    policy = ALLOW_CONTEXT_POLICIES.get(context["context_id"])
    if policy is None:
        raise ScanError("unknown allow context id")
    globs = context.get("path_globs")
    if not isinstance(globs, list) or not globs or any(not is_restricted_path_glob(item) for item in globs):
        raise ScanError("allow context requires restricted path_globs")
    if not set(globs).issubset(policy["path_globs"]):
        raise ScanError("allow context path_globs do not match context policy")
    rule_ids = context.get("rule_ids")
    if not isinstance(rule_ids, list) or not rule_ids or any(not isinstance(item, str) for item in rule_ids):
        raise ScanError("allow context requires rule_ids")
    if any(rule_id not in known_rule_ids for rule_id in rule_ids):
        raise ScanError("allow context references unknown rule id")
    if not set(rule_ids).issubset(policy["rule_ids"]):
        raise ScanError("allow context rule_ids do not match context policy")
    if not isinstance(context.get("sentinel"), str) or not context["sentinel"]:
        raise ScanError("allow context requires same-line sentinel")
    if not isinstance(context.get("max_lines_per_file"), int) or context["max_lines_per_file"] < 1:
        raise ScanError("allow context requires max_lines_per_file")
    if not isinstance(context.get("justification"), str) or not context["justification"]:
        raise ScanError("allow context requires justification")


def is_restricted_path_glob(pattern: object) -> bool:
    if not isinstance(pattern, str) or not pattern:
        return False
    if pattern in {"*", "**"} or pattern.endswith("/*") or pattern.endswith("/**") or "**" in pattern:
        return False
    name = Path(pattern).name
    if not name or name == "*":
        return False
    return Path(pattern).suffix.lower() in TEXT_SUFFIXES


def build_rules(record: dict) -> list[Rule]:
    rules: list[Rule] = []
    for rule in record["rules"]:
        rules.append(
            Rule(
                id=rule["id"],
                severity=rule["severity"],
                description=rule["description"],
                patterns=[re.compile(pattern) for pattern in rule["patterns"]],
            )
        )
    return rules


def build_allow_contexts(records: list[dict]) -> list[AllowContext]:
    return [
        AllowContext(
            context_id=record["context_id"],
            path_globs=list(record["path_globs"]),
            rule_ids=set(record["rule_ids"]),
            sentinel=record["sentinel"],
            max_lines_per_file=record["max_lines_per_file"],
            justification=record["justification"],
        )
        for record in records
    ]


def looks_sensitive(value: str) -> bool:
    return any(
        regex.search(value)
        for regex in [EMAIL_RE, HOST_RE, PRIVATE_PATH_RE, IDENTIFIER_ASSIGNMENT_RE, HEX_DIGEST_RE, SECRET_ASSIGNMENT_RE, SSN_RE, PHONE_RE]
    )


def classify_path(rel_path: Path) -> str:
    parts = rel_path.parts
    if not parts or any(part in EXCLUDED_PARTS for part in parts):
        return "exclude"
    suffix = rel_path.suffix.lower()
    rel = rel_path.as_posix()
    if suffix == ".pyc" or rel.startswith(".claude/state/"):
        return "exclude"
    if rel == ".legal-deny-list.yaml":
        return "include"
    if parts[0] == ".github":
        return "include" if len(parts) >= 3 and parts[1] == "workflows" and suffix in {".yaml", ".yml"} else "exclude"
    if parts[0] == ".planning":
        return "include" if suffix in {".md", ".json"} else "exclude"
    if parts[0] == ".claude":
        return "include" if suffix in {".md", ".json", ".yaml", ".yml"} else "exclude"
    if parts[0] in INCLUDE_PREFIXES:
        if parts[0] == "scripts" and len(parts) >= 3 and parts[1] == "review" and parts[2] == "results":
            return "include" if suffix == ".md" else "exclude"
        return "include" if suffix in TEXT_SUFFIXES or rel.endswith("/.gitignore") else "exclude"
    if len(parts) == 1 and (suffix in TOP_LEVEL_TEXT_SUFFIXES or rel in {".gitignore", ".gitattributes"}):
        return "include"
    return "unclassified" if suffix in TEXT_SUFFIXES else "exclude"


def candidate_from_path(repo: Path, rel_path: Path, source_kind: str) -> Candidate | None:
    classification = classify_path(rel_path)
    if classification == "exclude":
        return None
    if classification == "unclassified":
        raise ScanError(f"unclassified public-surface candidate: {redact(rel_path.as_posix())}")
    path = repo / rel_path
    try:
        text = path.read_text(errors="replace")
    except OSError as exc:
        raise ScanError(f"candidate read failed: {redact(str(exc))}") from exc
    return Candidate(rel_path=rel_path, source_kind=source_kind, content=text)


def staged_candidate(repo: Path, rel_path: Path) -> Candidate | None:
    classification = classify_path(rel_path)
    if classification == "exclude":
        return None
    if classification == "unclassified":
        raise ScanError(f"unclassified public-surface candidate: {redact(rel_path.as_posix())}")
    blob = run_git(repo, ["show", f":{rel_path.as_posix()}"])
    return Candidate(rel_path=rel_path, source_kind="staged", content=blob.decode("utf-8", errors="replace"))


def collect_diff_candidates(repo: Path) -> tuple[list[Candidate], list[str]]:
    candidates: list[Candidate] = []
    errors: list[str] = []
    for rel_path in git_paths(repo, ["diff", "-z", "--cached", "--name-only", "--diff-filter=ACMR"]):
        candidate = staged_candidate(repo, rel_path)
        if candidate is not None:
            candidates.append(candidate)
    for rel_path in git_paths(repo, ["diff", "-z", "--name-only", "--diff-filter=ACMR"]):
        candidate = candidate_from_path(repo, rel_path, "unstaged")
        if candidate is not None:
            candidates.append(candidate)
    for rel_path in git_paths(repo, ["ls-files", "-z", "--others", "--exclude-standard"]):
        classification = classify_path(rel_path)
        if classification in {"include", "unclassified"}:
            errors.append(f"DENY candidate-untracked source=untracked path={redact(rel_path.as_posix())}: untracked public-surface candidate")
    return candidates, errors


def collect_tracked_candidates(repo: Path) -> list[Candidate]:
    candidates: list[Candidate] = []
    for rel_path in git_paths(repo, ["ls-files", "-z"]):
        candidate = candidate_from_path(repo, rel_path, "tracked")
        if candidate is not None:
            candidates.append(candidate)
    return candidates


def collect_explicit_candidates(repo: Path, requested: list[str]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for item in requested:
        path = Path(item)
        if ".." in path.parts:
            raise ScanError(f"path traversal is not allowed: {redact(str(path))}")
        resolved = path.resolve() if path.is_absolute() else (repo / path).resolve()
        try:
            resolved.relative_to(repo)
        except ValueError as exc:
            raise ScanError(f"path outside repository: {redact(str(path))}") from exc
        if not resolved.exists():
            raise ScanError(f"scan path missing: {redact(str(path))}")
        paths = iter_files_bounded(resolved) if resolved.is_dir() else [resolved]
        for candidate_path in paths:
            rel_path = candidate_path.relative_to(repo)
            candidate = candidate_from_path(repo, rel_path, "explicit")
            if candidate is not None:
                candidates.append(candidate)
    return candidates


def iter_files_bounded(root: Path) -> list[Path]:
    files: list[Path] = []
    stack = [root]
    while stack:
        current = stack.pop()
        for child in sorted(current.iterdir()):
            if child.is_symlink():
                raise ScanError(f"symlink scan path rejected: {redact(str(child))}")
            if child.is_dir():
                if child.name not in EXCLUDED_PARTS:
                    stack.append(child)
            elif child.is_file():
                files.append(child)
    return files


def scan_candidates(candidates: list[Candidate], rules: list[Rule], allow_contexts: list[AllowContext]) -> list[str]:
    findings: list[str] = []
    allow_counts: dict[tuple[str, str], int] = {}
    for index, candidate in enumerate(candidates, start=1):
        line_items = config_scan_lines(candidate.content) if candidate.rel_path.as_posix() == ".legal-deny-list.yaml" else list(enumerate(candidate.content.splitlines(), start=1))
        for line_number, line in line_items:
            for rule in rules:
                if any(pattern.search(line) for pattern in rule.patterns):
                    if allowed_by_context(candidate.rel_path, line, rule.id, allow_contexts, allow_counts):
                        continue
                    findings.append(
                        "DENY "
                        f"candidate-{index:04d} source={candidate.source_kind} "
                        f"path={redact(candidate.rel_path.as_posix())} line={line_number} "
                        f"severity={rule.severity} rule={rule.id} description={redact(rule.description)}"
                    )
                    break
    return findings


def config_scan_lines(text: str) -> list[tuple[int, str]]:
    try:
        record = json.loads(text)
    except json.JSONDecodeError:
        return list(enumerate(text.splitlines(), start=1))
    lines: list[tuple[int, str]] = []
    counter = 1

    def walk(value, key: str = "") -> None:
        nonlocal counter
        if key == "patterns":
            return
        if isinstance(value, dict):
            for child_key, child in value.items():
                walk(child, str(child_key))
        elif isinstance(value, list):
            for child in value:
                walk(child, key)
        elif isinstance(value, str):
            lines.append((counter, value))
            counter += 1

    walk(record)
    return lines


def allowed_by_context(
    rel_path: Path,
    line: str,
    rule_id: str,
    allow_contexts: list[AllowContext],
    allow_counts: dict[tuple[str, str], int],
) -> bool:
    rel = rel_path.as_posix()
    for context in allow_contexts:
        if rule_id not in context.rule_ids:
            continue
        if context.sentinel not in line:
            continue
        if any(fnmatch.fnmatch(rel, pattern) for pattern in context.path_globs):
            policy = ALLOW_CONTEXT_POLICIES.get(context.context_id, {})
            if not re.fullmatch(str(policy.get("line_pattern", r".*")), line):
                continue
            key = (context.context_id, rel)
            if allow_counts.get(key, 0) >= context.max_lines_per_file:
                return False
            allow_counts[key] = allow_counts.get(key, 0) + 1
            return True
    return False


def redact(text: str) -> str:
    redacted = PRIVATE_PATH_RE.sub("[REDACTED-PATH]", text)
    redacted = EMAIL_RE.sub("[REDACTED-EMAIL]", redacted)
    redacted = HOST_RE.sub("[REDACTED-HOST]", redacted)
    redacted = SSN_RE.sub("[REDACTED-SSN]", redacted)
    redacted = PHONE_RE.sub("[REDACTED-PHONE]", redacted)
    redacted = IDENTIFIER_ASSIGNMENT_RE.sub("[REDACTED-ID]", redacted)
    redacted = SECRET_ASSIGNMENT_RE.sub("[REDACTED-SECRET]", redacted)
    redacted = HEX_DIGEST_RE.sub("[REDACTED-DIGEST]", redacted)
    return redacted


def emit_errors(errors: list[str]) -> None:
    for error in errors:
        print(redact(error), file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config")
    parser.add_argument("--diff-only", action="store_true")
    parser.add_argument("--all-tracked-public-surfaces", action="store_true")
    parser.add_argument("--scan-public-path", action="append", default=[])
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args(argv)
    if not args.diff_only and not args.all_tracked_public_surfaces and not args.scan_public_path:
        print("tool usage error: choose --diff-only, --all-tracked-public-surfaces, or --scan-public-path", file=sys.stderr)
        return 2
    try:
        repo = git_root()
        rules, allow_contexts = load_config(repo, args.config)
        candidates: list[Candidate] = []
        errors: list[str] = []
        if args.diff_only:
            diff_candidates, diff_errors = collect_diff_candidates(repo)
            candidates.extend(diff_candidates)
            errors.extend(diff_errors)
        if args.all_tracked_public_surfaces:
            candidates.extend(collect_tracked_candidates(repo))
        if args.scan_public_path:
            candidates.extend(collect_explicit_candidates(repo, args.scan_public_path))
        findings = scan_candidates(candidates, rules, allow_contexts)
        errors.extend(findings)
    except ScanError as exc:
        print(redact(str(exc)), file=sys.stderr)
        return exc.code
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        if args.debug:
            raise
        print(f"redacted tool failure: {redact(str(exc))}", file=sys.stderr)
        return 2
    emit_errors(errors)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
