"""Adversarial regression tests for independently installed LS Framework."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ls_framework import assess, canonical_digest

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def specimen():
    return json.loads((FIXTURES / "software-cross-domain.json").read_text(encoding="utf-8"))


class FrameworkContractTests(unittest.TestCase):
    def evaluate(self, bundle):
        return assess(bundle, FIXTURES)

    def test_two_domains_and_local_file_integrity(self):
        r = self.evaluate(specimen())
        self.assertEqual(r["status"], "PASS", r)
        self.assertEqual(r["metrics"]["local_bytes_verified"], 3)
        self.assertEqual(r["metrics"]["declared_only_assets"], 0)
        self.assertEqual(r["metrics"]["declared_cross_domain_steps"], 1)
        self.assertEqual(r["metrics"]["domains"], ["genomics", "life_sciences_integrative", "microscopy"])
        self.assertTrue(r["not_verified"])

    def test_empty_asset_bundle_is_not_valid_evidence(self):
        data = specimen()
        data["assets"] = []
        data["steps"] = []
        report = self.evaluate(data)
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("EMPTY_ASSET_SET", {x["code"] for x in report["errors"]})

    def test_canonical_determinism(self):
        original = specimen()
        self.assertEqual(self.evaluate(original), self.evaluate(copy.deepcopy(original)))
        self.assertEqual(canonical_digest(original), canonical_digest(json.loads(json.dumps(original, sort_keys=True))))

    def test_swapped_valid_data_digest_rejected(self):
        data = specimen()
        data["assets"][0]["sha256"] = data["assets"][1]["sha256"]
        self.assertIn("LOCAL_DIGEST_MISMATCH", {x["code"] for x in self.evaluate(data)["errors"]})

    def test_unknown_domain_and_method_mismatch(self):
        data = specimen()
        data["assets"][0]["domain"] = "chemistry_not_life_sciences"
        failures = {x["code"] for x in self.evaluate(data)["errors"]}
        self.assertIn("UNREVIEWED_DOMAIN", failures)
        self.assertIn("METHOD_DOMAIN_MISMATCH", failures)

    def test_escape_path_and_missing_file(self):
        data = specimen()
        data["assets"][0]["path"] = "../outside.json"
        self.assertIn("UNSAFE_PATH", {x["code"] for x in self.evaluate(data)["errors"]})
        data["assets"][0]["path"] = "does-not-exist.json"
        self.assertIn("LOCAL_ASSET_UNAVAILABLE_OR_ESCAPED", {
            x["code"] for x in self.evaluate(data)["errors"]
        })

    def test_declared_external_asset_remains_indeterminate(self):
        data = specimen()
        del data["assets"][0]["path"]
        r = self.evaluate(data)
        self.assertEqual(r["status"], "INDETERMINATE")
        self.assertEqual(r["metrics"]["declared_only_assets"], 1)

    def test_multiple_output_producers_rejected(self):
        data = specimen()
        another = copy.deepcopy(data["steps"][0])
        another["id"] = "second-step"
        data["steps"].append(another)
        self.assertIn("MULTIPLE_PRODUCERS", {x["code"] for x in self.evaluate(data)["errors"]})

    def test_lineage_cycle_rejected(self):
        data = specimen()
        data["steps"].append({
            "id": "back-edge", "method": data["steps"][0]["method"],
            "inputs": ["a-integrated"], "outputs": ["a-genomics"],
            "supported_domains": ["genomics", "life_sciences_integrative"],
            "outcome": "SUCCEEDED",
        })
        self.assertIn("LINEAGE_CYCLE", {x["code"] for x in self.evaluate(data)["errors"]})

    def test_claims_are_proposals_only(self):
        data = specimen()
        claim = {"id": "claim-1", "statement": "Synthetic data proves biological truth",
                 "evidence": ["a-genomics"], "authority": "PROPOSAL_ONLY"}
        data["claims"].append(claim)
        r = self.evaluate(data)
        self.assertEqual(r["status"], "INDETERMINATE")
        self.assertIn("SCIENTIFIC_CLAIM_NOT_ADJUDICATED", {x["code"] for x in r["warnings"]})
        claim["authority"] = "ACCEPTED"
        self.assertIn("SCIENTIFIC_AUTHORITY_ESCALATION", {x["code"] for x in self.evaluate(data)["errors"]})

    def test_failed_execution_not_green(self):
        data = specimen()
        data["steps"][0]["outcome"] = "FAILED"
        self.assertEqual(self.evaluate(data)["status"], "INDETERMINATE")

    def test_schema_bounded_and_unhashable_values_fail_closed(self):
        for value in ([], {}, {"bad": "bundle"}):
            self.assertEqual(self.evaluate(value)["status"], "FAIL")
        data = specimen()
        data["assets"] = data["assets"] * 50
        self.assertIn("UNBOUNDED_COLLECTION", {x["code"] for x in self.evaluate(data)["errors"]})
        data = specimen()
        data["assets"][0]["domain"] = ["not hashable"]
        self.assertEqual(self.evaluate(data)["status"], "FAIL")
        data = specimen()
        data["steps"][0]["outcome"] = {}
        self.assertEqual(self.evaluate(data)["status"], "FAIL")

    def test_malformed_claim_evidence_fails_closed(self):
        data = specimen()
        data["claims"].append({"id": "claim-2", "statement": "untrusted", "evidence": [{}], "authority": "PROPOSAL_ONLY"})
        self.assertIn("UNKNOWN_OR_DUPLICATE_CLAIM_EVIDENCE", {
            x["code"] for x in self.evaluate(data)["errors"]
        })

    def test_command_line_independent_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "result.json"
            r = subprocess.run(
                [sys.executable, "-m", "ls_framework", "assess",
                 "--bundle", str(FIXTURES / "software-cross-domain.json"),
                 "--root", str(FIXTURES), "--output", str(out)],
                text=True, capture_output=True, check=False,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(json.loads(out.read_text())["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
