from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LIBRARY_PATH = REPO_ROOT / "scripts" / "ace_public_output_contract.py"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_public_artifacts.py"
TOKEN_CONTRACT_PATH = REPO_ROOT / "config" / "ace-public-token-fixture-contract.json"
OUTPUT_CONTRACT_PATH = REPO_ROOT / "config" / "ace-public-output-contract.json"
DENY_LIST_PATH = REPO_ROOT / "config" / "ace-public-surface-deny-list.json"
SWEEP_PATH = REPO_ROOT / "artifacts" / "ace-source-hash-policy-sweep.md"
CONTRACT_DOC_PATH = REPO_ROOT / "docs" / "case-studies" / "ace-public-output-redaction-contract.md"
SKILL_EVAL_PATH = REPO_ROOT / "skills" / "public-private-routing" / "evals" / "evals.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_library():
    return load_module(LIBRARY_PATH, "ace_public_output_contract")


def load_validator():
    return load_module(VALIDATOR_PATH, "validate_ace_public_artifacts")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def source_term(*parts: str) -> str:
    return "_".join(parts)


def private_root() -> str:
    return "/" + "mnt" + "/" + "ace" + "/" + "private" + "/" + "record.txt"


def email_value() -> str:
    return "owner" + "@" + "example.com"


def token_value() -> str:
    return "pst_" + ("0" * 32)


def digest_value() -> str:
    return "0123456789abcdef" * 4


