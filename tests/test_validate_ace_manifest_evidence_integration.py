from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from importlib import import_module


REPO_ROOT = Path(__file__).resolve().parents[1]
LIBRARY_PATH = REPO_ROOT / "scripts" / "ace_bounded_sampling_firewall.py"
TRUST_PATH = REPO_ROOT / "scripts" / "ace_manifest_evidence_trust.py"
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "ace-manifest-freshness" / "valid-operational-evidence.json"
ARTIFACT_ROOT = REPO_ROOT / "artifacts" / "ace-manifest-freshness"
RUNTIME_ARTIFACT = ARTIFACT_ROOT / "issue-70-runtime-test-evidence.json"
RUNTIME_REGISTRY = ARTIFACT_ROOT / "issue-70-runtime-test-registry.json"
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "validate.yml"
ISSUE_COMMENT_URL = "https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/62#issuecomment-4860000000"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_library():
    return load_module(LIBRARY_PATH, "ace_bounded_sampling_firewall_issue70")


def load_trust():
    return load_module(TRUST_PATH, "ace_manifest_evidence_trust_issue70")


def base_downstream_request() -> dict:
    request = {
        "target_issue": 52,
        "manifest_source": "INDEX.md",
        "seed_id": "ace_seed_issue_70_downstream_v1",
        "sort_rule": {
            "strategy": "stable_private_term_order",
            "term_refs": ["source_id"],
            "direction": "ascending",
            "tie_breaker": "public_manifest_row_ordinal",
        },
        "per_bucket_row_cap": 25,
        "max_files_touched": 5,
        "max_bytes_touched": 65536,
        "request_class": "downstream_manifest_backed_sampling",
        "requires_manifest_snapshot_id": True,
        "output_shape": "metadata_only_request_record",
        "route_target": "metadata_only",
        "logical_target_store": "metadata_ledger_store",
        "target_wave_class": "ingestion_wave",
    }
    return request


def fixture_pointer() -> dict:
    return {
        "source_issue": 62,
        "record_id": "ace62-compatible-fixture",
        "evidence_artifact_ref": "tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json",
    }


def operational_record(ref: str) -> dict:
    record = copy.deepcopy(json.loads(FIXTURE_PATH.read_text()))
    record["evidence_artifact_ref"] = ref
    record["validator_command"] = ["uv", "run", "python", "scripts/validate_ace_manifest_freshness.py", "--evidence", ref]
    return record


def registry_row(record: dict, raw: bytes, digest: str | None = None) -> dict:
    return {
        "record_id": record["record_id"],
        "evidence_artifact_ref": record["evidence_artifact_ref"],
        "artifact_integrity_digest": digest or hashlib.sha256(raw).hexdigest(),
        "reviewed_commit": record["reviewed_commit"],
        "validator_ref": record["validator_ref"],
        "validator_command": record["validator_command"],
        "validator_exit_status": record["validator_exit_status"],
        "issue_evidence_comment_url": ISSUE_COMMENT_URL,
    }


def write_json(path: Path, value: dict) -> bytes:
    raw = (json.dumps(value, indent=2) + "\n").encode()
    path.write_bytes(raw)
    return raw


def write_registry(rows: list[dict]) -> None:
    write_json(
        RUNTIME_REGISTRY,
        {
            "registry_schema_version": "1.0.0",
            "owner_issue": 70,
            "consumer_issue": 67,
            "evidence_source_issue": 62,
            "trusted_evidence": rows,
        },
    )


