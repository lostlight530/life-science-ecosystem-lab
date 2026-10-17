"""Domain-neutral, proposal-only research case integrity contract.

A PASS checks the reusable methodological *envelope*, not data validity,
execution truth, scientific causality, biological accuracy, or reviewer approval.
Domain-specific method adapters remain independently testable and replaceable.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import math
import re
from typing import Any
from urllib.parse import urlsplit

from .aggregation import canonical_bytes
from .agent_identity import proposer_errors

STAGES = ("DEFINE", "PIN", "QUALIFY", "EXECUTE", "EVALUATE", "AUDIT", "REVIEW", "REPLAY")
STAGE_STATES = frozenset({"PENDING", "REPORTED", "BLOCKED", "NOT_APPLICABLE"})
REF_TYPES = frozenset({"NONE", "PEER_MODEL", "EXPERIMENTAL_REFERENCE", "SIMULATED", "LITERATURE_REFERENCE"})
_ID = re.compile(r"^[a-z][a-z0-9_.-]{0,95}$")
_HEX = re.compile(r"^[0-9a-f]{64}$")
_COMMIT = re.compile(r"^[0-9a-f]{40}$")
MAX_INPUTS = 30
MAX_METRICS = 100


@dataclass(frozen=True)
class CaseVerdict:
    valid: bool
    errors: tuple[str, ...]


def _text(value: Any, maximum: int = 1200) -> bool:
    return isinstance(value, str) and 0 < len(value.strip()) <= maximum and "\x00" not in value


def _https(value: Any) -> bool:
    if not _text(value, 2000):
        return False
    try:
        uri = urlsplit(value)
        return (uri.scheme == "https" and bool(uri.hostname) and uri.username is None
                and uri.password is None and not uri.fragment)
    except ValueError:
        return False


def _digest(value: Any) -> bool:
    return isinstance(value, str) and bool(_HEX.fullmatch(value))


def validate_research_case(value: Any) -> CaseVerdict:
    """Validate fixed research stages independently of any biological algorithm."""
    errors: list[str] = []
    if not isinstance(value, dict):
        return CaseVerdict(False, ("research case must be a JSON object",))
    if value.get("schema_version") != "1.0.0" or value.get("kind") != "RESEARCH_CASE_PROPOSAL":
        errors.append("unsupported research case identity")
    if not isinstance(value.get("case_id"), str) or not _ID.fullmatch(value["case_id"]):
        errors.append("invalid case_id")
    if not _text(value.get("domain"), 120) or not _text(value.get("question")):
        errors.append("domain and research question are required")
    if value.get("authority") != "PROPOSAL_ONLY":
        errors.append("case cannot grant scientific acceptance or production write authority")
    if "proposer" in value:
        errors.extend(proposer_errors(value["proposer"]))
    stages = value.get("stages")
    if not isinstance(stages, dict) or set(stages) != set(STAGES):
        errors.append("all eight fixed methodological stages are required")
    else:
        for stage in STAGES:
            item = stages[stage]
            if not isinstance(item, dict) or item.get("state") not in STAGE_STATES:
                errors.append(f"invalid stage state: {stage}")
                continue
            if item["state"] in ("NOT_APPLICABLE", "BLOCKED") and not _text(item.get("reason")):
                errors.append(f"stage {stage} requires an explicit reason")
            refs = item.get("evidence_refs", [])
            if not isinstance(refs, list) or len(refs) > 12 or not all(_text(x, 300) for x in refs):
                errors.append(f"invalid stage evidence references: {stage}")
            if item["state"] == "REPORTED" and not refs:
                errors.append(f"reported stage {stage} needs at least one evidence reference")
    inputs = value.get("inputs")
    if not isinstance(inputs, list) or not 1 <= len(inputs) <= MAX_INPUTS:
        errors.append("1..30 source-identifiable inputs required")
    else:
        names = set()
        for i, item in enumerate(inputs):
            if not isinstance(item, dict):
                errors.append(f"input[{i}] must be an object")
                continue
            name = item.get("name")
            if not isinstance(name, str) or not _ID.fullmatch(name) or name in names:
                errors.append(f"input[{i}] invalid or duplicate name")
            else:
                names.add(name)
            if not _digest(item.get("sha256")):
                errors.append(f"input[{i}] source_sha256 required")
            if item.get("scope") not in ("LOCAL_FIXTURE", "PINNED_EXTERNAL"):
                errors.append(f"input[{i}] must state source scope")
            if item.get("scope") == "PINNED_EXTERNAL":
                if not _https(item.get("uri")) or not isinstance(item.get("revision"), str) or not _COMMIT.fullmatch(item["revision"]):
                    errors.append(f"input[{i}] externally pinned URI and 40-hex revision required")
            if not _text(item.get("format"), 100):
                errors.append(f"input[{i}] requires declared data format")
    method = value.get("method")
    if not isinstance(method, dict):
        errors.append("method descriptor required")
    else:
        if not _text(method.get("name"), 150) or not _text(method.get("version"), 100):
            errors.append("method name and version required")
        if not _digest(method.get("parameters_sha256")):
            errors.append("method parameters must have a reproducibility digest")
        if not isinstance(method.get("software_commit"), str) or not _COMMIT.fullmatch(method["software_commit"]):
            errors.append("method must be pinned to a software commit")
        if method.get("role") not in ("DATA_QA", "COMPUTATION", "COMPARISON", "WORKFLOW_VALIDATION"):
            errors.append("method role must be explicit")
    execution = value.get("execution")
    if not isinstance(execution, dict) or execution.get("state") not in ("NOT_RUN", "REPORTED_RUN", "REPORTED_FAILURE"):
        errors.append("execution must report NOT_RUN / REPORTED_RUN / REPORTED_FAILURE")
    elif execution["state"] != "NOT_RUN":
        if not _digest(execution.get("environment_sha256")) or not _digest(execution.get("report_sha256")):
            errors.append("reported execution requires environment and report digests")
    evaluation = value.get("evaluation")
    if not isinstance(evaluation, dict) or evaluation.get("state") not in ("NOT_EVALUATED", "REPORTED_UNVERIFIED"):
        errors.append("evaluation must be NOT_EVALUATED or REPORTED_UNVERIFIED")
    else:
        metrics = evaluation.get("metrics")
        if not isinstance(metrics, list) or len(metrics) > MAX_METRICS:
            errors.append("evaluation metrics must be a bounded array")
        else:
            if evaluation["state"] == "NOT_EVALUATED" and metrics:
                errors.append("NOT_EVALUATED cannot contain results")
            if execution is not None and isinstance(execution, dict) and execution.get("state") == "NOT_RUN" and metrics:
                errors.append("unexecuted case cannot self-report computed metrics")
            for i, metric in enumerate(metrics):
                if not isinstance(metric, dict):
                    errors.append(f"metric[{i}] must be an object")
                    continue
                number = metric.get("value")
                if (not isinstance(number, (int, float)) or isinstance(number, bool) or not math.isfinite(number)
                        or not _text(metric.get("name"), 100) or not _text(metric.get("unit"), 60)
                        or metric.get("reference_type") not in REF_TYPES):
                    errors.append(f"metric[{i}] needs finite value, unit and reference_type")
    limitations = value.get("limitations")
    if not isinstance(limitations, list) or not 1 <= len(limitations) <= 30 or not all(_text(x) for x in limitations):
        errors.append("explicit bounded uncertainty and limitations required")
    review = value.get("review")
    if not isinstance(review, dict) or review.get("authority") != "HUMAN_REQUIRED" or review.get("status") not in ("PENDING", "NEEDS_CHANGES"):
        errors.append("review must remain human-authoritative and pending for proposals")
    return CaseVerdict(not errors, tuple(errors))


def research_case_shape_report(value: Any) -> dict[str, Any]:
    verdict = validate_research_case(value)
    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "kind": "RESEARCH_CASE_SHAPE_REVIEW",
        "status": "PASS" if verdict.valid else "FAIL",
        "errors": list(verdict.errors),
        "case_id": value.get("case_id") if isinstance(value, dict) else None,
        "methodology": list(STAGES),
        "assurance": "PROPOSAL_SHAPE_ONLY",
        "not_verified": [
            "input bytes against pinned sources",
            "method implementation or its scientific suitability",
            "execution and reported measurement truth",
            "independent references, controls, or scientific conclusions",
            "actual human approval or production acceptance",
        ],
    }
    report["report_sha256"] = sha256(canonical_bytes(report)).hexdigest()
    return report
