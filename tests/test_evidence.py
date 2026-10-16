import json
import tempfile
import unittest
from pathlib import Path

from life_science_ecosystem_lab.evidence.aggregation import aggregate_evidence
from life_science_ecosystem_lab.evidence.models import GitTreeEntry, SourceIdentity
from life_science_ecosystem_lab.evidence.normalization import normalize_text_bytes
from life_science_ecosystem_lab.evidence.profiles import load_source_registry, load_topic_registry
from life_science_ecosystem_lab.evidence.selection import select_paths


class EvidenceTests(unittest.TestCase):
    def test_normalization_is_platform_independent(self):
        self.assertEqual(normalize_text_bytes(b"\xef\xbb\xbfCafe\xcc\x81\r\n"), "Caf\u00e9\n")

    def test_excludes_override_includes(self):
        profile = {
            "include": ["docs/**/*.md", "README.md"],
            "exclude": ["docs/archive/**"],
            "max_bytes": 1000,
        }
        entries = (
            GitTreeEntry("README.md", "a" * 40, 10),
            GitTreeEntry("docs/current/a.md", "b" * 40, 10),
            GitTreeEntry("docs/archive/a.md", "c" * 40, 10),
        )
        self.assertEqual([item.path for item in select_paths(entries, profile)], ["README.md", "docs/current/a.md"])

    def test_registry_rejects_unsafe_path(self):
        value = {
            "schema_version": "1.0.0",
            "registry_id": "test",
            "sources": [{
                "id": "bad",
                "repository": "owner/repo",
                "ref": "main",
                "approved": True,
                "required": True,
                "trust": "primary",
                "include": ["../secret"],
                "exclude": [],
                "max_bytes": 1000,
            }],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sources.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "safe repository-relative"):
                load_source_registry(path)

    def test_aggregation_is_deterministic_and_explainable(self):
        topics = {
            "schema_version": "1.0.0",
            "registry_id": "topics",
            "topics": [{
                "id": "workflow",
                "aliases": ["workflow", "pipeline"],
                "required_terms": ["research"],
                "excluded_terms": ["marketing"],
                "minimum_matches": 1,
            }],
        }
        records = [{
            "source_id": "s1",
            "repository": "owner/repo",
            "commit": "1" * 40,
            "path": "README.md",
            "blob_sha": "2" * 40,
            "content_sha256": "3" * 64,
            "text": "Research workflow pipeline",
        }]
        first = aggregate_evidence(records, topics, previous=None)
        second = aggregate_evidence(list(reversed(records)), topics, previous=None)
        self.assertEqual(first["output_digest"], second["output_digest"])
        self.assertEqual(first["changes"][0]["kind"], "unknown_baseline")
        self.assertEqual(first["topics"][0]["contributions"][0]["source_id"], "s1")

    def test_source_identity_is_stable(self):
        self.assertEqual(SourceIdentity("owner", "repo", "main").key, "owner/repo@main")

    def test_equal_content_at_new_path_is_classified_as_move(self):
        topics = {"topics": []}
        old = {
            "records": [{"source_id":"s1", "repository":"owner/repo", "path": "old.md", "content_sha256": "3" * 64}],
        }
        records = [{
            "source_id": "s1", "repository": "owner/repo", "commit": "1" * 40,
            "path": "new.md", "blob_sha": "2" * 40, "content_sha256": "3" * 64,
            "text": "same",
        }]
        bundle = aggregate_evidence(records, topics, previous=old)
        self.assertEqual(bundle["changes"], [{"source_id":"s1", "repository":"owner/repo", "from_path": "old.md", "path": "new.md", "kind": "moved"}])


if __name__ == "__main__":
    unittest.main()
