# Life Science Lab · Canonical Architecture

## Two peer assets, one native execution environment

1. **Knowledge Workflow** — `.github/` is the canonical lifecycle and knowledge runtime. The GitHub Actions workflow controls scheduling, source ingestion, knowledge transformation, state recovery, conditional persistence and receipts; a CWL computational sub-workflow offers portable replay
2. **Evidence Tool** — `evidence/` is an independent Python package and CLI for source identification, immutable provenance, diff/replay, scientific-software documentation checks and independent verdicts

A workflow can call the tool, and the tool can validate workflow artifacts, but **neither asset's identity is defined by that call graph**

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

LifeMonitor's existing global all-branch/all-tag/issue-check preferences remain untouched — no `lifemonitor.yaml` override is committed

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
