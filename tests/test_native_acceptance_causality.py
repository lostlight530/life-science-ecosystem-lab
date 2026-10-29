"""Characterization of native accepted-state causality; synthetic temporary roots only.

These tests assert the current software predicate, not a policy endorsement that
all metadata-only transitions should count as new research knowledge.
"""
import json
import tempfile
import unittest
from pathlib import Path

from evidence.aggregation import aggregate_evidence
from evidence.normalization import canonical_text_bytes, sha256_bytes
from life_science_ecosystem_lab.graph import verify_graph_events
from life_science_ecosystem_lab.knowledge import build_knowledge
from life_science_ecosystem_lab.lifecycle.orchestrator import apply_lifecycle
from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state


TOPICS = {"topics": []}
HEAD = "1" * 40


def record(*, commit="a" * 40):
    text = "same selected source document\n"
    return {
        "source_id": "example",
        "source_registry": "fixture-v1",
        "repository": "owner/repo",
        "ref": "main",
        "commit": commit,
        "tree_sha": "2" * 40,
        "blob_sha": "3" * 40,
        "path": "README.md",
        "text": text,
        "raw_size": len(text.encode("utf-8")),
        "content_sha256": sha256_bytes(canonical_text_bytes(text)),
        "selection_rule": "test@1.0.0",
        "trust": "primary",
        "collector_version": "0.2.0",
    }


def apply(candidate, roots, execution):
    return apply_lifecycle(
        candidate,
        roots,
        logical_date="2026-10-30",
        validated_head=HEAD,
        current_head=HEAD,
        knowledge=build_knowledge(candidate, TOPICS),
        topic_registry=TOPICS,
        execution_id=execution,
    )


class NativeAcceptanceCausalityTests(unittest.TestCase):
    def test_first_baseline_reclassification_then_true_stable_no_delta(self):
        initial = aggregate_evidence([record()], TOPICS)
        classified = aggregate_evidence([record()], TOPICS, previous=initial)
        stable = aggregate_evidence([record()], TOPICS, previous=classified)
        self.assertEqual(initial["changes"][0]["kind"], "unknown_baseline")
        self.assertEqual(classified["changes"][0]["kind"], "unchanged")
        self.assertEqual(stable["changes"][0]["kind"], "unchanged")
        self.assertEqual(initial["input_digest"], classified["input_digest"])
        self.assertEqual(initial["profile_digest"], classified["profile_digest"])
        self.assertNotEqual(initial["output_digest"], classified["output_digest"])
        self.assertNotEqual(build_knowledge(initial, TOPICS),
                            build_knowledge(classified, TOPICS))
        self.assertEqual(classified, stable)

        with tempfile.TemporaryDirectory() as directory:
            roots = StateRoots(Path(directory))
            first = apply(initial, roots, "synthetic-baseline")
            second = apply(classified, roots, "synthetic-classification")
            self.assertEqual(first["outcome"], "APPLIED")
            self.assertEqual(second["outcome"], "APPLIED")
            self.assertEqual(second["change_kind"], "DOCUMENT_TEXT_UNCHANGED")
            before = roots.current.read_bytes()
            third = apply(stable, roots, "synthetic-true-repeat")
            self.assertEqual(third["outcome"], "NO_MEANINGFUL_DELTA")
            self.assertEqual(roots.current.read_bytes(), before)
            self.assertFalse((roots.root / "data/receipts/synthetic-true-repeat.json").exists())
            self.assertEqual(verify_graph_events(roots.root / "data/knowledge"), 2)
            self.assertEqual(len(list((roots.root / "data/receipts").glob("*.json"))), 2)
            self.assertTrue(verify_state(roots, require_accepted=True).valid)

    def test_revision_only_is_an_accept_but_identical_next_repeat_is_not(self):
        initial = aggregate_evidence([record(commit="a" * 40)], TOPICS)
        revised = aggregate_evidence([record(commit="b" * 40)], TOPICS,
                                     previous=initial)
        repeated = aggregate_evidence([record(commit="b" * 40)], TOPICS,
                                      previous=revised)
        self.assertEqual(initial["records"][0]["content_sha256"],
                         revised["records"][0]["content_sha256"])
        self.assertEqual(revised["changes"][0]["kind"], "unchanged")
        self.assertNotEqual(initial["input_digest"], revised["input_digest"])
        self.assertEqual(revised, repeated)

        with tempfile.TemporaryDirectory() as directory:
            roots = StateRoots(Path(directory))
            self.assertEqual(apply(initial, roots, "revision-baseline")["outcome"], "APPLIED")
            accepted = apply(revised, roots, "revision-transition")
            self.assertEqual(accepted["outcome"], "APPLIED")
            self.assertEqual(accepted["change_kind"], "DOCUMENT_TEXT_UNCHANGED")
            self.assertEqual(
                apply(repeated, roots, "revision-repeat")["outcome"],
                "NO_MEANINGFUL_DELTA",
            )
            self.assertFalse((roots.root / "data/receipts/revision-repeat.json").exists())
            self.assertEqual(verify_graph_events(roots.root / "data/knowledge"), 2)
            self.assertTrue(verify_state(roots, require_accepted=True).valid)


if __name__ == "__main__":
    unittest.main()
