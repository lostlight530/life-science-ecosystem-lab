"""Offline replay of three distinct dated observations of GitHub Actions.

No API calls, production writes, institutional claims or scientific conclusions.
The fixed 531/547/563 populations are historical, not 'current' GitHub totals.
"""
import json
import statistics
import unittest
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "provenance"

WORKFLOW_CRONS = {
    ".github/workflows/life-science-knowledge.yml": (3, 23),
    ".github/workflows/life-science-continuity.yml": (4, 17),
    ".github/workflows/life-science-daily-selfcheck.yml": (1, 41),
    ".github/workflows/life-science-bio.yml": (2, 19),
}

WORKFLOW_NAMES = {
    "Life Science Knowledge Workflow — Native Lifecycle":
        ".github/workflows/life-science-knowledge.yml",
    "Verify accepted life-science knowledge continuity":
        ".github/workflows/life-science-continuity.yml",
    "Daily research self-check — Institutional defaults and project custom":
        ".github/workflows/life-science-daily-selfcheck.yml",
    "Life Science Bio Tool — Independent Data Processing":
        ".github/workflows/life-science-bio.yml",
}


def read(name):
    return json.loads((ARCHIVE / name).read_text(encoding="utf-8"))


def utc(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert result.utcoffset().total_seconds() == 0
    return result


class PostScheduleObservationReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = read("actions-visible-index-2026-10-30.json")
        cls.mid = read("post-merge-observation-2026-10-30.json")
        cls.last = read("post-schedule-observation-2026-10-30.json")
        cls.daily = read("native-daily-quality-2026-10-30.json")
        cls.original_failure_snapshot = read("action-runs-2026-10-30.json")

    def replay(self):
        """Decode per-run source rows; do not join historic names by workflow ID."""
        prior = {}
        for run_id, workflow_id, event_code, created, conclusion_code in self.index["records"]:
            self.assertNotIn(run_id, prior)
            prior[run_id] = {
                "event": self.index["event_codes"][event_code],
                "conclusion": self.index["conclusion_codes"][conclusion_code],
                "created_at_utc": created,
                "workflow_id": workflow_id,
            }
        self.assertEqual(len(prior), 531)
        for name, obj, expected_before in (
            ("mid", self.mid, 531),
            ("last", self.last, 547),
        ):
            self.assertEqual(len(prior), expected_before, name)
            self.assertEqual(obj["previous_count"] if name == "last" else obj["earlier_count"], expected_before)
            new = obj["new_run_records"]
            self.assertEqual(len(new), obj["new_count"])
            self.assertEqual(len({x["id"] for x in new}), len(new))
            self.assertFalse(set(prior) & {x["id"] for x in new})
            self.assertEqual(obj["previous_ids_absent"], [])
            self.assertEqual(obj["previous_id_event_or_outcome_changes"], [])
            for x in new:
                self.assertEqual(x["conclusion"], "success")
                self.assertEqual(x["attempt"], 1)
                self.assertEqual(len(x["head_sha"]), 40)
                self.assertTrue(x["path"].startswith(".github/workflows/") if "path" in x else True)
                prior[x["id"]] = x
            self.assertEqual(len(prior), obj["current_count"])
            self.assertEqual(Counter(x["event"] for x in prior.values()), obj["current_events"])
            self.assertEqual(Counter(x["conclusion"] for x in prior.values()), obj["current_conclusions"])
        return prior

    def test_exact_id_replay_and_old_negative_evidence(self):
        result = self.replay()
        self.assertEqual(len(result), 563)
        self.assertEqual(Counter(x["event"] for x in result.values()),
                         {"push": 266, "pull_request": 262,
                          "schedule": 31, "workflow_dispatch": 4})
        self.assertEqual(Counter(x["conclusion"] for x in result.values()),
                         {"success": 522, "cancelled": 41})
        self.assertEqual(self.last["observation_day_utc"], "2026-10-30")
        self.assertIsNone(self.last["observed_at_utc"])
        self.assertIn("Exact original", self.last["observation_clock_limitation"])
        self.assertEqual(len(self.last["source_urls"]), 6)
        failures = [x["id"] for x in self.original_failure_snapshot["records"]
                    if x["conclusion"] == "failure"]
        self.assertEqual(len(failures), 8)
        self.assertTrue(set(failures).isdisjoint(result))

    def test_scheduled_jobs_and_day_are_not_production_writes(self):
        result = self.replay()
        old = self.daily["scheduled_runs"]
        new_jobs = self.last["new_scheduled_job_observations"]
        old_scheduled_ids = {x["id"] for x in old}
        self.assertEqual(len(old_scheduled_ids), 28)
        self.assertEqual(len(new_jobs), 3)
        new_ids = {x["run_id"] for x in new_jobs}
        self.assertFalse(old_scheduled_ids & new_ids)
        scheduled_ids = {run_id for run_id, x in result.items()
                         if x["event"] == "schedule"}
        self.assertEqual(old_scheduled_ids | new_ids, scheduled_ids)
        self.assertEqual(len(scheduled_ids), 31)
        old_job_count = sum(len(x["verified_jobs_from_job_list"]) for x in old)
        new_job_count = sum(len(x["jobs"]) for x in new_jobs)
        self.assertEqual((old_job_count, new_job_count), (43, 5))
        for record in old:
            self.assertEqual(record["conclusion"], "success")
            self.assertTrue(all(j["conclusion"] == "success"
                                for j in record["verified_jobs_from_job_list"]))
        for record in new_jobs:
            self.assertEqual(result[record["run_id"]]["event"], "schedule")
            self.assertEqual(result[record["run_id"]]["conclusion"], "success")
            self.assertTrue(all(j["conclusion"] == "success" and j["id"] > 0
                                for j in record["jobs"]))
            created = utc(result[record["run_id"]]["created_at_utc"])
            # Oct 30 UTC entries are all Oct 30 local; not an activation SLA.
            self.assertEqual((created.hour + 8) // 24, 0)
            self.assertEqual(created.day, 30)
        self.assertEqual(old_job_count + new_job_count, 48)
        receipts = self.last["production_acceptance_receipts"]
        self.assertEqual(len(receipts), 3)
        self.assertEqual({x["run_id"] for x in self.daily["accepted_native_execution_receipts"]},
                         {38995485443, 39227185707, 40297059874})
        for receipt in receipts:
            self.assertTrue((ROOT / receipt).is_file())

    def test_cron_offsets_are_recomputed_by_population_not_copied(self):
        rows = self.daily["scheduled_runs"]
        grouped = defaultdict(list)
        for r in rows:
            path = WORKFLOW_NAMES[r["workflow"]]
            grouped[path].append(utc(r["created_at_utc"]))
        all_new = {x["id"]: x for x in self.last["new_run_records"]}
        for group in self.last["new_scheduled_job_observations"]:
            run = all_new[group["run_id"]]
            grouped[run["path"]].append(utc(run["created_at_utc"]))
        expected = {
            ".github/workflows/life-science-knowledge.yml": (2, 342.01),
            ".github/workflows/life-science-continuity.yml": (14, 312.07),
            ".github/workflows/life-science-daily-selfcheck.yml": (13, 309.05),
            ".github/workflows/life-science-bio.yml": (2, 347.60),
        }
        self.assertEqual(set(grouped), set(expected))
        for path, datetimes in grouped.items():
            hour, minute = WORKFLOW_CRONS[path]
            offsets = []
            for t in datetimes:
                nominal = t.replace(hour=hour, minute=minute, second=0, microsecond=0)
                offsets.append(round((t - nominal).total_seconds() / 60, 2))
            expected_n, expected_median = expected[path]
            self.assertEqual(len(offsets), expected_n)
            self.assertAlmostEqual(statistics.median(offsets), expected_median, places=2)
        self.assertEqual(sum(len(a) for a in grouped.values()), 31)

    def test_warning_retained_and_caveat_boundary(self):
        logs = self.last["independent_field_log_observations"]
        self.assertEqual(len(logs), 3)
        fasta = next(x for x in logs if x.get("python_unittest_passed"))
        self.assertEqual(fasta["fasta_status"], "WARN_UNCERTAIN_RESIDUES")
        self.assertEqual(fasta["pdb_status"], "PASS")
        self.assertEqual(fasta["python_unittest_passed"], 180)
        field = next(x for x in logs if "log_marker" in x
                     and "PINNED" in x["log_marker"])
        self.assertTrue(field["log_marker"].endswith(" 6"))
        self.assertTrue(all(x["source_grade"] == "RUNNER_JOB_LOG_READ"
                            for x in logs))
        self.assertTrue(any("not proven" in str(x).lower()
                            for x in self.last["caveats"]))


if __name__ == "__main__":
    unittest.main()
