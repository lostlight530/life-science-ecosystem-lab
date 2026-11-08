"""Offline falsifiers for the 768->788 observed Run/Job, clock and acceptance boundaries."""
from collections import Counter
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"
NEW = PROV / "post-768-to-788-observation-2026-11-08.json"
OLD = PROV / "post-758-to-768-observation-2026-11-07.json"
BASE = PROV / "post-750-to-758-observation-2026-11-06.json"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

class Post768AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a, cls.prev, cls.base = read(NEW), read(OLD), read(BASE)

    def test_lossless_ids_and_current_conclusion_scope(self):
        a = self.a["action_census"]
        baseline = self.base["action_census"]["current_visible_run_ids"]
        prior_new = [r["id"] for r in self.prev["action_census"]["new_runs"]]
        ids = [r["id"] for r in a["new_runs"]]
        expected = {
            42343672701, 42343769852, 42343772342,
            42343813706, 42343813682, 42343813651,
            42343880966, 42343880964, 42343880958,
            42352695753, 42366998260, 42368933925,
            42368938291, 42368938301, 42368938295,
            42369007585, 42369007482, 42369007432,
            42460920843, 42475429538
        }
        self.assertEqual(len(set(baseline)), 758)
        self.assertEqual(len(set(baseline + prior_new)), 768)
        self.assertEqual(set(ids), expected)
        self.assertEqual(len(ids), 20)
        self.assertTrue(set(ids).isdisjoint(baseline + prior_new))
        self.assertEqual(len(set(baseline + prior_new + ids)), 788)
        self.assertEqual((a["previous_visible"], a["retained_prior_ids"],
                          a["new_count"], a["current_visible"]), (768, 768, 20, 788))
        self.assertEqual(a["missing_prior_ids"], [])
        self.assertEqual(a["source_page_counts"], [100] * 7 + [88])
        self.assertEqual(a["current_conclusions"], {"success": 747, "cancelled": 41})
        self.assertEqual(a["current_events"],
                         {"schedule": 51, "push": 406, "pull_request": 327, "workflow_dispatch": 4})
        self.assertEqual(Counter(r["event"] for r in a["new_runs"]),
                         {"push": 10, "pull_request": 6, "schedule": 4})
        self.assertTrue(all(r["attempt"] == 1 and r["conclusion"] == "success"
                            and len(r["head_sha"]) == 40 for r in a["new_runs"]))

    def test_each_job_and_conditional_gate(self):
        rows = self.a["action_census"]["new_runs"]
        jobs = [j for r in rows for j in r["jobs"]]
        self.assertEqual(len(jobs), 42)
        self.assertEqual(len({j["id"] for j in jobs}), 42)
        self.assertEqual(Counter(j["conclusion"] for j in jobs),
                         {"success": 40, "skipped": 2})
        self.assertEqual(self.a["action_census"]["new_run_jobs"],
                         {"count": 42, "success": 40, "skipped": 2, "failed": 0})
        skipped = {r["id"] for r in rows if any(j["conclusion"] == "skipped"
                                               for j in r["jobs"])}
        self.assertEqual(skipped, {42343880958, 42369007585})
        for r in rows:
            if r["id"] in skipped:
                self.assertEqual(r["event"], "push")
                self.assertEqual(r["branch"], "main")
                self.assertEqual(next(j["name"] for j in r["jobs"]
                                      if j["conclusion"] == "skipped"), "pinned-field")

    def test_schedule_clocks_and_acceptance_are_not_claimed_from_ci(self):
        s = self.a["schedule"]
        self.assertEqual((s["prior_verified_runs"], s["prior_verified_success_jobs"],
                          s["current_visible_runs"], s["cross_cutoff_verified_success_jobs"]),
                         (47, 73, 51, 79))
        from datetime import datetime
        for r in s["new_scheduled_runs"]:
            self.assertEqual(int((datetime.fromisoformat(r["created_utc"].replace("Z","+00:00"))
                              - datetime.fromisoformat(r["nominal_utc"].replace("Z","+00:00")))
                                 .total_seconds()), r["offset_seconds"])
            match = next(x for x in self.a["action_census"]["new_runs"] if x["id"] == r["run_id"])
            self.assertEqual(match["event"], "schedule")
            self.assertEqual(len(match["jobs"]), len(r["job_ids"]))
            self.assertEqual({j["id"] for j in match["jobs"]}, set(r["job_ids"]))
            self.assertTrue(all(j["conclusion"] == "success" for j in match["jobs"]))
        self.assertEqual({r["offset_seconds"] for r in s["new_scheduled_runs"]},
                         {21953, 24765, 22637, 25501})
        a = self.a["accepted_state"]
        self.assertEqual((a["receipts"], a["chained_events"], a["archived_candidates"]),
                         (4, 4, 3))
        self.assertFalse(a["new_production_acceptance"])
        self.assertEqual(len(list((ROOT/"data/receipts").glob("gh-*.json"))), 4)
        self.assertEqual(len((ROOT/"data/knowledge/events.jsonl").read_text(encoding="utf-8").splitlines()), 4)
        import hashlib
        for name,sha in (("data/knowledge/events.jsonl", a["event_ledger_blob_sha"]),
                         ("data/knowledge/current.json", a["accepted_knowledge_blob_sha"]),
                         ("data/knowledge/graph-manifest.json", a["graph_manifest_blob_sha"]),
                         ("data/receipts/gh-41436556408-1.json", a["latest_receipt_blob_sha"])):
            blob=(ROOT/name).read_bytes()
            actual=hashlib.sha1(b"blob "+str(len(blob)).encode()+bytes((0,))+blob).hexdigest()
            self.assertEqual(actual, sha, name)

    def test_method_and_doc_boundaries(self):
        a = self.a
        self.assertEqual((a["git_scope"]["main_reachable_commits"],
                          a["git_scope"]["tracked_blob_paths"],
                          a["git_scope"]["pull_requests"]), (261, 312, 69))
        self.assertEqual(a["git_scope"]["closed_unmerged_prs"], [29,32,67])
        self.assertEqual(a["git_scope"]["new_merged_prs"], [68,69])
        self.assertFalse(a["disposition"]["accepted_data_modified"])
        self.assertFalse(a["disposition"]["scientific_claim_promoted"])
        self.assertEqual(a["negative_evidence"]["absence_reason"], "UNKNOWN")
        docs=set(read(ROOT/"evidence/profiles/docs.json")["documents"])
        for p in ("docs/provenance/POST_768_TO_788_RECONCILIATION_2026-11-08.md",
                  "docs/lessons/2026-11-08-green-checks-are-not-scientific-acceptance.md"):
            self.assertIn(p,docs)
            self.assertTrue((ROOT/p).is_file())

if __name__ == "__main__":
    unittest.main()
