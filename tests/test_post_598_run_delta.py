"""Offline consistency check for the add-only 598 -> 614 GitHub observation.

This validates archived objects and our documented transformation, not the live API.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "docs/provenance/full-history-census-2026-10-31.json"
NEW = ROOT / "docs/provenance/post-598-to-614-observation-2026-10-31.json"


class Post598RunDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.previous = json.loads(OLD.read_text(encoding="utf-8"))
        cls.current = json.loads(NEW.read_text(encoding="utf-8"))

    def test_exact_additive_identity_and_denominator(self):
        previous_ids = [r[0] for r in self.previous["actions"]["records"]]
        added = self.current["new_runs"]
        added_ids = [r[0] for r in added]
        self.assertEqual(len(previous_ids), 598)
        self.assertEqual(len(previous_ids), len(set(previous_ids)))
        self.assertEqual(len(added), 16)
        self.assertEqual(len(added_ids), len(set(added_ids)))
        self.assertFalse(set(previous_ids) & set(added_ids))
        self.assertEqual(self.current["old_count"], self.previous["actions"]["total"])
        self.assertEqual(self.current["retained_old_ids"], 598)
        self.assertEqual(self.current["missing_old_ids"], [])
        self.assertEqual(self.current["changed_old_identity_fields"], [])
        self.assertEqual(self.current["page_counts"], [100] * 6 + [14])
        self.assertEqual(self.current["api_total_count"], len(set(previous_ids + added_ids)))

    def test_consistent_events_and_results(self):
        from collections import Counter
        self.assertEqual(Counter(x[2] for x in self.current["new_runs"]),
                         Counter({"push": 11, "pull_request": 3, "schedule": 2}))
        self.assertEqual(self.previous["actions"]["conclusions"]["success"] + 16,
                         self.current["visible_conclusions"]["success"])
        self.assertEqual(self.previous["actions"]["conclusions"]["cancelled"],
                         self.current["visible_conclusions"]["cancelled"])
        self.assertEqual(self.current["visible_conclusions"]["failure"], 0)
        self.assertEqual(sum(self.current["visible_events"].values()), 614)
        self.assertEqual(sum(self.current["visible_conclusions"].values()), 614)
        self.assertEqual(self.current["new_run_fields_common"]["conclusion"], "success")

    def test_native_jobs_and_unchanged_production(self):
        a = self.current["visible_scheduled_by_workflow"]
        self.assertEqual(sum(a.values()), 33)
        self.assertEqual(a["life-science-continuity.yml"] +
                         2 * a["life-science-daily-selfcheck.yml"] +
                         2 * a["life-science-knowledge.yml"] +
                         2 * a["life-science-bio.yml"], 51)
        self.assertEqual(self.current["visible_scheduled_job_status"]["successful_jobs"], 51)
        self.assertEqual({i["run_id"] for i in self.current["new_scheduled_jobs"]},
                         {41180826289, 41192786481})
        self.assertEqual(self.current["accepted_state_reconciliation"]["new_applied_receipts"], 0)
        receipts = list((ROOT / "data/receipts").glob("gh-*.json"))
        events = (ROOT / "data/knowledge/events.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(receipts), 3)
        self.assertEqual(len(events), 3)
        for event in events:
            self.assertEqual(json.loads(event)["outcome"], "APPLIED")
        self.assertEqual(self.current["historical_negative"]["original_frozen_failed_runs"], 8)
        self.assertEqual(self.current["decision"]["software"], "NO_CHANGE_REQUIRED")


if __name__ == "__main__":
    unittest.main()
