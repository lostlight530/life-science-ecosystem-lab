import base64
import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from life_science_ecosystem_lab.cli import main
from evidence.cli import main as evidence_main
from evidence.collector import collect_sources
from evidence.profiles import SourceRegistry


class FixtureTransport:
    def get_repository(self, identity):
        return {"default_branch": "main"}

    def get_commit(self, identity, ref):
        return {"sha": "1" * 40, "commit": {"tree": {"sha": "2" * 40}}}

    def get_tree(self, identity, tree_sha):
        return {
            "truncated": False,
            "tree": [
                {"path": "README.md", "type": "blob", "sha": "3" * 40, "size": 32},
                {"path": "archive/old.md", "type": "blob", "sha": "4" * 40, "size": 32},
            ],
        }

    def get_blob(self, identity, blob_sha):
        return b"Research workflow evidence\r\n"


class CollectorCliTests(unittest.TestCase):
    def registry(self):
        return SourceRegistry("1.0.0", "fixture", ({
            "id": "s1",
            "repository": "owner/repo",
            "ref": "main",
            "approved": True,
            "required": True,
            "trust": "primary",
            "include": ["README.md", "archive/**"],
            "exclude": ["archive/**"],
            "max_bytes": 1000,
        },))

    def test_collects_selected_blob_with_provenance(self):
        result = collect_sources(self.registry(), FixtureTransport(), retrieved_at="2026-10-16T00:00:00Z")
        self.assertEqual(len(result.records), 1)
        record = result.records[0]
        self.assertEqual(record["repository"], "owner/repo")
        self.assertEqual(record["commit"], "1" * 40)
        self.assertEqual(record["path"], "README.md")
        self.assertEqual(record["retrieved_at"], "2026-10-16T00:00:00Z")

    def test_truncated_tree_is_not_silently_accepted(self):
        class Truncated(FixtureTransport):
            def get_tree(self, identity, tree_sha):
                return {"truncated": True, "tree": []}

        with self.assertRaisesRegex(ValueError, "TREE_TRUNCATED"):
            collect_sources(self.registry(), Truncated(), retrieved_at="2026-10-16T00:00:00Z")

    def test_cli_validates_source_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sources.json"
            path.write_text(json.dumps({
                "schema_version": "1.0.0",
                "registry_id": "fixture",
                "sources": list(self.registry().sources),
            }), encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output), redirect_stderr(output):
                code = main(["validate-source-registry", str(path)])
            self.assertEqual(code, 0)
            self.assertIn("source registry is valid", output.getvalue())

    def test_cli_aggregates_only_to_requested_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records = root / "records.json"
            topics = root / "topics.json"
            output_path = root / "out" / "candidate.json"
            records.write_text((Path(__file__).resolve().parents[1] / "evidence/examples/evidence-records.json").read_text(encoding="utf-8"), encoding="utf-8")
            topics.write_text(json.dumps({
                "schema_version": "1.0.0", "registry_id": "topics",
                "topics": [{"id": "workflow", "aliases": ["workflow"], "required_terms": ["research"], "excluded_terms": [], "minimum_matches": 1}],
            }), encoding="utf-8")
            code = evidence_main(["aggregate", "--input", str(records), "--topics", str(topics), "--output", str(output_path)])
            self.assertEqual(code, 0)
            self.assertTrue(output_path.is_file())
            self.assertEqual(evidence_main(["validate", "--bundle", str(output_path)]), 0)

    def test_cli_applies_lifecycle_with_explicit_world_line(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            from evidence.aggregation import aggregate_evidence
            candidate = aggregate_evidence([], {"topics": []})
            path = root / "candidate.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            code = main([
                "lifecycle", "apply", "--candidate", str(path), "--repository-root", str(root),
                "--logical-date", "2026-10-16", "--validated-head", "1" * 40, "--current-head", "1" * 40, "--execution-id", "fixture-cli-1",
            ])
            self.assertEqual(code, 0)
            self.assertTrue((root / "data" / "receipts" / "fixture-cli-1.json").is_file())


if __name__ == "__main__":
    unittest.main()
