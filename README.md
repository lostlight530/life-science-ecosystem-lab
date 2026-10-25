# Life Science Ecosystem Lab

**Three established independent research-software assets plus one experimental independent cross-domain software engineering Framework**

This open-source repository contains **three established independently callable research-software assets**, plus a separately packaged, experimental **Life Sciences Cross-Domain Software Engineering Framework**. Each can be tested independently and combined through explicit public file/CLI contracts. GitHub Actions operates the Knowledge Workflow; it is the native execution environment for that asset, not a fourth asset. External Agents and human research are independent collaborators, **not runtime requirements**.

| Asset | Execution | Primary output |
| --- | --- | --- |
| [Knowledge Workflow](.github/README.md) | `ls-knowledge` / native GitHub Actions / CWL | Accepted source-linked knowledge, graph and receipts |
| [Evidence Tool](evidence/README.md) | `ls-evidence` independently | Software and evidence checks, JSON/Markdown/SARIF |
| [Bio Tool](bio_tool/README.md) | `ls-bio` independently / CWL wrappers | Real protein FASTA/PDB file analysis and bounded JSON results |
| [Framework — experimental](framework/README.md) | Separate `pip install -e ./framework` / `ls-framework` | Life-science cross-domain software-contract and lineage assessment, not biological interpretation |

## Heterogeneous Agent cohort research

[**谁说 Agent 集群不可以科研？ — An auditable multi-Agent research case**](docs/AGENT_CLUSTER_RESEARCH_CASE.md) documents three externally submitted contributions (local IDE, cloud observer, desktop Codex), their GitHub reviews, accepted corrections and evidentiary limits. [Decision ledger](docs/AGENT_REVIEW_DECISIONS.md) preserves the difference between a claim, its correction, code acceptance and independent scientific proof. Multiple Agent contributions are inspectable, but Agent runtime identity and independent scientific reproduction are not inferred from a shared Git account.

## Daily institutional and project self-checks

[**Daily fixed self-check SOP**](docs/DAILY_SELF_CHECK.md) runs two fully isolated, read-only checks: [institutional official public references](checks/institutional/README.md) and [our custom repository contracts](checks/project/README.md). Their JSON reports, document inventories and 30-day GitHub Artifacts are separate. External endpoint HTTP observations are not official uptime verification, external registry accession or LS Login authorization.

Research scope selection belongs to the separate Knowledge Workflow. Its closed profile registry currently offers production `native` and read-only `protein_structure` executions. The protein field workflow is a dedicated rendering of that isolated profile; the daily self-check does not select research subjects or approve evidence sources.

## First use: four independent paths

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

**4. Assess an experimental cross-domain software bundle independently**

```sh
python -m pip install --no-deps -e ./framework
ls-framework assess --bundle framework/fixtures/software-cross-domain.json --root framework/fixtures --output build/framework/assessment.json
```

`ls-framework` validates bounded software contracts, local byte identity and declared lineage. It does not execute scientific methods or establish biological truth. See [Framework](framework/README.md).

Run from the cloned **repository root** with Python 3.11+. The CWL replay is offline *after installing the required packages* and uses **synthetic**, not live, GitHub observations. For detailed instructions, networked collection, exit statuses and troubleshooting, see [Getting Started](docs/GETTING_STARTED.md).

## How the repository is organized

```text
.github/                  Native knowledge lifecycle (Actions, CWL, runtime, guards)
evidence/                 Independent installed Evidence Tool, profiles and schemas
bio_tool/                 Independent protein FASTA/PDB analysis package
framework/                Independent experimental cross-domain software engineering package
data/                     Git-tracked accepted inputs, graph, memory and receipts
metadata/                 Public Bioschemas descriptors and standards-status data
docs/                     User guides, scope, interfaces, architecture and provenance
tests/                    Executable regression and integration contracts
ro-crate-metadata.json    Workflow and testing research-object metadata
codemeta.json             Current repository component inventory, including the experimental Framework boundary
CITATION.cff              Citation and Zenodo DOI for the released v0.4.0 three-asset baseline
.gitattributes            Cross-platform LF and binary rules for reproducible byte verification
```

