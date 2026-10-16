"""Stable value objects shared by the evidence pipeline."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePosixPath

SHA40 = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_PART = re.compile(r"^[A-Za-z0-9_.-]+$")


def require_safe_posix_path(value: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "\\" in value:
        raise ValueError("path must be a safe repository-relative POSIX path")
    return value


@dataclass(frozen=True)
class SourceIdentity:
    owner: str
    repository: str
    ref: str

    def __post_init__(self) -> None:
        if not REPOSITORY_PART.fullmatch(self.owner) or not REPOSITORY_PART.fullmatch(self.repository):
            raise ValueError("repository must use owner/name form")
        if not self.ref or any(character.isspace() for character in self.ref):
            raise ValueError("ref must be non-empty and contain no whitespace")

    @property
    def key(self) -> str:
        return f"{self.owner}/{self.repository}@{self.ref}"


@dataclass(frozen=True)
class GitTreeEntry:
    path: str
    object_id: str
    size: int

    def __post_init__(self) -> None:
        require_safe_posix_path(self.path)
        if not SHA40.fullmatch(self.object_id):
            raise ValueError("object_id must be a lowercase 40-character Git SHA")
        if self.size < 0:
            raise ValueError("size must be non-negative")
