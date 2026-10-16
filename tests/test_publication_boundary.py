"""Do not accidentally publish internal plans or credential-like literals."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.github' / 'scripts'))
from check_publication_boundary import verify


class PublicationBoundaryTests(unittest.TestCase):
    def test_public_tree(self):
        verify()

    def test_rejects_private_material(self):
        with self.assertRaises(SystemExit):
            verify(['docs/archive/original-design-2026-10-16/specs/a.md'])


if __name__ == '__main__':
    unittest.main()
