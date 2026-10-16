import unittest
from evidence.aggregation import aggregate_evidence
from evidence.normalization import canonical_text_bytes, sha256_bytes
from life_science_ecosystem_lab.knowledge import build_knowledge, verify_knowledge

class GraphTests(unittest.TestCase):
 def test_graph_contains_only_verified_citations(self):
  text='Workflow registration uses provenance.'
  record={"source_id":"test","source_registry":"life-science-test","repository":"example/science","ref":"main","commit":"a"*40,"tree_sha":"b"*40,"blob_sha":"c"*40,"path":"docs/workflow.md","text":text,"raw_size":len(text),"content_sha256":sha256_bytes(canonical_text_bytes(text)),"selection_rule":"test@1.0.0","trust":"primary","collector_version":"0.3.0"}
  registry={"topics":[{"id":"registration","aliases":["workflow"],"required_terms":[],"excluded_terms":[],"minimum_matches":1}]}
  candidate=aggregate_evidence([record],registry)
  map_=build_knowledge(candidate,registry)
  self.assertEqual(len(map_['knowledge_graph']['edges']),1)
  self.assertIn('github:example/science@',map_['knowledge_graph']['edges'][0]['to'])
  verify_knowledge(candidate,registry,map_)

if __name__=='__main__':unittest.main()
