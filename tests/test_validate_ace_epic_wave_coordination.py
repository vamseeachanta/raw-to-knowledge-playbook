from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_epic_wave_coordination.py"
PRIVATE_SOURCE_PATH = "/mnt" + "/ace/private/source.docx"
PRIVATE_EMAIL = "person" + "@example.com"
CLIENT_ID_SNIPPET = "client_" + "id=ACME-123"
CONFIDENTIAL_SNIPPET = "PROPRIETARY " + "CONFIDENTIAL payload"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_ace_epic_wave_coordination", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


METHOD_ISSUES = {
    51: "#1, #12",
    52: "#1, #12",
    53: "#5, #6, #12, #33",
    54: "#2, #3, #7, #12, #33",
    55: "#8, #12, #33",
    56: "#3, #4, #12",
    57: "#1, #12",
    58: "#9, #10, #12",
    59: "#6, #12",
    60: "#12",
    61: "#12, #1",
    62: "#12",
    63: "#12",
}

EXECUTABLE_BINDINGS = {
    51: "content-triage-and-exclusion; scripts/validate_ace_wave0_control_plane.py",
    52: "content-triage-and-exclusion; scripts/validate_ace_wave1_text_json.py",
    53: "format-coverage-ledger; scripts/validate_ace_wave2_spreadsheet_csv.py",
    54: "source-extraction-coverage; scripts/validate_ace_wave3_document_lane.py",
    55: "format-coverage-ledger; scripts/validate_ace_wave4_decks_email.py",
    56: "content-triage-and-exclusion; scripts/validate_ace_wave5_images.py",
    57: "docs/21-cad-and-brep-geometry.md; scripts/validate_ace_wave6_cad.py",
    58: "simulation-engineering-file-lane; examples/simulation-engineering-lane/check.py",
    59: "database-geospatial-structured-index-lane; examples/database-geospatial-index-lane/check.py",
    60: "archive-extraction-integrity; scripts/validate_ace_wave9_media_archive_noise.py",
    61: "page-shape-contract; scripts/validate_ace_knowledge_store_contract.py; scripts/validate_ace_ingested_success_metric.py",
    62: "source-extraction-coverage; scripts/validate_ace_manifest_freshness.py",
    63: "public-private-routing; scripts/validate_ace_public_artifacts.py; tests/fixtures/ace-public-artifact-safety/",
}

DIFFICULTY_RANK = {
    51: "1/11",
    52: "2/11",
    53: "3/11",
    54: "4/11",
    55: "5/11",
    56: "6/11",
    57: "7/11",
    58: "8/11",
    59: "9/11",
    60: "10/11",
    61: "11/11",
    62: "2/11",
    63: "11/11",
}

CONTROL_GATE_ISSUES = {51, 61, 62, 63}
WAVE_CLASSES = {
    51: "control_plane",
    **{issue: "ingestion_wave" for issue in range(52, 61)},
    61: "storage_lifecycle_gate",
    62: "manifest_freshness_gate",
    63: "public_canary_gate",
}


def metric_cell(issue: int) -> str:
    if issue in CONTROL_GATE_ISSUES:
        return (
            "0% direct source ingestion; "
            "success_metric_applicability=not_applicable_control_plane; "
            "expected_yield=0; measured_success_numerator=0; "
            "measured_success_denominator=0; success_threshold=0; "
            f"validation_command={EXECUTABLE_BINDINGS[issue]}; "
            f"difficulty {DIFFICULTY_RANK[issue]}"
        )
    return (
        "70-95%; success = successful_routed_items / eligible_candidate_items * 100; "
        f"difficulty {DIFFICULTY_RANK[issue]}"
    )


def valid_marker(issue: int) -> str:
    return "\n".join(
        [
            "Approved by: vamseeachanta",
            "Approval date: 2026-06-29",
            f"Issue: https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/{issue}",
            f"Plan path: docs/plans/issue-{issue}.md",
            "Reviewed commit: ba1041f117f00a6c36fd35298b84856d1dd92f56",
            "Review artifacts:",
            "  - scripts/review/results/2026-06-29-plan-50-claude-r4.md",
        ]
    )


def row(issue: int) -> str:
    manifest_gate = (
        "not applicable for own sampling; #62 gate applies to downstream sampling"
        if issue in {51, 61, 62, 63}
        else "yes; #62 status:plan-approved+approval marker+implemented validator+recorded passing-command+snapshot_id before sampling"
    )
    dependencies = "#51; #61 status:plan-approved + approval marker + implemented validator + recorded passing-command durable-output gate"
    if issue == 62:
        dependencies = "#65 schema is the canonical registry source; #70 consumes the #62 evidence contract for #67 integration; #51 remains umbrella context only"
    return (
        f"| #{issue} | docs/plans/issue-{issue}.md | lane:claude | T2 | draft | "
        f"2026-06-29 no status label; no approval marker | false | {METHOD_ISSUES[issue]} | "
        f"{EXECUTABLE_BINDINGS[issue]} | Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41 | "
        f"{dependencies} | {metric_cell(issue)} | {manifest_gate} | "
        "yes; #63 status:plan-approved+approval marker+implemented canary+recorded passing-command before publication | "
        "closed-set: doc-update, skill-eval-update, follow-on-issue | false |"
    )


def structural_row(issue: int) -> str:
    requires_snapshot = "true" if 52 <= issue <= 60 else "false"
    if issue in CONTROL_GATE_ISSUES:
        denominator = "measured_success_denominator"
    else:
        denominator = "eligible_candidate_items"
    numerator = "measured_success_numerator" if issue in CONTROL_GATE_ISSUES else "successful_routed_items"
    return f"| #{issue} | {WAVE_CLASSES[issue]} | {requires_snapshot} | {numerator} | {denominator} |"