class AcePublicArtifactValidationTests(unittest.TestCase):
    def test_public_output_contract_imports_66_terms_and_closes_handoff(self):
        library = load_library()
        token_contract = load_json(TOKEN_CONTRACT_PATH)
        output_contract = load_json(OUTPUT_CONTRACT_PATH)

        self.assertFalse(token_contract["provisional_fixture_contract"])
        self.assertEqual([], library.validate_public_output_contract(output_contract, token_contract=token_contract))
        self.assertEqual(token_contract["public_token_field_name"], output_contract["public_token_field_name"])
        self.assertEqual(token_contract["public_token_grammar"], output_contract["public_token_grammar"])
        self.assertEqual([token_contract["public_token_field_name"]], output_contract["public_safe_source_reference_fields"])
        self.assertEqual(token_contract["private_source_terms"], output_contract["private_only_provenance_fields"])
        self.assertEqual(token_contract["source_like_raw_digest_terms"], output_contract["source_like_raw_digest_terms"])

    def test_public_output_contract_rejects_private_inventory_keys(self):
        library = load_library()
        token_contract = load_json(TOKEN_CONTRACT_PATH)
        output_contract = load_json(OUTPUT_CONTRACT_PATH)
        bad_contract = deepcopy(output_contract)
        bad_contract["client_names"] = ["fixture"]

        errors = library.validate_public_output_contract(bad_contract, token_contract=token_contract)

        self.assertIn("forbidden inventory key", "\n".join(errors))

    def test_public_deny_list_supplement_is_public_safe(self):
        library = load_library()
        deny_list = load_json(DENY_LIST_PATH)

        self.assertEqual([], library.validate_deny_list_supplement(deny_list))
        bad_deny_list = deepcopy(deny_list)
        bad_deny_list["private_roots"] = ["fixture"]

        self.assertIn("forbidden inventory key", "\n".join(library.validate_deny_list_supplement(bad_deny_list)))

    def test_source_hash_policy_sweep_classifies_without_raw_digests(self):
        library = load_library()
        sweep_text = SWEEP_PATH.read_text()

        self.assertEqual([], library.validate_source_hash_policy_sweep_text(sweep_text))
        bad_unclassified = sweep_text + "\n| docs/example.md:1 | source-hash-claim | reject_unclassified | |\n"
        bad_digest = sweep_text + f"\nraw digest {digest_value()}\n"

        self.assertIn("unclassified", "\n".join(library.validate_source_hash_policy_sweep_text(bad_unclassified)))
        self.assertIn("raw digest", "\n".join(library.validate_source_hash_policy_sweep_text(bad_digest)))

    def test_source_hash_policy_sweep_requires_live_hit_coverage(self):
        library = load_library()
        live_hits = library.iter_source_hash_policy_hits()
        self.assertGreater(len(live_hits), 1)
        stale_text = "\n".join(
            [
                "# ACE Source-Hash Policy Sweep",
                "",
                "| Hit key | Surface class | Classification | Disposition |",
                "|---|---|---|---|",
                f"| {live_hits[0].key} | methodology-doc | modify_public_safe_hash_claim | Public references use opaque tokens only. |",
            ]
        )

        self.assertIn("missing live hit classification", "\n".join(library.validate_source_hash_policy_sweep_text(stale_text)))

    def test_canary_blocks_public_leak_patterns_and_redacts_diagnostics(self):
        library = load_library()
        media_key = "gps" + "_" + "latitude"
        title_key = "title" + "_" + "block"
        bom_key = "bom" + "_" + "table"
        copied_snippet_key = "copied" + "_" + "private" + "_" + "snippet"
        unsafe_text = "\n".join(
            [
                f"path: {private_root()}",
                f"contact: {email_value()}",
                f"{media_key}: 29.0",
                f"{title_key}: fixture",
                f"{bom_key}: fixture",
                f"{copied_snippet_key}: true",
                f"{source_term('source', 'hash')}: {digest_value()}",
                f"{source_term('public', 'source', 'token')}: {token_value()}",
            ]
        )

        errors = library.validate_public_output_text("runtime-negative.md", unsafe_text)
        rendered = "\n".join(errors)

        self.assertIn("raw-host-path", rendered)
        self.assertIn("personal-identifier", rendered)
        self.assertIn("media-metadata", rendered)
        self.assertIn("engineering-metadata", rendered)
        self.assertIn("copied-private-snippet", rendered)
        self.assertNotIn(private_root(), rendered)
        self.assertNotIn(email_value(), rendered)
        self.assertNotIn(digest_value(), rendered)
        self.assertNotIn(token_value(), rendered)

    def test_canary_allows_git_governance_sha_only_in_named_context(self):
        library = load_library()
        good = f"reviewed_commit_sha: {digest_value()[:40]}"
        bad = f"{source_term('source', 'hash')}: {digest_value()}"

        self.assertEqual([], library.validate_public_output_text("governance.md", good))
        self.assertIn("source-like", "\n".join(library.validate_public_output_text("bad-source.md", bad)))

    def test_validator_accepts_committed_safe_surfaces(self):
        validator = load_validator()

        errors = validator.collect_errors(
            scan_public_paths=[
                CONTRACT_DOC_PATH,
                SWEEP_PATH,
                OUTPUT_CONTRACT_PATH,
                DENY_LIST_PATH,
                LIBRARY_PATH,
                VALIDATOR_PATH,
                Path(__file__),
                SKILL_EVAL_PATH,
            ]
        )

        self.assertEqual([], errors)

    def test_validator_scans_issue_comment_body_files(self):
        validator = load_validator()

        with tempfile.TemporaryDirectory() as tmp:
            safe_comment = Path(tmp) / "safe-comment.md"
            unsafe_comment = Path(tmp) / "unsafe-comment.md"
            unsafe_secret_comment = Path(tmp) / "unsafe-secret-comment.md"
            secret_field = "api" + "_" + "key"
            safe_comment.write_text("Synthetic closeout with public methodology only.\n")
            unsafe_comment.write_text(f"Unsafe pointer {private_root()}\n")
            unsafe_secret_comment.write_text(f"{secret_field}: abcdefghijk\n")

            self.assertEqual([], validator.collect_errors(issue_comment_body_files=[safe_comment]))
            self.assertIn("raw-host-path", "\n".join(validator.collect_errors(issue_comment_body_files=[unsafe_comment])))
            self.assertIn("secret-assignment", "\n".join(validator.collect_errors(issue_comment_body_files=[unsafe_secret_comment])))

    def test_validator_redacts_issue_comment_body_read_failures(self):
        validator = load_validator()
        sensitive_segment = "client-secret" + "@" + "example.com"
        private_path = Path("/") / "home" / "vamsee" / "private" / sensitive_segment / "comment.md"

        rendered = "\n".join(validator.collect_errors(issue_comment_body_files=[private_path]))

        self.assertIn("path=REDACTED", rendered)
        self.assertNotIn(private_path.as_posix(), rendered)
        self.assertNotIn(sensitive_segment, rendered)

    def test_validator_reuses_legal_scan_for_secret_assignments(self):
        validator = load_validator()

        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests" / "fixtures") as tmp:
            unsafe_file = Path(tmp) / "unsafe-secret.md"
            secret_field = "api" + "_" + "key"
            unsafe_file.write_text(f"{secret_field}: abcdefghijk\n")

            errors = validator.collect_errors(scan_public_paths=[unsafe_file])

        self.assertIn("secret-assignment", "\n".join(errors))

    def test_publication_specific_canary_scans_json_and_python(self):
        validator = load_validator()
        media_key = "gps" + "_" + "latitude"
        engineering_key = "title" + "_" + "block"

        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests" / "fixtures") as tmp:
            tmp_path = Path(tmp)
            unsafe_json = tmp_path / "unsafe-media.json"
            unsafe_python = tmp_path / "unsafe-engineering.py"
            unsafe_json.write_text(json.dumps({media_key: 29}))
            unsafe_python.write_text(f"{engineering_key} = 'fixture'\n")

            errors = validator.collect_errors(scan_public_paths=[unsafe_json, unsafe_python])

        rendered = "\n".join(errors)
        self.assertIn("media-metadata", rendered)
        self.assertIn("engineering-metadata", rendered)

    def test_public_private_routing_eval_cases_are_issue_tagged(self):
        evals = load_json(SKILL_EVAL_PATH)["evals"]
        issue_cases = [case for case in evals if case.get("issue") == 63]

        self.assertTrue(issue_cases)
        self.assertTrue(all(str(case.get("id", "")).startswith("ace-63-") for case in issue_cases))


if __name__ == "__main__":
    unittest.main()
