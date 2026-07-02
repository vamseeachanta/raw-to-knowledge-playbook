"""Repo-local public-surface scanner facade for ACE issue 68."""
from __future__ import annotations

try:
    from .ace_public_surface_contract import (
        CONTRACT_PATH, MANIFEST_CONTRACT_PATH, REVIEW_ROOT, TOKEN_CONTRACT_PATH,
        load_json, repo_path, validate_contract, validate_contract_file,
    )
    from .ace_public_surface_review import (
        review_sidecar_status, select_review_artifact_paths, validate_issue_comment_snapshot_file,
        validate_issue_comment_snapshot_pair, validate_review_artifacts,
    )
    from .ace_public_surface_rules import validate_public_artifact_paths
except ImportError:
    from ace_public_surface_contract import (
        CONTRACT_PATH, MANIFEST_CONTRACT_PATH, REVIEW_ROOT, TOKEN_CONTRACT_PATH,
        load_json, repo_path, validate_contract, validate_contract_file,
    )
    from ace_public_surface_review import (
        review_sidecar_status, select_review_artifact_paths, validate_issue_comment_snapshot_file,
        validate_issue_comment_snapshot_pair, validate_review_artifacts,
    )
    from ace_public_surface_rules import validate_public_artifact_paths

__all__ = [
    "CONTRACT_PATH",
    "MANIFEST_CONTRACT_PATH",
    "REVIEW_ROOT",
    "TOKEN_CONTRACT_PATH",
    "load_json",
    "repo_path",
    "review_sidecar_status",
    "select_review_artifact_paths",
    "validate_contract",
    "validate_contract_file",
    "validate_issue_comment_snapshot_file",
    "validate_issue_comment_snapshot_pair",
    "validate_public_artifact_paths",
    "validate_review_artifacts",
]
