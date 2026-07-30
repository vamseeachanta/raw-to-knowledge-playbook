from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_wave2_spreadsheet_csv.py"
XLSX_HELPER_PATH = (
    REPO_ROOT / "skills" / "xlsx-input-code-output-canary" / "resources" / "xlsx_canary.py"
)
CSV_HELPER_PATH = (
    REPO_ROOT / "skills" / "format-coverage-ledger" / "resources" / "csv_dialect_probe.py"
)
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "ace-wave2-spreadsheet-csv"
SCHEMA_PATH = REPO_ROOT / "artifacts" / "ace-wave0-ledger-schema.json"
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "validate.yml"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_validator():
    return load_module(VALIDATOR_PATH, "validate_ace_wave2_spreadsheet_csv")


def load_xlsx_helper():
    return load_module(XLSX_HELPER_PATH, "xlsx_canary")


def load_csv_helper():
    return load_module(CSV_HELPER_PATH, "csv_dialect_probe")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def fixture(name: str) -> Path:
    return FIXTURE_ROOT / name


class AceWave2SpreadsheetCsvTests(unittest.TestCase):
    def test_workbook_classification_closed_values(self):
        validator = load_validator()

        for workbook_class in ["data_workbook", "calculation_workbook", "report_workbook", "excluded_workbook"]:
            record = load_json(fixture("valid-ledger.json"))["records"][0]
            record["workbook_class"] = workbook_class
            self.assertNotIn("workbook_class", "\n".join(validator.validate_workbook_record(record)))

        bad = load_json(fixture("valid-ledger.json"))["records"][0]
        bad["workbook_class"] = "mixed"
        self.assertIn("workbook_class", "\n".join(validator.validate_workbook_record(bad)))

    def test_existing_canary_classes_map_losslessly(self):
        helper = load_xlsx_helper()
        cases = {
            "workbook-data-inventory.json": ("data", "data_workbook"),
            "workbook-calculation-inventory.json": ("calculation", "calculation_workbook"),
            "workbook-mixed-chart-inventory.json": ("mixed", "calculation_workbook"),
            "workbook-guarded-inventory.json": ("guarded", "excluded_workbook"),
        }

        for name, expected in cases.items():
            with self.subTest(name=name):
                result = helper.ace_classification_from_inventory(load_json(fixture(name)))
                self.assertEqual(expected[0], result["original_canary_class"])
                self.assertEqual(expected[1], result["workbook_class"])
                self.assertIn("route_target", result)

    def test_report_workbook_class_uses_emitted_inventory_fields(self):
        helper = load_xlsx_helper()

        result = helper.ace_classification_from_inventory(load_json(fixture("workbook-report-inventory.json")))

        self.assertEqual("unsupported", result["original_canary_class"])
        self.assertEqual("report_workbook", result["workbook_class"])
        self.assertEqual("metadata_only", result["route_target"])

    def test_merged_only_layout_is_not_report_evidence(self):
        helper = load_xlsx_helper()
        inventory = load_json(fixture("workbook-data-inventory.json"))
        inventory["summary"]["table_count"] = 0
        inventory["summary"]["merged_range_count"] = 1
        inventory["sheets"][0]["merged_ranges"] = ["A1:C1"]
        inventory["sheets"][0]["tables"] = []

        result = helper.ace_classification_from_inventory(inventory)

        self.assertFalse(result["report_evidence"])
        self.assertEqual("data_workbook", result["workbook_class"])

    def test_mixed_formula_chart_stays_calculation_workbook(self):
        helper = load_xlsx_helper()

        result = helper.ace_classification_from_inventory(load_json(fixture("workbook-mixed-chart-inventory.json")))

        self.assertEqual("mixed", result["original_canary_class"])
        self.assertEqual("calculation_workbook", result["workbook_class"])
        self.assertTrue(result["report_evidence"])

    def test_workbook_route_enum_is_separate_from_class_enum(self):
        validator = load_validator()
        record = load_json(fixture("valid-ledger.json"))["records"][0]
        record["workbook_class"] = "excluded_workbook"
        record["route_target"] = "excluded_workbook"

        errors = "\n".join(validator.validate_workbook_record(record))

        self.assertIn("route_target", errors)

    def test_excluded_workbook_can_be_metadata_only_deferral(self):
        validator = load_validator()
        record = load_json(fixture("valid-ledger.json"))["records"][0]
        record["original_canary_class"] = "unsupported"
        record["workbook_class"] = "excluded_workbook"
        record["route_target"] = "metadata_only"
        record["logical_target_store"] = "metadata_ledger_store"
        record["visibility"] = "private"
        record["content_eligible"] = False
        record["deferral_reasons"] = ["adapter_required"]

        self.assertEqual([], validator.validate_workbook_record(record))

    def test_formula_cached_values_not_verification(self):
        validator = load_validator()
        record = load_json(fixture("valid-ledger.json"))["records"][0]
        record["workbook_class"] = "calculation_workbook"
        record["original_canary_class"] = "calculation"
        record["cached_values_only"] = True

        self.assertIn("cached values", "\n".join(validator.validate_workbook_record(record)))

    def test_calculation_triplet_required(self):
        validator = load_validator()
        record = load_json(fixture("valid-ledger.json"))["records"][0]
        record["workbook_class"] = "calculation_workbook"
        record["original_canary_class"] = "calculation"

        self.assertIn("calculation triplet", "\n".join(validator.validate_workbook_record(record)))

        record["calculation_triplet"] = {
            "input_contract": "synthetic inputs",
            "code_artifact": "synthetic evaluator",
            "output_proof": "independent recompute",
        }
        self.assertEqual([], validator.validate_workbook_record(record))

    def test_runtime_generated_workbook_fixtures_only(self):
        validator = load_validator()

        self.assertEqual([], validator.validate_no_raw_workbook_bytes(FIXTURE_ROOT))

    def test_nested_raw_workbook_fixture_is_blocked(self):
        validator = load_validator()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nested = root / "nested"
            nested.mkdir()
            (nested / "leak.xlsx").write_bytes(b"raw workbook bytes")

            self.assertIn("raw workbook fixture", "\n".join(validator.validate_no_raw_workbook_bytes(root)))

    def test_renamed_openxml_workbook_container_is_blocked(self):
        validator = load_validator()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nested = root / "nested"
            nested.mkdir()
            renamed = nested / "workbook.payload"
            with zipfile.ZipFile(renamed, "w") as archive:
                archive.writestr("[Content_Types].xml", "<Types />")
                archive.writestr("xl/workbook.xml", "<workbook />")

            self.assertIn("raw workbook fixture", "\n".join(validator.validate_no_raw_workbook_bytes(root)))

    def test_xls_requires_adapter_before_content_success(self):
        helper = load_xlsx_helper()

        result = helper.ace_classification_from_inventory(load_json(fixture("workbook-legacy-xls-inventory.json")))

        self.assertEqual("excluded_workbook", result["workbook_class"])
        self.assertIn("adapter_required", result["deferral_reasons"])

    def test_macro_and_external_link_flags_are_inventory_only(self):
        helper = load_xlsx_helper()

        result = helper.ace_classification_from_inventory(load_json(fixture("workbook-macro-external-inventory.json")))

        self.assertEqual("calculation_workbook", result["workbook_class"])
        self.assertIn("macro_present", result["inventory_flags"])
        self.assertIn("external_links_present", result["inventory_flags"])
        self.assertIn("macro_or_external_logic_deferred", result["deferral_reasons"])

    def test_xlsm_macro_payload_detected_from_container(self):
        helper = load_xlsx_helper()

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "macro.xlsm"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("xl/vbaProject.bin", b"synthetic macro payload")

            self.assertTrue(helper.workbook_has_macro_payload(path))

    def test_protected_workbook_is_deferred(self):
        helper = load_xlsx_helper()

        result = helper.ace_classification_from_inventory(load_json(fixture("workbook-guarded-inventory.json")))

        self.assertEqual("excluded_workbook", result["workbook_class"])
        self.assertEqual("excluded_no_ingest", result["route_target"])
        self.assertIn("protected_workbook", result["deferral_reasons"])

    def test_csv_dialect_field_count_digests(self):
        helper = load_csv_helper()

        comma = helper.probe_csv(fixture("comma-data.csv"))
        semicolon = helper.probe_csv(fixture("semicolon-data.csv"))
        ragged = helper.probe_csv(fixture("ragged-data.csv"))

        self.assertEqual(",", comma["delimiter"])
        self.assertEqual(";", semicolon["delimiter"])
        self.assertEqual([], comma["ragged_rows"])
        self.assertTrue(ragged["ragged_rows"])
        self.assertRegex(comma["content_digest"], r"^[0-9a-f]{64}$")
        self.assertNotEqual(comma["content_digest"], semicolon["content_digest"])

    def test_csv_dialect_detection_respects_quoted_delimiters(self):
        helper = load_csv_helper()

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "quoted-semicolon.csv"
            path.write_text('"label, with comma";value\nalpha;1\n', encoding="utf-8")

            self.assertEqual(";", helper.probe_csv(path)["delimiter"])

    def test_csv_convention_sidecar_required(self):
        validator = load_validator()
        helper = load_csv_helper()
        probe = helper.probe_csv(fixture("comma-data.csv"))

        self.assertIn("convention sidecar", "\n".join(validator.validate_csv_probe(probe, None)))
        self.assertEqual([], validator.validate_csv_probe(probe, load_json(fixture("numeric-conventions.json"))))

    def test_delimited_record_requires_probe_and_convention_sidecar(self):
        validator = load_validator()
        record = load_json(fixture("valid-ledger.json"))["records"][1]
        record.pop("dialect_probe", None)
        record.pop("convention_sidecar", None)

        errors = "\n".join(validator.validate_delimited_record(record))

        self.assertIn("dialect probe", errors)

    def test_delimited_probe_rejects_malformed_evidence(self):
        validator = load_validator()
        record = load_json(fixture("valid-ledger.json"))["records"][1]
        record["dialect_probe"] = {
            "delimiter": ",",
            "expected_field_count": 3,
            "row_count": 2,
            "field_counts": [],
            "ragged_rows": [],
            "content_digest": "z" * 64,
            "numeric_columns": [],
        }
        record.pop("convention_sidecar", None)

        errors = "\n".join(validator.validate_delimited_record(record))

        self.assertIn("field_counts", errors)
        self.assertIn("content_digest", errors)
        self.assertIn("convention sidecar", errors)

    def test_delimited_probe_rejects_inconsistent_ragged_evidence(self):
        validator = load_validator()
        record = load_json(fixture("valid-ledger.json"))["records"][1]
        record["dialect_probe"]["ragged_rows"] = [
            {"row_number": 999, "field_count": 2, "expected_field_count": 3}
        ]

        self.assertIn("ragged_rows", "\n".join(validator.validate_delimited_record(record)))

    def test_delimited_probe_rejects_header_and_numeric_column_mismatch(self):
        validator = load_validator()
        record = load_json(fixture("valid-ledger.json"))["records"][1]
        record["dialect_probe"]["field_counts"][0] = 2
        record["dialect_probe"]["numeric_columns"] = ["missing_column"]

        errors = "\n".join(validator.validate_delimited_record(record))

        self.assertIn("header", errors)
        self.assertIn("numeric_columns", errors)

    def test_67_boundary_caps_import_contract_values(self):
        validator = load_validator()
        request = load_json(fixture("sample-manifest.json"))

        self.assertIn("SELF_ATTESTED_62_EVIDENCE", "\n".join(validator.validate_sampling_request(request)))

        for key in ["per_bucket_row_cap", "max_files_touched", "max_bytes_touched"]:
            with self.subTest(key=key):
                bad = copy.deepcopy(request)
                bad[key] += 1
                self.assertIn("cap", "\n".join(validator.validate_sampling_request(bad)).lower())

    def test_missing_trusted_62_evidence_fails_closed(self):
        validator = load_validator()
        request = load_json(fixture("sample-manifest.json"))
        request.pop("snapshot_evidence")

        self.assertIn("MISSING_62_EVIDENCE_POINTER", "\n".join(validator.validate_sampling_request(request)))

    def test_fixture_62_evidence_cannot_authorize_sampling(self):
        validator = load_validator()

        self.assertEqual([], validator.validate_committed_sampling_fixture(fixture("sample-manifest.json")))

    def test_61_durable_fields_blocked(self):
        validator = load_validator()
        record = load_json(fixture("valid-ledger.json"))["records"][0]
        record["target_path"] = "knowledge-store/spreadsheets/example"
        record["retrieval_metadata"] = {"lifecycle_state": "candidate"}

        self.assertIn("durable output", "\n".join(validator.validate_workbook_record(record)))

    def test_private_sidecar_route_and_field_blocked(self):
        validator = load_validator()
        record = load_json(fixture("valid-ledger.json"))["records"][0]
        record["route_target"] = "private_sidecar"
        record["logical_target_store"] = "private_sidecar_store"
        record["visibility"] = "private"
        record["private_sidecar"] = {"path": "private/sidecar"}

        self.assertIn("durable output", "\n".join(validator.validate_workbook_record(record)))

    def test_63_public_output_blocked(self):
        validator = load_validator()
        record = load_json(fixture("valid-ledger.json"))["records"][0]
        record["route_target"] = "public_llm_wiki"
        record["logical_target_store"] = "public_llm_wiki_store"
        record["visibility"] = "public"

        self.assertIn("public-output canary", "\n".join(validator.validate_workbook_record(record)))

    def test_wave2_success_metric_defined(self):
        validator = load_validator()
        payload = load_json(fixture("valid-ledger.json"))

        self.assertEqual([], validator.validate_ledger_payload(payload))

        mismatched = copy.deepcopy(payload)
        mismatched["metric"]["eligible_candidate_items"] = 2
        self.assertIn("eligible_candidate_items", "\n".join(validator.validate_ledger_payload(mismatched)))

    def test_scan_safe_negative_fixtures(self):
        validator = load_validator()

        self.assertEqual([], validator.validate_public_surfaces())

    def test_xlsx_canary_cli_can_emit_ace_classification(self):
        result = subprocess.run(
            [
                sys.executable,
                str(XLSX_HELPER_PATH),
                "classify",
                "--inventory",
                str(fixture("workbook-data-inventory.json")),
                "--ace",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual("data_workbook", payload["workbook_class"])

    def test_workflow_runs_wave2_validator_and_unit_tests(self):
        workflow = WORKFLOW_PATH.read_text()

        self.assertIn("scripts/validate_ace_wave2_spreadsheet_csv.py", workflow)
        self.assertIn("tests.test_validate_ace_wave2_spreadsheet_csv", workflow)


if __name__ == "__main__":
    unittest.main()
