"""Offline invariants of two independent daily research self-check planes."""
from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from evidence.daily_selfcheck import (
    OFFICIAL, institutional_report, load_object, project_report,
    validate_official, validate_project_manifest, write_report,
)

ROOT = Path(__file__).resolve().parents[1]


class DailySelfcheckTests(unittest.TestCase):
    def setUp(self):
        self.institutional, self.institutional_sha = load_object(
            ROOT / "checks/institutional/defaults.json"
        )
        self.project, self.project_sha = load_object(ROOT / "checks/project/manifest.json")

    def test_our_public_official_reference_list_is_fixed_and_unique(self):
        rows = validate_official(self.institutional)
        self.assertEqual({item["id"] for item in rows}, set(OFFICIAL))
        self.assertEqual(len(rows), 6)
        for row in rows:
            self.assertTrue(row["public_probe_url"].startswith("https://"))

    def test_upstream_endpoint_redirection_and_single_run_can_never_prove_registration(self):
        report = institutional_report(self.institutional, self.institutional_sha,
            live=True, probe=lambda _: {"result": "HTTP_REDIRECT", "http_status": 302})
        self.assertEqual(report["mode"], "PUBLIC_HTTP_READ_ONLY")
        self.assertEqual({x["observation"]["http_status"] for x in report["checks"]}, {302})
        self.assertTrue(any("registration" in item for item in report["non_claims"]))
        self.assertNotIn("status", report)  # No fictitious official health verdict.

    def test_network_failures_are_inconclusive_not_official_outages(self):
        report = institutional_report(self.institutional, self.institutional_sha,
            live=True, probe=lambda _: {"result": "INCONCLUSIVE_NETWORK", "error_type": "TimeoutError"})
        self.assertEqual(report["inconclusive_count"], 6)
        self.assertNotIn("FAIL", json.dumps(report))
        self.assertEqual(institutional_report(self.institutional, self.institutional_sha)["mode"],
                         "OFFLINE_CONTRACT_ONLY")

    def test_unreviewed_official_endpoint_or_extra_service_fails_closed(self):
        bad = copy.deepcopy(self.institutional)
        bad["services"][0]["public_probe_url"] = "https://evil.example/"
        with self.assertRaisesRegex(ValueError, "URL mismatch"):
            validate_official(bad)
        bad = copy.deepcopy(self.institutional)
        bad["services"].append(copy.deepcopy(bad["services"][0]))
        with self.assertRaises(ValueError):
            validate_official(bad)

    def test_project_owns_file_inventory_not_institutional_defaults(self):
        paths = validate_project_manifest(self.project)
        self.assertIn("bio_tool/cli.py", paths)
        self.assertIn(".github/workflows/life-science-knowledge.yml", paths)
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

    def test_missing_file_and_bad_cli_are_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = {
                "schema_version": "1.0.0", "scope": "PROJECT_CUSTOM_CONTRACT",
                "required_commands": ["ls-knowledge", "ls-evidence", "ls-bio"],
                "required_files": [".lifemonitor.yaml", "pyproject.toml"] +
                                  ["docs/file_" + str(i) + ".md" for i in range(10)],
            }
            (root / ".lifemonitor.yaml").write_text("issues:\n  check: true\n")
            (root / "pyproject.toml").write_text(
                '[project.scripts]\nls-knowledge = "k:x"\nls-evidence = "e:y"\nls-bio = "b:z"\n')
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


if __name__ == "__main__":
    unittest.main()
