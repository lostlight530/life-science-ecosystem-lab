import unittest

from life_science_ecosystem_lab.workflow_profile import validate_workflow_profile


VALID = {
    "schema_version": "1.0.0",
    "repository": "lostlight530/life-science-ecosystem-lab",
    "source_commit": "1" * 40,
    "workflow_path": ".github/workflows/validate.yml",
    "workflow_sha256": "2" * 64,
    "maturity": "pilot",
    "registry_status": "not-connected",
    "monitoring_status": "not-connected",
}


class WorkflowProfileTests(unittest.TestCase):
    def test_valid_profile(self):
        self.assertEqual(validate_workflow_profile(VALID), [])

    def test_mutable_branch_is_not_a_commit(self):
        value = {**VALID, "source_commit": "main"}
        self.assertIn("source_commit must be a lowercase 40-character Git SHA", validate_workflow_profile(value))

    def test_parent_traversal_is_rejected(self):
        value = {**VALID, "workflow_path": "../workflow.yml"}
        self.assertIn("workflow_path must be a safe repository-relative POSIX path", validate_workflow_profile(value))


if __name__ == "__main__":
    unittest.main()

