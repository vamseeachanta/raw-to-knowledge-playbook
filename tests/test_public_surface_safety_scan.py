from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCAN_SCRIPT = REPO_ROOT / "scripts" / "security" / "public_surface_safety_scan.py"
WRAPPER = REPO_ROOT / "scripts" / "legal" / "legal-sanity-scan.sh"
CONFIG = REPO_ROOT / ".public-surface-safety.json"
TEST_GIT_EMAIL = "test" + "@" + "example" + "." + "invalid"


def synthetic_email() -> str:
    return "person" + "@" + "example" + "." + "com"


def synthetic_host() -> str:
    return "internal" + "." + "example" + "." + "com"


def synthetic_private_path(tail: str = "/example/private") -> str:
    return "/" + "home" + tail


def synthetic_confidentiality_marker() -> str:
    return "PROPRIETARY" + " " + "CONFIDENTIAL"


def synthetic_identifier_assignment() -> str:
    return "client_" + "id = SYNTHETIC-12345"


def synthetic_secret_assignment() -> str:
    return "pass" + "word = synthetic-secret-value"


def synthetic_raw_source_assignment() -> str:
    return "source_" + "id: SYNTHETIC-12345"


def synthetic_ssn() -> str:
    return "-".join(["123", "45", "6789"])


def synthetic_phone() -> str:
    return "-".join(["555", "123", "4567"])


def synthetic_private_fixture_id() -> str:
    return "CLIENT-PRIVATE-123456"


def run_cmd(args: list[str], cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        check=False,
    )


def git(cwd: Path, *args: str) -> None:
    result = run_cmd(["git", *args], cwd=cwd)
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)


def write_config(path: Path, *, extra: dict | None = None) -> None:
    record = json.loads(CONFIG.read_text()) if CONFIG.exists() else {
        "format": "json-subset-yaml",
        "owner_issue": 69,
        "private_runtime_config_owner_issue": 63,
        "rules": [],
        "allow_contexts": [],
    }
    if extra:
        record.update(extra)
    path.write_text(json.dumps(record, indent=2) + "\n")


