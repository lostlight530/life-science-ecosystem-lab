"""Stable, independently verifiable GitHub source aggregation.

Observation timestamps are intentionally excluded from semantic record identity.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Mapping, Sequence

from .normalization import canonical_text_bytes, sha256_bytes


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def stable_records(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Drop volatile envelope fields; enforce an unambiguous source + path key."""
    ordered = sorted((dict(item) for item in records), key=lambda i: (str(i["source_id"]), str(i["repository"]), str(i["path"])))
    seen: set[tuple[str, str, str]] = set()
    output = []
    for item in ordered:
        identity = (str(item["source_id"]), str(item["repository"]), str(item["path"]))
        if identity in seen:
            raise ValueError(f"duplicate evidence identity: {identity!r}")
        seen.add(identity)
        item.pop("retrieved_at", None)
        output.append(item)
    return output


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9][a-z0-9_-]*", text.casefold()))


def aggregate_evidence(records: Sequence[Mapping[str, Any]], topics: Mapping[str, Any] | object, previous: Mapping[str, Any] | None = None) -> dict[str, Any]:
    topic_items = topics.topics if hasattr(topics, "topics") else topics["topics"]
    ordered = stable_records(records)
    contributions: list[dict[str, Any]] = []
    for topic in sorted(topic_items, key=lambda item: item["id"]):
        accepted: list[dict[str, Any]] = []
        for record in ordered:
            tokens = _tokens(str(record.get("text", "")))
            aliases = sorted({str(value).casefold() for value in topic.get("aliases", [])})
            required = {str(value).casefold() for value in topic.get("required_terms", [])}
            excluded = {str(value).casefold() for value in topic.get("excluded_terms", [])}
            matched = [alias for alias in aliases if alias in tokens]
            if matched and required.issubset(tokens) and not excluded.intersection(tokens):
                accepted.append({"source_id": record["source_id"], "repository": record["repository"], "path": record["path"], "matched_aliases": matched})
        if len(accepted) >= int(topic.get("minimum_matches", 1)):
            contributions.append({"topic_id": topic["id"], "contributions": accepted, "match_count": len(accepted)})

    def key(r: Mapping[str, Any]) -> tuple[str, str, str]:
        return str(r.get("source_id", "")), str(r.get("repository", "")), str(r["path"])

    past = {key(r): r for r in previous.get("records", [])} if previous is not None else {}
    now = {key(r): r for r in ordered}
    changes: list[dict[str, str]] = []
    if previous is None:
        changes = [{"source_id": sid, "repository": repo, "path": path, "kind": "unknown_baseline"} for sid, repo, path in sorted(now)]
    else:
        removed = set(past) - set(now)
        added = set(now) - set(past)
        consumed_removed: set[tuple[str, str, str]] = set()
        consumed_added: set[tuple[str, str, str]] = set()
        for new_key in sorted(added):
            digest = now[new_key].get("content_sha256")
            matches = sorted(old for old in removed if old not in consumed_removed and old[:2] == new_key[:2] and past[old].get("content_sha256") == digest)
            if matches:
                old_key = matches[0]
                changes.append({"source_id": new_key[0], "repository": new_key[1], "from_path": old_key[2], "path": new_key[2], "kind": "moved"})
                consumed_removed.add(old_key)
                consumed_added.add(new_key)
        for current in sorted(set(past) | set(now)):
            if current in consumed_removed or current in consumed_added:
                continue
            if current not in past:
                kind = "added"
            elif current not in now:
                kind = "removed"
            elif past[current].get("content_sha256") != now[current].get("content_sha256"):
                kind = "modified"
            else:
                kind = "unchanged"
            changes.append({"source_id": current[0], "repository": current[1], "path": current[2], "kind": kind})
    body: dict[str, Any] = {
        "schema_version": "1.0.0", "algorithm_version": "1.1.0", "records": ordered,
        "topics": contributions, "changes": changes, "diagnostics": [], "projection_eligible": True,
    }
    body["input_digest"] = sha256_bytes(canonical_bytes(ordered))
    body["profile_digest"] = sha256_bytes(canonical_bytes(topic_items))
    body["run_id"] = body["input_digest"][:16] + "-" + body["profile_digest"][:16]
    body["sources"] = [{"source_id": a, "repository": b, "commit": c} for a, b, c in sorted({(str(i["source_id"]), str(i["repository"]), str(i["commit"])) for i in ordered})]
    body["output_digest"] = sha256_bytes(canonical_bytes(body))
    return body
