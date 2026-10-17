"""Contract tests for non-scientific cross-version knowledge quality review."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

from evidence.aggregation import aggregate_evidence, canonical_bytes
from evidence.knowledge_quality import audit_knowledge
from life_science_ecosystem_lab.knowledge import build_knowledge

ROOT = Path(__file__).resolve().parents[1]


def _seal(value):
    value["knowledge_digest"] = hashlib.sha256(
        canonical_bytes({k: v for k, v in value.items() if k != "knowledge_digest"})
    ).hexdigest()
    return value


def _knowledge():
    records = json.loads((ROOT / "evidence/examples/evidence-records.json").read_text(encoding="utf-8"))
    topics = json.loads((ROOT / "evidence/profiles/topics.json").read_text(encoding="utf-8"))
    return build_knowledge(aggregate_evidence(records, topics), topics), records, topics


class QualityAuditTests(unittest.TestCase):
    def test_current_accepted_state_is_valid_structural_input(self):
        knowledge = json.loads((ROOT / "data/knowledge/current.json").read_text(encoding="utf-8"))
        report = audit_knowledge(knowledge)
        self.assertEqual(report["status"], "PASS", report["structural_findings"])
        self.assertEqual(report["topic_count"], 3)
        self.assertEqual(report["fragment_count"], 26)
        self.assertIsNone(report["label_evaluation"]["precision"])
        self.assertEqual(report["label_evaluation"]["status"], "NO_HUMAN_LABELS")
        self.assertIn("scientific truth or biological causal relationships", report["not_verified"])

    def test_synthetic_map_and_repeat_review_are_deterministic(self):
        value, _, _ = _knowledge()
        a = audit_knowledge(value, previous=value)
        b = audit_knowledge(copy.deepcopy(value), previous=copy.deepcopy(value))
        self.assertEqual(a, b)
        self.assertEqual(a["status"], "PASS")
        self.assertEqual(a["comparison"]["added"], [])
        self.assertEqual(a["comparison"]["document_text_changed"], [])

    def test_modified_excerpt_requires_digest_and_upstream_independent_check(self):
        value, _, _ = _knowledge()
        value["topics"][0]["fragments"][0]["excerpt"] = "fabricated"
        self.assertIn("DIGEST_MISMATCH", {i["code"] for i in audit_knowledge(value)["structural_findings"]})
        # Re-signing an unsupported excerpt does NOT establish scientific truth.
        _seal(value)
        report = audit_knowledge(value)
        self.assertEqual(report["status"], "PASS")
        self.assertIn("source excerpt accuracy against remote upstream without supplied candidate",
                      report["not_verified"])

    def test_corrupt_graph_or_counts_fail_even_with_recomputed_digest(self):
        value, _, _ = _knowledge()
        value["knowledge_graph"]["edges"].pop()
        _seal(value)
        self.assertIn("GRAPH_EDGE_MISMATCH", {i["code"] for i in audit_knowledge(value)["structural_findings"]})
        other, _, _ = _knowledge()
        other["topics"][0]["fragment_count"] += 1
        _seal(other)
        self.assertIn("COVERAGE_COUNT_MISMATCH",
                      {i["code"] for i in audit_knowledge(other)["structural_findings"]})

    def test_revision_only_does_not_claim_scientific_novelty(self):
        old, records, topics = _knowledge()
        records[0]["commit"] = "a" * 40
        new = build_knowledge(aggregate_evidence(records, topics), topics)
        report = audit_knowledge(new, previous=old)
        self.assertEqual(report["status"], "PASS", report["structural_findings"])
        self.assertTrue(report["comparison"]["source_revision_only"])
        self.assertFalse(report["comparison"]["document_text_changed"])
        self.assertEqual(report["comparison"]["semantic_novelty"], "NOT_EVALUATED")

    def test_profile_change_is_distinct_from_document_change(self):
        old, records, topics = _knowledge()
        topics["topics"][0]["aliases"].append("structure")
        new = build_knowledge(aggregate_evidence(records, topics), topics)
        report = audit_knowledge(new, previous=old)
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["comparison"]["topic_profile_changed"])

    def test_explicit_user_labels_are_a_sample_not_truth(self):
        knowledge, _, _ = _knowledge()
        fragment = knowledge["topics"][0]["fragments"][0]
        topic_id = knowledge["topics"][0]["topic_id"]
        labels = {"schema_version": "1.0.0", "cases": [
            {"topic_id": topic_id, "repository": fragment["repository"],
             "path": fragment["path"], "relevant": True},
            {"topic_id": topic_id, "repository": "test/example",
             "path": "not-selected.md", "relevant": False},
        ]}
        report = audit_knowledge(knowledge, labels=labels)
        self.assertEqual(report["label_evaluation"]["counts"], {"TP": 1, "FP": 0, "TN": 1, "FN": 0})
        self.assertIn("USER_SUPPLIED", report["label_evaluation"]["status"])

    def test_duplicate_and_invalid_labels_are_rejected(self):
        knowledge, _, _ = _knowledge()
        labels = {"schema_version": "1.0.0", "cases": [
            {"topic_id": "test", "repository": "sample/repo", "path": "README.md", "relevant": True}
        ]}
        with self.assertRaisesRegex(ValueError, "duplicate"):
            audit_knowledge(knowledge, labels={"schema_version": "1.0.0",
                                             "cases": labels["cases"] * 2})
        with self.assertRaisesRegex(ValueError, "boolean"):
            audit_knowledge(knowledge, labels={"schema_version": "1.0.0",
                                             "cases": [dict(labels["cases"][0], relevant="yes")]})

    def test_corrupt_previous_state_fails_without_comparison(self):
        value, _, _ = _knowledge()
        old = copy.deepcopy(value)
        old["knowledge_digest"] = "0" * 64
        report = audit_knowledge(value, previous=old)
        self.assertEqual(report["status"], "FAIL")
        self.assertIsNone(report["comparison"])
        self.assertIn("BASELINE_DIGEST_MISMATCH", {x["code"] for x in report["structural_findings"]})


if __name__ == "__main__":
    unittest.main()
