#!/usr/bin/env python3
"""Validate the ACE public-surface self-scan contract."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ace_public_surface_scan import (  # noqa: E402
    CONTRACT_PATH,
    review_sidecar_status,
    select_review_artifact_paths,
    validate_contract,
    validate_contract_file,
    validate_issue_comment_snapshot_file,
    validate_issue_comment_snapshot_pair,
    validate_public_artifact_paths,
    validate_review_artifacts,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=str(CONTRACT_PATH), help="public-surface scan contract JSON path")
    parser.add_argument(
        "--scan-public-path",
        action="append",
        default=[],
        help="repo-local public artifact file/directory to scan",
    )
    parser.add_argument("--review-issue", type=int, help="review artifact issue selector")
    parser.add_argument("--review-phase", choices=["plan", "implementation"], help="review artifact phase selector")
    parser.add_argument("--review-provider", help="review artifact provider selector")
    parser.add_argument("--review-round", help="review artifact round selector, e.g. r3")
    parser.add_argument("--review-root", default="scripts/review/results", help="review artifact root")
    parser.add_argument("--include-sidecars", action="store_true", help="scan same-stem review sidecars")
    parser.add_argument("--sidecar-required", action="store_true", help="fail when selected review sidecars are absent")
    parser.add_argument("--snapshot", action="append", default=[], help="issue/comment body snapshot JSON to scan")
    parser.add_argument(
        "--snapshot-pair",
        nargs=2,
        action="append",
        default=[],
        metavar=("PRE_POST", "POST_REFETCH"),
        help="validate a pre-post/refetched snapshot pair",
    )
    args = parser.parse_args(argv)

    errors = collect_errors(args)
    if errors:
        for error in errors:
            print(f"DENY  {error}", file=sys.stderr)
        print(f"\nFAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: ACE public-surface scan contract valid")
    return 0


def collect_errors(args: argparse.Namespace) -> list[str]:
    contract_path = Path(args.contract)
    errors = validate_contract_file(contract_path)
    paths = [Path(item) for item in args.scan_public_path]
    errors.extend(validate_public_artifact_paths(paths, contract_path=contract_path))
    if args.review_issue or args.review_phase or args.review_provider or args.review_round:
        if not all([args.review_issue, args.review_phase, args.review_provider, args.review_round]):
            errors.append("review selector requires --review-issue, --review-phase, --review-provider, and --review-round")
        else:
            errors.extend(
                validate_review_artifacts(
                    review_issue=args.review_issue,
                    phase=args.review_phase,
                    provider=args.review_provider,
                    round_id=args.review_round,
                    include_sidecars=args.include_sidecars,
                    sidecar_required=args.sidecar_required,
                    review_root=Path(args.review_root),
                    contract_path=contract_path,
                )
            )
    for snapshot in args.snapshot:
        errors.extend(validate_issue_comment_snapshot_file(Path(snapshot), contract_path))
    for pre_post, post_refetch in args.snapshot_pair:
        errors.extend(validate_issue_comment_snapshot_pair(Path(pre_post), Path(post_refetch), contract_path))
    return errors


if __name__ == "__main__":
    raise SystemExit(main())
