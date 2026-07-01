from __future__ import annotations

import importlib.util
import json
import copy
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = REPO_ROOT / "config" / "ace-manifest-evidence-contract.json"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_manifest_freshness.py"
SCHEMA_PATH = REPO_ROOT / "artifacts" / "ace-wave0-ledger-schema.json"
VALID_OPERATIONAL_FIXTURE = (
    REPO_ROOT / "tests" / "fixtures" / "ace-manifest-freshness" / "valid-operational-evidence.json"
)
EXPECTED_CORE_PUBLIC_PATHS = {
    "docs/plans/2026-06-29-issue-62-ace-manifest-freshness-and-drift-sentinel.md",
    "docs/plans/README.md",
    "docs/plans/ace-share-ingestion-wave-coordination.md",
    ".planning/plan-approved/62.md",
    "config/ace-manifest-evidence-contract.json",
    "scripts/validate_ace_manifest_freshness.py",
    "scripts/ace_manifest_freshness_contract.py",
    "scripts/ace_manifest_freshness_emit.py",
    "scripts/ace_manifest_freshness_operational.py",
    "tests/test_validate_ace_manifest_freshness.py",
    "tests/test_validate_ace_manifest_freshness_runtime.py",
    "tests/test_validate_ace_manifest_freshness_security.py",
    "tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json",
    "docs/case-studies/ace-manifest-freshness-drift-sentinel.md",
    "docs/16-corpus-lifecycle.md",
    ".github/workflows/validate.yml",
}
EXPECTED_MANIFEST_KEYS = [
    "INDEX.md",
    "assets.json",
    "docs/master-index.jsonl",
    "_cad-index/index-summary.json",
    "_cad-index/cad-readability-index.tsv",
    ".ace-knowledge/index.db",
]
EXPECTED_MANIFEST_ROLES = {
    "INDEX.md": "root_inventory_index",
    "assets.json": "asset_manifest",
    "docs/master-index.jsonl": "master_record_index",
    "_cad-index/index-summary.json": "cad_summary_index",
    "_cad-index/cad-readability-index.tsv": "cad_readability_index",
    ".ace-knowledge/index.db": "knowledge_store_index",
}
EXPECTED_PAIR_IDS = {
    "inventory_to_assets_presence",
    "assets_to_master_records",
    "master_records_to_cad_summary",
    "cad_summary_to_cad_readability",
    "master_records_to_knowledge_store",
}


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_ace_manifest_freshness", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text())


def load_valid_operational_evidence() -> dict:
    return json.loads(VALID_OPERATIONAL_FIXTURE.read_text())


