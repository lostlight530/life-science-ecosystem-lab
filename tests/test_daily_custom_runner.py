"""Fail-closed tests for the bounded daily custom execution registry."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from types import SimpleNamespace

from evidence.daily_custom_runner import REQUIRED, run_checks, validate_registry
from evidence.daily_selfcheck import load_object

ROOT = Path(__file__).resolve().parents[1]


class DailyCustomRunnerTests(unittest.TestCase):
    def setUp(self):
        self.policy, self.digest = load_object(ROOT / "checks/project/daily_checks.json")

    def test_reviewed_registry_preserves_all_original_mandatory_gates(self):
        entries = validate_registry(self.policy)
        self.assertTrue(REQUIRED.issubset({x["id"] for x in entries}))
        self.assertEqual(entries[-1], {"id": "ecosystem_preflight", "severity": "advisory"})

    def test_rejects_arbitrary_commands_duplicates_and_downgraded_gates(self):
        for mutation in ("unknown", "duplicate", "downgrade", "omission"):
            policy = copy.deepcopy(self.policy)
            if mutation == "unknown":
                policy["checks"][-1]["id"] = "sh -c echo injected"
            elif mutation == "duplicate":
                policy["checks"][-1]["id"] = policy["checks"][0]["id"]
            elif mutation == "downgrade":
                policy["checks"][0]["severity"] = "advisory"
            else:
                policy["checks"].pop(0)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_registry(policy)

    def test_every_gate_runs_even_when_earlier_gate_fails(self):
        called = []

        def fake(argv, **kwargs):
            self.assertFalse(kwargs.get("shell", False))
            self.assertEqual(kwargs["timeout"], 120)
            called.append(argv)
            return SimpleNamespace(returncode=2 if len(called) == 1 else 0,
                                   stdout="", stderr="one failed" if len(called) == 1 else "")
        result = run_checks(ROOT, self.policy, self.digest, executor=fake)
        self.assertEqual(len(called), len(self.policy["checks"]))
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["blocking_failure_count"], 1)
        self.assertEqual(result["checks"][-1]["outcome"], "PASS")
        self.assertEqual(result["checks"][0]["id"], "manifest")

    def test_advisory_failure_kept_without_weakening_required_gates(self):
        def fake(argv, **kwargs):
            failed = "audit-ecosystem" in argv
            return SimpleNamespace(returncode=1 if failed else 0, stdout="", stderr="")
        result = run_checks(ROOT, self.policy, self.digest, executor=fake)
        self.assertEqual(result["status"], "PASS_WITH_ADVISORY")
        self.assertEqual(result["blocking_failure_count"], 0)
        self.assertEqual(result["advisory_failure_count"], 1)

    def test_timeout_is_distinct_and_execution_continues(self):
        calls = []
        def fake(argv, **kwargs):
            calls.append(argv)
            if len(calls) == 2:
                raise subprocess.TimeoutExpired(argv, 120)
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        result = run_checks(ROOT, self.policy, self.digest, executor=fake)
        self.assertEqual(result["checks"][1]["outcome"], "TIMEOUT")
        self.assertEqual(result["checks"][2]["outcome"], "PASS")
        self.assertEqual(result["status"], "FAIL")

    def test_report_is_serializable_and_no_raw_logs_are_retained(self):
        def fake(argv, **kwargs):
            return SimpleNamespace(returncode=0, stdout="some private log", stderr="detail")
        report = run_checks(ROOT, self.policy, hashlib.sha256(b"policy").hexdigest(), executor=fake)
        encoded = json.dumps(report)
        self.assertNotIn("some private log", encoded)
        self.assertNotIn("detail", encoded)
        self.assertEqual(report["checks"][0]["stdout_sha256"], hashlib.sha256(b"some private log").hexdigest())

    def test_report_records_unambiguous_github_execution_identity(self):
        def fake(argv, **kwargs):
            return SimpleNamespace(returncode=0, stdout="ok", stderr="")
        environment = {
            "GITHUB_SHA": "a" * 40,
            "GITHUB_REF": "refs/pull/28/merge",
            "GITHUB_HEAD_REF": "feature/profile-contracts",
            "GITHUB_BASE_REF": "main",
            "GITHUB_RUN_ID": "123",
            "GITHUB_RUN_ATTEMPT": "2",
            "GITHUB_EVENT_NAME": "pull_request",
            "GITHUB_WORKFLOW_REF": "lostlight530/lab/.github/workflows/check.yml@refs/pull/28/merge",
        }
        with patch.dict("os.environ", environment, clear=True):
            report = run_checks(ROOT, self.policy, self.digest, executor=fake)
        self.assertEqual(report["tested_sha"], "a" * 40)
        self.assertEqual(report["git_ref"], "refs/pull/28/merge")
        self.assertEqual(report["head_ref"], "feature/profile-contracts")
        self.assertEqual(report["base_ref"], "main")
        self.assertEqual(report["run_id"], "123")
        self.assertEqual(report["run_attempt"], "2")
        self.assertEqual(report["selected_check_count"], len(self.policy["checks"]))
        self.assertGreaterEqual(report["elapsed_ms"], 0)


if __name__ == "__main__":
    unittest.main()
