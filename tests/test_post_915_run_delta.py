"""Source-cutoff and offline regression: 2026-11-22 native Runs, Jobs and scientific nonclaims."""
from collections import Counter
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"
SOURCE = PROV / "post-915-to-932-observation-2026-11-22.json"
PRIOR = PROV / "post-889-to-915-observation-2026-11-20.json"

class Post915To932Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.p = json.loads(PRIOR.read_text(encoding="utf-8"))

    def test_pinned_provenance_not_live_population(self):
        d = self.d
        self.assertEqual(d["kind"], "SOURCE_SCOPED_GITHUB_READ_ONLY_RECONCILIATION")
        self.assertEqual(d["source_main_sha"], "36cd0b14a8d0dd13fd36a506be2d85e6e500c79f")
        self.assertEqual(d["prior_archive"], str(PRIOR.relative_to(ROOT)))
        self.assertIsNone(d["per_request_acquisition_timestamps"])
        self.assertFalse(d["acquisition_scope"]["exact_run_id_set_reconciliation_to_prior_archive"])
        self.assertEqual(d["latest_included_run_created_at_utc"], "2026-11-22T12:40:38Z")

    def test_run_and_latest_attempt_job_identities(self):
        a = self.d["actions"]
        self.assertEqual(a["prior_visible"]["count"], self.p["actions"]["current_visible"]["visible"])
        self.assertEqual((a["prior_visible"]["count"], a["current_visible"]["count"]), (915, 932))
        self.assertEqual(a["visible_count_difference"], 17)
        self.assertEqual(a["current_visible"]["conclusions"], {"success": 881, "cancelled": 51, "failure": 0})
        self.assertEqual(sum(a["current_visible"]["conclusions"].values()), 932)
        self.assertEqual(sum(a["current_visible"]["events"].values()), 932)
        runs = a["new_runs"]
        self.assertEqual((len(runs), len({r["id"] for r in runs})), (17, 17))
        self.assertEqual(Counter(r["event"] for r in runs), {"push": 7, "pull_request": 3, "schedule": 7})
        self.assertEqual(Counter(r["conclusion"] for r in runs), {"success": 17})
        self.assertTrue(all(r["created_at_utc"] > self.p["latest_included_run_created_at_utc"] for r in runs))
        jobs = [j for r in runs for j in r["jobs"]]
        self.assertEqual((len(jobs), len({j["id"] for j in jobs})), (31, 31))
        self.assertEqual(Counter(j["conclusion"] for j in jobs), {"success": 30, "skipped": 1})
        self.assertEqual([j["id"] for j in jobs if j["conclusion"] == "skipped"], [136079944159])

    def test_schedules_and_clock_boundary(self):
        s = self.d["schedules"]
        self.assertEqual((s["prior_visible_scheduled_runs"], s["current_visible_scheduled_runs"]), (76, 83))
        self.assertEqual(s["post_cutoff_schedule_run_count"], 7)
        self.assertEqual(s["post_cutoff_schedule_latest_attempt_job_conclusions"], {"success": 11})
        self.assertEqual(len(s["post_cutoff_created_clock_witness"]), 7)
        self.assertEqual({r["run_id"] for r in s["post_cutoff_created_clock_witness"]},
                         {r["id"] for r in self.d["actions"]["new_runs"] if r["event"] == "schedule"})
        self.assertIn("not scheduler queue latency", s["nominal_to_created_offset_cause"])

    def test_reconstructed_git_and_frozen_accepted_prefix(self):
        g, a = self.d["git"], self.d["accepted_state"]
        self.assertEqual((g["main_reachable_commits"], g["tracked_blob_paths"], g["current_recursive_tree_entries"]), (325, 347, 398))
        self.assertEqual(g["pull_requests"], {"total": 82, "merged": 78, "closed_unmerged": [29, 32, 67, 78], "open": []})
        self.assertEqual((a["event_count_at_source_main"], a["receipt_count"], a["previous_candidate_archives"]), (6, 6, 5))
        self.assertEqual(a["last_execution_id"], "gh-43859884737-1")
        self.assertEqual((a["graph_entities"], a["graph_relations"], a["new_scientific_discoveries_verified"]), (17, 26, 0))
        events = [json.loads(s) for s in (ROOT / "data/knowledge/events.jsonl").read_text(encoding="utf-8").splitlines() if s]
        self.assertGreaterEqual(len(events), 6)
        self.assertEqual([e["run_id"] for e in events[:6]], a["accepted_execution_ids"])
        self.assertTrue(all(events[i]["previous_event_sha256"] == events[i-1]["event_sha256"] for i in range(1, 6)))

    def test_failure_identity_retained_without_attribution(self):
        n = self.d["negative_controls"]
        self.assertEqual(n["prior_archived_failure_run_ids"], [43919536363, 43919549660, 43919549686, 43919549907])
        self.assertIn("UNKNOWN", n["current_individual_get_status_for_each"])
        self.assertEqual(n["new_bio_push_skipped_pinned_field_job"], 136079944159)
        report=(PROV / "POST_915_TO_932_RECONCILIATION_2026-11-22.md").read_text(encoding="utf-8")
        self.assertIn("UNKNOWN", report)
        self.assertIn("30 success and 1 skipped", report)
        self.assertNotIn("personally deleted", report.lower())

if __name__ == "__main__":
    unittest.main()
