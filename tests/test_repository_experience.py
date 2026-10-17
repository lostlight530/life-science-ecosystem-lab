"""Public repository contracts from a first-time user's point of view.

Zero extra test dependencies: structural checks should work before any optional
CWL, remote GitHub collection or Agent integration is configured.
"""
import json
import re
import unittest
from pathlib import Path
from evidence.documentation import audit_documents

ROOT = Path(__file__).resolve().parents[1]

PUBLIC_DOCS = {
    "README.md", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md",
    ".github/README.md", ".github/knowledge/README.md", "evidence/README.md"
}

class RepositoryExperienceTests(unittest.TestCase):
    def test_public_documentation_inventory_is_complete(self):
        expected = PUBLIC_DOCS | {p.relative_to(ROOT).as_posix()
                                   for p in (ROOT / "docs").glob("*.md")}
        stored = json.loads((ROOT / "evidence/profiles/docs.json").read_text(encoding="utf-8"))
        self.assertEqual(stored["schema_version"], "1.0.0")
        self.assertEqual(stored["documents"], sorted(expected))
        report = audit_documents(ROOT, stored["documents"])
        self.assertEqual(report.issues, (), "\n".join(report.issues))

    def test_github_issue_forms_have_required_keys_and_safe_fields(self):
        forms = sorted((ROOT / ".github/ISSUE_TEMPLATE").glob("*.yml"))
        self.assertGreaterEqual(len(forms), 3)
        for form in forms:
            data = form.read_text(encoding="utf-8")
            with self.subTest(form=form.name):
                for key in ("name", "description", "body"):
                    self.assertRegex(data, rf"(?m)^{key}:\s*\S")
                self.assertNotRegex(data, r"(?m)^about:")
                self.assertRegex(data, r"(?m)^\s+- type: (input|textarea|markdown)")

    def test_first_use_commands_and_dual_identity_exist(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("ls-knowledge", readme)
        self.assertIn("ls-evidence", readme)
        self.assertIn("docs/GETTING_STARTED.md", readme)
        self.assertIn("CITATION.cff", readme)
        self.assertTrue((ROOT / ".github/workflows/life-science-knowledge.yml").is_file())
        self.assertTrue((ROOT / "evidence/inspection.py").is_file())
        self.assertFalse((ROOT / "lifemonitor.yaml").exists())

    def test_changelog_has_single_unreleased_and_no_fabricated_release(self):
        value = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"(?im)^## Unreleased\b", value)), 1)
        self.assertIn("0.3.0", value)

if __name__ == "__main__":
    unittest.main()