class AceManifestFreshnessValidationTests(unittest.TestCase):
    def test_contract_is_json_and_owned_by_62(self):
        validator = load_validator()
        contract = load_contract()

        self.assertEqual([], validator.validate_contract(contract))
        self.assertEqual("ace-manifest-evidence-contract", contract["contract_id"])
        self.assertRegex(contract["contract_version"], r"^1\.0\.\d+$")
        self.assertEqual(62, contract["owner_issue"])
        self.assertEqual(65, contract["depends_on_schema_issue"])
        self.assertEqual(70, contract["downstream_consumer_issue"])

    def test_manifest_source_enum_matches_coordination(self):
        contract = load_contract()

        self.assertEqual(EXPECTED_MANIFEST_KEYS, contract["manifest_source_keys"])

    def test_manifest_source_roles_are_closed(self):
        contract = load_contract()

        self.assertEqual(EXPECTED_MANIFEST_ROLES, contract["manifest_source_roles"])

    def test_drift_eligible_pairs_are_closed(self):
        validator = load_validator()
        contract = load_contract()
        pair_ids = {pair["pair_id"] for pair in contract["drift_eligible_pairs"]}
        emitted_pairs = {pair["pair_id"]: (pair["left_source"], pair["right_source"]) for pair in contract["drift_eligible_pairs"]}

        self.assertEqual(EXPECTED_PAIR_IDS, pair_ids)
        self.assertEqual(validator.EXPECTED_PAIR_SOURCES, emitted_pairs)

        mutated = copy.deepcopy(contract)
        mutated["drift_eligible_pairs"][1]["left_source"] = "INDEX.md"
        self.assertIn("configured source pair", "\n".join(validator.validate_contract(mutated)))

    def test_imports_65_manifest_required_waves(self):
        validator = load_validator()
        contract = load_contract()

        self.assertEqual([], validator.validate_wave0_schema_dependency(contract, SCHEMA_PATH))

    def test_public_snapshot_id_is_opaque(self):
        validator = load_validator()
        record = load_valid_operational_evidence()

        for snapshot_id in record["snapshot_ids_by_manifest_source"].values():
            self.assertTrue(validator.is_snapshot_id(snapshot_id))
        self.assertFalse(validator.is_snapshot_id("assets-json-0000000000000000000000000001"))

    def test_operational_evidence_json_schema_is_closed_for_70(self):
        validator = load_validator()
        record = load_valid_operational_evidence()

        self.assertEqual([], validator.validate_operational_evidence(record))

        mutated = copy.deepcopy(record)
        mutated["extra_field"] = "not allowed"
        self.assertIn("closed root object", "\n".join(validator.validate_operational_evidence(mutated)))

    def test_operational_source_statuses_justify_pair_verdicts(self):
        validator = load_validator()
        record = load_valid_operational_evidence()

        mutated = copy.deepcopy(record)
        mutated["source_status_by_manifest_source"]["assets.json"]["content_fingerprint_status"] = "unavailable"
        self.assertIn("compatible pair", "\n".join(validator.validate_operational_evidence(mutated)))

    def test_unavailable_pair_blocks_authorization(self):
        validator = load_validator()
        record = load_valid_operational_evidence()
        mutated = copy.deepcopy(record)
        pair = mutated["drift_verdicts_by_manifest_source_pair"]["assets_to_master_records"]
        pair["drift_severity"] = "unavailable"
        pair["evidence_mode"] = "blocked_unavailable"
        pair["reconciliation_required"] = False

        self.assertIn("authorization_status", "\n".join(validator.validate_operational_evidence(mutated)))

    def test_drift_severity_evidence_mode_matrix_is_closed(self):
        validator = load_validator()
        record = load_valid_operational_evidence()
        mutated = copy.deepcopy(record)
        pair = mutated["drift_verdicts_by_manifest_source_pair"]["assets_to_master_records"]
        pair["evidence_mode"] = "missing_manifest"

        self.assertIn("illegal severity", "\n".join(validator.validate_operational_evidence(mutated)))

    def test_malformed_operational_maps_fail_closed(self):
        validator = load_validator()
        record = load_valid_operational_evidence()
        bad_snapshots = copy.deepcopy(record)
        bad_snapshots["snapshot_ids_by_manifest_source"] = []
        bad_statuses = copy.deepcopy(record)
        bad_statuses["source_status_by_manifest_source"] = []
        bad_verdicts = copy.deepcopy(record)
        bad_verdicts["drift_verdicts_by_manifest_source_pair"] = []

        snapshot_errors = "\n".join(validator.validate_operational_evidence(bad_snapshots))
        status_errors = "\n".join(validator.validate_operational_evidence(bad_statuses))
        verdict_errors = "\n".join(validator.validate_operational_evidence(bad_verdicts))

        self.assertIn("snapshot_ids_by_manifest_source", snapshot_errors)
        self.assertIn("source_status_by_manifest_source", status_errors)
        self.assertIn("drift verdicts", verdict_errors)

        bad_nested_status = copy.deepcopy(record)
        bad_nested_status["source_status_by_manifest_source"]["assets.json"] = 1
        nested_errors = "\n".join(validator.validate_operational_evidence(bad_nested_status))
        self.assertIn("source status for assets.json", nested_errors)

    def test_under_cap_manifest_can_be_fingerprinted_within_caps(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "assets.json"
            manifest.write_text("[{\"name\":\"synthetic\"}]\n")

            evidence = validator.collect_manifest_status(
                "assets.json",
                manifest,
                caps={"max_under_cap_bytes": 128, "max_under_cap_rows": 10},
                snapshot_id="ams_00000000000000000000000000000002",
            )

        self.assertEqual("available_under_cap", evidence["content_fingerprint_status"])
        self.assertEqual("available_under_cap", evidence["row_count_status"])
        self.assertEqual("public_safe_summary", evidence["evidence_mode"])
        self.assertNotIn("digest", json.dumps(evidence).lower())

    def test_large_manifest_without_sidecar_is_unavailable(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "assets.json"
            manifest.write_text("x" * 256)

            evidence = validator.collect_manifest_status(
                "assets.json",
                manifest,
                caps={"max_under_cap_bytes": 16, "max_under_cap_rows": 10},
                snapshot_id="ams_00000000000000000000000000000002",
            )

        self.assertEqual("unavailable", evidence["content_fingerprint_status"])
        self.assertEqual("unavailable", evidence["row_count_status"])
        self.assertEqual("blocked_unavailable", evidence["evidence_mode"])

    def test_missing_manifest_is_not_stale(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.json"
            evidence = validator.collect_manifest_status(
                "assets.json",
                missing,
                caps={"max_under_cap_bytes": 16, "max_under_cap_rows": 10},
                snapshot_id="ams_00000000000000000000000000000002",
            )

        self.assertEqual("not_present", evidence["content_fingerprint_status"])
        self.assertEqual("not_present", evidence["row_count_status"])
        self.assertEqual("missing_manifest", evidence["evidence_mode"])

    def test_no_unbounded_manifest_operations(self):
        validator = load_validator()
        root_token = "ACE_" + "SHARE_ROOT"
        denied = [
            " ".join(["fi" + "nd", root_token, "-type", "f"]),
            " ".join(["j" + "q", ".", "assets.json"]),
            " ".join(["c" + "at", root_token, "assets.json"]),
            " ".join(["sha256" + "sum", "docs/master-index.jsonl"]),
        ]

        for command in denied:
            self.assertIn("unbounded", "\n".join(validator.validate_operation_is_bounded(command)))

        allowed = "bounded-read --manifest assets.json --max-bytes 128 --max-rows 10"
        self.assertEqual([], validator.validate_operation_is_bounded(allowed))

    def test_public_surfaces_are_scan_clean(self):
        validator = load_validator()

        self.assertEqual([], validator.validate_public_surfaces())

    def test_public_scan_paths_cover_62_artifacts(self):
        validator = load_validator()
        paths = {path.as_posix() for path in validator.public_scan_paths()}

        self.assertTrue(EXPECTED_CORE_PUBLIC_PATHS <= paths)
        review_paths = {
            path.relative_to(REPO_ROOT).as_posix()
            for pattern in ["*plan-62*.md", "*implementation-62*.md"]
            for path in (REPO_ROOT / "scripts" / "review" / "results").glob(pattern)
        }
        self.assertTrue(review_paths <= paths)

    def test_ci_invokes_manifest_freshness_validator(self):
        workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()

        self.assertIn("scripts/validate_ace_manifest_freshness.py", workflow)
        self.assertIn("tests.test_validate_ace_manifest_freshness", workflow)
        self.assertIn("tests.test_validate_ace_manifest_freshness_runtime", workflow)
        self.assertIn("tests.test_validate_ace_manifest_freshness_security", workflow)
        self.assertIn("--evidence tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json", workflow)

    def test_ci_invokes_parent_public_scan_for_62_paths(self):
        workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()

        for path in sorted(EXPECTED_CORE_PUBLIC_PATHS - {"docs/16-corpus-lifecycle.md"}):
            self.assertIn(f"--scan-public-path {path}", workflow)


if __name__ == "__main__":
    unittest.main()
