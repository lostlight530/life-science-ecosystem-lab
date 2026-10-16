# Life Science Ecosystem Lab

**GitHub-native, knowledge-first scientific workflow engineering · Independently verifiable evidence tools**

This repository carries two peer research-software assets, each with its own source, contract, documentation and tests. Their GitHub integration implements the native knowledge ingestion, processing, storage, verification and iteration practices established in our earlier research repositories, now specialized for the **Life Science** domain

| Asset | Canonical directory | Responsibility |
| --- | --- | --- |
| **Life Science Knowledge Workflow** | [`.github/`](.github/README.md) | Scheduled GitHub Actions runtime, approved document ingestion, source-cited knowledge projections, state/memory, versioned history, guarded iterative application |
| **Life Science Evidence Tool** | [`evidence/`](evidence/README.md) | Independently callable provenance collection, evidence aggregation and validation, documentation maintenance, advisory GitHub topic discovery |

GitHub Actions is the **native runtime for our workflow**, not a third independent research asset. Evidence is a peer tool with an independent CLI/CI lifecycle, not an incidental post-processing script

## Workflow lifecycle

The canonical executable is [`.github/workflows/life-science-knowledge.yml`](.github/workflows/life-science-knowledge.yml), with a portable [CWL v1.2 knowledge sub-workflow](.github/knowledge/main.cwl)

```sh
python -m pip install -e .
python -m life_science_ecosystem_lab validate-source-registry evidence/profiles/sources.json
python -m life_science_ecosystem_lab validate-topic-registry evidence/profiles/topics.json
ls-evidence audit-docs --root . --files evidence/profiles/docs.json --output build/docs-audit.json
python -m unittest discover -s tests -v
```

For fully offline CWL reproduction (uses synthetic test data only):

```sh
python -m pip install cwltool
cwltool --no-container .github/knowledge/main.cwl .github/knowledge/test/workflow-job.yml
```

For live approved GitHub-source observation and standalone tool usage, see [Evidence CLI](evidence/README.md)

## Evidence, data and standards

- **Knowledge:** source-cited excerpts, explicit coverage states and unresolved gaps, then stateful bounded revisions — deterministic classification, **not** autonomous biological interpretation or scientific inference
- **Evidence:** source repo, immutable Git object identity, content SHA, source registry/trust rules and independent reproducibility checks
- **Data:** `data/inputs/current`, `data/inputs/archive`, `data/knowledge`, `data/memories`, `data/state`, `data/receipts`
- **Standards:** Workflow RO-Crate, Workflow Testing RO-Crate, Bioschemas ComputationalWorkflow / ComputationalTool / FormalParameter, Citation File Format and MIT — inspect [metadata](ro-crate-metadata.json)
- **Monitoring:** existing LifeMonitor global defaults for all branches, all tags and issue checks remain unmodified; repository packaging does not prove registration or active monitoring

See the public [architecture](docs/ARCHITECTURE.md), [scope](docs/SCOPE.md), [provenance](docs/PROVENANCE.md) and [publication policy](SECURITY.md)

## Origins

The project was established in October 2026 from an earlier research-workflow prototype. Only the current public software interfaces, metadata, tests and documentation define its supported behavior. Private working documents and internal decisions are not part of the published artifact
