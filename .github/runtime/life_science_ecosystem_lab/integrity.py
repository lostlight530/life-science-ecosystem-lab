"""Canonical research-record hashing with no domain interpretation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def load_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("input must be a JSON object")
    return value


def canonical_json_bytes(value: Any) -> bytes:
    text = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return text.encode("utf-8")


def build_record_manifest(source: Path) -> dict[str, Any]:
    value = load_json_object(source)
    payload = canonical_json_bytes(value)
    return {
        "schema_version": "1.0.0",
        "algorithm": "sha256",
        "canonicalization": "json-sort-keys-utf8-v1",
        "media_type": "application/json",
        "source_name": source.name,
        "canonical_bytes": len(payload),
        "canonical_sha256": hashlib.sha256(payload).hexdigest(),
    }


def write_manifest(manifest: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

