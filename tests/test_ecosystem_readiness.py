"""External readiness evidence is explicitly distinct from service acceptance."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from evidence.interoperability import audit_ecosystem

ROOT = Path(__file__).resolve().parents[1]


class EcosystemReadinessTests(unittest.TestCase):
    def test_current_repository_reports_requirements_and_unknown_external_states(self):
        report = audit_ecosystem(ROOT)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")
        self.assertEqual(report["external_states"]["WorkflowHub"], "NOT_VERIFIED")
        self.assertEqual(report["external_states"]["LifeMonitor"], "NOT_VERIFIED")
        self.assertEqual(report["external_states"]["bio.tools"], "NOT_VERIFIED")
        self.assertEqual(report["readiness"]["bio.tools"], "DOMAIN_SCOPE_AND_EDAM_CURATION_REQUIRED")
        self.assertTrue(any(x["code"] == "MAIN_WORKFLOW_PORTABILITY_NOT_VERIFIED" for x in report["findings"]))
        self.assertEqual(report, audit_ecosystem(ROOT))

    def test_missing_local_files_do_not_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = audit_ecosystem(Path(tmp))
            self.assertEqual(report["status"], "REVIEW_REQUIRED")
            self.assertTrue(any(x["platform"] == "LifeMonitor" for x in report["findings"]))
            self.assertEqual(report["external_states"]["third_party_usage"], "NOT_MEASURED")

    def test_symlink_metadata_not_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ro-crate-metadata.json").symlink_to(ROOT / "ro-crate-metadata.json")
            report = audit_ecosystem(root)
            self.assertIn("MAIN_WORKFLOW_PORTABILITY_NOT_VERIFIED", {x["code"] for x in report["findings"]})


if __name__ == "__main__":
    unittest.main()
