import copy
import json
import unittest
from pathlib import Path

from life_science_ecosystem_lab.evidence.aggregation import aggregate_evidence
from life_science_ecosystem_lab.evidence.validation import validate_candidate_bundle
from life_science_ecosystem_lab.knowledge import build_knowledge, verify_knowledge

ROOT = Path(__file__).resolve().parents[1]


class KnowledgeWorkflowTests(unittest.TestCase):
    def setup_inputs(self):
        records = json.loads((ROOT / 'examples/evidence-records.json').read_text())
        topics = json.loads((ROOT / 'profiles/topics.json').read_text())
        return records, topics

    def test_extracts_actual_source_cited_fragments_with_stable_digests(self):
        records, topics = self.setup_inputs()
        first = aggregate_evidence(records, topics)
        self.assertTrue(validate_candidate_bundle(first).valid)
        knowledge = build_knowledge(first, topics)
        self.assertEqual(len(knowledge['topics']), 3)
        self.assertTrue(all(f['commit'] and f['url'].startswith('https://github.com/') for t in knowledge['topics'] for f in t['fragments']))
        verify_knowledge(first, topics, knowledge)
        second = aggregate_evidence(list(reversed(records)), topics)
        self.assertEqual(first['output_digest'], second['output_digest'])
        self.assertEqual(knowledge['knowledge_digest'], build_knowledge(second, topics)['knowledge_digest'])

    def test_changes_to_observation_clock_do_not_change_semantic_digest(self):
        records, topics = self.setup_inputs()
        first = aggregate_evidence(records, topics)
        for record in records:
            record['retrieved_at'] = '2027-01-01T00:00:00Z'
        self.assertEqual(first['output_digest'], aggregate_evidence(records, topics)['output_digest'])

    def test_tampered_citation_is_rejected(self):
        records, topics = self.setup_inputs()
        bundle = aggregate_evidence(records, topics)
        value = build_knowledge(bundle, topics)
        changed = copy.deepcopy(value)
        changed['topics'][0]['fragments'][0]['excerpt'] = 'fabricated'
        with self.assertRaisesRegex(ValueError, 'does not match'):
            verify_knowledge(bundle, topics, changed)

    def test_forged_content_digest_is_rejected(self):
        records, topics = self.setup_inputs()
        records[0]['content_sha256'] = '0' * 64
        bundle = aggregate_evidence(records, topics)
        self.assertFalse(validate_candidate_bundle(bundle).valid)
        with self.assertRaisesRegex(ValueError, 'unverified candidate'):
            build_knowledge(bundle, topics)

    def test_same_path_in_different_repositories_remains_distinct(self):
        records, topics = self.setup_inputs()
        output = aggregate_evidence(records, topics)
        self.assertEqual(len(output['changes']), 3)
        self.assertEqual(len({(r['repository'], r['path']) for r in output['records']}), 3)

    def test_unobserved_topic_has_explicit_uncertainty(self):
        records, topics = self.setup_inputs()
        topics['topics'].append({'id':'not-observed','aliases':['antimatter'],'required_terms':[],'excluded_terms':[],'minimum_matches':1})
        knowledge = build_knowledge(aggregate_evidence(records, topics), topics)
        self.assertEqual(next(t for t in knowledge['topics'] if t['topic_id'] == 'not-observed')['coverage'], 'UNOBSERVED')
        self.assertEqual(next(u for u in knowledge['unresolved'] if u['topic_id'] == 'not-observed')['reason'], 'NO_SELECTED_EVIDENCE')
