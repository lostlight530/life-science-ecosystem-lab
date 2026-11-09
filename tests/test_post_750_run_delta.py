"""Independently replay the frozen 750 → current 758 observation without network."""
import json
from collections import Counter
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PROV=ROOT/"docs"/"provenance"
TAX=ROOT/"docs"/"taxonomy"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def old_ids():
    base=load(PROV/"full-history-census-2026-10-31.json")
    ids=[r[0] for r in base["actions"]["records"]]
    for name in (
        "post-598-to-614-observation-2026-10-31.json",
        "post-614-to-628-observation-2026-11-01.json",
        "post-628-to-640-observation-2026-11-02.json",
        "post-640-to-653-observation-2026-11-02.json",
        "post-653-to-673-observation-2026-11-03.json",
        "post-673-to-684-observation-2026-11-03.json",
        "post-684-to-711-observation-2026-11-04.json"
    ):
        ids.extend(r[0] for r in load(PROV/name)["new_runs"])
    ids.extend(r[0] for r in load(TAX/"post-2026-11-04-source-classification.json")["actions"]["new_current_runs"])
    ids.extend(r["run_id"] for r in load(PROV/"post-721-to-730-observation-2026-11-05.json")["new_runs"])
    ids.extend(r["run_id"] for r in load(PROV/"post-730-to-750-observation-2026-11-05.json")["action_census"]["new_runs"])
    return ids

class Post750RunDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load(PROV/"post-750-to-758-observation-2026-11-06.json")

    def test_exact_prior_and_current_run_id_sets(self):
        old=old_ids()
        self.assertEqual((len(old),len(set(old))),(750,750))
        a=self.d["action_census"]
        current=a["current_visible_run_ids"]
        self.assertEqual((len(current),len(set(current))),(758,758))
        self.assertEqual(current,sorted(current))
        self.assertEqual(a["source_page_counts"],[100]*7+[58])
        missing=sorted(set(old)-set(current))
        added=sorted(set(current)-set(old))
        self.assertEqual(missing,[42010968246,42010981438,42010981442,42010981547])
        self.assertEqual(missing,sorted(r["run_id"] for r in a["prior_ids_missing"]))
        self.assertEqual(added,sorted(r["run_id"] for r in a["new_runs"]))
        self.assertEqual((a["previous_visible"],a["prior_ids_retained"],a["new_count"],a["current_visible"]),(750,746,12,758))

    def test_outcomes_job_evidence_and_scientific_nonpromotion(self):
        a=self.d["action_census"]
        self.assertEqual(a["current_conclusions"],{"success":717,"cancelled":41})
        self.assertEqual(a["current_events"],{"schedule":46,"push":390,"pull_request":318,"workflow_dispatch":4})
        self.assertEqual(Counter(r["conclusion"] for r in a["new_runs"]),{"success":12})
        self.assertTrue(all(r["attempt"]==1 for r in a["new_runs"]))
        jobs=[j for r in a["new_runs"] for j in r["jobs"]]
        self.assertEqual(len(jobs),24)
        self.assertEqual(Counter(j["conclusion"] for j in jobs),{"success":23,"skipped":1})
        self.assertEqual(len({j["job_id"] for j in jobs}),24)
        old=load(PROV/"post-730-to-750-observation-2026-11-05.json")
        failures={r["run_id"] for r in old["action_census"]["new_runs"] if r["conclusion"]=="failure"}
        self.assertEqual(failures,{r["run_id"] for r in a["prior_ids_missing"]})
        self.assertTrue(all(r["previous_conclusion"]=="failure" and r["current_get"]=="HTTP_404" for r in a["prior_ids_missing"]))
        self.assertEqual(self.d["native_state"]["receipts"],4)
        self.assertFalse(self.d["native_state"]["new_production_acceptance"])
        self.assertGreaterEqual(len(list((ROOT/"data"/"receipts").glob("gh-*.json"))),4)
        self.assertTrue((ROOT/"data"/"receipts"/"gh-41436556408-1.json").is_file())

    def test_daily_and_periodic_job_boundaries(self):
        s=self.d["scheduled"]
        self.assertEqual((s["total_visible"],s["jobs_success"],s["jobs_other"]),(46,72,0))
        self.assertEqual(s["by_workflow"],{"life-science-bio.yml":3,"life-science-daily-selfcheck.yml":20,
                                          "life-science-continuity.yml":20,"life-science-knowledge.yml":3})
        self.assertEqual(len({x["run_id"] for x in s["runs"]}),46)
        self.assertTrue(all(x["conclusion"]=="success" for x in s["runs"]))
        self.assertEqual(sum(x["jobs_success"] for x in s["runs"]),72)
        self.assertEqual(s["nov_6_daily"]["nominal_to_created_seconds"],24534)
        self.assertEqual(s["nov_6_bio"]["nominal_to_created_seconds"],25585)
        docs=set(load(ROOT/"evidence"/"profiles"/"docs.json")["documents"])
        for path in ("docs/provenance/POST_750_TO_758_RECONCILIATION_2026-11-06.md",
                     "docs/lessons/2026-11-06-visible-history-and-scientific-nonclaims.md"):
            self.assertIn(path,docs)

if __name__=="__main__":
    unittest.main()
