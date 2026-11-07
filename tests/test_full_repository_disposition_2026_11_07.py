"""Independent offline verification of source-pinned complete Git file governance."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
TAX = ROOT / "docs" / "taxonomy"
H = "363d977fa17fe368fe9db1fd28c46aba7285cd84"
ORIGIN = "00009a38bc136a7c245270770b005e4e102a870d"
NEW_REPORT = "docs/taxonomy/COMPLETE_FILE_GOVERNANCE_2026-11-07.md"
NEW_TEST = "tests/test_full_repository_disposition_2026_11_07.py"
NEW_JSON = "docs/taxonomy/full-repository-disposition-2026-11-07.json"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def blob(path):
    b = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + bytes((0,)) + b).hexdigest()

class FullCurrentRepositoryDispositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = read(ROOT / NEW_JSON)
        cls.old = read(TAX / "full-file-lifecycle-2026-11-05.json")

    def test_pinned_all_commit_tree_and_pr_identities(self):
        r = self.r
        self.assertEqual((r["source_main_sha"], r["source_root_sha"]), (H, ORIGIN))
        c = r["source_commits"]
        rows = c["records"]
        self.assertEqual(len(rows), 260)
        self.assertEqual(len({x["sha"] for x in rows}), 260)
        self.assertEqual(rows[0]["sha"], H)
        self.assertEqual({x["sha"] for x in rows if not x["parents"]}, {ORIGIN})
        self.assertEqual(len({x["tree_sha"] for x in rows}), 239)
        ids = {x["sha"] for x in rows}
        self.assertTrue(all(set(x["parents"]) <= ids for x in rows))
        previous = {x["sha"]: x for x in self.old["source_commits"]["records"]}
        self.assertEqual(len(previous), 256)
        for row in rows:
            if row["sha"] in previous:
                self.assertEqual(row["tree_sha"], previous[row["sha"]]["tree_sha"])
                self.assertEqual(row["parents"], previous[row["sha"]]["parents"])
        checks = c["post_prior_tree_verifications"]
        self.assertEqual(len(checks), 4)
        self.assertTrue(all(not x["truncated"] and x["tree_sha"] == x["returned_tree_sha"]
                            and not x["noncurrent_paths"] for x in checks))
        p = r["source_prs"]
        self.assertEqual((p["count"], p["merged"], p["closed_unmerged"], p["open"]),
                         (68, 65, [29, 32, 67], 0))
        self.assertEqual(sorted(x["number"] for x in p["records"]), list(range(1, 69)))
        self.assertTrue(all(x["original_title"].strip() for x in p["records"]))
        self.assertFalse(next(x for x in p["records"] if x["number"] == 67)["merged"])

    def test_all_309_files_have_reviewed_categories_and_nonreplacement(self):
        d = self.r["current_files"]
        rows = d["rows"]
        self.assertEqual(len(rows), 309)
        self.assertEqual(len({x["path"] for x in rows}), 309)
        self.assertEqual(Counter(x["category"] for x in rows), d["category_counts"])
        self.assertTrue(all(x["category"] and x["role"] and x["review_disposition"] == "RETAIN" for x in rows))
        self.assertTrue(all(re.fullmatch("[0-9a-f]{40}", x["git_blob_sha"]) for x in rows))
        old = {x["path"]: x for x in self.old["current_files"]["rows"]}
        now = {x["path"]: x for x in rows}
        self.assertEqual(len(old), 294)
        self.assertTrue(set(old) <= set(now))
        self.assertEqual(len(set(now) - set(old)), 15)
        self.assertEqual(d["removed_prior_paths"], [])
        for path, rec in old.items():
            self.assertEqual(now[path]["category"], rec["category"])
        changes = {item["path"] for item in d["changed_prior_files"]}
        self.assertEqual(len(changes), 4)
        self.assertEqual({x["path"] for x in d["changed_prior_files"]},
                         {"docs/README.md", "docs/provenance/README.md",
                          "docs/taxonomy/README.md", "evidence/profiles/docs.json"})
        for rec in d["changed_prior_files"]:
            self.assertEqual(rec["prior_sha"], old[rec["path"]]["git_blob_sha"])
            self.assertNotEqual(rec["prior_sha"], rec["current_sha"])
        for rec in rows:
            if rec["path"] in old and rec["path"] not in {x["path"] for x in d["changed_prior_files"]}:
                self.assertEqual(rec["git_blob_sha"], old[rec["path"]]["git_blob_sha"])
        allowed = {"docs/provenance/": "HISTORICAL_PROVENANCE",
                   "docs/taxonomy/": "HISTORICAL_PROVENANCE",
                   "docs/lessons/": "PUBLIC_RESEARCH_LESSONS",
                   "tests/": "VALIDATION_AND_REGRESSION"}
        for path in d["new_paths"]:
            self.assertEqual([c for prefix, c in allowed.items() if path.startswith(prefix)],
                             [now[path]["category"]])

    def test_47_historical_only_witnesses_still_absent(self):
        old = self.old["historical_only_files"]["rows"]
        h = self.r["historical_only"]
        self.assertEqual((len(old), h["count"]), (47, 47))
        self.assertEqual([x["path"] for x in h["rows"]], [x["path"] for x in old])
        self.assertEqual(h["reappeared_paths"], [])
        self.assertEqual(h["post_2026_11_05_new_retired_paths"], [])
        current = {x["path"]: x for x in self.r["current_files"]["rows"]}
        self.assertFalse(set(current) & {x["path"] for x in h["rows"]})
        self.assertEqual(h["exact_byte_reuse_at_current"], 19)
        for rec in h["rows"]:
            self.assertEqual(rec["current_status"], "HISTORICAL_ONLY_NOT_TRACKED_DO_NOT_DELETE_AGAIN")
            self.assertEqual(rec["historical_git_blob_sha"],
                             next(x for x in old if x["path"] == rec["path"])["historical_git_blob_sha"])
            for p in rec["content_identical_current_paths"]:
                self.assertIn(p, current)
                self.assertEqual(current[p]["git_blob_sha"], rec["historical_git_blob_sha"])

    def test_live_markdown_cleanup_and_accepted_data_boundary(self):
        d = self.r
        cleanup = d["cleanup_review"]
        self.assertEqual(cleanup["tracked_temporary_or_cache_candidates"], [])
        self.assertEqual(cleanup["unsafe_case_collisions"], [])
        self.assertEqual(cleanup["tracked_git_file_removal_candidates"], [])
        self.assertEqual(cleanup["deletion_outcome"], "NO_CHANGE_REQUIRED")
        self.assertEqual(len(cleanup["tracked_structural_placeholders_retained"]), 6)
        self.assertEqual(cleanup["workflow_yaml_count"], 9)
        self.assertEqual((d["accepted_state"]["receipts"], d["accepted_state"]["events"],
                          d["accepted_state"]["archive_candidates"]), (4, 4, 3))
        self.assertFalse(d["accepted_state"]["new_write"])
        self.assertFalse((ROOT / "docs/registration").exists())
        tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
        pinned = {x["path"] for x in d["current_files"]["rows"]}
        self.assertTrue(pinned <= tracked)
        allowed_extra = {NEW_REPORT, NEW_JSON, NEW_TEST}
        self.assertTrue((tracked - pinned) <= allowed_extra | {
            "docs/lessons/2026-11-07-cleanup-and-retention-evidence.md"})
        md = {p for p in tracked if p.endswith(".md")}
        docs = set(read(ROOT / "evidence/profiles/docs.json")["documents"])
        self.assertEqual(md, docs)
        self.assertEqual((d["current_files"]["current_markdown"],
                          d["current_files"]["registered_markdown"]), (80, 80))
        for rec in d["current_files"]["rows"]:
            if rec["path"].startswith("data/"):
                self.assertEqual(blob(ROOT / rec["path"]), rec["git_blob_sha"],
                                 "ACCEPTED_DATA_WAS_CHANGED: " + rec["path"])
            if rec["path"].endswith(".json") and rec["path"].startswith(
                   ("docs/provenance/", "docs/taxonomy/")):
                self.assertEqual(blob(ROOT / rec["path"]), rec["git_blob_sha"],
                                 "FROZEN_ARCHIVE_WAS_CHANGED: " + rec["path"])

if __name__ == "__main__":
    unittest.main()
