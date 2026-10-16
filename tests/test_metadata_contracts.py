import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.github/scripts'))
from check_metadata import verify

class MetadataContracts(unittest.TestCase):
 def test_versions_creators_and_standard_statuses(self):
  verify()

if __name__=='__main__':unittest.main()
