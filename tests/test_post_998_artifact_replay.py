"""Replay frozen addendum relationships; not a new remote download or experiment."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/provenance/2026-11-27-independent-artifact-byte-replay.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class Post998ArtifactReplay(unittest.TestCase):
    def test_addendum_preserves_cutoff_and_byte_identities(self):
        d = load(RECORD)
        p = load(ROOT / d["prior_observation"])
        self.assertFalse(p["schedule"]["artifact_contents_independently_read"])
        self.assertTrue(d["prior_cutoff_preserved"])
        self.assertTrue(d["artifact_contents_independently_read"])
        before = {a["id"]: a for a in p["schedule"]["artifacts"]}
        after = {a["id"]: a for a in d["artifacts"]}
        self.assertEqual(set(before), set(after))
        self.assertEqual(len(after), d["artifact_count"])
        self.assertEqual(sum(len(a["members_sha256"]) for a in after.values()), d["member_count"])
        for key, old in before.items():
            a = after[key]
            for field in ("run_id", "job_id", "sha256"):
                self.assertEqual(a[field], old[field])
            self.assertTrue(a["independent_zip_sha256_match"] and a["zip_crc_ok"] and a["tamper_digest_rejected"])
            self.assertGreater(a["byte_count"], 0)
            self.assertTrue(all(len(x) == 64 for x in a["members_sha256"].values()))
        self.assertEqual(d["embedded_report_digest_match_count"], d["embedded_report_digest_recomputed_count"])
        self.assertEqual(d["negative_controls"]["zip_mutation_rejected_count"], len(after))

    def test_boundaries_and_pinned_sample_identities(self):
        d = load(RECORD)
        bio = d["bio"]
        manifest = load(ROOT / "evidence/profiles/research/protein_structure/sample-manifest.json")
        pinned = {s["id"]: s for s in manifest["samples"] if s["format"] in ("FASTA", "PDB")}
        samples = {s["id"]: s for s in bio["samples"]}
        self.assertEqual(set(samples), set(pinned))
        self.assertEqual(len(samples), bio["pinned_verified_count"])
        for key, sample in samples.items():
            for field in ("repository", "commit", "path", "blob_sha", "bytes", "format"):
                self.assertEqual(sample[field], pinned[key][field])
            self.assertEqual(sample["independently_recomputed_git_blob_sha"], sample["blob_sha"])
            self.assertTrue(sample["independent_sha256_and_count_match"])
        self.assertEqual(bio["offline_fasta"]["status"], "WARN_UNCERTAIN_RESIDUES")
        self.assertEqual(bio["scientific_model_execution_or_accuracy_claim"], "NOT_EVALUATED")
        self.assertEqual(d["daily_custom"]["ecosystem_preflight_status"], "REVIEW_REQUIRED")
        self.assertFalse(d["institutional"]["service_health_or_authorization_verified"])
        k = d["knowledge"]
        self.assertFalse(k["observed_native_quality_report_source_binding_present"])
        self.assertEqual(k["label_status"], "NO_HUMAN_LABELS")
        self.assertEqual(k["independent_candidate_binding"]["expected_fragments"], k["fragments"])
        self.assertEqual(k["independent_candidate_binding"]["identity_alias_excerpt_findings"], 0)
        self.assertTrue(k["independent_candidate_binding"]["fabricated_excerpt_rejected"])
        self.assertEqual(k["independent_candidate_binding"]["scientific_truth"], "NOT_EVALUATED")
