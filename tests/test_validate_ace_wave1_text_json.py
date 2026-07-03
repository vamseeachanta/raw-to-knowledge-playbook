from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_wave1_text_json.py"
HELPER_PATH = (
    REPO_ROOT
    / "skills"
    / "content-triage-and-exclusion"
    / "resources"
    / "text_json_triage.py"
)
CONTRACT_PATH = REPO_ROOT / "config" / "ace-wave1-text-json-contract.json"
SCHEMA_PATH = REPO_ROOT / "artifacts" / "ace-wave0-ledger-schema.json"
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "ace-wave1-text-json"
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "validate.yml"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_validator():
    return load_module(VALIDATOR_PATH, "validate_ace_wave1_text_json")


def load_helper():
    return load_module(HELPER_PATH, "text_json_triage")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def fixture(name: str) -> Path:
    return FIXTURE_ROOT / name


class AceWave1TextJsonTests(unittest.TestCase):
    def test_contract_imports_route_targets_from_wave0_schema(self):
        validator = load_validator()
        contract = load_json(CONTRACT_PATH)
        schema = load_json(SCHEMA_PATH)

        self.assertEqual([], validator.validate_contract(contract))
        self.assertEqual("ace-wave1-text-json-contract", contract["contract_id"])
        self.assertEqual(52, contract["owner_issue"])
        self.assertEqual(65, contract["imports_route_targets_from_issue"])
        self.assertEqual(schema["route_targets"], contract["route_targets"])
        self.assertEqual("successful_routed_items", contract["success_metric"]["numerator_field"])
        self.assertEqual("eligible_candidate_items", contract["success_metric"]["denominator_field"])

        drifted = copy.deepcopy(contract)
        drifted["route_targets"] = ["public_llm_wiki"]
        self.assertIn("route targets", "\n".join(validator.validate_contract(drifted)))

    def test_sampling_request_uses_downstream_manifest_backed_class_for_issue_52(self):
        validator = load_validator()
        contract = load_json(CONTRACT_PATH)
        schema = load_json(SCHEMA_PATH)
        wave52 = {row["issue"]: row for row in schema["canonical_wave_registry"]}[52]

        self.assertEqual("ingestion_wave", wave52["wave_class"])
        self.assertTrue(wave52["requires_manifest_snapshot_id"])
        self.assertEqual(
            wave52["requires_manifest_snapshot_id"],
            contract["sampling_gate"]["requires_manifest_snapshot_id"],
        )
        self.assertEqual([], validator.validate_committed_sampling_fixture(fixture("sample-manifest.json")))

    def test_downstream_sampling_delegates_to_67_and_fails_shape_only_for_issue_52(self):
        validator = load_validator()
        request = load_json(fixture("sample-manifest.json"))

        errors = validator.validate_sampling_request(request)

        self.assertIn("SELF_ATTESTED_62_EVIDENCE", "\n".join(errors))

    def test_operational_sampling_fails_closed_without_trusted_62_pointer(self):
        validator = load_validator()
        request = load_json(fixture("sample-manifest.json"))
        request.pop("snapshot_evidence", None)

        self.assertIn("MISSING_62_EVIDENCE_POINTER", "\n".join(validator.validate_sampling_request(request)))

    def test_cap_violating_sampling_request_is_rejected(self):
        validator = load_validator()
        request = load_json(fixture("sample-manifest.json"))
        request["per_bucket_row_cap"] = 201

        self.assertIn("cap", "\n".join(validator.validate_sampling_request(request)))

    def test_generated_json_detected_by_shape_not_extension(self):
        helper = load_helper()

        manual = helper.classify_candidate(fixture("manual-config.json"))
        repetitive = helper.classify_candidate(fixture("generated-repetitive-json.json"))

        self.assertEqual("small_config_json", manual["candidate_class"])
        self.assertEqual("metadata_only", manual["route_target"])
        self.assertEqual("generated_repetitive_json", repetitive["candidate_class"])
        self.assertEqual("excluded_no_ingest", repetitive["route_target"])

    def test_lockfile_like_json_is_excluded(self):
        helper = load_helper()

        result = helper.classify_candidate(fixture("generated-lockfile-like.json"))

        self.assertEqual("generated_lockfile_like_json", result["candidate_class"])
        self.assertEqual("excluded_no_ingest", result["route_target"])
        self.assertIn("lockfile", result["signals"])

    def test_high_cardinality_and_repeated_json_are_excluded_without_timestamp(self):
        helper = load_helper()

        for name in [
            "generated-high-cardinality-json.json",
            "generated-repeated-objects-json.json",
            "generated-path-key-cardinality-json.json",
        ]:
            with self.subTest(name=name):
                result = helper.classify_candidate(fixture(name))
                self.assertEqual("excluded_no_ingest", result["route_target"])
                self.assertIn(result["candidate_class"], {"generated_repetitive_json", "source_tree_noise"})

    def test_declared_generated_json_signals_are_emitted(self):
        helper = load_helper()

        package_cache = helper.classify_candidate(fixture("generated-package-cache-json.json"))
        minified_bulk = helper.classify_candidate(fixture("generated-minified-bulk-array.json"))

        self.assertEqual("excluded_no_ingest", package_cache["route_target"])
        self.assertIn("package_cache_shape", package_cache["signals"])
        self.assertEqual("excluded_no_ingest", minified_bulk["route_target"])
        self.assertIn("minified_bulk_array", minified_bulk["signals"])

    def test_hand_authored_markup_kept_without_public_route(self):
        helper = load_helper()

        for name in ["hand-authored-markdown.md", "hand-authored-rst.rst"]:
            with self.subTest(name=name):
                result = helper.classify_candidate(fixture(name))
                self.assertEqual("hand_authored_markup", result["candidate_class"])
                self.assertEqual("private_sidecar", result["route_target"])
                self.assertIn("extraction_estimate", result)
                self.assertIn("extraction_yield", result)

    def test_markup_classification_uses_content_not_extension(self):
        helper = load_helper()

        result = helper.classify_candidate(fixture("empty-markdown.md"))

        self.assertEqual("source_tree_noise", result["candidate_class"])
        self.assertEqual("excluded_no_ingest", result["route_target"])

    def test_source_tree_not_bulk_ingested(self):
        helper = load_helper()

        docstring = helper.classify_candidate(fixture("source-tree-docstring.py"))
        minified = helper.classify_candidate(fixture("source-tree-vendored-minified.js"))

        self.assertEqual("code_documentation", docstring["candidate_class"])
        self.assertEqual("metadata_only", docstring["route_target"])
        self.assertEqual("source_tree_noise", minified["candidate_class"])
        self.assertEqual("excluded_no_ingest", minified["route_target"])

    def test_ordinary_source_code_without_documentation_is_excluded(self):
        helper = load_helper()

        result = helper.classify_candidate(fixture("source-tree-ordinary-code.py"))

        self.assertEqual("source_tree_noise", result["candidate_class"])
        self.assertEqual("excluded_no_ingest", result["route_target"])

        for name in ["source-tree-shebang-only.py", "source-tree-url-string.js"]:
            with self.subTest(name=name):
                result = helper.classify_candidate(fixture(name))
                self.assertEqual("source_tree_noise", result["candidate_class"])
                self.assertEqual("excluded_no_ingest", result["route_target"])

    def test_exclusions_precede_value_ranking(self):
        validator = load_validator()
        row = {
            "candidate_id": "fixture-hard-exclusion",
            "candidate_class": "hand_authored_markup",
            "route_target": "private_sidecar",
            "value_rank": "high",
            "hard_exclusion_reason": "private_security_material",
        }

        errors = validator.validate_candidate_record(row)

        self.assertIn("hard exclusions", "\n".join(errors))

    def test_kept_rows_require_extraction_estimate_and_yield(self):
        validator = load_validator()
        row = load_json(fixture("expected-routing.json"))["candidates"][0]

        self.assertEqual([], validator.validate_candidate_record(row))
        missing = copy.deepcopy(row)
        missing.pop("extraction_yield")

        self.assertIn("extraction_yield", "\n".join(validator.validate_candidate_record(missing)))

    def test_candidate_row_shape_and_store_are_enforced(self):
        validator = load_validator()
        row = load_json(fixture("expected-routing.json"))["candidates"][0]

        missing_store = copy.deepcopy(row)
        missing_store.pop("logical_target_store")
        self.assertIn("logical_target_store", "\n".join(validator.validate_candidate_record(missing_store)))

        bad_store = copy.deepcopy(row)
        bad_store["logical_target_store"] = "metadata_ledger_store"
        self.assertIn("logical_target_store", "\n".join(validator.validate_candidate_record(bad_store)))

        bad_status = copy.deepcopy(row)
        bad_status["parse_status"] = "verified"
        self.assertIn("parse_status", "\n".join(validator.validate_candidate_record(bad_status)))

        metadata_row = copy.deepcopy(row)
        metadata_row["candidate_class"] = "small_config_json"
        metadata_row["route_target"] = "metadata_only"
        metadata_row["logical_target_store"] = "metadata_ledger_store"
        metadata_row["visibility"] = "public"
        self.assertIn("metadata_only", "\n".join(validator.validate_candidate_record(metadata_row)))

        metadata_row["visibility"] = "none"
        self.assertIn("metadata_only", "\n".join(validator.validate_candidate_record(metadata_row)))

        empty_estimate = copy.deepcopy(row)
        empty_estimate["extraction_estimate"] = {}
        self.assertIn("extraction_estimate", "\n".join(validator.validate_candidate_record(empty_estimate)))

    def test_generated_and_noise_classes_must_route_excluded(self):
        validator = load_validator()
        row = load_json(fixture("expected-routing.json"))["candidates"][0]
        for candidate_class in [
            "generated_repetitive_json",
            "generated_lockfile_like_json",
            "source_tree_noise",
            "hard_excluded_material",
        ]:
            mutated = copy.deepcopy(row)
            mutated["candidate_class"] = candidate_class
            mutated["route_target"] = "metadata_only"
            mutated["logical_target_store"] = "metadata_ledger_store"
            with self.subTest(candidate_class=candidate_class):
                self.assertIn("route compatibility", "\n".join(validator.validate_candidate_record(mutated)))

    def test_route_targets_use_closed_enum(self):
        validator = load_validator()
        row = load_json(fixture("expected-routing.json"))["candidates"][0]
        invalid = copy.deepcopy(row)
        invalid["route_target"] = "invented_public_route"

        self.assertIn("closed route", "\n".join(validator.validate_candidate_record(invalid)))

    def test_success_metric_uses_successful_routed_items_over_eligible_candidate_items(self):
        validator = load_validator()
        metric = load_json(fixture("expected-routing.json"))["metric"]

        self.assertEqual([], validator.validate_metric_record(metric))
        bad = copy.deepcopy(metric)
        bad["ingested_success_percent"] = 75.0

        self.assertIn("successful_routed_items / eligible_candidate_items", "\n".join(validator.validate_metric_record(bad)))

    def test_zero_denominator_metric_statuses_are_closed(self):
        validator = load_validator()
        metric = load_json(fixture("expected-routing.json"))["metric"]

        garbage = copy.deepcopy(metric)
        garbage.update(
            {
                "metric_status": "garbage_status",
                "total_classified_items": 0,
                "hard_excluded_items": 0,
                "eligible_candidate_items": 0,
                "successful_routed_items": 0,
            }
        )
        self.assertIn("metric_status", "\n".join(validator.validate_metric_record(garbage)))

        no_eligible = copy.deepcopy(metric)
        no_eligible.update(
            {
                "metric_status": "no_eligible_candidates",
                "total_classified_items": 2,
                "hard_excluded_items": 2,
                "eligible_candidate_items": 0,
                "successful_routed_items": 0,
                "ingested_success_percent": 0.0,
                "excluded_percent": 100.0,
            }
        )
        self.assertIn("no_eligible_candidates", "\n".join(validator.validate_metric_record(no_eligible)))

        control_only = copy.deepcopy(metric)
        control_only["metric_status"] = "not_applicable_control_plane"
        self.assertIn("metric_status", "\n".join(validator.validate_metric_record(control_only)))

    def test_public_route_requires_63_gate_or_demotes(self):
        validator = load_validator()
        helper = load_helper()
        row = load_json(fixture("expected-routing.json"))["candidates"][0]

        for name in ["manual-config.json", "source-tree-docstring.py"]:
            with self.subTest(name=name):
                metadata_row = helper.classify_candidate(fixture(name), public_clearance=True)
                self.assertEqual("metadata_only", metadata_row["route_target"])
                self.assertEqual("private", metadata_row["visibility"])
                self.assertEqual([], validator.validate_candidate_record(metadata_row))

        public_row = copy.deepcopy(row)
        public_row["route_target"] = "public_llm_wiki"
        public_row["logical_target_store"] = "public_llm_wiki_store"
        public_row["visibility"] = "public"
        public_row["public_clearance"] = False

        self.assertIn("public_clearance", "\n".join(validator.validate_candidate_record(public_row)))

        public_row["public_clearance"] = True
        self.assertIn("public-output canary", "\n".join(validator.validate_candidate_record(public_row)))

        public_row["public_output_path"] = "docs/case-studies/ace-wave-1-text-markup-code-json-bootstrap.md"
        public_row["public_clearance_evidence"] = {
            "source_issue": 63,
            "validator_exit_status": 0,
            "scan_public_paths": ["config/ace-wave1-text-json-contract.json"],
        }
        self.assertIn("certification evidence", "\n".join(validator.validate_candidate_record(public_row)))

        public_row["public_clearance_evidence"] = {
            "canary_command": "uv run python scripts/validate_ace_public_artifacts.py",
            "exit_code": 0,
            "scanned_paths": ["config/ace-wave1-text-json-contract.json"],
            "contract_version": "1.0.0",
            "timestamp_utc": "2026-07-03T00:00:00Z",
        }
        self.assertIn("exact public surface", "\n".join(validator.validate_candidate_record(public_row)))

        public_row["public_clearance_evidence"]["scanned_paths"] = [public_row["public_output_path"]]
        self.assertEqual([], validator.validate_candidate_record(public_row))

    def test_durable_output_fields_require_61_gate(self):
        validator = load_validator()
        row = load_json(fixture("expected-routing.json"))["candidates"][0]
        durable = copy.deepcopy(row)
        durable["target_path"] = "knowledge-store/example"
        durable["retrieval_metadata"] = {"lifecycle_state": "candidate"}

        self.assertIn("durable output", "\n".join(validator.validate_candidate_record(durable)))

        durable["durable_output_gate_evidence"] = "issue_61_verified"
        self.assertIn("durable output", "\n".join(validator.validate_candidate_record(durable)))

    def test_committed_fixtures_are_public_scan_safe(self):
        validator = load_validator()
        paths = {path.as_posix() for path in validator.public_scan_paths()}

        self.assertIn("config/ace-wave1-text-json-contract.json", paths)
        self.assertIn("scripts/validate_ace_wave1_text_json.py", paths)
        self.assertIn("tests/test_validate_ace_wave1_text_json.py", paths)
        self.assertIn("tests/fixtures/ace-wave1-text-json", paths)
        self.assertEqual([], validator.validate_public_surfaces())

    def test_metric_counts_match_candidate_rows(self):
        validator = load_validator()
        payload = load_json(fixture("expected-routing.json"))

        self.assertEqual([], validator.validate_routing_payload(payload))
        mismatched = copy.deepcopy(payload)
        mismatched["metric"]["total_classified_items"] = 99

        self.assertIn("total_classified_items", "\n".join(validator.validate_routing_payload(mismatched)))
        missing_scope = copy.deepcopy(payload)
        missing_scope["metric"].pop("metric_scope")
        self.assertIn("metric_scope", "\n".join(validator.validate_routing_payload(missing_scope)))

        bad_candidate = copy.deepcopy(payload)
        bad_candidate["candidates"].append("not an object")
        self.assertIn("candidate rows", "\n".join(validator.validate_routing_payload(bad_candidate)))

    def test_non_object_payloads_return_errors_without_tracebacks(self):
        validator = load_validator()

        self.assertIn("routing payload", "\n".join(validator.validate_routing_payload([])))

        bad_metric = copy.deepcopy(load_json(fixture("expected-routing.json")))
        bad_metric["metric"] = []
        self.assertIn("metric record", "\n".join(validator.validate_routing_payload(bad_metric)))

        self.assertIn("sampling request", "\n".join(validator.validate_sampling_request([])))

    def test_workflow_runs_wave1_validator_and_unit_tests(self):
        workflow = WORKFLOW_PATH.read_text()

        self.assertIn("scripts/validate_ace_wave1_text_json.py", workflow)
        self.assertIn("tests.test_validate_ace_wave1_text_json", workflow)


if __name__ == "__main__":
    unittest.main()
