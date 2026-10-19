"""Resolve reviewed Workflow profiles without accepting arbitrary paths or commands."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0.0"
PROFILE_IDS = frozenset({"native", "protein_structure"})
AUTHORITIES = {"native": "PRODUCTION", "protein_structure": "ISOLATED_RESEARCH"}
PATH_KEYS = ("sources", "topics", "agent_handoff", "sample_manifest")
SAFE_PATH = re.compile(r"^[A-Za-z0-9._/-]+$")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_relative_path(value: Any) -> Path:
    if not isinstance(value, str) or not value or not SAFE_PATH.fullmatch(value):
        raise ValueError("profile path must be a safe repository-relative path")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise ValueError("profile path must stay inside the repository")
    return path


def load_profile_registry(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    if len(raw) > 20_000:
        raise ValueError("workflow profile registry is too large")
    registry = json.loads(raw)
    validate_profile_registry(registry)
    return registry, hashlib.sha256(raw).hexdigest()


def validate_profile_registry(registry: dict[str, Any]) -> None:
    if not isinstance(registry, dict) or set(registry) != {"schema_version", "profiles"}:
        raise ValueError("unexpected workflow profile registry keys")
    if registry["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported workflow profile registry schema")
    profiles = registry["profiles"]
    if not isinstance(profiles, dict) or set(profiles) != PROFILE_IDS:
        raise ValueError("reviewed workflow profile set changed")
    for profile_id, profile in profiles.items():
        required = {"authority", "sources", "topics", "persistence_allowed"}
        optional = {"agent_handoff", "sample_manifest"}
        if not isinstance(profile, dict) or not required.issubset(profile) or not set(profile) <= required | optional:
            raise ValueError("invalid workflow profile shape")
        if profile["authority"] != AUTHORITIES[profile_id]:
            raise ValueError("workflow profile authority mismatch")
        if type(profile["persistence_allowed"]) is not bool:
            raise ValueError("persistence_allowed must be boolean")
        if profile["persistence_allowed"] != (profile_id == "native"):
            raise ValueError("only the native profile may allow persistence")
        for key in PATH_KEYS:
            if key in profile:
                _safe_relative_path(profile[key])


def resolve_profile(
    root: Path,
    registry: dict[str, Any],
    registry_sha256: str,
    profile_id: str,
) -> dict[str, Any]:
    if profile_id not in PROFILE_IDS or profile_id not in registry["profiles"]:
        raise ValueError("unknown or unreviewed workflow profile")
    root = root.resolve(strict=True)
    profile = registry["profiles"][profile_id]
    resolved: dict[str, str] = {}
    digests: dict[str, str] = {}
    for key in PATH_KEYS:
        if key not in profile:
            continue
        relative = _safe_relative_path(profile[key])
        absolute = (root / relative).resolve(strict=True)
        try:
            absolute.relative_to(root)
        except ValueError as error:
            raise ValueError("workflow profile escaped repository root") from error
        if not absolute.is_file():
            raise ValueError("workflow profile path is not a file")
        resolved[key] = relative.as_posix()
        digests[f"{key}_sha256"] = _digest(absolute)
    return {
        "kind": "WORKFLOW_EXECUTION_PROFILE",
        "schema_version": SCHEMA_VERSION,
        "profile_id": profile_id,
        "authority": profile["authority"],
        "persistence_allowed": profile["persistence_allowed"],
        "registry_sha256": registry_sha256,
        **resolved,
        **digests,
    }


def _write_github_env(path: Path, receipt: dict[str, Any]) -> None:
    values = {
        "LS_PROFILE_ID": receipt["profile_id"],
        "LS_PROFILE_AUTHORITY": receipt["authority"],
        "LS_PROFILE_PERSISTENCE_ALLOWED": str(receipt["persistence_allowed"]).lower(),
        "LS_SOURCES_PROFILE": receipt["sources"],
        "LS_TOPICS_PROFILE": receipt["topics"],
    }
    if "agent_handoff" in receipt:
        values["LS_AGENT_HANDOFF"] = receipt["agent_handoff"]
    if "sample_manifest" in receipt:
        values["LS_SAMPLE_MANIFEST"] = receipt["sample_manifest"]
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resolve a reviewed Workflow execution profile")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--registry", type=Path, default=Path("evidence/profiles/workflow-profiles.json"))
    parser.add_argument("--profile", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--github-env", type=Path)
    args = parser.parse_args(argv)
    registry, digest = load_profile_registry(args.registry)
    receipt = resolve_profile(args.root, registry, digest, args.profile)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.github_env:
        _write_github_env(args.github_env, receipt)
    print(json.dumps({"profile_id": receipt["profile_id"], "authority": receipt["authority"],
                      "persistence_allowed": receipt["persistence_allowed"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
