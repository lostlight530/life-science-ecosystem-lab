"""Reconcile the frozen Nov 28 census, without network or accepted-state writes."""
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import statistics
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/provenance/post-998-to-1015-observation-2026-11-28.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def event_digest(event):
    body = {k: v for k, v in event.items() if k != "event_sha256"}
    return hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def exact_delta(old_ids, new_ids):
    if len(old_ids) != len(set(old_ids)) or len(new_ids) != len(set(new_ids)):
        raise ValueError("duplicate Run identity")
    return set(new_ids) - set(old_ids), set(old_ids) - set(new_ids)


class Post998Observation(unittest.TestCase):
    def test_exact_visible_run_join_and_conditional_jobs(self):
        d = load(RECORD)
        a = d["actions"]
        prior = load(ROOT / d["prior_archive"])["actions"]["current_visible_run_ids"]
        ids = a["current_visible_run_ids"]
        new, missing = exact_delta(prior, ids)
        self.assertEqual((len(prior), len(ids), len(new), len(missing)), (998, 1015, 17, 0))
        self.assertEqual(new, set(a["new_ids"]))
        self.assertEqual(missing, set(a["prior_ids_missing"]))
        self.assertEqual(len(ids), sum(a["pages"]))
        for key in ("conclusions", "events"):
            self.assertEqual(sum(a["current_visible"][key].values()), len(ids))
        rows = a["post_cutoff_runs"]
        self.assertEqual({r["id"] for r in rows}, new)
        self.assertEqual(len(rows), len(new))
        self.assertTrue(all(d["prior_latest_run_created_at_utc"] < r["created_at_utc"]
                            <= d["latest_included_run_created_at_utc"]
                            and r["attempt"] == 1 and r["conclusion"] == "success" for r in rows))
        jobs = [j for r in rows for j in r["jobs"]]
        self.assertEqual(len(jobs), len({j["id"] for j in jobs}))
        self.assertEqual(Counter(j["conclusion"] for j in jobs), {"success": 36, "skipped": 2})
        for r in rows:
            for j in r["jobs"]:
                if j["conclusion"] == "skipped":
                    self.assertEqual((r["event"], j["name"]), ("push", "pinned-field"))
        with self.assertRaises(ValueError):
            exact_delta(prior, ids + [ids[0]])
        _, removed = exact_delta(prior, [i for i in ids if i != prior[0]])
        self.assertEqual(removed, {prior[0]})

    def test_schedule_denominators_and_retention_boundary(self):
        d = load(RECORD)
        s = d["schedule"]
        rows = s["rows"]
        self.assertEqual(len(rows), len({r["id"] for r in rows}))
        self.assertEqual(len(rows), 97)
        self.assertTrue({r["id"] for r in rows} <= set(d["actions"]["current_visible_run_ids"]))
        self.assertTrue(all(r["attempt"] == 1 and r["conclusion"] == "success"
                            and r["failed_cancelled_timed_out_steps"] == 0 for r in rows))
        for r in rows:
            self.assertEqual((datetime.fromisoformat(r["created_at_utc"]) -
                              datetime.fromisoformat(r["nominal_reference_utc"])).total_seconds(),
                             r["offset_seconds"])
        for key, v in s["stats"].items():
            group = [r for r in rows if r["workflow_key"] == key]
            offsets = [r["offset_seconds"] for r in group]
            self.assertEqual((len(group), min(offsets), statistics.median(offsets), max(offsets)),
                             (v["runs"], v["min_offset_seconds"], v["median_offset_seconds"],
                              v["max_offset_seconds"]))
            self.assertEqual(sum(r["latest_attempt_success_jobs"] for r in group), v["jobs"])
            self.assertEqual(sum(r["visible_artifact_count"] for r in group), v["artifacts"])
            self.assertEqual(sum(r["visible_artifact_count"] > 0 for r in group), v["runs_with_artifacts"])
        self.assertEqual(sum(r["latest_attempt_success_jobs"] for r in rows), 151)
        self.assertEqual(sum(r["visible_artifact_count"] for r in rows), 80)
        self.assertEqual(sum(r["visible_artifact_count"] == 0 for r in rows), 49)
        self.assertEqual(s["artifact_absence_cause"], "UNKNOWN")
        self.assertEqual(s["offset_cause"], "UNKNOWN")
        self.assertFalse(s["artifact_contents_independently_read"])
        self.assertTrue(all(not a["independent_zip_bytes_verified"] for a in s["new_artifacts"]))

    def test_accepted_prefix_and_negative_control(self):
        d = load(RECORD)
        p = d["production"]
        events = [json.loads(s) for s in (ROOT / "data/knowledge/events.jsonl")
                  .read_text(encoding="utf-8").splitlines() if s]
        prefix = events[:p["accepted_event_count"]]
        self.assertEqual(len(prefix), p["accepted_event_count"])
        previous = None
        for e in prefix:
            self.assertEqual(event_digest(e), e["event_sha256"])
            self.assertEqual(e["previous_event_sha256"], previous)
            receipt = load(ROOT / "data/receipts" / (e["run_id"] + ".json"))
            self.assertEqual(receipt["execution_id"], e["run_id"])
            self.assertEqual(receipt["output_digest"], e["evidence_digest"])
            self.assertEqual(receipt["snapshot_id"], e["snapshot_id"])
            previous = e["event_sha256"]
        self.assertEqual(previous, p["last_event_sha256"])
        self.assertEqual(prefix[-1]["run_id"], p["last_execution_id"])
        tampered = dict(prefix[2], outcome="FAILED")
        self.assertNotEqual(event_digest(tampered), prefix[2]["event_sha256"])
        self.assertEqual(p["last_change_kind"], "DOCUMENT_TEXT_UNCHANGED")
        self.assertEqual(d["negative_evidence"]["historical_2026_10_30_failure_count"], 8)


if __name__ == "__main__":
    unittest.main()
