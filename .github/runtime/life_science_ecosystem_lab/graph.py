"""Rebuildable, source-cited JSONL knowledge graph and bounded lexical graph search.

Only SOURCE_MATCH edges are derived from verified source fragments. This module
never turns lexical similarity or graph rank into a factual scientific claim.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Mapping


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _digest(value: object) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _write_jsonl(path: Path, values: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(_json(value) + "\n" for value in values)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(payload, encoding="utf-8", newline="\n")
    temporary.replace(path)


def _read_jsonl(path: Path, *, max_records: int = 50000) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                raise ValueError(f"blank JSONL row: {path}")
            item = json.loads(line)
            if not isinstance(item, dict):
                raise ValueError(f"non-object JSONL row: {path}")
            values.append(item)
            if len(values) > max_records:
                raise ValueError("graph size limit exceeded")
    return values


def project_graph(knowledge: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    graph = knowledge.get("knowledge_graph")
    if not isinstance(graph, Mapping):
        raise ValueError("knowledge_graph is required")
    topics = {"topic:" + str(t["topic_id"]): t for t in knowledge.get("topics", [])}
    fragments: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for topic_id, topic in topics.items():
        for fragment in topic.get("fragments", []):
            doc_id = f"github:{fragment['repository']}@{fragment['commit']}:{fragment['path']}"
            fragments[doc_id].append({"topic": topic_id, "excerpt": fragment["excerpt"], "url": fragment["url"]})
    entities: list[dict[str, Any]] = []
    for node in graph.get("nodes", []):
        if not isinstance(node, Mapping) or not isinstance(node.get("id"), str):
            raise ValueError("invalid graph entity")
        node_id = node["id"]
        data = fragments.get(node_id, [])
        entities.append({
            "id": node_id,
            "kind": node.get("kind", "unknown"),
            "label": node_id[6:] if node_id.startswith("topic:") else node_id.split(":")[-1],
            "text": " ".join(sorted({x["excerpt"] for x in data})),
            "citations": sorted({x["url"] for x in data}),
            "source_digest": knowledge.get("knowledge_digest"),
        })
    ids = {e["id"] for e in entities}
    if len(ids) != len(entities):
        raise ValueError("duplicate graph entity")
    relations: list[dict[str, Any]] = []
    for edge in graph.get("edges", []):
        if edge.get("from") not in ids or edge.get("to") not in ids:
            raise ValueError("dangling graph relation")
        if edge.get("relation") != "SOURCE_MATCH":
            raise ValueError("unverified graph predicate")
        if not re.fullmatch(r"[0-9a-f]{64}", str(edge.get("evidence_sha256", ""))):
            raise ValueError("relation evidence digest missing")
        relations.append({
            "id": _digest([edge["from"], edge["relation"], edge["to"], edge["evidence_sha256"]]),
            "subject": edge["from"],
            "predicate": edge["relation"],
            "object": edge["to"],
            "evidence_sha256": edge["evidence_sha256"],
            "status": "SOURCE_MATCH_ONLY",
        })
    entities.sort(key=lambda item: item["id"])
    relations.sort(key=lambda item: item["id"])
    if len({r["id"] for r in relations}) != len(relations):
        raise ValueError("duplicate graph relation")
    return entities, relations


def write_graph(knowledge: Mapping[str, Any], directory: Path) -> dict[str, Any]:
    entities, relations = project_graph(knowledge)
    directory.mkdir(parents=True, exist_ok=True)
    _write_jsonl(directory / "entities.jsonl", entities)
    _write_jsonl(directory / "relations.jsonl", relations)
    manifest = {"schema_version": "1.0.0", "knowledge_digest": knowledge.get("knowledge_digest"),
                "entity_count": len(entities), "relation_count": len(relations),
                "entities_sha256": _digest(entities), "relations_sha256": _digest(relations)}
    (directory / "graph-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def verify_graph(directory: Path, knowledge: Mapping[str, Any] | None = None) -> dict[str, Any]:
    entities = _read_jsonl(directory / "entities.jsonl")
    relations = _read_jsonl(directory / "relations.jsonl")
    manifest = json.loads((directory / "graph-manifest.json").read_text(encoding="utf-8"))
    ids = [x["id"] for x in entities]
    if ids != sorted(set(ids)):
        raise ValueError("noncanonical or duplicate entity IDs")
    relation_ids = [x["id"] for x in relations]
    if relation_ids != sorted(set(relation_ids)):
        raise ValueError("noncanonical or duplicate relation IDs")
    for r in relations:
        if r["subject"] not in ids or r["object"] not in ids:
            raise ValueError("dangling graph relation")
        if r["predicate"] != "SOURCE_MATCH" or r["status"] != "SOURCE_MATCH_ONLY":
            raise ValueError("graph relation is outside evidence-bound scope")
        if r["id"] != _digest([r["subject"], r["predicate"], r["object"], r["evidence_sha256"]]):
            raise ValueError("relation identity mismatch")
    if (manifest.get("entity_count") != len(entities) or manifest.get("relation_count") != len(relations)
            or manifest.get("entities_sha256") != _digest(entities) or manifest.get("relations_sha256") != _digest(relations)):
        raise ValueError("graph manifest digest mismatch")
    if knowledge is not None:
        expected_entities, expected_relations = project_graph(knowledge)
        if entities != expected_entities or relations != expected_relations or manifest.get("knowledge_digest") != knowledge.get("knowledge_digest"):
            raise ValueError("graph does not match verified knowledge")
    return manifest


def search_graph(directory: Path, query: str, *, limit: int = 10, hops: int = 1) -> dict[str, Any]:
    if not 1 <= limit <= 50 or not 0 <= hops <= 3:
        raise ValueError("search bounds exceeded")
    verify_graph(directory)
    entities = _read_jsonl(directory / "entities.jsonl")
    relations = _read_jsonl(directory / "relations.jsonl")
    terms = re.findall(r"[\w-]+", query.casefold(), flags=re.UNICODE)[:12]
    if not terms or len(query) > 256:
        raise ValueError("non-empty bounded search query required")
    # Query tokens are quoted and never passed as SQL fragments
    expression = " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)
    db = sqlite3.connect(":memory:")
    try:
        db.execute("CREATE VIRTUAL TABLE nodes USING fts5(node_id UNINDEXED, body)")
        db.executemany("INSERT INTO nodes(node_id, body) VALUES (?, ?)",
                       [(e["id"], e["label"] + " " + e["text"]) for e in entities])
        ranked = db.execute("SELECT node_id, bm25(nodes) FROM nodes WHERE nodes MATCH ? ORDER BY bm25(nodes), node_id LIMIT ?",
                            (expression, limit)).fetchall()
    except sqlite3.OperationalError as exc:
        raise ValueError(f"FTS5 search unavailable or invalid query: {exc}") from exc
    finally:
        db.close()
    adjacency: dict[str, set[str]] = defaultdict(set)
    for edge in relations:
        adjacency[edge["subject"]].add(edge["object"])
        adjacency[edge["object"]].add(edge["subject"])
    nodes = {e["id"]: e for e in entities}
    results = []
    for node_id, score in ranked:
        queue = deque([(node_id, 0)])
        visited = {node_id}
        while queue:
            current, depth = queue.popleft()
            if depth >= hops:
                continue
            for neighbour in sorted(adjacency[current]):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, depth + 1))
        results.append({"id": node_id, "bm25": score, "node": nodes[node_id],
                        "neighbors": sorted(visited - {node_id})[:100]})
    return {"schema_version": "1.0.0", "method": "SQLite FTS5 BM25 + bounded source-match traversal",
            "query": query, "hops": hops, "results": results,
            "limits": {"semantic_inference": False, "biological_validation": False}}


def append_graph_event(directory: Path, *, receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Append a replayable event with a previous-event digest pointer."""
    path = directory / "events.jsonl"
    prior = _read_jsonl(path) if path.exists() else []
    previous = prior[-1]["event_sha256"] if prior else None
    event = {"schema_version": "1.0.0", "run_id": receipt.get("execution_id", receipt["run_id"]),
             "logical_date": receipt["logical_date"], "outcome": "APPLIED",
             "evidence_digest": receipt["output_digest"], "previous_event_sha256": previous}
    if "execution_id" in receipt:
        event["snapshot_id"] = receipt["run_id"]
        event["change_kind"] = receipt["change_kind"]
    event["event_sha256"] = _digest(event)
    if any(x.get("run_id") == event["run_id"] for x in prior):
        raise ValueError("duplicate event run_id")
    _write_jsonl(path, prior + [event])
    return event


def verify_graph_events(directory: Path) -> int:
    path = directory / "events.jsonl"
    events = _read_jsonl(path) if path.exists() else []
    previous = None
    run_ids: set[str] = set()
    for item in events:
        claim = item.get("event_sha256")
        body = dict(item)
        body.pop("event_sha256", None)
        if claim != _digest(body) or body.get("previous_event_sha256") != previous:
            raise ValueError("graph event chain broken")
        if item.get("run_id") in run_ids or item.get("outcome") != "APPLIED":
            raise ValueError("invalid duplicate or non-applied graph event")
        run_ids.add(item["run_id"])
        previous = claim
    return len(events)