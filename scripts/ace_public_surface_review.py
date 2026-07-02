"""Review artifact and issue/comment snapshot scanning for ACE issue 68."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

try:
    from .ace_public_surface_contract import (
        CONTRACT_PATH, MANIFEST_CONTRACT_PATH, REVIEW_ARTIFACT_RE, REVIEW_PHASES, REVIEW_ROOT, ROUND_RE,
        SEMVER_RE, SIDECAR_SUFFIXES, SNAPSHOT_KEYS, SNAPSHOT_PAIRINGS, SNAPSHOT_PHASES,
        SNAPSHOT_SOURCE_KINDS, EXPECTED_PROVIDERS, _imported_token_values, load_json, repo_path,
    )
    from .ace_public_surface_rules import (
        _allowed_metadata_evidence_paths, _scan_line, validate_public_artifact_paths,
    )
except ImportError:
    from ace_public_surface_contract import (
        CONTRACT_PATH, MANIFEST_CONTRACT_PATH, REVIEW_ARTIFACT_RE, REVIEW_PHASES, REVIEW_ROOT, ROUND_RE,
        SEMVER_RE, SIDECAR_SUFFIXES, SNAPSHOT_KEYS, SNAPSHOT_PAIRINGS, SNAPSHOT_PHASES,
        SNAPSHOT_SOURCE_KINDS, EXPECTED_PROVIDERS, _imported_token_values, load_json, repo_path,
    )
    from ace_public_surface_rules import (
        _allowed_metadata_evidence_paths, _scan_line, validate_public_artifact_paths,
    )


def validate_review_artifacts(
    *,
    review_issue: int,
    phase: str,
    provider: str,
    round_id: str,
    include_sidecars: bool = False,
    sidecar_required: bool = False,
    review_root: Path = REVIEW_ROOT,
    contract_path: Path = CONTRACT_PATH,
) -> list[str]:
    selected, errors = select_review_artifact_paths(
        review_issue=review_issue,
        phase=phase,
        provider=provider,
        round_id=round_id,
        include_sidecars=include_sidecars,
        sidecar_required=sidecar_required,
        review_root=review_root,
    )
    if errors:
        return errors
    return validate_public_artifact_paths(selected, contract_path=contract_path)


def validate_issue_comment_snapshot_file(path: Path, contract_path: Path = CONTRACT_PATH) -> list[str]:
    snapshot, errors = _load_snapshot(path)
    if errors:
        return errors
    errors.extend(_validate_snapshot_record(snapshot, path))
    if not errors:
        errors.extend(_scan_snapshot_body(snapshot, path, contract_path))
    return errors


def validate_issue_comment_snapshot_pair(
    pre_path: Path,
    post_path: Path,
    contract_path: Path = CONTRACT_PATH,
) -> list[str]:
    errors = validate_issue_comment_snapshot_file(pre_path, contract_path)
    errors.extend(validate_issue_comment_snapshot_file(post_path, contract_path))
    if errors:
        return errors
    pre, _ = _load_snapshot(pre_path)
    post, _ = _load_snapshot(post_path)
    return _validate_snapshot_pair(pre, post, post_path)


def select_review_artifact_paths(
    *,
    review_issue: int,
    phase: str,
    provider: str,
    round_id: str,
    include_sidecars: bool = False,
    sidecar_required: bool = False,
    review_root: Path = REVIEW_ROOT,
) -> tuple[list[Path], list[str]]:
    errors = _validate_review_selector(review_issue, phase, provider, round_id)
    root, root_errors = _bounded_review_root(review_root)
    errors.extend(root_errors)
    if root.is_symlink():
        errors.append(f"review-root-symlink: {root}")
    if errors:
        return [], errors
    if not root.exists():
        return [], [f"missing review root: {review_root}"]
    selected, select_errors = _select_review_markdown(root, review_issue, phase, provider, round_id)
    errors.extend(select_errors)
    if selected and include_sidecars:
        selected, sidecar_errors = _with_sidecars(selected, sidecar_required)
        errors.extend(sidecar_errors)
    return selected, errors


def _load_snapshot(path: Path) -> tuple[dict, list[str]]:
    try:
        payload = json.loads(repo_path(path).read_text())
    except FileNotFoundError:
        return {}, [f"snapshot-missing: {path}"]
    except json.JSONDecodeError as exc:
        return {}, [f"snapshot-json: invalid JSON at {path}: {exc}"]
    if not isinstance(payload, dict):
        return {}, [f"snapshot-record: expected object at {path}"]
    return payload, []


def _validate_snapshot_record(snapshot: dict, path: Path) -> list[str]:
    errors: list[str] = []
    if list(snapshot) != SNAPSHOT_KEYS:
        errors.append(f"snapshot-keys: top-level keys must match contract at {path}")
    if not SEMVER_RE.fullmatch(str(snapshot.get("schema_version", ""))):
        errors.append(f"snapshot-version: schema_version must use 1.0.x at {path}")
    if snapshot.get("source_kind") not in SNAPSHOT_SOURCE_KINDS:
        errors.append(f"snapshot-source-kind: unknown source_kind at {path}")
    if snapshot.get("phase") not in SNAPSHOT_PHASES:
        errors.append(f"snapshot-phase: unknown phase at {path}")
    if snapshot.get("issue_number") != 68:
        errors.append(f"snapshot-issue: issue_number must be 68 at {path}")
    errors.extend(_validate_snapshot_phase_shape(snapshot, path))
    if _body_hash(snapshot.get("body", "")) != snapshot.get("body_sha256"):
        errors.append(f"snapshot-body-hash: body_sha256 does not match body at {path}")
    return errors


def _validate_snapshot_phase_shape(snapshot: dict, path: Path) -> list[str]:
    errors: list[str] = []
    if snapshot.get("phase") == "pre_post" and snapshot.get("comment_id") is not None:
        errors.append(f"snapshot-comment-id: pre_post comment_id must be null at {path}")
    if snapshot.get("phase") == "post_refetch" and snapshot.get("source_kind") == "issue_comment":
        if snapshot.get("comment_id") is None:
            errors.append(f"snapshot-comment-id: refetched issue_comment needs comment_id at {path}")
        errors.extend(_validate_github_comment_url(snapshot, path))
    if snapshot.get("source_kind") == "planned_comment":
        errors.extend(_validate_github_issue_url(snapshot, path))
    if snapshot.get("source_kind") == "issue_body":
        errors.extend(_validate_github_issue_url(snapshot, path))
    return errors


def _validate_github_comment_url(snapshot: dict, path: Path) -> list[str]:
    parsed = urlparse(str(snapshot.get("url", "")))
    issue = 68
    comment_id = snapshot.get("comment_id")
    expected_path = f"/vamseeachanta/raw-to-knowledge-playbook/issues/{issue}"
    expected_fragment = f"issuecomment-{comment_id}"
    if (
        parsed.scheme != "https"
        or parsed.netloc != "github.com"
        or parsed.path != expected_path
        or parsed.params
        or parsed.query
        or parsed.fragment != expected_fragment
    ):
        return [f"snapshot-url: refetched issue_comment URL mismatch at {path}"]
    return []


def _validate_github_issue_url(snapshot: dict, path: Path) -> list[str]:
    parsed = urlparse(str(snapshot.get("url", "")))
    issue = 68
    expected_path = f"/vamseeachanta/raw-to-knowledge-playbook/issues/{issue}"
    if (
        parsed.scheme != "https"
        or parsed.netloc != "github.com"
        or parsed.path != expected_path
        or parsed.params
        or parsed.query
        or parsed.fragment
    ):
        return [f"snapshot-url: issue_body URL mismatch at {path}"]
    return []


def _scan_snapshot_body(snapshot: dict, path: Path, contract_path: Path) -> list[str]:
    contract = load_json(contract_path)
    token_contract = _imported_token_values(contract)
    metadata_paths = _allowed_metadata_evidence_paths(MANIFEST_CONTRACT_PATH)
    errors: list[str] = []
    for line_number, line in enumerate(str(snapshot.get("body", "")).splitlines(), start=1):
        errors.extend(_scan_line(path, line_number, line, token_contract, metadata_paths))
    return errors


def _validate_snapshot_pair(pre: dict, post: dict, post_path: Path) -> list[str]:
    errors: list[str] = []
    pair = (pre.get("source_kind"), post.get("source_kind"))
    if pre.get("phase") != "pre_post" or post.get("phase") != "post_refetch":
        errors.append(f"snapshot-pair-phase: invalid pre/post phases for {post_path}")
    if pair not in SNAPSHOT_PAIRINGS:
        errors.append(f"snapshot-pair-source-kind: invalid source_kind transition for {post_path}")
    if pre.get("issue_number") != post.get("issue_number"):
        errors.append(f"snapshot-pair-issue: issue_number mismatch for {post_path}")
    if pre.get("body_sha256") != post.get("body_sha256"):
        errors.append(f"snapshot-pair-body-hash: body hash mismatch for {post_path}")
    return errors


def _body_hash(body: str) -> str:
    return hashlib.sha256(str(body).encode()).hexdigest()


def _validate_review_selector(review_issue: int, phase: str, provider: str, round_id: str) -> list[str]:
    errors: list[str] = []
    if review_issue != 68:
        errors.append("review-issue: #68 scanner accepts only issue 68 selectors")
    if phase not in REVIEW_PHASES:
        errors.append(f"review-phase: unknown phase {phase!r}")
    if provider not in EXPECTED_PROVIDERS:
        errors.append(f"review-provider: unknown provider {provider!r}")
    if not ROUND_RE.fullmatch(round_id):
        errors.append(f"review-round: invalid round {round_id!r}")
    return errors


def _select_review_markdown(
    root: Path,
    issue: int,
    phase: str,
    provider: str,
    round_id: str,
) -> tuple[list[Path], list[str]]:
    pattern = f"????-??-??-{phase}-{issue}-{provider}-{round_id}.md"
    matches = [path for path in sorted(root.glob(pattern)) if _review_name_matches(path.name, phase, provider, round_id)]
    errors: list[str] = []
    if not matches:
        return [], [f"review-artifact-missing: {pattern}"]
    for path in matches:
        if path.is_symlink():
            errors.append(f"review-artifact-symlink: {path}")
    return ([] if errors else matches), errors


def _review_name_matches(name: str, phase: str, provider: str, round_id: str) -> bool:
    match = REVIEW_ARTIFACT_RE.fullmatch(name)
    return bool(
        match
        and match.group("phase") == phase
        and match.group("provider") == provider
        and match.group("round") == round_id
    )


def _with_sidecars(paths: list[Path], sidecar_required: bool) -> tuple[list[Path], list[str]]:
    selected = list(paths)
    errors: list[str] = []
    for path in paths:
        sidecars = _existing_sidecars(path)
        if not sidecars and sidecar_required:
            errors.append(f"sidecar-required: no same-stem sidecar for {path}")
        selected.extend(sidecars)
    return selected, errors


def review_sidecar_status(
    *,
    review_issue: int,
    phase: str,
    provider: str,
    round_id: str,
) -> str:
    selected, errors = select_review_artifact_paths(
        review_issue=review_issue,
        phase=phase,
        provider=provider,
        round_id=round_id,
    )
    if errors:
        return "sidecar_status=selector_error"
    return "sidecar_status=present" if any(_existing_sidecars(path) for path in selected) else "sidecar_status=none_found"


def _existing_sidecars(path: Path) -> list[Path]:
    sidecars = []
    for suffix in sorted(SIDECAR_SUFFIXES):
        candidate = path.with_suffix(suffix)
        if candidate.exists():
            sidecars.append(candidate)
    return sidecars


def _bounded_review_root(review_root: Path) -> tuple[Path, list[str]]:
    root = repo_path(review_root)
    expected = repo_path(REVIEW_ROOT).resolve()
    try:
        if root.resolve() != expected:
            return root, [f"review-root: expected {REVIEW_ROOT}"]
    except FileNotFoundError:
        return root, [f"review-root: missing {review_root}"]
    return root, []
