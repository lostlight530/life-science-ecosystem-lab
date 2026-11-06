"""Source-pinned first-day Git/PR/file classifications and Actions continuity.

The frozen manifest is an historical source cutoff, not a live-file-count
invariant. No HTTP requests, external Agent calls or production writes.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest

from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state

ROOT = Path(__file__).resolve().parents[1]
TAX = ROOT / "docs" / "taxonomy"
PROV = ROOT / "docs" / "provenance"
BASE = "94f5f0875e7f590846781e5557912730bc482221"
ORIGIN = "00009a38bc136a7c245270770b005e4e102a870d"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def blob_sha(path):
    content = path.read_bytes()
    header = ("blob " + str(len(content)) + "\0").encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


class CompleteHistoryClassificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = load(TAX / "file-register-2026-11-03.json")
        cls.commits = load(TAX / "commit-register-2026-11-03.json")
        cls.prs = load(TAX / "pr-register-2026-11-03.json")
        cls.workflows = load(TAX / "workflow-register-2026-11-03.json")
        cls.latest = load(PROV / "post-673-to-684-observation-2026-11-03.json")

    def test_frozen_baseline_scopes_are_explicit(self):
        for ledger in (self.files, self.commits, self.prs, self.workflows):
            self.assertEqual(ledger["source_main_commit"], BASE)
            self.assertEqual(ledger["git_root"], ORIGIN)
            self.assertIsNone(ledger["per_http_request_clock_utc"])
        self.assertEqual(self.files["tracked_git_blobs"], 274)
        self.assertEqual(self.commits["commit_total"], 250)
        self.assertEqual(self.prs["pr_total"], 57)
        self.assertEqual(self.workflows["workflow_definition_count"], 9)

    def test_every_baseline_file_classified_without_rewriting_github_paths(self):
        rows = self.files["files"]
        self.assertEqual(len(rows), 274)
        paths = [r["path"] for r in rows]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(Counter(r["category"] for r in rows),
                         self.files["category_counts"])
        for row in rows:
            self.assertNotEqual(row["category"], "UNCLASSIFIED")
            self.assertTrue(re.fullmatch("[0-9a-f]{40}", row["git_blob_sha"]))
            self.assertTrue((ROOT / row["path"]).is_file(), row["path"])
        self.assertEqual(sum(self.files["category_counts"].values()), 274)
        self.assertEqual(
            sum(r["category"] == "ACCEPTED_PRODUCTION_STATE" for r in rows), 20)
        self.assertTrue(any(r["role"] ==
                            "STRUCTURAL_PLACEHOLDER_NOT_ACCEPTED_RESULT"
                            for r in rows))

    def test_post_baseline_live_paths_have_reviewed_canonical_categories(self):
        """Cover later tracked paths without changing the 274-file frozen source ledger."""
        raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
        tracked = set(raw.decode("utf-8").rstrip("\0").split("\0"))
        frozen = {row["path"] for row in self.files["files"]}
        self.assertTrue(frozen <= tracked)
        newer = tracked - frozen
        # Dedicated additive evidence directories and regressions can grow.
        # A new root outside these categories requires explicit governance.
        categories = {
            "docs/provenance/": "HISTORICAL_PROVENANCE",
            "docs/taxonomy/": "HISTORICAL_PROVENANCE",
            "docs/lessons/": "PUBLIC_RESEARCH_LESSONS",
            "docs/registration/": "RESEARCH_REGISTRATION_PREPARATION",
            "tests/": "VALIDATION_AND_REGRESSION",
        }
        assigned = {}
        for path in sorted(newer):
            matches = [label for prefix, label in categories.items()
                       if path.startswith(prefix)]
            self.assertEqual(len(matches), 1, f"UNCLASSIFIED_NEW_PATH: {path}")
            assigned[path] = matches[0]
        # The nine genuinely new paths since the PR #58 source cutoff.
        expected_since_cutoff = {
            "docs/provenance/POST_673_TO_684_RECONCILIATION_2026-11-03.md",
            "docs/provenance/post-673-to-684-observation-2026-11-03.json",
            "docs/taxonomy/CORRECTION_REGISTER_2026-11-03.md",
            "docs/taxonomy/README.md",
            "docs/taxonomy/commit-register-2026-11-03.json",
            "docs/taxonomy/file-register-2026-11-03.json",
            "docs/taxonomy/pr-register-2026-11-03.json",
            "docs/taxonomy/workflow-register-2026-11-03.json",
            "tests/test_first_day_taxonomy.py",
        }
        self.assertTrue(expected_since_cutoff <= assigned.keys())
        self.assertEqual(len(expected_since_cutoff), 9)
        self.assertTrue(all(assigned[p] == (
            "VALIDATION_AND_REGRESSION" if p.startswith("tests/")
            else "HISTORICAL_PROVENANCE") for p in expected_since_cutoff))

    def test_actual_frozen_bytes_still_match_pre_review_git_blob_guards(self):
        # Do not compare living README/docs headings to old Git blob SHAs.
        # Historical JSON and formally accepted data remain immutable.
        frozen = [r for r in self.files["files"]
                  if r["path"].startswith("data/")
                  or (r["path"].startswith("docs/provenance/")
                      and r["path"].endswith(".json"))]
        self.assertGreaterEqual(len(frozen), 40)
        for row in frozen:
            self.assertEqual(blob_sha(ROOT / row["path"]),
                             row["git_blob_sha"], row["path"])

    def test_all_pr_origins_and_dispositions_are_preserved(self):
        rows = self.prs["prs"]
        self.assertEqual([r["number"] for r in rows], list(range(1, 58)))
        self.assertEqual(Counter(r["disposition"] for r in rows),
                         {"MERGED": 55, "CLOSED_UNMERGED": 2})
        self.assertEqual([r["number"] for r in rows
                          if r["disposition"] == "CLOSED_UNMERGED"],
                         [29, 32])
        self.assertTrue(all(r["original_title"].strip() for r in rows))
        self.assertTrue(all(r["canonical_category"].strip() for r in rows))
        self.assertTrue(all(not r["agent_identity_attested"] for r in rows))
        self.assertEqual(Counter(r["canonical_category"] for r in rows),
                         self.prs["category_counts"])

    def test_all_reachable_main_commits_have_closed_parent_ancestry(self):
        rows = self.commits["commits"]
        self.assertEqual(len(rows), 250)
        self.assertEqual(len({r["sha"] for r in rows}), 250)
        ids = {r["sha"] for r in rows}
        self.assertEqual(rows[0]["sha"], BASE)
        roots = [r for r in rows if not r["parents"]]
        self.assertEqual([r["sha"] for r in roots], [ORIGIN])
        for record in rows:
            self.assertTrue(set(record["parents"]) <= ids, record["sha"])
            self.assertTrue(record["subject"].strip())
        self.assertEqual(self.commits["page_counts"], [100, 100, 50])
        self.assertTrue(self.commits["parent_closed"])

    def test_actions_are_nine_definitions_not_nine_research_products(self):
        rows = self.workflows["workflows"]
        self.assertEqual(len(rows), 9)
        self.assertEqual(len({r["path"] for r in rows}), 9)
        self.assertEqual(
            {r["path"] for r in rows},
            {r["path"] for r in self.files["files"]
             if r["path"].startswith(".github/workflows/")})
        self.assertTrue(all(r["naming_scope"] ==
            "CURRENT_DEFINITION_NOT_RETROACTIVE_RUN_NAME" for r in rows))

    def test_exact_action_run_673_to_684_census(self):
        first = load(PROV / "full-history-census-2026-10-31.json")
        names = (
            "post-598-to-614-observation-2026-10-31.json",
            "post-614-to-628-observation-2026-11-01.json",
            "post-628-to-640-observation-2026-11-02.json",
            "post-640-to-653-observation-2026-11-02.json",
            "post-653-to-673-observation-2026-11-03.json",
        )
        earlier = [r[0] for r in first["actions"]["records"]]
        count_steps = [len(earlier)]
        for name in names:
            ids = [r[0] for r in load(PROV / name)["new_runs"]]
            count_steps.append(len(ids))
            earlier.extend(ids)
        self.assertEqual(count_steps, [598, 16, 14, 12, 13, 20])
        self.assertEqual(len(set(earlier)), 673)
        additional = [r[0] for r in self.latest["new_runs"]]
        self.assertEqual(len(additional), 11)
        self.assertFalse(set(earlier) & set(additional))
        self.assertEqual(len(set(earlier + additional)), 684)
        self.assertEqual(self.latest["old_ids_retained"], 673)
        self.assertEqual(self.latest["old_ids_missing"], [])
        self.assertEqual(self.latest["page_counts"], [100]*6 + [84])
        self.assertEqual(self.latest["visible_events"],
                         {"push": 348, "pull_request": 294,
                          "schedule": 38, "workflow_dispatch": 4})
        self.assertEqual(self.latest["visible_conclusions"],
                         {"success": 643, "cancelled": 41, "failure": 0})

    def test_run_job_grain_does_not_inflate_skipped_execution(self):
        jobs = self.latest["jobs"]
        self.assertEqual((jobs["new_run_jobs"], jobs["new_success"],
                          jobs["new_skipped"], jobs["new_failed"]),
                         (21, 20, 1, 0))
        self.assertEqual(
            sum(len(r["success_names"]) for r in jobs["records"]), 20)
        self.assertEqual(
            sum(len(r["skipped_names"]) for r in jobs["records"]), 1)
        self.assertEqual(jobs["post_merge_bio_gate"]["pinned_field"], "skipped")
        self.assertEqual(jobs["pre_merge_bio_gate"]["pinned_field"], "success")

    def test_actual_native_accepted_state_is_verified_separately(self):
        report = verify_state(StateRoots(ROOT), require_accepted=True)
        self.assertTrue(report.valid, report.errors)
        events = [json.loads(line) for line in
                  (ROOT / "data/knowledge/events.jsonl")
                  .read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertGreaterEqual(len(events), 4)
        self.assertEqual(events[3]["run_id"], "gh-41436556408-1")
        self.assertEqual(events[3]["change_kind"], "DOCUMENT_TEXT_UNCHANGED")
        self.assertEqual(self.latest["native_state"]["accepted_events"], 4)

    def test_current_navigation_is_classified_without_broken_local_links(self):
        index = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        top = (ROOT / "README.md").read_text(encoding="utf-8")
        registry = (PROV / "README.md").read_text(encoding="utf-8")
        self.assertIn("taxonomy/README.md", index)
        self.assertIn("docs/taxonomy/README.md", top)
        self.assertIn("Provenance evidence registry", registry)
        for name in ("README.md",
                     "CORRECTION_REGISTER_2026-11-03.md"):
            path = TAX / name
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if target.startswith(("http:", "https:", "#")):
                    continue
                self.assertTrue((path.parent / target.split("#")[0]).is_file(),
                                f"{name} -> {target}")


if __name__ == "__main__":
    unittest.main()
