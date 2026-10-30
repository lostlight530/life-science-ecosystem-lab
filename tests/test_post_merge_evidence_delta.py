"""Offline, source-bound regressions for the add-only Oct 30 GitHub census."""
import json
import statistics
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "docs" / "provenance"

def load(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))

class PostMergeObservation(unittest.TestCase):
    def test_run_id_partition_and_snapshot_denominator(self):
        old = load("actions-visible-index-2026-10-30.json")
        new = load("post-merge-observation-2026-10-30.json")
        old_ids = {row[0] for row in old["records"]}
        added = new["new_run_records"]
        new_ids = {row["id"] for row in added}
        self.assertEqual(len(old_ids), 531)
        self.assertEqual(len(added), 16)
        self.assertEqual(len(new_ids), 16)
        self.assertFalse(old_ids & new_ids)
        self.assertEqual(new["current_count"], new["earlier_count"] + new["new_count"])
        self.assertEqual(sum(new["current_conclusions"].values()), 547)
        self.assertEqual(sum(new["current_events"].values()), 547)
        self.assertEqual(new["current_conclusions"], {"success": 506, "cancelled": 41})
        self.assertEqual(new["current_events"]["schedule"], 28)
        self.assertEqual(new["previous_ids_absent"], [])
        self.assertEqual(new["previous_id_event_or_outcome_changes"], [])
        self.assertEqual({row["conclusion"] for row in added}, {"success"})
        self.assertTrue(all(row["event"] in {"push", "pull_request"} for row in added))

    def test_source_grade_medians_are_computed_not_copied(self):
        daily = load("native-daily-quality-2026-10-30.json")
        fix = load("native-quality-corrections-2026-10-30.json")
        grouped = {}
        for row in daily["scheduled_runs"]:
            grouped.setdefault(row["workflow"], []).append(row["offset_from_nominal_minutes"])
        self.assertEqual(sum(map(len, grouped.values())), 28)
        self.assertEqual(set(fix["groups"]), set(grouped))
        for name, values in grouped.items():
            stats = fix["groups"][name]
            self.assertEqual(stats["observed_count"], len(values))
            self.assertEqual(stats["old_published_median_minutes"],
                             daily["workflow_class_summary"][name]["observed_offset_median"])
            self.assertAlmostEqual(stats["corrected_median_minutes"],
                                   statistics.median(values), places=2)
        self.assertEqual(fix["groups"]["Life Science Knowledge Workflow — Native Lifecycle"]["corrected_median_minutes"], 342.01)
        self.assertEqual(fix["groups"]["Daily research self-check — Institutional defaults and project custom"]["corrected_median_minutes"], 302.41)
        self.assertTrue(fix["original_source_unchanged"])

    def test_skipped_field_job_is_not_completed_field_evidence(self):
        snapshot = load("post-merge-observation-2026-10-30.json")
        jobs = snapshot["last_main_push_job_sample"]["40983926830"]
        self.assertIn({"name": "offline", "conclusion": "success"}, jobs)
        self.assertIn({"name": "pinned-field", "conclusion": "skipped"}, jobs)

if __name__ == "__main__":
    unittest.main()
