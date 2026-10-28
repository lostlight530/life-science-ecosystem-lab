"""Public repository contracts from a first-time user's point of view.

Zero extra test dependencies: structural checks should work before any optional
CWL, remote GitHub collection or Agent integration is configured.
"""
import json
import re
import tomllib
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

    def test_public_evidence_guide_keeps_peer_proofs_and_refusal_guard_distinct(self):
        guide = (ROOT / "docs/VERIFYING_RESULTS.md").read_text(encoding="utf-8")
        self.assertIn("## Six independent evidence surfaces", guide)
        for expected in (
            "| Local Tool inspection |",
            "| Evidence collection/aggregation |",
            "| Computational knowledge replay |",
            "| Bio Tool data audit |",
            "| Independent Framework assessment |",
            "| GitHub native durable lifecycle |",
        ):
            with self.subTest(surface=expected):
                self.assertIn(expected, guide)
        self.assertIn("python -m ls_framework.challenge", guide)
        self.assertIn("including when launched from a checkout subdirectory", guide)
        self.assertNotIn("when launched from checkout root", guide)
        standards = (ROOT / "docs/STANDARDS.md").read_text(encoding="utf-8")
        self.assertIn("Workflow Run RO-Crate 0.6 is not Workflow Testing RO-Crate 0.2", standards)
        self.assertIn("https://bioschemas.org/terms/", standards)
        provenance = (ROOT / "docs/PROVENANCE.md").read_text(encoding="utf-8")
        for asset in ("Knowledge Workflow", "Evidence Tool", "Bio Tool", "Experimental Framework", "External Agent"):
            self.assertIn(asset, provenance)

    def test_first_use_package_count_and_frozen_release_boundary(self):
        root_package = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        framework_package = tomllib.loads(
            (ROOT / "framework/pyproject.toml").read_text(encoding="utf-8")
        )
        self.assertEqual(
            set(root_package["project"]["scripts"]),
            {"ls-knowledge", "ls-evidence", "ls-bio"},
        )
        self.assertEqual(
            set(framework_package["project"]["scripts"]), {"ls-framework"}
        )
        self.assertNotEqual(
            root_package["project"]["name"], framework_package["project"]["name"]
        )
        guide = (ROOT / "docs/GETTING_STARTED.md").read_text(encoding="utf-8")
        self.assertIn("three independent commands", guide)
        self.assertIn("separate Python distribution", guide)
        self.assertNotIn("not two separately published PyPI packages", guide)

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
