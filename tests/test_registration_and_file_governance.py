"""Offline governance regression: frozen file identities and honest OSF planning."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"docs"/"taxonomy"/"current-main-file-disposition-2026-11-07.json"
HISTORY=ROOT/"docs"/"taxonomy"/"full-file-lifecycle-2026-11-05.json"
REG=ROOT/"docs"/"registration"
KNOWN_MAIN="5965f81d133623ea01cd826f25a5c1e48770b6fa"
KNOWN_TREE="b51b497f2f236447503e3e407602abb1f6f02669"
GIT_ROOT="00009a38bc136a7c245270770b005e4e102a870d"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def blob_sha(path):
    b=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+bytes((0,))+b).hexdigest()

def tracked():
    return set(subprocess.check_output(
        ["git","ls-files","-z"],cwd=ROOT).decode("utf-8").rstrip("\0").split("\0"))

class RegistrationAndFileGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load(SOURCE)
        cls.old=load(HISTORY)

    def test_pinned_origin_and_all_current_source_paths_are_classified(self):
        d=self.d
        self.assertEqual(d["source_main_sha"],KNOWN_MAIN)
        self.assertEqual(d["source_git_tree_sha"],KNOWN_TREE)
        self.assertNotEqual(KNOWN_TREE,KNOWN_MAIN)
        self.assertEqual(d["source_git_root_sha"],GIT_ROOT)
        self.assertEqual(d["source_ancestry_commits"],259)
        self.assertEqual((d["source_pr_total"],d["source_pr_merged"]),(66,64))
        self.assertEqual(d["source_pr_closed_unmerged"],[29,32])
        self.assertEqual(d["scope"]["current_tracked_paths"],305)
        self.assertEqual(d["scope"]["previous_full_tree_paths"],294)
        self.assertEqual(d["scope"]["historical_only_path_count"],47)
        self.assertEqual(d["scope"]["unique_current_plus_historical_only_path_names"],352)
        self.assertEqual(len(self.old["current_files"]["rows"]),294)
        self.assertEqual(len(self.old["historical_only_files"]["rows"]),47)
        paths=[r["path"] for r in d["rows"]]
        self.assertEqual(len(paths),305)
        self.assertEqual(len(paths),len(set(paths)))
        self.assertTrue(set(paths)<=tracked())
        self.assertEqual(Counter(r["primary_category"] for r in d["rows"]),
                         d["category_counts"])
        self.assertEqual(Counter(r["review_disposition"] for r in d["rows"]),
                         d["disposition_counts"])
        self.assertTrue(all(re.fullmatch("[0-9a-f]{40}",r["git_blob_sha"])
                            and r["size"]>=0 and r["primary_category"]
                            for r in d["rows"]))
        historic=set(d["historical_only_not_restored"])
        self.assertEqual(historic,{r["path"] for r in
                         self.old["historical_only_files"]["rows"]})
        self.assertFalse(historic & set(paths))
        self.assertFalse(historic & tracked())
        prior={r["path"]:r for r in self.old["current_files"]["rows"]}
        self.assertTrue(set(prior)<=set(paths))
        self.assertEqual(len(d["new_paths_since_previous_ledger"]),11)
        for row in d["rows"]:
            if row["path"] in prior:
                self.assertEqual(row["primary_category"],prior[row["path"]]["category"])
                self.assertEqual(row["source_grade"],"CARRIED_FROM_REVIEWED_FROZEN_CLASSIFICATION")
            else:
                self.assertIn(row["path"],d["new_paths_since_previous_ledger"])
                self.assertEqual(row["source_grade"],"NEW_PATH_RULE_REVIEWED")

    def test_retention_of_archives_and_accepted_state_exact_bytes(self):
        protected={
          "ACCEPTED_STATE_OR_SUPPORTING_PRODUCTION_LAYOUT_PRESERVE",
          "STRUCTURAL_PLACEHOLDER_PRESERVE",
          "DATED_PROVENANCE_PRESERVE",
          "SOURCE_PINNED_TAXONOMY_PRESERVE",
          "PUBLIC_LESSON_PRESERVE",
          "BOUNDED_FIELD_OBSERVATION_PRESERVE"}
        preserved=[r for r in self.d["rows"]
                   if r["review_disposition"] in protected]
        self.assertGreater(len(preserved),70)
        for row in preserved:
            p=ROOT/row["path"]
            self.assertTrue(p.is_file(),row["path"])
            self.assertEqual(blob_sha(p),row["git_blob_sha"],
                             "DO_NOT_REWRITE_FROZEN_WITNESS: "+row["path"])
        self.assertEqual(len(list((ROOT/"data"/"receipts").glob("gh-*.json"))),4)
        self.assertEqual(len(list((ROOT/"data"/"inputs"/"archive").rglob("*.json"))),3)
        self.assertTrue((ROOT/"metadata/biotools-protein-audit.draft.json").exists())

    def test_no_unreviewed_deletion_or_temporary_named_files(self):
        d=self.d["source_path_scan"]
        self.assertEqual(d["temporary_or_cache_name_hits"],[])
        self.assertEqual(d["verified_safe_deletion_candidates"],[])
        self.assertTrue(d["no_known_tracked_temporary_named_files"])
        self.assertEqual(self.d["file_count"] if "file_count" in self.d else 305,305)
        self.assertFalse(any(re.search(
            r"(^|/)(?:__pycache__|build|dist|\.agent-work)(/|$)|(\.pyc|\.tmp|\.bak|\.swp|~)$",
            p) for p in tracked()))
        self.assertFalse(any(p.startswith("docs/superpowers/") for p in tracked()))

    def test_osf_is_preparation_only_and_no_retrospective_relabel(self):
        home=(REG/"README.md").read_text(encoding="utf-8")
        mapping=(REG/"OSF_REGISTRATION_CROSSWALK.md").read_text(encoding="utf-8")
        template=(REG/"RESEARCH_STUDY_PLAN_TEMPLATE.md").read_text(encoding="utf-8")
        self.assertIn("LOCAL_PREPARATION_ONLY",home)
        self.assertIn("NOT_SUBMITTED",mapping)
        self.assertIn("NO_OSF_REGISTRATION_ID_VERIFIED",mapping)
        self.assertIn("NOT SUBMITTED",template)
        self.assertGreaterEqual(template.count("TBD"),18)
        for stage in ("DEFINE","PIN","QUALIFY","EXECUTE",
                      "EVALUATE","AUDIT","REVIEW","REPLAY"):
            self.assertIn(stage,template)
        for term in ("2026-10-16","2026-11-16","2027-02-19"):
            self.assertIn(term,home+mapping)
        for term in ("historical","prospective","retrospective","deviations"):
            self.assertIn(term,home.lower()+mapping.lower()+template.lower())
        self.assertIn("help.osf.io/article/330",home)
        self.assertIn("help.osf.io/article/759",home)
        self.assertIn("osf-partner-support.helpscoutdocs.com",mapping)
        self.assertNotIn("OSF_PREREGISTRATION_ACCEPTED",home+mapping+template)

    def test_all_current_markdown_files_remain_registered(self):
        paths=tracked()
        registered=load(ROOT/"evidence/profiles/docs.json")["documents"]
        self.assertEqual(len(registered),len(set(registered)))
        self.assertEqual({p for p in paths if p.endswith(".md")},set(registered))
        self.assertEqual(self.d["scope"]["current_markdown_paths"],78)
        self.assertEqual(self.d["scope"]["registered_markdown_paths"],78)
        for name in ("README.md","OSF_REGISTRATION_CROSSWALK.md",
                     "RESEARCH_STUDY_PLAN_TEMPLATE.md"):
            self.assertIn("docs/registration/"+name,registered)
        self.assertIn("docs/taxonomy/CURRENT_FILE_DISPOSITION_2026-11-07.md",
                      registered)

if __name__=="__main__":
    unittest.main()
