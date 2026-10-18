"""Portable CWL package must be deterministic, bounded and production-data free."""
import json
import runpy
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PortableCrateTests(unittest.TestCase):
    def test_two_portable_archives_match_and_have_cwl_main(self):
        script = runpy.run_path(str(ROOT / ".github/scripts/build_portable_workflow_crate.py"))
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a.crate.zip", Path(tmp) / "b.crate.zip"
            script["build"](a)
            script["build"](b)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            with zipfile.ZipFile(a) as crate:
                names = set(crate.namelist())
                self.assertIn("pyproject.toml", names)
                self.assertIn(".github/knowledge/main.cwl", names)
                self.assertIn("README.md", names)
                self.assertFalse(any(name.startswith("data/") or name.startswith(".agent-work/") for name in names))
                body = json.loads(crate.read("ro-crate-metadata.json"))
                nodes = {n["@id"]: n for n in body["@graph"] if isinstance(n, dict) and "@id" in n}
                self.assertEqual(nodes["./"]["name"], "Life Science Knowledge Workflow")
                self.assertEqual(nodes["./"]["version"], "0.4.0")
                self.assertEqual(nodes["./"]["author"]["@id"], "#creator")
                self.assertIn("portable CWL v1.2 workflow", nodes["./"]["description"])
                self.assertIn("no live collection", nodes["./"]["description"])
                self.assertEqual(nodes["./"]["mainEntity"]["@id"], ".github/knowledge/main.cwl")
                self.assertEqual(nodes["#suite"]["mainEntity"]["@id"], ".github/knowledge/main.cwl")
                self.assertEqual(nodes[".github/knowledge/main.cwl"]["version"], "0.4.0")
                self.assertEqual(nodes[".github/knowledge/main.cwl"]["programmingLanguage"]["@id"],
                                 "https://w3id.org/workflowhub/workflow-ro-crate#cwl")
                self.assertEqual(nodes["#gh-test"]["name"], "GitHub Actions integration validation")
                self.assertEqual(nodes["#gh-test"]["url"], "https://api.github.com")
                self.assertEqual(
                    nodes["#gh-test"]["runsOn"]["@id"],
                    "https://w3id.org/ro/terms/test#GithubService",
                )
                github_service = nodes["https://w3id.org/ro/terms/test#GithubService"]
                self.assertEqual(github_service["@type"], "TestService")
                self.assertEqual(github_service["name"], "Github Actions")
                self.assertEqual(github_service["url"]["@id"], "https://github.com")
                self.assertTrue({v["@id"] for v in nodes["./"]["hasPart"]}.issubset(names))


if __name__ == "__main__":
    unittest.main()
