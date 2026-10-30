"""Offline, read-only reconciliation of dated GitHub observations, not live authority.

Never replace either frozen snapshot with today's Actions list.
No API access, scientific inference, or production state writes.
"""
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "provenance"


def read(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


class ProvenanceObservationReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = read("action-runs-2026-10-30.json")
        cls.current = read("actions-visible-index-2026-10-30.json")
        cls.delta = read("action-run-reconciliation-2026-10-30.json")
        cls.history = read("history-delta-2026-10-30.json")
        cls.daily = read("native-daily-quality-2026-10-30.json")

    def test_two_observation_censuses_remain_independent(self):
        old = self.old["records"]
        now = self.current["records"]
        self.assertEqual(len(old), 531)
        self.assertEqual(len(now), 531)
        self.assertEqual(self.old["returned_count"], len(old))
        self.assertEqual(self.current["reported_total_count"], len(now))
        self.assertEqual(len({x["id"] for x in old}), len(old))
        self.assertEqual(len({x[0] for x in now}), len(now))
        self.assertNotEqual(
            self.old["observed_at_utc"], self.current["observed_at_utc"]
        )
        self.assertEqual(Counter(x["conclusion"] for x in old),
                         {"success": 483, "failure": 8, "cancelled": 40})
        self.assertEqual(
            Counter(self.current["conclusion_codes"][x[4]] for x in now),
            {"success": 490, "cancelled": 41},
        )

    def test_reconciliation_is_exact_set_difference(self):
        old = {x["id"] for x in self.old["records"]}
        now = {x[0] for x in self.current["records"]}
        missing = {x["id"] for x in self.delta["missing_from_later"]}
        added = {x["id"] for x in self.delta["added_in_later"]}
        self.assertEqual(missing, old - now)
        self.assertEqual(added, now - old)
        self.assertEqual(len(missing), 8)
        self.assertEqual(len(added), 8)
        self.assertTrue(all(x["conclusion"] == "failure"
                            for x in self.delta["missing_from_later"]))
        self.assertEqual(
            self.delta["later_observed_at_utc"],
            self.current["observed_at_utc"],
        )
        self.assertEqual(
            self.delta["earlier_observed_at_utc"],
            self.old["observed_at_utc"],
        )
        third = self.delta[
            "previous_session_observations_without_persisted_original_runner_log"
        ]
        self.assertEqual(len(third), 3)
        self.assertTrue(all(x["id"] not in old | now for x in third))
        self.assertTrue(all(x["source_grade"].startswith("PRIOR_")
                            for x in third))

    def test_scheduled_quality_recomputes_from_current_index(self):
        current_scheduled = {
            x[0] for x in self.current["records"]
            if self.current["event_codes"][x[2]] == "schedule"
        }
        scheduled = self.daily["scheduled_runs"]
        self.assertEqual(len(scheduled), 28)
        self.assertEqual(len({x["id"] for x in scheduled}), 28)
        self.assertEqual({x["id"] for x in scheduled}, current_scheduled)
        self.assertEqual(self.daily["scheduled_run_count"], 28)
        self.assertEqual(self.daily["scheduled_success_count"], 28)
        self.assertTrue(all(x["conclusion"] == "success" for x in scheduled))
        self.assertEqual(
            self.daily["observed_at_utc"],
            self.current["observed_at_utc"],
        )
        self.assertEqual(len(self.daily["daily_observation"]), 15)
        self.assertEqual(
            [x["day_asia_shanghai"] for x in self.daily["daily_observation"]],
            [f"2026-10-{i:02d}" for i in range(16, 31)],
        )
        day_ids = [run_id for day in self.daily["daily_observation"]
                   for run_id in day["scheduled_run_ids"]]
        self.assertEqual(Counter(day_ids),
                         Counter(x["id"] for x in scheduled))
        self.assertEqual(
            sum(day["scheduled_run_count"]
                for day in self.daily["daily_observation"]), 28
        )
        self.assertIn("PARTIAL_DAY", self.daily["daily_observation"][-1]["note"])

    def test_production_acceptance_is_not_daily_check_count(self):
        native = [x for x in self.current["records"]
                  if self.current["workflow_names"][str(x[1])]
                  == "Life Science Knowledge Workflow — Native Lifecycle"]
        self.assertEqual(len(native), 3)
        receipts = self.daily["accepted_native_execution_receipts"]
        self.assertEqual({x["run_id"] for x in receipts},
                         {x[0] for x in native})
        self.assertEqual(Counter(x["event"] for x in receipts),
                         {"schedule": 2, "workflow_dispatch": 1})
        for row in receipts:
            self.assertTrue((ROOT / row["receipt"]).is_file())

    def test_origin_to_latest_delta_is_not_backdated(self):
        self.assertEqual(self.history["previous_main_reachable_commits"], 234)
        self.assertEqual(self.history["current_main_reachable_commits"], 235)
        self.assertEqual(len(self.history["new_commits"]), 1)
        self.assertEqual(self.history["new_commits"][0]["sha"],
                         self.history["current_observed_main"])
        self.assertEqual(self.history["new_commits"][0]["parents"],
                         [self.history["previous_frozen_main"]])
        self.assertEqual(self.history["previous_pr_count"], 42)
        self.assertEqual(self.history["current_pr_count"], 43)
        self.assertEqual([x["number"] for x in self.history["new_prs"]], [43])
        self.assertEqual(self.history["total_pr_merged"], 41)
        self.assertEqual(self.history["total_pr_closed_without_merge"], 2)


if __name__ == "__main__":
    unittest.main()
