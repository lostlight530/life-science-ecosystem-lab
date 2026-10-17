"""Candidate format, provenance and semantic digest validation.

For locally supplied synthetic fixture records, strict validation is also enforced.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping

from .aggregation import canonical_bytes, stable_records
from .models import require_safe_posix_path
from .normalization import canonical_text_bytes, sha256_bytes

SHA256 = re.compile(r"^[0-9a-f]{64}$")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
REQUIRED = {"schema_version", "run_id", "profile_digest", "algorithm_version", "sources", "records", "topics", "changes", "diagnostics", "input_digest", "output_digest", "projection_eligible"}


@dataclass(frozen=True)
class BundleValidation:
    valid: bool
    errors: tuple[str, ...]


def validate_candidate_bundle(value: Mapping[str, Any]) -> BundleValidation:
    errors: list[str] = []
    missing = sorted(REQUIRED - value.keys())
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    if value.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    for field in ("profile_digest", "input_digest", "output_digest"):
        if not SHA256.fullmatch(str(value.get(field, ""))):
            errors.append(f"{field} must be a lowercase SHA-256 digest")
    # The published candidate run_id is a content identity, never an arbitrary
    # filesystem component. Rehashing a forged envelope cannot authorize it.
    input_digest = value.get("input_digest")
    profile_digest = value.get("profile_digest")
    if (isinstance(input_digest, str) and SHA256.fullmatch(input_digest) and
            isinstance(profile_digest, str) and SHA256.fullmatch(profile_digest)):
        expected_id = input_digest[:16] + "-" + profile_digest[:16]
        if value.get("run_id") != expected_id:
            errors.append("run_id does not match the canonical snapshot identity")
    records = value.get("records")
    if not isinstance(records, list):
        errors.append("records must be a list")
    else:
        try:
            ordered = stable_records(records)
            if ordered != records:
                errors.append("records must be canonical, sorted and free from retrieval timestamps")
        except (ValueError, KeyError, TypeError) as exc:
            ordered = []
            errors.append(f"invalid record identities: {exc}")
        for index, r in enumerate(records):
            if not isinstance(r, dict):
                errors.append(f"records[{index}] must be an object")
                continue
            for key in ("source_id", "repository", "path", "ref", "source_registry", "selection_rule", "trust", "collector_version"):
                if not isinstance(r.get(key), str) or not r[key]:
                    errors.append(f"records[{index}].{key} must be a non-empty string")
            if not REPO.fullmatch(str(r.get("repository", ""))):
                errors.append(f"records[{index}].repository must be owner/name")
            try:
                require_safe_posix_path(str(r.get("path", "")))
            except ValueError:
                errors.append(f"records[{index}].path is unsafe")
            for key in ("commit", "tree_sha", "blob_sha"):
                if not SHA40.fullmatch(str(r.get(key, ""))):
                    errors.append(f"records[{index}].{key} must be a Git SHA")
            if not SHA256.fullmatch(str(r.get("content_sha256", ""))):
                errors.append(f"records[{index}].content_sha256 must be a SHA-256 digest")
            elif "text" in r and (not isinstance(r["text"], str) or sha256_bytes(canonical_text_bytes(r["text"])) != r["content_sha256"]):
                errors.append(f"records[{index}] text digest mismatch")
            if not isinstance(r.get("raw_size"), int) or r["raw_size"] < 0:
                errors.append(f"records[{index}].raw_size must be a non-negative integer")
        if not errors and value.get("input_digest") != sha256_bytes(canonical_bytes(ordered)):
            errors.append("input_digest does not match canonical records")
    if isinstance(records, list):
        sources = value.get("sources")
        if not isinstance(sources, list):
            errors.append("sources must be an array")
        else:
            expected = [{"source_id": a, "repository": b, "commit": c} for a, b, c in sorted({(str(r.get("source_id")), str(r.get("repository")), str(r.get("commit"))) for r in records if isinstance(r, dict)})]
            if sources != expected:
                errors.append("sources do not match collected records")
    if not isinstance(value.get("projection_eligible"), bool):
        errors.append("projection_eligible must be boolean")
    for key in ("topics", "changes", "diagnostics"):
        if not isinstance(value.get(key), list):
            errors.append(f"{key} must be an array")
    if not errors:
        body = dict(value)
        claimed = str(body.pop("output_digest"))
        if sha256_bytes(canonical_bytes(body)) != claimed:
            errors.append("output_digest does not match bundle content")
    return BundleValidation(not errors, tuple(errors))
