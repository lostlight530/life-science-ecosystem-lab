"""Offline falsifier for the date-scoped 684→711 GitHub Actions census.

Reconstruct immutable prior ID sets, validate source arithmetic and test the
current accepted state independently. No GitHub API, external Agent or writes.
"""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import re
import unittest

from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"


def read(name):
    return json.loads((PROV / name).read_text(encoding="utf-8"))


class Post684RunDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.origin = read("full-history-census-2026-10-31.json")
        cls.deltas = [
            read("post-598-to-614-observation-2026-10-31.json"),
            read("post-614-to-628-observation-2026-11-01.json"),
            read("post-628-to-640-observation-2026-11-02.json"),
            read("post-640-to-653-observation-2026-11-02.json"),
            read("post-653-to-673-observation-2026-11-03.json"),
            read("post-673-to-684-observation-2026-11-03.json"),
        ]
        cls.new = read("post-684-to-711-observation-2026-11-04.json")

    def test_exact_run_identity_union_preserves_all_prior_cutoffs(self):
        pieces = [[r[0] for r in self.origin["actions"]["records"]]]
        pieces.extend([[r[0] for r in d["new_runs"]] for d in self.deltas])
        pieces.append([r[0] for r in self.new["new_runs"]])
        self.assertEqual([len(p) for p in pieces],
                         [598, 16, 14, 12, 13, 20, 11, 27])
        flattened = [id_ for p in pieces for id_ in p]
        self.assertEqual(len(flattened), 711)
        self.assertEqual(len(flattened), len(set(flattened)))
        self.assertEqual(len(flattened) - len(pieces[-1]), 684)
        self.assertEqual(self.new["previous_id_count_retained"], 684)
        self.assertEqual(self.new["previous_ids_absent"], [])
        self.assertEqual(self.new["page_counts"], [100] * 7 + [11])
        self.assertEqual(self.new["api_total_count"], 711)
        self.assertIsNone(self.new["exact_individual_api_request_timestamps_utc"])

    def test_run_grain_and_conditional_job_grain_are_distinct(self):
        d = self.new
        self.assertEqual(Counter(row[2] for row in d["new_runs"]),
                         Counter({"push": 16, "pull_request": 9,
                                  "schedule": 2}))
        self.assertEqual({row[5] for row in d["new_runs"]}, {"success"})
        self.assertEqual({row[6] for row in d["new_runs"]}, {1})
        self.assertEqual(d["new_conclusions"], {"success": 27})
        self.assertEqual(d["visible_conclusions"],
                         {"success": 670, "cancelled": 41, "failure": 0})
        self.assertEqual(d["visible_events"],
                         {"push": 364, "pull_request": 303,
                          "schedule": 40, "workflow_dispatch": 4})
        self.assertEqual(sum(d["visible_events"].values()), 711)
        self.assertEqual(sum(d["visible_conclusions"].values()), 711)
        j = d["new_job_census"]
        self.assertEqual((j["total"], j["success"], j["skipped"],
                          j["failure"], j["cancelled"]), (54, 51, 3, 0, 0))
        ids = {row[0] for row in d["new_runs"]}
        self.assertEqual(set(j["pinned_field_skipped_push_run_ids"]),
                         {41573113868, 41575989806, 41576421725})
        self.assertEqual(set(j["pinned_field_success_pr_run_ids"]),
                         {41573009904, 41575886687, 41576302737})
        self.assertTrue(set(j["pinned_field_skipped_push_run_ids"]) <= ids)
        self.assertTrue(set(j["pinned_field_success_pr_run_ids"]) <= ids)

    def test_scheduled_clock_differences_are_not_queue_duration_claims(self):
        d = self.new
        self.assertEqual(len(d["scheduled_delta"]), 2)
        self.assertEqual({x["run_id"] for x in d["scheduled_delta"]},
                         {41604262360, 41632276154})
        self.assertEqual(sum(len(x["jobs"]) for x in d["scheduled_delta"]), 3)
        self.assertEqual(sum(len(x["artifacts"]) for x in d["scheduled_delta"]), 3)
        for row in d["scheduled_delta"]:
            created = datetime.fromisoformat(row["created_at_utc"].replace("Z", "+00:00"))
            nominal = datetime.fromisoformat(row["nominal_cron_utc"].replace("Z", "+00:00"))
            self.assertEqual(int((created - nominal).total_seconds()),
                             row["cron_to_api_created_seconds"])
            self.assertTrue(all(job[2] == "success" for job in row["jobs"]))
            for artifact in row["artifacts"]:
                self.assertTrue(re.fullmatch("[0-9a-f]{64}",
                                             artifact["github_reported_zip_sha256"]))
        self.assertEqual(sorted(x["cron_to_api_created_seconds"]
                                for x in d["scheduled_delta"]), [24798, 27884])
        self.assertTrue(any("NOT runner queue time" in s
                            for s in d["observational_limits"]))

    def test_negative_history_and_accepted_production_are_not_conflated(self):
        d = self.new
        self.assertEqual(d["historical_negative"]["frozen_2026_10_30_failed_runs"], 8)
        self.assertEqual(d["historical_negative"]["cause_of_unavailable_runs"],
                         "UNKNOWN")
        self.assertEqual((d["native_state"]["accepted_receipts"],
                          d["native_state"]["linked_applied_events"],
                          d["native_state"]["candidate_archives"]), (4, 4, 3))
        events = [json.loads(line) for line in
                  (ROOT / "data/knowledge/events.jsonl")
                  .read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertGreaterEqual(len(events), 4)
        self.assertEqual([v["run_id"] for v in events[:4]], [
            "gh-38995485443-1", "gh-39227185707-1",
            "gh-40297059874-1", "gh-41436556408-1",
        ])
        receipts = list((ROOT / "data/receipts").glob("gh-*.json"))
        self.assertGreaterEqual(len(receipts), 4)
        self.assertTrue(verify_state(StateRoots(ROOT),
                                     require_accepted=True).valid)
        self.assertFalse(d["native_state"]["new_accepted_event_in_this_delta"])
        self.assertEqual(d["decision"]["scientific_status"],
                         "NO_NEW_VERIFIED_SCIENTIFIC_CLAIM")


if __name__ == "__main__":
    unittest.main()
