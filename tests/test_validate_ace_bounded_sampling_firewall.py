from __future__ import annotations
import copy
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_bounded_sampling_firewall.py"
LIBRARY_PATH = REPO_ROOT / "scripts" / "ace_bounded_sampling_firewall.py"
CONTRACT_PATH = REPO_ROOT / "config" / "ace-bounded-sampling-firewall-contract.json"
SCHEMA_PATH = REPO_ROOT / "artifacts" / "ace-wave0-ledger-schema.json"
MANIFEST_CONTRACT_PATH = REPO_ROOT / "config" / "ace-manifest-evidence-contract.json"
GOOD_FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "ace-bounded-sampling-firewall" / "good-request.json"
SHAPE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "ace-bounded-sampling-firewall"
    / "metadata-shape-only-evidence-request.json"
)
PARENT_VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_epic_wave_coordination.py"
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "validate.yml"
def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
def load_library():
    return load_module(LIBRARY_PATH, "ace_bounded_sampling_firewall")
def load_validator():
    return load_module(VALIDATOR_PATH, "validate_ace_bounded_sampling_firewall")
def load_parent_validator():
    return load_module(PARENT_VALIDATOR_PATH, "validate_ace_epic_wave_coordination_for_67")
def load_json(path: Path) -> dict:
    return json.loads(path.read_text())
def source_term(*parts: str) -> str:
    return "_".join(parts)
def good_request() -> dict:
    return load_json(GOOD_FIXTURE_PATH)
def downstream_request() -> dict:
    request = copy.deepcopy(good_request())
    request["target_issue"] = 52
    request["request_class"] = "downstream_manifest_backed_sampling"
    request["target_wave_class"] = "ingestion_wave"
    request["requires_manifest_snapshot_id"] = True
    request.pop("fixture_scope", None)
    request["snapshot_evidence"] = {
        "evidence_mode": "blocked_pending_62_contract",
        "source_issue": 62,
        "blocked_by_issue": 62,
        "follow_on_issue": 70,
        "reason_code": "MISSING_62_EVIDENCE_CONTRACT",
        "recorded_at": "2026-07-01",
    }
    return request
