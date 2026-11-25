"""Offline source-pinned complete Git history and native evidence census, 2026-11-15.

No HTTP, Agent runtime, data write, external provider claim or frozen-archive rewrite.
The publishing PR is intentionally outside the dated 299/331/868 observation.
"""
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest

from reviewed_framework_paths import REVIEWED_FRAMEWORK_PATHS
from accepted_production_history import authorized_native_append_paths
from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state

ROOT = Path(__file__).resolve().parents[1]
TAX = ROOT / "docs" / "taxonomy"
PROV = ROOT / "docs" / "provenance"
SOURCE_MAIN = "f2eeec69a1fe3295bf40aff06f0279a2f69c5ae5"
ROOT_SHA = "00009a38bc136a7c245270770b005e4e102a870d"
CATALOGUE = TAX / "full-history-classification-2026-11-15.json"
DELTA = PROV / "post-849-to-868-observation-2026-11-15.json"
FROZEN = TAX / "full-repository-disposition-2026-11-07.json"
FROZEN_ACTIONS = PROV / "post-807-to-849-observation-2026-11-13.json"
SAFE_NEW = {
    "docs/provenance/": "HISTORICAL_PROVENANCE",
    "docs/taxonomy/": "HISTORICAL_PROVENANCE",
    "docs/lessons/": "PUBLIC_RESEARCH_LESSONS",
    "tests/": "VALIDATION_AND_REGRESSION",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii")
                        + b"\0" + data).hexdigest()


def tracked_paths():
    result = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return {p for p in result.decode("utf-8").split("\0") if p}


