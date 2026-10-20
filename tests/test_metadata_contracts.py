import json
import sys
import tomllib
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.github/scripts'))
from check_metadata import verify

class MetadataContracts(unittest.TestCase):
 def test_versions_creators_and_standard_statuses(self):
  verify()

 def test_biotools_registration_identity_keeps_external_boundaries(self):
  descriptor=json.loads((ROOT/'metadata/biotools-protein-audit.draft.json').read_text(encoding='utf-8'))
  status=json.loads((ROOT/'metadata/standards-status.json').read_text(encoding='utf-8'))
  self.assertEqual(descriptor['biotoolsID'], 'life-science-protein-file-audit')
  self.assertEqual(descriptor['biotoolsCURIE'], 'biotools:life-science-protein-file-audit')
  self.assertEqual(status['biotools_registration'], {
   'biotools_id': 'life-science-protein-file-audit',
   'biotools_curie': 'biotools:life-science-protein-file-audit',
   'record_url': 'https://bio.tools/life-science-protein-file-audit',
   'status': 'EXTERNALLY_OBSERVED',
   'evidence_basis': 'MAINTAINER_OBSERVED_REGISTRY_RECORD',
   'api_verification': 'NOT_INDEPENDENTLY_VERIFIED',
   'curation_status': 'NOT_INDEPENDENTLY_VERIFIED',
  })
  self.assertEqual(status['openebench_record']['tool_id'], descriptor['biotoolsID'])
  self.assertEqual(status['openebench_record']['upstream_validated'], 0)
  self.assertIn('not an OpenEBench scientific benchmark', status['openebench_record']['limitations'][0])

 def test_external_release_and_workflow_records_are_separate(self):
  status=json.loads((ROOT/'metadata/standards-status.json').read_text(encoding='utf-8'))
  self.assertEqual(status['github_release']['tag'], 'v0.4.0')
  self.assertEqual(status['zenodo_release']['doi'], '10.5281/zenodo.23447089')
  self.assertEqual(status['workflowhub_registration']['version'], 2)
  self.assertEqual(status['workflowhub_registration']['doi'], '10.48546/workflowhub.workflow.2347.2')
  self.assertNotEqual(status['zenodo_release']['doi'], status['workflowhub_registration']['doi'])

 def test_framework_package_metadata_is_independent_and_bounded(self):
  data=tomllib.loads((ROOT/'framework/pyproject.toml').read_text(encoding='utf-8'))
  project=data['project']
  self.assertEqual(project['name'], 'life-sciences-rse-framework')
  self.assertEqual(project['version'], '0.1.0')
  self.assertEqual(project['scripts'], {'ls-framework': 'ls_framework.cli:main'})
  self.assertEqual(project['dependencies'], [])
  self.assertEqual(project['license']['text'], 'MIT')
  self.assertIn('/tree/main/framework', project['urls']['Homepage'])

 def test_portable_cwl_interfaces_have_human_readable_metadata(self):
  cwl=(ROOT/'.github/knowledge/main.cwl').read_text(encoding='utf-8')
  expected_labels=(
   'Frozen GitHub evidence records',
   'Versioned topic registry',
   'Aggregate evidence records',
   'Validate evidence candidate',
   'Extract source-grounded knowledge',
   'Verify knowledge map',
   'Candidate evidence package',
   'Validation report',
   'Source-grounded knowledge map',
   'Knowledge verification report',
  )
  for label in expected_labels:
   self.assertIn(f'label: {label}', cwl)
  self.assertGreaterEqual(cwl.count('    doc:'), 10)

if __name__=='__main__':unittest.main()
