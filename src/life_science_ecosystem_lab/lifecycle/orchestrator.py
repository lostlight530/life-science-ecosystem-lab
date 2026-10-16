"""Guarded projection and application of validated evidence candidates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from ..evidence.validation import validate_candidate_bundle
from ..knowledge import verify_knowledge
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
        if active.get("output_digest") == candidate.get("output_digest"):
            return {"outcome": "NO_MEANINGFUL_DELTA", "output_digest": candidate["output_digest"]}

    changed = [
        "data/inputs/current/candidate.json",
        "data/knowledge/current.json",
        "data/memories/current.json",
        f"data/receipts/{candidate['run_id']}.json",
    ]
    rejected = check_write_boundary(changed)
    if rejected:
        return {"outcome": "VALIDATION_FAILED", "errors": ["write boundary rejected: " + ", ".join(rejected)]}

    knowledge_output = dict(knowledge) if knowledge is not None else {
        "schema_version": "1.0.0",
        "source_bundle": candidate["output_digest"],
        "topics": candidate.get("topics", []),
    }
    memory = {
        "schema_version": "1.0.0",
        "source_bundle": candidate["output_digest"],
        "record_count": len(candidate.get("records", [])),
        "topic_count": len(candidate.get("topics", [])),
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
    _write_json(roots.root / "data" / "knowledge" / "current.json", knowledge)
    _write_json(roots.root / "data" / "memories" / "current.json", memory)
    _write_json(roots.root / "data" / "receipts" / f"{candidate['run_id']}.json", receipt)
    final = verify_state(roots)
    if not final.valid:
        raise ValueError("final state validation failed: " + "; ".join(final.errors))
    return receipt
