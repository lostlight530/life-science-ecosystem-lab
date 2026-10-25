"""Independent regression suite for research-software contract challenges."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ls_framework.challenge import CASES, run_challenge
from ls_framework.engine import assess

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
BUNDLE = FIXTURES / "software-cross-domain.json"


def specimen():
    return json.loads(BUNDLE.read_text(encoding="utf-8"))


class CrossDomainChallengeTests(unittest.TestCase):
    def test_expected_contract_mutations_all_match(self):
        report = run_challenge(specimen(), FIXTURES)
        self.assertEqual(report["status"], "PASS", report["mismatches"])
        self.assertEqual(report["counts"]["cases"], len(CASES))
        self.assertEqual(report["counts"]["mismatched"], 0)
        self.assertEqual(report["counts"]["expected_pass"], 2)
        self.assertGreater(report["counts"]["expected_fail"], 10)
        self.assertGreater(report["counts"]["expected_indeterminate"], 2)

    def test_repeat_is_byte_identical(self):
        first = json.dumps(run_challenge(specimen(), FIXTURES), sort_keys=True)
        second = json.dumps(run_challenge(specimen(), FIXTURES), sort_keys=True)
        self.assertEqual(first, second)

    def test_reference_bundle_is_not_modified(self):
        input_value = specimen()
        original = copy.deepcopy(input_value)
        run_challenge(input_value, FIXTURES)
        self.assertEqual(input_value, original)

    def test_no_cross_domain_biology_is_inferred(self):
        result = run_challenge(specimen(), FIXTURES)
        self.assertEqual(result["benchmark_type"], "SYNTHETIC_SOFTWARE_CONTRACT_MUTATION")
        self.assertTrue(result["nonclaims"])
        self.assertNotIn("scientific_truth_established", result)

    def test_independently_reported_failed_declaration(self):
        target = next(x for x in run_challenge(specimen(), FIXTURES)["cases"]
                      if x["id"] == "failed_execution_declaration")
        self.assertEqual(target["observed_status"], "INDETERMINATE")
        self.assertIn("NON_SUCCESSFUL_EXECUTION_RECORDED", target["observed_findings"])

    def test_wrong_source_bundle_fails_challenge(self):
        malformed = specimen()
        malformed["assets"][0]["sha256"] = "0" * 64
        result = run_challenge(malformed, FIXTURES)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("nominal_contract", result["mismatches"])

    def test_domain_names_are_not_biological_detection_algorithms(self):
        different = specimen()
        different["assets"][0]["domain"] = "transcriptomics"
        different["steps"][0]["supported_domains"].append("transcriptomics")
        different["steps"][0]["supported_domains"].remove("genomics")
        result = assess(different, FIXTURES)
        self.assertEqual(result["status"], "PASS")
        self.assertIn("transcriptomics", result["metrics"]["domains"])

    def test_standalone_module_cli_writes_report(self):
        with tempfile.TemporaryDirectory() as scratch:
            output = Path(scratch) / "challenge.json"
            proc = subprocess.run([
                sys.executable, "-m", "ls_framework.challenge",
                "--bundle", str(BUNDLE), "--root", str(FIXTURES),
                "--output", str(output),
            ], text=True, capture_output=True, check=False)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            summary = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "PASS")
            self.assertEqual(summary["counts"]["mismatched"], 0)


if __name__ == "__main__":
    unittest.main()
