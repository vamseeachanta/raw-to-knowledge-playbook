from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_manifest_freshness.py"
VALID_OPERATIONAL_FIXTURE = (
    REPO_ROOT / "tests" / "fixtures" / "ace-manifest-freshness" / "valid-operational-evidence.json"
)


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_ace_manifest_freshness", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_valid_operational_evidence() -> dict:
    return json.loads(VALID_OPERATIONAL_FIXTURE.read_text())


class AceManifestFreshnessSecurityTests(unittest.TestCase):
    def test_validator_env_is_separate_from_argv(self):
        validator = load_validator()
        record = load_valid_operational_evidence()

        mutated = copy.deepcopy(record)
        mutated["validator_env"] = {}
        mutated["validator_command"] = ["UV_CACHE_DIR=.claude/state/uv-cache", *record["validator_command"]]
        self.assertIn("validator_env", "\n".join(validator.validate_operational_evidence(mutated)))

    def test_validator_command_is_closed(self):
        validator = load_validator()
        record = load_valid_operational_evidence()
        mutated = copy.deepcopy(record)
        mutated["validator_command"] = [
            "uv",
            "run",
            "python",
            "scripts/validate_ace_manifest_freshness.py",
            "--contract",
            "other.json",
            "--evidence",
            "tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json",
        ]

        self.assertIn("validator_command", "\n".join(validator.validate_operational_evidence(mutated)))

    def test_operational_request_pointer_is_minimal(self):
        validator = load_validator()
        pointer = {
            "source_issue": 62,
            "record_id": "ace62-compatible-fixture",
            "evidence_artifact_ref": "tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json",
        }

        self.assertEqual([], validator.validate_request_pointer(pointer))

        mutated = copy.deepcopy(pointer)
        mutated["validator_command"] = ["uv", "run", "python", "scripts/validate_ace_manifest_freshness.py"]
        self.assertIn("minimal pointer", "\n".join(validator.validate_request_pointer(mutated)))

    def test_forged_or_self_attested_operational_evidence_fails(self):
        validator = load_validator()
        pointer = {
            "source_issue": 62,
            "record_id": "ace62-forged-fixture",
            "evidence_artifact_ref": "tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json",
        }

        self.assertIn("referenced artifact", "\n".join(validator.validate_request_pointer(pointer)))

    def test_non_object_operational_evidence_fails_closed(self):
        validator = load_validator()

        for record in ([], "not-object"):
            self.assertIn("operational evidence", "\n".join(validator.validate_operational_evidence(record)))

    def test_request_pointer_rejects_symlink_escape(self):
        validator = load_validator()
        outside_ref = copy.deepcopy(load_valid_operational_evidence())
        outside_ref["evidence_artifact_ref"] = "tests/fixtures/ace-manifest-freshness/link.json"
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "outside.json"
            outside.write_text(json.dumps(outside_ref))
            link = REPO_ROOT / "tests" / "fixtures" / "ace-manifest-freshness" / "link.json"
            if link.exists() or link.is_symlink():
                link.unlink()
            link.symlink_to(outside)
            self.addCleanup(lambda: (link.exists() or link.is_symlink()) and link.unlink())
            pointer = {
                "source_issue": 62,
                "record_id": "ace62-compatible-fixture",
                "evidence_artifact_ref": "tests/fixtures/ace-manifest-freshness/link.json",
            }
            errors = "\n".join(validator.validate_request_pointer(pointer))

        self.assertIn("referenced artifact", errors)

    def test_request_pointer_rejects_non_object_artifact_without_crash(self):
        validator = load_validator()
        ref = "tests/fixtures/ace-manifest-freshness/non-object-pointer.json"
        artifact = REPO_ROOT / ref
        if artifact.exists():
            artifact.unlink()
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())
        artifact.write_text("[]\n")
        pointer = {
            "source_issue": 62,
            "record_id": "ace62-compatible-fixture",
            "evidence_artifact_ref": ref,
        }

        self.assertIn("operational evidence", "\n".join(validator.validate_request_pointer(pointer)))


    def test_reconciliation_refs_are_required_for_noncompatible_pairs(self):
        validator = load_validator()
        mutated = self.warning_record()

        self.assertIn("reconciliation_refs", "\n".join(validator.validate_operational_evidence(mutated)))

        mutated["reconciliation_refs"] = {
            "assets_to_master_records": ["https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/70"]
        }
        self.assertEqual([], validator.validate_operational_evidence(mutated))

    def test_reconciliation_refs_reject_invalid_refs(self):
        validator = load_validator()
        mutated = self.warning_record()
        mutated["reconciliation_refs"] = {
            "assets_to_master_records": ["/" + "mnt" + "/ace/private"]
        }
        self.assertIn("reconciliation_refs", "\n".join(validator.validate_operational_evidence(mutated)))

        mutated["reconciliation_refs"] = {
            "assets_to_master_records": [
                "https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/not-a-number"
            ]
        }
        self.assertIn("reconciliation_refs", "\n".join(validator.validate_operational_evidence(mutated)))

        mutated["reconciliation_refs"] = {
            "assets_to_master_records": ["docs/does-not-exist.md"]
        }
        self.assertIn("reconciliation_refs", "\n".join(validator.validate_operational_evidence(mutated)))

    def test_evidence_file_rejects_absolute_paths(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            absolute = Path(tmp) / "evidence.json"
            absolute.write_text(VALID_OPERATIONAL_FIXTURE.read_text())
            errors = "\n".join(validator.validate_operational_evidence_file(absolute))

        self.assertIn("operational evidence path", errors)

    def test_non_object_pair_verdict_fails_closed(self):
        validator = load_validator()
        record = load_valid_operational_evidence()
        mutated = copy.deepcopy(record)
        mutated["drift_verdicts_by_manifest_source_pair"]["assets_to_master_records"] = 1

        self.assertIn("pair verdict for assets_to_master_records", "\n".join(validator.validate_operational_evidence(mutated)))

    def test_compatible_record_rejects_unneeded_reconciliation_refs(self):
        validator = load_validator()
        record = load_valid_operational_evidence()
        mutated = copy.deepcopy(record)
        mutated["reconciliation_refs"] = {
            "assets_to_master_records": ["docs/case-studies/ace-manifest-freshness-drift-sentinel.md"]
        }

        self.assertIn("reconciliation_refs", "\n".join(validator.validate_operational_evidence(mutated)))

    def warning_record(self) -> dict:
        mutated = copy.deepcopy(load_valid_operational_evidence())
        pair = mutated["drift_verdicts_by_manifest_source_pair"]["assets_to_master_records"]
        pair["drift_severity"] = "warning"
        pair["reconciliation_required"] = True
        mutated["authorization_status"] = "blocked_requires_reconciliation"
        return mutated


if __name__ == "__main__":
    unittest.main()
