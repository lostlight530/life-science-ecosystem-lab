"""Offline frozen source replay for the full first-day-to-main file lifecycle."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest
from accepted_production_history import authorized_native_append_paths

ROOT=Path(__file__).resolve().parents[1]
TAX=ROOT/"docs"/"taxonomy"
H="18c33998a78ff64537d993bd7d7408c5a5da0cf3"
ORIGIN="00009a38bc136a7c245270770b005e4e102a870d"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def git_blob(path):
    b=path.read_bytes()
    header=b"blob "+str(len(b)).encode("ascii")+bytes((0,))
    return hashlib.sha1(header+b).hexdigest()

class FullFirstDayFileLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obs=read(TAX/"full-file-lifecycle-2026-11-05.json")
        cls.base=read(TAX/"file-register-2026-11-03.json")
        cls.overlay=read(TAX/"post-2026-11-04-source-classification.json")
        cls.comm=read(TAX/"commit-register-2026-11-03.json")
        cls.pr=read(TAX/"pr-register-2026-11-03.json")
        cls.exact_path_categories = {
            row["path"]: row["category"]
            for row in read(TAX/"current-exact-path-classifications.json")["entries"]
        }

    def test_main_commit_ancestry_and_tree_identity(self):
        d=self.obs
        self.assertEqual(d["source_main_sha"],H)
        self.assertEqual(d["source_root_sha"],ORIGIN)
        rows=d["source_commits"]["records"]
        self.assertEqual(len(rows),256)
        ids={r["sha"] for r in rows}
        self.assertEqual(len(ids),256)
        self.assertEqual(rows[0]["sha"],H)
        self.assertEqual({r["sha"] for r in rows if not r["parents"]},{ORIGIN})
        self.assertTrue(all(set(r["parents"])<=ids for r in rows))
        self.assertEqual(len({r["tree_sha"] for r in rows}),235)
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{40}",r["sha"])
                            and re.fullmatch(r"[0-9a-f]{40}",r["tree_sha"])
                            for r in rows))
        frozen={r["sha"]:r for r in self.comm["commits"]}
        self.assertEqual(len(frozen),250)
        for r in rows:
            if r["sha"] in frozen:
                self.assertEqual(r["parents"],frozen[r["sha"]]["parents"])
        overlay={r["sha"]:r for r in self.overlay["post_baseline_main_commits"]}
        self.assertEqual(len(overlay),4)
        self.assertTrue(set(overlay)<=ids)
        self.assertEqual(len(ids-set(frozen)-set(overlay)),2)

    def test_pr_disposition_and_frozen_identity(self):
        p=self.obs["source_prs"]
        rows=p["records"]
        self.assertEqual(len(rows),63)
        self.assertEqual(sorted(r["number"] for r in rows),list(range(1,64)))
        self.assertEqual(Counter(r["merged"] for r in rows),{True:61,False:2})
        self.assertEqual([r["number"] for r in rows if not r["merged"]],[29,32])
        self.assertEqual(p["open"],0)
        old={r["number"]:r for r in self.pr["prs"]}
        for row in rows:
            self.assertTrue(row["original_title"])
            if row["number"] in old:
                self.assertEqual(row["original_title"],old[row["number"]]["original_title"])
        self.assertEqual(len(old),57)

    def test_every_live_file_has_a_role_and_frozen_comparison(self):
        d=self.obs["current_files"]
        rows=d["rows"]
        self.assertEqual(len(rows),294)
        paths={r["path"] for r in rows}
        self.assertEqual(len(paths),294)
        self.assertEqual(d["baseline_2026_11_03"],274)
        self.assertEqual(d["post_baseline_2026_11_04"],13)
        self.assertEqual(d["unclassified_count"],0)
        self.assertEqual(d["missing_frozen_paths"],[])
        self.assertEqual(len(d["changed_living_paths"]),10)
        previous={r["path"]:r for r in self.base["files"]+self.overlay["post_baseline_files"]}
        self.assertEqual(len(previous),287)
        self.assertTrue(set(previous)<=paths)
        categories={"docs/provenance/":"HISTORICAL_PROVENANCE",
                    "docs/taxonomy/":"HISTORICAL_PROVENANCE",
                    "docs/lessons/":"PUBLIC_RESEARCH_LESSONS",
                    "tests/":"VALIDATION_AND_REGRESSION"}
        for r in rows:
            self.assertTrue(r["category"] and r["role"])
            self.assertRegex(r["git_blob_sha"],r"^[a-f0-9]{40}$")
            self.assertGreaterEqual(r["size"],0)
            if r["path"] in previous:
                self.assertEqual(r["category"],previous[r["path"]]["category"])
                oldsha=previous[r["path"]]["git_blob_sha"]
                self.assertEqual(r.get("frozen_blob_sha",oldsha),oldsha)
            else:
                matches=[c for prefix,c in categories.items()
                         if r["path"].startswith(prefix)]
                if r["path"] in self.exact_path_categories:
                    matches.append(self.exact_path_categories[r["path"]])
                self.assertEqual(matches,[r["category"]])
        self.assertEqual(sorted(r["path"] for r in rows if "frozen_blob_sha" in r),
                         sorted(d["changed_living_paths"]))
        tracked=set(subprocess.check_output(["git","ls-files"],cwd=ROOT,text=True).splitlines())
        self.assertTrue(paths<=tracked)
        production_append = authorized_native_append_paths(ROOT)
        for path in tracked-paths:
            matches = (sum(path.startswith(p) for p in categories)
                       + int(path in self.exact_path_categories)
                       + int(path in production_append and path.startswith("data/")))
            self.assertEqual(matches,1,"NEW_PATH_REQUIRES_REVIEWED_CLASS: "+path)
        registered=set(read(ROOT/"evidence/profiles/docs.json")["documents"])
        markdown={p for p in tracked if p.endswith(".md")}
        self.assertEqual(markdown,registered)
        self.assertEqual(d["current_markdown_count"],73)
        self.assertEqual(d["registered_markdown_count"],73)
        self.assertEqual(d["unregistered_markdown_paths"],[])
        self.assertEqual(d["nonexistent_registry_paths"],[])

    def test_historical_only_path_witness_and_exact_bytes(self):
        d=self.obs["historical_only_files"]
        historic=d["rows"]
        self.assertEqual(len(historic),47)
        self.assertEqual(len({r["path"] for r in historic}),47)
        active={r["path"]:r for r in self.obs["current_files"]["rows"]}
        sha_set={r["tree_sha"] for r in self.obs["source_commits"]["records"]}
        self.assertFalse(set(active)&{r["path"] for r in historic})
        self.assertEqual(sum(bool(r["content_identical_current_paths"])
                             for r in historic),19)
        for r in historic:
            self.assertIn(r["witness_tree_sha"],sha_set)
            self.assertRegex(r["historical_git_blob_sha"],r"^[a-f0-9]{40}$")
            for path in r["content_identical_current_paths"]:
                self.assertEqual(active[path]["git_blob_sha"],r["historical_git_blob_sha"])
        self.assertEqual(
            {r["path"] for r in historic if r["path"] in {
              ".lifemonitor.yaml","tests/test_daily_selfcheck.py",
              "bio_tool/tabular.py",
              "evidence/field-tests/2026-10-17-first-accepted-cycle.json"}},
            {".lifemonitor.yaml","tests/test_daily_selfcheck.py",
             "bio_tool/tabular.py",
             "evidence/field-tests/2026-10-17-first-accepted-cycle.json"})

    def test_immutable_dated_json_not_silently_overwritten(self):
        immutable=[r for r in self.obs["current_files"]["rows"] if
                   (r["path"].startswith("docs/provenance/")
                    or r["path"].startswith("docs/taxonomy/"))
                   and r["path"].endswith(".json")]
        self.assertGreater(len(immutable),20)
        for row in immutable:
            self.assertEqual(git_blob(ROOT/row["path"]),row["git_blob_sha"],
                             "FROZEN_ARCHIVE_REQUIRES_ADDITIVE_CORRECTION: "+row["path"])
        self.assertTrue((ROOT/"data/receipts/gh-41436556408-1.json").is_file())

if __name__=="__main__": unittest.main()
