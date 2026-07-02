from __future__ import annotations

from tests.ace_public_surface_test_helpers import *
import importlib


class AcePublicSurfaceContractTests(unittest.TestCase):
    def test_contract_is_json_and_owned_by_68(self):
        contract = load_json(CONTRACT_PATH)

        self.assertEqual("ace-public-surface-self-scan-contract", contract["contract_id"])
        self.assertRegex(contract["contract_version"], r"^1\.0\.\d+$")
        self.assertEqual(68, contract["owner_issue"])
        self.assertEqual("repo_local_public_surface_self_scan", contract["mode"])
        self.assertEqual(63, contract["private_deny_list_owner_issue"])
        self.assertEqual({"65", "66", "69"}, set(contract["boundary_owner_issues"]))

    def test_contract_imports_66_without_drift(self):
        validator = load_validator()
        contract = load_json(CONTRACT_PATH)
        token_contract = load_json(TOKEN_CONTRACT_PATH)

        imported = contract["upstream_contracts"]["public_token_fixture_contract"]
        self.assertEqual("config/ace-public-token-fixture-contract.json", imported["path"])
        self.assertEqual(66, imported["owner_issue"])
        self.assertIn("generation_request_required_keys", imported["imported_fields"])
        for field in imported["imported_fields"]:
            self.assertEqual(token_contract[field], imported["imported_values"][field])
        self.assertEqual([], validator.validate_contract_file(CONTRACT_PATH))

    def test_contract_defines_closed_scan_policy(self):
        contract = load_json(CONTRACT_PATH)

        deny_ids = {item["id"] for item in contract["deny_classes"]}
        self.assertTrue(
            {
                "raw-host-path",
                "personal-identifier",
                "confidentiality-marker",
                "private-source-key",
                "source-like-key",
                "forbidden-request-key",
                "provider-sidecar-leak",
                "unbounded-traversal-command",
                "metadata-evidence-path",
                "generic-private-identifier",
            }.issubset(deny_ids)
        )
        context_ids = {item["id"] for item in contract["allow_contexts"]}
        self.assertEqual({"schema-term-policy-prose", "review-artifact-forensics"}, context_ids)
        suffixes = set(contract["sidecar_selector"]["suffixes"])
        self.assertEqual({".err", ".stderr", ".stdout", ".json", ".log", ".trace"}, suffixes)
        providers = set(contract["review_artifact_selector"]["provider_enum"])
        self.assertEqual(
            {"claude", "codex", "gemini", "subagent-boundary", "subagent-scanner", "subagent-workflow"},
            providers,
        )

    def test_contract_forbids_blanket_exemptions_and_live_ci_auth(self):
        contract = load_json(CONTRACT_PATH)

        self.assertFalse(contract["stock_ci_live_github_dependency"])
        self.assertNotIn("whole_file_exemptions", contract)
        self.assertNotIn("whole_directory_exemptions", contract)
        self.assertEqual([], contract["allow_contexts"][0].get("whole_file_exemptions", []))
        self.assertEqual([], contract["allow_contexts"][1].get("whole_directory_exemptions", []))
        self.assertEqual(
            [
                "schema_version",
                "issue_number",
                "comment_id",
                "url",
                "source_kind",
                "phase",
                "fetched_at",
                "body_sha256",
                "body",
            ],
            contract["issue_comment_snapshot_schema"]["top_level_keys"],
        )

    def test_package_import_facade_works_from_repo_root(self):
        module = importlib.import_module("scripts.ace_public_surface_scan")

        self.assertTrue(hasattr(module, "validate_public_artifact_paths"))


if __name__ == "__main__":
    unittest.main()
