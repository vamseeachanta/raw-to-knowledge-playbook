"""Repository flow permits identifiers; independent security checks remain."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ace_public_output_contract as output


class IdentifierGateRetirementTests(unittest.TestCase):
    def test_client_customer_project_identifiers_flow_through_body(self):
        for kind in ("client", "customer", "project"):
            with self.subTest(kind=kind):
                body = kind + "_id = SYNTHETIC-12345\n"
                self.assertEqual([], output.validate_public_output_body_text("report.md", body))

    def test_personal_and_path_mentions_flow(self):
        body = "contact: person" + "@example.com\n" + "/mnt" + "/ace/source.csv\n"
        self.assertEqual([], output.validate_public_output_body_text("report.md", body))

    def test_secret_assignment_still_blocks(self):
        body = "pass" + "word = synthetic-secret-value"
        errors = output.validate_public_output_body_text("report.md", body)
        self.assertIn("secret-assignment", "\n".join(errors))
        self.assertNotIn("synthetic-secret-value", "\n".join(errors))

    def test_unbounded_traversal_still_blocks(self):
        body = "find " + "$ACE_" + "SHARE_ROOT -type f"
        errors = output.validate_public_output_body_text("report.md", body)
        self.assertIn("unbounded-traversal-command", "\n".join(errors))

    def test_runtime_and_ci_no_longer_call_retired_scanner(self):
        for path in (ROOT / ".github/workflows/validate.yml",
                     ROOT / "scripts/ace_public_output_contract.py"):
            with self.subTest(path=path):
                text = path.read_text()
                self.assertNotIn("legal" + "_sanity_scan", text)
                self.assertNotIn("legal" + "-sanity-scan.sh", text)

    def test_retained_safety_scanner_is_explicit_in_ci(self):
        workflow = (ROOT / ".github/workflows/validate.yml").read_text()
        self.assertIn("scripts/security/public_surface_safety_scan.py", workflow)


if __name__ == "__main__":
    unittest.main()
