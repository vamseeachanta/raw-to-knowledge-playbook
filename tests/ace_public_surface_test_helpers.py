from __future__ import annotations

import importlib.util
import hashlib
import json
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_public_surface_scan.py"
CONTRACT_PATH = REPO_ROOT / "config" / "ace-public-surface-self-scan-contract.json"
TOKEN_CONTRACT_PATH = REPO_ROOT / "config" / "ace-public-token-fixture-contract.json"
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "validate.yml"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_validator():
    return load_module(VALIDATOR_PATH, "validate_ace_public_surface_scan")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def private_path_text() -> str:
    return "/mnt" + "/ace/private/source.docx"


def personal_email_text() -> str:
    return "person" + "@example.com"


def confidential_text() -> str:
    return "PROPRIETARY " + "CONFIDENTIAL payload"


def digest_value() -> str:
    return "0123456789abcdef" * 4


def public_token_value() -> str:
    return "pst_" + ("0123456789abcdef" * 2)


def allow_marker() -> str:
    return "ace-public-scan-" + "allow:"


def ace_root() -> str:
    return "ACE" + "_SHARE_ROOT"


def metadata_evidence_line(relative_path: str, kind: str) -> str:
    return f"EXISTS {ace_root()}/{relative_path} type={kind} details=withheld_public\n"


def write_tmp(tmp: str, name: str, text: str) -> Path:
    path = Path(tmp) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def repo_relative(path: Path) -> Path:
    return path.relative_to(REPO_ROOT)


@contextmanager
def repo_tmpdir():
    root = REPO_ROOT / "tests" / "fixtures" / "ace-public-surface-self-scan"
    root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".tmp-", dir=root) as tmp:
        yield Path(tmp)


def allow_start(context_id: str, token_class: str) -> str:
    return f"<!-- {allow_marker()}start context_id={context_id} token_class={token_class} -->"


def allow_end(context_id: str) -> str:
    return f"<!-- {allow_marker()}end context_id={context_id} -->"


def allowed_schema_term_block(*, context_id: str = "schema-term-policy-prose", token_class: str = "schema_term") -> str:
    return "\n".join(
        [
            "## Pseudocode",
            allow_start(context_id, token_class),
            "source_id",
            allow_end(context_id),
            "",
        ]
    )


def snapshot_record(
    *,
    body: str,
    source_kind: str,
    phase: str,
    issue_number: int = 68,
    comment_id=None,
    url: str = "https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68",
) -> dict:
    return {
        "schema_version": "1.0.0",
        "issue_number": issue_number,
        "comment_id": comment_id,
        "url": url,
        "source_kind": source_kind,
        "phase": phase,
        "fetched_at": "2026-07-02T00:00:00Z",
        "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
        "body": body,
    }
