"""Validate optional external-Agent research handoffs without granting runtime authority.

A valid handoff is an inspectable proposal, not accepted evidence, source approval,
a scientific finding, or permission to mutate the native production state.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Mapping
from urllib.parse import urlsplit

_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,95}$")
_SHA = re.compile(r"^[0-9a-f]{40}$")
_GITHUB_BLOB = re.compile(r"^/[^/]+/[^/]+/blob/([0-9a-f]{40})/(.+)$")
_MAX_ITEMS = 100


@dataclass(frozen=True)
class HandoffVerdict:
    valid: bool
    errors: tuple[str, ...]


def _text(value: Any, *, limit: int = 1600) -> bool:
    return isinstance(value, str) and 0 < len(value.strip()) <= limit and "\x00" not in value


def _safe_path(value: Any) -> bool:
    if not isinstance(value, str) or len(value) > 240 or "\\" in value:
        return False
    path = PurePosixPath(value)
    return bool(value and not path.is_absolute() and not any(
        part in ("", ".", "..") for part in value.split("/")
    ) and path.as_posix() == value)


def _source_url(value: Any) -> bool:
    if not _text(value, limit=2000):
        return False
    try:
        parsed = urlsplit(value)
        valid_host = parsed.hostname
        has_credentials = parsed.username or parsed.password
    except ValueError:
        return False
    if parsed.scheme != "https" or not parsed.netloc or not valid_host or has_credentials or parsed.fragment:
        return False
    if parsed.hostname == "github.com" and parsed.path.count("/") >= 4 and "/blob/" in parsed.path:
        matched = _GITHUB_BLOB.fullmatch(parsed.path)
        return matched is not None and _SHA.fullmatch(matched.group(1)) is not None
    return True


def validate_agent_handoff(value: Any, *, known_topics: set[str] | None = None) -> HandoffVerdict:
    errors: list[str] = []
    if not isinstance(value, dict):
        return HandoffVerdict(False, ("handoff must be a JSON object",))
    if value.get("schema_version") != "1.0.0" or value.get("kind") != "EXTERNAL_AGENT_RESEARCH_HANDOFF":
        errors.append("invalid handoff schema identity")
    if value.get("authority") != "PROPOSAL_ONLY":
        errors.append("external research cannot grant acceptance or write authority")
    task = value.get("task")
    if not isinstance(task, dict):
        errors.append("task must be an object")
    else:
        if not isinstance(task.get("id"), str) or not _ID.fullmatch(task["id"]):
            errors.append("invalid task id")
        if not _text(task.get("question")):
            errors.append("task question required")
        ids = task.get("topic_ids")
        if not isinstance(ids, list) or len(ids) > 30 or not all(_text(x, limit=100) for x in ids):
            errors.append("task topic_ids must be a bounded string array")
        elif len(set(ids)) != len(ids):
            errors.append("duplicate task topic_ids")
        elif known_topics is not None and not set(ids).issubset(known_topics):
            errors.append("unknown topic id; topic changes require a separately reviewed registry edit")
    result = value.get("result")
    if result not in ("PROPOSED", "NO_FINDINGS"):
        errors.append("result must be PROPOSED or NO_FINDINGS, never APPLIED")
    observations = value.get("observations")
    if not isinstance(observations, list) or len(observations) > _MAX_ITEMS:
        errors.append("observations must be a bounded array")
    else:
        if result == "NO_FINDINGS" and observations:
            errors.append("NO_FINDINGS must have no observations")
        for i, item in enumerate(observations):
            if not isinstance(item, dict) or not _text(item.get("statement")):
                errors.append(f"observation[{i}] requires statement")
                continue
            if item.get("status") != "UNVERIFIED":
                errors.append(f"observation[{i}] cannot self-certify")
            if not _source_url(item.get("source_url")):
                errors.append(f"observation[{i}] source_url must be a valid HTTPS link; GitHub blob links require a pinned commit")
    proposals = value.get("proposed_changes")
    if not isinstance(proposals, list) or len(proposals) > _MAX_ITEMS:
        errors.append("proposed_changes must be a bounded array")
    else:
        if result == "NO_FINDINGS" and proposals:
            errors.append("NO_FINDINGS cannot propose changes")
        for i, item in enumerate(proposals):
            if not isinstance(item, dict) or not _safe_path(item.get("path")):
                errors.append(f"proposed_changes[{i}] has an unsafe path")
                continue
            if item["path"].startswith("data/"):
                errors.append(f"proposed_changes[{i}] cannot directly target accepted data")
            if item.get("review_required") is not True or not _text(item.get("rationale")):
                errors.append(f"proposed_changes[{i}] requires explicit human review and rationale")
    limitations = value.get("limitations")
    if not isinstance(limitations, list) or len(limitations) > 30 or not all(_text(x) for x in limitations):
        errors.append("limitations must be a bounded string array")
    return HandoffVerdict(not errors, tuple(errors))
