"""Create a deterministic, minimal portable CWL Workflow Testing RO-Crate.

This is a package construction step, not a third-party profile certification or
a registration action. Live accepted data and original upstream content are excluded.
"""
from __future__ import annotations

import copy
import json
import runpy
import sys
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NATIVE_CRATE_FILES = runpy.run_path(str(Path(__file__).with_name('build_rocrate.py')))['FILES']
CWL_MAIN = ".github/knowledge/main.cwl"
REQUIRED = (
    "pyproject.toml", "LICENSE", "CITATION.cff",
    ".github/knowledge/main.cwl",
    ".github/knowledge/tools/aggregate.cwl",
    ".github/knowledge/tools/validate.cwl",
    ".github/knowledge/tools/knowledge.cwl",
    ".github/knowledge/tools/verify-knowledge.cwl",
    ".github/knowledge/test/workflow-job.yml",
    "evidence/examples/evidence-records.json",
    "evidence/profiles/topics.json",
    "evidence/profiles/sources.json",
    "bio_tool/README.md",
    ".github/bio/protein-fasta.cwl",
    ".github/bio/protein-pdb.cwl",
    ".github/bio/test/example.fasta",
    ".github/bio/test/example.pdb",
    ".github/bio/test/fasta-job.yml",
    ".github/bio/test/pdb-job.yml",
    "metadata/biotools-protein-audit.draft.json",
    "metadata/bioschemas-bio-tool.jsonld",
)
PORTABLE_README = """# Life Science Knowledge Workflow

This portable CWL v1.2 workflow processes supplied evidence-record fixtures.
It does not make network requests, register with external services, or produce
biological conclusions. The parent GitHub Actions lifecycle separately controls
live collection and accepted production state.

Requirements: Python 3.11+, pip and the CWL reference runner

    python -m pip install --no-deps -e .
    python -m pip install cwltool
    cwltool --no-container --outdir build/replay .github/knowledge/main.cwl .github/knowledge/test/workflow-job.yml

A separate ls-bio command supports protein FASTA/PDB file-level analysis. The included records are synthetic examples. Use externally validated records
only with appropriate source licenses and permission. See the public repository
for actual native ingestion, acceptance and provenance controls.
"""


def build(path: Path) -> None:
    metadata = json.loads((ROOT / "ro-crate-metadata.json").read_text(encoding="utf-8"))
    version = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    payload = copy.deepcopy(metadata)
    graph = payload["@graph"]
    nodes = {node["@id"]: node for node in graph if isinstance(node, dict) and "@id" in node}
    crate = nodes["./"]
    main = nodes[CWL_MAIN]
    if not {"File", "SoftwareSourceCode", "ComputationalWorkflow"}.issubset(set(main["@type"])):
        raise ValueError("CWL main workflow missing required computational types")
    if main.get("programmingLanguage", {}).get("@id") != "https://w3id.org/workflowhub/workflow-ro-crate#cwl":
        raise ValueError("CWL language identity missing")
    crate["mainEntity"] = {"@id": CWL_MAIN}
    crate["name"] = "Life Science Knowledge Workflow"
    crate["version"] = version
    crate["author"] = {"@id": "#creator"}
    crate["description"] = (
        "Deterministic and portable CWL v1.2 workflow that transforms supplied, source-linked GitHub "
        "evidence records into a topic-linked knowledge map, validates provenance and schema constraints, "
        "and reports explicit coverage gaps; no live collection, repository writes, biological inference "
        "or clinical analysis"
    )
    main["version"] = version
    suite = nodes.get("#suite")
    if isinstance(suite, dict):
        suite["mainEntity"] = {"@id": CWL_MAIN}
    files = set(REQUIRED)
    # Keep all local file entities already referenced by existing public RO-Crate metadata.
    files.update(name for name in NATIVE_CRATE_FILES if name not in ("README.md", "ro-crate-metadata.json"))
    files.update(p.relative_to(ROOT).as_posix() for p in (ROOT / ".github/runtime").rglob("*.py"))
    files.update(p.relative_to(ROOT).as_posix() for p in (ROOT / "evidence").glob("*.py"))
    files.update(p.relative_to(ROOT).as_posix() for p in (ROOT / "bio_tool").glob("*.py"))
    if not files or any(not (ROOT / name).is_file() or name.startswith("data/") for name in files):
        raise ValueError("missing or invalid source file in portable crate")
    crate["hasPart"] = [{"@id": name} for name in sorted(files)] + [{"@id": "README.md"}]
    # Any referenced node outside the root hasPart is informational metadata,
    # not an assertion that the portable bundle contains unrelated native files.
    body = (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")
    entries = {"ro-crate-metadata.json": body, "README.md": PORTABLE_README.encode("utf-8")}
    for name in files:
        entries[name] = (ROOT / name).read_bytes()
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, entries[name])


if __name__ == "__main__":
    build(Path(sys.argv[1] if len(sys.argv) > 1 else "build/life-science-portable.cwl.crate.zip"))
