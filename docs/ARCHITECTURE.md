# Life Science Lab · Canonical Architecture

## Three peer assets, one native execution environment

1. **Knowledge Workflow** — `.github/` is the canonical lifecycle and knowledge runtime. The GitHub Actions workflow controls scheduling, source ingestion, knowledge transformation, state recovery, conditional persistence and receipts; a CWL computational sub-workflow offers portable replay
2. **Evidence Tool** — `evidence/` is an independent Python package and CLI for source identification, immutable provenance, diff/replay, scientific-software documentation checks and independent verdicts
3. **Bio Tool** — `bio_tool/` is an independent Python package and CLI for bounded protein FASTA/PDB quality analysis, with portable CWL command wrappers

The three assets can be composed through explicit files and CLI calls, but **no asset's identity is defined by that call graph**

## Native lifecycle

`Approved source profiles → Collect → Validate → Aggregate → Project Knowledge → Verify Knowledge → Compare to Active → Archive Superseded → Record Memory → Check World-line → Guarded Apply → Receipt`

The canonical GitHub Actions workflow is **not a mere wrapper around CWL**. The CWL descriptor records a deterministic sub-workflow for portability, not the scheduler, branch authority or state machine

GitHub-native `data/` holds current evidence, immutable archive, source-cited knowledge, bounded memories, state and receipts. CI fixtures and manual dry-runs do not claim the durable live corpus was updated

## Trust and write boundaries

- Source discovery is read-only and advisory; only source profiles approve GitHub repositories
- Evidence collection requires actual commit, tree, blob and canonical content digest
- The tool cannot change the source registry or write active state
- Internally maintained decision records and historical operating plans are not required for public use and are not part of the release
- The scheduled workflow is eligible to persist only a verified meaningful delta after comparing remote `main`, validating `data/`-only writes and the knowledge output
- Rejected source, incomplete provenance, concurrent main changes or failed validation stop persistence; failed runs are not successful research outcomes

## Standards, scope and external states

The workflow descriptor, RO-Crate, Workflow Testing RO-Crate, Bioschemas, CFF and MIT licensing describe verifiable functionality. They do not certify clinical validity, automatic WorkflowHub registration, LifeMonitor enrollment or semantic scientific understanding

The repository's minimal `lifemonitor.yaml` enables issue checks and intentionally leaves branch and tag tracking to the existing account-wide global settings. It does not itself prove workflow-test enrollment or recurring monitoring. The Workflow and Tools are registration-ready research software assets, but repository metadata and CI success do not claim that an external registry has accepted them

## Validation, schedules and external observers

Pull-request validation is an actor-neutral repository authority plane. Four independent read-only jobs validate repository contracts, Knowledge Workflow replay, Evidence Tool behavior and the portable package. A final verdict aggregates their results without preventing any domain from starting. This makes failures complete and inspectable while preserving one strict merge decision

Scheduled checks, external Bots and institutional services are separate execution planes. A Bot PR runs the same repository contracts as a human PR without an identity bypass. LifeMonitor, WorkflowHub, LS Login and other public services may observe or register released assets, but their network, authentication or registration state is never a prerequisite for local required validation. The only intentional job dependency with write authority remains native validation before guarded `data/` apply

## Implementation precedents

- [WorkflowHub Workflow RO-Crate 1.1](https://about.workflowhub.eu/Workflow-RO-Crate/1.1/) — exchange metadata and primary workflow identity
- [Workflow Testing RO-Crate 0.2](https://w3id.org/ro/wftest/0.2) — documented test suites and instances
- [LifeMonitor GitHub App guide](https://lifemonitor.eu/lm_wft_best_practices_github_app) — branch/tag monitoring and issue checks
- [Bioschemas ComputationalWorkflow 1.0](https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE) — scientific workflow descriptors and formal inputs/outputs
- [nf-core pipeline guidelines](https://nf-co.re/docs/guidelines/pipelines/overview) — testable, versioned, documented scientific workflows
- [Galaxy IWC](https://github.com/galaxyproject/iwc) — executable workflows, workflow tests and release/registry metadata

These are design precedents, not endorsements or proof of external integration

## Rebuildable graph and peer Tool contracts

A validated knowledge map is projected into JSONL topic/source entities and evidenced `SOURCE_MATCH` relations, plus deterministic manifest and accepted-run event records. SQLite FTS5 BM25 and bounded adjacency traversal provide inspectable retrieval. Neither graph rank nor lexical proximity creates a new scientific claim. A separate static `ls-evidence inspect` function accepts third-party local research repositories and emits JSON/Markdown/SARIF findings. External Agents remain outside both native runtimes and may independently read these outputs. See [public interfaces](PUBLIC_INTERFACES.md) and [standards](STANDARDS.md).

## Third independent bioinformatics data-processing plane

The `bio_tool/` software asset exposes `ls-bio` and CWL CommandLineTool wrappers for protein FASTA/PDB files. It has no dependency on accepted `data/`, the Evidence Tool, external Agents or native GitHub scheduling. Outputs are bounded local JSON measurements with input SHA-256 and explicit biological non-claims. The native Workflow and Evidence Tool retain their existing responsibilities and write boundaries. This addition does not change any accepted `data/` snapshot or infer a new biological knowledge edge.
