"""Offline exact-identity check for the 758→768 audit and closed PR boundary."""
import json
from collections import Counter
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"
DATA = PROV / "post-758-to-768-observation-2026-11-07.json"
PREV = PROV / "post-750-to-758-observation-2026-11-06.json"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

class Post758RunDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.new = read(DATA)
        cls.prev = read(PREV)

    def test_exact_identity_set_and_conclusions(self):
        prior = self.prev["action_census"]["current_visible_run_ids"]
        a = self.new["action_census"]
        runs = a["new_runs"]
        expected = {42201128815, 42201172569, 42201172659, 42201172853,
                    42201309805, 42201309921, 42201310035, 42215956253,
                    42249767693, 42251678739}
        self.assertEqual((len(prior), len(set(prior))), (758, 758))
        ids = [r["id"] for r in runs]
        self.assertEqual(set(ids), expected)
        self.assertEqual(len(ids), len(expected))
        self.assertTrue(expected.isdisjoint(prior))
        self.assertEqual(len(set(prior) | expected), 768)
        self.assertEqual((a["previous_visible"], a["retained_prior_ids"],
                          a["new_count"], a["current_visible"]), (758, 758, 10, 768))
        self.assertEqual(a["missing_prior_ids"], [])
        self.assertEqual(a["source_page_counts"], [100] * 7 + [68])
        self.assertEqual(a["current_conclusions"], {"success": 727, "cancelled": 41})
        self.assertEqual(a["current_events"], {"push": 396, "pull_request": 321,
                                               "schedule": 47, "workflow_dispatch": 4})
        self.assertEqual(Counter(r["event"] for r in runs),
                         {"push": 6, "pull_request": 3, "schedule": 1})
        self.assertTrue(all(r["conclusion"] == "success" and r["attempt"] == 1 for r in runs))

    def test_jobs_and_native_receipt_disposition(self):
        a = self.new["action_census"]
        jobs = [j for r in a["new_runs"] for j in r["jobs"]]
        self.assertEqual(len(jobs), 20)
        self.assertEqual(len({j["id"] for j in jobs}), 20)
        self.assertEqual(Counter(j["conclusion"] for j in jobs),
                         {"success": 19, "skipped": 1})
        self.assertEqual(a["new_run_jobs"],
                         {"count": 20, "success": 19, "skipped": 1, "failed": 0})
        skip = [r["id"] for r in a["new_runs"]
                if any(j["conclusion"] == "skipped" for j in r["jobs"])]
        self.assertEqual(skip, [42201310035])
        s = self.new["schedule"]
        self.assertEqual((s["prior_verified_runs"], s["prior_verified_success_jobs"],
                          s["current_visible_runs"], s["cross_cutoff_success_jobs"]),
                         (46, 72, 47, 73))
        self.assertEqual(s["nominal_to_created_seconds"], 28559)
        n = self.new["accepted_state"]
        self.assertEqual((n["receipts"], n["chained_events"], n["archived_candidates"]),
                         (4, 4, 3))
        self.assertFalse(n["new_production_acceptance"])
        # Four receipts/events describe this frozen cutoff, not a permanent cap.
        self.assertGreaterEqual(len(list((ROOT / "data" / "receipts").glob("gh-*.json"))), 4)
        events = (ROOT / "data" / "knowledge" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertGreaterEqual(len(events), 4)
        self.assertEqual([json.loads(line)["run_id"] for line in events[:4]],
                         ["gh-38995485443-1", "gh-39227185707-1",
                          "gh-40297059874-1", "gh-41436556408-1"])

    def test_unmerged_branch_not_promoted_and_docs_tracked(self):
        g = self.new["governance"]
        self.assertEqual(g["closed_unmerged_prs"] if "closed_unmerged_prs" in g
                         else self.new["git_scope"]["closed_unmerged_prs"],
                         [29, 32, 67])
        self.assertTrue(g["pr66"]["merged"])
        self.assertFalse(g["pr67"]["merged"])
        self.assertEqual(g["pr67"]["state"], "closed")
        self.assertEqual(g["pr67"]["closure_reason"], "UNKNOWN")
        self.assertFalse((ROOT / "docs" / "registration").exists())
        docs = set(read(ROOT / "evidence" / "profiles" / "docs.json")["documents"])
        for name in ("docs/provenance/POST_758_TO_768_RECONCILIATION_2026-11-07.md",
                     "docs/lessons/2026-11-07-closed-branch-is-not-main-acceptance.md"):
            self.assertIn(name, docs)
            self.assertTrue((ROOT / name).is_file())

if __name__ == "__main__":
    unittest.main()
