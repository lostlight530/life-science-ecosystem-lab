"""Read-only interoperability readiness checks; never attest external acceptance."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .aggregation import canonical_bytes

MAX_METADATA_BYTES = 2_000_000


def _read_json(root: Path, rel: str) -> Any:
    file = root / rel
    target = file.resolve()
    if not target.is_relative_to(root) or not file.is_file() or file.is_symlink():
        return None
    if file.stat().st_size > MAX_METADATA_BYTES:
        raise ValueError(f"oversized metadata: {rel}")
    return json.loads(file.read_text(encoding="utf-8"))


def audit_ecosystem(directory: Path) -> dict[str, Any]:
    root = directory.resolve()
    if not root.is_dir():
        raise ValueError("repository root must be a directory")
    crate = _read_json(root, "ro-crate-metadata.json")
    tool = _read_json(root, "metadata/bioschemas-tool.jsonld")
    software = _read_json(root, "codemeta.json")
    findings: list[dict[str, str]] = []
    graph = crate.get("@graph") if isinstance(crate, dict) else None
    if not isinstance(graph, list):
        graph = []
    nodes = {n.get("@id"): n for n in graph if isinstance(n, dict) and isinstance(n.get("@id"), str)}
    root_entity = nodes.get("./", {})
    main_ref = root_entity.get("mainEntity") if isinstance(root_entity, dict) else None
    main_id = main_ref.get("@id") if isinstance(main_ref, dict) else None
    main = nodes.get(main_id, {})
    main_types = main.get("@type", []) if isinstance(main, dict) else []
    if isinstance(main_types, str):
        main_types = [main_types]
    language = main.get("programmingLanguage") if isinstance(main, dict) else None
    language_id = language.get("@id") if isinstance(language, dict) else None
    portable = (isinstance(main_id, str) and main_id.endswith(".cwl")
                and "ComputationalWorkflow" in main_types
                and language_id == "https://w3id.org/workflowhub/workflow-ro-crate#cwl"
                and (root / main_id).is_file())
    if not portable:
        findings.append({"platform": "WorkflowHub", "code": "MAIN_WORKFLOW_PORTABILITY_NOT_VERIFIED",
                         "detail": "The declared crate main workflow is not verified as the executable CWL entrypoint; package and validate a standalone CWL Workflow RO-Crate before registration"})
    if not (root / ".github/knowledge/main.cwl").is_file():
        findings.append({"platform": "WorkflowHub", "code": "PORTABLE_CWL_MISSING",
                         "detail": "No local portable CWL descriptor found"})
    has_license = bool((root / "LICENSE").is_file() and root_entity.get("license"))
    if not has_license:
        findings.append({"platform": "WorkflowHub", "code": "LICENSE_NOT_VERIFIED",
                         "detail": "Public license and RO-Crate license metadata required"})
    has_ci = (root / ".github/workflows/validate.yml").is_file()
    has_tests = (root / ".github/knowledge/test/workflow-job.yml").is_file()
    if not has_ci or not has_tests:
        findings.append({"platform": "LifeMonitor", "code": "WORKFLOW_TEST_EVIDENCE_INCOMPLETE",
                         "detail": "Workflow test definition and CI were not both found"})
    if not isinstance(tool, dict) or not isinstance(tool.get("name"), str):
        findings.append({"platform": "bio.tools", "code": "TOOL_METADATA_MISSING",
                         "detail": "Local tool identity not available"})
    if not isinstance(software, dict):
        findings.append({"platform": "bio.tools", "code": "SOFTWARE_METADATA_MISSING",
                         "detail": "CodeMeta JSON not available"})
    readiness = {
        "WorkflowHub": "LOCAL_PACKAGING_REVIEW_REQUIRED" if not portable or not has_license else "STRUCTURAL_PREFLIGHT_ONLY",
        "LifeMonitor": "TEST_INFRASTRUCTURE_PRESENT_ENROLLMENT_UNVERIFIED" if has_ci and has_tests else "TEST_SETUP_INCOMPLETE",
        "bio.tools": "DOMAIN_SCOPE_AND_EDAM_CURATION_REQUIRED",
    }
    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "kind": "RESEARCH_SOFTWARE_EXTERNAL_INTEROPERABILITY_PREFLIGHT",
        "status": "REVIEW_REQUIRED" if findings else "STRUCTURAL_PREFLIGHT_ONLY",
        "readiness": readiness,
        "findings": findings,
        "reviewed_identity": {
            "crate_main_entity": main_id,
            "portable_cwl_present": (root / ".github/knowledge/main.cwl").is_file(),
            "independent_tool_metadata_present": isinstance(tool, dict),
            "software_metadata_present": isinstance(software, dict),
        },
        "external_states": {
            "WorkflowHub": "NOT_VERIFIED",
            "LifeMonitor": "NOT_VERIFIED",
            "bio.tools": "NOT_VERIFIED",
            "third_party_usage": "NOT_MEASURED",
        },
        "not_verified": [
            "external account access or permissions",
            "external platform registration or approval",
            "LifeMonitor GitHub App installation or periodic monitoring",
            "bio.tools eligibility or EDAM operations",
            "any scientific or clinical result",
        ],
    }
    report["report_sha256"] = hashlib.sha256(canonical_bytes(report)).hexdigest()
    return report
