from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_manifest_freshness.py"
EXPECTED_MANIFEST_KEYS = [
    "INDEX.md",
    "assets.json",
    "docs/master-index.jsonl",
    "_cad-index/index-summary.json",
    "_cad-index/cad-readability-index.tsv",
    ".ace-knowledge/index.db",
]


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_ace_manifest_freshness", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def populate_share_root(share_root: Path) -> None:
    for key in EXPECTED_MANIFEST_KEYS:
        path = share_root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("synthetic\n")


class AceManifestFreshnessRuntimeTests(unittest.TestCase):
    def test_builds_runtime_operational_evidence_from_share_root(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            share_root = Path(tmp)
            populate_share_root(share_root)
            record = validator.build_operational_evidence_record(
                share_root,
                "tests/fixtures/ace-manifest-freshness/generated-runtime-evidence.json",
                reviewed_commit="82497120488a9a10036b30c676637966ec300c27",
                record_id="ace62-runtime-fixture",
            )

        self.assertEqual([], validator.validate_operational_evidence(record))
        self.assertEqual(set(EXPECTED_MANIFEST_KEYS), set(record["snapshot_ids_by_manifest_source"]))
        self.assertEqual("sampling_allowed", record["authorization_status"])
        self.assertEqual(
            [
                "uv",
                "run",
                "python",
                "scripts/validate_ace_manifest_freshness.py",
                "--evidence",
                "tests/fixtures/ace-manifest-freshness/generated-runtime-evidence.json",
            ],
            record["validator_command"],
        )

    def test_mismatched_runtime_counts_block_sampling(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            share_root = Path(tmp)
            populate_share_root(share_root)
            (share_root / "assets.json").write_text("[{\"name\":\"a\"}, {\"name\":\"b\"}]\n")
            (share_root / "docs" / "master-index.jsonl").write_text("{\"id\":1}\n")
            record = validator.build_operational_evidence_record(
                share_root,
                "tests/fixtures/ace-manifest-freshness/generated-runtime-evidence.json",
                reviewed_commit="82497120488a9a10036b30c676637966ec300c27",
                record_id="ace62-runtime-fixture",
            )

        pair = record["drift_verdicts_by_manifest_source_pair"]["assets_to_master_records"]
        self.assertEqual("warning", pair["drift_severity"])
        self.assertEqual("blocked_requires_reconciliation", record["authorization_status"])
        self.assertIn("reconciliation_refs", "\n".join(validator.validate_operational_evidence(record)))

    def test_cli_can_emit_runtime_operational_evidence(self):
        validator = load_validator()
        output_ref = "tests/fixtures/ace-manifest-freshness/runtime-emitted-evidence.json"
        output_path = REPO_ROOT / output_ref
        if output_path.exists():
            output_path.unlink()
        self.addCleanup(lambda: output_path.exists() and output_path.unlink())
        with tempfile.TemporaryDirectory() as tmp:
            share_root = Path(tmp)
            populate_share_root(share_root)
            rc = validator.main(
                [
                    "--emit-evidence",
                    output_ref,
                    "--share-root",
                    str(share_root),
                    "--reviewed-commit",
                    "82497120488a9a10036b30c676637966ec300c27",
                ]
            )

        self.assertEqual(0, rc)
        self.assertEqual([], validator.validate_operational_evidence(json.loads(output_path.read_text())))
        emitted = json.loads(output_path.read_text())
        replay_rc = validator.main([*emitted["validator_command"][4:]])
        self.assertEqual(0, replay_rc)

    def test_emit_rejects_symlink_output_escape(self):
        validator = load_validator()
        output_ref = "tests/fixtures/ace-manifest-freshness/link-output.json"
        output_path = REPO_ROOT / output_ref
        if output_path.exists() or output_path.is_symlink():
            output_path.unlink()
        self.addCleanup(lambda: (output_path.exists() or output_path.is_symlink()) and output_path.unlink())
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "outside.json"
            outside.write_text("{}\n")
            output_path.symlink_to(outside)
            share_root = Path(tmp) / "share"
            populate_share_root(share_root)
            errors = "\n".join(
                validator.emit_operational_evidence(
                    share_root,
                    output_ref,
                    reviewed_commit="82497120488a9a10036b30c676637966ec300c27",
                )
            )

        self.assertIn("evidence_artifact_ref", errors)

    def test_cli_can_emit_to_primary_artifact_root(self):
        validator = load_validator()
        output_ref = "artifacts/ace-manifest-freshness/runtime-emitted-evidence.json"
        output_path = REPO_ROOT / output_ref
        if output_path.exists():
            output_path.unlink()
        self.addCleanup(lambda: output_path.exists() and output_path.unlink())
        with tempfile.TemporaryDirectory() as tmp:
            share_root = Path(tmp)
            populate_share_root(share_root)
            rc = validator.main(
                [
                    "--emit-evidence",
                    output_ref,
                    "--share-root",
                    str(share_root),
                    "--reviewed-commit",
                    "82497120488a9a10036b30c676637966ec300c27",
                ]
            )

        self.assertEqual(0, rc)
        self.assertEqual([], validator.validate_operational_evidence_file(Path(output_ref)))


if __name__ == "__main__":
    unittest.main()
