"""Write-surface and world-line guards."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Iterable

ALLOWED_ROOTS = (
    "data/inputs/current/",
    "data/inputs/archive/",
    "data/state/",
    "data/knowledge/",
    "data/memories/",
    "data/receipts/",
)


def check_write_boundary(paths: Iterable[str]) -> list[str]:
    rejected: list[str] = []
    for value in paths:
        normalized = PurePosixPath(value).as_posix()
        if normalized.startswith("/") or ".." in PurePosixPath(normalized).parts or not normalized.startswith(ALLOWED_ROOTS) or normalized.count("data/") > 1:
            rejected.append(value)
    return sorted(rejected)


def world_line_matches(validated_head: str, current_head: str) -> bool:
    return len(validated_head) == 40 and validated_head == current_head
