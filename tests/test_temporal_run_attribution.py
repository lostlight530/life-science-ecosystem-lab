"""Independent offline regression for historical run name and schedule median corrections."""
import json
import statistics
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / "docs" / "provenance"


def read(name):
    return json.loads((PROV / name).read_text(encoding="utf-8"))


class TemporalRunAttributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = read("action-runs-2026-10-30.json")
        cls.index = read("actions-visible-index-2026-10-30.json")
        cls.audit = read("run-name-attribution-audit-2026-10-30.json")
        cls.quality = read("native-daily-quality-2026-10-30.json")

    def test_exact_run_names_recover_frozen_source(self):
        original = {r["id"]: r["name"] for r in self.old["records"]}
        rows = self.audit["corrected_per_run_names"]
        by_id = {r["id"]: r for r in rows}
        self.assertEqual(len(rows), 531)
        self.assertEqual(len(by_id), 531)
        self.assertEqual(set(by_id), {r[0] for r in self.index["records"]})
        self.assertEqual(self.audit["source_grades"]["frozen_run_objects"], 523)
        self.assertEqual(self.audit["source_grades"]["later_public_run_objects"], 8)
        for run_id, name in original.items():
            if run_id in by_id:
                self.assertEqual(by_id[run_id]["name"], name)
                self.assertEqual(by_id[run_id]["source"], "PREVIOUS_FROZEN_RUN_OBJECT")

    def test_mutable_workflow_name_is_not_workflow_id(self):
        indexed_names = self.index["workflow_names"]
        incorrect = [
            r for r in self.audit["corrected_per_run_names"]
            if indexed_names[str(r["workflow_id"])] != r["name"]
        ]
        self.assertEqual(len(incorrect), 134)
        self.assertEqual(
            {r["id"] for r in incorrect},
            {r["id"] for r in self.audit["misattributed_run_records"]},
        )
        self.assertEqual(Counter(r["name"] for r in incorrect), {
            "Validate life-science workflow and evidence contracts": 132,
            "Validate computational workflow and evidence contracts": 2,
        })

    def test_schedule_medians_use_full_sorted_populations(self):
        groups = {}
        for r in self.quality["scheduled_runs"]:
            groups.setdefault(r["workflow"], []).append(
                r["offset_from_nominal_minutes"]
            )
        expected = {
            "Life Science Knowledge Workflow — Native Lifecycle": 342.01,
            "Daily research self-check — Institutional defaults and project custom": 302.41,
            "Verify accepted life-science knowledge continuity": 311.38,
            "Life Science Bio Tool — Independent Data Processing": 314.35,
        }
        self.assertEqual(set(groups), set(expected))
        for workflow, median in expected.items():
            self.assertAlmostEqual(statistics.median(groups[workflow]), median, places=2)
            self.assertAlmostEqual(
                self.audit["recomputed_schedule_medians_minutes"][workflow],
                median, places=2,
            )

    def test_erratum_and_published_medians_agree(self):
        erratum = (PROV / "RUN_NAME_AND_MEDIAN_ERRATUM_2026-10-30.md").read_text(encoding="utf-8")
        report = (PROV / "NATIVE_DAILY_QUALITY_2026-10-30.md").read_text(encoding="utf-8")
        self.assertIn("134", erratum)
        self.assertIn("| 342.01 min |", report)
        self.assertIn("| 302.41 min |", report)
        self.assertNotIn("@gmail.com", erratum)
        self.assertEqual(self.audit["reference_main_sha"],
                         "ab56cd79f5532623c2043f5b18f744b159f39aa3")


if __name__ == "__main__":
    unittest.main()
