import json
import tempfile
import unittest
from pathlib import Path
from evidence.documentation import audit_documents
from evidence.discovery import discover_repositories

class DocumentationDiscoveryTests(unittest.TestCase):
    def test_discovery_is_unapproved_and_safe(self):
        value=discover_repositories('bioinformatics-workflow',retrieve=lambda _:{'items':[{'full_name':'foo/research','description':'Example','default_branch':'main'}]})
        self.assertEqual(value['candidates'][0]['approved'],False)
        self.assertEqual(value['candidates'][0]['status'],'DISCOVERY_ONLY')
        with self.assertRaises(ValueError):
            discover_repositories('bad topic')

    def test_local_links_and_traversal(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/'index.md').write_text('[valid](notes.md) [bad](missing.md) [remote](https://example.org/guide)')
            (root/'notes.md').write_text('# Notes')
            result=audit_documents(root,['index.md','../elsewhere.md'])
            self.assertEqual(len(result.external_links),1)
            self.assertEqual(len(result.issues),2)

    def test_repo_documentation_manifest(self):
        root=Path(__file__).resolve().parents[1]
        files=json.loads((root/'evidence/profiles/docs.json').read_text())['documents']
        report=audit_documents(root,files)
        self.assertEqual(report.issues,(), '\n'.join(report.issues))

if __name__=='__main__': unittest.main()
