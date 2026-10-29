"""Offline integrity checks of a fixed public GitHub history observation

These records are descriptive, non-production snapshots. No network, scheduler,
Tool implementation or accepted Knowledge state is touched
"""
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs" / "provenance"
DAY = "2026-10-30"
BASE = "05ab6b2dc98dfe13581b5ae1bedcd11a58dbbb77"
ROOT_SHA = "00009a38bc136a7c245270770b005e4e102a870d"


def load(name):
    path = DIRECTORY / f"{name}-{DAY}.json"
    return json.loads(path.read_text(encoding="utf-8"))


class FrozenRepositoryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.commits = load("commits")
        cls.prs = load("pull-requests")
        cls.runs = load("action-runs")

    def test_common_source_and_fixed_cutoff_are_explicit(self):
        observed = {s["observed_at_utc"] for s in
                    (self.commits, self.prs, self.runs)}
        self.assertEqual(observed, {"2026-10-29T16:24:03.499Z"})
        for snapshot in (self.commits, self.prs, self.runs):
            self.assertEqual(snapshot["reference_main_sha"], BASE)
            self.assertEqual(snapshot["repo"],
                             "lostlight530/life-science-ecosystem-lab")
            self.assertEqual(snapshot["schema_version"], "1.0.0")
            self.assertEqual(
                snapshot["snapshot_kind"],
                "PROJECT_OWNED_GITHUB_PUBLIC_API_READ_ONLY_OBSERVATION",
            )
            self.assertEqual(snapshot["returned_count"],
                             len(snapshot["records"]))
            self.assertTrue(snapshot["source_urls"])
            self.assertTrue(snapshot["provenance_limit"])

    def test_git_main_ancestry_is_unique_and_parent_closed(self):
        commits = self.commits["records"]
        self.assertEqual(len(commits), 234)
        self.assertEqual(commits[0]["sha"], BASE)
        self.assertEqual(commits[-1]["sha"], ROOT_SHA)
        shas = [record["sha"] for record in commits]
        self.assertEqual(len(shas), len(set(shas)))
        self.assertEqual([r["list_position"] for r in commits],
                         list(range(1, 235)))
        referenced = {parent for record in commits
                      for parent in record["parents"]}
        self.assertTrue(referenced.issubset(set(shas)))
        self.assertEqual(commits[-1]["parents"], [])
        self.assertIn(
            "c09d4f3d0a8ebe28970dd511c7ab1e96f2ee0ea6",
            set(shas),
        )
        self.assertEqual(len(self.commits["source_urls"]), 3)

    def test_prs_retain_unmerged_negative_and_full_coverage(self):
        prs = self.prs["records"]
        self.assertEqual(len(prs), 42)
        self.assertEqual([r["number"] for r in prs], list(range(1, 43)))
        merged = [r for r in prs if r["merged_at"]]
        unmerged = [r for r in prs if
                    r["state"] == "closed" and not r["merged_at"]]
        self.assertEqual(len(merged), 40)
        self.assertEqual({r["number"] for r in unmerged}, {29, 32})
        self.assertEqual(self.prs["merged_count"], 40)
        self.assertEqual(self.prs["closed_unmerged_count"], 2)
        self.assertFalse(any(r["state"] == "open" for r in prs))
        self.assertEqual(len(self.prs["source_urls"]), 1)

    def test_run_census_keeps_failures_and_cancellations(self):
        runs = self.runs["records"]
        self.assertEqual(len(runs), 531)
        self.assertEqual(len({r["id"] for r in runs}), 531)
        self.assertEqual(self.runs["reported_total_count"], 531)
        self.assertEqual(Counter(r["conclusion"] for r in runs), {
            "success": 483, "failure": 8, "cancelled": 40
        })
        self.assertEqual(Counter(r["event"] for r in runs), {
            "push": 251, "pull_request": 248,
            "schedule": 28, "workflow_dispatch": 4
        })
        self.assertEqual(len(self.runs["source_urls"]), 6)

    def test_only_three_native_runs_and_two_are_scheduled(self):
        runs = self.runs["records"]
        native = {r["id"]: r for r in runs if
                  r["name"] ==
                  "Life Science Knowledge Workflow — Native Lifecycle"}
        self.assertEqual(set(native),
                         {38995485443, 39227185707, 40297059874})
        self.assertEqual(
            [native[x]["event"] for x in sorted(native)],
            ["workflow_dispatch", "schedule", "schedule"],
        )
        self.assertTrue(all(x["conclusion"] == "success"
                            for x in native.values()))
        # This asserts the historical run identity only; it is not sufficient
        # to attest receipt/application without the separate Git data ledger.
        self.assertIn(38889128519, {r["id"] for r in runs})


if __name__ == "__main__":
    unittest.main()
