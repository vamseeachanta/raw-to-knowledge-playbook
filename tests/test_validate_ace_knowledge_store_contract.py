from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_knowledge_store_contract.py"
CONTRACT_PATH = REPO_ROOT / "config" / "ace-knowledge-store-contract.json"
SCHEMA_PATH = REPO_ROOT / "artifacts" / "ace-wave0-ledger-schema.json"

EXPECTED_STORAGE_FORMS = {"landing_page", "part_file", "dataset_table", "media_descriptor", "geometry_metadata", "private_sidecar_record", "exclusion_record", "retrieval_chunk", "eval_case"}
EXPECTED_METADATA_GROUPS = {"identity", "routing", "lifecycle", "verification", "provenance", "evaluation", "success"}
EXPECTED_LIFECYCLE_STATES = {"candidate", "provisional", "verified", "rejected", "superseded", "stale_requires_rescreen"}
EXPECTED_CHUNK_METADATA = {"citation_id", "logical_document_key", "edition", "revision", "is_current", "as_of_timestamp", "visibility", "lifecycle_state", "parse_status", "hash_reference", "structure_type", "route_target", "logical_target_store"}
EXPECTED_CORE_PUBLIC_PATHS = {
    "docs/plans/2026-06-29-issue-61-ace-cross-wave-knowledge-store-retrieval-evaluation-lifecycle-contract.md",
    "docs/plans/README.md",
    "docs/plans/ace-share-ingestion-wave-coordination.md",
    ".planning/plan-approved/61.md",
    "docs/case-studies/ace-share-knowledge-store-contract.md",
    "config/ace-knowledge-store-contract.json",
    "config/ace-ingested-success-metric-contract.json",
    "scripts/validate_ace_knowledge_store_contract.py",
    "scripts/validate_ace_ingested_success_metric.py",
    "tests/test_validate_ace_knowledge_store_contract.py",
    "tests/test_validate_ace_ingested_success_metric.py",
    "docs/14-chunking-and-embedding.md",
    "docs/15-retrieval-evaluation.md",
    "docs/16-corpus-lifecycle.md",
    "docs/07-data-governance.md",
    "docs/19-trust-boundary-and-private-mode.md",
    ".github/workflows/validate.yml",
}
BOUND_SKILL_EVAL_PATHS = ["skills/page-shape-contract/evals/evals.json", "skills/source-extraction-coverage/evals/evals.json", "skills/source-extract-fidelity/evals/evals.json", "skills/verify-batch/evals/evals.json", "skills/independent-oracle-validation/evals/evals.json", "skills/public-private-routing/evals/evals.json", "skills/stacked-batch-prs/evals/evals.json"]


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_ace_knowledge_store_contract", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_contract() -> dict:
    return json.loads(CONTRACT_PATH.read_text())


def load_wave0_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


def private_field(*parts: str) -> str:
    return "_".join(parts)


