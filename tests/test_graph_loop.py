"""Executable graph/FTS5 contract, no network or LLM."""
import json
import tempfile
import unittest
from pathlib import Path

from life_science_ecosystem_lab.graph import project_graph, search_graph, verify_graph, write_graph


class GraphLoopTests(unittest.TestCase):
    def knowledge(self):
        digest = "a" * 64
        doc = "github:example/work@" + "b" * 40 + ":README.md"
        return {"knowledge_digest": digest,
                "topics": [{"topic_id": "monitoring", "fragments": [{"repository": "example/work", "commit": "b" * 40,
                             "path": "README.md", "excerpt": "monitoring a workflow", "url": "https://github.com/example/work/blob/" + "b" * 40 + "/README.md"}]}],
                "knowledge_graph": {"nodes": [{"id": "topic:monitoring", "kind": "research-topic"},
                                              {"id": doc, "kind": "source-document"}],
                                    "edges": [{"from": "topic:monitoring", "to": doc, "relation": "SOURCE_MATCH",
                                               "evidence_sha256": "c" * 64}]}}

    def test_deterministic_projection_and_search(self):
        with tempfile.TemporaryDirectory() as td:
            directory = Path(td)
            k = self.knowledge()
            first = write_graph(k, directory)
            second = write_graph(k, directory)
            self.assertEqual(first, second)
            self.assertEqual(first, verify_graph(directory, k))
            q = search_graph(directory, "monitoring", limit=2, hops=1)
            self.assertGreaterEqual(len(q["results"]), 1)
            self.assertIn("topic:monitoring", {r["id"] for r in q["results"]})
            self.assertFalse(q["limits"]["semantic_inference"])

    def test_reject_dangling_and_invented_predicate(self):
        k = self.knowledge()
        k["knowledge_graph"]["edges"][0]["relation"] = "PROVES_CAUSALITY"
        with self.assertRaises(ValueError):
            project_graph(k)
        k["knowledge_graph"]["edges"][0]["relation"] = "SOURCE_MATCH"
        k["knowledge_graph"]["edges"][0]["to"] = "missing"
        with self.assertRaises(ValueError):
            project_graph(k)

    def test_detect_tampering_and_limits(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            write_graph(self.knowledge(), p)
            with self.assertRaises(ValueError):
                search_graph(p, "monitoring", hops=4)
            entity_path = p / "entities.jsonl"
            entity_path.write_text(entity_path.read_text() + '{"id":"unexpected"}\n')
            with self.assertRaises(ValueError):
                verify_graph(p)

class EventLedgerTests(unittest.TestCase):
    def test_event_chain(self):
        from life_science_ecosystem_lab.graph import append_graph_event, verify_graph_events
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for index in range(2):
                append_graph_event(root, receipt={"run_id": str(index), "logical_date": "2026-10-17", "output_digest": "a" * 64})
            self.assertEqual(verify_graph_events(root), 2)
            path = root / 'events.jsonl'
            content = path.read_text().replace('"run_id":"0"', '"run_id":"changed"')
            path.write_text(content)
            with self.assertRaises(ValueError):
                verify_graph_events(root)