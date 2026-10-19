"""Life-sciences cross-domain research-software evidence contract.

This is an OFFLINE software-engineering validator, not a biological inference
algorithm, standards certification, or scientific acceptance authority.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

VERSION = "0.1.0"
KIND = "LS_RSE_INTEROP_BUNDLE"
DOMAINS = frozenset({
    "genomics", "transcriptomics", "proteomics", "structural_biology",
    "cell_biology", "microscopy", "metabolomics", "microbiome",
    "ecology_life_sciences", "life_sciences_integrative",
})
OUTCOMES = frozenset({"SUCCEEDED", "FAILED", "NOT_RUN", "UNKNOWN"})
IDENTIFIER = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.:-]{0,95}$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")
MAX_ITEMS = 128
MAX_SOURCE_BYTES = 2_000_000


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")).hexdigest()


def _id(value: Any) -> bool:
    return isinstance(value, str) and IDENTIFIER.fullmatch(value) is not None


def _text(value: Any, max_length: int = 400) -> bool:
    return isinstance(value, str) and 0 < len(value) <= max_length and "\x00" not in value


def _array(value: Any, max_length: int = MAX_ITEMS) -> bool:
    return isinstance(value, list) and len(value) <= max_length


def _problem(problems: list[dict[str, str]], code: str, subject: str) -> None:
    problems.append({"code": code, "subject": subject})


def _check_local(root: Path, relative: str, digest: str, errors: list[dict[str, str]], asset: str) -> bool:
    if (not _text(relative, 240) or "\\" in relative or relative.startswith("/")
            or any(part in ("", ".", "..") for part in relative.split("/"))):
        _problem(errors, "UNSAFE_PATH", asset)
        return False
    try:
        target = (root / relative).resolve(strict=True)
        target.relative_to(root)
        if not target.is_file() or target.stat().st_size > MAX_SOURCE_BYTES:
            _problem(errors, "INVALID_LOCAL_ASSET", asset)
            return False
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
    except (OSError, ValueError):
        _problem(errors, "LOCAL_ASSET_UNAVAILABLE_OR_ESCAPED", asset)
        return False
    if actual != digest:
        _problem(errors, "LOCAL_DIGEST_MISMATCH", asset)
        return False
    return True


def assess(bundle: Any, root: Path) -> dict[str, Any]:
    """Validate independent cross-domain software contracts; never execute inputs."""
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    checked = 0
    declared = 0
    integrated = 0
    asset_ids: dict[str, dict[str, Any]] = {}
    step_ids: set[str] = set()
    producers: set[str] = set()
    graph: dict[str, set[str]] = {}
    domains: set[str] = set()
    try:
        digest = canonical_digest(bundle)
    except (TypeError, ValueError, OverflowError):
        digest = None
    if digest is None:
        _problem(errors, "INVALID_CANONICAL_DIGEST", "bundle")
    if not isinstance(bundle, dict) or set(bundle) != {
        "kind", "schema_version", "scope", "assets", "steps", "claims",
    } or bundle.get("kind") != KIND or bundle.get("schema_version") != VERSION or bundle.get("scope") != "LIFE_SCIENCES":
        _problem(errors, "INVALID_BUNDLE_CONTRACT", "bundle")
    else:
        assets, steps, claims = bundle["assets"], bundle["steps"], bundle["claims"]
        if not (_array(assets) and _array(steps) and _array(claims)):
            _problem(errors, "UNBOUNDED_COLLECTION", "bundle")
        else:
            if not assets:
                _problem(errors, "EMPTY_ASSET_SET", "bundle")
            for asset in assets:
                if (not isinstance(asset, dict)
                        or not {"id", "domain", "kind", "sha256", "source"}.issubset(asset)
                        or not set(asset) <= {"id", "domain", "kind", "sha256", "source", "path"}
                        or not _id(asset.get("id"))):
                    _problem(errors, "INVALID_ASSET", "asset")
                    continue
                aid = asset["id"]
                if aid in asset_ids:
                    _problem(errors, "DUPLICATE_ASSET", aid)
                    continue
                asset_ids[aid] = asset
                domain = asset["domain"]
                if not isinstance(domain, str) or domain not in DOMAINS:
                    _problem(errors, "UNREVIEWED_DOMAIN", aid)
                else:
                    domains.add(domain)
                if not _text(asset["kind"], 80) or not isinstance(asset["sha256"], str) or not SHA256.fullmatch(asset["sha256"]):
                    _problem(errors, "INVALID_ASSET_IDENTITY", aid)
                source = asset["source"]
                if (not isinstance(source, dict) or set(source) != {"id", "version"}
                        or not _text(source.get("id")) or not _text(source.get("version"), 100)):
                    _problem(errors, "INVALID_SOURCE_DECLARATION", aid)
                if "path" in asset:
                    if isinstance(asset["sha256"], str) and SHA256.fullmatch(asset["sha256"]):
                        if _check_local(root, asset["path"], asset["sha256"], errors, aid):
                            checked += 1
                    else:
                        _problem(errors, "UNVERIFIABLE_LOCAL_DIGEST", aid)
                else:
                    declared += 1
                graph[aid] = set()

            for step in steps:
                if not isinstance(step, dict) or set(step) != {
                    "id", "method", "inputs", "outputs", "supported_domains", "outcome",
                } or not _id(step.get("id")):
                    _problem(errors, "INVALID_STEP", "step")
                    continue
                sid = step["id"]
                if sid in step_ids:
                    _problem(errors, "DUPLICATE_STEP", sid)
                    continue
                step_ids.add(sid)
                method = step["method"]
                if (not isinstance(method, dict) or set(method) != {"id", "version", "sha256"}
                        or not _id(method.get("id")) or not _text(method.get("version"), 80)
                        or not isinstance(method.get("sha256"), str) or not SHA256.fullmatch(method["sha256"])):
                    _problem(errors, "INVALID_METHOD_IDENTITY", sid)
                inputs, outputs, supported = step["inputs"], step["outputs"], step["supported_domains"]
                if (not _array(inputs) or not _array(outputs) or not _array(supported)
                        or not inputs or not outputs
                        or not all(_id(x) for x in inputs + outputs)
                        or not all(isinstance(x, str) and x in DOMAINS for x in supported)):
                    _problem(errors, "INVALID_STEP_PORTS", sid)
                    continue
                if len(set(inputs)) != len(inputs) or len(set(outputs)) != len(outputs) or set(inputs) & set(outputs):
                    _problem(errors, "INVALID_STEP_LINKAGE", sid)
                if not isinstance(step["outcome"], str) or step["outcome"] not in OUTCOMES:
                    _problem(errors, "INVALID_EXECUTION_OUTCOME", sid)
                if any(x not in asset_ids for x in inputs + outputs):
                    _problem(errors, "UNKNOWN_ASSET_REFERENCE", sid)
                    continue
                related = {str(asset_ids[x]["domain"]) for x in inputs + outputs}
                if not related.issubset(set(supported)):
                    _problem(errors, "METHOD_DOMAIN_MISMATCH", sid)
                if len({str(asset_ids[x]["domain"]) for x in inputs}) > 1:
                    integrated += 1
                for output in outputs:
                    if output in producers:
                        _problem(errors, "MULTIPLE_PRODUCERS", output)
                    producers.add(output)
                for i in inputs:
                    graph[i].update(outputs)
                if step["outcome"] != "SUCCEEDED":
                    _problem(warnings, "NON_SUCCESSFUL_EXECUTION_RECORDED", sid)

            # All assets must participate in the lineage except single-asset
            # evidence bundles without computation steps.
            for asset in asset_ids:
                used = asset in producers or any(
                    isinstance(s, dict) and _array(s.get("inputs"))
                    and asset in s["inputs"] for s in steps
                )
                if steps and not used:
                    _problem(warnings, "UNLINKED_ASSET", asset)
            visited: set[str] = set()
            active: set[str] = set()

            def walk(node: str) -> None:
                if node in active:
                    _problem(errors, "LINEAGE_CYCLE", node)
                    return
                if node in visited:
                    return
                active.add(node)
                for child in sorted(graph[node]):
                    walk(child)
                active.remove(node)
                visited.add(node)

            for node in sorted(graph):
                walk(node)

            claim_ids: set[str] = set()
            for claim in claims:
                if (not isinstance(claim, dict) or set(claim) != {
                    "id", "statement", "evidence", "authority",
                } or not _id(claim.get("id")) or not _text(claim.get("statement"), 1000)
                        or not _array(claim.get("evidence")) or not claim["evidence"]):
                    _problem(errors, "INVALID_CLAIM_RECORD", "claim")
                    continue
                cid = claim["id"]
                if cid in claim_ids:
                    _problem(errors, "DUPLICATE_CLAIM", cid)
                claim_ids.add(cid)
                if claim["authority"] != "PROPOSAL_ONLY":
                    _problem(errors, "SCIENTIFIC_AUTHORITY_ESCALATION", cid)
                if (not all(_id(x) for x in claim["evidence"])
                        or len(set(claim["evidence"])) != len(claim["evidence"]) or any(
                    x not in asset_ids for x in claim["evidence"]
                )):
                    _problem(errors, "UNKNOWN_OR_DUPLICATE_CLAIM_EVIDENCE", cid)
                _problem(warnings, "SCIENTIFIC_CLAIM_NOT_ADJUDICATED", cid)

    status = "FAIL" if errors else "INDETERMINATE" if declared or warnings else "PASS"
    return {
        "kind": "LS_RSE_ENGINEERING_ASSESSMENT",
        "schema_version": VERSION,
        "bundle_sha256": digest,
        "status": status,
        "errors": sorted(errors, key=lambda x: (x["code"], x["subject"])),
        "warnings": sorted(warnings, key=lambda x: (x["code"], x["subject"])),
        "metrics": {
            "assets": len(asset_ids),
            "local_bytes_verified": checked,
            "declared_only_assets": declared,
            "domains": sorted(domains),
            "declared_cross_domain_steps": integrated,
        },
        "not_verified": [
            "Scientific truth or biological identity beyond checked local bytes",
            "Execution claims and method digests are declared, not independently attested",
            "Scientific correctness or applicability of declared methods",
            "Authenticity of external source claims and reference records",
            "Independent human review, institutional certification or production acceptance",
        ],
    }
