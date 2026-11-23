"""Replay bounded 939→949 GitHub Runs, schedule clocks and seventh accepted event."""
from collections import Counter
from datetime import datetime, timedelta
import json
from pathlib import Path
import statistics
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"
CURRENT = PROV / "post-939-to-949-observation-2026-11-24.json"
PREVIOUS = PROV / "post-932-to-939-schedule-quality-2026-11-23.json"


def utc(stamp):
    parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    if parsed.utcoffset() != timedelta(0):
        raise ValueError("timestamp must identify UTC")
    return parsed


class Post939NativeReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = json.loads(CURRENT.read_text(encoding="utf-8"))
        cls.previous = json.loads(PREVIOUS.read_text(encoding="utf-8"))

    def test_source_and_population_are_explicitly_bounded(self):
        d = self.current
        self.assertEqual(d["kind"], "SOURCE_SCOPED_GITHUB_RUN_JOB_AND_SEVENTH_ACCEPTED_LIFECYCLE_REPLAY")
        self.assertEqual(d["source_main_sha"], "c11343ece9ac3671700bb533cbf4eb00afac4d12")
        self.assertEqual(d["prior_archive"], str(PREVIOUS.relative_to(ROOT)))
        self.assertIsNone(d["per_request_acquisition_timestamps"])
        self.assertFalse(d["acquisition_scope"]["exact_prior_939_id_set_join"])
        self.assertFalse(d["acquisition_scope"]["prior_129_schedule_job_ids_not_fully_frozen"] is False)
        prior = d["actions"]["prior_visible"]
        curr = d["actions"]["current_visible"]
        self.assertEqual(prior, self.previous["actions"]["current_visible"])
        self.assertEqual((prior["count"], curr["count"], d["actions"]["net_visible_count_change"]), (939, 949, 10))
        self.assertEqual(curr["conclusions"], {"success": 898, "cancelled": 51, "failure": 0})
        self.assertEqual(curr["events"], {"push": 477, "pull_request": 382, "schedule": 86, "workflow_dispatch": 4})
        self.assertEqual(sum(curr["events"].values()), 949)
        self.assertEqual(d["git"]["pr_total"], 84)
        self.assertEqual(d["git"]["pr_merged"], 80)
        self.assertEqual(d["git"]["closed_unmerged_prs"], [29, 32, 67, 78])
        self.assertEqual((d["git"]["tracked_blob_paths"], d["git"]["recursive_tree_entries"]), (356, 407))

    def test_ten_exact_run_and_job_witnesses(self):
        d = self.current
        runs = d["actions"]["post_cutoff_new_runs"]
        self.assertEqual((len(runs), len({r["id"] for r in runs})), (10, 10))
        self.assertEqual({r["id"] for r in runs}, {
            45111769410, 45111810489, 45111810482, 45111810462,
            45111889828, 45111889816, 45111889811, 45150173180,
            45181050512, 45198977184,
        })
        self.assertEqual(Counter(r["event"] for r in runs), {"push": 4, "pull_request": 3, "schedule": 3})
        self.assertTrue(all(r["conclusion"] == "success" and r["attempt"] == 1 for r in runs))
        cutoff = utc(self.previous["latest_included_run_created_at_utc"])
        end = utc(d["latest_included_run_created_at_utc"])
        self.assertTrue(all(cutoff < utc(r["created_at_utc"]) <= end for r in runs))
        jobs = [j for r in runs for j in r["jobs"]]
        self.assertEqual((len(jobs), len({j["id"] for j in jobs})), (22, 22))
        self.assertEqual(Counter(j["conclusion"] for j in jobs), {"success": 21, "skipped": 1})
        self.assertEqual(d["actions"]["post_cutoff_latest_attempt_job_count"], 22)
        self.assertEqual(d["actions"]["post_cutoff_latest_attempt_job_conclusions"], {"success": 21, "skipped": 1})
        self.assertEqual([j["id"] for j in jobs if j["conclusion"] == "skipped"], [137485885479])
        bio = next(r for r in runs if r["id"] == 45111889828)
        self.assertEqual(bio["event"], "push")
        self.assertEqual({j["name"]: j["conclusion"] for j in bio["jobs"]},
                         {"offline": "success", "pinned-field": "skipped"})

    def test_native_clock_witnesses_and_day_coverage(self):
        d = self.current
        old = self.previous["schedules"]["runs"]
        new = d["schedules"]["new_schedule_runs"]
        self.assertEqual((len(old), len(new), len(old) + len(new)), (83, 3, 86))
        self.assertEqual({r["id"] for r in new}, {45150173180, 45181050512, 45198977184})
        self.assertEqual(d["schedules"]["current_visible_schedule_run_count"], 86)
        self.assertEqual(d["schedules"]["new_schedule_job_success_count"], 5)
        self.assertEqual(d["schedules"]["prior_job_success_count_from_prior_review"], 129)
        expected = {"daily_selfcheck": (37, 23900), "continuity": (38, 26943),
                    "knowledge": (6, 29375.5), "bio": (5, 25585)}
        for key, (total, median) in expected.items():
            subset = [r for r in old + new if r["workflow_key"] == key]
            current = d["schedules"]["current_cohorts"][key]
            self.assertEqual((len(subset), current["run_count"]), (total, total))
            self.assertEqual(current["median_created_offset_seconds"], median)
            nominal = current["cron_utc"].split(" ")
            diffs = []
            days = set()
            for r in subset:
                created_time, nominal_time = utc(r["created_at_utc"]), utc(r["nominal_utc"])
                self.assertEqual(created_time.date(), nominal_time.date())
                self.assertEqual((created_time - nominal_time).total_seconds(), r["created_minus_nominal_seconds"])
                self.assertEqual((nominal_time.minute, nominal_time.hour), (int(nominal[0]), int(nominal[1])))
                self.assertEqual(r["conclusion"], "success")
                days.add(created_time.date())
                diffs.append(r["created_minus_nominal_seconds"])
            self.assertEqual(statistics.median(diffs), median)
            self.assertEqual(min(diffs), current["min_created_offset_seconds"])
            self.assertEqual(max(diffs), current["max_created_offset_seconds"])
            day, last = min(days), max(days)
            while day <= last:
                due = key in {"daily_selfcheck", "continuity"} or (
                    key == "knowledge" and day.weekday() == 0
                ) or (key == "bio" and day.weekday() == 4)
                if due:
                    self.assertIn(day, days, f"missing native {key} schedule {day}")
                day += timedelta(days=1)
        self.assertEqual(
            {r["workflow_key"]: r["created_minus_nominal_seconds"] for r in new},
            {"daily_selfcheck": 29180, "knowledge": 35165, "continuity": 38159}
        )
        self.assertEqual(d["schedules"]["cause"], "UNKNOWN")
        self.assertTrue(d["schedules"]["created_minus_nominal_is_not_queue_duration"])

    def test_seventh_receipt_and_frozen_event_prefix(self):
        p = self.current["production"]
        self.assertEqual((p["previous_event_count"], p["event_count"]), (6, 7))
        self.assertEqual((p["run_id"], p["run_attempt"], p["outcome"], p["change_kind"]),
                         (45181050512, 1, "APPLIED", "DOCUMENT_TEXT_UNCHANGED"))
        self.assertEqual(p["validated_head"], "e813369d4d12dd676e123e21cd13c609255e5670")
        self.assertEqual(p["accepted_commit"], self.current["source_main_sha"])
        self.assertEqual((p["graph_entities"], p["graph_relations"]), (17, 26))
        self.assertNotEqual(p["previous_knowledge_digest"], p["knowledge_digest"])
        self.assertIn({"topic_id": "workflow-monitoring", "state": "UPDATED"}, p["topic_transitions"])
        self.assertEqual((p["historical_archive_count"], p["new_scientific_discovery_claims"]), (6, 0))
        self.assertEqual(p["continuity_run_id"], 45198977184)
        accepted = ROOT / "data" / "receipts" / "gh-45181050512-1.json"
        receipt = json.loads(accepted.read_text(encoding="utf-8"))
        self.assertEqual(receipt["execution_id"], p["new_execution_id"])
        self.assertEqual(receipt["output_digest"], p["receipt_output_digest"])
        self.assertEqual(receipt["outcome"], "APPLIED")
        events = [json.loads(line) for line in (ROOT / "data/knowledge/events.jsonl").read_text(
            encoding="utf-8").splitlines() if line]
        self.assertGreaterEqual(len(events), 7)
        self.assertTrue(all(e["outcome"] == "APPLIED" for e in events[:7]))
        for index in range(1, 7):
            self.assertEqual(events[index]["previous_event_sha256"], events[index - 1]["event_sha256"])
        self.assertEqual(events[6]["run_id"], p["new_execution_id"])
        self.assertEqual(events[6]["event_sha256"], p["new_event_sha256"])
        self.assertEqual(events[6]["previous_event_sha256"], p["previous_event_sha256"])
        self.assertEqual(events[6]["evidence_digest"], receipt["output_digest"])

    def test_negative_evidence_and_scientific_review_limits(self):
        d = self.current
        self.assertEqual(d["negative_evidence"]["historic_failed_run_ids_currently_http404"],
                         [43919536363, 43919549660, 43919549686, 43919549907])
        self.assertEqual(d["negative_evidence"]["prior_frozen_cancelled_run_with_failed_job"],
                         {"run_id": 43210854941, "job_id": 131157765073})
        self.assertTrue(d["negative_evidence"]["visible_parent_failures_zero_does_not_erase_frozen_history"])
        self.assertEqual(d["governance"]["repository_rulesets_count"], 0)
        self.assertIs(d["governance"]["main_protected"], False)
        self.assertFalse(d["governance"]["server_required_status_checks"])
        self.assertFalse(d["governance"]["settings_modified"])
        report = (PROV / "POST_939_TO_949_NATIVE_QUALITY_2026-11-24.md").read_text(encoding="utf-8")
        lesson = (ROOT / "docs/lessons/2026-11-24-acceptance-is-not-discovery.md").read_text(encoding="utf-8")
        self.assertIn("NO_NEW_SCIENTIFIC_CLAIM", report)
        self.assertIn("SCHEDULE_OFFSET_OBSERVED", report)
        self.assertIn("APPLIED_IS_NOT_DISCOVERY", lesson)
        self.assertNotIn("GitHub outage confirmed", report)


if __name__ == "__main__":
    unittest.main()
