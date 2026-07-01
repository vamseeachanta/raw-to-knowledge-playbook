from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_wave0_schema_contract.py"
PARENT_VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_epic_wave_coordination.py"
SCHEMA_PATH = REPO_ROOT / "artifacts" / "ace-wave0-ledger-schema.json"

EXPECTED_ROUTE_TO_STORE = {
    "public_llm_wiki": "public_llm_wiki_store",
    "private_sidecar": "private_sidecar_store",
    "metadata_only": "metadata_ledger_store",
    "excluded_no_ingest": "excluded_no_store",
}
EXPECTED_VERIFICATION_STATES = {
    "not_verified",
    "validator_passed",
    "independent_review_passed",
    "verification_rejected",
}
EXPECTED_FIELD_GROUPS = {
    "identity",
    "routing",
    "content",
    "method",
    "validation",
    "success",
    "readiness",
    "downstream_contracts",
}
EXPECTED_SOURCE_DIGEST_TERMS = {
    "source_" + "hash",
    "provenance_" + "pointer",
}
EXPECTED_SPLIT_DEPENDENCIES = {
    65: [],
    66: [65],
    67: [65],
    68: [65, 66],
    69: [65],
}
EXPECTED_CORE_PUBLIC_PATHS = {
    "docs/plans/2026-06-30-issue-65-ace-wave-0-ledger-schema-route-store-matrix.md",
    "docs/plans/README.md",
    "docs/plans/ace-share-ingestion-wave-coordination.md",
    "artifacts/ace-wave0-ledger-schema.json",
    "scripts/validate_ace_wave0_schema_contract.py",
    "tests/test_validate_ace_wave0_schema_contract.py",
    ".github/workflows/validate.yml",
}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_validator():
    return load_module(VALIDATOR_PATH, "validate_ace_wave0_schema_contract")


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


def source_term(*parts: str) -> str:
    return "_".join(parts)


