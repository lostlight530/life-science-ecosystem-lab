"""Date-scoped first-day -> Nov 4 Git/PR/file/Run taxonomy replay.

Frozen source IDs are immutable witnesses; later tracked additions are only
allowed under the reviewed classification families. No network or writes.
"""
from collections import Counter
import json
from pathlib import Path
import subprocess
import unittest

from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state
from accepted_production_history import authorized_native_append_paths

ROOT = Path(__file__).resolve().parents[1]
TAX = ROOT / "docs" / "taxonomy"
PROV = ROOT / "docs" / "provenance"
CURRENT = "991914541fc3f56b8da00b4a3b91cb0dd71572d1"
ORIGIN = "00009a38bc136a7c245270770b005e4e102a870d"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

class LiveTaxonomyAddendumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.delta = load(TAX / "post-2026-11-04-source-classification.json")
        cls.files = load(TAX / "file-register-2026-11-03.json")
        cls.commits = load(TAX / "commit-register-2026-11-03.json")
        cls.prs = load(TAX / "pr-register-2026-11-03.json")
        cls.wf = load(TAX / "workflow-register-2026-11-03.json")
        cls.exact_path_categories = {
            row["path"]: row["category"]
            for row in load(TAX / "current-exact-path-classifications.json")["entries"]
        }

    def test_main_parent_closure_through_day_one(self):
        self.assertEqual(self.delta["main_source_cutoff_sha"], CURRENT)
        history = self.delta["post_baseline_main_commits"] + self.commits["commits"]
        ids = {x["sha"] for x in history}
        self.assertEqual(len(history), 254)
        self.assertEqual(len(ids), len(history))
        self.assertEqual(history[0]["sha"], CURRENT)
        self.assertEqual([x["sha"] for x in history if not x["parents"]], [ORIGIN])
        for x in history:
            self.assertTrue(set(x["parents"]) <= ids, x["sha"])
        self.assertEqual({x["era"] for x in self.delta["post_baseline_main_commits"]},
                         {"HISTORY_AUDIT_AND_NATIVE_CONTINUITY"})

    def test_all_prs_classified_without_promoting_unmerged_or_agents(self):
        rows = self.prs["prs"] + self.delta["post_baseline_prs"]
        self.assertEqual(len(rows), 61)
        self.assertEqual(sorted(x["number"] for x in rows), list(range(1, 62)))
        self.assertEqual(Counter(x["disposition"] for x in rows),
                         {"MERGED": 59, "CLOSED_UNMERGED": 2})
        self.assertEqual(sorted(x["number"] for x in rows
                                if x["disposition"] == "CLOSED_UNMERGED"),
                         [29, 32])
        self.assertTrue(all(x["canonical_category"] and
                            x["original_title"] and
                            not x["agent_identity_attested"] for x in rows))

    def test_every_pinned_file_and_post_cutoff_living_file_is_routed(self):
        old = {x["path"] for x in self.files["files"]}
        newer = self.delta["post_baseline_files"]
        named = {x["path"] for x in newer}
        self.assertEqual(len(old), 274)
        self.assertEqual(len(newer), 13)
        self.assertEqual(len(named), 13)
        self.assertFalse(old & named)
        self.assertEqual(Counter(x["category"] for x in newer),
                         {"HISTORICAL_PROVENANCE": 10,
                          "PUBLIC_RESEARCH_LESSONS": 1,
                          "VALIDATION_AND_REGRESSION": 2})
        tracked = set(subprocess.check_output(
            ["git", "ls-files"], cwd=ROOT, text=True).splitlines())
        self.assertTrue(old | named <= tracked)
        category_prefixes = {
            "docs/provenance/": "HISTORICAL_PROVENANCE",
            "docs/taxonomy/": "HISTORICAL_PROVENANCE",
            "docs/lessons/": "PUBLIC_RESEARCH_LESSONS",
            "tests/": "VALIDATION_AND_REGRESSION",
        }
        for x in newer:
            self.assertEqual([cat for prefix, cat in category_prefixes.items()
                              if x["path"].startswith(prefix)], [x["category"]])
            self.assertEqual(len(x["git_blob_sha"]), 40)
        production_append = authorized_native_append_paths(ROOT)
        for path in sorted(tracked - old - named):
            matched = [cat for prefix, cat in category_prefixes.items()
                       if path.startswith(prefix)]
            if path in self.exact_path_categories:
                matched.append(self.exact_path_categories[path])
            if path in production_append and path.startswith("data/"):
                matched.append("ACCEPTED_PRODUCTION_STATE")
            self.assertEqual(len(matched), 1, "UNCLASSIFIED_NEW_PATH: " + path)
        self.assertEqual(len(self.wf["workflows"]), 9)
        self.assertEqual({x["path"] for x in self.wf["workflows"]},
                         {p for p in tracked if p.startswith(".github/workflows/")})

    def test_actions_frozen_chain_and_current_visibility_are_distinct(self):
        base = load(PROV / "full-history-census-2026-10-31.json")
        ids = [x[0] for x in base["actions"]["records"]]
        for filename in (
            "post-598-to-614-observation-2026-10-31.json",
            "post-614-to-628-observation-2026-11-01.json",
            "post-628-to-640-observation-2026-11-02.json",
            "post-640-to-653-observation-2026-11-02.json",
            "post-653-to-673-observation-2026-11-03.json",
            "post-673-to-684-observation-2026-11-03.json",
            "post-684-to-711-observation-2026-11-04.json",
        ):
            ids.extend(x[0] for x in load(PROV / filename)["new_runs"])
        self.assertEqual(len(ids), 711)
        self.assertEqual(len(set(ids)), 711)
        d = self.delta["actions"]
        new = d["new_current_runs"]
        self.assertEqual(len(new), 10)
        self.assertFalse(set(ids) & {x[0] for x in new})
        self.assertEqual(len(set(ids + [x[0] for x in new])), 721)
        self.assertEqual(Counter(x[2] for x in new),
                         {"push": 7, "pull_request": 3})
        self.assertEqual({x[5] for x in new}, {"success"})
        self.assertEqual(d["visible_conclusion_counts"],
                         {"success": 680, "cancelled": 41, "failure": 0})
        self.assertEqual(sum(d["visible_event_counts"].values()), 721)
        self.assertEqual(len(d["previously_seen_pre_pr_failure_run_ids_currently_404"]), 3)
        self.assertEqual(d["current_missing_failure_cause"], "UNKNOWN")
        self.assertIsNone(self.delta["exact_per_http_request_timestamp_utc"])

    def test_accepted_data_independent_and_public_document_registered(self):
        self.assertTrue(verify_state(StateRoots(ROOT), require_accepted=True).valid)
        receipts = list((ROOT / "data/receipts").glob("gh-*.json"))
        self.assertGreaterEqual(len(receipts), 4)
        lines = [json.loads(x) for x in
                 (ROOT / "data/knowledge/events.jsonl").read_text(encoding="utf-8").splitlines()
                 if x.strip()]
        self.assertGreaterEqual(len(lines), 4)
        self.assertEqual([x["run_id"] for x in lines[:4]],
                         ["gh-38995485443-1", "gh-39227185707-1",
                          "gh-40297059874-1", "gh-41436556408-1"])
        authorized_native_append_paths(ROOT)
        docs = load(ROOT / "evidence/profiles/docs.json")["documents"]
        self.assertIn("docs/taxonomy/POST_2026-11-04_SOURCE_CLASSIFICATION.md", docs)

if __name__ == "__main__":
    unittest.main()
