"""Offline, immutable 807→849 GitHub Run/Job audit; no live writes or network."""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

class Post807NativeAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new = read(PROV / "post-807-to-849-observation-2026-11-13.json")
        cls.old = [
            read(PROV / p) for p in (
                "post-750-to-758-observation-2026-11-06.json",
                "post-758-to-768-observation-2026-11-07.json",
                "post-768-to-788-observation-2026-11-08.json",
                "post-788-to-798-observation-2026-11-09.json",
                "post-798-to-807-observation-2026-11-10.json")]

    def test_frozen_population_and_nonloss(self):
        older = list(self.old[0]["action_census"]["current_visible_run_ids"])
        for d in self.old[1:]:
            older.extend(x["id"] for x in d["action_census"]["new_runs"])
        a = self.new["actions"]
        added = [x["id"] for x in a["new_runs"]]
        visible = a["current_visible_run_ids"]
        self.assertEqual((len(older), len(set(older))), (807, 807))
        self.assertEqual((len(visible), len(set(visible))), (849, 849))
        self.assertEqual((len(added), len(set(added))), (42, 42))
        self.assertFalse(set(older) & set(added))
        self.assertEqual(set(visible), set(older) | set(added))
        self.assertEqual(a["missing_old_ids"], [])
        self.assertEqual(a["page_counts"], [100] * 8 + [49])
        self.assertEqual(a["current_conclusions"], {"success": 798, "cancelled": 51})
        self.assertEqual(a["current_events"],
                         {"schedule": 60, "push": 431, "pull_request": 354,
                          "workflow_dispatch": 4})

    def test_job_grain_and_failed_cancelled_parent(self):
        a = self.new["actions"]
        jobs = [j for x in a["new_runs"] for j in x["jobs"]]
        self.assertEqual(len(jobs), 103)
        self.assertEqual(len({j["id"] for j in jobs}), 103)
        expected = {"success": 73, "skipped": 3, "cancelled": 26, "failure": 1}
        self.assertEqual(dict(Counter(j["conclusion"] for j in jobs)), expected)
        self.assertEqual(a["new_job_conclusions"], expected)
        self.assertEqual(dict(Counter(x["conclusion"] for x in a["new_runs"])),
                         {"success": 32, "cancelled": 10})
        failed = next(x for x in a["new_runs"] if x["id"] == 43210854941)
        self.assertEqual(failed["conclusion"], "cancelled")
        self.assertEqual([(x["name"], x["conclusion"]) for x in failed["jobs"]
                          if x["conclusion"] == "failure"],
                         [("Repository contracts", "failure")])
        self.assertEqual(
            {(x["id"], j["name"]) for x in a["new_runs"] for j in x["jobs"]
             if j["conclusion"] == "skipped"},
            {(43214236784, "pinned-field"), (43212135222, "pinned-field"),
             (42839729320, "pinned-field")})

    def test_four_scheduled_jobs_and_clock_offsets(self):
        s = self.new["schedule"]["new_runs"]
        self.assertEqual(len(s), 4)
        for row in s:
            a = datetime.fromisoformat(row["created_utc"].replace("Z", "+00:00"))
            b = datetime.fromisoformat(row["nominal_utc"].replace("Z", "+00:00"))
            self.assertEqual(round((a - b).total_seconds()), row["offset_seconds"])
            r = next(x for x in self.new["actions"]["new_runs"] if x["id"] == row["id"])
            self.assertEqual(r["event"], "schedule")
            self.assertEqual([x["id"] for x in r["jobs"]],
                             [x["id"] for x in row["jobs"]])
            self.assertTrue(all(j["conclusion"] == "success" for j in row["jobs"]))
        self.assertEqual(self.new["schedule"]["offset_cause"], "UNKNOWN")

    def test_production_continuity_not_frozen_to_five(self):
        a = self.new["accepted_state"]
        self.assertEqual((a["receipts"], a["events"], a["archives"]), (5, 5, 4))
        self.assertEqual(a["new_accepted_writes"], 0)
        self.assertEqual(a["new_scientific_conclusions_verified"], 0)
        from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state
        result = verify_state(StateRoots(ROOT), require_accepted=True)
        self.assertTrue(result.valid, result.errors)
        receipts = list((ROOT / "data/receipts").glob("gh-*.json"))
        events = [json.loads(x) for x in
                  (ROOT / "data/knowledge/events.jsonl").read_text().splitlines() if x]
        self.assertGreaterEqual(len(receipts), 5)
        self.assertGreaterEqual(len(events), 5)
        self.assertEqual(events[4]["run_id"], "gh-42611716908-1")

    def test_public_docs_paths_registered(self):
        docs = set(read(ROOT / "evidence/profiles/docs.json")["documents"])
        for p in (
            "docs/provenance/POST_807_TO_849_RECONCILIATION_2026-11-13.md",
            "docs/lessons/2026-11-13-fail-closed-paths-and-cancelled-jobs.md",
        ):
            self.assertIn(p, docs)
            self.assertTrue((ROOT / p).is_file())

if __name__ == "__main__":
    unittest.main()
