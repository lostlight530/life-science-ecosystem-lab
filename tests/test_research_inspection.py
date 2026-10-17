"""External Tool static inspection and report evidence tests."""
import json
import tempfile
import unittest
from pathlib import Path
from evidence.inspection import inspect_repository, write_reports

class InspectionTests(unittest.TestCase):
    def test_external_project_without_crate_is_warning(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'README.md').write_text('# Research project\n')
            report = inspect_repository(root)
            self.assertEqual(report['status'], 'WARN')
            self.assertEqual(report['counts']['FAIL'], 0)
            write_reports(report, root / 'out.json', markdown=root / 'out.md', sarif=root / 'out.sarif')
            self.assertIn('Research Software Evidence Inspection', (root / 'out.md').read_text())
            self.assertEqual(json.loads((root / 'out.sarif').read_text())['version'], '2.1.0')

    def test_bad_main_workflow_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'README.md').write_text('hi')
            (root / 'ro-crate-metadata.json').write_text(json.dumps({'@graph': [{'@id': './', 'mainEntity': {'@id': 'missing.cwl'}}]}))
            self.assertEqual(inspect_repository(root)['status'], 'FAIL')

    def test_workflow_file_and_bioschemas(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'README.md').write_text('hi')
            (root / 'CITATION.cff').write_text('cff-version: 1.2.0\n')
            (root / 'workflow.cwl').write_text('cwlVersion: v1.2\n')
            (root / 'ro-crate-metadata.json').write_text(json.dumps({'@graph': [{'@id': './', 'mainEntity': {'@id': 'workflow.cwl'}}]}))
            (root / 'metadata').mkdir()
            (root / 'metadata' / 'bioschemas-tool.jsonld').write_text('{"@type":"SoftwareApplication","name":"Tool"}')
            self.assertEqual(inspect_repository(root)['status'], 'PASS')