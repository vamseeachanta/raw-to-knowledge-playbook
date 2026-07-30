#!/usr/bin/env python3
"""Validate the ACE public token fixture contract for issue 66."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ace_public_token_fixtures import (  # noqa: E402
    CONTRACT_PATH,
    GOOD_FIXTURE_PATH,
    public_scan_paths,
    validate_contract_file,
    validate_fixture,
    validate_fixture_file,
    validate_public_surfaces,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", default=str(CONTRACT_PATH), help="fixture contract JSON path")
    parser.add_argument("--fixture", action="append", default=[], help="fixture request JSON path")
    args = parser.parse_args(argv)

    errors = validate_contract_file(Path(args.contract))
    fixture_paths = args.fixture or [str(GOOD_FIXTURE_PATH)]
    for fixture_path in fixture_paths:
        errors.extend(validate_fixture_file(Path(fixture_path)))
    errors.extend(validate_public_surfaces(public_scan_paths()))

    if errors:
        for error in errors:
            print(f"DENY  {error}", file=sys.stderr)
        print(f"\nFAIL: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: ACE public token fixture contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
