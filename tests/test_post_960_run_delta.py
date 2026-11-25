"""Replay the source-scoped 960-to-968 evidence without live-network claims."""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import statistics
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/provenance/post-960-to-968-observation-2026-11-25.json"


class Post960Observation(unittest.TestCase):
    def test_run_and_job_denominators(self):
        d = json.loads(RECORD.read_text(encoding="utf-8"))
        a = d["actions"]
        prior = json.loads((ROOT / d["prior_archive"]).read_text(encoding="utf-8"))
        self.assertEqual(a["prior_visible"], prior["actions"]["current_visible"])
        self.assertEqual(sum(a["pages"]), a["unique_run_count"])
        new, old = a["current_visible"], a["prior_visible"]
        self.assertEqual(sum(new["conclusions"].values()), new["count"])
        self.assertEqual(sum(new["events"].values()), new["count"])
        rows = a["post_cutoff_runs"]
        self.assertEqual(len(rows), len({r["id"] for r in rows}))
        self.assertEqual(len(rows), new["count"] - old["count"])
        self.assertEqual(Counter(r["event"] for r in rows), {k: new["events"][k] - old["events"][k] for k in new["events"] if new["events"][k] != old["events"][k]})
        self.assertTrue(all(d["prior_latest_run_created_at_utc"] < r["created_at_utc"] <= d["latest_included_run_created_at_utc"] for r in rows))
        jobs = [j for r in rows for j in r["jobs"]]
        self.assertEqual(len(jobs), len({j["id"] for j in jobs}))
        self.assertEqual(len(jobs), a["post_cutoff_job_count"])
        self.assertEqual(Counter(j["conclusion"] for j in jobs), a["post_cutoff_job_conclusions"])
        self.assertEqual([j["id"] for j in jobs if j["conclusion"] == "skipped"], [138490827732])
        self.assertFalse(a["exact_prior_960_id_set_join"])

    def test_schedule_and_frozen_state(self):
        d = json.loads(RECORD.read_text(encoding="utf-8"))
        s = d["schedule"]
        rows = s["observations"]
        self.assertEqual(len(rows), len({r["id"] for r in rows}))
        self.assertEqual(len(rows), 88)
        for r in rows:
            delta = datetime.fromisoformat(r["created_at_utc"]) - datetime.fromisoformat(r["nominal_utc"])
            self.assertEqual(delta.total_seconds(), r["offset_seconds"])
            self.assertEqual(r["conclusion"], "success")
        for key, summary in s["stats"].items():
            offsets = [r["offset_seconds"] for r in rows if r["workflow_key"] == key]
            self.assertEqual((len(offsets), statistics.median(offsets)), (summary["count"], summary["median_offset_seconds"]))
        row = next(r for r in rows if r["id"] == s["new_continuity_run"])
        self.assertEqual(row["offset_seconds"], s["created_minus_nominal_seconds"])
        self.assertEqual(s["cause"], "UNKNOWN")
        self.assertFalse(s["artifact_contents_independently_read"])
        p = d["production"]
        events = [json.loads(line) for line in (ROOT / "data/knowledge/events.jsonl").read_text(encoding="utf-8").splitlines() if line]
        self.assertGreaterEqual(len(events), p["accepted_event_count"])
        e = events[p["accepted_event_count"] - 1]
        self.assertEqual((e["run_id"], e["event_sha256"], e["change_kind"]), (p["last_execution_id"], p["last_event_sha256"], p["last_change_kind"]))
        self.assertFalse(p["data_paths_changed_since_prior_source"])
        self.assertEqual(p["selected_text_changes"], 0)
        self.assertEqual(p["selected_content_digest_changes"], 0)


if __name__ == "__main__":
    unittest.main()
