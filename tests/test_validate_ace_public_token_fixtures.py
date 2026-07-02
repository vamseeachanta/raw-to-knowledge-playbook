from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_public_token_fixtures.py"
CONTRACT_PATH = REPO_ROOT / "config" / "ace-public-token-fixture-contract.json"
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "ace-public-token-fixtures" / "good-request.json"
SCHEMA_PATH = REPO_ROOT / "artifacts" / "ace-wave0-ledger-schema.json"
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "validate.yml"
PARENT_VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_epic_wave_coordination.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_validator():
    return load_module(VALIDATOR_PATH, "validate_ace_public_token_fixtures")


def load_fixture_library():
    return load_module(REPO_ROOT / "scripts" / "ace_public_token_fixtures.py", "ace_public_token_fixtures")


def load_parent_validator():
    return load_module(PARENT_VALIDATOR_PATH, "validate_ace_epic_wave_coordination_for_66")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def source_term(*parts: str) -> str:
    return "_".join(parts)


EXPECTED_PRIVATE_TERMS = [
    source_term("source", "id"),
    source_term("source", "sha256"),
    source_term("private", "lookup_key"),
    source_term("private", "lookup_map"),
    source_term("share", "relative_path_private_only"),
]
EXPECTED_SOURCE_DIGEST_TERMS = [
    source_term("source", "hash"),
    source_term("provenance", "pointer"),
]
EXPECTED_PLACEHOLDERS = [
    "ACE_PRIVATE_PLACEHOLDER_IDENTITY",
    "ACE_PRIVATE_PLACEHOLDER_DIGEST",
    "ACE_PRIVATE_PLACEHOLDER_LOOKUP_KEY",
    "ACE_PRIVATE_PLACEHOLDER_LOOKUP_MAP",
    "ACE_PRIVATE_PLACEHOLDER_PATH",
]


