"""Profile-driven GitHub evidence collection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .models import GitTreeEntry, SourceIdentity
from .normalization import canonical_text_bytes, normalize_text_bytes, sha256_bytes
from .profiles import SourceRegistry
from .selection import select_paths
from .transport import GitHubTransport


@dataclass(frozen=True)
class CollectionResult:
    records: tuple[Mapping[str, Any], ...]
    diagnostics: tuple[Mapping[str, str], ...]


def collect_sources(
    registry: SourceRegistry,
    transport: GitHubTransport,
    *,
    retrieved_at: str,
) -> CollectionResult:
    records: list[Mapping[str, Any]] = []
    diagnostics: list[Mapping[str, str]] = []
    for profile in sorted(registry.sources, key=lambda item: str(item["id"])):
        owner, repository = str(profile["repository"]).split("/", 1)
        identity = SourceIdentity(owner, repository, str(profile["ref"]))
        try:
            commit = transport.get_commit(identity, identity.ref)
        except Exception as exc:
            if profile.get("required", True):
                raise
            diagnostics.append({"source_id": str(profile["id"]), "reason": "OPTIONAL_SOURCE_UNAVAILABLE", "detail": str(exc)})
            continue
        commit_sha = str(commit.get("sha", ""))
        commit_body = commit.get("commit")
        if len(commit_sha) != 40 or not isinstance(commit_body, Mapping):
            raise ValueError(f"INVALID_COMMIT for {identity.key}")
        tree_body = commit_body.get("tree")
        if not isinstance(tree_body, Mapping) or len(str(tree_body.get("sha", ""))) != 40:
            raise ValueError(f"INVALID_TREE_ID for {identity.key}")
        tree_sha = str(tree_body["sha"])
        response = transport.get_tree(identity, tree_sha)
        if response.get("truncated") is True:
            raise ValueError(f"TREE_TRUNCATED for {identity.key}")
        entries: list[GitTreeEntry] = []
        for item in response.get("tree", []):
            if isinstance(item, Mapping) and item.get("type") == "blob":
                entries.append(GitTreeEntry(str(item["path"]), str(item["sha"]), int(item.get("size", 0))))
        for entry in select_paths(entries, profile):
            raw = transport.get_blob(identity, entry.object_id)
            text = normalize_text_bytes(raw)
            records.append({
                "source_id": profile["id"],
                "source_registry": registry.registry_id,
                "repository": f"{owner}/{repository}",
                "ref": identity.ref,
                "commit": commit_sha,
                "tree_sha": tree_sha,
                "path": entry.path,
                "blob_sha": entry.object_id,
                "raw_size": len(raw),
                "content_sha256": sha256_bytes(canonical_text_bytes(text)),
                "retrieved_at": retrieved_at,
                "selection_rule": f"{profile['id']}@{registry.schema_version}",
                "trust": profile["trust"],
                "collector_version": "0.3.0",
                "text": text,
            })
    return CollectionResult(tuple(sorted(records, key=lambda item: (str(item["source_id"]), str(item["repository"]), str(item["path"])))), tuple(diagnostics))
