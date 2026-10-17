"""Bounded, deterministic audit of source-linked knowledge maps and cross-version changes.

This checks reproducibility contracts and optionally scores *supplied* relevance
judgments. It never infers biological truth from text matches or rankings.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import PurePosixPath
from typing import Any, Mapping
from urllib.parse import quote

from .aggregation import canonical_bytes

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
MAX_TOPICS = 128
MAX_FRAGMENTS = 25000
MAX_LABELS = 2000


def _safe_path(value: Any) -> bool:
    return (isinstance(value, str) and 0 < len(value) <= 400 and "\\" not in value
            and not value.startswith("/") and all(part not in ("", ".", "..") for part in value.split("/"))
            and PurePosixPath(value).as_posix() == value)


def _identity(topic_id: str, item: Mapping[str, Any]) -> tuple[str, str, str]:
    return (topic_id, str(item["repository"]), str(item["path"]))


def _fail(code: str, detail: str, issues: list[dict[str, str]]) -> None:
    issues.append({"code": code, "detail": detail})


def _inspect(value: Any) -> dict[str, Any]:
    """Independently check map envelope, relations and fragment provenance *shape*.

    No upstream text is available here: a matching digest does not prove a
    fragment's excerpt was truthfully selected from a remote source.
    """
    issues: list[dict[str, str]] = []
    if not isinstance(value, dict):
        return {"issues": [{"code": "INVALID_MAP", "detail": "knowledge must be a JSON object"}],
                "fragments": {}, "topics": {}, "review_candidates": []}
    signature = value.get("knowledge_digest")
    body = dict(value)
    body.pop("knowledge_digest", None)
    calculated = hashlib.sha256(canonical_bytes(body)).hexdigest()
    if signature != calculated:
        _fail("DIGEST_MISMATCH", "knowledge_digest differs from canonical content", issues)
    if value.get("kind") != "EXTRACTIVE_WORKFLOW_KNOWLEDGE_MAP":
        _fail("INVALID_KIND", "expected extractive source-linked knowledge map", issues)
    for key in ("evidence_bundle_digest", "topic_profile_digest"):
        if not isinstance(value.get(key), str) or not HEX64.fullmatch(value[key]):
            _fail("INVALID_DIGEST", key + " must be a SHA-256 digest", issues)
    raw_topics = value.get("topics")
    if not isinstance(raw_topics, list) or len(raw_topics) > MAX_TOPICS:
        _fail("INVALID_TOPICS", "topics must be a bounded array", issues)
        raw_topics = []
    topics: dict[str, dict[str, Any]] = {}
    fragments: dict[tuple[str, str, str], dict[str, Any]] = {}
    candidates: list[dict[str, str]] = []
    total = 0
    graph_edges = set()
    graph_nodes = set()
    for idx, topic in enumerate(raw_topics):
        if not isinstance(topic, dict) or not isinstance(topic.get("topic_id"), str):
            _fail("INVALID_TOPIC", f"topic[{idx}] missing topic_id", issues)
            continue
        topic_id = topic["topic_id"]
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,95}", topic_id) or topic_id in topics:
            _fail("DUPLICATE_OR_INVALID_TOPIC", topic_id, issues)
            continue
        topics[topic_id] = topic
        graph_nodes.add("topic:" + topic_id)
        rows = topic.get("fragments")
        if not isinstance(rows, list):
            _fail("INVALID_FRAGMENTS", topic_id, issues)
            continue
        total += len(rows)
        if total > MAX_FRAGMENTS:
            _fail("FRAGMENT_LIMIT", "too many knowledge fragments", issues)
            break
        sources: set[str] = set()
        for j, row in enumerate(rows):
            if not isinstance(row, dict):
                _fail("INVALID_FRAGMENT", f"{topic_id}[{j}]", issues)
                continue
            repo, commit, path, digest = (row.get(k) for k in ("repository", "commit", "path", "content_sha256"))
            if (not isinstance(repo, str) or not REPOSITORY.fullmatch(repo)
                    or not isinstance(commit, str) or not HEX40.fullmatch(commit)
                    or not _safe_path(path) or not isinstance(digest, str) or not HEX64.fullmatch(digest)):
                _fail("INVALID_SOURCE_IDENTITY", f"{topic_id}[{j}]", issues)
                continue
            url = f"https://github.com/{repo}/blob/{commit}/{quote(path, safe='/')}"
            if row.get("url") != url or not isinstance(row.get("excerpt"), str) or not row["excerpt"]:
                _fail("INVALID_SOURCE_CITATION", f"{topic_id}[{j}]", issues)
            aliases = row.get("matched_aliases")
            if not isinstance(aliases, list) or not aliases or not all(isinstance(a, str) and a for a in aliases):
                _fail("INVALID_MATCH_EVIDENCE", f"{topic_id}[{j}]", issues)
            key = _identity(topic_id, row)
            if key in fragments:
                _fail("DUPLICATE_FRAGMENT", f"{topic_id}:{repo}:{path}", issues)
            else:
                fragments[key] = row
            source_id = row.get("source_id")
            if not isinstance(source_id, str) or not source_id:
                _fail("MISSING_SOURCE_ID", f"{topic_id}[{j}]", issues)
            sources.add(repo)
            doc_id = f"github:{repo}@{commit}:{path}"
            graph_nodes.add(doc_id)
            graph_edges.add(("topic:" + topic_id, doc_id, digest))
            if isinstance(aliases, list) and len(aliases) == 1:
                candidates.append({"topic_id": topic_id, "repository": repo, "path": path,
                                   "reason": "SINGLE_MATCHED_ALIAS_NOT_SEMANTIC_VALIDATION"})
        expected = "UNOBSERVED" if not rows else "SINGLE_SOURCE" if len(sources) == 1 else "MULTI_SOURCE"
        if (topic.get("fragment_count") != len(rows) or topic.get("source_count") != len(sources)
                or topic.get("coverage") != expected):
            _fail("COVERAGE_COUNT_MISMATCH", topic_id, issues)
    graph = value.get("knowledge_graph")
    if not isinstance(graph, dict) or not isinstance(graph.get("nodes"), list) or not isinstance(graph.get("edges"), list):
        _fail("MISSING_GRAPH", "knowledge_graph requires nodes and edges", issues)
    else:
        actual_nodes = [x.get("id") for x in graph["nodes"] if isinstance(x, dict)]
        actual_edges = [(x.get("from"), x.get("to"), x.get("evidence_sha256")) for x in graph["edges"]
                        if isinstance(x, dict) and x.get("relation") == "SOURCE_MATCH"]
        if (set(actual_nodes) != graph_nodes or len(actual_nodes) != len(set(actual_nodes))
                or len(actual_nodes) != len(graph["nodes"])):
            _fail("GRAPH_NODE_MISMATCH", "graph nodes disagree with fragment projection", issues)
        if (set(actual_edges) != graph_edges or len(actual_edges) != len(graph["edges"])
                or len(actual_edges) != len(set(actual_edges))):
            _fail("GRAPH_EDGE_MISMATCH", "only exact evidenced SOURCE_MATCH edges are allowed", issues)
    if value.get("record_count", 0) < 0 or value.get("source_count", 0) < 0:
        _fail("INVALID_COUNTER", "negative record/source count", issues)
    return {"issues": issues, "fragments": fragments, "topics": topics,
            "review_candidates": sorted(candidates, key=lambda x: (x["topic_id"], x["repository"], x["path"]))}


def _compare(now: Mapping[str, Any], old: Mapping[str, Any]) -> dict[str, Any]:
    a, b = now["fragments"], old["fragments"]
    keys_a, keys_b = set(a), set(b)
    shared = keys_a & keys_b
    revision_only = []
    changed_text = []
    for key in sorted(shared):
        x, y = a[key], b[key]
        if x["content_sha256"] != y["content_sha256"]:
            changed_text.append({"topic_id": key[0], "repository": key[1], "path": key[2]})
        elif x["commit"] != y["commit"]:
            revision_only.append({"topic_id": key[0], "repository": key[1], "path": key[2]})
    topic_changes = []
    for topic_id in sorted(set(now["topics"]) | set(old["topics"])):
        old_coverage = old["topics"].get(topic_id, {}).get("coverage")
        new_coverage = now["topics"].get(topic_id, {}).get("coverage")
        if old_coverage != new_coverage:
            topic_changes.append({"topic_id": topic_id, "from": old_coverage, "to": new_coverage})
    return {
        "added": [{"topic_id": t, "repository": r, "path": p} for t, r, p in sorted(keys_a - keys_b)],
        "removed": [{"topic_id": t, "repository": r, "path": p} for t, r, p in sorted(keys_b - keys_a)],
        "document_text_changed": changed_text,
        "source_revision_only": revision_only,
        "coverage_transitions": topic_changes,
        "topic_profile_changed": now["value"].get("topic_profile_digest") != old["value"].get("topic_profile_digest"),
        "semantic_novelty": "NOT_EVALUATED",
    }


def _score_labels(fragment_keys: set[tuple[str, str, str]], labels: Any) -> dict[str, Any]:
    if labels is None:
        return {"status": "NO_HUMAN_LABELS", "counts": None, "precision": None, "recall": None}
    if not isinstance(labels, dict) or labels.get("schema_version") != "1.0.0" or not isinstance(labels.get("cases"), list):
        raise ValueError("labels must contain schema_version=1.0.0 and cases")
    cases = labels["cases"]
    if not cases or len(cases) > MAX_LABELS:
        raise ValueError("labels must contain 1..2000 cases")
    seen = set()
    counts = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("label case must be an object")
        key = (case.get("topic_id"), case.get("repository"), case.get("path"))
        if not all(isinstance(x, str) and x for x in key) or key in seen:
            raise ValueError("duplicate or invalid label identity")
        seen.add(key)
        if case.get("relevant") not in (True, False):
            raise ValueError("label relevant must be boolean")
        predicted = key in fragment_keys
        outcome = "TP" if predicted and case["relevant"] else "FP" if predicted else "FN" if case["relevant"] else "TN"
        counts[outcome] += 1
    precision = counts["TP"] / (counts["TP"] + counts["FP"]) if counts["TP"] + counts["FP"] else None
    recall = counts["TP"] / (counts["TP"] + counts["FN"]) if counts["TP"] + counts["FN"] else None
    return {"status": "USER_SUPPLIED_RELEVANCE_JUDGMENTS_NOT_SCIENTIFIC_TRUTH",
            "counts": counts, "precision": precision, "recall": recall, "sample_count": len(cases)}


def audit_knowledge(current: Any, *, previous: Any = None, labels: Any = None) -> dict[str, Any]:
    now = _inspect(current)
    now["value"] = current if isinstance(current, dict) else {}
    issues = list(now["issues"])
    comparison = None
    if previous is not None:
        old = _inspect(previous)
        old["value"] = previous if isinstance(previous, dict) else {}
        if old["issues"]:
            issues.extend({"code": "BASELINE_" + issue["code"], "detail": issue["detail"]}
                          for issue in old["issues"])
        if not issues:
            comparison = _compare(now, old)
    score = _score_labels(set(now["fragments"]), labels)
    report = {
        "schema_version": "1.0.0",
        "kind": "RESEARCH_KNOWLEDGE_QUALITY_AUDIT",
        "status": "FAIL" if issues else "PASS",
        "knowledge_digest": current.get("knowledge_digest") if isinstance(current, dict) else None,
        "baseline_digest": previous.get("knowledge_digest") if isinstance(previous, dict) else None,
        "topic_count": len(now["topics"]),
        "fragment_count": len(now["fragments"]),
        "structural_findings": issues,
        "review_candidates": now["review_candidates"],
        "comparison": comparison,
        "label_evaluation": score,
        "not_verified": [
            "scientific truth or biological causal relationships",
            "source excerpt accuracy against remote upstream without supplied candidate",
            "review quality of user-supplied relevance judgments",
            "external registry acceptance or third-party use",
        ],
    }
    report["report_sha256"] = hashlib.sha256(canonical_bytes(report)).hexdigest()
    return report
