"""Reconcile immutable post-PR64 file and 730-to-750 Actions observations."""
import hashlib
import json
from collections import Counter
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PROV=ROOT/"docs"/"provenance"
TAX=ROOT/"docs"/"taxonomy"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def git_blob(path):
    b=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+bytes((0,))+b).hexdigest()

class Post730RunDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=read(PROV/"post-730-to-750-observation-2026-11-05.json")

    def test_all_730_prior_run_ids_and_new_ids(self):
        baseline=read(PROV/"full-history-census-2026-10-31.json")
        old=[x[0] for x in baseline["actions"]["records"]]
        for name in (
          "post-598-to-614-observation-2026-10-31.json",
          "post-614-to-628-observation-2026-11-01.json",
          "post-628-to-640-observation-2026-11-02.json",
          "post-640-to-653-observation-2026-11-02.json",
          "post-653-to-673-observation-2026-11-03.json",
          "post-673-to-684-observation-2026-11-03.json",
          "post-684-to-711-observation-2026-11-04.json"):
            old.extend(r[0] for r in read(PROV/name)["new_runs"])
        old.extend(r[0] for r in read(TAX/"post-2026-11-04-source-classification.json")["actions"]["new_current_runs"])
        old.extend(r["run_id"] for r in read(PROV/"post-721-to-730-observation-2026-11-05.json")["new_runs"])
        self.assertEqual((len(old),len(set(old))),(730,730))
        d=self.d["action_census"]
        new=[r["run_id"] for r in d["new_runs"]]
        self.assertEqual((len(new),len(set(new))),(20,20))
        self.assertFalse(set(old)&set(new))
        self.assertEqual((d["previous_ids_retained"],d["previous_ids_missing"],d["current_visible"]),(730,[],750))
        self.assertEqual(d["source_page_counts"],[100]*7+[50])

    def test_job_outcomes_and_negative_source_heads(self):
        d=self.d["action_census"]
        self.assertEqual(d["current_conclusions"],{"success":705,"failure":4,"cancelled":41})
        self.assertEqual(d["current_triggers"],{"push":384,"pull_request":318,"schedule":44,"workflow_dispatch":4})
        self.assertEqual(Counter(r["conclusion"] for r in d["new_runs"]),{"success":16,"failure":4})
        self.assertEqual(Counter(r["trigger"] for r in d["new_runs"]),{"push":9,"pull_request":9,"schedule":2})
        all_jobs=[j for r in d["new_runs"] for j in r["jobs"]]
        self.assertEqual(len(all_jobs),46)
        self.assertEqual(Counter(j["conclusion"] for j in all_jobs),{"success":39,"failure":5,"skipped":2})
        self.assertEqual(len({j["job_id"] for j in all_jobs}),46)
        failed=sorted(r["run_id"] for r in d["new_runs"] if r["conclusion"]=="failure")
        self.assertEqual(failed,self.d["failure_repair"]["failed_run_ids"])
        self.assertEqual({r["head_sha"] for r in d["new_runs"] if r["conclusion"]=="failure"},
                         {self.d["failure_repair"]["failing_head_sha"]})
        self.assertEqual({r["run_attempt"] for r in d["new_runs"]},{1})

    def test_pinned_file_lineage_without_mutating_frozen_data(self):
        d=self.d
        prev=read(TAX/"full-file-lifecycle-2026-11-05.json")
        self.assertEqual(prev["source_main_sha"],d["source_previous_sha"])
        self.assertEqual(len(prev["source_commits"]["records"]),256)
        self.assertEqual(len(prev["current_files"]["rows"]),294)
        self.assertEqual(len(prev["historical_only_files"]["rows"]),47)
        c=d["file_census"]
        self.assertEqual((c["prior_ancestor_commits"],c["current_ancestor_commits"]),(256,257))
        self.assertEqual((c["prior_tracked"],c["current_tracked"]),(294,298))
        self.assertEqual(c["prior_historical_only"],47)
        self.assertEqual(len(c["added"]),4)
        self.assertEqual(len(c["modified"]),4)
        self.assertEqual(c["removed"],[])
        old_paths={r["path"] for r in prev["current_files"]["rows"]}
        for row in c["added"]:
            self.assertNotIn(row["path"],old_paths)
            if row["path"].startswith("tests/"):
                # An earlier test file may be repaired by a later PR; the
                # historical Git Blob in the frozen census is not its live SHA.
                self.assertTrue((ROOT/row["path"]).is_file(), row["path"])
                self.assertRegex(row["git_blob_sha"], r"^[0-9a-f]{40}$")
            else:
                # Dated Markdown/JSON provenance and lessons remain immutable.
                self.assertEqual(git_blob(ROOT/row["path"]),row["git_blob_sha"])
        for row in c["modified"]:
            self.assertIn(row["path"],old_paths)
            self.assertNotEqual(row["old_blob_sha"],row["current_blob_sha"])
        self.assertEqual(self.d["pr_census"],{"total":64,"merged":62,"closed_unmerged":[29,32],"open":0,"publishing_pr":64})

    def test_production_and_public_registry_do_not_promote(self):
        d=self.d["accepted_state"]
        self.assertEqual([d[x] for x in ("receipts","events","archived_candidates")],[4,4,3])
        self.assertFalse(d["new_acceptance"])
        self.assertTrue((ROOT/"data/receipts/gh-41436556408-1.json").exists())
        documents=read(ROOT/"evidence/profiles/docs.json")["documents"]
        self.assertIn("docs/provenance/POST_730_TO_750_RECONCILIATION_2026-11-05.md",documents)

if __name__=="__main__": unittest.main()
