"""Offline falsifiers: 788→798 Run/Job census, true fifth native acceptance and historical-prefix integrity."""
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def blob_sha(payload):
    return hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()

class Post788NativeAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = read(PROV / "post-788-to-798-observation-2026-11-09.json")
        cls.previous = read(PROV / "post-768-to-788-observation-2026-11-08.json")
        cls.prior = read(PROV / "post-758-to-768-observation-2026-11-07.json")
        cls.base = read(PROV / "post-750-to-758-observation-2026-11-06.json")

    def test_exact_population_and_identity_nonloss(self):
        c = self.current["action_census"]
        baseline = self.base["action_census"]["current_visible_run_ids"]
        ids = baseline + [x["id"] for x in self.prior["action_census"]["new_runs"]]
        ids += [x["id"] for x in self.previous["action_census"]["new_runs"]]
        additional = [x["id"] for x in c["new_runs"]]
        self.assertEqual((len(set(baseline)), len(set(ids))), (758, 788))
        self.assertEqual((len(additional), len(set(ids + additional))), (10, 798))
        self.assertEqual(set(additional) & set(ids), set())
        self.assertEqual(set(additional), {
            42496690023,42496731464,42496731547,42496731632,
            42496847866,42496847941,42496848029,
            42587589778,42611716908,42621610650})
        self.assertEqual((c["previous_visible"], c["retained_prior_ids"], c["new_count"], c["current_visible"]), (788,788,10,798))
        self.assertEqual(c["missing_prior_ids"], [])
        self.assertEqual(c["source_page_counts"], [100]*7+[98])
        self.assertEqual(c["current_conclusions"], {"success":757,"cancelled":41})
        self.assertEqual(c["current_events"], {"schedule":54,"push":410,"pull_request":330,"workflow_dispatch":4})
        self.assertEqual(Counter(x["event"] for x in c["new_runs"]), {"push":4,"pull_request":3,"schedule":3})

    def test_all_new_jobs_and_bio_gate(self):
        rows = self.current["action_census"]["new_runs"]
        jobs = [j for x in rows for j in x["jobs"]]
        self.assertEqual(len(jobs), 22)
        self.assertEqual(len({j["id"] for j in jobs}), 22)
        self.assertEqual(Counter(j["conclusion"] for j in jobs), {"success":21,"skipped":1})
        self.assertEqual(self.current["action_census"]["new_run_jobs"], {"count":22,"success":21,"skipped":1,"failed":0})
        self.assertTrue(all(x["attempt"]==1 and x["conclusion"]=="success" and len(x["head_sha"])==40 for x in rows))
        skipped = [(x["id"],j["name"]) for x in rows for j in x["jobs"] if j["conclusion"]=="skipped"]
        self.assertEqual(skipped, [(42496847941,"pinned-field")])

    def test_schedule_offsets_are_created_not_queue(self):
        s=self.current["schedule"]
        self.assertEqual((s["previous_verified_runs"],s["previous_verified_success_jobs"],s["current_visible_runs"],s["cross_cutoff_verified_success_jobs"]),(51,79,54,84))
        self.assertEqual([x["offset_seconds"] for x in s["new_scheduled_runs"]],[25134,30229,31373])
        for x in s["new_scheduled_runs"]:
            created = datetime.fromisoformat(x["created_utc"].replace("Z","+00:00"))
            nominal = datetime.fromisoformat(x["nominal_utc"].replace("Z","+00:00"))
            self.assertEqual(int((created-nominal).total_seconds()),x["offset_seconds"])
            run = next(r for r in self.current["action_census"]["new_runs"] if r["id"]==x["run_id"])
            self.assertEqual(run["event"],"schedule")
            self.assertEqual({j["id"] for j in run["jobs"]},set(x["job_ids"]))
            self.assertTrue(all(j["conclusion"]=="success" for j in run["jobs"]))
        self.assertEqual(s["nominal_to_created_cause"],"UNKNOWN")

    def test_frozen_prior_chain_plus_fifth_native_receipt(self):
        record=self.current["accepted_state"]
        self.assertEqual((record["previous_receipts"],record["previous_events"],record["previous_archive_candidates"]),(4,4,3))
        self.assertEqual((record["receipts"],record["chained_events"],record["archived_candidates"]),(5,5,4))
        self.assertEqual((record["outcome"],record["change_kind"]),("APPLIED","DOCUMENT_TEXT_UNCHANGED"))
        raw=(ROOT/"data/knowledge/events.jsonl").read_text(encoding="utf-8").splitlines(keepends=True)
        self.assertGreaterEqual(len(raw),5)
        ids=["gh-38995485443-1","gh-39227185707-1","gh-40297059874-1",
             "gh-41436556408-1","gh-42611716908-1"]
        events=[json.loads(x) for x in raw]
        self.assertEqual([e["run_id"] for e in events[:5]],ids)
        self.assertEqual(events[4]["previous_event_sha256"],events[3]["event_sha256"])
        self.assertEqual(events[4]["event_sha256"],record["latest_event_sha256"])
        self.assertEqual(blob_sha("".join(raw[:5]).encode("utf-8")),
                         record["event_ledger_blob_sha_at_cutoff"])
        receipt=ROOT/record["latest_receipt"]
        self.assertTrue(receipt.is_file())
        self.assertEqual(blob_sha(receipt.read_bytes()),record["latest_receipt_blob_sha"])
        r=read(receipt)
        self.assertEqual(r["execution_id"],"gh-42611716908-1")
        self.assertEqual(r["outcome"],"APPLIED")
        self.assertEqual(r["change_kind"],"DOCUMENT_TEXT_UNCHANGED")
        self.assertEqual(r["current_head"],record["validated_head"])
        self.assertEqual(r["logical_date"],"2026-11-09")
        self.assertTrue((ROOT/record["archived_previous_candidate"]).is_file())
        self.assertGreaterEqual(len(list((ROOT/"data/receipts").glob("gh-*.json"))),5)
        from life_science_ecosystem_lab.lifecycle.state import StateRoots,verify_state
        verification=verify_state(StateRoots(ROOT),require_accepted=True)
        self.assertTrue(verification.valid,verification.errors)

    def test_governance_publication_and_older_archive(self):
        g=self.current["git_scope"]
        self.assertEqual((g["main_reachable_commits"],g["tracked_blob_paths"],g["pull_requests"],g["merged_prs"]),(263,318,70,67))
        self.assertEqual(g["closed_unmerged_prs"],[29,32,67])
        self.assertEqual(g["release_tags"],["v0.4.0","v0.5.0"])
        self.assertFalse(g["main_branch_protected"])
        self.assertEqual(g["repository_rulesets"],[])
        self.assertFalse(self.current["disposition"]["accepted_data_manually_modified"])
        self.assertFalse(self.current["disposition"]["scientific_claim_promoted"])
        self.assertEqual(self.current["negative_evidence"]["historical_disappearance_cause"],"UNKNOWN")
        docs=set(read(ROOT/"evidence/profiles/docs.json")["documents"])
        for p in ("docs/provenance/POST_788_TO_798_RECONCILIATION_2026-11-09.md",
                  "docs/lessons/2026-11-09-frozen-tests-vs-native-continuity.md"):
            self.assertIn(p,docs)
            self.assertTrue((ROOT/p).is_file())

if __name__=="__main__":
    unittest.main()
