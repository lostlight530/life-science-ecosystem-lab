"""Approved tree-path selection."""

from __future__ import annotations

from fnmatch import fnmatch
from typing import Iterable, Mapping, Sequence

from .models import GitTreeEntry


def _matches(path: str, patterns: Sequence[str]) -> bool:
    return any(fnmatch(path, pattern) or ("/**/" in pattern and fnmatch(path, pattern.replace("/**/", "/"))) for pattern in patterns)


def select_paths(entries: Iterable[GitTreeEntry], profile: Mapping[str, object]) -> tuple[GitTreeEntry, ...]:
    includes = tuple(str(item) for item in profile.get("include", ()))
    excludes = tuple(str(item) for item in profile.get("exclude", ()))
    max_bytes = int(profile.get("max_bytes", 1_000_000))
    selected = [
        entry
        for entry in entries
        if entry.size <= max_bytes and _matches(entry.path, includes) and not _matches(entry.path, excludes)
    ]
    return tuple(sorted(selected, key=lambda item: (item.path, item.object_id)))
