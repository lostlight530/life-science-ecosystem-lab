"""Offline replay of frozen Nov 28 independent artifact observations; not new ZIP retrieval."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/provenance/2026-11-28-independent-artifact-byte-replay.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class Nov28ArtifactReplay(unittest.TestCase):
    def test_byte_identity_and_original_scope(self):
        d = load(RECORD)
        prior = load(ROOT / d["prior_observation"])
        self.assertTrue(d["prior_cutoff_preserved"])
        self.assertFalse(prior["schedule"]["artifact_contents_independently_read"])
        old = {a["id"]: a for a in prior["schedule"]["new_artifacts"]}
        new = {a["id"]: a for a in d["artifacts"]}
        self.assertEqual(set(old), set(new))
        self.assertEqual(len(new), d["artifact_count"])
        self.assertEqual(sum(len(a["members_sha256"]) for a in new.values()), d["member_occurrences"])
        self.assertEqual(sum(len(a["embedded_report_digests_recomputed"]) for a in new.values()),
                         d["embedded_report_digest_occurrences"])
        for identity, a in new.items():
            for key in ("run_id", "job_id", "provider_sha256"):
                self.assertEqual(a[key], old[identity][key])
            self.assertEqual(a["provider_sha256"], a["independently_measured_sha256"])
            self.assertEqual(a["provider_sha256"], a["upload_log_sha256"])
            self.assertTrue(a["zip_crc_ok"] and a["one_byte_mutation_rejected"])
            self.assertGreater(a["bytes"], 0)
            self.assertTrue(all(len(x) == 64 for x in a["members_sha256"].values()))
            self.assertLessEqual(set(a["embedded_report_digests_recomputed"]), set(a["members_sha256"]))

    def test_nonclaim_and_independent_quality_surfaces(self):
        d = load(RECORD)
        k = d["knowledge"]
        quality = [a["members_sha256"]["knowledge-quality.json"] for a in d["artifacts"]
                   if "knowledge-quality.json" in a["members_sha256"]]
        self.assertEqual(quality, [k["quality_report_member_sha256"]] * k["identical_report_occurrences"])
        self.assertEqual(k["label_status"], "NO_HUMAN_LABELS")
        self.assertEqual(k["scientific_truth"], "NOT_EVALUATED")
        self.assertEqual(k["source_binding"], "NOT_SUPPLIED_TO_NATIVE_QUALITY_REPORT")
        institution = d["institutional"]
        self.assertEqual(sum(v is None for v in institution["observations"].values()),
                         institution["inconclusive_count"])
        self.assertIsNone(institution["observations"][institution["inconclusive"]["service"]])
        self.assertEqual(institution["inconclusive"]["result"], "INCONCLUSIVE_NETWORK")
        self.assertEqual(institution["inconclusive"]["cause"], "UNKNOWN")
        self.assertFalse(institution["service_health_or_authorization_verified"])
        self.assertEqual(d["custom"]["status"], "PASS")
        self.assertEqual(d["custom"]["ecosystem_preflight_status"], "REVIEW_REQUIRED")
        self.assertEqual(d["custom"]["source_commit"], d["source_execution_sha"])


if __name__ == "__main__":
    unittest.main()
