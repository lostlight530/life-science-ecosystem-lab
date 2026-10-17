"""Daily read-only checks with strictly separated upstream and project evidence.

The upstream catalogue is a curated pointer set, never a local copy of official
standards, official service status, registration proof or account access record.
External HTTP evidence is a *single observation* and is never a platform verdict.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

OFFICIAL = {
    "ls-login": ("https://lifescience-ri.eu/ls-login/", "https://lifescience-ri.eu/ls-login/documentation/user-documentation/user-documentation.html"),
    "workflowhub": ("https://workflowhub.eu/", "https://about.workflowhub.eu/Workflow-RO-Crate/1.1/"),
    "lifemonitor": ("https://lifemonitor.eu/", "https://lifemonitor.eu/lm_test_monitoring"),
    "openebench": ("https://openebench.bsc.es/", "https://elixir-europe.org/services/openebench"),
    "fairdomhub": ("https://fairdomhub.org/", "https://fairdomhub.org/"),
    "bio-tools": ("https://bio.tools/", "https://bio.tools/components/about/about.html"),
}
_SHA256 = re.compile(r"^[a-f0-9]{64}$")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req: Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_report(target: Path, report: dict[str, Any]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def load_object(path: Path, maximum: int = 100_000) -> tuple[dict[str, Any], str]:
    if path.stat().st_size > maximum:
        raise ValueError("manifest exceeds size limit")
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest must be a JSON object")
    return value, hashlib.sha256(raw).hexdigest()


def validate_official(value: dict[str, Any]) -> list[dict[str, str]]:
    if set(value) != {"schema_version", "scope", "services"} or value["schema_version"] != "1.0.0" or value["scope"] != "CURATED_OFFICIAL_PUBLIC_POINTERS":
        raise ValueError("invalid institutional catalogue contract")
    rows = value["services"]
    if not isinstance(rows, list) or len(rows) != len(OFFICIAL):
        raise ValueError("the six curated institutional entries must each appear exactly once")
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"id", "public_probe_url", "official_documentation_url"}:
            raise ValueError("unknown institutional catalogue fields")
        key = row.get("id")
        if not isinstance(key, str) or key not in OFFICIAL or key in seen:
            raise ValueError("unknown or duplicate official service id")
        seen.add(key)
        if (row["public_probe_url"], row["official_documentation_url"]) != OFFICIAL[key]:
            raise ValueError("official reference URL mismatch; change code and catalogue only after independent review")
    return rows


def single_http_observation(url: str, *, timeout: float = 7.0) -> dict[str, Any]:
    """Bounded GET to a compile-time pinned HTTPS URL, with redirects disabled."""
    if url not in {item[0] for item in OFFICIAL.values()}:
        raise ValueError("outbound network target is not an allowlisted official public endpoint")
    opener = build_opener(NoRedirect)
    request = Request(url, headers={
        "User-Agent": "LifeScienceEcosystemLab-ReadOnlySelfcheck/1.0",
        "Accept": "text/html,application/json;q=0.8,*/*;q=0.2",
        "Range": "bytes=0-1023",
    })
    try:
        with opener.open(request, timeout=timeout) as response:
            response.read(1024)
            return {"result": "HTTP_RESPONSE", "http_status": response.status}
    except HTTPError as error:
        code = error.code
        return {"result": "HTTP_REDIRECT" if 300 <= code < 400 else "HTTP_RESPONSE",
                "http_status": code}
    except (URLError, OSError, TimeoutError, ValueError) as error:
        # Record class only: exception bodies may expose proxy, auth or local details.
        return {"result": "INCONCLUSIVE_NETWORK", "error_type": type(error).__name__}


def institutional_report(catalogue: dict[str, Any], digest: str, *,
                         live: bool = False,
                         probe: Callable[[str], dict[str, Any]] = single_http_observation) -> dict[str, Any]:
    rows = validate_official(catalogue)
    checks = []
    for item in rows:
        observation = probe(item["public_probe_url"]) if live else {"result": "NOT_RUN_OFFLINE"}
        if not isinstance(observation, dict) or observation.get("result") not in {
            "HTTP_RESPONSE", "HTTP_REDIRECT", "INCONCLUSIVE_NETWORK", "NOT_RUN_OFFLINE",
        }:
            raise ValueError("invalid observation result")
        checks.append({
            "id": item["id"],
            "public_probe_url": item["public_probe_url"],
            "official_documentation_url": item["official_documentation_url"],
            "observation": observation,
        })
    return {
        "kind": "INSTITUTIONAL_PUBLIC_DEFAULTS_SELF_CHECK",
        "schema_version": "1.0.0",
        "observed_at": utc_now(),
        "catalogue_sha256": digest,
        "mode": "PUBLIC_HTTP_READ_ONLY" if live else "OFFLINE_CONTRACT_ONLY",
        "checks": checks,
        "inconclusive_count": sum(x["observation"]["result"] == "INCONCLUSIVE_NETWORK" for x in checks),
        "non_claims": [
            "HTTP responses do not prove service health, uptime or current official standards compliance",
            "No LS Login credentials, institution affiliation or delegated authorization checked",
            "No WorkflowHub/bio.tools registration or LifeMonitor test enrollment verified",
            "No public upstream specifications were copied or overwritten as local custom files",
        ],
    }


def validate_project_manifest(value: dict[str, Any]) -> list[str]:
    if set(value) != {"schema_version", "scope", "required_files", "required_commands"} or value["schema_version"] != "1.0.0" or value["scope"] != "PROJECT_CUSTOM_CONTRACT":
        raise ValueError("invalid custom-project manifest contract")
    files, commands = value["required_files"], value["required_commands"]
    if not isinstance(files, list) or not 12 <= len(files) <= 100 or not all(isinstance(x, str) for x in files) or len(files) != len(set(files)):
        raise ValueError("custom files must be a bounded, unique list")
    if commands != ["ls-knowledge", "ls-evidence", "ls-bio"]:
        raise ValueError("three independently callable research assets required")
    for name in files:
        if not isinstance(name, str) or len(name) > 200 or "\\" in name:
            raise ValueError("unsafe custom file path")
        p = PurePosixPath(name)
        if (p.is_absolute() or p.as_posix() != name or any(part in ("", ".", "..") for part in name.split("/"))
                or name.startswith("checks/institutional/")):
            raise ValueError("custom file cannot escape its scope or impersonate upstream defaults")
    return files


def validate_lifemonitor_config(root: Path) -> list[str]:
    """Validate only this repository's config; never contact or mutate LifeMonitor."""
    path = root / "lifemonitor.yaml"
    legacy_path = root / ".lifemonitor.yaml"
    if path.is_symlink() or not path.is_file() or legacy_path.exists() or legacy_path.is_symlink():
        return ["LIFEMONITOR_CONFIG_PATH_CONTRACT"]
    text = path.read_text(encoding="utf-8")
    errors = []
    if not re.search(r"(?m)^name:[ \\t]*\\S", text):
        errors.append("LIFEMONITOR_CONFIG_NAME")
    if not re.search(r"(?m)^issues:[ \\t]*\\n[ \\t]+check:[ \\t]*true[ \\t]*(?:#.*)?$", text):
        errors.append("LIFEMONITOR_ISSUE_CHECK_CONTRACT")
    # Leave release tracking, registry updates and visibility to account-wide
    # settings; only an explicit top-level key would override those settings.
    if re.search(r"(?m)^(?:push|public)[ \\t]*:", text):
        errors.append("LIFEMONITOR_GLOBAL_SETTINGS_OVERRIDE")
    return errors