GOOD_DOC = "\n".join(
    [
        "# ACE Share Ingestion Wave Coordination",
        "",
        "## Source Inventory and Bounded Read Contract",
        "- Root abstraction: `ACE_SHARE_ROOT`.",
        "- Named manifest sources: `INDEX.md`, `assets.json`, `docs/master-index.jsonl`, `_cad-index/index-summary.json`, `_cad-index/cad-readability-index.tsv`, and `.ace-knowledge/index.db`.",
        "- Seed/sort rule: stable sort by `source_id`, then seeded sample `ace-epic-50-2026-06-29`.",
        "- Row caps: 200 rows per bucket; maximum files touched: 25; maximum bytes touched: 1048576.",
        "- Denied traversal patterns: recursive share walk; full-manifest materialization; full-file hashing/counting of large manifests; unrestricted `jq`; `os.walk`; `ls -R`; `find`; `du`; `rg`; `fd`.",
        "- Allowed proof command examples must be bounded and use share-relative paths only.",
        "",
        "## Epic Gates",
        "- Branch publication rule: dedicated planning branch or explicit stacked-branch note is required.",
        "- Public artifact safety gate: path-tokenization, opaque `public_source_token` use, raw source id/hash denial, generic private-like identifier check, personal identifier check, and proprietary snippet check before docs nav, mkdocs, llm-wiki, GitHub comments, or external publication; maintained deny-list certification is the #63 gate.",
        "- `% ingested success` = `successful_routed_items / eligible_candidate_items * 100`; hard exclusions are reported as `% excluded`.",
        "- Method gap disposition closed set: `doc-update`, `skill-eval-update`, `follow-on-issue`.",
        "- Wave #0 / #51 lifecycle contract: downstream waves depend on #51; durable outputs depend on #61 status:plan-approved plus approval marker plus implemented validators and recorded passing-command evidence.",
        "",
        "## Structural Wave Gate Registry",
        "| Issue | wave_class | requires_manifest_snapshot_id | success_numerator_field | success_denominator_field |",
        "|---|---|---|---|---|",
        *[structural_row(issue) for issue in range(51, 64)],
        "",
        "## Child Wave Ledger",
        "| Issue | Plan | Lane | Complexity | Plan status | Status snapshot | Implementation ready | Method issues | Skill groups and executable tests | Review artifacts | Dependencies | Expected useful ingestion / success metric / difficulty | Manifest gate | Public canary gate | Method gap disposition | Publication exposure |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
        *[row(issue) for issue in range(51, 64)],
    ]
)


