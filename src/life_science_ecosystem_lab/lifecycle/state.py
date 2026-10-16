"""Append-only archive and active-state transitions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from ..evidence.validation import validate_candidate_bundle


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


def apply_candidate(candidate: Mapping[str, Any], roots: StateRoots, *, logical_date: str) -> None:
    year, month, _ = logical_date.split("-", 2)
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


def verify_state(roots: StateRoots) -> ValidationReport:
    errors: list[str] = []
    if roots.current.exists():
        try:
            current = json.loads(roots.current.read_text(encoding="utf-8"))
            report = validate_candidate_bundle(current)
            if not report.valid:
                errors.extend("current: " + e for e in report.errors)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
    for path in roots.archive.rglob("*.json") if roots.archive.exists() else ():
        try:
            archived = json.loads(path.read_text(encoding="utf-8"))
            report = validate_candidate_bundle(archived)
            if not report.valid:
                errors.extend(f"archive {path}: " + e for e in report.errors)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid archive {path}: {exc}")
    return ValidationReport(not errors, tuple(errors))
