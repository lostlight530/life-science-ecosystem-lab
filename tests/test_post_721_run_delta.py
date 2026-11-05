"""Offline evidence test for 721-to-730 GitHub Action Run observations."""
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
import unittest
from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs/provenance"
def read(path):
    return json.loads(path.read_text(encoding="utf-8"))
class Post721RunDeltaTests(unittest.TestCase):
    def setUp(self):
        self.d = read(PROV / "post-721-to-730-observation-2026-11-05.json")
    def test_replay_source_population_and_new_ids(self):
        old = read(PROV / "full-history-census-2026-10-31.json")
        ids = [r[0] for r in old["actions"]["records"]]
        for filename in ("post-598-to-614-observation-2026-10-31.json",
                         "post-614-to-628-observation-2026-11-01.json",
                         "post-628-to-640-observation-2026-11-02.json",
                         "post-640-to-653-observation-2026-11-02.json",
                         "post-653-to-673-observation-2026-11-03.json",
                         "post-673-to-684-observation-2026-11-03.json",
                         "post-684-to-711-observation-2026-11-04.json"):
            ids += [r[0] for r in read(PROV / filename)["new_runs"]]
        overlay = read(ROOT / "docs/taxonomy/post-2026-11-04-source-classification.json")
        ids += [r[0] for r in overlay["actions"]["new_current_runs"]]
        self.assertEqual((len(ids), len(set(ids))), (721, 721))
        new = [r["run_id"] for r in self.d["new_runs"]]
        self.assertEqual((len(new), len(set(new))), (9, 9))
        self.assertFalse(set(ids) & set(new))
        self.assertEqual(self.d["previous_ids_retained"], 721)
        self.assertEqual(self.d["previous_ids_missing"], [])
        self.assertEqual(len(set(ids + new)), 730)
        self.assertEqual(self.d["page_counts"], [100]*7+[30])
    def test_job_counts_and_event_guard(self):
        d = self.d
        self.assertEqual(Counter(r["event"] for r in d["new_runs"]),
                         {"push":4,"pull_request":3,"schedule":2})
        self.assertEqual({r["conclusion"] for r in d["new_runs"]}, {"success"})
        jobs = [(r["run_id"],j) for r in d["new_runs"] for j in r["jobs"]]
        self.assertEqual(len(jobs),20)
        self.assertEqual(Counter(j["conclusion"] for _,j in jobs),
                         {"success":19,"skipped":1})
        self.assertEqual([r for r,j in jobs if j["conclusion"]=="skipped"],[41779069740])
        self.assertEqual(d["current_visible_conclusions"],
                         {"success":689,"cancelled":41,"failure":0})
        self.assertEqual(sum(d["current_visible_events"].values()),730)
    def test_scheduled_clock_and_negative_scope(self):
        d=self.d
        self.assertEqual({s["run_id"]:s["cron_to_created_seconds"]
                          for s in d["scheduled_observations"]},
                         {41796192635:22760,41827751347:28727})
        for s in d["scheduled_observations"]:
            created=datetime.fromisoformat(s["created_at_utc"].replace("Z","+00:00"))
            cron=datetime.fromisoformat(s["nominal_cron_utc"].replace("Z","+00:00"))
            self.assertEqual((created-cron).total_seconds(),s["cron_to_created_seconds"])
        self.assertEqual(len(d["scheduled_github_reported_artifacts"]),3)
        self.assertEqual(d["negative_evidence"]["explanation_for_404"],"UNKNOWN")
        self.assertEqual(d["negative_evidence"]["rechecked_api_404_run_ids"],
                         [41776345499,41776379847,41776461093])
    def test_accepted_state_and_public_docs(self):
        d=self.d
        self.assertEqual(d["main_history"]["main_reachable_parent_closed_commits"],255)
        self.assertEqual(d["main_history"]["prs_total"],62)
        self.assertEqual(d["main_history"]["tracked_blobs"],290)
        self.assertEqual(d["main_history"]["workflow_definitions"],9)
        self.assertFalse(d["accepted_state"]["new_apply"])
        self.assertEqual([d["accepted_state"][x] for x in ("receipts","events","archived_candidates")],
                         [4,4,3])
        self.assertTrue(verify_state(StateRoots(ROOT),require_accepted=True).valid)
        docs=read(ROOT / "evidence/profiles/docs.json")["documents"]
        self.assertIn("docs/provenance/POST_721_TO_730_RECONCILIATION_2026-11-05.md",docs)
        self.assertIn("docs/lessons/2026-11-05-cron-jobs-evidence-boundaries.md",docs)
if __name__=="__main__": unittest.main()
