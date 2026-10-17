"""Contract checks for publicly archived real protein-demo run evidence."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "evidence" / "field-tests" / "2026-10-17-protein-structure-demo.json"


class ProteinFieldRecordTests(unittest.TestCase):
    def test_run_index_matches_pinned_research_profiles(self):
        value = json.loads(RECORD.read_text())
        registry = json.loads((ROOT / value["sources"]["registry"]).read_text())
        manifest = json.loads((ROOT / value["data_samples"]["manifest"]).read_text())
        topics = json.loads((ROOT / value["knowledge"]["native_profile"]).read_text())
        self.assertEqual(len(registry["sources"]), value["sources"]["count"])
        self.assertEqual(len(manifest["samples"]), value["data_samples"]["verified_git_objects_and_file_format"])
        self.assertEqual(len(topics["topics"]), value["knowledge"]["topics"])
        self.assertEqual(value["agent"]["authority"], "PROPOSAL_ONLY")
        self.assertFalse(value["isolated_lifecycle"]["real_production_data_written"])
        self.assertFalse(value["data_samples"]["model_inference_executed"])

    def test_artifact_and_source_digests_are_hex_and_bound_to_run(self):
        value = json.loads(RECORD.read_text())
        for digest in (value["artifact"]["sha256"], value["artifact"]["field_summary_sha256"],
                       value["artifact"]["sample_audit_sha256"], value["sources"]["evidence_digest"],
                       value["knowledge"]["digest"]):
            self.assertTrue(re.fullmatch("[0-9a-f]{64}", digest))
        self.assertIn(str(value["source_run_id"]), value["source_run_url"])
        self.assertIn(str(value["artifact"]["id"]), value["artifact"]["url"])
        self.assertEqual(value["isolated_lifecycle"]["repeat_outcome"], "NO_MEANINGFUL_DELTA")
        self.assertEqual(value["isolated_lifecycle"]["linked_event_count"], 2)


if __name__ == "__main__":
    unittest.main()