[Optional external Agent handoff](docs/AGENT_COLLABORATION.md) · [Documentation index](docs/README.md) · [Public interfaces](docs/PUBLIC_INTERFACES.md) · [Understanding verification](docs/VERIFYING_RESULTS.md) · [Architecture](docs/ARCHITECTURE.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md)

## Independent Framework pilot

For evidence-safe CLI output paths, strict `INDETERMINATE` handling and limits of software-versus-science assurance, consult the [independent Framework assurance matrix](framework/docs/ASSURANCE.md).

The experimental [Framework](framework/README.md) is a **software-engineering** peer focused on versioned, bounded contracts across different life-science data systems. The frozen genomics/microscopy example uses synthetic JSON fixtures and tests local byte identity, declared method applicability, lineage and failure boundaries — **it performs no omics integration or scientific inference**. See [independent architecture decision](docs/ADR-INDEPENDENT-LS-FRAMEWORK.md)

It also provides an [independent synthetic contract challenge](framework/docs/CONTRACT_CHALLENGE.md), which exercises invalid inputs and correct abstention without introducing a scientific inference engine or modifying existing Workflow/Tool contracts

Its package version is `0.1.0` and it remains unreleased and unregistered as a separate external asset. The repository's `v0.4.0` Zenodo software DOI and WorkflowHub record describe the earlier released three-asset baseline and portable Knowledge Workflow, not this experimental Framework.

## Current capabilities and limits

- The Knowledge Workflow collects only **approved public GitHub sources**, verifies Git object/content identity, constructs a source-cited knowledge map and rebuildable JSONL graph, and supports bounded SQLite FTS5/BM25 search. Manual runs select only reviewed profiles from `evidence/profiles/workflow-profiles.json`; scheduled production always selects `native`. Persistence is gated by native authority, evidence completeness, state checks, `main` world-line, and a `data/`-only write boundary.
- The Evidence Tool provides source collection, aggregation, validation, advisory discovery, local Markdown-link auditing, and a standalone **nonexecuting** external-repository inspection function. Its reports distinguish findings from unknown or unverified outcomes.
- The third Bio Tool performs actual protein FASTA/PDB processing with bounded input sizes, deterministic composition/residue summaries and no model inference.
- The experimental Framework verifies bounded cross-domain software bundles, rejects missing multi-asset lineage, and runs on Linux and Windows. Its verdict is an engineering-contract result only.
- Graph `SOURCE_MATCH` edges are **document-topic matches**, not proven scientific, biological or causal relations. Metadata validation is not scientific validity or external certification.
- Accepted receipts distinguish `snapshot_id` from `execution_id` and classify selected document-content changes separately from provenance-only changes. Final production validation rejects a placeholder-only `data/` tree.
- The first verified live production snapshot was accepted on 2026-10-17 in [Run 38995485443](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/38995485443) and [Commit b2d1d31](https://github.com/lostlight530/life-science-ecosystem-lab/commit/b2d1d31f715275823f7ea0440d0a14a552f35e2a). This historic acceptance does **not** establish recurring schedule success or any external scientific certification.

Standards-facing descriptors exist for CWL, RO-Crate, Bioschemas, CFF and CodeMeta. The released baseline has a [Zenodo software DOI](https://doi.org/10.5281/zenodo.23447089), while the portable workflow has an independent [WorkflowHub version DOI](https://doi.org/10.48546/workflowhub.workflow.2347.2). Current external records and their evidence boundaries are maintained only in [standards status](docs/STANDARDS.md); local metadata alone is not proof of registration or scientific validity.

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

The software is MIT licensed. Cite the released baseline recorded in [CITATION.cff](CITATION.cff). The experimental Framework is not part of that frozen `v0.4.0` release. Never submit credentials, private research material or health/person-level data to public issues, Actions artifacts or PRs. The [public maintenance policy](docs/MAINTENANCE.md) explains the security and publication boundary.