def project_report(root: Path, manifest: dict[str, Any], digest: str) -> dict[str, Any]:
    files = validate_project_manifest(manifest)
    root = root.resolve(strict=True)
    checks = []
    errors = []
    for name in files:
        path = root / name
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root):
            errors.append("MISSING_OR_UNSAFE_FILE:" + name)
            checks.append({"path": name, "status": "FAIL"})
            continue
        raw = path.read_bytes()
        checks.append({"path": name, "status": "PRESENT", "size_bytes": len(raw),
                       "sha256": hashlib.sha256(raw).hexdigest()})
    try:
        import tomllib
        package = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
        scripts = package["project"]["scripts"]
        for cmd in manifest["required_commands"]:
            if not isinstance(scripts.get(cmd), str):
                errors.append("MISSING_ENTRYPOINT:" + cmd)
    except (OSError, KeyError, ValueError) as error:
        errors.append("INVALID_PACKAGE_METADATA:" + type(error).__name__)
    errors.extend(validate_lifemonitor_config(root))
    # No custom report may embed the separately governed institutional catalogue.
    return {
        "kind": "PROJECT_CUSTOM_SELF_CHECK",
        "schema_version": "1.0.0",
        "observed_at": utc_now(),
        "manifest_sha256": digest,
        "source_commit": os.environ.get("GITHUB_SHA", "LOCAL_UNSPECIFIED"),
        "status": "PASS" if not errors else "FAIL",
        "checks": checks,
        "errors": errors,
        "not_verified": [
            "External registry acceptance or institutional platform availability",
            "Scientific ground truth and external Agent execution identities",
            "Unexecuted or non-repeatable tasks beyond the performed repository checks",
        ],
    }


def github_summary(report: dict[str, Any]) -> str:
    heading = ("Institutional public defaults" if report["kind"].startswith("INSTITUTIONAL")
               else "Project custom evidence")
    lines = [f"### Daily self-check — {heading}", "", f"- Recorded at (UTC): {report['observed_at']}"]
    if report["kind"].startswith("INSTITUTIONAL"):
        lines.append(f"- Mode: {report['mode']}; inconclusive network observations: {report['inconclusive_count']}")
        lines.append("- **This is not official uptime monitoring or registry enrollment proof**")
        lines += ["", "| Service | Observation | HTTP |", "| --- | --- | --- |"]
        for row in report["checks"]:
            v = row["observation"]
            lines.append(f"| {row['id']} | {v['result']} | {v.get('http_status', '—')} |")
    else:
        lines.append(f"- Result: {report['status']}; inspected files: {len(report['checks'])}")
        lines.append(f"- Errors: {len(report['errors'])}")
        lines.append("- **No upstream default files or observations are included in this report**")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plane", choices=["institutional", "project"])
    parser.add_argument("--catalogue", type=Path, default=Path("checks/institutional/defaults.json"))
    parser.add_argument("--manifest", type=Path, default=Path("checks/project/manifest.json"))
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.plane == "institutional":
            value, digest = load_object(args.catalogue)
            report = institutional_report(value, digest, live=args.live)
        else:
            if args.live:
                raise ValueError("project custom plane is offline-only")
            value, digest = load_object(args.manifest)
            report = project_report(args.root, value, digest)
        write_report(args.output, report)
        summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary, "a", encoding="utf-8") as out:
                out.write(github_summary(report) + "\n")
        print(report["kind"], report.get("status", report.get("mode")), str(args.output))
        return 1 if report.get("status") == "FAIL" else 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print("DAILY_SELFCHECK_CONTRACT_FAIL", str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
