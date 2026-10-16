"""Transport protocol for GitHub evidence acquisition."""

from __future__ import annotations

from typing import Mapping, Protocol

from .models import SourceIdentity


class GitHubTransport(Protocol):
    def get_repository(self, identity: SourceIdentity) -> Mapping[str, object]: ...
    def get_commit(self, identity: SourceIdentity, ref: str) -> Mapping[str, object]: ...
    def get_tree(self, identity: SourceIdentity, tree_sha: str) -> Mapping[str, object]: ...
    def get_blob(self, identity: SourceIdentity, blob_sha: str) -> bytes: ...
