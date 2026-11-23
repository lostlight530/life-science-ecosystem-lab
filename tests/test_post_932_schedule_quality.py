"""Replay pinned 932→939 Run/Job identities and 83 scheduled created-clock observations offline."""
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import statistics
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"
SOURCE = PROV / "post-932-to-939-schedule-quality-2026-11-23.json"
PRIOR = PROV / "post-915-to-932-observation-2026-11-22.json"


def utc(value):
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.utcoffset() != timedelta(0):
        raise ValueError("expected UTC date")
    return dt


class Post932ScheduleQuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.p = json.loads(PRIOR.read_text(encoding="utf-8"))

    def test_source_boundaries_and_net_count_not_exact_set(self):
        d = self.d
        self.assertEqual(d["kind"], "SOURCE_SCOPED_GITHUB_READ_ONLY_RECONCILIATION_AND_SCHEDULE_CLOCK_LEDGER")
        self.assertEqual(d["source_main_sha"], "e5997e4221b6218d0315db9f146c33b289d6f8d7")
        self.assertEqual(d["prior_archive"], str(PRIOR.relative_to(ROOT)))
        self.assertEqual(d["per_request_acquisition_timestamps"], None)
        self.assertFalse(d["acquisition_scope"]["exact_previous_932_vs_current_939_id_set_join"])
        a = d["actions"]
        self.assertEqual(a["prior_visible"]["count"], self.p["actions"]["current_visible"]["count"])
        self.assertEqual((a["prior_visible"]["count"], a["current_visible"]["count"]), (932, 939))
        self.assertEqual(a["net_visible_count_change"], 7)
        self.assertEqual(a["current_visible"]["conclusions"], {"success": 888, "cancelled": 51, "failure": 0})
        self.assertEqual(sum(a["current_visible"]["events"].values()), 939)
        self.assertEqual(a["current_visible"]["events"], {"push": 473, "pull_request": 379, "schedule": 83, "workflow_dispatch": 4})

    def test_seven_post_cutoff_runs_and_seventeen_jobs(self):
        runs = self.d["actions"]["post_cutoff_new_runs"]
        self.assertEqual((len(runs), len(set(r["id"] for r in runs))), (7, 7))
        self.assertEqual(Counter(r["event"] for r in runs), {"push": 4, "pull_request": 3})
        self.assertEqual(Counter(r["conclusion"] for r in runs), {"success": 7})
        self.assertTrue(all(utc(r["created_at_utc"]) > utc(self.p["latest_included_run_created_at_utc"]) for r in runs))
        jobs = [j for r in runs for j in r["jobs"]]
        self.assertEqual((len(jobs), len({j["id"] for j in jobs})), (17, 17))
        self.assertEqual(Counter(j["conclusion"] for j in jobs), {"success": 16, "skipped": 1})
        self.assertEqual([j["id"] for j in jobs if j["conclusion"] == "skipped"], [137251151786])
        self.assertTrue(all(r["attempt"] == 1 for r in runs))

    def test_83_schedule_clock_records_and_date_coverage(self):
        s = self.d["schedules"]
        rows = s["runs"]
        self.assertEqual((len(rows), len({r["id"] for r in rows})), (83, 83))
        self.assertEqual(s["currently_visible_schedule_runs"], 83)
        self.assertEqual(s["observed_latest_attempt_job_conclusions"], {"success": 129})
        self.assertFalse(self.d["acquisition_scope"]["scheduled_129_job_ids_archived"])
        expected = {"daily_selfcheck": (36, "41 1 * * *", 23330),
                    "continuity": (37, "17 4 * * *", 26325),
                    "knowledge": (5, "23 3 * * 1", 28874),
                    "bio": (5, "19 2 * * 5", 25585)}
        self.assertEqual(set(s["cohorts"]), set(expected))
        for key, (count, cron, median) in expected.items():
            cohort = s["cohorts"][key]
            sub = [r for r in rows if r["workflow_key"] == key]
            self.assertEqual((len(sub), cohort["run_count"], cohort["cron_utc"]), (count, count, cron))
            self.assertTrue(all(r["conclusion"] == "success" for r in sub))
            deltas = []
            dates = set()
            for r in sub:
                created = utc(r["created_at_utc"])
                nominal = utc(r["nominal_utc"])
                self.assertEqual(created.date(), nominal.date())
                self.assertEqual((created - nominal).total_seconds(), r["created_minus_nominal_seconds"])
                self.assertGreaterEqual(r["created_minus_nominal_seconds"], 0)
                self.assertEqual((nominal.minute, nominal.hour), tuple(map(int, cron.split()[:2])))
                if key == "knowledge":
                    self.assertEqual(created.weekday(), 0)
                if key == "bio":
                    self.assertEqual(created.weekday(), 4)
                dates.add(created.date())
                deltas.append(r["created_minus_nominal_seconds"])
            self.assertEqual(statistics.median(deltas), median)
            self.assertEqual(statistics.median(deltas), cohort["median_created_offset_seconds"])
            self.assertEqual(min(deltas), cohort["min_created_offset_seconds"])
            self.assertEqual(max(deltas), cohort["max_created_offset_seconds"])
            first, last = min(dates), max(dates)
            self.assertEqual((first.isoformat(), last.isoformat()),
                             (cohort["first_observed_utc_day"], cohort["last_observed_utc_day"]))
            day, missing = first, []
            while day <= last:
                due = key in {"daily_selfcheck", "continuity"} or (key == "knowledge" and day.weekday() == 0) or (key == "bio" and day.weekday() == 4)
                if due and day not in dates:
                    missing.append(day.isoformat())
                day += timedelta(days=1)
            self.assertEqual(missing, cohort["missing_expected_dates_within_observed_span"])
            self.assertFalse(missing)

    def test_production_prefix_and_historical_failure_non_erasure(self):
        p = self.d["production"]
        self.assertEqual((p["accepted_event_count"], p["receipt_count"]), (6, 6))
        self.assertEqual((p["graph_entities"], p["graph_relations"]), (17, 26))
        self.assertEqual(p["new_accepted_science_claims"], 0)
        ev = [json.loads(x) for x in (ROOT / "data/knowledge/events.jsonl").read_text(encoding="utf-8").splitlines() if x]
        self.assertGreaterEqual(len(ev), 6)
        self.assertTrue(all(x["outcome"] == "APPLIED" for x in ev[:6]))
        self.assertEqual(ev[5]["run_id"], p["last_accepted_execution_id"])
        self.assertTrue(all(ev[i]["previous_event_sha256"] == ev[i-1]["event_sha256"] for i in range(1, 6)))
        n = self.d["negative_controls"]
        self.assertEqual(n["historic_failed_run_ids_with_current_http_404"], [43919536363, 43919549660, 43919549686, 43919549907])
        self.assertEqual(n["historic_cancelled_parent_containing_failed_job"]["job_conclusion"], "failure")
        self.assertEqual(n["root_cause_for_schedule_offsets"], "UNKNOWN")
        self.assertTrue(any("not independently measured" in x for x in self.d["limits"]) or
                        "not independently measured" in self.d["schedules"]["offset_semantics"])

    def test_historical_assets_and_scheduler_unchanged(self):
        self.assertTrue(self.d["acquisition_scope"]["github_actions_native_cron_unchanged"])
        self.assertEqual(self.d["git"]["current_main_reachable_commits"], 327)
        self.assertEqual(self.d["git"]["current_prs"], 83)
        self.assertIn("branch protection", " ".join(self.d["limits"]).lower())
        for key in self.d["schedules"]["schedule_definitions"]:
            self.assertIn("cron_utc", self.d["schedules"]["schedule_definitions"][key])
        lesson = (ROOT / "docs/lessons/2026-11-23-schedule-time-observability.md").read_text(encoding="utf-8")
        report = (PROV / "POST_932_TO_939_SCHEDULE_QUALITY_2026-11-23.md").read_text(encoding="utf-8")
        self.assertIn("SCHEDULER_CAUSE_UNKNOWN", lesson)
        self.assertIn("NO_CRON_CHANGE", report)
        self.assertNotIn("GitHub outage confirmed", report)

if __name__ == "__main__":
    unittest.main()
