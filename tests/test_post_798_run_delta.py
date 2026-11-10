"""Offline falsifiers for the 798→807 GitHub delta and unchanged accepted research state."""
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def blob_sha(payload):
    return hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()

class Post798AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = read(PROV / "post-798-to-807-observation-2026-11-10.json")
        cls.previous = read(PROV / "post-788-to-798-observation-2026-11-09.json")
        cls.prior = read(PROV / "post-768-to-788-observation-2026-11-08.json")
        cls.older = read(PROV / "post-758-to-768-observation-2026-11-07.json")
        cls.base = read(PROV / "post-750-to-758-observation-2026-11-06.json")

    def test_exact_population_and_identity_nonloss(self):
        c = self.current["action_census"]
        ids = list(self.base["action_census"]["current_visible_run_ids"])
        ids += [x["id"] for x in self.older["action_census"]["new_runs"]]
        ids += [x["id"] for x in self.prior["action_census"]["new_runs"]]
        ids += [x["id"] for x in self.previous["action_census"]["new_runs"]]
        additional = [x["id"] for x in c["new_runs"]]
        self.assertEqual((len(ids), len(set(ids))), (798, 798))
        self.assertEqual((len(additional), len(set(ids + additional))), (9, 807))
        self.assertFalse(set(ids) & set(additional))
        self.assertEqual(set(additional), {
            42649832401, 42649841279, 42649841329, 42649841330,
            42650065171, 42650065402, 42650065492,
            42785634316, 42818454449,
        })
        self.assertEqual((c["previous_visible"], c["retained_prior_ids"],
                          c["new_count"], c["current_visible"]),
                         (798, 798, 9, 807))
        self.assertEqual(c["missing_prior_ids"], [])
        self.assertEqual(c["source_page_counts"], [100] * 8 + [7])
        self.assertEqual(c["current_conclusions"],
                         {"success": 766, "cancelled": 41})
        self.assertEqual(c["current_events"],
                         {"schedule": 56, "push": 414,
                          "pull_request": 333, "workflow_dispatch": 4})
        self.assertEqual(Counter(x["event"] for x in c["new_runs"]),
                         {"push": 4, "pull_request": 3, "schedule": 2})

    def test_all_new_jobs_and_conditional_bio_skip(self):
        c = self.current["action_census"]
        jobs = [j for run in c["new_runs"] for j in run["jobs"]]
        self.assertEqual(len(jobs), 20)
        self.assertEqual(len({j["id"] for j in jobs}), 20)
        self.assertEqual(Counter(j["conclusion"] for j in jobs),
                         {"success": 19, "skipped": 1})
        self.assertEqual(c["new_run_jobs"],
                         {"count": 20, "success": 19,
                          "skipped": 1, "failed": 0})
        skipped = [(run["id"], j["name"]) for run in c["new_runs"]
                   for j in run["jobs"] if j["conclusion"] == "skipped"]
        self.assertEqual(skipped, [(42650065492, "pinned-field")])
        self.assertTrue(all(run["attempt"] == 1 and
                            run["conclusion"] == "success"
                            for run in c["new_runs"]))

    def test_daily_schedule_clocks_and_results(self):
        s = self.current["schedule"]
        self.assertEqual((s["previous_verified_runs"],
                          s["previous_verified_success_jobs"],
                          s["current_visible_runs"],
                          s["cross_cutoff_verified_success_jobs"]),
                         (54, 84, 56, 87))
        self.assertEqual([x["offset_seconds"] for x in s["new_scheduled_runs"]],
                         [25701, 30503])
        for row in s["new_scheduled_runs"]:
            created = datetime.fromisoformat(
                row["created_utc"].replace("Z", "+00:00"))
            nominal = datetime.fromisoformat(
                row["nominal_utc"].replace("Z", "+00:00"))
            self.assertEqual(int((created - nominal).total_seconds()),
                             row["offset_seconds"])
            run = next(x for x in self.current["action_census"]["new_runs"]
                       if x["id"] == row["run_id"])
            self.assertEqual(run["event"], "schedule")
            self.assertEqual({j["id"] for j in run["jobs"]},
                             set(row["job_ids"]))
            self.assertTrue(all(j["conclusion"] == "success"
                                for j in run["jobs"]))
        self.assertEqual(s["nominal_to_created_cause"], "UNKNOWN")

    def test_accepted_state_unchanged_and_valid(self):
        a = self.current["accepted_state"]
        self.assertEqual((a["previous_receipts"], a["previous_events"],
                          a["previous_archive_candidates"]), (5, 5, 4))
        self.assertEqual((a["receipts"], a["chained_events"],
                          a["archived_candidates"]), (5, 5, 4))
        receipts = sorted((ROOT / "data" / "receipts").glob("gh-*.json"))
        archives = sorted((ROOT / "data" / "inputs" / "archive").rglob("*.json"))
        self.assertEqual((len(receipts), len(archives)), (5, 4))
        raw = (ROOT / "data" / "knowledge" / "events.jsonl").read_bytes()
        events = [json.loads(x) for x in raw.decode("utf-8").splitlines()]
        self.assertEqual(len(events), 5)
        self.assertEqual(events[-1]["event_sha256"], a["latest_event_sha256"])
        self.assertEqual(events[-1]["run_id"], a["execution_id"])
        self.assertEqual(blob_sha(raw), a["event_ledger_blob_sha_at_cutoff"])
        receipt = ROOT / a["latest_receipt"]
        self.assertEqual(blob_sha(receipt.read_bytes()),
                         a["latest_receipt_blob_sha"])
        from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state
        result = verify_state(StateRoots(ROOT), require_accepted=True)
        self.assertTrue(result.valid, result.errors)
        self.assertEqual(a["new_scientific_claims_verified"], 0)

    def test_failed_gates_remain_negative_evidence(self):
        n = self.current["negative_evidence"]
        self.assertEqual(n["failed_post_cutoff_run_ids_now_404"],
                         [42648743634, 42648814068,
                          42648814253, 42648814000])
        self.assertEqual(n["current_404_disappearance_cause"], "UNKNOWN")
        self.assertEqual(n["repair_head"],
                         "17441ff48fd3391ddc68b9b53a73b3d7b7fe7d11")
        self.assertEqual(set(n["repair_visible_runs"]),
                         {42649832401, 42649841279,
                          42649841329, 42649841330})
        self.assertIn("failed gate evidence", n["interpretation"])

    def test_git_governance_and_public_docs(self):
        g = self.current["git_scope"]
        self.assertEqual((g["main_reachable_commits"],
                          g["tracked_blob_paths"],
                          g["pull_requests"], g["merged_prs"]),
                         (264, 323, 71, 68))
        self.assertEqual(g["closed_unmerged_prs"], [29, 32, 67])
        self.assertEqual(g["open_prs"], 0)
        self.assertFalse(g["main_branch_protected"])
        self.assertEqual(g["repository_rulesets"], [])
        self.assertFalse(
            self.current["disposition"]["accepted_data_manually_modified"])
        self.assertFalse(
            self.current["disposition"]["workflow_or_tool_modified"])
        docs = set(read(ROOT / "evidence" / "profiles" / "docs.json")["documents"])
        for path in (
            "docs/provenance/POST_798_TO_807_RECONCILIATION_2026-11-10.md",
            "docs/lessons/2026-11-10-repair-success-does-not-erase-failed-gates.md",
        ):
            self.assertIn(path, docs)
            self.assertTrue((ROOT / path).is_file())

if __name__ == "__main__":
    unittest.main()
