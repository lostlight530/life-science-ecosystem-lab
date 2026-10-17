"""Offline contract tests for the institutional reference plane only."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from evidence.daily_selfcheck import OFFICIAL, institutional_report, load_object, validate_official

ROOT = Path(__file__).resolve().parents[1]


class InstitutionalSelfcheckTests(unittest.TestCase):
    def setUp(self):
        self.catalogue, self.catalogue_sha = load_object(
            ROOT / "checks/institutional/defaults.json"
        )

    def test_our_public_official_reference_list_is_fixed_and_unique(self):
        rows = validate_official(self.catalogue)
        self.assertEqual({item["id"] for item in rows}, set(OFFICIAL))
        self.assertEqual(len(rows), 6)
        for row in rows:
            self.assertTrue(row["public_probe_url"].startswith("https://"))

    def test_upstream_endpoint_redirection_and_single_run_can_never_prove_registration(self):
        report = institutional_report(
            self.catalogue, self.catalogue_sha,
            live=True, probe=lambda _: {"result": "HTTP_REDIRECT", "http_status": 302}
        )
        self.assertEqual(report["mode"], "PUBLIC_HTTP_READ_ONLY")
        self.assertEqual({x["observation"]["http_status"] for x in report["checks"]}, {302})
        self.assertTrue(any("registration" in item for item in report["non_claims"]))
        self.assertNotIn("status", report)

    def test_network_failures_are_inconclusive_not_official_outages(self):
        report = institutional_report(
            self.catalogue, self.catalogue_sha,
            live=True, probe=lambda _: {"result": "INCONCLUSIVE_NETWORK", "error_type": "TimeoutError"}
        )
        self.assertEqual(report["inconclusive_count"], 6)
        self.assertNotIn("FAIL", json.dumps(report))
        self.assertEqual(
            institutional_report(self.catalogue, self.catalogue_sha)["mode"],
            "OFFLINE_CONTRACT_ONLY",
        )

    def test_unreviewed_official_endpoint_or_extra_service_fails_closed(self):
        bad = copy.deepcopy(self.catalogue)
        bad["services"][0]["public_probe_url"] = "https://evil.example/"
        with self.assertRaisesRegex(ValueError, "URL mismatch"):
            validate_official(bad)
        bad = copy.deepcopy(self.catalogue)
        bad["services"].append(copy.deepcopy(bad["services"][0]))
        with self.assertRaises(ValueError):
            validate_official(bad)

    def test_official_catalogue_cannot_claim_fabricated_approval_or_extra_fields(self):
        altered = copy.deepcopy(self.catalogue)
        altered["services"][0]["official_status"] = "CERTIFIED"
        with self.assertRaisesRegex(ValueError, "unknown institutional catalogue fields"):
            validate_official(altered)


if __name__ == "__main__":
    unittest.main()
