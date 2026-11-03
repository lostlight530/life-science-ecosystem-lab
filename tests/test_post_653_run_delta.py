"""Offline falsifier for the frozen 653→673 GitHub Run census.

The snapshot is historical evidence, not a mutable target for production.
Native state verification is performed separately against the actual data/.
"""
from collections import Counter
import json
from pathlib import Path
import unittest

from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT / "docs" / "provenance"


def read(name):
    return json.loads((PROVENANCE / name).read_text(encoding="utf-8"))


class Post653RunDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.origin = read("full-history-census-2026-10-31.json")
        cls.deltas = [
            read("post-598-to-614-observation-2026-10-31.json"),
            read("post-614-to-628-observation-2026-11-01.json"),
            read("post-628-to-640-observation-2026-11-02.json"),
            read("post-640-to-653-observation-2026-11-02.json"),
        ]
        cls.current = read("post-653-to-673-observation-2026-11-03.json")

    def test_exact_prior_identity_and_additive_population(self):
        origin_ids = [r[0] for r in self.origin["actions"]["records"]]
        delta_ids = [[r[0] for r in d["new_runs"]] for d in self.deltas]
        current_ids = [r[0] for r in self.current["new_runs"]]
        self.assertEqual([len(origin_ids), *map(len, delta_ids),
                          len(current_ids)], [598, 16, 14, 12, 13, 20])
        previous = origin_ids + [i for batch in delta_ids for i in batch]
        self.assertEqual(len(previous), len(set(previous)))
        self.assertEqual(len(previous), 653)
        self.assertEqual(len(current_ids), len(set(current_ids)))
        self.assertFalse(set(previous) & set(current_ids))
        self.assertEqual(len(set(previous + current_ids)), 673)
        self.assertEqual(self.current["old_ids_retained"], 653)
        self.assertEqual(self.current["old_ids_missing"], [])
        self.assertEqual(self.current["page_counts"], [100] * 6 + [73])
        self.assertEqual(self.current["api_total_count"], 673)
        self.assertIsNone(self.current["exact_http_read_timestamp_utc"])

    def test_run_and_job_grain_are_independent(self):
        d = self.current
        self.assertEqual(Counter(x[2] for x in d["new_runs"]),
                         Counter({"push": 14, "pull_request": 6}))
        self.assertEqual({x[5] for x in d["new_runs"]}, {"success"})
        self.assertEqual(d["new_conclusions"], {"success": 20})
        self.assertEqual(d["visible_conclusions"],
                         {"success": 632, "cancelled": 41})
        self.assertEqual(d["visible_events"],
                         {"push": 340, "pull_request": 291,
                          "schedule": 38, "workflow_dispatch": 4})
        self.assertEqual(sum(d["visible_conclusions"].values()), 673)
        self.assertEqual(sum(d["visible_events"].values()), 673)
        self.assertEqual(d["jobs"]["new_run_jobs_checked"], 38)
        self.assertEqual(d["jobs"]["new_run_job_success"], 36)
        self.assertEqual(d["jobs"]["new_run_job_skipped"], 2)
        self.assertEqual(d["jobs"]["new_run_job_failed"], 0)
        self.assertEqual(d["jobs"]["new_main_bio_pinned_field"], "skipped")
        self.assertEqual(d["jobs"]["new_pr_bio_pinned_field"], "success")
        self.assertEqual(
            set(d["jobs"]["new_main_bio_push_ids"]),
            {41450087249, 41453175179},
        )

    def test_scheduled_jobs_and_main_history_count_at_this_cutoff(self):
        d = self.current
        schedule = d["scheduled_by_workflow"]
        self.assertEqual(schedule,
                         {"life-science-continuity.yml": 17,
                          "life-science-knowledge.yml": 3,
                          "life-science-daily-selfcheck.yml": 16,
                          "life-science-bio.yml": 2})
        self.assertEqual(sum(schedule.values()), 38)
        self.assertEqual(d["jobs"]["scheduled_jobs_checked"], 59)
        self.assertEqual(d["jobs"]["scheduled_job_success"], 59)
        old = self.deltas[-1]["repository_census"]
        new = d["repository_census"]
        self.assertEqual((new["main_reachable_commits"] -
                          old["main_reachable_commits"],
                          new["prs_total"] - old["prs_total"],
                          new["tracked_git_blobs"] - old["tracked_blobs"]),
                         (2, 2, 5))
        self.assertEqual(new["prs_closed_not_merged"], [29, 32])
        self.assertEqual(new["workflows"], 9)
        self.assertEqual(new["releases"], ["v0.4.0", "v0.5.0"])

    def test_historical_negative_evidence_and_unknowns_not_erased(self):
        d = self.current
        n = d["negative_evidence"]
        self.assertEqual(n["archived_2026_10_30_failed_runs"], 8)
        self.assertEqual(n["currently_visible_failed_runs"], 0)
        self.assertEqual(len(n["three_previously_documented_pr55_intermediate_failures"]), 3)
        self.assertEqual(n["direct_retry_of_these_three"], "404_NOT_FOUND")
        self.assertEqual(n["cause_or_removal_operator"], "UNKNOWN")
        self.assertEqual(n["november_1_api_runner_clock_conflict"], "UNRESOLVED")
        self.assertFalse(d["repository_census"]["branch_protection_enabled"])
        self.assertEqual(d["decision"]["observed_research_claims"],
                         "NO_NEW_VERIFIED_CLAIM")

    def test_actual_accepted_state_is_verified_separately_from_cutoff(self):
        d = self.current
        self.assertEqual(
            (d["production"]["accepted_receipts"],
             d["production"]["events"],
             d["production"]["archived_candidates"]),
            (4, 4, 3))
        events = [
            json.loads(line)
            for line in (ROOT / "data" / "knowledge" / "events.jsonl")
                .read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        expected = [38995485443, 39227185707, 40297059874, 41436556408]
        self.assertGreaterEqual(len(events), 4)
        self.assertEqual([x["run_id"] for x in events[:4]],
                         [f"gh-{x}-1" for x in expected])
        self.assertEqual(events[3]["change_kind"], "DOCUMENT_TEXT_UNCHANGED")
        report = verify_state(StateRoots(ROOT), require_accepted=True)
        self.assertTrue(report.valid, report.errors)


if __name__ == "__main__":
    unittest.main()
