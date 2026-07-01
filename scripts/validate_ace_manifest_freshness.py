#!/usr/bin/env python3
"""Validate the ACE manifest freshness contract for issue 62."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ace_manifest_freshness_contract import (  # noqa: E402
    CONTRACT_PATH,
    EXPECTED_PAIR_SOURCES,
    collect_manifest_status,
    is_snapshot_id,
    load_contract,
    public_scan_paths,
    validate_contract,
    validate_contract_file,
    validate_operation_is_bounded,
    validate_public_surfaces,
    validate_wave0_schema_dependency,
)
from ace_manifest_freshness_emit import (  # noqa: E402
    build_operational_evidence_record,
    emit_operational_evidence,
)
from ace_manifest_freshness_operational import (  # noqa: E402
    validate_operational_evidence,
    validate_operational_evidence_file,
    validate_request_pointer,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=str(CONTRACT_PATH), help="contract JSON path")
    parser.add_argument("--evidence", action="append", default=[], help="operational evidence JSON path")
    parser.add_argument("--emit-evidence", help="write an operational evidence JSON artifact")
    parser.add_argument("--share-root", help="source root for --emit-evidence; defaults to ACE_SHARE_ROOT")
    parser.add_argument("--reviewed-commit", help="reviewed commit SHA for emitted evidence")
    args = parser.parse_args(argv)
    errors = validate_contract_file(Path(args.contract))
    if args.emit_evidence:
        share_root = args.share_root or os.environ.get("ACE_SHARE_ROOT")
        if not share_root:
            errors.append("--emit-evidence requires --share-root or ACE_SHARE_ROOT")
        if not args.reviewed_commit:
            errors.append("--emit-evidence requires --reviewed-commit")
        if not errors:
            errors.extend(
                emit_operational_evidence(
                    Path(share_root),
                    args.emit_evidence,
                    reviewed_commit=args.reviewed_commit,
                )
            )
    for evidence_path in args.evidence:
        errors.extend(validate_operational_evidence_file(Path(evidence_path)))
    errors.extend(validate_public_surfaces())
    if errors:
        for error in errors:
            print(f"DENY  {error}", file=sys.stderr)
        print(f"\nFAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: ACE manifest freshness contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
