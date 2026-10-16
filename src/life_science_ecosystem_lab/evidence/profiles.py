"""Strict profile loaders for approved GitHub sources and evidence topics."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .models import require_safe_posix_path

REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
ALLOWED_TRUST = {"primary", "maintainer", "community"}


@dataclass(frozen=True)
class SourceRegistry:
    schema_version: str
    registry_id: str
    sources: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True)
class TopicRegistry:
    schema_version: str
    registry_id: str
    topics: tuple[Mapping[str, Any], ...]


def _object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("profile must be a JSON object")
    return value


def validate_source_registry(value: Mapping[str, object]) -> list[str]:
    errors: list[str] = []
    if value.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if not value.get("registry_id"):
        errors.append("registry_id is required")
    sources = value.get("sources")
    if not isinstance(sources, list) or not sources:
        return errors + ["sources must be a non-empty array"]
    identifiers: set[str] = set()
    identities: set[str] = set()
    for index, item in enumerate(sources):
        prefix = f"sources[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        identifier = str(item.get("id", ""))
        if not identifier or identifier in identifiers:
            errors.append(f"{prefix}.id must be unique and non-empty")
        identifiers.add(identifier)
        repository = str(item.get("repository", ""))
        if not REPOSITORY.fullmatch(repository):
            errors.append(f"{prefix}.repository must use owner/name form")
        identity = f"{repository}@{item.get('ref', '')}"
        if identity in identities:
            errors.append(f"{prefix} duplicates source identity {identity}")
        identities.add(identity)
        if item.get("approved") is not True:
            errors.append(f"{prefix}.approved must be true")
        if item.get("trust") not in ALLOWED_TRUST:
            errors.append(f"{prefix}.trust is not recognized")
        includes = item.get("include")
        if not isinstance(includes, list) or not includes:
            errors.append(f"{prefix}.include must be a non-empty array")
        for field in ("include", "exclude"):
            patterns = item.get(field, [])
            if not isinstance(patterns, list):
                errors.append(f"{prefix}.{field} must be an array")
                continue
            for pattern in patterns:
                try:
                    require_safe_posix_path(str(pattern))
                except ValueError:
                    errors.append(f"{prefix}.{field} entries must be safe repository-relative POSIX paths")
    return errors


def validate_topic_registry(value: Mapping[str, object]) -> list[str]:
    errors: list[str] = []
    if value.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    topics = value.get("topics")
    if not isinstance(topics, list) or not topics:
        return errors + ["topics must be a non-empty array"]
    identifiers: set[str] = set()
    for index, item in enumerate(topics):
        if not isinstance(item, dict):
            errors.append(f"topics[{index}] must be an object")
            continue
        identifier = str(item.get("id", ""))
        if not identifier or identifier in identifiers:
            errors.append(f"topics[{index}].id must be unique and non-empty")
        identifiers.add(identifier)
        aliases = item.get("aliases")
        if not isinstance(aliases, list) or not aliases:
            errors.append(f"topics[{index}].aliases must be a non-empty array")
        if not isinstance(item.get("minimum_matches"), int) or int(item.get("minimum_matches", 0)) < 1:
            errors.append(f"topics[{index}].minimum_matches must be a positive integer")
    return errors


def load_source_registry(path: Path) -> SourceRegistry:
    value = _object(path)
    errors = validate_source_registry(value)
    if errors:
        raise ValueError("; ".join(errors))
    return SourceRegistry(str(value["schema_version"]), str(value["registry_id"]), tuple(value["sources"]))


def load_topic_registry(path: Path) -> TopicRegistry:
    value = _object(path)
    errors = validate_topic_registry(value)
    if errors:
        raise ValueError("; ".join(errors))
    return TopicRegistry(str(value["schema_version"]), str(value["registry_id"]), tuple(value["topics"]))