class AceBoundedSamplingFirewallTests(unittest.TestCase):
    def test_contract_file_is_json_and_owned_by_67(self):
        contract = load_json(CONTRACT_PATH)
        self.assertEqual("ace-bounded-sampling-firewall", contract["contract_id"])
        self.assertRegex(contract["contract_version"], r"^1\.0\.\d+$")
        self.assertEqual(67, contract["owner_issue"])
        self.assertEqual(65, contract["depends_on_schema_issue"])
        self.assertEqual([1, 12], contract["method_issue_bindings"])
        self.assertTrue(contract["public_safety_notes"])
    def test_contract_imports_65_schema_terms_and_62_manifest_keys(self):
        schema = load_json(SCHEMA_PATH)
        manifest_contract = load_json(MANIFEST_CONTRACT_PATH)
        contract = load_json(CONTRACT_PATH)
        self.assertEqual(manifest_contract["manifest_source_keys"], contract["allowed_manifest_sources"])
        self.assertEqual(
            schema["route_store_matrix"]["metadata_only"],
            contract["output_shape_route_store"]["logical_target_store"],
        )
        self.assertEqual("metadata_only", contract["output_shape_route_store"]["route_target"])
        self.assertNotIn("route_store_matrix", contract)
        self.assertNotIn("private_source_field_terms", contract)
        library = load_library()
        drifted = copy.deepcopy(schema)
        {row["issue"]: row for row in drifted["canonical_wave_registry"]}[52]["requires_manifest_snapshot_id"] = False
        self.assertIn("canonical registry", "\n".join(library.validate_contract(contract, drifted, manifest_contract)))
    def test_validator_accepts_committed_contract_and_fixtures(self):
        validator = load_validator()
        self.assertEqual([], validator.validate_contract_file(CONTRACT_PATH))
        self.assertEqual([], validator.validate_request_file(GOOD_FIXTURE_PATH))
        self.assertEqual([], validator.validate_request_file(SHAPE_FIXTURE_PATH))
    def test_required_sampling_json_keys_are_exact(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        base = good_request()
        self.assertTrue(library.validate_sampling_request(base, contract).authorized)
        for key in contract["required_sampling_fields"]:
            mutated = copy.deepcopy(base)
            mutated.pop(key)
            with self.subTest(missing=key):
                self.assertFalse(library.validate_sampling_request(mutated, contract).authorized)
        for extra in ["target_wave_class", "raw_query", "command_example"]:
            mutated = copy.deepcopy(base)
            mutated[extra] = "not-allowed"
            with self.subTest(extra=extra):
                self.assertFalse(library.validate_sampling_request(mutated, contract).authorized)
    def test_output_shape_route_store_is_metadata_only(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        request = good_request()
        for field, bad_value in [
            ("output_shape", "public_llm_wiki_record"),
            ("route_target", "public_llm_wiki"),
            ("logical_target_store", "public_llm_wiki_store"),
        ]:
            mutated = copy.deepcopy(request)
            mutated[field] = bad_value
            with self.subTest(field=field):
                result = library.validate_sampling_request(mutated, contract)
                self.assertFalse(result.authorized)
                self.assertIn("metadata_only", "\n".join(result.errors))
    def test_sampling_caps_seed_and_sort_rule_are_enforced(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        request = good_request()
        cases = [
            ("per_bucket_row_cap", 201, "cap"),
            ("max_files_touched", 26, "cap"),
            ("max_bytes_touched", 1048577, "cap"),
            ("seed_id", "random-clock-local", "seed"),
            ("sort_rule", {"strategy": "stable_private_term_order"}, "sort_rule"),
        ]
        for field, value, expected in cases:
            mutated = copy.deepcopy(request)
            mutated[field] = value
            result = library.validate_sampling_request(mutated, contract)
            with self.subTest(field=field):
                self.assertFalse(result.authorized)
                self.assertIn(expected, "\n".join(result.errors))
        mutated = copy.deepcopy(request)
        mutated["sort_rule"]["term_refs"] = [source_term("source", "id") + "=raw"]
        self.assertFalse(library.validate_sampling_request(mutated, contract).authorized)
    def test_request_class_mapping_covers_every_recognized_target_outcome(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        self.assertTrue(library.validate_sampling_request(good_request(), contract).authorized)
        for issue in [51, 61, 62, 63]:
            request = copy.deepcopy(good_request())
            request["target_issue"] = issue
            request["request_class"] = "control_plane_proof"
            request["target_wave_class"] = {
                51: "control_plane",
                61: "storage_lifecycle_gate",
                62: "manifest_freshness_gate",
                63: "public_canary_gate",
            }[issue]
            request.pop("fixture_scope", None)
            result = library.validate_sampling_request(request, contract)
            with self.subTest(issue=issue):
                self.assertFalse(result.authorized)
                self.assertEqual("CONTROL_PLANE_PROOF_NOT_SAMPLING_REQUEST", result.reason_code)
        for issue in [64, 66, 68, 69]:
            request = copy.deepcopy(good_request())
            request["target_issue"] = issue
            result = library.validate_sampling_request(request, contract)
            with self.subTest(issue=issue):
                self.assertFalse(result.authorized)
                self.assertEqual("NON_TARGET_SAMPLING_ISSUE", result.reason_code)
    def test_downstream_operational_sampling_blocked_until_70(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        result = library.validate_sampling_request(downstream_request(), contract)
        self.assertFalse(result.authorized)
        self.assertEqual("MISSING_62_EVIDENCE_CONTRACT", result.reason_code)
        self.assertEqual(62, result.blocked_by_issue)
    def test_snapshot_evidence_fields_are_mode_specific(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        shape_fixture = load_json(SHAPE_FIXTURE_PATH)
        self.assertTrue(library.validate_sampling_request(shape_fixture, contract).authorized)
        bad_shape = copy.deepcopy(shape_fixture)
        bad_shape["snapshot_evidence"]["blocked_by_issue"] = 62
        self.assertFalse(library.validate_sampling_request(bad_shape, contract).authorized)
        bad_blocked = downstream_request()
        bad_blocked["snapshot_evidence"].pop("follow_on_issue")
        self.assertFalse(library.validate_sampling_request(bad_blocked, contract).authorized)
        live_claim = downstream_request()
        live_claim["snapshot_evidence"] = {"evidence_mode": "operational_live", "source_issue": 62}
        result = library.validate_sampling_request(live_claim, contract)
        self.assertFalse(result.authorized)
        self.assertEqual("MISSING_62_EVIDENCE_CONTRACT", result.reason_code)
    def test_placeholder_snapshot_evidence_fails(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        for value in ["pending", "not-run", "expected-only", "todo"]:
            request = downstream_request()
            request["snapshot_evidence"]["recorded_at"] = value
            with self.subTest(value=value):
                result = library.validate_sampling_request(request, contract)
                self.assertFalse(result.authorized)
                self.assertIn("placeholder", "\n".join(result.errors))
    def test_classifier_distinguishes_policy_prose_from_executable_context(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        prose = "Policy names recursive traversal and raw manifest read as denied classes."
        self.assertTrue(library.classify_executable_context(prose, "markdown_policy_prose", contract).allowed)
        denied = library.build_runtime_deny_fixture("raw_manifest_read", "INDEX.md", contract)
        result = library.classify_executable_context(denied, "markdown_fence", contract)
        self.assertFalse(result.allowed)
        self.assertEqual("DENIED_EXECUTABLE_CONTEXT", result.reason_code)
    def test_manifest_operation_cross_product_denies_every_source_and_operation(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        operations = ["manifest_query", "raw_manifest_read", "full_file_count", "full_file_digest", "materialization"]
        for source in contract["allowed_manifest_sources"]:
            for operation in operations:
                with self.subTest(source=source, operation=operation):
                    result = library.validate_manifest_operation(source, operation, contract)
                    self.assertFalse(result.allowed)
                    self.assertEqual("DENIED_MANIFEST_OPERATION", result.reason_code)
        result = library.validate_manifest_operation("INDEX.md", "bounded_sample_selection", contract)
        self.assertFalse(result.allowed)
        self.assertEqual("MISSING_62_EVIDENCE_CONTRACT", result.reason_code)
    def test_json_executable_context_fields_scan_before_schema_rejection(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        for field in contract["json_executable_context_fields"]:
            request = copy.deepcopy(good_request())
            request[field] = library.build_runtime_deny_fixture("manifest_query", "assets.json", contract)
            with self.subTest(field=field):
                result = library.validate_sampling_request(request, contract)
                self.assertFalse(result.authorized)
                self.assertEqual("DENIED_EXECUTABLE_CONTEXT", result.reason_code)
    def test_source_root_guard_blocks_before_private_filesystem_access(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        env = {"ACE_SHARE_ROOT": "sentinel-share-root"}
        with mock.patch("pathlib.Path.exists", side_effect=AssertionError("filesystem touched")):
            result = library.classify_executable_context(
                library.build_runtime_deny_fixture("broad_source_root_search", "INDEX.md", contract),
                "python_string",
                contract,
                env=env,
            )
        self.assertFalse(result.allowed)
        self.assertEqual("ACE_SOURCE_ROOT_ACCESS_FORBIDDEN", result.reason_code)
    def test_ambient_source_root_env_is_refused(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        with mock.patch.dict(os.environ, {"ACE_SHARE_ROOT": "sentinel-share-root"}):
            result = library.validate_sampling_request(good_request(), contract)
        self.assertFalse(result.authorized)
        self.assertEqual("ACE_SOURCE_ROOT_ACCESS_FORBIDDEN", result.reason_code)
    def test_glob_source_root_context_is_denied(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        source_root = "ACE_" + "SHARE_ROOT"
        samples = [
            "pathlib.Path(${" + source_root + "}/INDEX.md)." + "glob(" + "'**/*')",
            "cp ${" + source_root + "}/INDEX.md /tmp/x",
            "rsync ${" + source_root + "}/INDEX.md /tmp/x",
            "tar cf /tmp/x.tar ${" + source_root + "}/INDEX.md",
            "sqlite3 ${" + source_root + "}/.ace-knowledge/index.db .dump",
            "du ${" + source_root + "}/INDEX.md",
        ]
        for text in samples:
            result = library.classify_executable_context(text, "python_string", contract)
            self.assertFalse(result.allowed)
            self.assertEqual("DENIED_EXECUTABLE_CONTEXT", result.reason_code)
    def test_source_root_guard_call_sites_are_enforced(self):
        library = load_library()
        contract = load_json(CONTRACT_PATH)
        calls: list[str] = []
        def fake_guard(operation_name, env=None):
            calls.append(operation_name)
            return None
        with mock.patch.object(library, "guard_no_source_root_access", side_effect=fake_guard):
            library.validate_sampling_request(good_request(), contract)
            library.classify_executable_context(
                library.build_runtime_deny_fixture("manifest_query", "INDEX.md", contract),
                "markdown_fence",
                contract,
            )
            library.validate_manifest_operation("INDEX.md", "raw_manifest_read", contract)
            library.build_runtime_deny_fixture("raw_manifest_read", "INDEX.md", contract)
        self.assertEqual(
            {
                "validate_sampling_request",
                "classify_executable_context",
                "validate_manifest_operation",
                "build_runtime_deny_fixture",
            },
            set(calls),
        )
    def test_public_scan_paths_cover_67_artifacts(self):
        validator = load_validator()
        paths = {path.as_posix() for path in validator.public_scan_paths()}
        expected = {
            "docs/plans/2026-06-30-issue-67-ace-wave-0-bounded-sampling-firewall.md",
            "config/ace-bounded-sampling-firewall-contract.json",
            "scripts/ace_bounded_sampling_firewall.py",
            "scripts/validate_ace_bounded_sampling_firewall.py",
            "tests/test_validate_ace_bounded_sampling_firewall.py",
            "tests/fixtures/ace-bounded-sampling-firewall/good-request.json",
            "tests/fixtures/ace-bounded-sampling-firewall/metadata-shape-only-evidence-request.json",
            "artifacts/ace-wave0-ledger-schema.json",
            ".github/workflows/validate.yml",
            ".planning/plan-approved/67.md",
        }
        self.assertTrue(expected <= paths)
        self.assertEqual([], validator.validate_public_surfaces())
    def test_review_artifacts_are_included_and_sidecars_block(self):
        library = load_library()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "2026-07-01-implementation-67-review-r1.md").write_text("## Verdict\nMINOR\n")
            (root / "2026-07-01-implementation-67-review-r1.stderr").write_text("stderr")
            paths = [path.as_posix() for path in library.review_artifact_paths(root)]
            errors = library.validate_review_sidecars(root)
        self.assertIn("2026-07-01-implementation-67-review-r1.md", paths)
        self.assertIn("sidecar", "\n".join(errors))
    def test_ci_invokes_67_validator_unit_tests_and_parent_scan(self):
        workflow = WORKFLOW_PATH.read_text()
        self.assertIn("uv run python scripts/validate_ace_bounded_sampling_firewall.py", workflow)
        self.assertIn("uv run python -m unittest tests.test_validate_ace_bounded_sampling_firewall", workflow)
        self.assertIn("--scan-public-path config/ace-bounded-sampling-firewall-contract.json", workflow)
    def test_schema_and_parent_validators_still_pass(self):
        schema_validator = load_module(REPO_ROOT / "scripts" / "validate_ace_wave0_schema_contract.py", "schema_for_67")
        parent = load_parent_validator()
        self.assertEqual([], schema_validator.validate_schema_file())
        coordination = REPO_ROOT / "docs" / "plans" / "ace-share-ingestion-wave-coordination.md"
        result = parent.validate_text(
            coordination.read_text(),
            approval_root=REPO_ROOT / ".planning" / "plan-approved",
        )
        self.assertEqual([], result.errors)
if __name__ == "__main__":
    unittest.main()
