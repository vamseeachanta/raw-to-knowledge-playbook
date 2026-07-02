from __future__ import annotations

from tests.ace_public_surface_test_helpers import *


class AcePublicSurfaceReviewTests(unittest.TestCase):
    def test_review_artifact_selector_is_bounded(self):
        validator = load_validator()

        root = REPO_ROOT / "scripts" / "review" / "results"
        artifact = write_tmp(root.as_posix(), "2099-01-01-plan-68-claude-r99.md", "## Verdict\nAPPROVE\n")
        ignored = write_tmp(root.as_posix(), "2099-01-01-plan-67-claude-r99.md", "## Verdict\nAPPROVE\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())
        self.addCleanup(lambda: ignored.exists() and ignored.unlink())

        selected, errors = validator.select_review_artifact_paths(
            review_issue=68,
            phase="plan",
            provider="claude",
            round_id="r99",
        )

        self.assertEqual([], errors)
        self.assertIn(artifact, selected)
        self.assertNotIn(ignored, selected)

    def test_review_artifact_selector_rejects_non_date_prefix_and_custom_root(self):
        validator = load_validator()

        root = REPO_ROOT / "scripts" / "review" / "results"
        artifact = write_tmp(root.as_posix(), "not-date-plan-68-claude-r99.md", "## Verdict\nAPPROVE\n")
        wildcard = write_tmp(root.as_posix(), "abcd-ef-gh-plan-68-claude-r99.md", "## Verdict\nAPPROVE\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())
        self.addCleanup(lambda: wildcard.exists() and wildcard.unlink())

        selected, errors = validator.select_review_artifact_paths(
            review_issue=68,
            phase="plan",
            provider="claude",
            round_id="r99",
        )
        _, root_errors = validator.select_review_artifact_paths(
            review_issue=68,
            phase="plan",
            provider="claude",
            round_id="r99",
            review_root=REPO_ROOT / "docs",
        )

        self.assertNotIn(artifact, selected)
        self.assertNotIn(wildcard, selected)
        self.assertIn("review-root", "\n".join(root_errors))

    def test_review_artifact_selector_rejects_traversal_symlinks_and_unknown_provider(self):
        validator = load_validator()

        root = REPO_ROOT / "scripts" / "review" / "results"
        outside = write_tmp(REPO_ROOT.as_posix(), ".tmp-outside-review.md", "## Verdict\nAPPROVE\n")
        link = root / "2099-01-02-plan-68-claude-r98.md"
        if link.exists() or link.is_symlink():
            link.unlink()
        link.symlink_to(outside)
        self.addCleanup(lambda: outside.exists() and outside.unlink())
        self.addCleanup(lambda: link.exists() and link.unlink())
        _, unknown_errors = validator.select_review_artifact_paths(
            review_issue=68,
            phase="plan",
            provider="unknown",
            round_id="r3",
        )
        _, symlink_errors = validator.select_review_artifact_paths(
            review_issue=68,
            phase="plan",
            provider="claude",
            round_id="r98",
        )

        self.assertIn("review-provider", "\n".join(unknown_errors))
        self.assertIn("review-artifact-symlink", "\n".join(symlink_errors))

    def test_same_stem_sidecars_are_scanned(self):
        validator = load_validator()

        root = REPO_ROOT / "scripts" / "review" / "results"
        artifact = write_tmp(root.as_posix(), "2099-01-03-plan-68-claude-r97.md", "## Verdict\nAPPROVE\n")
        sidecar = write_tmp(root.as_posix(), "2099-01-03-plan-68-claude-r97.stderr", f"trace: file://{private_path_text()}\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())
        self.addCleanup(lambda: sidecar.exists() and sidecar.unlink())
        errors = validator.validate_review_artifacts(
            review_issue=68,
            phase="plan",
            provider="claude",
            round_id="r97",
            include_sidecars=True,
        )

        self.assertIn("provider-sidecar-leak", "\n".join(errors))

    def test_sidecar_absence_semantics_are_explicit(self):
        validator = load_validator()

        root = REPO_ROOT / "scripts" / "review" / "results"
        artifact = write_tmp(root.as_posix(), "2099-01-04-plan-68-claude-r96.md", "## Verdict\nAPPROVE\n")
        self.addCleanup(lambda: artifact.exists() and artifact.unlink())
        optional = validator.review_sidecar_status(
            review_issue=68,
            phase="plan",
            provider="claude",
            round_id="r96",
        )
        required = validator.validate_review_artifacts(
            review_issue=68,
            phase="plan",
            provider="claude",
            round_id="r96",
            include_sidecars=True,
            sidecar_required=True,
        )

        self.assertEqual("sidecar_status=none_found", optional)
        self.assertIn("sidecar-required", "\n".join(required))

    def test_issue_comment_snapshot_schema_is_closed(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            good_record = snapshot_record(body="safe body\n", source_kind="planned_comment", phase="pre_post")
            extra_record = dict(good_record)
            extra_record["extra"] = "not allowed"
            invalid_phase = dict(good_record)
            invalid_phase["phase"] = "posted"
            good = write_tmp(tmp, "good.json", json.dumps(good_record))
            extra = write_tmp(tmp, "extra.json", json.dumps(extra_record))
            phase = write_tmp(tmp, "phase.json", json.dumps(invalid_phase))

            self.assertEqual([], validator.validate_issue_comment_snapshot_file(good))
            joined = "\n".join(
                validator.validate_issue_comment_snapshot_file(extra)
                + validator.validate_issue_comment_snapshot_file(phase)
            )

        self.assertIn("snapshot-keys", joined)
        self.assertIn("snapshot-phase", joined)

    def test_issue_comment_snapshot_pairing_is_enforced(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            body = "safe body\n"
            pre = write_tmp(
                tmp,
                "pre.json",
                json.dumps(snapshot_record(body=body, source_kind="planned_comment", phase="pre_post")),
            )
            post = write_tmp(
                tmp,
                "post.json",
                json.dumps(
                    snapshot_record(
                        body=body,
                        source_kind="issue_comment",
                        phase="post_refetch",
                        comment_id=123,
                        url="https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68#issuecomment-123",
                    )
                ),
            )
            mismatched = write_tmp(
                tmp,
                "mismatch.json",
                json.dumps(
                    snapshot_record(
                        body="changed body\n",
                        source_kind="issue_comment",
                        phase="post_refetch",
                        comment_id=123,
                        url="https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68#issuecomment-123",
                    )
                ),
            )

            self.assertEqual([], validator.validate_issue_comment_snapshot_pair(pre, post))
            errors = validator.validate_issue_comment_snapshot_pair(pre, mismatched)

        self.assertIn("snapshot-pair-body-hash", "\n".join(errors))

    def test_issue_comment_snapshot_rejects_forged_url_relationship(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            body = "safe body\n"
            forged = write_tmp(
                tmp,
                "forged.json",
                json.dumps(
                    snapshot_record(
                        body=body,
                        source_kind="issue_comment",
                        phase="post_refetch",
                        comment_id=123,
                        url="https://example.com/wrong/issues/68#issuecomment-999",
                    )
                ),
            )
            errors = validator.validate_issue_comment_snapshot_file(forged)

        self.assertIn("snapshot-url", "\n".join(errors))

    def test_planned_comment_snapshot_rejects_forged_issue_url(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            forged = write_tmp(
                tmp.as_posix(),
                "planned.json",
                json.dumps(
                    snapshot_record(
                        body="safe body\n",
                        source_kind="planned_comment",
                        phase="pre_post",
                        url="https://example.com/vamseeachanta/raw-to-knowledge-playbook/issues/68",
                    )
                ),
            )
            errors = validator.validate_issue_comment_snapshot_file(forged)

        self.assertIn("snapshot-url", "\n".join(errors))

    def test_issue_comment_body_files_scan_before_and_after_posting(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            unsafe_pre = write_tmp(
                tmp,
                "unsafe-pre.json",
                json.dumps(
                    snapshot_record(
                        body=f"contact: {personal_email_text()}\n",
                        source_kind="planned_comment",
                        phase="pre_post",
                    )
                ),
            )
            safe_post = write_tmp(
                tmp,
                "safe-post.json",
                json.dumps(
                    snapshot_record(
                        body="safe body\n",
                        source_kind="issue_comment",
                        phase="post_refetch",
                        comment_id=123,
                        url="https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68#issuecomment-123",
                    )
                ),
            )

            pre_errors = validator.validate_issue_comment_snapshot_file(unsafe_pre)
            post_errors = validator.validate_issue_comment_snapshot_file(safe_post)

        self.assertIn("personal-identifier", "\n".join(pre_errors))
        self.assertEqual([], post_errors)

    def test_workflow_preserves_69_legal_scan_step(self):
        workflow = WORKFLOW_PATH.read_text()

        self.assertIn("bash scripts/legal/legal-sanity-scan.sh --all-tracked-public-surfaces", workflow)

    def test_stock_ci_has_no_live_github_dependency(self):
        workflow = WORKFLOW_PATH.read_text()

        self.assertNotIn("GH_TOKEN", workflow)
        self.assertNotIn("gh issue", workflow)
        self.assertNotIn("api.github.com", workflow)

    def test_ci_invokes_public_surface_scanner(self):
        workflow = WORKFLOW_PATH.read_text()

        self.assertIn("scripts/validate_ace_public_surface_scan.py", workflow)
        self.assertIn("scripts/ace_public_surface_rules.py", workflow)
        self.assertIn("tests.test_validate_ace_public_surface_scan", workflow)
        self.assertIn("--scan-public-path config/ace-public-surface-self-scan-contract.json", workflow)
        self.assertIn("--review-issue 68", workflow)
        self.assertIn("--include-sidecars", workflow)

    def test_cli_scan_uses_supplied_contract_path(self):
        validator = load_validator()
        contract = load_json(CONTRACT_PATH)
        contract["owner_issue"] = 999

        with repo_tmpdir() as tmp:
            contract_path = write_tmp(tmp, "bad-contract.json", json.dumps(contract))
            args = type(
                "Args",
                (),
                {
                    "contract": str(contract_path),
                    "scan_public_path": [str(CONTRACT_PATH)],
                    "review_issue": None,
                    "review_phase": None,
                    "review_provider": None,
                    "review_round": None,
                    "review_root": "scripts/review/results",
                    "include_sidecars": False,
                    "sidecar_required": False,
                    "snapshot": [],
                    "snapshot_pair": [],
                },
            )()
            errors = validator.collect_errors(args)

        self.assertIn("owner_issue", "\n".join(errors))

    def test_cli_review_and_snapshot_use_supplied_contract_path(self):
        validator = load_validator()
        contract = load_json(CONTRACT_PATH)
        contract["owner_issue"] = 999
        root = REPO_ROOT / "scripts" / "review" / "results"
        artifact = write_tmp(root.as_posix(), "2099-01-05-plan-68-claude-r95.md", "## Verdict\nAPPROVE\n")

        with repo_tmpdir() as tmp:
            contract_path = write_tmp(tmp.as_posix(), "bad-contract.json", json.dumps(contract))
            snapshot = write_tmp(
                tmp.as_posix(),
                "snapshot.json",
                json.dumps(snapshot_record(body="safe\n", source_kind="planned_comment", phase="pre_post")),
            )
            args = type(
                "Args",
                (),
                {
                    "contract": str(contract_path),
                    "scan_public_path": [],
                    "review_issue": 68,
                    "review_phase": "plan",
                    "review_provider": "claude",
                    "review_round": "r95",
                    "review_root": "scripts/review/results",
                    "include_sidecars": False,
                    "sidecar_required": False,
                    "snapshot": [str(snapshot)],
                    "snapshot_pair": [],
                },
            )()
            errors = validator.collect_errors(args)

        if artifact.exists():
            artifact.unlink()
        self.assertIn("owner_issue", "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
