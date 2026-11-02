"""Offline, read-only 598 + 16 + 14 GitHub observation reconciliation.

Checks the archived observations, not the live API or scientific validity.
"""
from collections import Counter
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT / "docs" / "provenance"


def read_json(name):
    return json.loads((PROVENANCE / name).read_text(encoding="utf-8"))


class Post614RunDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = read_json("full-history-census-2026-10-31.json")
        cls.prior = read_json("post-598-to-614-observation-2026-10-31.json")
        cls.latest = read_json("post-614-to-628-observation-2026-11-01.json")

    def test_identity_union_and_pagination(self):
        original = [row[0] for row in self.root["actions"]["records"]]
        first_delta = [row[0] for row in self.prior["new_runs"]]
        second_delta = [row[0] for row in self.latest["new_runs"]]
        self.assertEqual((len(original), len(first_delta), len(second_delta)), (598, 16, 14))
        self.assertEqual(len(set(original + first_delta + second_delta)), 628)
        self.assertEqual(self.latest["old_count"], self.prior["api_total_count"])
        self.assertEqual(self.latest["retained_old_ids"], 614)
        self.assertEqual(self.latest["missing_old_ids"], [])
        self.assertEqual(self.latest["page_counts"], [100] * 6 + [28])
        self.assertEqual(sum(self.latest["page_counts"]), self.latest["api_total_count"])
        self.assertEqual(self.latest["observed_reference_main"],
                         "3afea285b3660f9482c935c13160705eecfb332a")
        self.assertIsNone(self.latest["exact_request_timestamp_utc"])

    def test_exact_new_run_identity_and_outcomes(self):
        rows = self.latest["new_runs"]
        self.assertEqual(self.latest["new_count"], len(rows))
        self.assertEqual(Counter(row[2] for row in rows),
                         Counter({"push": 9, "pull_request": 3, "schedule": 2}))
        self.assertEqual({row[5] for row in rows}, {"success"})
        self.assertEqual({row[0] for row in rows if row[2] == "schedule"},
                         {41287694940, 41301526739})
        self.assertEqual(len({row[0] for row in rows}), len(rows))
        self.assertTrue(all(row[3].endswith("Z") and len(row[4]) == 40 for row in rows))
        self.assertEqual(self.latest["visible_conclusions"],
                         {"success": 587, "cancelled": 41, "failure": 0})
        self.assertEqual(self.latest["visible_events"],
                         {"push": 310, "pull_request": 279, "schedule": 35, "workflow_dispatch": 4})
        self.assertEqual(sum(self.latest["visible_conclusions"].values()), 628)
        self.assertEqual(sum(self.latest["visible_events"].values()), 628)

    def test_native_jobs_artifacts_and_replay_boundary(self):
        schedule = self.latest["native_schedule"]
        by = schedule["by_workflow"]
        self.assertEqual(sum(by.values()), schedule["runs"])
        expected_jobs = (by["life-science-continuity.yml"]
                         + 2 * by["life-science-daily-selfcheck.yml"]
                         + 2 * by["life-science-knowledge.yml"]
                         + 2 * by["life-science-bio.yml"])
        self.assertEqual((schedule["runs"], schedule["jobs"], expected_jobs), (35, 54, 54))
        self.assertEqual(schedule["success_jobs"], expected_jobs)
        scheduled = self.latest["new_scheduled_runs"]
        self.assertEqual({x["run_id"] for x in scheduled}, {41287694940, 41301526739})
        self.assertEqual(sum(len(x["jobs"]) for x in scheduled), 3)
        artifact_ids = []
        for run in scheduled:
            for job in run["jobs"]:
                self.assertEqual(job["conclusion"], "success")
                self.assertEqual(len(job["artifact_sha256"]), 64)
                artifact_ids.append(job["artifact_id"])
        self.assertEqual(set(artifact_ids), {13076345169, 13075767738, 13080969938})
        receipts = list((ROOT / "data" / "receipts").glob("gh-*.json"))
        events = (ROOT / "data" / "knowledge" / "events.jsonl").read_text(
            encoding="utf-8").splitlines()
        # The 628-Run observation has three accepted events at its cutoff;
        # later native production must not invalidate the frozen record.
        self.assertGreaterEqual(len(receipts), 3)
        self.assertGreaterEqual(len(events), 3)
        self.assertEqual([json.loads(s)["run_id"] for s in events[:3]],
                         ["gh-38995485443-1", "gh-39227185707-1",
                          "gh-40297059874-1"])
        self.assertTrue(all(json.loads(e)["outcome"] == "APPLIED" for e in events))
        self.assertEqual(self.latest["accepted_reconciliation"]["new_applied_receipts"], 0)

    def test_negative_evidence_release_and_uncertainty(self):
        self.assertEqual(self.latest["historical_negative"]["old_frozen_failed_runs"], 8)
        self.assertEqual(self.latest["historical_negative"]["old_temporal_run_name_corrections"], 134)
        self.assertEqual(self.latest["historical_negative"]["old_median_corrections"], 2)
        self.assertEqual(self.latest["repo_reconciliation"]["prs_closed_unmerged"], [29, 32])
        self.assertEqual(self.latest["repo_reconciliation"]["tracked_git_blobs"], 255)
        self.assertEqual(self.latest["repo_reconciliation"]["prs_total"], 52)
        release = self.latest["repo_reconciliation"]["releases"][-1]
        self.assertEqual(release["tag"], "v0.5.0")
        self.assertEqual(release["source_commit"], self.latest["observed_reference_main"])
        self.assertEqual(self.latest["runner_timestamp_observation"]["causal_explanation"],
                         "UNKNOWN")
        self.assertEqual(self.latest["decision"]["production_data"], "NO_CHANGE_REQUIRED")
        self.assertEqual(self.latest["decision"]["scientific_claim"],
                         "NO_NEW_VERIFIED_CLAIM")


if __name__ == "__main__":
    unittest.main()
