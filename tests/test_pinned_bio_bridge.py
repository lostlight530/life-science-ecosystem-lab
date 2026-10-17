"""Offline proof of the external pinned Git blob to Bio Tool boundary."""
import base64
import hashlib
import unittest
from unittest.mock import patch

from bio_tool.pinned_samples import audit_samples


def fake_fixture():
    raw = b">real_test_protein\nACDX\n"
    sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()
    sample = {"id": "fixed-test", "repository": "test/source",
              "commit": "1" * 40, "path": "examples/sequence.fasta", "blob_sha": sha,
              "bytes": len(raw), "format": "FASTA", "role": "example_sequence"}
    manifest = {"kind": "PINNED_PROTEIN_RESEARCH_DATA_SAMPLE_MANIFEST", "samples": [sample]}
    tree = {"truncated": False, "tree": [{"path": sample["path"], "type": "blob",
                                         "sha": sha, "size": len(raw)}]}
    blob = {"sha": sha, "encoding": "base64", "content": base64.b64encode(raw).decode("ascii")}
    return manifest, tree, blob


class PinnedBioBridgeTests(unittest.TestCase):
    def test_exact_git_identity_and_real_bio_analysis_without_source_republishing(self):
        manifest, tree, blob = fake_fixture()
        with patch("bio_tool.pinned_samples._fetch", side_effect=[tree, blob]) as fetch:
            report = audit_samples(manifest)
        self.assertEqual(fetch.call_count, 2)
        self.assertEqual(report["verified_count"], 1)
        self.assertEqual(report["samples"][0]["records"], 1)
        self.assertEqual(report["samples"][0]["residue_count"], 4)
        self.assertEqual(report["samples"][0]["status"], "WARN_UNCERTAIN_RESIDUES")
        self.assertNotIn("ACDX", repr(report))
        self.assertEqual(report["status"], "VERIFIED_PINNED_BLOBS_AND_ANALYZED_BIO_DATA")

    def test_tree_identity_mismatch_never_reaches_bio_parser(self):
        manifest, tree, blob = fake_fixture()
        tree["tree"][0]["sha"] = "0" * 40
        with patch("bio_tool.pinned_samples._fetch", return_value=tree) as fetch:
            with self.assertRaisesRegex(ValueError, "source tree/blob mismatch"):
                audit_samples(manifest)
        self.assertEqual(fetch.call_count, 1)

    def test_corrupt_blob_rejected_even_when_api_echoes_correct_sha(self):
        manifest, tree, blob = fake_fixture()
        blob["content"] = base64.b64encode(b">fake\nFAKE\n").decode()
        with patch("bio_tool.pinned_samples._fetch", side_effect=[tree, blob]):
            with self.assertRaisesRegex(ValueError, "raw size mismatch|Git blob identity mismatch"):
                audit_samples(manifest)


if __name__ == "__main__":
    unittest.main()
