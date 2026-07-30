#!/usr/bin/env python3
"""Validate ACE public-output artifacts for issue 63."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ace_public_output_contract import (  # noqa: E402
    DENY_LIST_PATH,
    OUTPUT_CONTRACT_PATH,
    SOURCE_HASH_SWEEP_PATH,
    validate_deny_list_file,
    validate_public_output_contract_file,
    validate_public_output_body_text,
    validate_public_output_paths,
    validate_source_hash_policy_sweep_file,
)


DEFAULT_PUBLIC_PATHS = [
    Path("docs/plans/2026-06-29-issue-63-ace-public-output-redaction-and-identifier-canary.md"),
    Path("docs/case-studies/ace-public-output-redaction-contract.md"),
    Path("artifacts/ace-source-hash-policy-sweep.md"),
    OUTPUT_CONTRACT_PATH,
    DENY_LIST_PATH,
    Path("scripts/ace_public_output_contract.py"),
    Path("scripts/validate_ace_public_artifacts.py"),
    Path("tests/test_validate_ace_public_artifacts.py"),
    Path("tests/fixtures/ace-public-artifact-safety/"),
    Path("docs/07-data-governance.md"),
    Path("docs/18-security-and-pii.md"),
    Path("docs/19-trust-boundary-and-private-mode.md"),
    Path("scripts/review/results/2026-07-02-implementation-63-contract-runtime-r1.md"),
    Path("scripts/review/results/2026-07-02-implementation-63-public-legal-r1.md"),
    Path("scripts/review/results/2026-07-02-implementation-63-governance-ci-r1.md"),
    Path("skills/public-private-routing/SKILL.md"),
    Path("skills/public-private-routing/evals/evals.json"),
    Path(".github/workflows/validate.yml"),
]


def collect_errors(
    *,
    scan_public_paths: list[Path] | None = None,
    issue_comment_body_files: list[Path] | None = None,
    contract_path: Path = OUTPUT_CONTRACT_PATH,
    deny_list_path: Path = DENY_LIST_PATH,
    source_hash_sweep_path: Path = SOURCE_HASH_SWEEP_PATH,
) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_public_output_contract_file(contract_path))
    errors.extend(validate_deny_list_file(deny_list_path))
    errors.extend(validate_source_hash_policy_sweep_file(source_hash_sweep_path))
    paths = scan_public_paths if scan_public_paths is not None else DEFAULT_PUBLIC_PATHS
    errors.extend(validate_public_output_paths(paths))
    for index, body_path in enumerate(issue_comment_body_files or [], start=1):
        try:
            body = Path(body_path).read_text()
        except OSError:
            errors.append(f"issue-comment-body-file: could not read body index {index}; path=REDACTED")
            continue
        errors.extend(validate_public_output_body_text(f"issue-comment-body-{index}.md", body))
    return _dedupe(errors)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=str(OUTPUT_CONTRACT_PATH), help="public-output contract JSON path")
    parser.add_argument("--deny-list", default=str(DENY_LIST_PATH), help="public deny-list supplement JSON path")
    parser.add_argument("--source-hash-sweep", default=str(SOURCE_HASH_SWEEP_PATH), help="source-hash policy sweep path")
    parser.add_argument("--scan-public-path", action="append", default=[], help="repo-local public artifact file/directory to scan")
    parser.add_argument("--issue-comment-body-file", action="append", default=[], help="planned issue comment body file to scan")
    args = parser.parse_args(argv)

    errors = collect_errors(
        scan_public_paths=[Path(path) for path in args.scan_public_path] if args.scan_public_path else None,
        issue_comment_body_files=[Path(path) for path in args.issue_comment_body_file],
        contract_path=Path(args.contract),
        deny_list_path=Path(args.deny_list),
        source_hash_sweep_path=Path(args.source_hash_sweep),
    )
    if errors:
        for error in errors:
            print(f"DENY  {error}", file=sys.stderr)
        print(f"\nFAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: ACE public-output artifact contract valid")
    return 0


def _dedupe(errors: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for error in errors:
        if error not in seen:
            seen.add(error)
            unique.append(error)
    return unique


if __name__ == "__main__":
    raise SystemExit(main())
