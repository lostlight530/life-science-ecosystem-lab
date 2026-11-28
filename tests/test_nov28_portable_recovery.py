"""Frozen evidence relationships and a report-digest scope falsifier, not new ZIP retrieval."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/provenance/2026-11-28-portable-independent-recovery.json"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


class PortableIndependentRecovery(unittest.TestCase):
    def setUp(self):
        self.d = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_frozen_artifact_join(self):
        d = self.d
        old = json.loads((ROOT / d["prior_observation"]).read_text(encoding="utf-8"))
        current = {x["id"]: x for x in d["artifacts"]}
        self.assertEqual(len(current), len(d["artifacts"]))
        self.assertEqual(len(current), d["artifact_count"])
        for a in old["artifacts"]:
            self.assertEqual(current[a["id"]]["provider_sha256"], a["provider_sha256"])
            self.assertEqual(current[a["id"]]["bytes"], a["bytes"])
        for a in current.values():
            self.assertEqual(a["provider_sha256"], a["independently_measured_sha256"])
            self.assertRegex(a["provider_sha256"], r"^[0-9a-f]{64}$")
        self.assertIn(d["recovery"]["artifact_id"], current)
        self.assertIn(d["replay"]["source_candidate_artifact_id"], current)
        self.assertIn(d["replay"]["quality_comparator_artifact_id"], current)
        self.assertIn(d["replay"]["bio_comparator_artifact_id"], current)

    def test_actual_inspection_digest_contract_and_negative_control(self):
        r = self.d["inspection_digest_scope"]
        payload = r["included_payload"]
        self.assertEqual(digest(payload), r["expected_sha256"])
        # The naive oracle included a location field outside the stable digest.
        self.assertNotEqual(digest(dict(payload, object=r["observed_object"])), r["expected_sha256"])
        # A real covered-field mutation must change the digest.
        self.assertNotEqual(digest(dict(payload, status="FAIL")), r["expected_sha256"])

    def test_execution_scope_does_not_promote_claims(self):
        d = self.d
        self.assertEqual(d["recovery"]["source_git_blob_matches"], d["recovery"]["python_source_paths"])
        self.assertFalse(d["recovery"]["full_repo_clone"])
        self.assertFalse(d["recovery"]["full_suite_independently_run"])
        self.assertFalse(d["recovery"]["framework_independently_run"])
        self.assertEqual(d["replay"]["scientific_truth"], "NOT_EVALUATED")
        self.assertEqual(len(d["replay"]["byte_equal"]), 4)
        self.assertEqual(len(d["replay"]["json_equal"]), 3)
        self.assertEqual([x["exit"] for x in d["replay"]["negative_cli_controls"]], [2, 2, 2])
        self.assertEqual(d["census"]["visible_runs"], d["census"]["success"] + d["census"]["cancelled"])
        self.assertEqual(d["census"]["visible_runs"] - d["census"]["previous_visible_run_count"],
                         d["census"]["additional_successful_pr_or_push_runs"])


if __name__ == "__main__":
    unittest.main()
