"""Fail-closed source diagnostics and graph state verification regression."""
import json
import tempfile
import unittest
from pathlib import Path

from evidence.cli import main as evidence_main
from evidence.validation import validate_candidate_bundle
from life_science_ecosystem_lab.graph import write_graph
from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state


class DegradedSourceTests(unittest.TestCase):
    def test_optional_source_warning_does_not_become_accepted_knowledge(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            diagnostics = root / 'warnings.json'
            diagnostics.write_text('[{"source_id":"optional","reason":"OPTIONAL_SOURCE_UNAVAILABLE"}]')
            candidate = root / 'candidate.json'
            repository_root = Path(__file__).resolve().parents[1]
            self.assertEqual(evidence_main([
                'aggregate', '--input', str(repository_root / 'evidence/examples/evidence-records.json'),
                '--topics', str(repository_root / 'evidence/profiles/topics.json'),
                '--diagnostics', str(diagnostics), '--output', str(candidate)
            ]), 0)
            output = json.loads(candidate.read_text())
            self.assertTrue(validate_candidate_bundle(output).valid)
            self.assertFalse(output['projection_eligible'])
            self.assertEqual(len(output['diagnostics']), 1)

    def test_graph_integrity_is_part_of_state_verification(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            directory = root / 'data' / 'knowledge'
            directory.mkdir(parents=True)
            doc = {"knowledge_digest": "b" * 64, "knowledge_graph": {"nodes": [], "edges": []}, "topics": []}
            (directory / 'current.json').write_text(json.dumps(doc))
            write_graph(doc, directory)
            self.assertTrue(verify_state(StateRoots(root)).valid)
            (directory / 'entities.jsonl').write_text('{"id":"tampered"}\n')
            self.assertFalse(verify_state(StateRoots(root)).valid)