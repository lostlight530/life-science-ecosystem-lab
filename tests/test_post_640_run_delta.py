"""Offline falsifier for the frozen 640→653 GitHub census and native #4 acceptance.

Historical GitHub API observations are immutable. Current accepted data is
append-only and may advance beyond this cutoff without breaking old tests.
No network, external research, or model execution is required.
"""
from collections import Counter
from pathlib import Path
import json
import shutil
import tempfile
import unittest

from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "docs" / "provenance"


def read(name):
    return json.loads((P / name).read_text(encoding="utf-8"))


class Post640RunDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = read("full-history-census-2026-10-31.json")
        cls.d1 = read("post-598-to-614-observation-2026-10-31.json")
        cls.d2 = read("post-614-to-628-observation-2026-11-01.json")
        cls.d3 = read("post-628-to-640-observation-2026-11-02.json")
        cls.current = read("post-640-to-653-observation-2026-11-02.json")

    def test_exact_frozen_population_closure(self):
        previous = ([r[0] for r in self.base["actions"]["records"]]
                    + [r[0] for d in (self.d1, self.d2, self.d3)
                       for r in d["new_runs"]])
        added = [r[0] for r in self.current["new_runs"]]
        self.assertEqual([len(self.base["actions"]["records"]),
                          len(self.d1["new_runs"]), len(self.d2["new_runs"]),
                          len(self.d3["new_runs"]), len(added)],
                         [598, 16, 14, 12, 13])
        self.assertEqual(len(set(previous)), 640)
        self.assertEqual(len(set(added)), 13)
        self.assertFalse(set(previous) & set(added))
        self.assertEqual(len(set(previous + added)), 653)
        self.assertEqual(self.current["old_ids_retained"], 640)
        self.assertEqual(self.current["old_ids_missing"], [])
        self.assertEqual(self.current["page_counts"], [100] * 6 + [53])
        self.assertEqual(sum(self.current["page_counts"]), 653)
        self.assertIsNone(self.current["exact_http_read_timestamp_utc"])

    def test_run_and_schedule_grain_not_scientific_claims(self):
        record = self.current
        new = record["new_runs"]
        self.assertEqual(Counter(x[2] for x in new),
                         Counter({"push": 7, "pull_request": 3, "schedule": 3}))
        self.assertEqual({x[5] for x in new}, {"success"})
        self.assertEqual(sum(record["visible_events"].values()), 653)
        self.assertEqual(sum(record["visible_conclusions"].values()), 653)
        self.assertEqual(record["visible_conclusions"],
                         {"success": 612, "cancelled": 41, "failure": 0})
        schedule = record["scheduled_by_workflow"]
        self.assertEqual(sum(schedule.values()), 38)
        expected_jobs = (schedule["life-science-continuity.yml"]
                         + 2 * schedule["life-science-daily-selfcheck.yml"]
                         + 2 * schedule["life-science-knowledge.yml"]
                         + 2 * schedule["life-science-bio.yml"])
        self.assertEqual(expected_jobs, 59)
        self.assertEqual(len(record["jobs_new_schedules"]), 3)
        self.assertEqual(sum(len(x["jobs"]) for x in record["jobs_new_schedules"]), 5)
        for x in record["jobs_new_schedules"]:
            self.assertTrue(all(job["conclusion"] == "success" for job in x["jobs"]))
        self.assertEqual(record["bio_job_gate"]["pinned_field"], "skipped")
        self.assertEqual(record["bio_job_gate"]["pr_pinned_field"], "success")
        self.assertEqual(record["negative_and_unknown"]["scientific_new_claim"],
                         "NONE_VERIFIED")

    def test_native_fourth_acceptance_is_historical_prefix(self):
        snapshot = self.current["production"]
        self.assertEqual((snapshot["accepted_receipts"], snapshot["event_lines"],
                          snapshot["archived_candidates"]), (4, 4, 3))
        events = [json.loads(s) for s in
                  (ROOT / "data/knowledge/events.jsonl")
                  .read_text(encoding="utf-8").splitlines() if s.strip()]
        self.assertGreaterEqual(len(events), 4)
        expected = [38995485443, 39227185707, 40297059874, 41436556408]
        self.assertEqual([s["run_id"] for s in events[:4]],
                         [f"gh-{i}-1" for i in expected])
        self.assertIsNone(events[0]["previous_event_sha256"])
        for a, b in zip(events, events[1:]):
            self.assertEqual(b["previous_event_sha256"], a["event_sha256"])
        for event in events[:4]:
            receipt = ROOT / "data" / "receipts" / (event["run_id"] + ".json")
            self.assertTrue(receipt.is_file())
            body = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(body["outcome"], "APPLIED")
            self.assertEqual(body["execution_id"], event["run_id"])
            self.assertEqual(body["snapshot_id"], event["snapshot_id"])
        self.assertEqual(events[3]["change_kind"], "DOCUMENT_TEXT_UNCHANGED")
        fourth = json.loads((ROOT / snapshot["latest_receipt"])
                            .read_text(encoding="utf-8"))
        self.assertEqual(fourth["current_head"],
                         "d339e4d9dcac8b4b5e1ee215dde0edcbf775dc1b")
        self.assertEqual(fourth["validated_head"], fourth["current_head"])
        self.assertTrue((ROOT / "data/inputs/archive/2026/11"
                        / "4a9aeb43c99dadb6-787471b78dfe37c2-0a20ce424193.json")
                        .is_file())

    def test_latest_accepted_state_is_verified_not_just_present(self):
        # This test is deliberately evaluated against the moving real data/
        # independently from the old, frozen API population.
        report = verify_state(StateRoots(ROOT), require_accepted=True)
        self.assertTrue(report.valid, report.errors)

    def test_receipt_tamper_fails_closed_in_isolated_copy(self):
        # Negative control: never modify real, accepted data/.
        with tempfile.TemporaryDirectory() as directory:
            isolated = Path(directory)
            shutil.copytree(ROOT / "data", isolated / "data")
            roots = StateRoots(isolated)
            baseline = verify_state(roots, require_accepted=True)
            self.assertTrue(baseline.valid, baseline.errors)
            events = (isolated / "data/knowledge/events.jsonl").read_text(
                encoding="utf-8").splitlines()
            latest = json.loads(events[-1])
            receipt_path = isolated / "data" / "receipts" / (latest["run_id"] + ".json")
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["output_digest"] = "0" * 64
            receipt_path.write_text(
                json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8")
            invalid = verify_state(roots, require_accepted=True)
            self.assertFalse(invalid.valid)
            self.assertIn(
                "latest accepted receipt does not match graph event",
                invalid.errors)

    def test_historical_negative_provenance_remains_visible(self):
        d = self.current["negative_and_unknown"]
        self.assertEqual(d["historical_failed_runs_in_older_archive"], 8)
        self.assertEqual(d["historical_temporal_name_corrections"], 134)
        self.assertEqual(d["historical_schedule_median_corrections"], 2)
        self.assertEqual(d["scheduler_root_cause"], "UNKNOWN")
        self.assertEqual(d["external_registry_parity"], "UNKNOWN")
        self.assertEqual(self.current["repository_census"]["prs_closed_unmerged"],
                         [29, 32])
        self.assertEqual(self.current["decision"]["scientific_assets"],
                         "NO_CHANGE_REQUIRED")


if __name__ == "__main__":
    unittest.main()
