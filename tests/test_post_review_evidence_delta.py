"""Offline replay for 2026-10-31 observed GitHub Actions population.

Source-specific structural test only; never fetches network, executes domain science
or mutates approved Knowledge. Frozen historic negative cases remain preserved.
"""
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "provenance"

def read(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))

class PostReviewDeltaReplay(unittest.TestCase):
    def test_exact_population_and_negative_history(self):
        idx = read("actions-visible-index-2026-10-30.json")
        mid = read("post-merge-observation-2026-10-30.json")
        last = read("post-schedule-observation-2026-10-30.json")
        new = read("post-review-observation-2026-10-31.json")
        raw_failure = read("action-runs-2026-10-30.json")
        population = {}
        for rid, workflow_id, event_code, created, status_code in idx["records"]:
            self.assertNotIn(rid, population)
            population[rid] = {
                "event": idx["event_codes"][event_code],
                "conclusion": idx["conclusion_codes"][status_code],
            }
        self.assertEqual(len(population), 531)
        for delta, expected_old, expected_new in ((mid, 531, 547),
                                                   (last, 547, 563),
                                                   (new, 563, 587)):
            self.assertEqual(len(population), expected_old)
            self.assertEqual(delta["new_count"], expected_new - expected_old)
            ids = [x["id"] for x in delta["new_run_records"]]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertFalse(set(ids) & set(population))
            for x in delta["new_run_records"]:
                self.assertEqual(x["conclusion"], "success")
                self.assertEqual(len(x["head_sha"]), 40)
                self.assertEqual(x["attempt"], 1)
                population[x["id"]] = x
            self.assertEqual(len(population), expected_new)
        self.assertEqual(new["previous_count"], 563)
        self.assertEqual(new["current_count"], 587)
        self.assertEqual(new["old_run_ids_missing"], [])
        self.assertEqual(new["old_run_event_or_conclusion_changes"], [])
        self.assertEqual(new["page_lengths"], [100,100,100,100,100,87])
        self.assertEqual(len(new["source_urls"]), 6)
        self.assertEqual(Counter(x["event"] for x in population.values()),
                         new["current_events"])
        self.assertEqual(Counter(x["conclusion"] for x in population.values()),
                         new["current_conclusions"])
        self.assertEqual(new["current_conclusions"], {"success":546,"cancelled":41})
        self.assertEqual(new["current_events"]["schedule"], 31)
        self.assertEqual(Counter(x["event"] for x in new["new_run_records"]),
                         {"push":16,"pull_request":8})
        historical_failures = [v["id"] for v in raw_failure["records"]
                               if v["conclusion"] == "failure"]
        self.assertEqual(len(historical_failures), 8)
        self.assertTrue(set(historical_failures).isdisjoint(population))
        self.assertIsNone(new["observed_at_utc"])
        self.assertEqual(new["scientific_status"], "NO_NEW_SCIENTIFIC_CLAIM")
        self.assertEqual(new["production_status"], "NO_CHANGE_REQUIRED")

    def test_production_is_independent_of_run_count(self):
        new = read("post-review-observation-2026-10-31.json")
        self.assertEqual(len(new["accepted_production_receipts"]), 3)
        for p in new["accepted_production_receipts"]:
            receipt = json.loads((ROOT / p).read_text(encoding="utf-8"))
            self.assertEqual(receipt["outcome"], "APPLIED")
        self.assertEqual(new["scheduled_jobs_independently_rechecked"]["scheduled_runs"], 31)
        self.assertEqual(new["scheduled_jobs_independently_rechecked"]["successful_jobs"], 48)
        self.assertEqual(sum(new["scheduled_jobs_independently_rechecked"]["job_classes"].values()), 48)
        self.assertEqual(new["repository_pre_pr"]["main_reachable_commits"], 241)
        self.assertEqual(new["repository_pre_pr"]["pr_merged"], 47)
        self.assertEqual(new["repository_pre_pr"]["pr_closed_not_merged"], [29,32])

if __name__ == "__main__":
    unittest.main()
