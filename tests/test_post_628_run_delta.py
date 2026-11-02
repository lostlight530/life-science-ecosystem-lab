"""Independent offline validation of the 598+16+14+12 public GitHub census.

Checks pinned records and current production Git blobs, never queries GitHub,
executes external research material, or promotes a scientific claim.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"


def load(name):
    return json.loads((PROV / name).read_text(encoding="utf-8"))


class Post628RunDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = load("full-history-census-2026-10-31.json")
        cls.first = load("post-598-to-614-observation-2026-10-31.json")
        cls.second = load("post-614-to-628-observation-2026-11-01.json")
        cls.latest = load("post-628-to-640-observation-2026-11-02.json")

    def test_previous_identity_union_and_pagination(self):
        base = [r[0] for r in self.root["actions"]["records"]]
        d1 = [r[0] for r in self.first["new_runs"]]
        d2 = [r[0] for r in self.second["new_runs"]]
        d3 = [r[0] for r in self.latest["new_runs"]]
        self.assertEqual(tuple(map(len, (base, d1, d2, d3))), (598, 16, 14, 12))
        previous = base + d1 + d2
        self.assertEqual(len(previous), len(set(previous)))
        self.assertEqual(len(d3), len(set(d3)))
        self.assertFalse(set(previous) & set(d3))
        self.assertEqual(self.latest["old_ids_retained"], 628)
        self.assertEqual(self.latest["old_ids_missing"], [])
        self.assertEqual(len(set(previous + d3)), 640)
        self.assertEqual(self.latest["page_counts"], [100] * 6 + [40])
        self.assertEqual(sum(self.latest["page_counts"]), 640)
        self.assertEqual(self.latest["previous_visible_total"], 628)
        self.assertIsNone(self.latest["exact_request_timestamp_utc"])

    def test_exact_run_identity_jobs_and_event_arithmetic(self):
        latest = self.latest
        rows = latest["new_runs"]
        self.assertEqual(len(rows), latest["new_count"])
        self.assertEqual(Counter(r[2] for r in rows), Counter({"push": 9, "pull_request": 3}))
        self.assertEqual({r[5] for r in rows}, {"success"})
        self.assertEqual({r[0] for r in rows if r[2] == "schedule"}, set())
        self.assertTrue(all(r[3].endswith("Z") and len(r[4]) == 40 for r in rows))
        self.assertEqual(latest["visible_events"], {
            "push": 319, "pull_request": 282, "schedule": 35, "workflow_dispatch": 4
        })
        self.assertEqual(latest["visible_conclusions"], {
            "success": 599, "cancelled": 41, "failure": 0
        })
        self.assertEqual(sum(latest["visible_events"].values()), 640)
        self.assertEqual(sum(latest["visible_conclusions"].values()), 640)
        j = latest["new_job_reconciliation"]
        self.assertEqual((j["new_successful_jobs"], j["new_skipped_jobs"]), (21, 1))
        main = {x["run_id"]: x for x in j["main_push_runs"]}
        self.assertEqual(set(main), {41302294001, 41302293913, 41302293885})
        self.assertEqual(Counter(x["conclusion"] for x in main[41302294001]["jobs"]),
                         Counter({"success": 1, "skipped": 1}))
        self.assertEqual(j["pr_pinned_field"]["conclusion"], "success")
        self.assertEqual(j["observed_python_regression_tests"], 204)

    def test_reconcile_native_jobs_and_production_boundary(self):
        s = self.latest["observed_native_schedule"]
        by = s["by_workflow"]
        self.assertEqual(sum(by.values()), s["runs"])
        expected_jobs = (by["life-science-continuity.yml"] +
                         2 * by["life-science-daily-selfcheck.yml"] +
                         2 * by["life-science-knowledge.yml"] +
                         2 * by["life-science-bio.yml"])
        self.assertEqual((s["runs"], s["successful_jobs"], expected_jobs), (35, 54, 54))
        self.assertEqual(s["new_scheduled_runs"], 0)
        prod = self.latest["production_reconciliation"]
        self.assertEqual((prod["accepted_receipts"], prod["accepted_event_lines"],
                          prod["archived_candidates"], prod["new_accepted_receipts"]),
                         (3, 3, 2, 0))
        receipts = sorted((ROOT / "data" / "receipts").glob("gh-*.json"))
        events = [json.loads(line) for line in
                  (ROOT / "data/knowledge/events.jsonl").read_text(encoding="utf-8").splitlines()]
        # The three accepted records belong to this fixed 640-Run observation.
        # New native APPLIED records must extend, not rewrite, that history.
        self.assertGreaterEqual(len(receipts), 3)
        self.assertGreaterEqual(len(events), 3)
        self.assertEqual([x["run_id"] for x in events[:3]],
                         ["gh-38995485443-1", "gh-39227185707-1",
                          "gh-40297059874-1"])
        self.assertTrue(all(json.loads(p.read_text(encoding="utf-8"))["outcome"] == "APPLIED"
                            for p in receipts))
        self.assertTrue(all(x["outcome"] == "APPLIED" for x in events))

    def test_exact_git_blob_guards_and_historical_negatives(self):
        guards = self.latest["production_reconciliation"]["git_blob_guards"]
        self.assertEqual(len(guards), 10)
        pins = load("historical-production-tree-guards-2026-11-02.json")
        historical = pins["cutoffs"]["post_628"]
        self.assertEqual(historical["commit"], self.latest["observed_source_main"])
        self.assertEqual(set(historical["blobs"]), set(guards))
        for path, expected in guards.items():
            self.assertEqual(historical["blobs"][path], expected, path)
            raw = (ROOT / path).read_bytes()
            blob = b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
            if path.startswith("data/receipts/"):
                # Old accepted receipts are immutable, even as current state advances.
                self.assertEqual(hashlib.sha1(blob).hexdigest(), expected, path)
            else:
                # Snapshot-local hashes are evidence of the old world-line, not
                # the expected hash of mutable current production files forever.
                self.assertEqual(len(expected), 40)
                self.assertTrue((ROOT / path).is_file())
        repo = self.latest["repository_reconciliation"]
        self.assertEqual((repo["main_reachable_commits"], repo["prs_total"],
                          repo["prs_merged"], repo["tracked_git_blobs"],
                          repo["workflow_definitions"]), (245, 53, 51, 259, 9))
        self.assertEqual(repo["prs_closed_unmerged"], [29, 32])
        self.assertEqual(repo["prs_open"], 0)
        self.assertEqual(repo["github_releases"], ["v0.4.0", "v0.5.0"])
        self.assertEqual(self.latest["negative_and_unknown"]["historical_frozen_failed_runs"], 8)
        self.assertEqual(self.latest["negative_and_unknown"]["historical_workflow_name_corrections"], 134)
        self.assertEqual(self.latest["negative_and_unknown"]["historical_median_corrections"], 2)
        self.assertEqual(self.latest["negative_and_unknown"]["latest_log_read_unavailable"]["log_fetch_result"],
                         "BlobNotFound/404")
        self.assertEqual(self.latest["decision"]["production_data"], "NO_CHANGE_REQUIRED")
        self.assertEqual(self.latest["decision"]["scientific_claim"], "NO_NEW_VERIFIED_CLAIM")


if __name__ == "__main__":
    unittest.main()
