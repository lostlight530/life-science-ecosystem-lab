"""Verify archived real-world field reports against independent source-run hashes."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "evidence" / "field-tests" / "2026-10-17-live-readonly.json"


def validate_archive(index):
    errors = []
    for item in index["independent_inspections"]:
        path = item.get("archived_report", "")
        target = (ROOT / path).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            errors.append("missing or unsafe report path")
            continue
        report = json.loads(target.read_text(encoding="utf-8"))
        normalized = dict(report)
        normalized.pop("object", None)
        normalized.pop("report_sha256", None)
        digest = hashlib.sha256(json.dumps(
            normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            allow_nan=False).encode("utf-8")).hexdigest()
        if digest != report["report_sha256"] or digest != item["report_digest"]:
            errors.append(f"report checksum mismatch: {path}")
        if report["counts"] != item["counts"] or report["status"] != item["status"]:
            errors.append(f"report status mismatch: {path}")
    return errors


class RealEvidenceIndexTests(unittest.TestCase):
    def test_actual_github_artifact_reports_are_reproducibly_indexed(self):
        index = json.loads(INDEX.read_text(encoding="utf-8"))
        self.assertEqual(index["source_run_id"], 38994004639)
        self.assertEqual(index["artifact_id"], 12086636220)
        self.assertEqual(index["source_evidence"]["record_count"], 15)
        self.assertEqual(validate_archive(index), [])

    def test_reject_bad_index_hash(self):
        index = json.loads(INDEX.read_text(encoding="utf-8"))
        changed = copy.deepcopy(index)
        changed["independent_inspections"][0]["report_digest"] = "0" * 64
        self.assertTrue(any("checksum mismatch" in s for s in validate_archive(changed)))

    def test_reject_escaped_or_missing_report_path(self):
        index = json.loads(INDEX.read_text(encoding="utf-8"))
        changed = copy.deepcopy(index)
        changed["independent_inspections"][0]["archived_report"] = "../../etc/passwd"
        self.assertTrue(any("unsafe report path" in s for s in validate_archive(changed)))


if __name__ == "__main__":
    unittest.main()
