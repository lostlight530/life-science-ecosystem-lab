"""Offline independent replay of the 2026-10-31 root-to-current GitHub census.

Frozen source populations and accepted state are never overwritten. This
verifies the recorded observations and immutable local file bytes; it does
not attest to future GitHub availability, vanished logs, institution status,
external Agent identity, or biological truth.
"""
import hashlib
import json
import statistics
import unittest
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"
CENSUS = "full-history-census-2026-10-31.json"


def read(name):
    return json.loads((PROV / name).read_text(encoding="utf-8"))


def utc(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.utcoffset().total_seconds() != 0:
        raise AssertionError("Timestamp is not UTC: " + value)
    return parsed


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


class FullOriginHistoryReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.x = read(CENSUS)

    def test_first_commit_to_reference_main_is_parent_closed(self):
        x = self.x
        self.assertEqual(x["repository_created_at_utc"], "2026-10-16T10:35:54Z")
        self.assertEqual(x["git_root_sha"], "00009a38bc136a7c245270770b005e4e102a870d")
        rows = x["repo_git"]["records"]
        self.assertEqual(x["repo_git"]["columns"], ["sha", "committed_at_utc", "parent_shas", "subject"])
        self.assertEqual(len(rows), 242)
        self.assertEqual(x["repo_git"]["count"], 242)
        self.assertEqual(len({row[0] for row in rows}), len(rows))
        self.assertEqual(rows[0][0], x["reference_main"])
        roots = [row[0] for row in rows if not row[2]]
        self.assertEqual(roots, [x["git_root_sha"]])
        sha_set = {row[0] for row in rows}
        for sha, when, parents, title in rows:
            self.assertEqual(len(sha), 40)
            self.assertIsNotNone(utc(when))
            self.assertTrue(isinstance(parents, list))
            self.assertTrue(set(parents).issubset(sha_set))
            self.assertTrue(title)
        self.assertIn(x["release"]["tag_ref"], sha_set)

    def test_all_pr_outcomes_not_promotion(self):
        x = self.x
        self.assertEqual(x["prs"]["columns"][:3], ["number", "state", "created_at_utc"])
        rows = x["prs"]["records"]
        self.assertEqual(len(rows), 50)
        self.assertEqual(len({r[0] for r in rows}), 50)
        self.assertEqual({r[0] for r in rows}, set(range(1, 51)))
        self.assertEqual(sum(bool(r[3]) for r in rows), 48)
        self.assertEqual(sorted(r[0] for r in rows if r[1] == "closed" and not r[3]), [29, 32])
        self.assertEqual(x["prs"]["closed_not_merged"], [29, 32])
        self.assertEqual(x["prs"]["open"], [])
        self.assertEqual(x["prs"]["merged"], 48)
        self.assertEqual(x["release"]["published_tag"], "v0.4.0")
        self.assertEqual(x["release"]["release_count"], 1)

    def test_full_action_population_and_independent_append_only_union(self):
        x = self.x
        actions = x["actions"]
        rows = actions["records"]
        self.assertEqual(actions["columns"], [
            "run_id", "workflow_id", "path", "observed_run_name", "event",
            "created_at_utc", "conclusion", "head_sha", "attempt"])
        self.assertEqual(actions["page_counts"], [100, 100, 100, 100, 100, 98])
        self.assertEqual(actions["api_reported_total"], 598)
        self.assertEqual(len(rows), 598)
        self.assertEqual(len({r[0] for r in rows}), 598)
        self.assertEqual(Counter(r[4] for r in rows), actions["events"])
        self.assertEqual(Counter(r[6] for r in rows), actions["conclusions"])
        self.assertEqual(actions["events"], {
            "push": 290, "pull_request": 273, "schedule": 31, "workflow_dispatch": 4})
        self.assertEqual(actions["conclusions"], {"success": 557, "cancelled": 41})
        self.assertEqual(Counter(r[5][:10] for r in rows), actions["utc_created_dates"])
        self.assertEqual(len(actions["source_urls"]), 6)
        for run_id, workflow_id, path, name, event, when, result, head, attempt in rows:
            self.assertTrue(run_id > 0 and workflow_id > 0)
            self.assertTrue(path.startswith(".github/workflows/"))
            self.assertTrue(name)
            utc(when)
            self.assertIn(result, ("success", "cancelled"))
            self.assertEqual(len(head), 40)
            self.assertEqual(attempt, 1)

        idx = read("actions-visible-index-2026-10-30.json")
        mid = read("post-merge-observation-2026-10-30.json")
        sched = read("post-schedule-observation-2026-10-30.json")
        prior = read("post-review-observation-2026-10-31.json")
        assembled = {}
        for rid, wf, code, when, conclusion_code in idx["records"]:
            self.assertNotIn(rid, assembled)
            assembled[rid] = (wf, idx["event_codes"][code],
                              when, idx["conclusion_codes"][conclusion_code])
        self.assertEqual(len(assembled), 531)
        for delta, expected in ((mid, 547), (sched, 563), (prior, 587)):
            for r in delta["new_run_records"]:
                self.assertNotIn(r["id"], assembled)
                assembled[r["id"]] = (
                    r["workflow_id"], r["event"], r["created_at_utc"], r["conclusion"])
            self.assertEqual(len(assembled), expected)

        full = {r[0]: r for r in rows}
        self.assertTrue(set(assembled).issubset(full))
        for rid, (wf, event, when, conclusion) in assembled.items():
            self.assertEqual((full[rid][1], full[rid][4], full[rid][5], full[rid][6]),
                             (wf, event, when, conclusion), rid)
        new_ids = sorted(set(full) - set(assembled))
        self.assertEqual(len(new_ids), 11)
        self.assertEqual(new_ids, x["snapshot_join"]["new_record_ids"])
        self.assertEqual(x["snapshot_join"]["prior_587_ids_absent"], [])
        self.assertEqual(x["snapshot_join"]["prior_587_fields_changed"], [])
        self.assertTrue(all(full[rid][6] == "success" for rid in new_ids))

        historical = read("action-runs-2026-10-30.json")
        failed = [r["id"] for r in historical["records"] if r["conclusion"] == "failure"]
        self.assertEqual(len(failed), 8)
        self.assertTrue(set(failed).isdisjoint(full))
        self.assertEqual(x["historical_negative"]["frozen_failed_runs"], 8)
        self.assertEqual(x["historical_negative"]["run_name_erratum"], 134)

    def test_each_observed_schedule_and_offset(self):
        x = self.x
        rows = {r[0]: r for r in x["actions"]["records"] if r[4] == "schedule"}
        self.assertEqual(len(rows), 31)
        self.assertEqual(len(x["scheduled"]["runs"]), 31)
        self.assertEqual(x["scheduled"]["job_checks"], {
            "runs": 31, "successful_runs": 31, "successful_jobs": 48, "failures": 0})
        self.assertEqual(sum(x["scheduled"]["job_categories"].values()), 48)

        grouped = defaultdict(list)
        crons = {
            ".github/workflows/life-science-knowledge.yml": (3, 23),
            ".github/workflows/life-science-continuity.yml": (4, 17),
            ".github/workflows/life-science-daily-selfcheck.yml": (1, 41),
            ".github/workflows/life-science-bio.yml": (2, 19),
        }
        self.assertEqual(set(x["scheduled"]["cron_utc"]), set(crons))
        for rid, path, when, outcome in x["scheduled"]["runs"]:
            self.assertIn(rid, rows)
            self.assertEqual((rows[rid][2], rows[rid][5], rows[rid][6]),
                             (path, when, outcome))
            self.assertEqual(outcome, "success")
            t = utc(when)
            hour, minute = crons[path]
            nominal = t.replace(hour=hour, minute=minute, second=0, microsecond=0)
            grouped[path].append(round((t - nominal).total_seconds() / 60, 2))
        self.assertEqual({path: len(a) for path, a in grouped.items()}, {
            ".github/workflows/life-science-knowledge.yml": 2,
            ".github/workflows/life-science-continuity.yml": 14,
            ".github/workflows/life-science-daily-selfcheck.yml": 13,
            ".github/workflows/life-science-bio.yml": 2})
        for path, offsets in grouped.items():
            self.assertAlmostEqual(statistics.median(offsets),
                x["scheduled"]["cron_to_created_at_median_minutes"][path], places=2)

    def test_production_and_frozen_archive_bytes(self):
        x = self.x
        guards = x["repository_tree"]["git_blob_guards"]
        self.assertEqual(x["repository_tree"]["tracked_blobs"], 247)
        self.assertFalse(x["repository_tree"]["tree_truncated"])
        self.assertEqual(len(x["repository_tree"]["workflow_paths"]), 9)
        for category in ("production", "frozen_sources"):
            for path, expected_sha in guards[category].items():
                self.assertEqual(len(expected_sha), 40)
                self.assertEqual(git_blob_sha((ROOT / path).read_bytes()),
                                 expected_sha, path)
        accepted = x["accepted_production"]
        self.assertEqual(len(accepted["receipt_paths"]), 3)
        self.assertEqual(accepted["run_ids"], [38995485443, 39227185707, 40297059874])
        events = [json.loads(s) for s in (ROOT / "data/knowledge/events.jsonl")
                  .read_text(encoding="utf-8").splitlines() if s.strip()]
        self.assertEqual(len(events), accepted["accepted_event_count"])
        self.assertIsNone(events[0]["previous_event_sha256"])
        for previous, current in zip(events, events[1:]):
            self.assertEqual(current["previous_event_sha256"], previous["event_sha256"])
        for run_id, receipt_path, evt in zip(
                accepted["run_ids"], accepted["receipt_paths"], events):
            receipt = json.loads((ROOT / receipt_path).read_text(encoding="utf-8"))
            self.assertEqual(receipt["outcome"], "APPLIED")
            self.assertEqual(receipt["execution_id"], evt["run_id"])
            self.assertEqual(receipt["execution_id"], f"gh-{run_id}-1")
            self.assertEqual(receipt["logical_date"], evt["logical_date"])
            self.assertEqual(receipt["change_kind"], evt["change_kind"])
        self.assertEqual(len(list((ROOT / "data/inputs/archive/2026/10").glob("*.json"))), 2)
        graph = json.loads((ROOT / "data/knowledge/graph-manifest.json").read_text())
        self.assertEqual(graph["entity_count"], 17)
        self.assertEqual(graph["relation_count"], 26)
        self.assertEqual(accepted["scientific_claims_added"], 0)

    def test_observation_clock_and_science_boundary(self):
        x = self.x
        win = x["observed_window_utc"]
        self.assertLess(utc(win["started_at"]), utc(win["finished_at"]))
        self.assertIsNone(x["observed_at_utc"])
        self.assertEqual(x["decision"]["software_and_data"], "NO_CHANGE_REQUIRED")
        self.assertEqual(x["decision"]["scientific_result"],
                         "NO_NEW_VERIFIED_SCIENTIFIC_CLAIM")
        self.assertEqual(x["governance"]["main_branch_protected_flag"], False)
        self.assertEqual(x["governance"]["public_rulesets"], [])


if __name__ == "__main__":
    unittest.main()
