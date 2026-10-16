import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WorkflowContractTests(unittest.TestCase):
    def test_cwl_executes_peer_tool_not_legacy_nested_command(self):
        for command in ("aggregate", "validate"):
            doc = (ROOT / ".github" / "knowledge" / "tools" / f"{command}.cwl").read_text(encoding="utf-8")
            self.assertIn("baseCommand: [python3, -m, evidence]", doc)
            self.assertNotIn("  - evidence\n", doc)

    def test_lifecycle_has_split_permissions_and_ordered_guards(self):
        text = (ROOT / ".github" / "workflows" / "life-science-knowledge.yml").read_text(encoding="utf-8")
        self.assertIn("validate:", text)
        self.assertIn("apply:", text)
        self.assertIn("needs: validate", text)
        self.assertIn("contents: read", text)
        self.assertIn("contents: write", text)
        self.assertIn("check_write_boundary.py", text)
        self.assertIn("verify_world_line.py", text)
        self.assertLess(text.index("evidence collect"), text.index("evidence aggregate"))
        self.assertLess(text.index("lifecycle apply"), text.index("Final validation"))
        uses = re.findall(r"uses:\s*[^@\s]+@([^\s#]+)", text)
        self.assertTrue(uses)
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{40}", value) for value in uses))

    def test_validation_workflow_checks_profiles_and_caches(self):
        text = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
        self.assertIn("validate-source-registry", text)
        self.assertIn("validate-topic-registry", text)
        self.assertIn("Generated cache files are not allowed", text)


if __name__ == "__main__":
    unittest.main()
