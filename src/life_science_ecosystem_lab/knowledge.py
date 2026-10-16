"""Reproducible source-grounded knowledge extraction for life-science workflow practice.

This is extractive cartography, not semantic inference or validation of scientific claims.
Every knowledge fragment retains a path and immutable source commit.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Mapping
from urllib.parse import quote

from .evidence.aggregation import canonical_bytes
from .evidence.normalization import sha256_bytes
from .evidence.validation import validate_candidate_bundle


def _terms(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9][a-z0-9_-]*", text.casefold()))


def _excerpt(text: str, aliases: list[str]) -> str:
    """Choose an actually present passage without inventing or paraphrasing content."""
    pieces = [p.strip() for p in re.split(r"\n\s*\n|(?<=\.)\s+(?=[A-Z])", text) if p.strip()]
    for passage in pieces:
        if _terms(passage).intersection(a.casefold() for a in aliases):
            compact = " ".join(passage.split())
            return compact[:400] + ("…" if len(compact) > 400 else "")
    return " ".join(text.split())[:400]


def build_knowledge(candidate: Mapping[str, Any], registry: Mapping[str, Any]) -> dict[str, Any]:
    report = validate_candidate_bundle(candidate)
    if not report.valid:
        raise ValueError("unverified candidate: " + "; ".join(report.errors))
    topics = registry.get("topics")
    if not isinstance(topics, list):
        raise ValueError("topic registry must contain topics list")
    if candidate["profile_digest"] != sha256_bytes(canonical_bytes(topics)):
        raise ValueError("topic profile digest does not match candidate")

    identities = {(r["source_id"], r["repository"], r["path"]): r for r in candidate["records"]}
    matches = {m["topic_id"]: m for m in candidate["topics"]}
    knowledge_topics: list[dict[str, Any]] = []
    for topic in sorted(topics, key=lambda item: item["id"]):
        fragments: list[dict[str, Any]] = []
        match = matches.get(topic["id"], {"contributions": []})
        for contribution in match["contributions"]:
            key = (contribution["source_id"], contribution["repository"], contribution["path"])
            record = identities.get(key)
            if record is None:
                raise ValueError(f"topic citation does not resolve to record: {key}")
            text = record.get("text")
            if not isinstance(text, str):
                raise ValueError(f"no auditable text for record: {key}")
            path = quote(record["path"], safe="/")
            fragments.append({
                "source_id": record["source_id"],
                "repository": record["repository"],
                "path": record["path"],
                "commit": record["commit"],
                "content_sha256": record["content_sha256"],
                "url": f"https://github.com/{record['repository']}/blob/{record['commit']}/{path}",
                "matched_aliases": contribution["matched_aliases"],
                "excerpt": _excerpt(text, topic["aliases"]),
            })
        source_count = len({(f["source_id"], f["repository"]) for f in fragments})
        status = ("UNOBSERVED" if not fragments else "SINGLE_SOURCE" if source_count == 1 else "MULTI_SOURCE")
        knowledge_topics.append({
            "topic_id": topic["id"],
            "coverage": status,
            "source_count": source_count,
            "fragment_count": len(fragments),
            "fragments": fragments,
        })
    body: dict[str, Any] = {
        "schema_version": "1.0.0",
        "kind": "EXTRACTIVE_WORKFLOW_KNOWLEDGE_MAP",
        "method": "deterministic topic matching and source-cited passage extraction; not scientific inference",
        "evidence_bundle_digest": candidate["output_digest"],
        "topic_profile_digest": candidate["profile_digest"],
        "source_count": len({r["repository"] for r in candidate["records"]}),
        "record_count": len(candidate["records"]),
        "topics": knowledge_topics,
        "unresolved": [
            {"topic_id": t["topic_id"], "reason": "NO_SELECTED_EVIDENCE" if t["coverage"] == "UNOBSERVED" else "NO_INDEPENDENT_CORROBORATION"}
            for t in knowledge_topics if t["coverage"] != "MULTI_SOURCE"
        ],
    }
    body["knowledge_digest"] = hashlib.sha256(canonical_bytes(body)).hexdigest()
    return body


def verify_knowledge(candidate: Mapping[str, Any], registry: Mapping[str, Any], knowledge: Mapping[str, Any]) -> None:
    expected = build_knowledge(candidate, registry)
    if knowledge != expected:
        raise ValueError("knowledge does not match verified candidate and topic registry")