class AceManifestEvidenceIntegrationTests(unittest.TestCase):
    def tearDown(self):
        RUNTIME_ARTIFACT.unlink(missing_ok=True)
        RUNTIME_REGISTRY.unlink(missing_ok=True)

    def request_with_pointer(self, pointer: dict) -> dict:
        request = base_downstream_request()
        request["snapshot_evidence"] = pointer
        return request

    def test_70_imports_62_pointer_fields_and_validator(self):
        trust = load_trust()
        operational = import_module("ace_manifest_freshness_operational")
        self.assertIs(trust.REQUEST_POINTER_FIELDS, operational.REQUEST_POINTER_FIELDS)
        self.assertIs(trust.validate_operational_evidence, operational.validate_operational_evidence)

    def test_missing_62_pointer_fails_closed(self):
        library = load_library()
        result = library.validate_sampling_request(base_downstream_request())
        self.assertFalse(result.authorized)
        self.assertEqual("MISSING_62_EVIDENCE_POINTER", result.reason_code)
        self.assertEqual(62, result.blocked_by_issue)
        self.assertEqual(70, result.follow_on_issue)

    def test_self_attested_62_evidence_body_fails_closed(self):
        library = load_library()
        pointer = fixture_pointer()
        pointer["validator_command"] = ["uv", "run", "python", "scripts/validate_ace_manifest_freshness.py"]
        result = library.validate_sampling_request(self.request_with_pointer(pointer))
        self.assertFalse(result.authorized)
        self.assertEqual("SELF_ATTESTED_62_EVIDENCE", result.reason_code)

    def test_fixture_62_evidence_cannot_authorize_operational_sampling(self):
        library = load_library()
        result = library.validate_sampling_request(self.request_with_pointer(fixture_pointer()))
        self.assertFalse(result.authorized)
        self.assertEqual("FIXTURE_62_EVIDENCE_NOT_OPERATIONAL", result.reason_code)

    def test_schema_valid_but_untrusted_operational_artifact_fails_closed(self):
        library = load_library()
        ref = "artifacts/ace-manifest-freshness/issue-70-runtime-test-evidence.json"
        record = operational_record(ref)
        write_json(RUNTIME_ARTIFACT, record)
        pointer = {"source_issue": 62, "record_id": record["record_id"], "evidence_artifact_ref": ref}
        result = library.validate_sampling_request(self.request_with_pointer(pointer))
        self.assertFalse(result.authorized)
        self.assertEqual("UNTRUSTED_62_EVIDENCE", result.reason_code)

    def test_trusted_registry_allows_only_matching_raw_digest(self):
        trust = load_trust()
        ref = "artifacts/ace-manifest-freshness/issue-70-runtime-test-evidence.json"
        record = operational_record(ref)
        raw = write_json(RUNTIME_ARTIFACT, record)
        pointer = {"source_issue": 62, "record_id": record["record_id"], "evidence_artifact_ref": ref}
        write_registry([registry_row(record, raw)])
        self.assertTrue(trust.validate_trusted_62_evidence_pointer(pointer, RUNTIME_REGISTRY).authorized)

        mutated = json.dumps(record, separators=(",", ":")).encode()
        RUNTIME_ARTIFACT.write_bytes(mutated)
        stale = trust.validate_trusted_62_evidence_pointer(pointer, RUNTIME_REGISTRY)
        self.assertFalse(stale.authorized)
        self.assertEqual("UNTRUSTED_62_EVIDENCE", stale.reason_code)
        self.assertIn("artifact_integrity_digest", "\n".join(stale.errors))

    def test_symlinked_operational_artifact_to_fixture_cannot_authorize(self):
        trust = load_trust()
        ref = "artifacts/ace-manifest-freshness/issue-70-symlink-evidence.json"
        link = REPO_ROOT / ref
        target = REPO_ROOT / "tests" / "fixtures" / "ace-manifest-freshness" / "issue-70-symlink-target.json"
        record = operational_record(ref)
        raw = write_json(target, record)
        link.unlink(missing_ok=True)
        link.symlink_to(Path("../../tests/fixtures/ace-manifest-freshness/issue-70-symlink-target.json"))
        self.addCleanup(lambda: link.is_symlink() and link.unlink())
        self.addCleanup(lambda: target.exists() and target.unlink())
        write_registry([registry_row(record, raw)])
        pointer = {"source_issue": 62, "record_id": record["record_id"], "evidence_artifact_ref": ref}
        result = trust.validate_trusted_62_evidence_pointer(pointer, RUNTIME_REGISTRY)
        self.assertFalse(result.authorized)
        self.assertIn(result.reason_code, {"INVALID_62_EVIDENCE_POINTER", "UNTRUSTED_62_EVIDENCE"})
        self.assertIn("symlink", "\n".join(result.errors))

    def test_blocked_reconciliation_evidence_does_not_authorize_sampling(self):
        trust = load_trust()
        ref = "artifacts/ace-manifest-freshness/issue-70-runtime-test-evidence.json"
        record = operational_record(ref)
        pair = record["drift_verdicts_by_manifest_source_pair"]["inventory_to_assets_presence"]
        pair["drift_severity"] = "warning"
        pair["reconciliation_required"] = True
        record["authorization_status"] = "blocked_requires_reconciliation"
        record["reconciliation_refs"] = {"inventory_to_assets_presence": [ISSUE_COMMENT_URL]}
        raw = write_json(RUNTIME_ARTIFACT, record)
        write_registry([registry_row(record, raw)])
        pointer = {"source_issue": 62, "record_id": record["record_id"], "evidence_artifact_ref": ref}
        result = trust.validate_trusted_62_evidence_pointer(pointer, RUNTIME_REGISTRY)
        self.assertFalse(result.authorized)
        self.assertEqual("62_EVIDENCE_NOT_AUTHORIZING", result.reason_code)

    def test_registry_requires_issue_62_evidence_comment_url(self):
        trust = load_trust()
        ref = "artifacts/ace-manifest-freshness/issue-70-runtime-test-evidence.json"
        record = operational_record(ref)
        raw = write_json(RUNTIME_ARTIFACT, record)
        row = registry_row(record, raw)
        row["issue_evidence_comment_url"] = row["issue_evidence_comment_url"].replace("/issues/62", "/issues/70")
        write_registry([row])
        pointer = {"source_issue": 62, "record_id": record["record_id"], "evidence_artifact_ref": ref}
        result = trust.validate_trusted_62_evidence_pointer(pointer, RUNTIME_REGISTRY)
        self.assertFalse(result.authorized)
        self.assertEqual("UNTRUSTED_62_EVIDENCE", result.reason_code)
        self.assertIn("issue 62", "\n".join(result.errors))

    def test_70_public_scan_paths_include_registry_plan_review_and_tests(self):
        trust = load_trust()
        paths = {path.as_posix() for path in trust.issue_70_public_scan_paths()}
        expected = {
            "docs/plans/2026-07-01-issue-70-ace-67-62-manifest-evidence-contract-integration.md",
            "artifacts/ace-manifest-freshness/trusted-evidence-registry.json",
            "scripts/ace_manifest_evidence_trust.py",
            "tests/test_validate_ace_manifest_evidence_integration.py",
        }
        self.assertTrue(expected <= paths)

    def test_ci_runs_70_integration_tests_and_public_scan_paths(self):
        workflow = WORKFLOW_PATH.read_text()
        self.assertIn("uv run python -m unittest tests.test_validate_ace_manifest_evidence_integration", workflow)
        self.assertIn("--scan-public-path scripts/ace_manifest_evidence_trust.py", workflow)
        self.assertIn("--scan-public-path artifacts/ace-manifest-freshness/trusted-evidence-registry.json", workflow)


if __name__ == "__main__":
    unittest.main()
