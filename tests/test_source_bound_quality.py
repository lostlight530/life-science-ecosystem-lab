"""Independent source binding and real upstream version-delta replay, never production."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from evidence.aggregation import aggregate_evidence, canonical_bytes
from evidence.knowledge_quality import audit_knowledge
from life_science_ecosystem_lab.knowledge import build_knowledge
from life_science_ecosystem_lab.lifecycle.orchestrator import apply_lifecycle
from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state

ROOT = Path(__file__).resolve().parents[1]
BASE = "dd2902a4b7acaa6e39112cb356a79fc1748ccb39"
WITNESS = (
    ("d2d7ea5136e34759cb48a1ae6cd4c35877074214", "78b4f53e748edb7acbdfce1991c71b139180e73a",
     "312b7363ff14b9f793bc47a523b999c8032a0d83", "ruby-3.3.10\n"),
    ("8d69b15b06aa7120ceffb96ae9a1113c3913b9f2", "9cf241ced3e335c6f8b3e8d77522d1570a6ad416",
     "73f716f1adce4be2077cebf25499cdb056f7b786", "ruby-3.3.14\n"),
)


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def reseal(value):
    value["knowledge_digest"] = hashlib.sha256(canonical_bytes(
        {k: v for k, v in value.items() if k != "knowledge_digest"})).hexdigest()
    return value


def record(witness):
    commit, tree, blob, text = witness
    raw = text.encode()
    assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == blob
    return {"source_id": "seek-version-case", "source_registry": "isolated-field-case",
            "repository": "seek4science/seek", "ref": "main", "commit": commit,
            "tree_sha": tree, "blob_sha": blob, "path": ".ruby-version", "text": text,
            "raw_size": len(raw), "content_sha256": hashlib.sha256(raw).hexdigest(),
            "selection_rule": "isolated@1.0.0", "trust": "primary", "collector_version": "field-case"}


class SourceBindingTests(unittest.TestCase):
    def setUp(self):
        self.c = load("data/inputs/current/candidate.json")
        self.k = load("data/knowledge/current.json")
        self.t = load("evidence/profiles/topics.json")

    def audit(self, value):
        return audit_knowledge(value, candidate=self.c, registry=self.t)

    def test_accepted_binding_and_nonclaims(self):
        report = self.audit(self.k)
        self.assertEqual(report["status"], "PASS", report["structural_findings"])
        self.assertEqual(report["source_binding"]["checked_fragments"], report["fragment_count"])
        self.assertEqual(report["source_binding"]["upstream_authenticity"], "NOT_ATTESTED")
        self.assertIsNone(report["label_evaluation"]["precision"])

    def test_resigned_fabrication_is_caught_without_workflow_builder(self):
        other = copy.deepcopy(self.k)
        other["topics"][0]["fragments"][0]["excerpt"] = "fabricated non-source excerpt 78342"
        reseal(other)
        self.assertEqual(audit_knowledge(other)["status"], "PASS")
        self.assertIn("BOUND_EXCERPT_NOT_IN_SOURCE",
                      {x["code"] for x in self.audit(other)["structural_findings"]})

    def test_resigned_alias_and_wrong_profile(self):
        other = copy.deepcopy(self.k)
        other["topics"][0]["fragments"][0]["matched_aliases"] = ["invented-alias"]
        self.assertIn("BOUND_ALIAS_MISMATCH",
                      {x["code"] for x in self.audit(reseal(other))["structural_findings"]})
        profile = copy.deepcopy(self.t)
        profile["topics"][0]["aliases"].append("invented")
        self.assertEqual(audit_knowledge(self.k, candidate=self.c, registry=profile)["status"], "FAIL")

    def test_missing_binding_input_and_numeric_labels(self):
        self.assertEqual(audit_knowledge(self.k, candidate=self.c)["status"], "FAIL")
        self.assertEqual(audit_knowledge(self.k, candidate=None, registry=None)["status"], "FAIL")
        with self.assertRaisesRegex(ValueError, "boolean"):
            audit_knowledge(self.k, labels={"schema_version": "1.0.0", "cases": [
                {"topic_id": "t", "repository": "a/b", "path": "x", "relevant": 1}]})

    def test_real_version_change_isolated_not_scientific_novelty(self):
        # Pinned factual version declarations, not a newly approved native source.
        profile = {"topics": [{"id": "runtime-version", "aliases": ["ruby-3"]}]}
        first = aggregate_evidence([record(WITNESS[0])], profile)
        second = aggregate_evidence([record(WITNESS[1])], profile, previous=first)
        a, b = (build_knowledge(c, profile) for c in (first, second))
        report = audit_knowledge(b, previous=a, candidate=second, registry=profile)
        self.assertEqual(report["status"], "PASS", report["structural_findings"])
        self.assertEqual(second["changes"][0]["kind"], "modified")
        self.assertEqual(len(report["comparison"]["document_text_changed"]), 1)
        self.assertFalse(report["comparison"]["source_revision_only"])
        self.assertEqual(report["comparison"]["semantic_novelty"], "NOT_EVALUATED")
        with tempfile.TemporaryDirectory() as tmp:
            roots = StateRoots(Path(tmp))
            for index, (candidate, knowledge) in enumerate(((first, a), (second, b))):
                result = apply_lifecycle(candidate, roots, logical_date="2026-11-25",
                    validated_head=BASE, current_head=BASE, knowledge=knowledge,
                    topic_registry=profile, execution_id="field-" + str(index))
                self.assertEqual(result["change_kind"], ("INITIAL_SNAPSHOT",
                    "DOCUMENT_CONTENT_OR_SELECTION_CHANGE")[index])
            self.assertTrue(verify_state(roots, require_accepted=True).valid)
            self.assertEqual(len(list((roots.root / "data/receipts").glob("*.json"))), 2)
            self.assertEqual(apply_lifecycle(second, roots, logical_date="2026-11-25",
                validated_head=BASE, current_head=BASE, knowledge=b, topic_registry=profile,
                execution_id="repeat")["outcome"], "NO_MEANINGFUL_DELTA")
