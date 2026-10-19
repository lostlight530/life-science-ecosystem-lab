"""Deterministic, read-only execution ledger for the daily project custom checks.

A reviewed JSON policy selects only built-in check identifiers, never arbitrary
commands, Python entrypoints, URLs or filesystem destinations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .daily_selfcheck import load_object, write_report

SCHEMA_VERSION = "1.0.0"
SCOPE = "PROJECT_CUSTOM_DAILY_CHECKS"
ALGORITHM = "BOUNDED_INDEPENDENT_CHECK_RUNNER_V1"
REQUIRED = frozenset({
    "manifest", "regression", "documentation", "metadata", "rocrate",
    "publication_boundary", "accepted_state", "knowledge", "graph",
    "knowledge_quality",
})
OPTIONAL = frozenset({"ecosystem_preflight"})
TIMEOUT_SECONDS = 120


def _commands() -> dict[str, list[str]]:
    """Compile-time command catalogue; JSON cannot inject programs or flags."""
    py = sys.executable
    return {
        "manifest": [
            py, "-m", "evidence.daily_selfcheck", "project", "--root", ".",
            "--manifest", "checks/project/manifest.json", "--output",
            "build/daily-selfcheck/project-custom/file-contract.json",
        ],
        "regression": [py, "-m", "unittest", "discover", "-s", "tests", "-v"],
        "documentation": [
            py, "-m", "evidence", "audit-docs", "--root", ".", "--files",
            "evidence/profiles/docs.json", "--output",
            "build/daily-selfcheck/project-custom/docs-audit.json",
        ],
        "metadata": [py, ".github/scripts/check_metadata.py"],
        "rocrate": [py, ".github/scripts/check_rocrate.py"],
        "publication_boundary": [py, ".github/scripts/check_publication_boundary.py"],
        "accepted_state": [
            py, "-m", "life_science_ecosystem_lab", "state", "verify",
            "--repository-root", ".", "--require-accepted",
        ],
        "knowledge": [
            py, "-m", "life_science_ecosystem_lab", "knowledge", "verify",
            "--candidate", "data/inputs/current/candidate.json",
            "--topics", "evidence/profiles/topics.json",
            "--knowledge", "data/knowledge/current.json",
        ],
        "graph": [
            py, "-m", "life_science_ecosystem_lab", "graph", "verify",
            "--dir", "data/knowledge", "--knowledge", "data/knowledge/current.json",
        ],
        "knowledge_quality": [
            py, "-m", "evidence", "audit-knowledge",
            "--knowledge", "data/knowledge/current.json",
            "--output", "build/daily-selfcheck/project-custom/knowledge-quality.json",
        ],
        "ecosystem_preflight": [
            py, "-m", "evidence", "audit-ecosystem", "--root", ".",
            "--output", "build/daily-selfcheck/project-custom/ecosystem-preflight.json",
        ],
    }


def validate_registry(policy: dict[str, Any]) -> list[dict[str, str]]:
    if (set(policy) != {"schema_version", "scope", "checks"}
            or policy["schema_version"] != SCHEMA_VERSION
            or policy["scope"] != SCOPE):
        raise ValueError("invalid custom daily check registry")
    checks = policy["checks"]
    if not isinstance(checks, list) or not 10 <= len(checks) <= len(REQUIRED | OPTIONAL):
        raise ValueError("bounded list of custom check identifiers required")
    ids: set[str] = set()
    for check in checks:
        if not isinstance(check, dict) or set(check) != {"id", "severity"}:
            raise ValueError("check must contain only id and severity")
        check_id, severity = check["id"], check["severity"]
        if not isinstance(check_id, str) or check_id not in REQUIRED | OPTIONAL or check_id in ids:
            raise ValueError("unknown or duplicate custom check identifier")
        if severity not in {"blocking", "advisory"}:
            raise ValueError("invalid check severity")
        if check_id in REQUIRED and severity != "blocking":
            raise ValueError("required check cannot be disabled or downgraded")
        ids.add(check_id)
    if not REQUIRED.issubset(ids):
        raise ValueError("all original required validation gates must remain present")
    return checks


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _digest(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8", errors="replace")).hexdigest()


def run_checks(
    root: Path,
    policy: dict[str, Any],
    policy_sha256: str,
    *,
    executor: Callable[..., Any] = subprocess.run,
) -> dict[str, Any]:
    checks = validate_registry(policy)
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("repository root must be a directory")
    commands = _commands()
    rows = []
    for entry in checks:
        check_id = entry["id"]
        argv = commands[check_id]
        began = time.monotonic()
        row: dict[str, Any] = {"id": check_id, "severity": entry["severity"]}
        try:
            completed = executor(
                argv, cwd=root, capture_output=True, text=True,
                timeout=TIMEOUT_SECONDS, check=False,
            )
            code = completed.returncode
            row["outcome"] = "PASS" if code == 0 else "FAIL"
            row["exit_code"] = code
            # Preserve diagnostic identities without archiving raw logs or secrets.
            row["stdout_sha256"] = _digest(completed.stdout or "")
            row["stderr_sha256"] = _digest(completed.stderr or "")
        except subprocess.TimeoutExpired:
            row.update(outcome="TIMEOUT", error_type="TimeoutExpired")
        except OSError as error:
            row.update(outcome="ERROR", error_type=type(error).__name__)
        row["elapsed_ms"] = max(0, int((time.monotonic() - began) * 1000))
        rows.append(row)
        print(check_id, row["outcome"], row.get("exit_code", "-"), flush=True)

    blocking_failed = any(row["outcome"] != "PASS" and row["severity"] == "blocking" for row in rows)
    advisory_failed = any(row["outcome"] != "PASS" and row["severity"] == "advisory" for row in rows)
    return {
        "kind": "PROJECT_CUSTOM_DAILY_EXECUTION",
        "schema_version": SCHEMA_VERSION,
        "algorithm": ALGORITHM,
        "observed_at": utc_now(),
        "registry_sha256": policy_sha256,
        "source_commit": os.environ.get("GITHUB_SHA", "LOCAL_UNSPECIFIED"),
        "execution_id": (os.environ.get("GITHUB_RUN_ID", "LOCAL_UNSPECIFIED")
                         + "-" + os.environ.get("GITHUB_RUN_ATTEMPT", "1")),
        "event": os.environ.get("GITHUB_EVENT_NAME", "LOCAL_UNSPECIFIED"),
        "status": ("FAIL" if blocking_failed else
                   "PASS_WITH_ADVISORY" if advisory_failed else "PASS"),
        "checks": rows,
        "blocking_failure_count": sum(
            item["severity"] == "blocking" and item["outcome"] != "PASS" for item in rows
        ),
        "advisory_failure_count": sum(
            item["severity"] == "advisory" and item["outcome"] != "PASS" for item in rows
        ),
        "not_verified": [
            "Scientific truth, experiment ground truth or external registry certification",
            "Institutional health or identity authorization",
            "Independent human or agent scientific review",
            "Recurring scheduled execution from a single run",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Independent daily custom check ledger")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--registry", type=Path, default=Path("checks/project/daily_checks.json"))
    parser.add_argument(
        "--output", type=Path,
        default=Path("build/daily-selfcheck/project-custom/execution-report.json"),
    )
    args = parser.parse_args(argv)
    try:
        policy, digest = load_object(args.registry, maximum=20_000)
        report = run_checks(args.root, policy, digest)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        report = {
            "kind": "PROJECT_CUSTOM_DAILY_EXECUTION",
            "schema_version": SCHEMA_VERSION,
            "algorithm": ALGORITHM,
            "observed_at": utc_now(),
            "status": "FAIL",
            "checks": [],
            "configuration_error_type": type(error).__name__,
            "not_verified": ["No custom check execution was established"],
        }
    write_report(args.output, report)
    print(report["kind"], report["status"], str(args.output))
    return 0 if report["status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
