"""Tests for this repository's custom self-check contract only."""
from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from evidence.daily_selfcheck import (
    institutional_report, load_object, project_report, validate_lifemonitor_config,
    validate_project_manifest, write_report,
)

ROOT = Path(__file__).resolve().parents[1]


class ProjectSelfcheckTests(unittest.TestCase):
    def setUp(self):
        self.institutional, self.institutional_sha = load_object(
            ROOT / "checks/institutional/defaults.json"
        )
        self.project, self.project_sha = load_object(ROOT / "checks/project/manifest.json")

    def test_project_owns_file_inventory_not_institutional_defaults(self):
        paths = validate_project_manifest(self.project)
        self.assertIn("bio_tool/cli.py", paths)
        self.assertIn(".github/workflows/life-science-knowledge.yml", paths)
        self.assertIn("lifemonitor.yaml", paths)
        self.assertNotIn(".lifemonitor.yaml", paths)
        self.assertNotIn("checks/institutional/defaults.json", paths)
        bad = copy.deepcopy(self.project)
        bad["required_files"].append("checks/institutional/defaults.json")
        with self.assertRaisesRegex(ValueError, "impersonate upstream"):
            validate_project_manifest(bad)
        bad = copy.deepcopy(self.project)
        bad["required_files"][1] = "../secret"
        with self.assertRaises(ValueError):
            validate_project_manifest(bad)

    def test_current_project_files_and_three_commands_are_present(self):
        report = project_report(ROOT, self.project, self.project_sha)
        self.assertEqual(report["status"], "PASS", report["errors"])
        self.assertEqual(len(report["checks"]), len(self.project["required_files"]))
        self.assertNotIn("institutional", json.dumps(report["checks"]))

    def test_lifemonitor_config_uses_official_path_and_preserves_global_policy(self):
        config = ROOT / "lifemonitor.yaml"
        self.assertTrue(config.is_file())
        self.assertFalse((ROOT / ".lifemonitor.yaml").exists())
        self.assertEqual(validate_lifemonitor_config(ROOT), [])
        content = config.read_text(encoding="utf-8")
        self.assertRegex(content, r"(?m)^name:[ \t]*\S")
        self.assertRegex(content, r"(?m)^issues:[ \t]*\n[ \t]+check:[ \t]*true[ \t]*(?:#.*)?$")
        self.assertNotRegex(content, r"(?m)^(?:push|public)[ \t]*:")

    def test_lifemonitor_config_rejects_global_policy_overrides(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "lifemonitor.yaml"
            path.write_text('name: "Fixture"\nissues:\n  check: true\n', encoding="utf-8")
            self.assertEqual(validate_lifemonitor_config(root), [])
            path.write_text(
                'name: "Fixture"\nissues:\n  check: true\npush:\n  branches: []\n',
                encoding="utf-8",
            )
            self.assertIn("LIFEMONITOR_GLOBAL_SETTINGS_OVERRIDE", validate_lifemonitor_config(root))
            path.write_text(
                'name: "Fixture"\nissues:\n  check: true\npublic: true\n',
                encoding="utf-8",
            )
            self.assertIn("LIFEMONITOR_GLOBAL_SETTINGS_OVERRIDE", validate_lifemonitor_config(root))

    def test_missing_file_and_bad_cli_are_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = {
                "schema_version": "1.0.0", "scope": "PROJECT_CUSTOM_CONTRACT",
                "required_commands": ["ls-knowledge", "ls-evidence", "ls-bio"],
                "required_files": ["lifemonitor.yaml", "pyproject.toml"] +
                                  ["docs/file_" + str(i) + ".md" for i in range(10)],
            }
            (root / "lifemonitor.yaml").write_text(
                'name: "Fixture"\nissues:\n  check: true\n', encoding="utf-8"
            )
            (root / "pyproject.toml").write_text(
                '[project.scripts]\nls-knowledge = "k:x"\nls-evidence = "e:y"\nls-bio = "b:z"\n'
            )
            (root / "docs").mkdir()
            for i in range(10):
                (root / "docs" / f"file_{i}.md").write_text("fixture")
            valid = project_report(root, manifest, hashlib.sha256(b"manifest").hexdigest())
            self.assertEqual(valid["status"], "PASS", valid["errors"])
            (root / "docs/file_0.md").unlink()
            failing = project_report(root, manifest, hashlib.sha256(b"manifest").hexdigest())
            self.assertEqual(failing["status"], "FAIL")
            self.assertTrue(any("MISSING_OR_UNSAFE_FILE" in x for x in failing["errors"]))

    def test_derived_reports_are_serializable_in_separate_locations(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "institutional-defaults" / "report.json"
            second = Path(tmp) / "project-custom" / "report.json"
            write_report(first, institutional_report(self.institutional, self.institutional_sha))
            write_report(second, project_report(ROOT, self.project, self.project_sha))
            self.assertNotEqual(json.loads(first.read_text())["kind"],
                                json.loads(second.read_text())["kind"])
            self.assertNotIn("official_documentation_url", second.read_text())

    def test_custom_manifest_refuses_fourth_asset_or_silent_scope_expansion(self):
        altered = copy.deepcopy(self.project)
        altered["required_commands"].append("ls-agent")
        with self.assertRaisesRegex(ValueError, "three independently callable"):
            validate_project_manifest(altered)
        altered = copy.deepcopy(self.project)
        altered["required_files"].append("/etc/passwd")
        with self.assertRaises(ValueError):
            validate_project_manifest(altered)


if __name__ == "__main__":
    unittest.main()
