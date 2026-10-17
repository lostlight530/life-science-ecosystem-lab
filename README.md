# Life Science Ecosystem Lab

**Three independently callable life-science research software assets: Knowledge Workflow, Evidence Tool and Bio Tool**

This open-source repository contains **three independently callable research-software assets**. Both can be used separately, tested separately, and composed through public file/CLI interfaces. GitHub Actions operates the native knowledge workflow; it is not a third asset. External Agents and human research are independent collaborators, **not runtime requirements**.

| Asset | Execution | Primary output |
| --- | --- | --- |
| [Knowledge Workflow](.github/README.md) | `ls-knowledge` / native GitHub Actions / CWL | Accepted source-linked knowledge, graph and receipts |
| [Evidence Tool](evidence/README.md) | `ls-evidence` independently | Software and evidence checks, JSON/Markdown/SARIF |
| [Bio Tool](bio_tool/README.md) | `ls-bio` independently / CWL wrappers | Real protein FASTA/PDB file analysis and bounded JSON results |

## First use: three independent paths

**1. Try the Tool without network access or executing research code**

```sh
python -m pip install -e .
ls-evidence inspect --root . --output build/inspection.json --markdown build/inspection.md --sarif build/inspection.sarif
```

**2. Reproduce the computational knowledge sub-workflow using synthetic fixtures**

```sh
python -m pip install cwltool
mkdir -p build/replay
cwltool --no-container --outdir build/replay .github/knowledge/main.cwl .github/knowledge/test/workflow-job.yml
ls-knowledge graph project --knowledge build/replay/knowledge.json --output-dir build/graph
ls-knowledge graph verify --dir build/graph --knowledge build/replay/knowledge.json
ls-knowledge graph search --dir build/graph --query workflow --limit 5 --hops 1
```

**3. Analyze real protein FASTA/PDB files independently**
```sh
ls-bio protein-fasta --input .github/bio/test/example.fasta --output build/fasta-quality.json
ls-bio protein-pdb --input .github/bio/test/example.pdb --output build/pdb-quality.json
```
`ls-bio` parses biological files; it does not claim protein structure prediction or clinical utility. See [Bio Tool](bio_tool/README.md).

Run from the cloned **repository root** with Python 3.11+. The CWL replay is offline *after installing the required packages* and uses **synthetic**, not live, GitHub observations. For detailed instructions, networked collection, exit statuses and troubleshooting, see [Getting Started](docs/GETTING_STARTED.md).

## How the repository is organized

```text
.github/                  Native knowledge lifecycle (Actions, CWL, runtime, guards)
evidence/                 Independent installed Evidence Tool, profiles and schemas
bio_tool/                 Independent protein FASTA/PDB analysis package
data/                     Git-tracked accepted inputs, graph, memory and receipts
metadata/                 Public Bioschemas descriptors and standards-status data
docs/                     User guides, scope, interfaces, architecture and provenance
tests/                    Executable regression and integration contracts
ro-crate-metadata.json    Workflow and testing research-object metadata
codemeta.json             Shared software identity, three named asset components
CITATION.cff              Citation for the repository's software version
```

[Optional external Agent handoff](docs/AGENT_COLLABORATION.md) · [Documentation index](docs/README.md) · [Public interfaces](docs/PUBLIC_INTERFACES.md) · [Understanding verification](docs/VERIFYING_RESULTS.md) · [Architecture](docs/ARCHITECTURE.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md)

## Current capabilities and limits

- The Knowledge Workflow collects only **approved public GitHub sources**, verifies Git object/content identity, constructs a source-cited knowledge map and rebuildable JSONL graph, and supports bounded SQLite FTS5/BM25 search. Scheduled persistence is gated by evidence completeness, state checks, `main` world-line, and a `data/`-only write boundary.
- The Evidence Tool provides source collection, aggregation, validation, advisory discovery, local Markdown-link auditing, and a standalone **nonexecuting** external-repository inspection function. Its reports distinguish findings from unknown or unverified outcomes.
- The third Bio Tool performs actual protein FASTA/PDB processing with bounded input sizes, deterministic composition/residue summaries and no model inference.
- Graph `SOURCE_MATCH` edges are **document-topic matches**, not proven scientific, biological or causal relations. Metadata validation is not scientific validity or external certification.
- Accepted receipts distinguish `snapshot_id` from `execution_id` and classify selected document-content changes separately from provenance-only changes. Final production validation rejects a placeholder-only `data/` tree.
- The first verified live production snapshot was accepted on 2026-10-17 in [Run 38995485443](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/38995485443) and [Commit b2d1d31](https://github.com/lostlight530/life-science-ecosystem-lab/commit/b2d1d31f715275823f7ea0440d0a14a552f35e2a). This historic acceptance does **not** establish recurring schedule success or any external scientific certification.

Standards-facing descriptors exist for CWL, RO-Crate, Bioschemas, CFF and CodeMeta. **The LifeMonitor GitHub App installation and first Bot PR are externally observed; LifeMonitor test enrollment, WorkflowHub registration, and bio.tools acceptance require independent external verification**. See [standards status](docs/STANDARDS.md).

## Reusable research methodology

The stable research lifecycle—define, pin, qualify, execute, evaluate, audit, review and replay—applies across replaceable scientific examples, not just the existing protein-data demonstration. See [Research Methodology](docs/RESEARCH_METHODOLOGY.md) and `ls-evidence validate-research-case` for a domain-neutral, proposal-only evidence envelope. File-format parsers and individual scientific algorithms are examples of the method, not its scientific or ecosystem limits.

## Ongoing verification

The read-only [continuity check](.github/workflows/life-science-continuity.yml) validates the accepted Git-backed state independently of the production scheduler. The Evidence Tool also offers bounded offline `audit-knowledge` for reproducibility and cross-version selection changes and `audit-ecosystem` for local standards readiness. A reproducible CWL-main archive including all three source assets can be created using `.github/scripts/build_portable_workflow_crate.py`. None of these actions implies external platform registration or scientific verification.

## Development, identity and responsible use

```sh
python -m unittest discover -s tests -v
ls-evidence audit-docs --root . --files evidence/profiles/docs.json --output build/docs-audit.json
python .github/scripts/check_metadata.py
python .github/scripts/check_publication_boundary.py
```

The software is MIT licensed. Cite the version recorded in [CITATION.cff](CITATION.cff). Never submit credentials, private research material or health/person-level data to public issues, Actions artifacts or PRs. The [public maintenance policy](docs/MAINTENANCE.md) explains the security and publication boundary.