class AcePublicTokenFixtureTests(unittest.TestCase):
    def test_fixture_contract_is_json_and_owned_by_66(self):
        contract = load_json(CONTRACT_PATH)

        self.assertEqual("ace-public-token-fixture-contract", contract["contract_id"])
        self.assertRegex(contract["contract_version"], r"^1\.0\.\d+$")
        self.assertEqual(66, contract["owner_issue"])
        self.assertEqual("fixture_only", contract["mode"])
        self.assertEqual(65, contract["depends_on_schema_issue"])
        self.assertTrue(contract["provisional_fixture_contract"])

    def test_contract_imports_65_schema_terms(self):
        schema = load_json(SCHEMA_PATH)
        contract = load_json(CONTRACT_PATH)

        self.assertEqual(
            schema["downstream_contracts"]["public_token"]["field_name"],
            contract["public_token_field_name"],
        )
        self.assertEqual([66, 63], contract["public_token_policy_owner_issues"])
        self.assertEqual(EXPECTED_PRIVATE_TERMS, contract["private_source_terms"])
        self.assertEqual(EXPECTED_SOURCE_DIGEST_TERMS, contract["source_like_raw_digest_terms"])
        self.assertNotIn("route_targets", contract)
        self.assertNotIn("logical_target_stores", contract)

    def test_fixture_contract_reconciles_with_63_when_present(self):
        library = load_fixture_library()
        schema = load_json(SCHEMA_PATH)
        contract = load_json(CONTRACT_PATH)
        public_output_contract = {
            "public_token_field_name": "public_source_token",
            "public_token_grammar": {"prefix": "pst_", "hex_characters": 32},
            "public_safe_source_reference_fields": ["public_source_token"],
            "private_only_provenance_fields": EXPECTED_PRIVATE_TERMS,
            "source_like_raw_digest_terms": EXPECTED_SOURCE_DIGEST_TERMS,
        }

        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "ace-public-output-contract.json"
            output_path.write_text(json.dumps(public_output_contract))
            original_repo_path = library.repo_path

            def mapped_repo_path(path: Path) -> Path:
                if Path(path).as_posix() == "config/ace-public-output-contract.json":
                    return output_path
                return original_repo_path(path)

            library.repo_path = mapped_repo_path
            try:
                still_provisional = library.validate_contract(contract, schema)

                reconciled = deepcopy(contract)
                reconciled["provisional_fixture_contract"] = False
                self.assertEqual([], library.validate_contract(reconciled, schema))

                drifted = deepcopy(reconciled)
                public_output_contract["public_token_grammar"]["hex_characters"] = 64
                public_output_contract["private_only_provenance_fields"] = ["other_private_field"]
                public_output_contract["source_like_raw_digest_terms"] = []
                output_path.write_text(json.dumps(public_output_contract))
                drift_errors = library.validate_contract(drifted, schema)

                alias_conflict = deepcopy(reconciled)
                public_output_contract = {
                    "public_token_field_name": "public_source_token",
                    "public_token_grammar": {"prefix": "pst_", "hex_characters": 32, "extra": "drift"},
                    "public_safe_source_reference_fields": ["public_source_token"],
                    "public_source_reference_fields": [source_term("source", "id")],
                    "private_only_provenance_fields": EXPECTED_PRIVATE_TERMS,
                    "private_only_fields": ["other_private_field"],
                    "source_like_raw_digest_terms": EXPECTED_SOURCE_DIGEST_TERMS,
                    "source_hash_private_terms": [],
                }
                output_path.write_text(json.dumps(public_output_contract))
                alias_errors = library.validate_contract(alias_conflict, schema)
            finally:
                library.repo_path = original_repo_path

        self.assertIn("must not remain provisional", "\n".join(still_provisional))
        self.assertIn("#63 public output contract", "\n".join(drift_errors))
        self.assertIn("#63 public output contract", "\n".join(alias_errors))

    def test_good_fixture_uses_generation_request_marker(self):
        fixture = load_json(FIXTURE_PATH)
        marker = fixture["public_source_token_request"]

        self.assertEqual({"fixture_set_id", "fixture_row_id", "count"}, set(marker))
        self.assertEqual("wave0_public_token_good", marker["fixture_set_id"])
        self.assertRegex(marker["fixture_row_id"], r"^fixture_row_\d{3}$")
        self.assertIsInstance(marker["count"], int)
        self.assertNotIn("public_source_token", fixture)

    def test_private_placeholder_mapping_rows_are_neutral(self):
        fixture = load_json(FIXTURE_PATH)
        contract = load_json(CONTRACT_PATH)

        self.assertEqual(EXPECTED_PLACEHOLDERS, contract["placeholder_values"])
        self.assertEqual(
            contract["private_placeholder_mapping"],
            fixture["private_field_placeholders"],
        )
        for row in fixture["private_field_placeholders"]:
            self.assertEqual({"schema_term", "placeholder_value"}, set(row))
            self.assertIn(row["schema_term"], EXPECTED_PRIVATE_TERMS)
            self.assertIn(row["placeholder_value"], EXPECTED_PLACEHOLDERS)

    def test_validator_accepts_committed_contract_and_fixture(self):
        validator = load_validator()

        self.assertEqual([], validator.validate_contract_file(CONTRACT_PATH))
        self.assertEqual([], validator.validate_fixture_file(FIXTURE_PATH))

    def test_generation_request_marker_rejects_forbidden_inputs(self):
        library = load_fixture_library()
        marker = load_json(FIXTURE_PATH)["public_source_token_request"]

        for key in load_json(CONTRACT_PATH)["forbidden_request_keys"]:
            bad_marker = dict(marker)
            bad_marker[key] = "fixture-local"
            with self.subTest(key=key):
                errors = []
                library._validate_request_marker(bad_marker, load_json(CONTRACT_PATH), errors)
                self.assertTrue(errors)

    def test_request_values_reject_leak_predicates(self):
        library = load_fixture_library()
        contract = load_json(CONTRACT_PATH)
        marker = load_json(FIXTURE_PATH)["public_source_token_request"]
        token_literal = "pst_" + ("0" * 32)
        digest_literal = "0123456789abcdef" * 4
        private_term = source_term("source", "id")
        digest_term = source_term("provenance", "pointer")

        email_like = "owner" + "@example.com"
        for value in ["../private", "row/name", email_like, token_literal, digest_literal, private_term, digest_term]:
            bad_marker = dict(marker)
            bad_marker["fixture_row_id"] = value
            errors = []
            library._validate_request_marker(bad_marker, contract, errors)
            with self.subTest(value=value):
                self.assertTrue(errors)

    def test_malformed_request_markers_fail(self):
        library = load_fixture_library()
        contract = load_json(CONTRACT_PATH)
        marker = load_json(FIXTURE_PATH)["public_source_token_request"]

        cases = [
            {**marker, "extra": "value"},
            {**marker, "fixture_set_id": "wave0_public_token_other"},
            {**marker, "fixture_row_id": "row001"},
            {**marker, "count": 0},
            {**marker, "count": 101},
            {**marker, "count": "3"},
        ]
        for bad_marker in cases:
            errors = []
            library._validate_request_marker(bad_marker, contract, errors)
            with self.subTest(bad_marker=bad_marker):
                self.assertTrue(errors)

    def test_generator_emits_opaque_unique_fixture_tokens(self):
        library = load_fixture_library()
        marker = {"fixture_set_id": "wave0_public_token_good", "fixture_row_id": "fixture_row_001", "count": 2}
        values = iter([
            "1" * 32,
            "1" * 32,
            "2" * 32,
        ])

        tokens = library.generate_fixture_tokens(marker, random_hex=lambda: next(values))

        self.assertEqual(["pst_" + ("1" * 32), "pst_" + ("2" * 32)], tokens)

    def test_generator_rejects_bad_marker_and_invalid_randomness(self):
        library = load_fixture_library()
        bad_marker = {"fixture_set_id": "wave0_public_token_good", "fixture_row_id": "fixture_row_001", "count": 1, "deterministic_seed": "fixed"}
        good_marker = {"fixture_set_id": "wave0_public_token_good", "fixture_row_id": "fixture_row_001", "count": 1}

        with self.assertRaises(ValueError):
            library.generate_fixture_tokens(bad_marker, random_hex=lambda: "1" * 32)
        with self.assertRaises(ValueError):
            library.generate_fixture_tokens(good_marker, random_hex=lambda: "not-hex")

    def test_bad_fixture_rejects_unknown_placeholder_and_lookup_persistence(self):
        validator = load_validator()
        fixture = load_json(FIXTURE_PATH)
        bad_placeholder = json.loads(json.dumps(fixture))
        bad_placeholder["private_field_placeholders"][0]["placeholder_value"] = "ACE_PRIVATE_PLACEHOLDER_UNKNOWN"

        self.assertIn("placeholder", "\n".join(validator.validate_fixture(bad_placeholder, load_json(CONTRACT_PATH))))

        persistence_attempt = dict(fixture)
        persistence_attempt[source_term("private", "lookup_map")] = {"fixture": "lookup"}
        self.assertIn("key is not allowed", "\n".join(validator.validate_fixture(persistence_attempt, load_json(CONTRACT_PATH))))

    def test_concrete_token_assignment_matches_parent_scanner(self):
        parent = load_parent_validator()
        validator = load_validator()
        token_assignment = "public_" + "source_token: " + "pst_" + ("0" * 32)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.md"
            path.write_text(token_assignment + "\n")

            parent_errors = parent.validate_public_artifact_paths([path])
            fixture_errors = validator.validate_public_surfaces([path])

        self.assertIn("private source field assignment", "\n".join(parent_errors))
        self.assertIn("private source field assignment", "\n".join(fixture_errors))

    def test_bare_concrete_token_literals_are_fixture_validator_only(self):
        validator = load_validator()
        fixture = load_json(FIXTURE_PATH)
        fixture["fixture_kind"] = "pst_" + ("0" * 32)

        errors = validator.validate_fixture(fixture, load_json(CONTRACT_PATH))

        self.assertIn("concrete public token literals", "\n".join(errors))

    def test_public_scan_paths_cover_66_artifacts(self):
        validator = load_validator()
        paths = {path.as_posix() for path in validator.public_scan_paths()}
        expected = {
            "docs/plans/2026-06-30-issue-66-ace-public-token-fixtures-private-field-placeholders.md",
            "config/ace-public-token-fixture-contract.json",
            "scripts/ace_public_token_fixtures.py",
            "scripts/validate_ace_public_token_fixtures.py",
            "tests/test_validate_ace_public_token_fixtures.py",
            "tests/test_validate_ace_wave0_schema_contract.py",
            "tests/fixtures/ace-public-token-fixtures/good-request.json",
            ".github/workflows/validate.yml",
            ".planning/plan-approved/66.md",
        }

        self.assertTrue(expected <= paths)
        self.assertEqual([], validator.validate_public_surfaces())

    def test_ci_invokes_public_token_fixture_validator(self):
        workflow = WORKFLOW_PATH.read_text()

        self.assertIn("uv run python scripts/validate_ace_public_token_fixtures.py", workflow)
        self.assertIn("uv run python -m unittest tests.test_validate_ace_public_token_fixtures", workflow)
        self.assertIn("--scan-public-path config/ace-public-token-fixture-contract.json", workflow)


if __name__ == "__main__":
    unittest.main()
