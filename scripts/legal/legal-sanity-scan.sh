#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
exec "${PYTHON:-python3}" "$REPO_ROOT/scripts/legal/legal_sanity_scan.py" "$@"
