"""Validation for immutable research-workflow identity profiles."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath
from typing import Any

from .integrity import load_json_object

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
REQUIRED = {
    "schema_version",
    "repository",
    "source_commit",
    "workflow_path",
    "workflow_sha256",
    "maturity",
    "registry_status",
    "monitoring_status",
}
ALLOWED_MATURITY = {"prototype", "pilot", "candidate", "stable"}
ALLOWED_STATE = {"not-connected", "prepared", "submitted", "accepted", "verified"}


def validate_workflow_profile(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED - value.keys())
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    if value.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if not REPOSITORY.fullmatch(str(value.get("repository", ""))):
        errors.append("repository must use owner/name form")
    if not SHA40.fullmatch(str(value.get("source_commit", ""))):
        errors.append("source_commit must be a lowercase 40-character Git SHA")
    if not SHA256.fullmatch(str(value.get("workflow_sha256", ""))):
        errors.append("workflow_sha256 must be a lowercase SHA-256 digest")
    workflow_path = str(value.get("workflow_path", ""))
    parsed = PurePosixPath(workflow_path)
    if not workflow_path or parsed.is_absolute() or ".." in parsed.parts or "\\" in workflow_path:
        errors.append("workflow_path must be a safe repository-relative POSIX path")
    if value.get("maturity") not in ALLOWED_MATURITY:
        errors.append("maturity is not recognized")
    for field in ("registry_status", "monitoring_status"):
        if value.get(field) not in ALLOWED_STATE:
            errors.append(f"{field} is not recognized")
    return errors


def validate_workflow_profile_file(path: Path) -> list[str]:
    return validate_workflow_profile(load_json_object(path))

