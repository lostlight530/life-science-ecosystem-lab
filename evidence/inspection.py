"""Read-only, local research software and workflow evidence inspector.

This is a bounded preflight, not a scientific truth check or external
WorkflowHub/bio.tools/Bioschemas conformance certification. No network or
untrusted workflow execution is performed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

MAX_DOCUMENT_BYTES = 2_000_000


def _load(root: Path, relative: str) -> tuple[Path, str] | None:
    candidate = root / relative
    target = candidate.resolve()
    if not target.is_relative_to(root) or not target.is_file() or candidate.is_symlink():
        return None
    if target.stat().st_size > MAX_DOCUMENT_BYTES:
        raise ValueError(f"document too large: {relative}")
    return target, target.read_text(encoding="utf-8")


def inspect_repository(directory: Path) -> dict[str, Any]:
    root = directory.resolve()
    if not root.is_dir():
        raise ValueError("inspection input must be a directory")
    findings: list[dict[str, str]] = []
    observed: list[str] = []

    def add(rule: str, outcome: str, detail: str, path: str = "") -> None:
        findings.append({"rule": rule, "status": outcome, "detail": detail, "path": path})

    readme = _load(root, "README.md")
    add("documentation.readme", "PASS" if readme else "WARN", "README available" if readme else "README not found", "README.md")
    if readme:
        observed.append("README.md")
    cff = _load(root, "CITATION.cff")
    if cff:
        observed.append("CITATION.cff")
        add("citation.version", "PASS" if "cff-version:" in cff[1] else "WARN",
            "Citation metadata contains CFF version" if "cff-version:" in cff[1] else "No CFF version declared", "CITATION.cff")
    else:
        # Some real bioinformatics projects (e.g. nf-core workflows) supply
        # CITATIONS.md with linked primary/software citations rather than CFF.
        # The alternative is evidence of guidance, NOT CFF conformance.
        alternatives = ("CITATIONS.md", "CITATION.md", "CITATION.txt")
        alternate = next(((path, item) for path in alternatives
                          if (item := _load(root, path)) is not None), None)
        if alternate is not None:
            observed.append(alternate[0])
            add("citation.alternative", "WARN",
                f"CITATION.cff absent; alternative citation guidance at {alternate[0]} (not CFF validation)",
                alternate[0])
        else:
            add("citation.present", "WARN", "Root CITATION.cff not found; citation information in other locations was not assessed", "CITATION.cff")
    crate = _load(root, "ro-crate-metadata.json")
    if crate:
        observed.append("ro-crate-metadata.json")
        try:
            body = json.loads(crate[1])
        except json.JSONDecodeError:
            add("rocrate.json", "FAIL", "Invalid RO-Crate JSON", "ro-crate-metadata.json")
        else:
            graph = body.get("@graph") if isinstance(body, dict) else None
            if not isinstance(graph, list):
                add("rocrate.graph", "FAIL", "@graph must be an array", "ro-crate-metadata.json")
            else:
                root_items = [x for x in graph if isinstance(x, dict) and x.get("@id") == "./"]
                entity = root_items[0].get("mainEntity") if root_items else None
                main = entity.get("@id") if isinstance(entity, dict) else None
                if not isinstance(main, str) or not main or main.startswith(("/", "http:", "https:")) or ".." in Path(main).parts:
                    add("rocrate.main_entity", "FAIL", "Local mainEntity path missing or unsafe", "ro-crate-metadata.json")
                elif _load(root, main) is None:
                    add("rocrate.main_entity", "FAIL", "Main workflow file not present", main)
                else:
                    observed.append(main)
                    add("rocrate.main_entity", "PASS", "Main workflow referenced by existing local file", main)
    else:
        add("rocrate.present", "WARN",
            "No root-level ro-crate-metadata.json (may be in examples; not required for service repositories)",
            "ro-crate-metadata.json")
    bioschemas = 0
    metadata = root / "metadata"
    if metadata.is_dir() and not metadata.is_symlink():
        for candidate in sorted(metadata.glob("bioschemas-*.jsonld"))[:30]:
            item = _load(root, candidate.relative_to(root).as_posix())
            if not item:
                add("bioschemas.unsafe", "FAIL", "Unsafe local metadata file", candidate.name)
                continue
            observed.append(candidate.relative_to(root).as_posix())
            try:
                value = json.loads(item[1])
                if not isinstance(value, dict) or "@type" not in value or "name" not in value:
                    raise ValueError("missing basic JSON-LD identity")
            except (json.JSONDecodeError, ValueError):
                add("bioschemas.identity", "FAIL", "Invalid Bioschemas JSON-LD basic identity", candidate.name)
            else:
                bioschemas += 1
                add("bioschemas.identity", "PASS", "Basic JSON-LD identity present (not profile certification)", candidate.name)
    if not bioschemas:
        add("bioschemas.present", "WARN", "No successfully inspected Bioschemas descriptor")
    observed = sorted(set(observed))
    counters = {s: sum(f["status"] == s for f in findings) for s in ("PASS", "WARN", "FAIL")}
    payload = {"schema_version": "1.0.0", "kind": "RESEARCH_SOFTWARE_EVIDENCE_INSPECTION",
               "object": str(directory), "observed_files": observed, "findings": findings, "counts": counters,
               "status": "FAIL" if counters["FAIL"] else "WARN" if counters["WARN"] else "PASS",
               "scope": "local, static, nonexecuting, basic scientific-software identity and metadata preflight",
               "unverified": ["scientific validity", "external registrations", "full standards conformance",
                              "remote links", "workflow reproducibility"]}
    stable = dict(payload)
    stable.pop("object")
    payload["report_sha256"] = hashlib.sha256(json.dumps(stable, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    return payload


def write_reports(report: dict[str, Any], output: Path, *, markdown: Path | None = None, sarif: Path | None = None) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if markdown:
        markdown.parent.mkdir(parents=True, exist_ok=True)
        lines = ["# Research Software Evidence Inspection", "", f"Status: **{report['status']}**", "",
                 "| Rule | Status | Detail |", "| --- | --- | --- |"]
        for x in report["findings"]:
            detail = x["detail"].replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {x['rule']} | {x['status']} | {detail} |")
        lines.extend(["", "Static inspection only; no scientific or external registry verification", ""])
        markdown.write_text("\n".join(lines), encoding="utf-8")
    if sarif:
        sarif.parent.mkdir(parents=True, exist_ok=True)
        results = []
        for x in report["findings"]:
            if x["status"] == "PASS":
                continue
            item = {"ruleId": x["rule"], "level": "error" if x["status"] == "FAIL" else "warning",
                    "message": {"text": x["detail"]}}
            if x["path"]:
                item["locations"] = [{"physicalLocation": {"artifactLocation": {"uri": x["path"]}}}]
            results.append(item)
        payload = {"version": "2.1.0", "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
                   "runs": [{"tool": {"driver": {"name": "ls-evidence", "informationUri": "https://github.com/lostlight530/life-science-ecosystem-lab", "rules": []}}, "results": results}]}
        sarif.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")