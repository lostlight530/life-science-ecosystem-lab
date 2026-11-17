"""Offline falsifiers for source-scoped Oct 16 -> Nov 17 Git/PR/Run/Job evidence.

The 868/889 figures are frozen API populations, never live GitHub counters.
Current accepted data may grow through legitimate native APPLIED events.
No network, external Agent, provider write or production mutation.
"""
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import unittest

from accepted_production_history import authorized_native_append_paths
from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs/provenance"
TAX = ROOT / "docs/taxonomy"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(content):
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()


class Post868To889EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = read(PROV / "post-868-to-889-observation-2026-11-17.json")
        cls.frozen849 = read(PROV / "post-807-to-849-observation-2026-11-13.json")
        cls.frozen868 = read(PROV / "post-849-to-868-observation-2026-11-15.json")
        cls.source = read(TAX / "full-history-classification-2026-11-15.json")

    def test_first_day_to_source_head_parent_closed(self):
        d = self.d
        g = d["git"]
        old = self.source["git"]["commits"]
        new = g["new_main_commits"]
        self.assertEqual((len(old), len(new)), (299, 3))
        records = old + new
        ids = {r["sha"] for r in records}
        self.assertEqual(len(ids), 302)
        self.assertEqual({r["sha"] for r in records if not r["parents"]},
                         {d["source_root_sha"]})
        self.assertTrue(all(set(r["parents"]) <= ids for r in records))
        self.assertEqual(new[0]["sha"], d["source_main_sha"])
        self.assertEqual(len({r["tree_sha"] for r in records}), 276)
        self.assertEqual(g["current_unique_trees"], 276)

    def test_main_file_delta_is_eight_additions_and_twelve_changes(self):
        g = self.d["git"]
        old = {r["path"]: r["git_blob_sha"]
               for r in self.source["tracked_files"]["records"]}
        added = {r["path"]: r["git_blob_sha"] for r in g["added_paths"]}
        changed = {r["path"]: r for r in g["changed_existing_paths"]}
        self.assertEqual((len(old), len(added), len(changed)), (331, 8, 12))
        self.assertFalse(set(old) & set(added))
        self.assertEqual(g["removed_prior_paths"], [])
        self.assertEqual(len(old) + len(added), 339)
        self.assertEqual(set(added) & set(changed), set())
        for path, record in changed.items():
            self.assertEqual(record["prior_git_blob_sha"], old[path])
            self.assertNotEqual(record["current_git_blob_sha"], old[path])
        # Native append-only records and old frozen JSON are byte witnesses.
        for path, blob in added.items():
            if path.startswith(("data/receipts/", "data/inputs/archive/")) or (
                path.startswith(("docs/provenance/", "docs/taxonomy/")) and
                path.endswith(".json")
            ):
                self.assertEqual(git_blob((ROOT / path).read_bytes()), blob, path)

    def test_prs_and_releases_preserve_real_dispositions(self):
        g = self.d["git"]
        self.assertEqual((g["prs"], g["merged_prs"]), (79, 74))
        self.assertEqual(g["closed_unmerged_prs"], [29, 32, 67, 78])
        self.assertEqual(g["open_prs"], [79])
        self.assertEqual({r["number"]: r["disposition"] for r in g["pr_delta"]},
                         {77: "MERGED", 78: "CLOSED_UNMERGED", 79: "OPEN_DRAFT"})
        self.assertEqual(g["releases"], ["v0.4.0", "v0.5.0", "v0.5.1"])

    def test_868_frozen_ids_plus_21_are_889_without_duplication(self):
        a = self.d["actions"]
        old = set(self.frozen849["actions"]["current_visible_run_ids"])
        next19 = {r["id"] for r in self.frozen868["actions"]["new_runs"]}
        new = {r["id"] for r in a["new_runs"]}
        self.assertEqual((len(old), len(next19), len(new)), (849, 19, 21))
        self.assertFalse(old & next19 or old & new or next19 & new)
        self.assertEqual(len(old | next19 | new), 889)
        self.assertEqual((a["previous_visible"], a["current_prewrite_visible"]),
                         (868, 889))
        self.assertEqual(a["old_ids_missing"], [])
        self.assertEqual(a["new_events"],
                         {"push": 10, "pull_request": 8, "schedule": 3})
        self.assertEqual(a["new_conclusions"],
                         {"success": 17, "failure": 4})
        self.assertEqual(Counter(r["conclusion"] for r in a["new_runs"]),
                         {"success": 17, "failure": 4})
        self.assertTrue(all(r["attempt"] == 1 for r in a["new_runs"]))

    def test_all_40_new_latest_attempt_jobs_and_negative_cases(self):
        a = self.d["actions"]
        jobs = [(r["id"], j) for r in a["new_runs"] for j in r["jobs"]]
        self.assertEqual((len(jobs), len({j["id"] for _, j in jobs})), (40, 40))
        self.assertEqual(Counter(j["conclusion"] for _, j in jobs),
                         {"success": 34, "failure": 5, "skipped": 1})
        self.assertEqual(a["new_latest_attempt_job_conclusions"],
                         {"success": 34, "skipped": 1, "failure": 5})
        self.assertEqual([(run, j["name"]) for run, j in jobs
                          if j["conclusion"] == "skipped"],
                         [(43731037006, "pinned-field")])
        self.assertEqual({r["id"] for r in a["new_runs"]
                          if r["conclusion"] == "failure"},
                         {43919536363, 43919549660, 43919549686, 43919549907})
        fail_jobs = [j for _, j in jobs if j["conclusion"] == "failure"]
        self.assertEqual(len(fail_jobs), 5)
        self.assertTrue(all(any(step["conclusion"] == "failure"
                                for step in j["not_success_steps"])
                            for j in fail_jobs))

    def test_three_scheduled_runs_and_nominal_created_clock(self):
        s = self.d["schedule"]
        self.assertEqual(len(s["new_runs"]), 3)
        self.assertEqual(s["nominal_to_created_cause"], "UNKNOWN")
        for r in s["new_runs"]:
            nominal = datetime.fromisoformat(r["nominal_utc"].replace("Z", "+00:00"))
            actual = datetime.fromisoformat(r["created_utc"].replace("Z", "+00:00"))
            self.assertEqual(int((actual - nominal).total_seconds()),
                             r["offset_seconds"])
            self.assertTrue(all(j["conclusion"] == "success"
                                for j in r["job_conclusions"]))
        self.assertEqual({r["run_id"] for r in s["new_runs"]},
                         {43832487384, 43859884737, 43870632783})

    def test_sixth_acceptance_frozen_prefix_and_live_continuity(self):
        a = self.d["accepted_state"]
        self.assertEqual((a["receipts"], a["events"], a["archives"]), (6, 6, 5))
        lines = (ROOT / "data/knowledge/events.jsonl").read_bytes().splitlines(keepends=True)
        events = [json.loads(line) for line in lines if line.strip()]
        self.assertGreaterEqual(len(events), 6)
        self.assertEqual(events[5]["run_id"], a["latest_execution_id"])
        self.assertEqual(events[5]["event_sha256"],
                         "9665258e83117c625f03ad43794fa260785887653a5c898ad6e2f15f6a9d7dfa")
        self.assertEqual(git_blob(b"".join(lines[:6])),
                         "002fc4295d98156fe3971106490f90f1ab879026")
        receipt = ROOT / ("data/receipts/" + a["latest_execution_id"] + ".json")
        self.assertEqual(git_blob(receipt.read_bytes()),
                         "9b15cd2d59f48498c017db27f3f19465c2607230")
        verified = verify_state(StateRoots(ROOT), require_accepted=True)
        self.assertTrue(verified.valid, verified.errors)
        authorized_native_append_paths(ROOT)
        self.assertEqual(a["new_scientific_claims_verified"], 0)

    def test_historical_failure_and_scientific_nonclaim_stay_visible(self):
        n = self.d["negative_evidence"]
        self.assertEqual(n["failed_pr79_run_ids"],
                         [43919536363, 43919549660, 43919549686, 43919549907])
        self.assertEqual(n["cancelled_parent_with_failed_job"], 43210854941)
        self.assertEqual(n["successful_parent_with_skipped_bio_job"], 43266573648)
        self.assertEqual(n["failure_kind"],
                         "FROZEN_NOV10_ASSERTION_AGAINST_LIVE_APPEND_ONLY_DATA")
        self.assertIn("scientific truth", " ".join(self.d["limits"]))

    def test_new_public_reconciliation_and_lesson_are_registered(self):
        docs = set(read(ROOT / "evidence/profiles/docs.json")["documents"])
        for path in (
            "docs/provenance/POST_868_TO_889_RECONCILIATION_2026-11-17.md",
            "docs/lessons/2026-11-17-frozen-history-vs-live-accepted-state.md",
        ):
            self.assertTrue((ROOT / path).is_file(), path)
            self.assertIn(path, docs)


if __name__ == "__main__":
    unittest.main()
