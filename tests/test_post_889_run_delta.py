"""Offline, non-live verification of the dated 889→915 Run and Job ledger.

Deliberately does not require current GitHub API populations, fixed live data/
cardinality, network, institutional services or any Agent runtime.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"
SOURCE = PROV / "post-889-to-915-observation-2026-11-20.json"
FROZEN = PROV / "post-868-to-889-observation-2026-11-17.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


class Post889To915EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = read(SOURCE)
        cls.old = read(FROZEN)

    def test_explicit_pinned_source_and_prior_archive(self):
        d = self.d
        self.assertEqual(d["kind"], "SOURCE_SCOPED_GITHUB_READ_ONLY_RECONCILIATION")
        self.assertEqual(d["source_main_sha"], "fe03f5bd935c0d64b90fb217feac40f0f15ce078")
        self.assertEqual(d["source_git_root_sha"], self.old["source_root_sha"])
        self.assertEqual(d["per_request_acquisition_timestamps"], None)
        self.assertEqual(d["prior_archive"], str(FROZEN.relative_to(ROOT)))
        self.assertEqual(d["review_logical_day_asia_shanghai"], "2026-11-20")

    def test_visible_set_math_and_frozen_failure_preservation(self):
        a = self.d["actions"]
        old = a["prior_frozen"]
        cur = a["current_visible"]
        failed = a["disappeared_historical_failure_run_ids"]
        observed_old = {
            run["id"] for run in self.old["actions"]["new_runs"]
            if run["conclusion"] == "failure"
        }
        self.assertEqual((old["visible"], cur["visible"]), (889, 915))
        self.assertEqual(old["visible"], self.old["actions"]["current_prewrite_visible"])
        self.assertEqual(old["conclusions"], {"success": 834, "cancelled": 51, "failure": 4})
        self.assertEqual(cur["conclusions"], {"success": 864, "cancelled": 51, "failure": 0})
        self.assertEqual(set(failed), observed_old)
        self.assertEqual(len(failed), 4)
        self.assertEqual(old["visible"] - len(failed) + a["additional_post_cutoff_run_count"], cur["visible"])
        self.assertEqual(sum(cur["conclusions"].values()), cur["visible"])
        self.assertEqual(sum(cur["events"].values()), cur["visible"])
        self.assertEqual(a["additional_events"], {"push": 15, "pull_request": 9, "schedule": 6})

    def test_new_run_and_latest_job_population(self):
        a = self.d["actions"]
        runs = a["new_runs"]
        ids = [r["id"] for r in runs]
        jobs = [j for run in runs for j in run["jobs"]]
        self.assertEqual((len(runs), len(set(ids))), (30, 30))
        self.assertEqual(Counter(r["event"] for r in runs), a["additional_events"])
        self.assertEqual(Counter(r["conclusion"] for r in runs), {"success": 30})
        self.assertEqual(Counter(j["conclusion"] for j in jobs), {"success": 62, "skipped": 1})
        self.assertEqual(len(jobs), a["additional_latest_attempt_job_count"])
        self.assertEqual(len({j["id"] for j in jobs}), len(jobs))
        self.assertEqual(a["additional_latest_attempt_job_conclusions"], dict(Counter(j["conclusion"] for j in jobs)))
        prior_ids = set(self.old["actions"]["new_runs"][i]["id"] for i in range(len(self.old["actions"]["new_runs"])))
        self.assertFalse(prior_ids.intersection(ids))
        self.assertFalse(set(a["disappeared_historical_failure_run_ids"]).intersection(ids))
        self.assertTrue(all(r["created_at_utc"] > self.old["latest_included_run_created_at_utc"] for r in runs))
        self.assertTrue(all(r["created_at_utc"] <= self.d["latest_included_run_created_at_utc"] for r in runs))
        self.assertEqual([j["id"] for j in jobs if j["conclusion"] == "skipped"], [133728607991])

    def test_schedule_jobs_and_clocks_are_not_provider_latency(self):
        s = self.d["schedules"]
        v = s["current_visible"]
        groups = v["by_workflow"]
        self.assertEqual((v["scheduled_runs"], sum(k["runs"] for k in groups.values())), (76, 76))
        self.assertEqual(sum(k["jobs"] for k in groups.values()), 118)
        self.assertEqual(v["latest_attempt_job_conclusions"], {"success": 118})
        self.assertEqual(s["prior_frozen"]["scheduled_runs"], 70)
        self.assertEqual(len(s["new_scheduled_runs"]), 6)
        self.assertEqual({x["run_id"] for x in s["new_scheduled_runs"]},
                         {r["id"] for r in self.d["actions"]["new_runs"] if r["event"] == "schedule"})
        for r in s["new_scheduled_runs"]:
            hh, mm, ss = map(int, r["scheduled_clock_utc"].split(":"))
            date = datetime.fromisoformat(r["actual_created_at_utc"].replace("Z", "+00:00"))
            expected = date.replace(hour=hh, minute=mm, second=ss, microsecond=0)
            interval = int((date - expected).total_seconds())
            hours, rem = divmod(interval, 3600)
            mins, sec = divmod(rem, 60)
            self.assertEqual(r["nominal_to_created_gap"], f"{hours:02}:{mins:02}:{sec:02}")
            self.assertGreaterEqual(interval, 0)
        self.assertIn("UNKNOWN", s["nominal_to_created_offset_cause"])

    def test_git_and_accepted_state_are_separate_counts(self):
        g = self.d["git"]
        self.assertEqual((g["main_reachable_commits"], g["distinct_git_trees"], g["current_tracked_blob_paths"]), (317, 289, 343))
        self.assertEqual((g["previous_source_commits"], g["previous_source_unique_trees"], g["previous_source_tracked_paths"]), (302, 276, 339))
        self.assertEqual(g["pull_requests"], {"total": 81, "merged": 77, "closed_unmerged": [29, 32, 67, 78], "open": []})
        self.assertEqual(g["release_tags"], ["v0.4.0", "v0.5.0", "v0.5.1"])
        accepted = self.d["accepted_state"]
        self.assertEqual((accepted["receipts"], accepted["chained_events"], accepted["previous_candidate_archives"]), (6, 6, 5))
        self.assertEqual((accepted["graph_entities"], accepted["graph_relations"]), (17, 26))
        self.assertEqual(accepted["latest_change_kind"], "DOCUMENT_TEXT_UNCHANGED")
        self.assertEqual(accepted["verified_new_scientific_discoveries"], 0)

    def test_negative_controls_and_public_privacy(self):
        cases = {r["run_id"]: r for r in self.d["negative_controls"]}
        self.assertEqual(cases[43210854941]["job_conclusion"], "failure")
        self.assertEqual(cases[43210854941]["parent_conclusion"], "cancelled")
        self.assertEqual(cases[43266573648]["job_conclusion"], "skipped")
        self.assertEqual(cases[43266573648]["parent_conclusion"], "success")
        self.assertEqual(cases[43990225775]["job_id"], 133728607991)
        self.assertEqual(len(self.d["actions"]["disappeared_historical_failure_run_ids"]), 4)
        report = (PROV / "POST_889_TO_915_RECONCILIATION_2026-11-20.md").read_text(encoding="utf-8")
        self.assertIn("404", report)
        self.assertIn("UNKNOWN", report)
        self.assertNotIn("personally deleted", report.lower())


if __name__ == "__main__":
    unittest.main()