class AceKnowledgeStoreContractTests(unittest.TestCase):
    def test_contract_is_json_and_owned_by_61(self):
        validator = load_validator()
        contract = load_contract()

        self.assertEqual([], validator.validate_contract(contract))
        self.assertEqual("ace-knowledge-store-contract", contract["contract_id"])
        self.assertRegex(contract["contract_version"], r"^1\.0\.\d+$")
        self.assertEqual(61, contract["owner_issue"])
        self.assertEqual(65, contract["depends_on_schema_issue"])
        self.assertEqual(62, contract["depends_on_manifest_evidence_issue"])
        self.assertEqual(63, contract["publication_gate_issue"])

    def test_storage_forms_are_closed_set(self):
        validator = load_validator()
        contract = load_contract()

        self.assertEqual(EXPECTED_STORAGE_FORMS, set(contract["storage_forms"]))

        mutated = copy.deepcopy(contract)
        mutated["storage_forms"].append("physical_vector_database")
        self.assertIn("storage form", "\n".join(validator.validate_contract(mutated)))

    def test_storage_forms_have_required_metadata_groups(self):
        validator = load_validator()
        contract = load_contract()

        metadata = contract["required_metadata_by_storage_form"]
        self.assertEqual(EXPECTED_STORAGE_FORMS, set(metadata))
        for form, form_contract in metadata.items():
            self.assertTrue(EXPECTED_METADATA_GROUPS <= set(form_contract["field_groups"]), form)

        mutated = copy.deepcopy(contract)
        mutated["required_metadata_by_storage_form"]["retrieval_chunk"]["field_groups"].remove("evaluation")
        self.assertIn("metadata group", "\n".join(validator.validate_contract(mutated)))

    def test_imports_65_route_store_without_redefinition(self):
        validator = load_validator()
        contract = load_contract()
        schema = load_wave0_schema()
        dependency = contract["route_store_dependency"]

        self.assertEqual(65, dependency["owner_issue"])
        self.assertEqual("artifacts/ace-wave0-ledger-schema.json", dependency["schema_path"])
        self.assertEqual("import_only", dependency["mode"])
        self.assertNotIn("route_targets", contract)
        self.assertNotIn("route_store_matrix", contract)
        self.assertEqual(set(schema["route_targets"]), set(validator.load_wave0_schema()["route_targets"]))

        mutated = copy.deepcopy(contract)
        mutated["route_targets"] = ["public_llm_wiki"]
        self.assertIn("redefine #65", "\n".join(validator.validate_contract(mutated)))

        bad_dependency = copy.deepcopy(contract)
        bad_dependency["route_store_dependency"]["validator_path"] = "scripts/other.py"
        self.assertIn("route/store dependency", "\n".join(validator.validate_contract(bad_dependency)))

        bad_schema = copy.deepcopy(schema)
        bad_schema["route_targets"].append("unexpected_route")
        bad_schema["route_store_matrix"]["unexpected_route"] = "/" + "mnt" + "/ace/private-store"
        with tempfile.TemporaryDirectory() as tmpdir:
            bad_schema_path = Path(tmpdir) / "bad-schema.json"
            bad_schema_path.write_text(json.dumps(bad_schema))
            self.assertIn("#65 route/store schema", "\n".join(validator.validate_contract(contract, bad_schema_path)))

    def test_lifecycle_state_machine_is_closed(self):
        validator = load_validator()
        contract = load_contract()

        self.assertEqual(EXPECTED_LIFECYCLE_STATES, set(contract["lifecycle_states"]))

        unknown_state = copy.deepcopy(contract)
        unknown_state["lifecycle_states"].append("trusted")
        self.assertIn("lifecycle state", "\n".join(validator.validate_contract(unknown_state)))

        forbidden_transition = copy.deepcopy(contract)
        forbidden_transition["lifecycle_transitions"].append(
            {"from": "stale_requires_rescreen", "to": "verified", "reason_required": "manual_override"}
        )
        self.assertIn("lifecycle transition", "\n".join(validator.validate_contract(forbidden_transition)))

    def test_rescreen_transition_reaches_verified_again(self):
        validator = load_validator()
        valid_events = [
            {"from": "candidate", "to": "stale_requires_rescreen", "reason": "source_or_policy_change"},
            {
                "from": "stale_requires_rescreen",
                "to": "provisional",
                "reason": "confidentiality_rescreen_passed",
                "rescreen_evidence_ref": "evidence:synthetic",
            },
            {"from": "provisional", "to": "verified", "reason": "independent_verification"},
        ]
        invalid_events = [
            {"from": "stale_requires_rescreen", "to": "verified", "reason": "manual_override"},
        ]
        bad_reason_events = [
            {"from": "verified", "to": "superseded", "reason": "manual_override"},
        ]
        missing_rescreen_evidence = [
            {"from": "stale_requires_rescreen", "to": "rejected", "reason": "rescreen_failure"},
        ]

        self.assertEqual([], validator.validate_lifecycle_events(valid_events))
        self.assertIn("transition", "\n".join(validator.validate_lifecycle_events(invalid_events)))
        self.assertIn("reason", "\n".join(validator.validate_lifecycle_events(bad_reason_events)))
        self.assertIn("rescreen evidence", "\n".join(validator.validate_lifecycle_events(missing_rescreen_evidence)))

    def test_storage_record_drift_requires_stale_rescreen(self):
        validator = load_validator()
        previous = {
            "lifecycle_state": "verified",
            "source_fingerprint_ref": "hashref:old",
            "manifest_snapshot_id": "ams_00000000000000000000000000000001",
            "route_target": "metadata_only",
            "logical_target_store": "metadata_ledger_store",
            "visibility": "private",
            "parser_version": "parser-1",
        }
        current = dict(previous)
        current["parser_version"] = "parser-2"

        self.assertIn("stale_requires_rescreen", "\n".join(validator.validate_storage_record_update(previous, current)))

        current["lifecycle_state"] = "stale_requires_rescreen"
        self.assertEqual([], validator.validate_storage_record_update(previous, current))

    def test_enum_owner_map_keeps_status_vocabularies_separate(self):
        validator = load_validator()
        contract = load_contract()
        owners = contract["enum_owner_map"]

        self.assertEqual(65, owners["route_target"]["owner_issue"])
        self.assertEqual(61, owners["lifecycle_state"]["owner_issue"])
        self.assertEqual("page-shape-contract", owners["page_shape_parse_status"]["owner_skill"])
        self.assertEqual(62, owners["manifest_freshness_status"]["owner_issue"])
        self.assertEqual(63, owners["publication_certification_status"]["owner_issue"])

        mutated = copy.deepcopy(contract)
        mutated["enum_owner_map"]["route_target"]["owner_issue"] = 61
        self.assertIn("enum owner", "\n".join(validator.validate_contract(mutated)))

    def test_public_contract_uses_private_provenance_bundle_only(self):
        validator = load_validator()
        contract = load_contract()
        private_term = private_field("source", "id")
        public_token_value = "pst_" + ("0" * 32)

        self.assertIn("private_provenance_bundle_ref", contract["private_provenance_policy"]["allowed_public_fields"])

        private_key = copy.deepcopy(contract)
        private_key["unsafe_private_fixture"] = {private_term: "raw-value"}
        self.assertIn("private source field", "\n".join(validator.validate_contract(private_key)))

        token_value = copy.deepcopy(contract)
        token_value["unsafe_token_fixture"] = {"public_" + private_field("source", "token"): public_token_value}
        self.assertIn("public token value", "\n".join(validator.validate_contract(token_value)))

        extra_public_field = copy.deepcopy(contract)
        extra_public_field["private_provenance_policy"]["allowed_public_fields"].append(
            private_field("private", "lookup", "map")
        )
        self.assertIn("private provenance", "\n".join(validator.validate_contract(extra_public_field)))

    def test_publication_gate_blocks_exposure_until_63_canary(self):
        validator = load_validator()
        contract = load_contract()
        gate = contract["publication_gate"]

        self.assertEqual(63, gate["owner_issue"])
        self.assertIs(gate["publication_exposure_allowed"], False)
        self.assertIn("docs_navigation", gate["blocked_public_surfaces"])
        self.assertIn("mkdocs_yml", gate["blocked_public_surfaces"])
        self.assertIn("llm_wiki", gate["blocked_public_surfaces"])
        self.assertIn("derived_public_summaries", gate["blocked_public_surfaces"])

        unsafe = copy.deepcopy(contract)
        unsafe["publication_gate"]["publication_exposure_allowed"] = True
        self.assertIn("publication gate", "\n".join(validator.validate_contract(unsafe)))

    def test_retrieval_chunk_metadata_required_and_tables_preserve_structure(self):
        validator = load_validator()
        contract = load_contract()

        self.assertEqual(EXPECTED_CHUNK_METADATA, set(contract["retrieval_chunk_required_metadata"]))
        valid_chunk = {field: "synthetic" for field in EXPECTED_CHUNK_METADATA}
        valid_chunk.update(
            {
                "is_current": True,
                "structure_type": "table",
                "table_preserved": True,
                "lifecycle_state": "verified",
                "parse_status": "parse_succeeded",
                "visibility": "private",
                "hash_reference": "hashref:synthetic",
                "route_target": "metadata_only",
                "logical_target_store": "metadata_ledger_store",
            }
        )
        self.assertEqual([], validator.validate_retrieval_chunk_record(valid_chunk))

        missing = copy.deepcopy(valid_chunk)
        missing.pop("citation_id")
        self.assertIn("retrieval chunk metadata", "\n".join(validator.validate_retrieval_chunk_record(missing)))

        split_table = copy.deepcopy(valid_chunk)
        split_table["table_preserved"] = False
        self.assertIn("table structure", "\n".join(validator.validate_retrieval_chunk_record(split_table)))

        bad_visibility = copy.deepcopy(valid_chunk)
        bad_visibility["visibility"] = "public_unreviewed"
        self.assertIn("visibility", "\n".join(validator.validate_retrieval_chunk_record(bad_visibility)))

        bad_parse_status = copy.deepcopy(valid_chunk)
        bad_parse_status["parse_status"] = "trusted"
        self.assertIn("parse_status", "\n".join(validator.validate_retrieval_chunk_record(bad_parse_status)))

        raw_hash = copy.deepcopy(valid_chunk)
        raw_hash["hash_reference"] = "0" * 64
        self.assertIn("hash_reference", "\n".join(validator.validate_retrieval_chunk_record(raw_hash)))

        bad_store = copy.deepcopy(valid_chunk)
        bad_store["logical_target_store"] = "public_llm_wiki_store"
        self.assertIn("route-store", "\n".join(validator.validate_retrieval_chunk_record(bad_store)))

    def test_golden_eval_is_excluded_from_ingest_and_chunk_store(self):
        validator = load_validator()
        valid_case = {
            "case_id": "golden-synthetic-1",
            "eval_tier": "golden",
            "storage_form": "eval_case",
            "outside_ingest_path": True,
            "outside_chunk_store": True,
        }
        bad_case = copy.deepcopy(valid_case)
        bad_case["outside_chunk_store"] = False

        self.assertEqual([], validator.validate_eval_case_record(valid_case))
        self.assertIn("eval leakage", "\n".join(validator.validate_eval_case_record(bad_case)))

    def test_no_ace_share_root_or_raw_manifest_reads(self):
        validator = load_validator()
        root_token = "ACE_" + "SHARE_ROOT"
        denied_text = "\n".join(
            [
                " ".join(["fi" + "nd", root_token, "-type", "f"]),
                " ".join(["ca" + "t", root_token, "assets" + ".json"]),
                " ".join(["sha256" + "sum", "docs/master" + "-index.jsonl"]),
                "os" + ".walk(source_root)",
                "." + "rglob('*')",
            ]
        )
        allowed_text = "Path('tests/fixtures/ace-knowledge-store-contract').glob('*.json')"

        self.assertIn("source traversal", "\n".join(validator.validate_source_read_policy(denied_text)))
        self.assertEqual([], validator.validate_source_read_policy(allowed_text))

    def test_public_scan_paths_cover_61_artifacts(self):
        validator = load_validator()
        paths = {path.as_posix() for path in validator.public_scan_paths()}

        self.assertTrue(EXPECTED_CORE_PUBLIC_PATHS <= paths)
        for skill_path in BOUND_SKILL_EVAL_PATHS:
            self.assertIn(skill_path, paths)

    def test_coordination_row_lists_all_61_skill_eval_bindings(self):
        coordination = (REPO_ROOT / "docs" / "plans" / "ace-share-ingestion-wave-coordination.md").read_text()
        issue_61_row = next(
            line
            for line in coordination.splitlines()
            if line.startswith("| #61 |") and "issue-61-ace-cross-wave" in line
        )

        self.assertIn("eval bindings", issue_61_row)
        for skill_path in BOUND_SKILL_EVAL_PATHS:
            self.assertIn(skill_path, issue_61_row)

    def test_readme_gate_wording_separates_61_closeout_from_63_publication(self):
        readme = (REPO_ROOT / "docs" / "plans" / "README.md").read_text()
        doc_07 = (REPO_ROOT / "docs" / "07-data-governance.md").read_text()
        doc_19 = (REPO_ROOT / "docs" / "19-trust-boundary-and-private-mode.md").read_text()

        self.assertIn("implemented validators", readme)
        self.assertIn("implementation cross-review closeout", readme)
        self.assertIn("Public docs navigation", readme)
        self.assertIn("implemented canary", readme)
        self.assertNotIn("until [#61](https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/61) is approved.", readme)
        self.assertIn("raw source digest values stay private-sidecar only", doc_07)
        self.assertIn("raw source digest values stay private-sidecar only", doc_19)
        self.assertNotIn("sha256 pointer only", doc_19)
        self.assertNotIn("always safe", doc_19)

    def test_skill_evals_include_61_metadata_cases(self):
        validator = load_validator()

        for skill_path in BOUND_SKILL_EVAL_PATHS:
            errors = validator.validate_skill_eval_file(REPO_ROOT / skill_path)
            self.assertEqual([], errors, skill_path)
            evals = json.loads((REPO_ROOT / skill_path).read_text())["evals"]
            matching = [case for case in evals if case.get("issue") == 61]
            self.assertTrue(matching, skill_path)
            self.assertTrue(all(case["id"].startswith("ace-61-") for case in matching), skill_path)

    def test_ci_invokes_61_validators_and_unit_tests(self):
        workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()

        self.assertIn("scripts/validate_ace_knowledge_store_contract.py", workflow)
        self.assertIn("scripts/validate_ace_ingested_success_metric.py", workflow)
        self.assertIn("--chunk-record tests/fixtures/ace-knowledge-store-contract/valid-retrieval-chunk.json", workflow)
        self.assertIn("--eval-record tests/fixtures/ace-knowledge-store-contract/valid-eval-case.json", workflow)
        self.assertIn("docs/14-chunking-and-embedding.md", workflow)
        self.assertIn("docs/15-retrieval-evaluation.md", workflow)
        self.assertIn("docs/16-corpus-lifecycle.md", workflow)
        self.assertIn("docs/07-data-governance.md", workflow)
        self.assertIn("docs/19-trust-boundary-and-private-mode.md", workflow)
        self.assertIn("tests.test_validate_ace_knowledge_store_contract", workflow)
        self.assertIn("tests.test_validate_ace_ingested_success_metric", workflow)


if __name__ == "__main__":
    unittest.main()
