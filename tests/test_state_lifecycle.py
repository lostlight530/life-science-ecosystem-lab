import json
import hashlib
import tempfile
import unittest
from pathlib import Path

from evidence.aggregation import aggregate_evidence
from life_science_ecosystem_lab.lifecycle.guard import check_write_boundary, world_line_matches
from life_science_ecosystem_lab.lifecycle.orchestrator import apply_lifecycle
from life_science_ecosystem_lab.lifecycle.state import StateRoots, apply_candidate, verify_state
from life_science_ecosystem_lab.knowledge import build_knowledge
from life_science_ecosystem_lab.graph import verify_graph_events


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
            self.assertTrue((roots.root / "data" / "receipts" / f"{receipt['execution_id']}.json").is_file())


    def test_a_b_a_replay_preserves_independent_receipts_and_events(self):
        with tempfile.TemporaryDirectory() as directory:
            roots = StateRoots(Path(directory))
            registry = {"topics": []}
            a, b = self.candidate("original"), self.candidate("updated")
            for value, execution in ((a, "gh-120-1"), (b, "gh-121-1"), (a, "gh-122-1")):
                receipt = apply_lifecycle(value, roots, logical_date="2026-10-17",
                    validated_head="1" * 40, current_head="1" * 40,
                    knowledge=build_knowledge(value, registry), topic_registry=registry,
                    execution_id=execution)
                self.assertEqual(receipt["outcome"], "APPLIED")
                self.assertEqual(receipt["snapshot_id"], value["run_id"])
                self.assertEqual(receipt["execution_id"], execution)
            self.assertTrue(verify_state(roots, require_accepted=True).valid)
            self.assertEqual(verify_graph_events(roots.root / "data" / "knowledge"), 3)
            self.assertEqual(len(list((roots.root / "data" / "receipts").glob("*.json"))), 3)
            self.assertEqual(json.loads((roots.root / "data" / "receipts" / "gh-120-1.json").read_text())["snapshot_id"], a["run_id"])
            self.assertEqual(json.loads((roots.root / "data" / "receipts" / "gh-122-1.json").read_text())["snapshot_id"], a["run_id"])
            outcome = apply_lifecycle(a, roots, logical_date="2026-10-17",
                validated_head="1" * 40, current_head="1" * 40,
                knowledge=build_knowledge(a, registry), topic_registry=registry,
                execution_id="gh-123-1")["outcome"]
            self.assertEqual(outcome, "NO_MEANINGFUL_DELTA")
            self.assertFalse((roots.root / "data" / "receipts" / "gh-123-1.json").exists())

    def test_source_revision_is_not_document_text_change(self):
        with tempfile.TemporaryDirectory() as directory:
            roots = StateRoots(Path(directory))
            a = self.candidate("same text")
            changed = [dict(r, commit="9" * 40, tree_sha="8" * 40) for r in a["records"]]
            b = aggregate_evidence(changed, {"topics": []})
            first = apply_lifecycle(a, roots, logical_date="2026-10-17",
                validated_head="1" * 40, current_head="1" * 40, execution_id="revision-a")
            second = apply_lifecycle(b, roots, logical_date="2026-10-17",
                validated_head="1" * 40, current_head="1" * 40, execution_id="revision-b")
            self.assertEqual(first["change_kind"], "INITIAL_SNAPSHOT")
            self.assertEqual(second["change_kind"], "DOCUMENT_TEXT_UNCHANGED")
            self.assertNotEqual(a["input_digest"], b["input_digest"])

    def test_execution_id_path_safety_and_no_receipt_reuse(self):
        with tempfile.TemporaryDirectory() as directory:
            roots = StateRoots(Path(directory))
            a = self.candidate("a")
            with self.assertRaisesRegex(ValueError, "execution_id"):
                apply_lifecycle(a, roots, logical_date="2026-10-17",
                    validated_head="1" * 40, current_head="1" * 40, execution_id="../bad")
            apply_lifecycle(a, roots, logical_date="2026-10-17",
                validated_head="1" * 40, current_head="1" * 40, execution_id="gh-reuse")
            b = self.candidate("b")
            with self.assertRaisesRegex(ValueError, "already has an accepted receipt"):
                apply_lifecycle(b, roots, logical_date="2026-10-17",
                    validated_head="1" * 40, current_head="1" * 40, execution_id="gh-reuse")
            self.assertEqual(json.loads(roots.current.read_text())["run_id"], a["run_id"])

    def test_strict_state_check_rejects_empty_bootstrap(self):
        with tempfile.TemporaryDirectory() as directory:
            roots = StateRoots(Path(directory))
            self.assertTrue(verify_state(roots).valid)
            self.assertFalse(verify_state(roots, require_accepted=True).valid)

if __name__ == "__main__":
    unittest.main()