class RootToNovember15SourceClassificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = load(CATALOGUE)
        cls.d = load(DELTA)
        cls.p = load(FROZEN)
        cls.old = load(FROZEN_ACTIONS)

    def test_source_cutoff_and_closed_ancestry(self):
        c = self.c
        self.assertEqual(c["observation_provenance"]["source_main_sha"],
                         SOURCE_MAIN)
        self.assertEqual(c["observation_provenance"]["git_root_sha"],
                         ROOT_SHA)
        self.assertIsNone(
            c["observation_provenance"]["per_http_request_acquisition_timestamps"])
        rows = c["git"]["commits"]
        self.assertEqual((len(rows), c["git"]["commit_count"]), (299, 299))
        self.assertEqual((rows[0]["sha"], rows[-1]["sha"]),
                         (SOURCE_MAIN, ROOT_SHA))
        ids = {r["sha"] for r in rows}
        self.assertEqual(len(ids), 299)
        self.assertEqual(len({r["tree_sha"] for r in rows}), 274)
        self.assertEqual({r["sha"] for r in rows if not r["parents"]},
                         {ROOT_SHA})
        self.assertTrue(all(set(r["parents"]) <= ids for r in rows))
        self.assertTrue(all(r["subject"].strip() for r in rows))
        prior = {r["sha"]: r for r in self.p["source_commits"]["records"]}
        self.assertEqual(len(prior), 260)
        now = {r["sha"]: r for r in rows}
        self.assertTrue(set(prior) <= set(now))
        self.assertEqual(len(set(now) - set(prior)), 39)
        for sha, row in prior.items():
            self.assertEqual(now[sha]["parents"], row["parents"])
            self.assertEqual(now[sha]["tree_sha"], row["tree_sha"])
        self.assertEqual(len({r["tree_sha"] for r in rows} -
                              {r["tree_sha"] for r in prior.values()}), 35)

    def test_all_76_prs_preserve_original_disposition(self):
        rows = self.c["pull_requests"]["records"]
        self.assertEqual([r["number"] for r in rows], list(range(1, 77)))
        self.assertEqual(Counter(r["disposition"] for r in rows),
                         {"MERGED": 73, "CLOSED_UNMERGED": 3})
        self.assertEqual([r["number"] for r in rows
                          if r["disposition"] == "CLOSED_UNMERGED"],
                         [29, 32, 67])
        self.assertTrue(all(r["original_title"].strip() for r in rows))
        old = {r["number"]: r for r in
               self.p["source_prs"]["records"]}
        self.assertEqual(len(old), 68)
        for r in rows:
            if r["number"] in old:
                self.assertEqual(r["original_title"],
                                 old[r["number"]]["original_title"])
                self.assertEqual(r["disposition"],
                                 old[r["number"]]["disposition"])
        self.assertEqual(self.c["pull_requests"]["dispositions"],
                         {"MERGED": 73, "CLOSED_UNMERGED": 3})

    def test_all_331_current_paths_have_one_reviewed_role_and_original_bytes(self):
        rows = self.c["tracked_files"]["records"]
        self.assertEqual(len(rows), 331)
        self.assertEqual(len({r["path"] for r in rows}), 331)
        self.assertEqual(Counter(r["category"] for r in rows),
                         self.c["tracked_files"]["category_counts"])
        self.assertTrue(all(re.fullmatch("[0-9a-f]{40}", r["git_blob_sha"])
                            and r["review_disposition"] == "RETAIN"
                            and r["role"] for r in rows))
        old = {r["path"]: r for r in self.p["current_files"]["rows"]}
        current = {r["path"]: r for r in rows}
        self.assertEqual(len(old), 309)
        self.assertTrue(set(old) <= set(current))
        self.assertEqual(len(set(current) - set(old)), 22)
        self.assertEqual(self.c["tracked_files"]["prior_missing"], [])
        for path, r in old.items():
            self.assertEqual(current[path]["category"], r["category"])
            self.assertEqual(current[path]["baseline_2026_11_07_sha"],
                             r["git_blob_sha"])
        native_append = authorized_native_append_paths(ROOT)
        for path, rec in current.items():
            if path not in old:
                admitted = [cat for prefix, cat in SAFE_NEW.items()
                            if path.startswith(prefix)]
                if path in native_append and path.startswith("data/"):
                    admitted.append("ACCEPTED_PRODUCTION_STATE")
                self.assertEqual(admitted, [rec["category"]],
                                 "UNCLASSIFIED_SOURCE_PATH: " + path)
        self.assertEqual(self.c["tracked_files"]["changed_prior_paths"],
                         sorted(p for p in old
                                if old[p]["git_blob_sha"]
                                != current[p]["git_blob_sha"]))
        self.assertEqual(len(self.c["tracked_files"]["changed_prior_paths"]), 22)
        self.assertEqual(self.c["tracked_files"]["new_paths"],
                         sorted(set(current) - set(old)))
        all_tracked = tracked_paths()
        self.assertTrue(set(current) <= all_tracked)
        # Frozen historical evidence is not a permanent live-data oracle.
        # Only immutable archives and receipts demand byte-identical witnesses.
        immutable_prefixes = ("data/receipts/", "data/inputs/archive/")
        for path, row in current.items():
            archived_json = (path.startswith(("docs/provenance/",
                                              "docs/taxonomy/"))
                             and path.endswith(".json"))
            if not (path.startswith(immutable_prefixes) or archived_json):
                continue
            self.assertEqual(git_blob(ROOT / path), row["git_blob_sha"],
                             "IMMUTABLE_FROZEN_SOURCE_REWRITTEN: " + path)
        for path in all_tracked - set(current):
            allowed = path in REVIEWED_FRAMEWORK_PATHS or any(path.startswith(p) for p in SAFE_NEW)
            allowed = allowed or (path in native_append
                                  and path.startswith("data/"))
            self.assertTrue(allowed, "UNREVIEWED_NEW_ROOT_PATH: " + path)
        self.assertEqual(self.c["cleanup"]["tracked_removed_prior_paths"], [])
        self.assertEqual(self.c["cleanup"]
                         ["tracked_obvious_cache_or_temporary_paths"], [])

    def test_53_ancestor_only_paths_include_six_retired_intermediate_names(self):
        h = self.c["historical_only"]
        rows = h["records"]
        self.assertEqual((h["count"], h["previous_count"], h["new_count"]),
                         (53, 47, 6))
        self.assertEqual(len(rows), 53)
        self.assertEqual(len({r["path"] for r in rows}), 53)
        current = {r["path"] for r in self.c["tracked_files"]["records"]}
        self.assertFalse(current & {r["path"] for r in rows})
        prior = {r["path"]: r for r in self.p["historical_only"]["rows"]}
        self.assertEqual(len(prior), 47)
        for row in rows:
            self.assertRegex(row["historical_git_blob_sha"], r"^[0-9a-f]{40}$")
            self.assertRegex(row["witness_commit_sha"], r"^[0-9a-f]{40}$")
            self.assertRegex(row["witness_tree_sha"], r"^[0-9a-f]{40}$")
            if row["path"] in prior:
                self.assertEqual(row["historical_git_blob_sha"],
                                 prior[row["path"]]["historical_git_blob_sha"])
                self.assertEqual(row["witness_tree_sha"],
                                 prior[row["path"]]["witness_tree_sha"])
        self.assertEqual({r["path"] for r in rows} - set(prior), {
            ".editorconfig", "CODE_OF_CONDUCT.md", "OPEN_RESEARCH.md",
            "RELEASE_POLICY.md", "RESEARCH_TEMPLATE.md",
            "docs/taxonomy/current-exact-path-classifications.json",
        })
        self.assertEqual(len(current) + len(rows), 384)
        self.assertFalse({r["path"] for r in rows} & tracked_paths())

    def test_exact_849_to_868_run_identity_delta_and_actual_job_grain(self):
        a = self.c["actions"]
        d = self.d["actions"]
        old = set(self.old["actions"]["current_visible_run_ids"])
        now = a["run_records"]
        ids = [r["id"] for r in now]
        self.assertEqual((len(old), len(now), len(set(ids))),
                         (849, 868, 868))
        self.assertEqual((a["visible_run_count"], a["previous_visible"],
                          a["old_run_ids_retained"]), (868, 849, 849))
        self.assertTrue(old <= set(ids))
        self.assertEqual(a["old_run_ids_missing"], [])
        self.assertEqual(set(ids) - old, set(a["new_run_ids"]))
        self.assertEqual(len(a["new_run_ids"]), 19)
        self.assertEqual(Counter(r["conclusion"] for r in now),
                         {"success": 817, "cancelled": 51})
        self.assertEqual(Counter(r["event"] for r in now),
                         {"push": 438, "pull_request": 359,
                          "schedule": 67, "workflow_dispatch": 4})
        self.assertTrue(all(r["name_at_execution"].strip()
                            and r["workflow_path"].startswith(".github/workflows/")
                            for r in now))
        self.assertEqual((d["previous_visible"], d["current_visible"],
                          d["new_count"]), (849, 868, 19))
        self.assertEqual(d["old_ids_missing"], [])
        self.assertEqual({r["id"] for r in d["new_runs"]},
                         set(a["new_run_ids"]))
        self.assertEqual(len({r["id"] for r in d["new_runs"]}), 19)
        jobs = [j for run in d["new_runs"] for j in run["jobs"]]
        self.assertEqual(len(jobs), 41)
        self.assertEqual(len({j["id"] for j in jobs}), 41)
        self.assertEqual(Counter(j["conclusion"] for j in jobs),
                         {"success": 40, "skipped": 1})
        skipped = [(run["id"], j["name"]) for run in d["new_runs"]
                   for j in run["jobs"] if j["conclusion"] == "skipped"]
        self.assertEqual(skipped, [(43266573648, "pinned-field")])
        self.assertEqual(d["new_latest_attempt_job_conclusions"],
                         {"success": 40, "skipped": 1})
        self.assertEqual(self.d["negative_evidence"]
                         ["older_cancelled_run_contains_failed_job"], 43210854941)

    def test_seven_new_scheduled_runs_typed_clocks_and_11_jobs(self):
        scheduled = self.d["scheduled"]["new_runs"]
        self.assertEqual(len(scheduled), 7)
        self.assertEqual(sum(len(r["latest_attempt_jobs"]) for r in scheduled), 11)
        self.assertTrue(all(j["conclusion"] == "success" for r in scheduled
                            for j in r["latest_attempt_jobs"]))
        self.assertEqual(self.d["scheduled"]["causal_status"], "UNKNOWN")
        self.assertEqual(Counter(r["logical_day_shanghai"] for r in scheduled),
                         {"2026-11-13": 3, "2026-11-14": 2,
                          "2026-11-15": 2})
        for r in scheduled:
            nominal = datetime.fromisoformat(r["nominal_utc"].replace("Z", "+00:00"))
            observed = datetime.fromisoformat(r["created_utc"].replace("Z", "+00:00"))
            self.assertEqual(round((observed - nominal).total_seconds()),
                             r["offset_seconds"])
            self.assertGreater(r["offset_seconds"], 0)
        self.assertEqual(self.c["workflows"]["current_definition_count"], 9)
        self.assertEqual(len(self.c["workflows"]
                             ["current_definition_paths"]), 9)

    def test_frozen_archive_and_live_accepted_state_are_separate(self):
        report = verify_state(StateRoots(ROOT), require_accepted=True)
        self.assertTrue(report.valid, report.errors)
        self.assertEqual(self.c["accepted_state"]["new_accepted_writes_since_previous_audit"], 0)
        self.assertEqual(self.d["accepted_state"]["new_applied_events"], 0)
        events = [json.loads(x) for x in
                  (ROOT / "data/knowledge/events.jsonl")
                  .read_text(encoding="utf-8").splitlines() if x.strip()]
        self.assertGreaterEqual(len(events), 5)
        self.assertEqual(events[4]["run_id"], "gh-42611716908-1")
        self.assertEqual(events[4]["outcome"], "APPLIED")
        receipts = list((ROOT / "data/receipts").glob("gh-*.json"))
        self.assertGreaterEqual(len(receipts), 5)
        self.assertGreaterEqual(len(list((ROOT / "data/inputs/archive")
                                   .rglob("*.json"))), 4)
        for path in (CATALOGUE, DELTA, FROZEN, FROZEN_ACTIONS):
            self.assertTrue(path.is_file())
        # Existing frozen source files and their original failure witnesses
        # are not reauthored by the 2026-11-15 successor observation.
        self.assertIn("historical_only", self.p)
        self.assertEqual(self.old["actions"]["current_visible"], 849)
        self.assertEqual(self.old["actions"]["new_job_conclusions"]["failure"], 1)

    def test_exact_document_inventory_and_public_lessons_navigation(self):
        registered = set(load(ROOT / "evidence/profiles/docs.json")["documents"])
        discovered = {p for p in tracked_paths() if p.endswith(".md")}
        self.assertEqual(registered, discovered)
        new_docs = (
            "docs/taxonomy/FULL_HISTORY_CLASSIFICATION_2026-11-15.md",
            "docs/provenance/POST_849_TO_868_RECONCILIATION_2026-11-15.md",
            "docs/lessons/2026-11-15-generalizable-research-software-failure-catalog.md",
        )
        for path in new_docs:
            self.assertIn(path, registered)
            contents = (ROOT / path).read_text(encoding="utf-8")
            self.assertGreater(len(contents), 3000)
            for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", contents):
                if raw.startswith(("https:", "http:", "#", "mailto:")):
                    continue
                relative = raw.split("#", 1)[0].split("?", 1)[0]
                self.assertTrue((ROOT / path).parent.joinpath(relative).exists(),
                                path + " has broken link to " + raw)
        index = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        self.assertIn("FULL_HISTORY_CLASSIFICATION_2026-11-15.md", index)
        self.assertIn("generalizable-research-software-failure-catalog.md", index)


if __name__ == "__main__":
    unittest.main()
