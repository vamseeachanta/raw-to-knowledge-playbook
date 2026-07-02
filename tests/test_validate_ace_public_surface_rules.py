from __future__ import annotations

from tests.ace_public_surface_test_helpers import *


class AcePublicSurfaceRulesTests(unittest.TestCase):
    def test_blocks_raw_host_and_source_paths(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            path = write_tmp(tmp, "public.md", f"unsafe: {private_path_text()}\n")
            errors = validator.validate_public_artifact_paths([path])

        self.assertIn("raw-host-path", "\n".join(errors))
        self.assertNotIn(private_path_text(), "\n".join(errors))

    def test_blocks_personal_identifier_patterns(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            path = write_tmp(tmp, "public.md", f"contact: {personal_email_text()}\n")
            errors = validator.validate_public_artifact_paths([path])

        self.assertIn("personal-identifier", "\n".join(errors))
        self.assertNotIn(personal_email_text(), "\n".join(errors))

    def test_blocks_confidentiality_marker_phrases(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            path = write_tmp(tmp, "public.md", confidential_text() + "\n")
            errors = validator.validate_public_artifact_paths([path])

        self.assertIn("confidentiality-marker", "\n".join(errors))

    def test_blocks_generic_private_like_identifiers(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            path = write_tmp(tmp, "public.md", "client_" + "id=ACME-123\n")
            errors = validator.validate_public_artifact_paths([path])

        self.assertIn("generic-private-identifier", "\n".join(errors))

    def test_blocks_private_source_field_assignments(self):
        validator = load_validator()
        token_contract = load_json(TOKEN_CONTRACT_PATH)

        with repo_tmpdir() as tmp:
            for term in token_contract["private_source_terms"]:
                with self.subTest(term=term):
                    path = write_tmp(tmp, f"{term}.json", json.dumps({term: "public-looking"}))
                    errors = validator.validate_public_artifact_paths([path])
                    self.assertIn("private-source-key", "\n".join(errors))

    def test_blocks_private_source_keys_regardless_of_value_shape(self):
        validator = load_validator()
        token_contract = load_json(TOKEN_CONTRACT_PATH)
        value_shapes = [
            token_contract["placeholder_values"][0],
            "safe-looking",
            None,
            ["safe-looking"],
            {"nested": "safe-looking"},
        ]

        with repo_tmpdir() as tmp:
            for term in token_contract["private_source_terms"]:
                for index, value in enumerate(value_shapes):
                    with self.subTest(term=term, shape=index):
                        path = write_tmp(tmp, f"private-{index}.json", json.dumps({term: value}))
                        errors = validator.validate_public_artifact_paths([path])
                        self.assertIn("private-source-key", "\n".join(errors))

    def test_blocks_source_like_digest_keys_regardless_of_value_shape(self):
        validator = load_validator()
        token_contract = load_json(TOKEN_CONTRACT_PATH)
        value_shapes = [token_contract["placeholder_values"][0], "safe-looking", None, [], {}]

        with repo_tmpdir() as tmp:
            for term in token_contract["source_like_raw_digest_terms"]:
                for index, value in enumerate(value_shapes):
                    with self.subTest(term=term, shape=index):
                        path = write_tmp(tmp, f"digest-{index}.json", json.dumps({term: value}))
                        errors = validator.validate_public_artifact_paths([path])
                        self.assertIn("source-like-key", "\n".join(errors))

    def test_blocks_66_forbidden_request_keys_as_public_keys_or_assignments(self):
        validator = load_validator()
        token_contract = load_json(TOKEN_CONTRACT_PATH)

        with repo_tmpdir() as tmp:
            for key in token_contract["forbidden_request_keys"]:
                with self.subTest(key=key):
                    keyed = write_tmp(tmp, f"{key}.json", json.dumps({key: "public-looking"}))
                    assigned = write_tmp(tmp, f"{key}.txt", f"{key}=public-looking\n")
                    errors = validator.validate_public_artifact_paths([keyed, assigned])
                    self.assertIn("forbidden-request-key", "\n".join(errors))

    def test_blocks_assigned_source_like_digest_values(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            path = write_tmp(tmp, "digest.txt", f"{'source_' + 'hash'}={digest_value()}\n")
            errors = validator.validate_public_artifact_paths([path])

        self.assertIn("source-like-digest-assignment", "\n".join(errors))

    def test_blocks_public_source_token_assignment(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            path = write_tmp(tmp, "token.txt", f"public_source_token={public_token_value()}\n")
            errors = validator.validate_public_artifact_paths([path])

        self.assertIn("public-token-assignment", "\n".join(errors))

    def test_blocks_provider_stderr_and_log_sidecar_leaks(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            path = write_tmp(tmp, "provider.stderr", f"trace: file://{private_path_text()}\n")
            errors = validator.validate_public_artifact_paths([path])

        self.assertIn("provider-sidecar-leak", "\n".join(errors))
        self.assertNotIn(private_path_text(), "\n".join(errors))

    def test_allows_fixed_metadata_evidence_shape_only(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            good = write_tmp(
                tmp,
                "good.md",
                metadata_evidence_line("INDEX.md", "file")
                + metadata_evidence_line("assets.json", "file")
                + metadata_evidence_line("llm-wiki", "directory"),
            )
            bad = write_tmp(tmp, "bad.md", metadata_evidence_line("private/report.docx", "file"))

            self.assertEqual([], validator.validate_public_artifact_paths([good]))
            errors = validator.validate_public_artifact_paths([bad])

        self.assertIn("metadata-evidence-path", "\n".join(errors))

    def test_blocks_unbounded_manifest_traversal_examples(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            path = write_tmp(tmp, "walk.md", f"find {ace_root()} -type f\n")
            errors = validator.validate_public_artifact_paths([path])

        self.assertIn("unbounded-traversal-command", "\n".join(errors))

    def test_blocks_recursive_grep_manifest_traversal_examples(self):
        validator = load_validator()
        grep = "gr" + "ep"
        examples = [
            f"{grep} -R needle {ace_root()}",
            f"{grep} -r needle assets.json",
            f"{grep} --recursive needle master-index.jsonl",
            f"{grep} -Rn needle index.db",
            f"{grep} -r needle _cad-index",
        ]

        with repo_tmpdir() as tmp:
            for index, command in enumerate(examples):
                with self.subTest(command=command):
                    path = write_tmp(tmp, f"grep-{index}.md", command + "\n")
                    errors = validator.validate_public_artifact_paths([path])
                    self.assertIn("unbounded-traversal-command", "\n".join(errors))

    def test_allow_context_does_not_hide_other_deny_classes(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            path = write_tmp(
                tmp.as_posix(),
                "docs/plans/2026-06-30-issue-68-example.md",
                "\n".join(
                    [
                        "## Pseudocode",
                        allow_start("schema-term-policy-prose", "schema_term"),
                        "source_id " + personal_email_text(),
                        allow_end("schema-term-policy-prose"),
                    ]
                ),
            )
            errors = validator.validate_public_artifact_paths([repo_relative(path)])

        self.assertIn("personal-identifier", "\n".join(errors))

    def test_allow_context_does_not_hide_assignment_values(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            path = write_tmp(
                tmp.as_posix(),
                "docs/plans/2026-06-30-issue-68-example.md",
                "\n".join(
                    [
                        "## Pseudocode",
                        allow_start("schema-term-policy-prose", "schema_term"),
                        "source_" + "id: vendor_doc_001",
                        allow_end("schema-term-policy-prose"),
                    ]
                ),
            )
            errors = validator.validate_public_artifact_paths([repo_relative(path)])

        self.assertIn("private-source-key", "\n".join(errors))

    def test_public_scan_rejects_outside_absolute_parent_traversal_and_symlinks(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            safe = write_tmp(tmp.as_posix(), "safe.md", "safe\n")
            link = tmp / "linked.md"
            link.symlink_to(safe)
            errors = (
                validator.validate_public_artifact_paths([Path("/tmp/outside.md")])
                + validator.validate_public_artifact_paths([Path("../outside.md")])
                + validator.validate_public_artifact_paths([repo_relative(link)])
            )

        joined = "\n".join(errors)
        self.assertIn("scan-path-absolute", joined)
        self.assertIn("scan-path-traversal", joined)
        self.assertIn("scan-path-symlink", joined)

    def test_public_scan_rejects_symlink_ancestor_escape(self):
        validator = load_validator()

        with repo_tmpdir() as tmp, tempfile.TemporaryDirectory() as outside_tmp:
            outside = write_tmp(outside_tmp, "outside.md", "safe\n")
            link_dir = tmp / "linked-dir"
            link_dir.symlink_to(outside.parent, target_is_directory=True)
            errors = validator.validate_public_artifact_paths([repo_relative(link_dir / "outside.md")])

        self.assertIn("scan-path-symlink", "\n".join(errors))

    def test_allow_context_ids_are_closed(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            path = write_tmp(
                tmp,
                "docs/plans/2026-06-30-issue-68-example.md",
                allowed_schema_term_block(context_id="unknown-context"),
            )
            errors = validator.validate_public_artifact_paths([path])

        self.assertIn("allow-context-unknown", "\n".join(errors))

    def test_allow_context_requires_start_and_end_sentinels(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            missing_end = write_tmp(
                tmp,
                "docs/plans/2026-06-30-issue-68-example.md",
                "\n".join(["## Pseudocode", allow_start("schema-term-policy-prose", "schema_term"), "source_id"]),
            )
            stray_end = write_tmp(
                tmp,
                "docs/plans/2026-06-30-issue-68-stray.md",
                "\n".join(["## Pseudocode", "source_id", allow_end("schema-term-policy-prose")]),
            )
            errors = validator.validate_public_artifact_paths([missing_end, stray_end])

        joined = "\n".join(errors)
        self.assertIn("allow-context-eof", joined)
        self.assertIn("allow-context-stray-end", joined)

    def test_allow_context_enforces_path_and_heading_constraints(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            wrong_path = write_tmp(tmp, "docs/plans/issue-67-example.md", allowed_schema_term_block())
            wrong_heading = write_tmp(
                tmp,
                "docs/plans/2026-06-30-issue-68-example.md",
                allowed_schema_term_block().replace("## Pseudocode", "## Random Notes"),
            )
            errors = validator.validate_public_artifact_paths([wrong_path, wrong_heading])

        joined = "\n".join(errors)
        self.assertIn("allow-context-path", joined)
        self.assertIn("allow-context-heading", joined)

    def test_allow_context_enforces_token_classes_and_max_lines(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            wrong_token = write_tmp(
                tmp,
                "docs/plans/2026-06-30-issue-68-token.md",
                allowed_schema_term_block(token_class="review_finding_excerpt"),
            )
            too_long = "\n".join(
                ["## Pseudocode", allow_start("schema-term-policy-prose", "schema_term")]
                + ["source_id" for _ in range(41)]
                + [allow_end("schema-term-policy-prose")]
            )
            over_budget = write_tmp(tmp, "docs/plans/2026-06-30-issue-68-long.md", too_long)
            errors = validator.validate_public_artifact_paths([wrong_token, over_budget])

        joined = "\n".join(errors)
        self.assertIn("allow-context-token-class", joined)
        self.assertIn("allow-context-line-budget", joined)

    def test_allow_context_rejects_nested_overlapping_and_eof_blocks(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            nested = "\n".join(
                [
                    "## Pseudocode",
                    allow_start("schema-term-policy-prose", "schema_term"),
                    allow_start("schema-term-policy-prose", "schema_term"),
                    "source_id",
                    allow_end("schema-term-policy-prose"),
                    allow_end("schema-term-policy-prose"),
                ]
            )
            path = write_tmp(tmp, "docs/plans/2026-06-30-issue-68-nested.md", nested)
            errors = validator.validate_public_artifact_paths([path])

        self.assertIn("allow-context-nested", "\n".join(errors))

    def test_json_and_python_artifacts_do_not_use_html_comment_sentinels(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            json_path = write_tmp(
                tmp,
                "contract.json",
                json.dumps({"note": allow_start("schema-term-policy-prose", "schema_term")}),
            )
            py_path = write_tmp(
                tmp,
                "scanner.py",
                f"NOTE = {allow_start('schema-term-policy-prose', 'schema_term')!r}\n",
            )
            errors = validator.validate_public_artifact_paths([json_path, py_path])

        self.assertIn("allow-context-forbidden-filetype", "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