class AceEpicWaveCoordinationValidationTests(unittest.TestCase):
    def assert_rejects(self, text: str, expected: str):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            result = validator.validate_text(text, approval_root=Path(tmp))

        self.assertTrue(result.errors, "expected validation errors")
        self.assertIn(expected, "\n".join(result.errors))

    def test_epic_coordination_lists_all_children(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            result = validator.validate_text(GOOD_DOC, approval_root=Path(tmp))

        self.assertEqual([], result.errors)

    def test_each_child_has_method_issue_binding(self):
        bad_doc = GOOD_DOC.replace("| #52 | docs/plans/issue-52.md | lane:claude | T2 | draft | 2026-06-29 no status label; no approval marker | false | #1, #12 |", "| #52 | docs/plans/issue-52.md | lane:claude | T2 | draft | 2026-06-29 no status label; no approval marker | false | none |")
        self.assert_rejects(bad_doc, "#52 method issues")

    def test_each_child_has_expected_method_issue_binding(self):
        bad_doc = GOOD_DOC.replace("| #52 | docs/plans/issue-52.md | lane:claude | T2 | draft | 2026-06-29 no status label; no approval marker | false | #1, #12 |", "| #52 | docs/plans/issue-52.md | lane:claude | T2 | draft | 2026-06-29 no status label; no approval marker | false | #999 |")
        self.assert_rejects(bad_doc, "#52 method issues")

    def test_each_child_has_skill_group_and_executable_test_binding(self):
        bad_doc = GOOD_DOC.replace("content-triage-and-exclusion; scripts/validate_ace_wave0_control_plane.py", "content-triage-and-exclusion", 1)
        self.assert_rejects(bad_doc, "#51 skill groups")

    def test_each_child_rejects_placeholder_executable_binding(self):
        bad_doc = GOOD_DOC.replace("content-triage-and-exclusion; scripts/validate_ace_wave1_text_json.py", "content-triage-and-exclusion; validator TBD", 1)
        self.assert_rejects(bad_doc, "#52 skill groups")

    def test_review_artifact_status_recorded_per_child(self):
        bad_doc = GOOD_DOC.replace("Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41", "pending; pending; pending", 1)
        self.assert_rejects(bad_doc, "#51 review artifacts")

    def test_review_artifact_status_requires_provider_specific_segments(self):
        bad_doc = GOOD_DOC.replace("Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41", "Claude: Codex: Gemini: pending", 1)
        self.assert_rejects(bad_doc, "#51 review artifacts")

    def test_review_artifact_status_rejects_unbacked_verdict_words(self):
        bad_doc = GOOD_DOC.replace(
            "Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41",
            "Claude: approve; Codex: minor; Gemini: major",
            1,
        )
        self.assert_rejects(bad_doc, "#51 review artifacts")

    def test_review_artifact_status_rejects_path_traversal(self):
        bad_doc = GOOD_DOC.replace(
            "Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41",
            "Claude: scripts/review/results/../../../docs/plans/ace-share-ingestion-wave-coordination.md; Codex: pending; Gemini: not-run",
            1,
        )
        self.assert_rejects(bad_doc, "#51 review artifacts")

    def test_review_artifact_status_rejects_empty_artifact_file(self):
        artifact = REPO_ROOT / "scripts" / "review" / "results" / "test-empty-review-artifact.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())

        bad_doc = GOOD_DOC.replace(
            "Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41",
            "Claude: scripts/review/results/test-empty-review-artifact.md; Codex: pending; Gemini: not-run",
            1,
        )
        self.assert_rejects(bad_doc, "#51 review artifacts")

    def test_review_artifact_status_requires_verdict_section(self):
        artifact = REPO_ROOT / "scripts" / "review" / "results" / "test-review-artifact-no-verdict.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("# Review\n\nNo verdict section.\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())

        bad_doc = GOOD_DOC.replace(
            "Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41",
            "Claude: scripts/review/results/test-review-artifact-no-verdict.md; Codex: pending; Gemini: not-run",
            1,
        )
        self.assert_rejects(bad_doc, "#51 review artifacts")

    def test_review_artifact_status_rejects_verdict_heading_without_value(self):
        artifact = REPO_ROOT / "scripts" / "review" / "results" / "test-review-artifact-empty-verdict.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("## Verdict\n\nProvider failed before producing a verdict.\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())

        bad_doc = GOOD_DOC.replace(
            "Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41",
            "Claude: scripts/review/results/test-review-artifact-empty-verdict.md; Codex: pending; Gemini: not-run",
            1,
        )
        self.assert_rejects(bad_doc, "#51 review artifacts")

    def test_review_artifact_status_rejects_unavailable_artifact_path(self):
        artifact = REPO_ROOT / "scripts" / "review" / "results" / "test-review-artifact-unavailable.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("## Verdict\nUNAVAILABLE (provider auth failed)\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())

        bad_doc = GOOD_DOC.replace(
            "Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41",
            "Claude: pending; Codex: scripts/review/results/test-review-artifact-unavailable.md; Gemini: unavailable: auth exit 41",
            1,
        )
        self.assert_rejects(bad_doc, "#51 review artifacts")

    def test_review_artifact_status_rejects_verdict_word_not_at_value_start(self):
        artifact = REPO_ROOT / "scripts" / "review" / "results" / "test-review-artifact-late-verdict-word.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("## Verdict\nThis is not a verdict, but APPROVE appears later.\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())

        bad_doc = GOOD_DOC.replace(
            "Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41",
            "Claude: scripts/review/results/test-review-artifact-late-verdict-word.md; Codex: pending; Gemini: not-run",
            1,
        )
        self.assert_rejects(bad_doc, "#51 review artifacts")

    def test_review_artifact_status_rejects_same_line_verdict_word_not_at_value_start(self):
        artifact = REPO_ROOT / "scripts" / "review" / "results" / "test-review-artifact-same-line-late-verdict-word.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("Verdict: unresolved, maybe MINOR after more review\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())

        bad_doc = GOOD_DOC.replace(
            "Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41",
            "Claude: scripts/review/results/test-review-artifact-same-line-late-verdict-word.md; Codex: pending; Gemini: not-run",
            1,
        )
        self.assert_rejects(bad_doc, "#51 review artifacts")

    def test_review_artifact_status_accepts_verdict_with_explanatory_prose(self):
        validator = load_validator()
        artifact = REPO_ROOT / "scripts" / "review" / "results" / "test-review-artifact-verdict-with-prose.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("## Verdict\n**MINOR** - no MAJOR findings remain.\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())

        doc = GOOD_DOC.replace(
            "Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41",
            "Claude: scripts/review/results/test-review-artifact-verdict-with-prose.md; Codex: pending; Gemini: unavailable: auth exit 41",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = validator.validate_text(doc, approval_root=Path(tmp))

        self.assertEqual([], result.errors)

    def test_review_artifact_status_accepts_uppercase_bold_verdict_heading(self):
        validator = load_validator()
        artifact = REPO_ROOT / "scripts" / "review" / "results" / "test-review-artifact-uppercase-bold-verdict.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("## VERDICT\n\n**MAJOR**\n\nFindings follow.\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())

        doc = GOOD_DOC.replace(
            "Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41",
            "Claude: scripts/review/results/test-review-artifact-uppercase-bold-verdict.md; Codex: pending; Gemini: unavailable: auth exit 41",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = validator.validate_text(doc, approval_root=Path(tmp))

        self.assertEqual([], result.errors)

    def test_review_artifact_status_accepts_legacy_verdict_heading(self):
        validator = load_validator()
        artifact = REPO_ROOT / "scripts" / "review" / "results" / "test-review-artifact-legacy-verdict.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("Provider\n\nCodex\n\nVerdict\n\nMINOR\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())

        doc = GOOD_DOC.replace(
            "Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41",
            "Claude: scripts/review/results/test-review-artifact-legacy-verdict.md; Codex: pending; Gemini: unavailable: auth exit 41",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = validator.validate_text(doc, approval_root=Path(tmp))

        self.assertEqual([], result.errors)

    def test_approval_marker_can_preserve_unavailable_provider_history(self):
        validator = load_validator()
        artifact = REPO_ROOT / "scripts" / "review" / "results" / "test-review-artifact-unavailable-history.md"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("- **Verdict:** UNAVAILABLE\n\nProvider authentication failed.\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())

        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "51.md"
            marker.write_text(
                "\n".join(
                    [
                        "Approved by: vamseeachanta",
                        "Approval date: 2026-06-29",
                        "Issue: https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51",
                        "Plan path: docs/plans/issue-51.md",
                        "Reviewed commit: ba1041f117f00a6c36fd35298b84856d1dd92f56",
                        "Review artifacts:",
                        f"  - {artifact.relative_to(REPO_ROOT)}",
                    ]
                )
            )

            result = validator.validate_approval_marker(
                marker,
                51,
                "docs/plans/issue-51.md",
            )

        self.assertEqual([], result)

    def test_status_gate_records_unapproved_children(self):
        bad_doc = GOOD_DOC.replace("2026-06-29 no status label; no approval marker | false | #1, #12", "2026-06-29 no status label; no approval marker | true | #1, #12", 1)
        self.assert_rejects(bad_doc, "#51 implementation ready")

    def test_approved_marker_requires_required_fields_when_ready(self):
        validator = load_validator()
        ready_doc = GOOD_DOC.replace(
            "2026-06-29 no status label; no approval marker | false | #1, #12",
            "2026-06-29 status:plan-approved | true | #1, #12",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            approval_root = Path(tmp)
            (approval_root / "51.md").write_text("Approved by: reviewer\n")
            result = validator.validate_text(ready_doc, approval_root=approval_root)

        self.assertIn("#51 approval marker", "\n".join(result.errors))

    def test_approved_marker_requires_matching_values_when_ready(self):
        validator = load_validator()
        ready_doc = GOOD_DOC.replace(
            "2026-06-29 no status label; no approval marker | false | #1, #12",
            "2026-06-29 status:plan-approved | true | #1, #12",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            approval_root = Path(tmp)
            (approval_root / "51.md").write_text(
                "\n".join(
                    [
                        "Approved by:",
                        "Approval date:",
                        "Issue: https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/999",
                        "Plan path: docs/plans/wrong.md",
                        "Reviewed commit: not-a-sha",
                        "Review artifacts:",
                        "  - missing.md",
                    ]
                )
            )
            result = validator.validate_text(ready_doc, approval_root=approval_root)

        self.assertIn("#51 approval marker", "\n".join(result.errors))

    def test_approved_marker_requires_review_artifact_paths(self):
        validator = load_validator()
        ready_doc = GOOD_DOC.replace(
            "2026-06-29 no status label; no approval marker | false | #1, #12",
            "2026-06-29 status:plan-approved | true | #1, #12",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            approval_root = Path(tmp)
            (approval_root / "51.md").write_text(
                "\n".join(
                    [
                        "Approved by: vamseeachanta",
                        "Approval date: 2026-06-29",
                        "Issue: https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51",
                        "Plan path: docs/plans/issue-51.md",
                        "Reviewed commit: ba1041f117f00a6c36fd35298b84856d1dd92f56",
                        "Review artifacts: present",
                        "  - README.md",
                    ]
                )
            )
            result = validator.validate_text(ready_doc, approval_root=approval_root)

        self.assertIn("#51 approval marker", "\n".join(result.errors))

    def test_approved_marker_rejects_review_artifact_path_traversal(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "51.md"
            marker.write_text(
                "\n".join(
                    [
                        "Approved by: vamseeachanta",
                        "Approval date: 2026-06-29",
                        "Issue: https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/51",
                        "Plan path: docs/plans/issue-51.md",
                        "Reviewed commit: ba1041f117f00a6c36fd35298b84856d1dd92f56",
                        "Review artifacts:",
                        "  - scripts/review/results/../../../docs/plans/ace-share-ingestion-wave-coordination.md",
                    ]
                )
            )

            result = validator.validate_approval_marker(
                marker,
                51,
                "docs/plans/issue-51.md",
            )

        self.assertIn("#51 approval marker review artifact", "\n".join(result))

    def test_approved_marker_accepts_documented_bullet_list_format(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "51.md"
            marker.write_text(valid_marker(51))

            result = validator.validate_approval_marker(
                marker,
                51,
                "docs/plans/issue-51.md",
            )

        self.assertEqual([], result)

    def test_plan_approved_status_requires_snapshot_and_marker(self):
        bad_doc = GOOD_DOC.replace(
            "| #52 | docs/plans/issue-52.md | lane:claude | T2 | draft | 2026-06-29 no status label; no approval marker | false | #1, #12 |",
            "| #52 | docs/plans/issue-52.md | lane:claude | T2 | plan-approved | 2026-06-29 no status label; no approval marker | false | #1, #12 |",
        )
        self.assert_rejects(bad_doc, "#52 plan-approved")

    def test_downstream_ready_requires_issue_61_ready(self):
        validator = load_validator()
        ready_doc = GOOD_DOC.replace(
            "| #52 | docs/plans/issue-52.md | lane:claude | T2 | draft | 2026-06-29 no status label; no approval marker | false | #1, #12 |",
            "| #52 | docs/plans/issue-52.md | lane:claude | T2 | draft | 2026-06-29 status:plan-approved | true | #1, #12 |",
        )
        with tempfile.TemporaryDirectory() as tmp:
            approval_root = Path(tmp)
            (approval_root / "52.md").write_text(valid_marker(52))
            result = validator.validate_text(ready_doc, approval_root=approval_root)

        self.assertIn("#52 #61 dependency", "\n".join(result.errors))

    def test_dependencies_include_wave0_and_lifecycle_contract(self):
        good_row = "| #52 | docs/plans/issue-52.md | lane:claude | T2 | draft | 2026-06-29 no status label; no approval marker | false | #1, #12 | content-triage-and-exclusion; scripts/validate_ace_wave1_text_json.py | Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41 | #51; #61 status:plan-approved + approval marker + implemented validator + recorded passing-command durable-output gate |"
        bad_row = "| #52 | docs/plans/issue-52.md | lane:claude | T2 | draft | 2026-06-29 no status label; no approval marker | false | #1, #12 | content-triage-and-exclusion; scripts/validate_ace_wave1_text_json.py | Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41 | #61 durable-output gate |"
        bad_doc = GOOD_DOC.replace(good_row, bad_row)
        self.assert_rejects(bad_doc, "#52 dependencies")

    def test_lifecycle_contract_requires_full_gate_details(self):
        good_row = "| #52 | docs/plans/issue-52.md | lane:claude | T2 | draft | 2026-06-29 no status label; no approval marker | false | #1, #12 | content-triage-and-exclusion; scripts/validate_ace_wave1_text_json.py | Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41 | #51; #61 status:plan-approved + approval marker + implemented validator + recorded passing-command durable-output gate |"
        bad_row = "| #52 | docs/plans/issue-52.md | lane:claude | T2 | draft | 2026-06-29 no status label; no approval marker | false | #1, #12 | content-triage-and-exclusion; scripts/validate_ace_wave1_text_json.py | Claude: pending; Codex: pending; Gemini: unavailable: auth exit 41 | #51; #61 durable-output gate |"
        bad_doc = GOOD_DOC.replace(good_row, bad_row)
        self.assert_rejects(bad_doc, "#52 #61 gate")

    def test_method_gap_disposition_is_closed_set(self):
        bad_doc = GOOD_DOC.replace("closed-set: doc-update, skill-eval-update, follow-on-issue", "notes-only", 1)
        self.assert_rejects(bad_doc, "#51 method gap disposition")

    def test_method_gap_disposition_can_record_one_actual_resolution(self):
        validator = load_validator()
        good_doc = GOOD_DOC.replace("closed-set: doc-update, skill-eval-update, follow-on-issue", "follow-on-issue #99", 1)
        with tempfile.TemporaryDirectory() as tmp:
            result = validator.validate_text(good_doc, approval_root=Path(tmp))

        self.assertEqual([], result.errors)

    def test_method_gap_disposition_requires_durable_target(self):
        bad_doc = GOOD_DOC.replace("closed-set: doc-update, skill-eval-update, follow-on-issue", "follow-on-issue", 1)
        self.assert_rejects(bad_doc, "#51 method gap disposition")

    def test_public_artifact_safety_gate_required(self):
        bad_doc = GOOD_DOC.replace("path-tokenization, opaque `public_source_token` use, raw source id/hash denial, generic private-like identifier check, personal identifier check, and proprietary snippet check", "manual review")
        self.assert_rejects(bad_doc, "public artifact safety gate")

    def test_public_artifact_safety_gate_blocks_raw_private_leaks(self):
        leak_doc = GOOD_DOC + f"\n\n## Bad Public Example\n- `{PRIVATE_SOURCE_PATH}`\n- `{PRIVATE_EMAIL}`\n- `{CLIENT_ID_SNIPPET}`\n- `{CONFIDENTIAL_SNIPPET}`\n"
        self.assert_rejects(leak_doc, "public artifact leak")

    def test_public_artifact_safety_sentinel_does_not_allow_raw_private_leaks(self):
        leak_doc = GOOD_DOC + f"\n\n## Bad Public Example\n- validator-allow-forbidden-example `{PRIVATE_SOURCE_PATH}` `{PRIVATE_EMAIL}`\n"
        self.assert_rejects(leak_doc, "public artifact leak")

    def test_denied_traversal_policy_line_does_not_hide_private_leaks(self):
        leak_doc = GOOD_DOC.replace(
            "Denied traversal patterns:",
            f"Denied traversal patterns: `{PRIVATE_SOURCE_PATH}`;",
        )
        self.assert_rejects(leak_doc, "public artifact leak")

    def test_denied_traversal_policy_line_does_not_hide_command_examples(self):
        bad_doc = GOOD_DOC.replace(
            "Denied traversal patterns:",
            "Denied traversal patterns: `find ACE_SHARE_ROOT -type f`;",
        )
        self.assert_rejects(bad_doc, "unbounded traversal")

    def test_branch_publication_rule_present(self):
        bad_doc = GOOD_DOC.replace("Branch publication rule: dedicated planning branch or explicit stacked-branch note is required.", "Branch publication rule: TBD.")
        self.assert_rejects(bad_doc, "branch publication rule")

    def test_ingested_success_metric_is_defined(self):
        bad_doc = GOOD_DOC.replace("successful_routed_items / eligible_candidate_items * 100", "manual estimate")
        self.assert_rejects(bad_doc, "ingested success")

    def test_structural_wave_gate_registry_is_required(self):
        bad_doc = GOOD_DOC.replace("## Structural Wave Gate Registry", "## Wave Notes")
        self.assert_rejects(bad_doc, "Structural Wave Gate Registry")

    def test_structural_wave_gate_registry_requires_expected_wave_class(self):
        bad_doc = GOOD_DOC.replace(structural_row(52), structural_row(52).replace("ingestion_wave", "control_plane"))
        self.assert_rejects(bad_doc, "#52 wave_class")

    def test_structural_wave_gate_registry_requires_manifest_boolean(self):
        bad_doc = GOOD_DOC.replace(structural_row(52), structural_row(52).replace("| true |", "| false |"))
        self.assert_rejects(bad_doc, "#52 requires_manifest_snapshot_id")

    def test_structural_wave_gate_registry_uses_authoritative_success_terms(self):
        bad_doc = GOOD_DOC.replace(structural_row(52), structural_row(52).replace("eligible_candidate_items", "computed_sample"))
        self.assert_rejects(bad_doc, "#52 success_denominator_field")

    def test_control_gate_rows_require_zero_success_sentinel(self):
        bad_doc = GOOD_DOC.replace(
            metric_cell(51),
            "0% direct source ingestion; success = successful_routed_items / eligible_candidate_items * 100; difficulty 1/11",
            1,
        )
        self.assert_rejects(bad_doc, "#51 ingestion metric")

    def test_downstream_rows_reject_zero_success_sentinel(self):
        bad_doc = GOOD_DOC.replace(
            metric_cell(52),
            "0% direct source ingestion; success_metric_applicability=not_applicable_control_plane; expected_yield=0; measured_success_numerator=0; measured_success_denominator=0; success_threshold=0; validation_command=scripts/validate_ace_wave1_text_json.py; difficulty 2/11",
            1,
        )
        self.assert_rejects(bad_doc, "#52 ingestion metric")

    def test_manifest_snapshot_gate_bound_per_downstream_sampling_row(self):
        bad_doc = GOOD_DOC.replace(
            "yes; #62 status:plan-approved+approval marker+implemented validator+recorded passing-command+snapshot_id before sampling",
            "yes; snapshot later",
            1,
        )
        self.assert_rejects(bad_doc, "#52 manifest gate")

    def test_non_sampling_manifest_gate_is_explicit(self):
        bad_doc = GOOD_DOC.replace(
            "not applicable for own sampling; #62 gate applies to downstream sampling",
            "yes; #62 status:plan-approved+approval marker+implemented validator+recorded passing-command+snapshot_id before sampling",
            1,
        )
        self.assert_rejects(bad_doc, "#51 manifest gate")

    def test_manifest_snapshot_gate_rejects_negated_wording(self):
        bad_doc = GOOD_DOC.replace(
            "yes; #62 status:plan-approved+approval marker+implemented validator+recorded passing-command+snapshot_id before sampling",
            "yes; #62 does not require status:plan-approved approval marker implemented validator recorded passing-command snapshot_id",
            1,
        )
        self.assert_rejects(bad_doc, "#52 manifest gate")

    def test_public_redaction_canary_gate_bound_per_row(self):
        bad_doc = GOOD_DOC.replace("yes; #63 status:plan-approved+approval marker+implemented canary+recorded passing-command before publication", "yes; canary later", 1)
        self.assert_rejects(bad_doc, "#51 public canary gate")

    def test_public_redaction_canary_gate_rejects_negated_wording(self):
        bad_doc = GOOD_DOC.replace(
            "yes; #63 status:plan-approved+approval marker+implemented canary+recorded passing-command before publication",
            "yes; #63 does not require status:plan-approved approval marker implemented canary recorded passing-command",
            1,
        )
        self.assert_rejects(bad_doc, "#51 public canary gate")

    def test_bounded_share_reads_are_declared(self):
        bad_doc = GOOD_DOC.replace("maximum files touched: 25; maximum bytes touched: 1048576", "limits TBD")
        self.assert_rejects(bad_doc, "bounded read contract")

    def test_manifest_sources_exact_set_in_inventory(self):
        bad_doc = GOOD_DOC.replace("`_cad-index/cad-readability-index.tsv`, and ", "")
        self.assert_rejects(bad_doc, "manifest source inventory")

    def test_issue_62_handoff_requires_65_and_70(self):
        bad_doc = GOOD_DOC.replace(
            "#65 schema is the canonical registry source; #70 consumes the #62 evidence contract for #67 integration; #51 remains umbrella context only",
            "#51 umbrella context only",
        )
        self.assert_rejects(bad_doc, "#62 dependency handoff")

    def test_unbounded_manifest_traversal_is_denied(self):
        commands = [
            'find ACE_SHARE_ROOT -type f',
            'find "$ACE_SHARE_ROOT" -type f',
            'find ${ACE_SHARE_ROOT} -type f',
            'jq \'.[]\' "$ACE_SHARE_ROOT/assets.json"',
            'cat $ACE_SHARE_ROOT/assets.json',
            'wc -l $ACE_SHARE_ROOT/docs/master-index.jsonl',
            'wc -c $ACE_SHARE_ROOT/assets.json',
            'sha256sum $ACE_SHARE_ROOT/assets.json',
            'Path(ACE_SHARE_ROOT).rglob("*")',
            'grep -R needle $ACE_SHARE_ROOT',
            'grep --recursive needle $ACE_SHARE_ROOT',
            'grep -r needle $ACE_SHARE_ROOT',
            'grep -nr needle "$ACE_SHARE_ROOT"',
            'wc $ACE_SHARE_ROOT/assets.json',
            'ls -R $ACE_SHARE_ROOT',
            'du -sh "$ACE_SHARE_ROOT"',
            'rg needle $ACE_SHARE_ROOT',
            'fd needle $ACE_SHARE_ROOT',
            'os.walk(ACE_SHARE_ROOT)',
        ]
        for command in commands:
            with self.subTest(command=command):
                bad_doc = GOOD_DOC + f"\n\n## Proposed Commands\n- `{command}`\n"
                self.assert_rejects(bad_doc, "unbounded traversal")

    def test_duplicate_child_issue_rows_are_rejected(self):
        duplicate_bad_row = row(52).replace("#1, #12", "#999", 1)
        bad_doc = GOOD_DOC.replace(row(52), duplicate_bad_row + "\n" + row(52))
        self.assert_rejects(bad_doc, "duplicate child issue row")

    def test_child_ledger_header_drift_does_not_skip_row_validation(self):
        bad_doc = GOOD_DOC.replace("| Issue | Plan | Lane | Complexity |", "| Issue Number | Plan | Lane | Complexity |")
        self.assert_rejects(bad_doc, "child wave ledger")

    def test_child_ledger_section_is_required(self):
        bad_doc = GOOD_DOC.replace("## Child Wave Ledger", "## Appendix Table")
        self.assert_rejects(bad_doc, "Child Wave Ledger")

    def test_row_width_must_match_header(self):
        bad_doc = GOOD_DOC.replace("| #51 | docs/plans/issue-51.md |", "| #51 | docs/plans/issue-51.md | extra |", 1)
        self.assert_rejects(bad_doc, "#51 row has")

    def test_ledger_header_schema_must_be_exact(self):
        header = "| Issue | Plan | Lane | Complexity | Plan status | Status snapshot | Implementation ready | Method issues | Skill groups and executable tests | Review artifacts | Dependencies | Expected useful ingestion / success metric / difficulty | Manifest gate | Public canary gate | Method gap disposition | Publication exposure |"
        bad_doc = GOOD_DOC.replace(header, header[:-1] + " Extra |")
        self.assert_rejects(bad_doc, "child wave ledger header")

    def test_required_row_fields_are_validated(self):
        bad_doc = GOOD_DOC.replace("| #52 | docs/plans/issue-52.md | lane:claude | T2 | draft |", "| #52 |  | lane:bad | T9 | unknown |", 1)
        self.assert_rejects(bad_doc, "#52 plan")

    def test_publication_exposure_requires_issue_63_ready(self):
        bad_doc = GOOD_DOC.replace(
            "closed-set: doc-update, skill-eval-update, follow-on-issue | false |",
            "closed-set: doc-update, skill-eval-update, follow-on-issue | true |",
            2,
        )
        self.assert_rejects(bad_doc, "#52 publication exposure")

    def test_gate_ready_requires_executable_and_passing_command_evidence(self):
        validator = load_validator()
        ready_63 = row(63).replace(
            "draft | 2026-06-29 no status label; no approval marker | false",
            "plan-approved | 2026-06-29 status:plan-approved | true",
        )
        exposed_52 = row(52).replace(
            "closed-set: doc-update, skill-eval-update, follow-on-issue | false |",
            "closed-set: doc-update, skill-eval-update, follow-on-issue | true |",
        )
        bad_doc = GOOD_DOC.replace(row(63), ready_63).replace(row(52), exposed_52)
        with tempfile.TemporaryDirectory() as tmp:
            approval_root = Path(tmp)
            (approval_root / "63.md").write_text(valid_marker(63))
            result = validator.validate_text(bad_doc, approval_root=approval_root)

        self.assertIn("#63 gate readiness", "\n".join(result.errors))

    def test_issue_62_gate_ready_requires_snapshot_id(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            executable = Path(tmp) / "validate_ace_manifest_freshness.py"
            executable.write_text("# test executable\n")
            validator.EXPECTED_EXECUTABLE_BINDINGS[62] = {str(executable)}
            status_snapshot = (
                "2026-07-01 status:plan-approved; "
                f"implemented-validator:{executable}; "
                f"passing-command: uv run python {executable}; "
                "exit-code:0"
            )
            ready_62 = (
                row(62)
                .replace("scripts/validate_ace_manifest_freshness.py", str(executable))
                .replace(
                    "draft | 2026-06-29 no status label; no approval marker | false",
                    f"plan-approved | {status_snapshot} | true",
                )
            )
            doc = GOOD_DOC.replace(row(62), ready_62)
            approval_root = Path(tmp)
            (approval_root / "62.md").write_text(valid_marker(62))
            result = validator.validate_text(doc, approval_root=approval_root)

        self.assertIn("#62 gate readiness requires snapshot_id", "\n".join(result.errors))

    def test_issue_62_gate_ready_snapshot_id_must_match_evidence(self):
        validator = load_validator()
        status_snapshot = (
            "2026-07-01 status:plan-approved; "
            "implemented-validator:scripts/validate_ace_manifest_freshness.py; "
            "passing-command: uv run python scripts/validate_ace_manifest_freshness.py "
            "--evidence tests/fixtures/ace-manifest-freshness/valid-operational-evidence.json; "
            "exit-code:0; "
            "snapshot_id:ams_deadbeefdeadbeefdeadbeefdeadbeef"
        )
        ready_62 = row(62).replace(
            "draft | 2026-06-29 no status label; no approval marker | false",
            f"plan-approved | {status_snapshot} | true",
        )
        doc = GOOD_DOC.replace(row(62), ready_62)
        with tempfile.TemporaryDirectory() as tmp:
            approval_root = Path(tmp)
            (approval_root / "62.md").write_text(valid_marker(62))
            result = validator.validate_text(doc, approval_root=approval_root)

        self.assertIn("#62 gate readiness snapshot_id must match validated evidence", "\n".join(result.errors))

    def test_issue_62_gate_ready_rejects_forged_evidence_outside_allowed_roots(self):
        validator = load_validator()
        forged_ref = Path("tests/fixtures/forged-ace62-evidence.json")
        forged = REPO_ROOT / forged_ref
        if forged.exists():
            forged.unlink()
        self.addCleanup(lambda: forged.exists() and forged.unlink())
        forged.write_text(
            json.dumps(
                {
                    "snapshot_ids_by_manifest_source": {
                        "INDEX.md": "ams_deadbeefdeadbeefdeadbeefdeadbeef",
                        "assets.json": "ams_00000000000000000000000000000002",
                        "docs/master-index.jsonl": "ams_00000000000000000000000000000003",
                        "_cad-index/index-summary.json": "ams_00000000000000000000000000000004",
                        "_cad-index/cad-readability-index.tsv": "ams_00000000000000000000000000000005",
                        ".ace-knowledge/index.db": "ams_00000000000000000000000000000006",
                    }
                }
            )
        )
        status_snapshot = (
            "2026-07-01 status:plan-approved; "
            "implemented-validator:scripts/validate_ace_manifest_freshness.py; "
            f"passing-command: uv run python scripts/validate_ace_manifest_freshness.py --evidence {forged_ref}; "
            "exit-code:0; "
            "snapshot_id:ams_deadbeefdeadbeefdeadbeefdeadbeef"
        )
        ready_62 = row(62).replace(
            "draft | 2026-06-29 no status label; no approval marker | false",
            f"plan-approved | {status_snapshot} | true",
        )
        doc = GOOD_DOC.replace(row(62), ready_62)
        with tempfile.TemporaryDirectory() as tmp:
            approval_root = Path(tmp)
            (approval_root / "62.md").write_text(valid_marker(62))
            result = validator.validate_text(doc, approval_root=approval_root)

        self.assertIn("#62 gate readiness requires allowed evidence artifact", "\n".join(result.errors))

    def test_gate_ready_rejects_placeholder_passing_command_evidence(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            executable = Path(tmp) / "validate_ace_public_artifacts.py"
            executable.write_text("# test executable\n")
            validator.EXPECTED_EXECUTABLE_BINDINGS[63] = {str(executable)}
            status_snapshot = (
                "2026-06-29 status:plan-approved; "
                f"implemented-canary:{executable}; "
                f"passing-command: not run {executable}; "
                "exit-code:0 expected"
            )
            ready_63 = (
                row(63)
                .replace("scripts/validate_ace_public_artifacts.py", str(executable))
                .replace(
                    "draft | 2026-06-29 no status label; no approval marker | false",
                    f"plan-approved | {status_snapshot} | true",
                )
            )
            exposed_52 = row(52).replace(
                "closed-set: doc-update, skill-eval-update, follow-on-issue | false |",
                "closed-set: doc-update, skill-eval-update, follow-on-issue | true |",
            )
            bad_doc = GOOD_DOC.replace(row(63), ready_63).replace(row(52), exposed_52)
            approval_root = Path(tmp)
            (approval_root / "63.md").write_text(valid_marker(63))
            result = validator.validate_text(bad_doc, approval_root=approval_root)

        self.assertIn("#63 gate readiness", "\n".join(result.errors))

    def test_gate_ready_rejects_hyphenated_not_run_evidence(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            executable = Path(tmp) / "validate_ace_public_artifacts.py"
            executable.write_text("# test executable\n")
            validator.EXPECTED_EXECUTABLE_BINDINGS[63] = {str(executable)}
            status_snapshot = (
                "2026-06-29 status:plan-approved; "
                f"implemented-canary:{executable}; "
                f"passing-command:not-run {executable}; "
                "exit-code:0"
            )
            ready_63 = (
                row(63)
                .replace("scripts/validate_ace_public_artifacts.py", str(executable))
                .replace(
                    "draft | 2026-06-29 no status label; no approval marker | false",
                    f"plan-approved | {status_snapshot} | true",
                )
            )
            exposed_52 = row(52).replace(
                "closed-set: doc-update, skill-eval-update, follow-on-issue | false |",
                "closed-set: doc-update, skill-eval-update, follow-on-issue | true |",
            )
            bad_doc = GOOD_DOC.replace(row(63), ready_63).replace(row(52), exposed_52)
            approval_root = Path(tmp)
            (approval_root / "63.md").write_text(valid_marker(63))
            result = validator.validate_text(bad_doc, approval_root=approval_root)

        self.assertIn("#63 gate readiness", "\n".join(result.errors))

    def test_publication_exposure_allows_structured_issue_63_evidence(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            executable = Path(tmp) / "validate_ace_public_artifacts.py"
            executable.write_text("# test executable\n")
            validator.EXPECTED_EXECUTABLE_BINDINGS[63] = {str(executable)}
            status_snapshot = (
                "2026-06-29 status:plan-approved; "
                f"implemented-canary:{executable}; "
                f"passing-command: uv run python {executable}; "
                "exit-code:0"
            )
            ready_63 = (
                row(63)
                .replace("scripts/validate_ace_public_artifacts.py", str(executable))
                .replace(
                    "draft | 2026-06-29 no status label; no approval marker | false",
                    f"plan-approved | {status_snapshot} | true",
                )
            )
            exposed_52 = row(52).replace(
                "closed-set: doc-update, skill-eval-update, follow-on-issue | false |",
                "closed-set: doc-update, skill-eval-update, follow-on-issue | true |",
            )
            good_doc = GOOD_DOC.replace(row(63), ready_63).replace(row(52), exposed_52)
            approval_root = Path(tmp)
            (approval_root / "63.md").write_text(valid_marker(63))
            result = validator.validate_text(good_doc, approval_root=approval_root)

        self.assertEqual([], result.errors)

    def test_public_artifact_scan_rejects_missing_paths(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            result = validator.validate_public_artifact_paths([Path(tmp) / "missing.md"])

        self.assertIn("missing public artifact scan path", "\n".join(result))

    def test_public_artifact_scan_rejects_leaks(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "public.md"
            path.write_text(f"contact {PRIVATE_EMAIL}\n")
            result = validator.validate_public_artifact_paths([path])

        self.assertIn("public artifact leak", "\n".join(result))

    def test_public_artifact_scan_rejects_python_file_leaks(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "public.py"
            path.write_text(f"PRIVATE_PATH = {PRIVATE_SOURCE_PATH!r}\nCONTACT = {PRIVATE_EMAIL!r}\n")
            result = validator.validate_public_artifact_paths([path])

        self.assertIn("public artifact leak", "\n".join(result))

    def test_public_artifact_scan_rejects_local_runtime_file_uris(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review.md"
            path.write_text("provider trace: file://" + "/" + "home/agent/.npm-global/lib/tool.js\n")
            result = validator.validate_public_artifact_paths([path])

        self.assertIn("public artifact leak", "\n".join(result))

    def test_public_artifact_scan_rejects_local_home_paths(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "review.md"
            path.write_text("provider trace: " + "/" + "home/agent/.codex/auth.json\n")
            result = validator.validate_public_artifact_paths([path])

        self.assertIn("public artifact leak", "\n".join(result))

    def test_public_artifact_scan_rejects_unbounded_traversal_examples(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "comment.md"
            path.write_text("Example to reject: `find ACE_SHARE_ROOT -type f`.\n")
            result = validator.validate_public_artifact_paths([path])

        self.assertIn("unbounded traversal", "\n".join(result))

    def test_public_artifact_scan_rejects_assigned_private_source_fields(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "comment.md"
            path.write_text(
                "source_id: vendor_doc_001\n"
                "source_sha256: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef\n"
                "private_lookup_key: lookup_001\n"
                "private_lookup_map: {lookup_001: vendor_doc_001}\n"
                "public_source_token: pst_0123456789abcdef0123456789abcdef\n"
            )
            result = validator.validate_public_artifact_paths([path])

        self.assertIn("private source field assignment", "\n".join(result))

    def test_public_artifact_scan_rejects_private_source_field_table_rows(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "comment.md"
            path.write_text(
                "| field | value |\n"
                "|---|---|\n"
                "| source_id | PRIVATE-123 |\n"
                "| private_lookup_key | lookup-abc |\n"
                "| share_relative_path_private_only | reports/private.docx |\n"
            )
            result = validator.validate_public_artifact_paths([path])

        self.assertIn("private source field assignment", "\n".join(result))

    def test_public_artifact_scan_rejects_source_hash_values(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "comment.md"
            path.write_text(
                "source hash: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef\n"
                "| source_sha256 | 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef |\n"
            )
            result = validator.validate_public_artifact_paths([path])

        self.assertIn("source-like raw digest", "\n".join(result))

    def test_public_artifact_scan_allows_fixed_metadata_evidence_rows(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evidence.md"
            path.write_text(
                "EXISTS ACE_SHARE_ROOT/INDEX.md type=file details=withheld_public\n"
                "EXISTS ACE_SHARE_ROOT/assets.json type=file details=withheld_public\n"
                "EXISTS ACE_SHARE_ROOT/docs/master-index.jsonl type=file details=withheld_public\n"
                "EXISTS ACE_SHARE_ROOT/_cad-index/index-summary.json type=file details=withheld_public\n"
                "EXISTS ACE_SHARE_ROOT/_cad-index/cad-readability-index.tsv type=file details=withheld_public\n"
                "EXISTS ACE_SHARE_ROOT/.ace-knowledge/index.db type=file details=withheld_public\n"
                "EXISTS ACE_SHARE_ROOT/llm-wiki type=directory details=withheld_public\n"
            )
            result = validator.validate_public_artifact_paths([path])

        self.assertEqual([], result)

    def test_public_artifact_scan_rejects_unlisted_metadata_evidence_rows(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evidence.md"
            path.write_text("EXISTS ACE_SHARE_ROOT/private/internal/report.docx type=file details=withheld_public\n")
            result = validator.validate_public_artifact_paths([path])

        self.assertIn("unlisted ACE metadata evidence path", "\n".join(result))

    def test_public_artifact_scan_allows_source_field_policy_prose(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.md"
            path.write_text(
                "Policy may name source_id, source_sha256, private_lookup_key, "
                "private_lookup_map, share_relative_path_private_only, and "
                "public_source_token as schema field names only.\n"
            )
            result = validator.validate_public_artifact_paths([path])

        self.assertEqual([], result)

    def test_public_artifact_scan_allows_denied_traversal_policy_prose(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.md"
            path.write_text(
                "- Denied traversal patterns: recursive walk; `os.walk`; `ls -R`; `find`.\n"
                "| test_unbounded_manifest_traversal_is_denied | Recursive share walk, unrestricted `jq`, "
                "`os.walk`, `ls -R`, `find`, `du`, `rg`, and `fd` patterns fail validation |\n"
            )
            result = validator.validate_public_artifact_paths([path])

        self.assertEqual([], result)

    def test_validator_source_is_not_self_blocking_public_artifact(self):
        validator = load_validator()
        result = validator.validate_public_artifact_paths([VALIDATOR_PATH])

        self.assertEqual([], result)


if __name__ == "__main__":
    unittest.main()
