"""Guarded projection and application of validated evidence candidates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from evidence.validation import validate_candidate_bundle
from ..knowledge import verify_knowledge
from ..graph import write_graph, append_graph_event
from .guard import check_write_boundary, world_line_matches
from .state import StateRoots, apply_candidate, verify_state


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def apply_lifecycle(
    candidate: Mapping[str, Any],
    roots: StateRoots,
    *,
    logical_date: str,
    validated_head: str,
    current_head: str,
    knowledge: Mapping[str, Any] | None = None,
    topic_registry: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    report = validate_candidate_bundle(candidate)
    if not report.valid or candidate.get("projection_eligible") is not True:
        return {"outcome": "VALIDATION_FAILED", "errors": list(report.errors)}
    if (knowledge is None) != (topic_registry is None):
        return {"outcome": "VALIDATION_FAILED", "errors": ["knowledge and topic registry must be supplied together"]}
    if knowledge is not None and topic_registry is not None:
        try:
            verify_knowledge(candidate, topic_registry, knowledge)
        except ValueError as exc:
            return {"outcome": "VALIDATION_FAILED", "errors": [str(exc)]}
    if not world_line_matches(validated_head, current_head):
        return {
            "outcome": "CONFLICTED_WORLD_LINE_NO_APPLY",
            "validated_head": validated_head,
            "current_head": current_head,
        }
    if roots.current.exists():
        active = json.loads(roots.current.read_text(encoding="utf-8"))
        previous_knowledge = roots.root / "data" / "knowledge" / "current.json"
        same_knowledge = (knowledge is None or
                          (previous_knowledge.exists() and json.loads(previous_knowledge.read_text(encoding="utf-8")) == knowledge))
        if (active.get("input_digest") == candidate.get("input_digest") and
                active.get("profile_digest") == candidate.get("profile_digest") and same_knowledge):
            return {"outcome": "NO_MEANINGFUL_DELTA", "output_digest": candidate["output_digest"]}

    changed = [
        "data/inputs/current/candidate.json",
        "data/knowledge/current.json",
        "data/memories/current.json",
        f"data/receipts/{candidate['run_id']}.json",
    ]
    if knowledge is not None:
        changed.extend([
            "data/knowledge/entities.jsonl", "data/knowledge/relations.jsonl",
            "data/knowledge/graph-manifest.json", "data/knowledge/events.jsonl",
        ])
    rejected = check_write_boundary(changed)
    if rejected:
        return {"outcome": "VALIDATION_FAILED", "errors": ["write boundary rejected: " + ", ".join(rejected)]}

    knowledge_output = dict(knowledge) if knowledge is not None else {
        "schema_version": "1.0.0",
        "source_bundle": candidate["output_digest"],
        "topics": candidate.get("topics", []),
    }
    old_knowledge_path = roots.root / "data" / "knowledge" / "current.json"
    old_knowledge = json.loads(old_knowledge_path.read_text(encoding="utf-8")) if old_knowledge_path.exists() else {}
    old_topics = {topic["topic_id"]: topic for topic in old_knowledge.get("topics", []) if isinstance(topic, dict) and "topic_id" in topic}
    new_topics = {topic["topic_id"]: topic for topic in knowledge_output.get("topics", []) if isinstance(topic, dict) and "topic_id" in topic}
    transitions = [
        {"topic_id": name,
         "state": "ADDED" if name not in old_topics else "REMOVED" if name not in new_topics
                  else "UNCHANGED" if old_topics[name] == new_topics[name] else "UPDATED",
         "previous_coverage": old_topics.get(name, {}).get("coverage"),
         "current_coverage": new_topics.get(name, {}).get("coverage")}
        for name in sorted(set(old_topics) | set(new_topics))
    ]
    memory = {
        "schema_version": "1.0.0",
        "source_bundle": candidate["output_digest"],
        "record_count": len(candidate.get("records", [])),
        "topic_count": len(candidate.get("topics", [])),
        "previous_knowledge_digest": old_knowledge.get("knowledge_digest"),
        "current_knowledge_digest": knowledge_output.get("knowledge_digest"),
        "topic_transitions": transitions,
        "unresolved_topics": [item["topic_id"] for item in knowledge_output.get("unresolved", [])],
    }
    receipt: dict[str, Any] = {
        "schema_version": "1.0.0",
        "run_id": candidate["run_id"],
        "logical_date": logical_date,
        "validated_head": validated_head,
        "current_head": current_head,
        "input_digest": candidate["input_digest"],
        "output_digest": candidate["output_digest"],
        "changed_paths": changed,
        "outcome": "APPLIED",
    }
    apply_candidate(candidate, roots, logical_date=logical_date)
    _write_json(roots.root / "data" / "knowledge" / "current.json", knowledge_output)
    _write_json(roots.root / "data" / "memories" / "current.json", memory)
    _write_json(roots.root / "data" / "receipts" / f"{candidate['run_id']}.json", receipt)
    if knowledge is not None:
        graph_root = roots.root / "data" / "knowledge"
        write_graph(knowledge_output, graph_root)
        append_graph_event(graph_root, receipt=receipt)
    final = verify_state(roots)
    if not final.valid:
        raise ValueError("final state validation failed: " + "; ".join(final.errors))
    return receipt
