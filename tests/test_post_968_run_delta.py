"""Offline source-scoped census replay; not historical runner execution."""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import statistics
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/provenance/post-968-to-987-observation-2026-11-26.json"


class Post968Observation(unittest.TestCase):
    def test_run_and_job_denominators(self):
        d = json.loads(RECORD.read_text(encoding="utf-8"))
        a = d["actions"]
        prior = json.loads((ROOT / d["prior_archive"]).read_text(encoding="utf-8"))
        self.assertEqual(a["prior_visible"], prior["actions"]["current_visible"])
        self.assertEqual(sum(a["pages"]), a["unique_run_count"])
        new, old = a["current_visible"], a["prior_visible"]
        for key in ("conclusions", "events"):
            self.assertEqual(sum(new[key].values()), new["count"])
        rows = a["post_cutoff_runs"]
        self.assertEqual(len(rows), len({r["id"] for r in rows}))
        self.assertEqual(len(rows), new["count"] - old["count"])
        self.assertEqual(Counter(r["event"] for r in rows), {k: new["events"][k] - old["events"][k] for k in new["events"] if new["events"][k] != old["events"][k]})
        self.assertTrue(all(d["prior_latest_run_created_at_utc"] < r["created_at_utc"] <= d["latest_included_run_created_at_utc"] and r["conclusion"] == "success" for r in rows))
        jobs = [j for r in rows for j in r["jobs"]]
        self.assertEqual(len(jobs), len({j["id"] for j in jobs}))
        self.assertEqual(len(jobs), a["post_cutoff_job_count"])
        self.assertEqual(Counter(j["conclusion"] for j in jobs), a["post_cutoff_job_conclusions"])
        self.assertEqual({j["id"] for j in jobs if j["conclusion"] == "skipped"}, {139089926487, 139055164926})
        self.assertFalse(a["exact_prior_968_id_set_join"])

    def test_schedule_prefix_and_production_boundary(self):
        d = json.loads(RECORD.read_text(encoding="utf-8"))
        prior = json.loads((ROOT / d["prior_archive"]).read_text(encoding="utf-8"))
        s = d["schedule"]
        rows = s["observations"]
        by_id = {r["id"]: r for r in rows}
        self.assertEqual(len(rows), len(by_id))
        self.assertEqual(len(rows), d["actions"]["current_visible"]["events"]["schedule"])
        for r in prior["schedule"]["observations"]:
            self.assertEqual(by_id[r["id"]]["offset_seconds"], r["offset_seconds"])
        for r in rows:
            self.assertEqual((datetime.fromisoformat(r["created_at_utc"]) - datetime.fromisoformat(r["nominal_utc"])).total_seconds(), r["offset_seconds"])
            self.assertEqual(r["conclusion"], "success")
        for key, summary in s["stats"].items():
            offsets = [r["offset_seconds"] for r in rows if r["workflow_key"] == key]
            self.assertEqual((len(offsets), min(offsets), max(offsets), statistics.median(offsets)), (summary["count"], summary["min_offset_seconds"], summary["max_offset_seconds"], summary["median_offset_seconds"]))
        self.assertEqual(s["cause"], "UNKNOWN")
        self.assertFalse(s["artifact_contents_independently_read"])
        p = d["production"]
        events = [json.loads(line) for line in (ROOT / "data/knowledge/events.jsonl").read_text(encoding="utf-8").splitlines() if line]
        e = events[p["accepted_event_count"] - 1]
        self.assertEqual((e["run_id"], e["event_sha256"], e["change_kind"]), (p["last_execution_id"], p["last_event_sha256"], p["last_change_kind"]))
        self.assertFalse(p["data_paths_changed_since_prior_source"])
        self.assertEqual(d["method_transfer"]["scientific_claim"], "NOT_EVALUATED")


if __name__ == "__main__":
    unittest.main()
