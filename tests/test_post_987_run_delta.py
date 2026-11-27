"""Offline replay of frozen Nov 27 observation; no network or production writes."""
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import statistics
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/provenance/post-987-to-998-observation-2026-11-27.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


class Post987Observation(unittest.TestCase):
    def test_visible_id_and_job_denominators(self):
        d = load(RECORD)
        a = d["actions"]
        prior = load(ROOT / d["prior_archive"])
        self.assertEqual(a["prior_visible"], prior["actions"]["current_visible"])
        ids = a["current_visible_run_ids"]
        self.assertEqual(ids, sorted(set(ids)))
        self.assertEqual(len(ids), sum(a["pages"]))
        self.assertEqual(len(ids), a["unique_run_count"])
        self.assertEqual(len(ids), a["current_visible"]["count"])
        for key in ("events", "conclusions"):
            self.assertEqual(sum(a["current_visible"][key].values()), len(ids))
        rows = a["post_cutoff_runs"]
        self.assertEqual(len(rows), len(ids) - a["prior_visible"]["count"])
        self.assertEqual(len(rows), len({r["id"] for r in rows}))
        self.assertTrue({r["id"] for r in rows} <= set(ids))
        self.assertTrue(all(d["prior_latest_run_created_at_utc"] < r["created_at_utc"]
                            <= d["latest_included_run_created_at_utc"] and r["attempt"] == 1
                            and r["conclusion"] == "success" for r in rows))
        self.assertEqual(Counter(r["event"] for r in rows),
                         {k: v - a["prior_visible"]["events"].get(k, 0)
                          for k, v in a["current_visible"]["events"].items()
                          if v != a["prior_visible"]["events"].get(k, 0)})
        jobs = [j for r in rows for j in r["jobs"]]
        self.assertEqual(len(jobs), len({j["id"] for j in jobs}))
        self.assertEqual(len(jobs), a["post_cutoff_job_count"])
        self.assertEqual(Counter(j["conclusion"] for j in jobs), a["post_cutoff_job_conclusions"])
        self.assertEqual([j["id"] for j in jobs if j["conclusion"] == "skipped"], [139801601911])
        self.assertFalse(a["exact_prior_987_id_set_join"])

    def test_clock_and_native_evidence(self):
        d = load(RECORD)
        s = d["schedule"]
        prior = load(ROOT / d["prior_archive"])["schedule"]["observations"]
        self.assertEqual(len(prior), s["prior_schedule_ids_rechecked"])
        rows = prior + s["new_observations"]
        self.assertEqual(len(rows), len({r["id"] for r in rows}))
        self.assertEqual(len(rows), d["actions"]["current_visible"]["events"]["schedule"])
        self.assertTrue({r["id"] for r in rows} <= set(d["actions"]["current_visible_run_ids"]))
        for r in rows:
            self.assertEqual((datetime.fromisoformat(r["created_at_utc"]) -
                              datetime.fromisoformat(r["nominal_utc"])).total_seconds(), r["offset_seconds"])
        for key, v in s["stats"].items():
            a = [r["offset_seconds"] for r in rows if r["workflow_key"] == key]
            self.assertEqual((len(a), min(a), max(a), statistics.median(a)),
                             (v["count"], v["min_offset_seconds"], v["max_offset_seconds"], v["median_offset_seconds"]))
        native = [r for r in d["actions"]["post_cutoff_runs"] if r["event"] == "schedule"]
        self.assertEqual({r["id"] for r in native}, {r["id"] for r in s["new_observations"]})
        jobs = {j["id"]: j for r in native for j in r["jobs"]}
        self.assertEqual(len(jobs), 7)
        self.assertTrue(all(j["conclusion"] == "success" for j in jobs.values()))
        self.assertEqual(jobs[140460569313]["log_signals"]["pinned_bio_analyzed"], 6)
        self.assertEqual(jobs[139959758047]["log_signals"]["knowledge_quality"], "PASS")
        self.assertEqual(len(s["artifacts"]), 7)
        self.assertEqual(len({x["id"] for x in s["artifacts"]}), 7)
        self.assertTrue(all(x["job_id"] in jobs and x["log_api_digest_agreement"]
                            and len(x["sha256"]) == 64 for x in s["artifacts"]))
        self.assertEqual(s["cause"], "UNKNOWN")
        self.assertFalse(s["artifact_contents_independently_read"])

    def test_frozen_accepted_prefix_and_tamper_control(self):
        d = load(RECORD)
        p = d["production"]
        events = [json.loads(x) for x in (ROOT / "data/knowledge/events.jsonl")
                  .read_text(encoding="utf-8").splitlines() if x]
        prefix = events[:p["accepted_event_count"]]
        self.assertEqual(len(prefix), p["accepted_event_count"])
        previous = None
        for event in prefix:
            body = {k: v for k, v in event.items() if k != "event_sha256"}
            self.assertEqual(digest(body), event["event_sha256"])
            self.assertEqual(event["previous_event_sha256"], previous)
            previous = event["event_sha256"]
        self.assertEqual(previous, p["last_event_sha256"])
        body = {k: v for k, v in prefix[0].items() if k != "event_sha256"}
        body["outcome"] = "FAILED"
        self.assertNotEqual(digest(body), prefix[0]["event_sha256"])
        self.assertFalse(p["data_paths_changed_since_prior_source"])
        self.assertFalse(d["git"]["data_paths_changed"])
