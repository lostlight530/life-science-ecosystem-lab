"""Offline replay of the bounded 949 to 960 Run observation."""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/provenance/post-949-to-960-observation-2026-11-24.json"


class Post949Observation(unittest.TestCase):
    def test_population_and_delta(self):
        d = json.loads(RECORD.read_text(encoding="utf-8"))
        a = d["actions"]
        old = a["prior_visible"]
        new = a["current_visible"]
        prior = json.loads((ROOT / d["prior_archive"]).read_text(encoding="utf-8"))
        self.assertEqual(old, prior["actions"]["current_visible"])
        self.assertEqual(sum(a["pages"]), a["unique_run_count"])
        self.assertEqual(sum(new["conclusions"].values()), new["count"])
        self.assertEqual(sum(new["events"].values()), new["count"])
        rows = a["post_cutoff_runs"]
        self.assertEqual(len(rows), len({r["id"] for r in rows}))
        self.assertEqual(len(rows), new["count"] - old["count"])
        self.assertEqual(Counter(r["event"] for r in rows),
                         {k: new["events"][k] - old["events"][k]
                          for k in new["events"] if new["events"][k] != old["events"][k]})
        self.assertTrue(all(r["conclusion"] == "success" for r in rows))
        self.assertTrue(all(d["prior_latest_run_created_at_utc"] < r["created_at_utc"]
                            <= d["latest_included_run_created_at_utc"] for r in rows))
        jobs = [j for r in rows for j in r["jobs"]]
        self.assertEqual(len(jobs), len({j["id"] for j in jobs}))
        self.assertEqual(len(jobs), a["post_cutoff_job_count"])
        self.assertEqual(Counter(j["conclusion"] for j in jobs),
                         a["post_cutoff_job_conclusions"])
        self.assertEqual([j["id"] for j in jobs if j["conclusion"] == "skipped"],
                         [137857271934])
        self.assertFalse(a["exact_prior_949_id_set_join"])

    def test_schedule_and_frozen_acceptance_boundary(self):
        d = json.loads(RECORD.read_text(encoding="utf-8"))
        s = d["schedule"]
        row = next(r for r in d["actions"]["post_cutoff_runs"]
                   if r["id"] == s["new_selfcheck_run"])
        offset = datetime.fromisoformat(row["created_at_utc"]) - datetime.fromisoformat(s["nominal_utc"])
        self.assertEqual(offset.total_seconds(), s["created_minus_nominal_seconds"])
        self.assertEqual(sum(s["visible_successful_runs_by_workflow"].values()), 87)
        self.assertEqual(s["continuity_2026_11_24"], "NOT_OBSERVED_AT_CUTOFF")
        self.assertFalse(s["artifact_contents_independently_read"])
        p = d["production"]
        events = [json.loads(line) for line in (ROOT / "data/knowledge/events.jsonl").read_text(
            encoding="utf-8").splitlines() if line]
        self.assertGreaterEqual(len(events), p["accepted_event_count"])
        e = events[p["accepted_event_count"] - 1]
        self.assertEqual((e["run_id"], e["event_sha256"], e["change_kind"]),
                         (p["last_execution_id"], p["last_event_sha256"], p["last_change_kind"]))
        self.assertFalse(p["data_paths_changed_since_prior_source"])
        self.assertEqual(len(d["negative_evidence"]["historic_failed_run_ids_currently_http404"]), 4)


if __name__ == "__main__":
    unittest.main()
