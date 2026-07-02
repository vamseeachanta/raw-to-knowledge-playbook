from __future__ import annotations

from tests.ace_public_surface_test_helpers import *


class AcePublicSurfaceSnapshotUrlTests(unittest.TestCase):
    def test_snapshot_urls_require_https_and_no_unexpected_parts(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            planned_fragment = write_tmp(
                tmp.as_posix(),
                "planned-fragment.json",
                json.dumps(
                    snapshot_record(
                        body="safe body\n",
                        source_kind="planned_comment",
                        phase="pre_post",
                        url="https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68#issuecomment-999",
                    )
                ),
            )
            planned_http = write_tmp(
                tmp.as_posix(),
                "planned-http.json",
                json.dumps(
                    snapshot_record(
                        body="safe body\n",
                        source_kind="planned_comment",
                        phase="pre_post",
                        url="http://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68",
                    )
                ),
            )
            comment_query = write_tmp(
                tmp.as_posix(),
                "comment-query.json",
                json.dumps(
                    snapshot_record(
                        body="safe body\n",
                        source_kind="issue_comment",
                        phase="post_refetch",
                        comment_id=123,
                        url="http://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68?x=1#issuecomment-123",
                    )
                ),
            )
            errors = (
                validator.validate_issue_comment_snapshot_file(planned_fragment)
                + validator.validate_issue_comment_snapshot_file(planned_http)
                + validator.validate_issue_comment_snapshot_file(comment_query)
            )

        self.assertEqual(3, "\n".join(errors).count("snapshot-url"))

    def test_snapshot_urls_are_pinned_to_issue_68(self):
        validator = load_validator()

        with repo_tmpdir() as tmp:
            planned_url_69 = write_tmp(
                tmp.as_posix(),
                "planned-69.json",
                json.dumps(
                    snapshot_record(
                        body="safe body\n",
                        source_kind="planned_comment",
                        phase="pre_post",
                        issue_number=69,
                        url="https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69",
                    )
                ),
            )
            comment_url_69 = write_tmp(
                tmp.as_posix(),
                "comment-69.json",
                json.dumps(
                    snapshot_record(
                        body="safe body\n",
                        source_kind="issue_comment",
                        phase="post_refetch",
                        issue_number=69,
                        comment_id=123,
                        url="https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/69#issuecomment-123",
                    )
                ),
            )
            planned_claim_69 = write_tmp(
                tmp.as_posix(),
                "planned-claim-69.json",
                json.dumps(
                    snapshot_record(
                        body="safe body\n",
                        source_kind="planned_comment",
                        phase="pre_post",
                        issue_number=69,
                        url="https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68",
                    )
                ),
            )
            comment_claim_69 = write_tmp(
                tmp.as_posix(),
                "comment-claim-69.json",
                json.dumps(
                    snapshot_record(
                        body="safe body\n",
                        source_kind="issue_comment",
                        phase="post_refetch",
                        issue_number=69,
                        comment_id=123,
                        url="https://github.com/vamseeachanta/raw-to-knowledge-playbook/issues/68#issuecomment-123",
                    )
                ),
            )
            errors = (
                validator.validate_issue_comment_snapshot_file(planned_url_69)
                + validator.validate_issue_comment_snapshot_file(comment_url_69)
                + validator.validate_issue_comment_snapshot_file(planned_claim_69)
                + validator.validate_issue_comment_snapshot_file(comment_claim_69)
            )

        self.assertEqual(2, "\n".join(errors).count("snapshot-url"))
        self.assertEqual(4, "\n".join(errors).count("snapshot-issue"))


if __name__ == "__main__":
    unittest.main()
