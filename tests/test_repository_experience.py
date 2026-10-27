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

# Every public Markdown surface is audited, not just docs/ and root guides.
# Deliberately enumerate owned documentation directories; do not traverse
# downloaded fixtures, ignored scratch, virtualenvs or accepted research data.
PUBLIC_DOC_DIRS = (
    ".", ".github", ".github/knowledge", ".github/agent-handoff",
    "docs", "evidence", "bio_tool", "framework", "framework/docs",
    "checks/institutional", "checks/project",
)

class RepositoryExperienceTests(unittest.TestCase):
    def test_public_documentation_inventory_is_complete(self):
        expected = {
            path.relative_to(ROOT).as_posix()
            for directory in PUBLIC_DOC_DIRS
            for path in (ROOT / directory).glob("*.md")
            if path.is_file()
        }
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

    def test_first_use_commands_and_repository_component_identity_exist(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("ls-knowledge", readme)
        self.assertIn("ls-evidence", readme)
        self.assertIn("ls-bio", readme)
        self.assertIn("ls-framework", readme)
        self.assertIn("docs/GETTING_STARTED.md", readme)
        self.assertIn("CITATION.cff", readme)
        self.assertTrue((ROOT / ".github/workflows/life-science-knowledge.yml").is_file())
        self.assertTrue((ROOT / "evidence/inspection.py").is_file())
        self.assertTrue((ROOT / "bio_tool/cli.py").is_file())
        self.assertTrue((ROOT / "framework/src/ls_framework/cli.py").is_file())
        self.assertTrue((ROOT / "lifemonitor.yaml").is_file())
        self.assertFalse((ROOT / ".lifemonitor.yaml").exists())

    def test_changelog_has_single_unreleased_and_no_fabricated_release(self):
        value = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"(?im)^## Unreleased\b", value)), 1)
        self.assertIn("0.3.0", value)

    def test_exact_byte_inputs_have_cross_platform_checkout_policy(self):
        attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")
        self.assertIn("* text=auto eol=lf", attributes)
        self.assertIn("*.zip binary", attributes)
        self.assertIn("*.sqlite binary", attributes)

if __name__ == "__main__":
    unittest.main()
