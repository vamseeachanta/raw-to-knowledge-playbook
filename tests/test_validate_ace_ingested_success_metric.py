from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_ingested_success_metric.py"
CONTRACT_PATH = REPO_ROOT / "config" / "ace-ingested-success-metric-contract.json"
SCHEMA_PATH = REPO_ROOT / "artifacts" / "ace-wave0-ledger-schema.json"
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "ace-knowledge-store-contract"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_ace_ingested_success_metric", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text())


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_ROOT / name).read_text())


class AceIngestedSuccessMetricTests(unittest.TestCase):
    def test_metric_contract_is_json_and_owned_by_61(self):
        validator = load_validator()
        contract = load_contract()

        self.assertEqual([], validator.validate_metric_contract(contract))
        self.assertEqual("ace-ingested-success-metric-contract", contract["contract_id"])
        self.assertRegex(contract["contract_version"], r"^1\.0\.\d+$")
        self.assertEqual(61, contract["owner_issue"])
        self.assertEqual(65, contract["imports_success_fields_from_issue"])

    def test_success_metric_formula_imports_65_fields(self):
        validator = load_validator()
        contract = load_contract()
        schema = json.loads(SCHEMA_PATH.read_text())

        self.assertEqual("successful_routed_items", contract["success_metric"]["numerator_field"])
        self.assertEqual("eligible_candidate_items", contract["success_metric"]["denominator_field"])
        self.assertIn("successful_routed_items", schema["ledger_field_groups"]["success"])
        self.assertIn("eligible_candidate_items", schema["ledger_field_groups"]["success"])

        mutated = copy.deepcopy(contract)
        mutated["success_metric"]["numerator_field"] = "verified_items"
        self.assertIn("success numerator", "\n".join(validator.validate_metric_contract(mutated)))

        bad_exclusion = copy.deepcopy(contract)
        bad_exclusion["exclusion_metric"]["denominator_field"] = "eligible_candidate_items"
        self.assertIn("exclusion denominator", "\n".join(validator.validate_metric_contract(bad_exclusion)))

    def test_valid_measured_ingestion_record_passes(self):
        validator = load_validator()
        record = load_fixture("valid-ingestion-metric.json")

        self.assertEqual([], validator.validate_metric_record(record))

    def test_wrong_denominator_or_percentage_fails(self):
        validator = load_validator()
        record = load_fixture("valid-ingestion-metric.json")

        bad_denominator = copy.deepcopy(record)
        bad_denominator["eligible_candidate_items"] = bad_denominator["total_classified_items"]
        self.assertIn("eligible_candidate_items", "\n".join(validator.validate_metric_record(bad_denominator)))

        bad_percent = copy.deepcopy(record)
        bad_percent["ingested_success_percent"] = 99.0
        self.assertIn("ingested success percent", "\n".join(validator.validate_metric_record(bad_percent)))

        bad_wave_class = copy.deepcopy(record)
        bad_wave_class["wave_class"] = "not_a_real_wave_class"
        self.assertIn("wave_class", "\n".join(validator.validate_metric_record(bad_wave_class)))

    def test_hard_exclusions_are_reported_separately(self):
        validator = load_validator()
        record = load_fixture("valid-ingestion-metric.json")

        self.assertEqual(10, record["total_classified_items"])
        self.assertEqual(2, record["hard_excluded_items"])
        self.assertEqual(8, record["eligible_candidate_items"])
        self.assertEqual(20.0, record["excluded_percent"])

        bad = copy.deepcopy(record)
        bad["eligible_candidate_items"] = 10
        self.assertIn("hard exclusions", "\n".join(validator.validate_metric_record(bad)))

        missing_excluded_percent = copy.deepcopy(record)
        missing_excluded_percent["hard_excluded_items"] = 0
        missing_excluded_percent["eligible_candidate_items"] = 10
        missing_excluded_percent["successful_routed_items"] = 10
        missing_excluded_percent["ingested_success_percent"] = 100.0
        missing_excluded_percent.pop("excluded_percent")
        self.assertIn("excluded_percent", "\n".join(validator.validate_metric_record(missing_excluded_percent)))

    def test_zero_denominator_behavior_is_explicit(self):
        validator = load_validator()

        self.assertEqual([], validator.validate_metric_record(load_fixture("valid-control-metric.json")))
        self.assertEqual([], validator.validate_metric_record(load_fixture("valid-no-eligible-metric.json")))
        self.assertEqual([], validator.validate_metric_record(load_fixture("valid-no-classified-metric.json")))

        no_classified = load_fixture("valid-no-classified-metric.json")
        with_excluded_percent = copy.deepcopy(no_classified)
        with_excluded_percent["excluded_percent"] = 0.0
        self.assertIn("no_classified_items", "\n".join(validator.validate_metric_record(with_excluded_percent)))

        no_eligible = load_fixture("valid-no-eligible-metric.json")
        with_success_percent = copy.deepcopy(no_eligible)
        with_success_percent["ingested_success_percent"] = 0.0
        self.assertIn("no_eligible_candidates", "\n".join(validator.validate_metric_record(with_success_percent)))

    def test_control_plane_metric_requires_zero_sentinel(self):
        validator = load_validator()
        record = load_fixture("valid-control-metric.json")

        self.assertEqual("not_applicable_control_plane", record["metric_status"])
        self.assertEqual(0, record["measured_success_numerator"])
        self.assertEqual(0, record["measured_success_denominator"])
        self.assertEqual(0, record["success_threshold"])

        bad = copy.deepcopy(record)
        bad["metric_status"] = "measured"
        self.assertIn("control plane", "\n".join(validator.validate_metric_record(bad)))

        polluted = copy.deepcopy(record)
        polluted["total_classified_items"] = 1
        self.assertIn("zero counts", "\n".join(validator.validate_metric_record(polluted)))

    def test_public_scan_paths_cover_metric_artifacts(self):
        validator = load_validator()
        paths = {path.as_posix() for path in validator.public_scan_paths()}

        self.assertIn("config/ace-ingested-success-metric-contract.json", paths)
        self.assertIn("scripts/validate_ace_ingested_success_metric.py", paths)
        self.assertIn("tests/test_validate_ace_ingested_success_metric.py", paths)
        self.assertIn("tests/fixtures/ace-knowledge-store-contract/valid-ingestion-metric.json", paths)


if __name__ == "__main__":
    unittest.main()
