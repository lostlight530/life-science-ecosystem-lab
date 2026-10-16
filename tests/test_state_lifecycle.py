import json
import hashlib
import tempfile
import unittest
from pathlib import Path

from evidence.aggregation import aggregate_evidence
from life_science_ecosystem_lab.lifecycle.guard import check_write_boundary, world_line_matches
from life_science_ecosystem_lab.lifecycle.orchestrator import apply_lifecycle
from life_science_ecosystem_lab.lifecycle.state import StateRoots, apply_candidate, verify_state


class StateLifecycleTests(unittest.TestCase):
    def candidate(self, text="first"):
        from evidence.normalization import sha256_bytes, canonical_text_bytes
        record = {
            "source_id": "source", "source_registry": "fixture-v1", "repository": "owner/repo", "ref": "main",
            "commit": "1" * 40, "tree_sha": "2" * 40, "blob_sha": "3" * 40,
            "path": "README.md", "text": text, "raw_size": len(text.encode()),
            "content_sha256": sha256_bytes(canonical_text_bytes(text)), "selection_rule": "test@1.0.0",
            "trust": "primary", "collector_version": "0.2.0",
        }
        return aggregate_evidence([record], {"topics": []})

    def test_apply_archives_previous_current_without_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            roots = StateRoots(Path(directory))
            first = self.candidate("first")
            second = self.candidate("second")
            apply_candidate(first, roots, logical_date="2026-10-16")
            apply_candidate(second, roots, logical_date="2026-10-17")
            archived = list((roots.archive / "2026" / "10").glob("*.json"))
            self.assertEqual(len(archived), 1)
            self.assertEqual(json.loads(archived[0].read_text(encoding="utf-8"))["output_digest"], first["output_digest"])
            self.assertTrue(verify_state(roots).valid)

    def test_archive_collision_with_different_bytes_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            roots = StateRoots(Path(directory))
            first = self.candidate("first")
            second = self.candidate("second")
            apply_candidate(first, roots, logical_date="2026-10-16")
            apply_candidate(second, roots, logical_date="2026-10-17")
            collision = roots.archive / "2026" / "10" / f"{second['run_id']}-{second['output_digest'][:12]}.json"
            collision.write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "archive collision"):
                apply_candidate(self.candidate("third"), roots, logical_date="2026-10-18")

    def test_boundary_and_world_line_guards(self):
        self.assertEqual(check_write_boundary(["data/state/current.json", "data/receipts/run.json"]), [])
        self.assertEqual(check_write_boundary(["README.md"]), ["README.md"])
        self.assertTrue(world_line_matches("a" * 40, "a" * 40))
        self.assertFalse(world_line_matches("a" * 40, "b" * 40))

    def test_lifecycle_applies_only_on_matching_world_line(self):
        with tempfile.TemporaryDirectory() as directory:
            roots = StateRoots(Path(directory))
            candidate = self.candidate("active")
            conflict = apply_lifecycle(candidate, roots, logical_date="2026-10-16", validated_head="1" * 40, current_head="2" * 40)
            self.assertEqual(conflict["outcome"], "CONFLICTED_WORLD_LINE_NO_APPLY")
            self.assertFalse(roots.current.exists())
            receipt = apply_lifecycle(candidate, roots, logical_date="2026-10-16", validated_head="1" * 40, current_head="1" * 40)
            self.assertEqual(receipt["outcome"], "APPLIED")
            self.assertTrue((roots.root / "data" / "knowledge" / "current.json").is_file())
            self.assertTrue((roots.root / "data" / "memories" / "current.json").is_file())
            self.assertTrue((roots.root / "data" / "receipts" / f"{candidate['run_id']}.json").is_file())


if __name__ == "__main__":
    unittest.main()