def collect_keys(value) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key))
            keys.update(collect_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(collect_keys(nested))
    return keys


class AceWave0SchemaContractTests(unittest.TestCase):
    def test_schema_file_is_json_and_versioned(self):
        schema = load_schema()

        self.assertEqual("ace-wave0-ledger-schema", schema["schema_id"])
        self.assertRegex(schema["schema_version"], r"^1\.0\.\d+$")
        self.assertEqual(65, schema["owner_issue"])
        self.assertEqual("plan-approved", schema["status"])
        self.assertIn("public_safety_notes", schema)
        self.assertTrue(schema["public_safety_notes"])

    def test_validator_accepts_committed_schema(self):
        validator = load_validator()

        self.assertEqual([], validator.validate_schema_file(SCHEMA_PATH))

    def test_route_enum_is_closed(self):
        schema = load_schema()

        self.assertEqual(set(EXPECTED_ROUTE_TO_STORE), set(schema["route_targets"]))

    def test_logical_store_enum_is_closed(self):
        schema = load_schema()

        self.assertEqual(set(EXPECTED_ROUTE_TO_STORE.values()), set(schema["logical_target_stores"]))

    def test_route_to_store_matrix_is_logical_only(self):
        validator = load_validator()
        schema = load_schema()

        self.assertEqual(EXPECTED_ROUTE_TO_STORE, schema["route_store_matrix"])
        for unsafe_store in [
            "/" + "tmp/private",
            ".." + "/private-sidecar",
            "llm" + "-wiki/public",
            "repo/docs/output",
            "host" + ":/share/private",
        ]:
            mutated = copy.deepcopy(schema)
            mutated["route_store_matrix"]["private_sidecar"] = unsafe_store
            errors = validator.validate_schema(mutated)
            self.assertIn("logical store", "\n".join(errors))

    def test_control_plane_verification_state_enum_is_closed(self):
        validator = load_validator()
        schema = load_schema()

        states = set(schema["control_plane_verification_states"])
        self.assertEqual(EXPECTED_VERIFICATION_STATES, states)
        comparison_sets = schema["external_status_vocabularies"]
        lifecycle_states = set(comparison_sets["issue_61_lifecycle_states"]["values"])
        parse_states = set(comparison_sets["page_shape_parse_status_values"]["values"])
        self.assertFalse(states & lifecycle_states)
        self.assertFalse(states & parse_states)

        mutated = copy.deepcopy(schema)
        mutated["control_plane_verification_states"].append("rejected")
        errors = validator.validate_schema(mutated)
        self.assertIn("verification state", "\n".join(errors))

    def test_required_field_groups_are_present(self):
        schema = load_schema()

        self.assertEqual(EXPECTED_FIELD_GROUPS, set(schema["required_field_groups"]))

    def test_private_source_terms_are_values_not_keys(self):
        schema = load_schema()
        private_terms = set(schema["private_source_field_terms"])

        self.assertEqual(
            {
                source_term("source", "id"),
                source_term("source", "sha256"),
                source_term("private", "lookup_key"),
                source_term("private", "lookup_map"),
                source_term("share", "relative_path_private_only"),
            },
            private_terms,
        )
        self.assertFalse(private_terms & collect_keys(schema))

    def test_private_field_names_are_schema_terms_only(self):
        validator = load_validator()
        schema = load_schema()
        private_term = source_term("source", "id")

        key_mutation = copy.deepcopy(schema)
        key_mutation["unsafe_private_key_fixture"] = {private_term: "raw-value"}
        self.assertIn("private source field", "\n".join(validator.validate_schema(key_mutation)))

        value_mutation = copy.deepcopy(schema)
        value_mutation["unsafe_private_value_fixture"] = [private_term + "=raw-value"]
        self.assertIn("private source field", "\n".join(validator.validate_schema(value_mutation)))

    def test_json_source_hash_assignments_are_rejected(self):
        validator = load_validator()
        schema = load_schema()
        hash_key = source_term("source", "hash")
        digest = "0123456789abcdef" * 4

        self.assertEqual(EXPECTED_SOURCE_DIGEST_TERMS, set(schema["source_like_raw_digest_terms"]))

        mutated = copy.deepcopy(schema)
        mutated["unsafe_digest_fixture"] = {hash_key: digest}
        self.assertIn("raw digest", "\n".join(validator.validate_schema(mutated)))

        for term in EXPECTED_SOURCE_DIGEST_TERMS:
            key_mutation = copy.deepcopy(schema)
            key_mutation["unsafe_digest_key_fixture"] = {term: "placeholder"}
            self.assertIn("raw digest", "\n".join(validator.validate_schema(key_mutation)))

    def test_public_token_field_is_delegated(self):
        schema = load_schema()
        public_token = schema["downstream_contracts"]["public_token"]

        self.assertEqual([66, 63], public_token["owner_issues"])
        self.assertEqual("delegated_not_implemented_in_65", public_token["generation_status"])
        self.assertNotIn("grammar", public_token)

    def test_split_registry_dependencies_are_parseable(self):
        schema = load_schema()
        dependencies = {
            row["issue"]: row["depends_on"]
            for row in schema["wave0_split_registry"]
        }

        self.assertEqual(EXPECTED_SPLIT_DEPENDENCIES, dependencies)

    def test_non_ready_split_registry_rejects_wrong_issue_plan_path(self):
        validator = load_validator()
        schema = load_schema()
        rows = {row["issue"]: row for row in schema["wave0_split_registry"]}
        mutated = copy.deepcopy(schema)
        mutated_rows = {row["issue"]: row for row in mutated["wave0_split_registry"]}

        mutated_rows[66]["plan_path"] = rows[67]["plan_path"]
        mutated_rows[66]["implementation_ready"] = False

        errors = validator.validate_schema(mutated)

        self.assertIn("#66 split plan_path", "\n".join(errors))

    def test_non_ready_split_registry_rejects_empty_plan_path_when_expected_file_exists(self):
        validator = load_validator()
        schema = load_schema()
        mutated = copy.deepcopy(schema)
        rows = {row["issue"]: row for row in mutated["wave0_split_registry"]}

        rows[68]["plan_path"] = ""
        rows[68]["implementation_ready"] = False

        errors = validator.validate_schema(mutated)

        self.assertIn("#68 split plan_path", "\n".join(errors))

    def test_non_ready_split_registry_rejects_invalid_status_snapshot(self):
        validator = load_validator()
        schema = load_schema()
        mutated = copy.deepcopy(schema)
        rows = {row["issue"]: row for row in mutated["wave0_split_registry"]}

        rows[67]["status_snapshot"] = "nonsense-stale-status"
        rows[67]["implementation_ready"] = False

        errors = validator.validate_schema(mutated)

        self.assertIn("#67 split status_snapshot", "\n".join(errors))

    def test_non_ready_split_registry_rejects_status_drift_from_readme(self):
        validator = load_validator()
        schema = load_schema()
        mutated = copy.deepcopy(schema)
        rows = {row["issue"]: row for row in mutated["wave0_split_registry"]}

        rows[66]["status_snapshot"] = "status:blocked-draft"
        rows[66]["implementation_ready"] = False

        errors = validator.validate_schema(mutated)

        self.assertIn("#66 split status_snapshot must match repo-local status", "\n".join(errors))

    def test_split_registry_rejects_lower_precedence_status_contradiction(self):
        validator = load_validator()
        schema = load_schema()
        readme_path = REPO_ROOT / "docs" / "plans" / "README.md"
        with tempfile.TemporaryDirectory() as tmp:
            fake_readme = Path(tmp) / "README.md"
            fake_readme.write_text(readme_path.read_text().replace(
                "| [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) | ace-public-token-fixtures-private-field-placeholders | `docs/plans/2026-06-30-issue-66-ace-public-token-fixtures-private-field-placeholders.md` | 2026-06-30 | plan-review |",
                "| [#66](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/66) | ace-public-token-fixtures-private-field-placeholders | `docs/plans/2026-06-30-issue-66-ace-public-token-fixtures-private-field-placeholders.md` | 2026-06-30 | draft |",
            ))
            original_repo_path = validator._repo_path

            def mapped_repo_path(path: Path) -> Path:
                if Path(path).as_posix() == "docs/plans/README.md":
                    return fake_readme
                return original_repo_path(path)

            validator._repo_path = mapped_repo_path
            try:
                errors = validator.validate_schema(schema)
            finally:
                validator._repo_path = original_repo_path

        self.assertIn("lower-precedence README contradicts", "\n".join(errors))

    def test_split_registry_requires_plan_required_state_when_expected_plan_missing(self):
        validator = load_validator()
        schema = load_schema()
        original_paths = dict(validator.EXPECTED_SPLIT_PLAN_PATHS)

        validator.EXPECTED_SPLIT_PLAN_PATHS[66] = "docs/plans/nonexistent-issue-66-plan.md"
        try:
            errors = validator.validate_schema(schema)
        finally:
            validator.EXPECTED_SPLIT_PLAN_PATHS.clear()
            validator.EXPECTED_SPLIT_PLAN_PATHS.update(original_paths)

        joined = "\n".join(errors)
        self.assertIn("#66 split plan_path must be empty", joined)
        self.assertIn("#66 split status_snapshot must be status:plan-required", joined)

    def test_split_registry_covers_66_67_swapped_regression(self):
        validator = load_validator()
        schema = load_schema()
        rows = {row["issue"]: row for row in schema["wave0_split_registry"]}
        mutated = copy.deepcopy(schema)
        mutated_rows = {row["issue"]: row for row in mutated["wave0_split_registry"]}

        mutated_rows[66]["plan_path"] = rows[67]["plan_path"]
        mutated_rows[66]["implementation_ready"] = False
        mutated_rows[67]["plan_path"] = ""
        mutated_rows[67]["status_snapshot"] = "nonsense-stale-status"
        mutated_rows[67]["implementation_ready"] = False

        errors = "\n".join(validator.validate_schema(mutated))

        self.assertIn("#66 split plan_path", errors)
        self.assertIn("#67 split plan_path", errors)
        self.assertIn("#67 split status_snapshot", errors)

    def test_split_registry_normalizes_current_68_69_rows(self):
        schema = load_schema()
        rows = {row["issue"]: row for row in schema["wave0_split_registry"]}

        self.assertEqual(
            "docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md",
            rows[68]["plan_path"],
        )
        self.assertEqual("status:blocked-draft", rows[68]["status_snapshot"])
        self.assertFalse(rows[68]["implementation_ready"])
        self.assertEqual(
            "docs/plans/2026-07-01-issue-69-repo-local-legal-security-scan-gate.md",
            rows[69]["plan_path"],
        )
        self.assertEqual("status:plan-approved", rows[69]["status_snapshot"])
        self.assertTrue(rows[69]["implementation_ready"])

    def test_split_registry_records_69_dependency_correction(self):
        schema = load_schema()
        rows = {row["issue"]: row for row in schema["wave0_split_registry"]}

        self.assertEqual([65], rows[69]["depends_on"])
        self.assertNotIn(68, rows[69]["depends_on"])

    def test_non_ready_split_registry_allows_no_approval_marker(self):
        validator = load_validator()
        schema = load_schema()
        rows = {row["issue"]: row for row in schema["wave0_split_registry"]}

        self.assertFalse(rows[66]["implementation_ready"])
        self.assertEqual("status:plan-review", rows[66]["status_snapshot"])
        self.assertNotIn("#66 implementation_ready", "\n".join(validator.validate_schema(schema)))

    def test_split_registry_allows_65_implemented_note_with_approval_marker(self):
        validator = load_validator()
        schema = load_schema()

        errors = validator.validate_schema(schema)

        self.assertNotIn("#65 split status_snapshot", "\n".join(errors))

    def test_split_registry_allows_68_readme_draft_coarsening_when_blocked_draft_source_exists(self):
        validator = load_validator()
        schema = load_schema()

        errors = validator.validate_schema(schema)

        self.assertNotIn("#68 split status_snapshot", "\n".join(errors))

    def test_split_registry_uses_68_plan_body_when_coordination_status_is_silent(self):
        validator = load_validator()
        schema = load_schema()
        coordination_path = REPO_ROOT / "docs" / "plans" / "ace-share-ingestion-wave-coordination.md"
        with tempfile.TemporaryDirectory() as tmp:
            fake_coordination = Path(tmp) / "coordination.md"
            fake_coordination.write_text(coordination_path.read_text().replace(
                "blocked-draft: `docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md`",
                "decision pending in plan body: `docs/plans/2026-06-30-issue-68-ace-public-surface-self-scan-control-plane.md`",
            ))
            original_repo_path = validator._repo_path

            def mapped_repo_path(path: Path) -> Path:
                if Path(path).as_posix() == "docs/plans/ace-share-ingestion-wave-coordination.md":
                    return fake_coordination
                return original_repo_path(path)

            validator._repo_path = mapped_repo_path
            try:
                errors = validator.validate_schema(schema)
            finally:
                validator._repo_path = original_repo_path

        self.assertNotIn("#68 split status_snapshot", "\n".join(errors))

    def test_schema_normalizes_status_snapshot_vocabulary(self):
        schema = load_schema()

        for row in schema["wave0_split_registry"]:
            self.assertTrue(row["status_snapshot"].startswith("status:"))

    def test_split_registry_requires_approval_marker_contract(self):
        validator = load_validator()
        schema = load_schema()

        with tempfile.TemporaryDirectory() as tmp:
            errors = validator.validate_schema(schema, approval_root=Path(tmp))
        self.assertIn("#65 implementation_ready", "\n".join(errors))

        mutated = copy.deepcopy(schema)
        for row in mutated["wave0_split_registry"]:
            if row["issue"] == 65:
                row["implementation_ready"] = False
                row["status_snapshot"] = "status:plan-review"
            if row["issue"] == 66:
                row["implementation_ready"] = True
                row["status_snapshot"] = "status:plan-approved"
        with tempfile.TemporaryDirectory() as tmp:
            errors = validator.validate_schema(mutated, approval_root=Path(tmp))
        self.assertIn("#66 implementation_ready", "\n".join(errors))

    def test_wave_registry_compatibility_matches_coordination(self):
        validator = load_validator()
        schema = load_schema()

        self.assertEqual([], validator.validate_coordination_compatibility(schema))

    def test_public_scan_paths_cover_65_artifacts(self):
        validator = load_validator()
        paths = {path.as_posix() for path in validator.public_scan_paths()}

        self.assertTrue(EXPECTED_CORE_PUBLIC_PATHS <= paths)
        review_artifacts = {
            path.relative_to(REPO_ROOT).as_posix()
            for path in (REPO_ROOT / "scripts" / "review" / "results").glob("*plan-65*.md")
        }
        self.assertTrue(review_artifacts <= paths)
        self.assertNotIn("skills/content-triage-and-exclusion/SKILL.md", paths)

    def test_negative_fixtures_are_not_committed_as_raw_examples(self):
        validator = load_validator()
        denied_assignment = source_term("source", "id") + ": raw-value"
        token_assignment = "public_" + "source_token: pst_" + ("0" * 32)
        source_text = VALIDATOR_PATH.read_text() + "\n" + Path(__file__).read_text()

        self.assertNotIn(denied_assignment, source_text)
        self.assertNotIn(token_assignment, source_text)
        self.assertEqual([], validator.validate_public_surfaces())

    def test_validator_source_avoids_denied_recursive_traversal(self):
        source_text = VALIDATOR_PATH.read_text() + "\n" + Path(__file__).read_text()

        self.assertNotIn("os." + "walk(", source_text)
        self.assertNotIn("." + "rglob(", source_text)

    def test_changed_skill_docs_are_scan_clean_or_follow_on(self):
        validator = load_validator()

        self.assertEqual([], validator.changed_bound_skill_docs())
        self.assertEqual("none_discovered", load_schema()["method_gap_disposition"])

    def test_parent_validator_still_passes(self):
        parent = load_module(PARENT_VALIDATOR_PATH, "validate_ace_epic_wave_coordination_for_65")
        result = parent.validate_text(
            (REPO_ROOT / "docs" / "plans" / "ace-share-ingestion-wave-coordination.md").read_text(),
            approval_root=REPO_ROOT / ".planning" / "plan-approved",
        )

        self.assertEqual([], result.errors)

    def test_ci_invokes_wave0_schema_validator_and_scan(self):
        workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()

        self.assertIn("scripts/validate_ace_wave0_schema_contract.py", workflow)
        self.assertIn("tests.test_validate_ace_wave0_schema_contract", workflow)
        self.assertIn("--scan-public-path artifacts/ace-wave0-ledger-schema.json", workflow)


if __name__ == "__main__":
    unittest.main()