class LegalSanityScanTests(unittest.TestCase):
    def test_config_loads_as_strict_json_subset_yaml(self):
        record = json.loads(CONFIG.read_text())

        self.assertEqual("json-subset-yaml", record["format"])
        self.assertEqual(69, record["owner_issue"])
        self.assertTrue(record["rules"])

    def test_old_wrapper_is_retired(self):
        self.assertFalse(WRAPPER.exists())
        self.assertTrue(SCAN_SCRIPT.exists())

    def test_config_rejects_yaml_only_constructs(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "bad.yaml"
            config.write_text("format: json-subset-yaml\nowner_issue: 69\n")

            result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--config", str(config), "--scan-public-path", str(CONFIG)])

        self.assertEqual(2, result.returncode)
        self.assertIn("strict JSON", result.stderr)

    def test_config_rejects_unknown_keys_and_inventory_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "bad.json"
            bad_rule = Path(tmp) / "bad-rule.json"
            write_config(
                config,
                extra={
                    "client_names": ["synthetic-client"],
                    "rules": [
                        {
                            "id": "bad",
                            "severity": "block",
                            "description": "bad",
                            "patterns": ["synthetic"],
                            "literal_values": ["synthetic"],
                        }
                    ],
                },
            )
            rule_record = json.loads(CONFIG.read_text())
            rule_record["rules"] = [
                {
                    "id": "bad",
                    "severity": "block",
                    "description": "bad",
                    "patterns": ["synthetic"],
                    "unknown_rule_key": "bad",
                }
            ]
            bad_rule.write_text(json.dumps(rule_record, indent=2) + "\n")

            result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--config", str(config), "--scan-public-path", str(CONFIG)])
            rule_result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--config", str(bad_rule), "--scan-public-path", str(CONFIG)])

        self.assertEqual(2, result.returncode)
        self.assertIn("forbidden inventory", result.stderr)
        self.assertEqual(2, rule_result.returncode)
        self.assertIn("unknown key", rule_result.stderr)

    def test_pattern_fields_allow_policy_regexes_but_reject_literal_private_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "good.json"
            bad = Path(tmp) / "bad.json"
            bad_escaped = Path(tmp) / "bad-escaped.json"
            bad_grouped = Path(tmp) / "bad-grouped.json"
            bad_private = Path(tmp) / "bad-private.json"
            bad_host = Path(tmp) / "bad-host.json"
            bad_host_class = Path(tmp) / "bad-host-class.json"
            bad_ssn = Path(tmp) / "bad-ssn.json"
            bad_phone = Path(tmp) / "bad-phone.json"
            write_config(
                good,
                extra={
                    "allow_contexts": [],
                    "rules": [
                        {
                            "id": "structural-email",
                            "severity": "block",
                            "description": "synthetic email-shaped value",
                            "patterns": [r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"],
                        }
                    ]
                },
            )
            for target, pattern in [
                (bad, synthetic_email()),
                (bad_escaped, synthetic_email().replace(".", r"\.")),
                (bad_grouped, "(?:" + synthetic_email() + ")"),
                (bad_private, synthetic_private_path() + "/.+"),
                (bad_host, synthetic_host()),
                (bad_host_class, synthetic_host().replace(".", "[.]")),
                (bad_ssn, synthetic_ssn()),
                (bad_phone, synthetic_phone()),
            ]:
                write_config(
                    target,
                    extra={
                        "allow_contexts": [],
                        "rules": [
                            {
                                "id": "literal-email",
                                "severity": "block",
                                "description": "bad literal",
                                "patterns": [pattern],
                            }
                        ]
                    },
                )

            good_result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--config", str(good), "--scan-public-path", str(CONFIG)])
            bad_results = [
                run_cmd([sys.executable, str(SCAN_SCRIPT), "--config", str(path), "--scan-public-path", str(CONFIG)])
                for path in [bad, bad_escaped, bad_grouped, bad_private, bad_host, bad_host_class, bad_ssn, bad_phone]
            ]

        self.assertNotEqual(2, good_result.returncode)
        for result in bad_results:
            self.assertEqual(2, result.returncode)
            self.assertIn("literal sensitive-looking value", result.stderr)

    def test_obsolete_allow_context_cannot_exempt_secrets(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.json"
            record = json.loads(CONFIG.read_text())
            record["allow_contexts"] = [{
                "context_id": "test-fixture-forensic-examples",
                "path_globs": ["tests/fixtures/.tmp-legal-allow-*.md"],
                "rule_ids": ["secret-assignment"],
                "sentinel": "legal-scan-allow: bounded-test",
                "max_lines_per_file": 1,
                "justification": "attempted credential exemption",
            }]
            config.write_text(json.dumps(record))
            result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--config",
                              str(config), "--scan-public-path", str(CONFIG)])
        self.assertEqual(2, result.returncode)
        self.assertIn("unknown allow context id", result.stderr)

    def test_xlsx_source_id_allow_context_is_content_restricted(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            git(repo, "init")
            git(repo, "config", "user.email", TEST_GIT_EMAIL)
            git(repo, "config", "user.name", "Test")
            (repo / ".public-surface-safety.json").write_text(CONFIG.read_text())
            manifest = repo / "skills" / "xlsx-input-code-output-canary" / "resources" / "canary_manifest.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({"source_" + "id": synthetic_private_fixture_id(), "_legal_scan_context": "legal-scan-allow: public-xlsx-canary-source-id"}) + "\n")
            git(repo, "add", ".public-surface-safety.json", "skills")

            result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--all-tracked-public-surfaces"], cwd=repo)

        self.assertEqual(1, result.returncode)
        self.assertIn("raw-source-provenance-assignment", result.stderr)
        self.assertNotIn(synthetic_private_fixture_id(), result.stderr)

    def test_blocks_synthetic_sensitive_rule_shapes_without_echoing_matches(self):
        fixture_dir = REPO_ROOT / "tests" / "fixtures"
        cases = [
            ("confidentiality-marker", synthetic_confidentiality_marker() + "\n", synthetic_confidentiality_marker()),
            ("secret-assignment", synthetic_secret_assignment() + "\n", "synthetic-secret-value"),
            ("raw-source-provenance-assignment", synthetic_raw_source_assignment() + "\n", "SYNTHETIC-12345"),
        ]
        for rule_id, content, forbidden_echo in cases:
            with self.subTest(rule_id=rule_id):
                with tempfile.NamedTemporaryFile("w", dir=fixture_dir, prefix=".tmp-legal-rule-", suffix=".md", delete=False) as handle:
                    path = Path(handle.name)
                    handle.write(content)
                try:
                    result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--scan-public-path", str(path)])
                finally:
                    if path.exists():
                        path.unlink()

                self.assertEqual(1, result.returncode)
                self.assertIn(rule_id, result.stderr)
                self.assertNotIn(forbidden_echo, result.stderr)

    def test_blocks_synthetic_sensitive_shapes_without_echoing_match(self):
        fixture_dir = REPO_ROOT / "tests" / "fixtures"
        with tempfile.NamedTemporaryFile("w", dir=fixture_dir, prefix=".tmp-legal-sensitive-", suffix=".md", delete=False) as handle:
            path = Path(handle.name)
            secret = "sk_" + ("a" * 24)
            handle.write(f"{'api_' + 'key'} = {secret}\n")
        self.addCleanup(lambda: path.exists() and path.unlink())
        try:
            result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--scan-public-path", str(path)])
        finally:
            if path.exists():
                path.unlink()

        self.assertEqual(1, result.returncode)
        self.assertIn("secret-assignment", result.stderr)
        self.assertNotIn(secret, result.stderr)

    def test_scan_public_path_rejects_path_escape(self):
        outside = "/" + "tmp" + "/outside.md"
        result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--scan-public-path", outside])
        traversal_result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--scan-public-path", "docs/../docs/plans/README.md"])
        host_result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--scan-public-path", "docs/" + synthetic_host() + ".md"])
        phone_result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--scan-public-path", "docs/" + synthetic_phone() + ".md"])
        ssn_result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--scan-public-path", "docs/" + synthetic_ssn() + ".md"])

        self.assertEqual(2, result.returncode)
        self.assertIn("path outside repository", result.stderr)
        self.assertNotIn(outside, result.stderr)
        self.assertEqual(2, traversal_result.returncode)
        self.assertIn("path traversal", traversal_result.stderr)
        for sensitive, redacted_result in [
            (synthetic_host(), host_result),
            (synthetic_phone(), phone_result),
            (synthetic_ssn(), ssn_result),
        ]:
            self.assertEqual(2, redacted_result.returncode)
            self.assertIn("scan path missing", redacted_result.stderr)
            self.assertNotIn(sensitive, redacted_result.stderr)

    def test_diff_only_scans_staged_blob_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            git(repo, "init")
            git(repo, "config", "user.email", TEST_GIT_EMAIL)
            git(repo, "config", "user.name", "Test")
            (repo / ".public-surface-safety.json").write_text(CONFIG.read_text())
            (repo / "docs").mkdir()
            path = repo / "docs" / "candidate.md"
            path.write_text("clean\n")
            git(repo, "add", ".")
            git(repo, "commit", "-m", "init")
            path.write_text(synthetic_secret_assignment() + "\n")
            git(repo, "add", "docs/candidate.md")
            path.write_text("clean again\n")

            result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--diff-only"], cwd=repo)

        self.assertEqual(1, result.returncode)
        self.assertIn("staged", result.stderr)
        self.assertIn("secret-assignment", result.stderr)

    def test_diff_only_scans_unstaged_tracked_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            git(repo, "init")
            git(repo, "config", "user.email", TEST_GIT_EMAIL)
            git(repo, "config", "user.name", "Test")
            (repo / ".public-surface-safety.json").write_text(CONFIG.read_text())
            (repo / "docs").mkdir()
            path = repo / "docs" / "candidate.md"
            path.write_text("clean\n")
            git(repo, "add", ".")
            git(repo, "commit", "-m", "init")
            path.write_text(synthetic_secret_assignment() + "\n")

            result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--diff-only"], cwd=repo)

        self.assertEqual(1, result.returncode)
        self.assertIn("unstaged", result.stderr)

    def test_diff_only_fails_closed_on_untracked_public_surface_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            git(repo, "init")
            git(repo, "config", "user.email", TEST_GIT_EMAIL)
            git(repo, "config", "user.name", "Test")
            (repo / ".public-surface-safety.json").write_text(CONFIG.read_text())
            git(repo, "add", ".public-surface-safety.json")
            git(repo, "commit", "-m", "init")
            (repo / "docs").mkdir()
            (repo / "docs" / "new.md").write_text("clean\n")

            result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--diff-only"], cwd=repo)

        self.assertEqual(1, result.returncode)
        self.assertIn("untracked public-surface candidate", result.stderr)

    @unittest.skipIf(os.name == "nt", "Windows forbids newline filenames")
    def test_git_path_collection_uses_nul_delimiters(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            git(repo, "init")
            git(repo, "config", "user.email", TEST_GIT_EMAIL)
            git(repo, "config", "user.name", "Test")
            (repo / ".public-surface-safety.json").write_text(CONFIG.read_text())
            docs = repo / "docs"
            docs.mkdir()
            weird = docs / "line\nbreak.md"
            weird.write_text(synthetic_secret_assignment() + "\n")
            git(repo, "add", ".public-surface-safety.json", "docs")

            result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--diff-only"], cwd=repo)

        self.assertEqual(1, result.returncode)
        self.assertIn("candidate-", result.stderr)

    def test_all_tracked_public_surfaces_scans_clean_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            git(repo, "init")
            git(repo, "config", "user.email", TEST_GIT_EMAIL)
            git(repo, "config", "user.name", "Test")
            (repo / ".public-surface-safety.json").write_text(CONFIG.read_text())
            (repo / "docs").mkdir()
            (repo / "docs" / "candidate.md").write_text(synthetic_confidentiality_marker() + "\n")
            git(repo, "add", ".")
            git(repo, "commit", "-m", "init")

            result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--all-tracked-public-surfaces"], cwd=repo)

        self.assertEqual(1, result.returncode)
        self.assertIn("confidentiality-marker", result.stderr)

    def test_candidate_path_matrix_rejects_unclassified_public_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            git(repo, "init")
            git(repo, "config", "user.email", TEST_GIT_EMAIL)
            git(repo, "config", "user.name", "Test")
            (repo / ".public-surface-safety.json").write_text(CONFIG.read_text())
            (repo / "misc").mkdir()
            (repo / "misc" / "scratch-public.md").write_text("clean\n")
            git(repo, "add", ".")
            git(repo, "commit", "-m", "init")

            result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--all-tracked-public-surfaces"], cwd=repo)

        self.assertEqual(2, result.returncode)
        self.assertIn("unclassified public-surface candidate", result.stderr)

    def test_all_tracked_text_paths_are_classified_or_excluded_with_reason(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("legal_sanity_scan_under_test", SCAN_SCRIPT)
        self.assertIsNotNone(spec)
        scanner = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        sys.modules["legal_sanity_scan_under_test"] = scanner
        spec.loader.exec_module(scanner)
        result = run_cmd(["git", "ls-files", "-z"])
        self.assertEqual("", result.stderr)
        self.assertEqual(0, result.returncode)
        unclassified = [
            item
            for item in result.stdout.split("\0")
            if item and scanner.classify_path(Path(item)) == "unclassified"
        ]

        self.assertEqual([], unclassified)

    def test_issue_69_scanner_artifacts_self_scan(self):
        args = [sys.executable, str(SCAN_SCRIPT)]
        for path in [
            CONFIG,
            SCAN_SCRIPT,
            REPO_ROOT / "tests" / "test_public_surface_safety_scan.py",
            REPO_ROOT / ".github" / "workflows" / "validate.yml",
        ]:
            args.extend(["--scan-public-path", str(path)])

        result = run_cmd(args)

        self.assertEqual("", result.stderr)
        self.assertEqual(0, result.returncode)

    def test_parent_public_scan_accepts_issue_69_policy_surfaces(self):
        args = [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate_ace_epic_wave_coordination.py"),
        ]
        for path in [
            CONFIG,
            SCAN_SCRIPT,
            REPO_ROOT / "tests" / "test_public_surface_safety_scan.py",
            REPO_ROOT / ".github" / "workflows" / "validate.yml",
            REPO_ROOT / "skills" / "xlsx-input-code-output-canary" / "resources" / "canary_manifest.json",
            REPO_ROOT / "skills" / "xlsx-input-code-output-canary" / "resources" / "xlsx_canary.py",
        ]:
            args.extend(["--scan-public-path", str(path)])

        result = run_cmd(args)

        self.assertEqual("", result.stderr)
        self.assertEqual(0, result.returncode)

    def test_issue_62_public_scan_paths_are_legal_scan_inputs(self):
        from scripts.ace_manifest_freshness_contract import public_scan_paths

        scan_paths = public_scan_paths()
        self.assertIn(Path("docs/plans/2026-06-29-issue-62-ace-manifest-freshness-and-drift-sentinel.md"), scan_paths)
        missing = [path.as_posix() for path in scan_paths if not (REPO_ROOT / path).exists()]
        self.assertEqual([], missing)
        args = [sys.executable, str(SCAN_SCRIPT)]
        for path in scan_paths:
            args.extend(["--scan-public-path", str(REPO_ROOT / path)])

        result = run_cmd(args)

        self.assertEqual("", result.stderr)
        self.assertEqual(0, result.returncode)

    def test_real_repo_all_tracked_public_surfaces_passes(self):
        result = run_cmd([sys.executable, str(SCAN_SCRIPT), "--all-tracked-public-surfaces"])

        self.assertEqual("", result.stderr)
        self.assertEqual(0, result.returncode)

    def test_bound_skills_document_69_scan_gate(self):
        for skill_path in [
            "skills/public-private-routing/SKILL.md",
            "skills/content-triage-and-exclusion/SKILL.md",
            "skills/verify-batch/SKILL.md",
            "skills/independent-oracle-validation/SKILL.md",
            "skills/adversarial-verify-loop/SKILL.md",
        ]:
            with self.subTest(skill_path=skill_path):
                text = (REPO_ROOT / skill_path).read_text()
                self.assertIn("scripts/security/public_surface_safety_scan.py", text)
                self.assertIn("--all-tracked-public-surfaces", text)

    def test_wave0_schema_records_69_issue_skill_group(self):
        schema = json.loads((REPO_ROOT / "artifacts" / "ace-wave0-ledger-schema.json").read_text())
        rows = {row["issue"]: row for row in schema["wave0_split_registry"]}

        self.assertEqual(
            [
                "public-private-routing",
                "content-triage-and-exclusion",
                "verify-batch",
                "independent-oracle-validation",
                "adversarial-verify-loop",
            ],
            rows[69]["issue_skill_groups"],
        )

    def test_legal_scan_is_in_ci(self):
        workflow = (REPO_ROOT / ".github" / "workflows" / "validate.yml").read_text()

        self.assertIn("scripts/security/public_surface_safety_scan.py --all-tracked-public-surfaces", workflow)


if __name__ == "__main__":
    unittest.main()
