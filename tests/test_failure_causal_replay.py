"""Offline regression for the privacy-minimized historical causal case contract.

The fixture is a secondary source: these tests do not authenticate remote Git trees
or recreate expired Actions job logs. Synthetic cases test the exact-set mechanism.
"""
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = ROOT / "docs" / "provenance" / "failure-causal-replay-2026-10-31.json"


def selected_public_markdown(base, directories):
    return sorted(
        p.relative_to(base).as_posix()
        for directory in directories
        for p in (base / directory).glob("*.md")
        if p.is_file()
    )


class CausalFailureArchiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(CASE_PATH.read_text(encoding="utf-8"))

    def test_frozen_failure_population_and_sources_are_not_overstated(self):
        record = self.record
        self.assertEqual(record["kind"], "PROJECT_OWNED_PRIVACY_MINIMIZED_CAUSAL_REPLAY")
        self.assertIsNone(record["utc_observed_at"])
        self.assertEqual(len(record["failed_cases"]), 8)
        self.assertEqual(len(record["additional_failed_run_observations"]), 3)
        self.assertEqual(
            {r["archived_failure_run_id"] for r in record["failed_cases"]},
            {40907559247, 40907729879, 40907800054, 40907810044,
             40907818486, 40907827214, 40907834368, 40907843653},
        )
        self.assertEqual(record["invariant_test_blob_sha"],
                         "4ab741a26d1f9aaf592029427f5b127e951336c8")
        self.assertEqual(record["invariant_evidence_workflow_blob_sha"],
                         "0b6d4d99adbb9bd552fcbd0cf47378b12388004b")

    def test_reconstructed_git_tree_discrepancy_and_two_repairs(self):
        record = self.record
        expected_omissions = [
            ["docs/EVIDENCE_REPLAY_PROTOCOL.md"],
        ] + [
            ["docs/EVIDENCE_REPLAY_PROTOCOL.md",
             "docs/INTEROPERABILITY_REVIEW.md"]
        ] * 7
        for case, missing in zip(record["failed_cases"], expected_omissions):
            self.assertEqual(case["case"], "OMITTED_PUBLIC_DOCUMENT")
            self.assertEqual(case["missing_from_manifest"], missing)
            self.assertEqual(case["excess_in_manifest"], [])
            self.assertEqual(case["manifest_document_count"], 37)
            self.assertEqual(
                case["expected_public_document_count"],
                case["manifest_document_count"]
                + len(case["missing_from_manifest"])
                - len(case["excess_in_manifest"]),
            )
        repairs = record["repair_cases"]
        self.assertEqual([r["case"] for r in repairs],
            ["OMITTED_PUBLIC_DOCUMENT_REPAIRED",
             "EXTRA_UNSCANNED_DOCUMENT",
             "EXTRA_UNSCANNED_DOCUMENT_REPAIRED"])
        for case in repairs:
            self.assertEqual(
                case["expected_public_document_count"],
                case["manifest_document_count"]
                + len(case["missing_from_manifest"])
                - len(case["excess_in_manifest"]),
            )
        self.assertEqual(repairs[0]["expected_public_document_count"], 39)
        self.assertEqual(repairs[0]["manifest_document_count"], 39)
        self.assertEqual(repairs[1]["excess_in_manifest"],
                         ["docs/provenance/README.md"])
        self.assertEqual(repairs[2]["expected_public_document_count"], 42)
        self.assertEqual(repairs[2]["manifest_document_count"], 42)

    def test_synthetic_omission_overinclusion_and_positive_controls(self):
        # Reconstruct the specific semantics (nonrecursive glob + equality)
        # without network calls or touching accepted repository data.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "docs" / "provenance").mkdir(parents=True)
            (root / "docs" / "one.md").write_text("one\n", encoding="utf-8")
            (root / "docs" / "two.md").write_text("two\n", encoding="utf-8")
            (root / "docs" / "provenance" / "nested.md").write_text(
                "nested\n", encoding="utf-8"
            )
            actual = selected_public_markdown(root, ("docs",))
            self.assertEqual(actual, ["docs/one.md", "docs/two.md"])
            with_omission = ["docs/one.md"]
            with_excess = actual + ["docs/provenance/nested.md"]
            self.assertNotEqual(with_omission, actual)
            self.assertNotEqual(with_excess, actual)
            self.assertEqual(list(actual), actual)

    def test_predecessor_executions_are_distinct_and_source_bounded(self):
        predecessors = self.record["cross_repository_predecessor"]
        runs = predecessors["native_execution_summaries"]
        self.assertEqual(len(runs), 2)
        self.assertEqual({r["event"] for r in runs},
                         {"schedule", "workflow_dispatch"})
        self.assertNotEqual(runs[0]["workflow_path"], runs[1]["workflow_path"])
        self.assertEqual([r["conclusion"] for r in runs], ["success", "success"])
        self.assertIn("not attested", predecessors["scope_limit"])

    def test_no_identity_or_secret_material_is_needed_for_causal_case(self):
        text = CASE_PATH.read_text(encoding="utf-8").lower()
        for forbidden_key in ('"actor"', '"email"', '"token"', '"secret"',
                              '"job_logs"', '"task_url"', '"private_messages"'):
            self.assertNotIn(forbidden_key, text)
        self.assertIn("privacy", self.record)
        self.assertTrue(self.record["limits"])


if __name__ == "__main__":
    unittest.main()
