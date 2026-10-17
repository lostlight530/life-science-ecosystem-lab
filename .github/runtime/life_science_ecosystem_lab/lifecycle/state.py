"""Append-only archive and active-state transitions."""

from __future__ import annotations

import json
import re
from datetime import date
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from evidence.validation import validate_candidate_bundle
from ..graph import verify_graph, verify_graph_events


def _bytes(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


@dataclass(frozen=True)
class ValidationReport:
    valid: bool
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class StateRoots:
    root: Path

    @property
    def current(self) -> Path:
        return self.root / "data" / "inputs" / "current" / "candidate.json"

    @property
    def archive(self) -> Path:
        return self.root / "data" / "inputs" / "archive"

    @property
    def state(self) -> Path:
        return self.root / "data" / "state"


def validated_date_parts(logical_date: str) -> tuple[str, str]:
    """Accept only canonical Gregorian YYYY-MM-DD before constructing paths."""
    try:
        parsed = date.fromisoformat(logical_date)
    except (TypeError, ValueError) as exc:
        raise ValueError("logical_date must be an ISO YYYY-MM-DD calendar date") from exc
    if parsed.isoformat() != logical_date:
        raise ValueError("logical_date must be an ISO YYYY-MM-DD calendar date")
    return f"{parsed.year:04d}", f"{parsed.month:02d}"


def apply_candidate(candidate: Mapping[str, Any], roots: StateRoots, *, logical_date: str) -> None:
    year, month = validated_date_parts(logical_date)
    new_bytes = _bytes(candidate)
    if roots.current.exists():
        previous = json.loads(roots.current.read_text(encoding="utf-8"))
        archive = roots.archive / year / month / f"{previous['run_id']}-{previous['output_digest'][:12]}.json"
        archive.parent.mkdir(parents=True, exist_ok=True)
        previous_bytes = _bytes(previous)
        if archive.exists() and archive.read_bytes() != previous_bytes:
            raise ValueError(f"archive collision at {archive}")
        if not archive.exists():
            archive.write_bytes(previous_bytes)
    roots.current.parent.mkdir(parents=True, exist_ok=True)
    temporary = roots.current.with_suffix(".tmp")
    temporary.write_bytes(new_bytes)
    temporary.replace(roots.current)


def verify_state(roots: StateRoots, *, require_accepted: bool = False) -> ValidationReport:
    errors: list[str] = []
    if require_accepted:
        if not roots.current.is_file():
            errors.append('no accepted current evidence snapshot')
        if not (roots.root / 'data' / 'knowledge' / 'current.json').is_file():
            errors.append('no accepted current knowledge')
        if not (roots.root / 'data' / 'knowledge' / 'events.jsonl').is_file():
            errors.append('no accepted knowledge event ledger')
    if roots.current.exists():
        try:
            current = json.loads(roots.current.read_text(encoding="utf-8"))
            report = validate_candidate_bundle(current)
            if not report.valid:
                errors.extend("current: " + e for e in report.errors)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
    knowledge_path = roots.root / "data" / "knowledge" / "current.json"
    if knowledge_path.exists():
        try:
            knowledge = json.loads(knowledge_path.read_text(encoding="utf-8"))
            if isinstance(knowledge, dict) and isinstance(knowledge.get("knowledge_graph"), dict):
                graph_dir = knowledge_path.parent
                verify_graph(graph_dir, knowledge)
                event_count = verify_graph_events(graph_dir)
                if require_accepted and not event_count:
                    errors.append('accepted knowledge has no graph events')
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            errors.append(f"knowledge graph integrity: {exc}")
    if require_accepted and not any((roots.root / 'data' / 'receipts').glob('*.json')):
        errors.append('no accepted run receipt')
    if require_accepted and roots.current.is_file():
        event_file = roots.root / 'data' / 'knowledge' / 'events.jsonl'
        if event_file.is_file():
            try:
                events = [json.loads(line) for line in event_file.read_text(encoding='utf-8').splitlines() if line.strip()]
                current = json.loads(roots.current.read_text(encoding='utf-8'))
                if not events or events[-1].get('evidence_digest') != current.get('output_digest'):
                    errors.append('last accepted graph event does not match active evidence snapshot')
                elif ('snapshot_id' in events[-1] and
                      events[-1]['snapshot_id'] != current.get('run_id')):
                    errors.append('last accepted graph event has a different snapshot ID')
                # New-format accepted events have a uniquely named receipt.
                # Older ledgers remain readable without inventing a receipt link.
                if events and 'snapshot_id' in events[-1]:
                    event = events[-1]
                    execution_id = event.get('run_id')
                    if not isinstance(execution_id, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', execution_id):
                        errors.append('latest event execution identity is unsafe')
                    else:
                        receipt_file = roots.root / 'data' / 'receipts' / f'{execution_id}.json'
                        if not receipt_file.is_file():
                            errors.append('latest accepted event has no matching receipt')
                        else:
                            receipt = json.loads(receipt_file.read_text(encoding='utf-8'))
                            if (not isinstance(receipt, dict) or receipt.get('execution_id') != execution_id or
                                    receipt.get('snapshot_id') != event.get('snapshot_id') or
                                    receipt.get('output_digest') != event.get('evidence_digest') or
                                    receipt.get('outcome') != 'APPLIED'):
                                errors.append('latest accepted receipt does not match graph event')
            except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
                errors.append(f'event-to-current binding invalid: {exc}')
    for path in roots.archive.rglob("*.json") if roots.archive.exists() else ():
        try:
            archived = json.loads(path.read_text(encoding="utf-8"))
            report = validate_candidate_bundle(archived)
            if not report.valid:
                errors.extend(f"archive {path}: " + e for e in report.errors)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid archive {path}: {exc}")
    return ValidationReport(not errors, tuple(errors))
