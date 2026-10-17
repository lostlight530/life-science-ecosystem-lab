# Life Science Knowledge Workflow

[First-use tutorial](../docs/GETTING_STARTED.md) · [Public interfaces](../docs/PUBLIC_INTERFACES.md) · [Verification limits](../docs/VERIFYING_RESULTS.md)

**Canonical runtime:** [`.github/workflows/life-science-knowledge.yml`](workflows/life-science-knowledge.yml)

This directory owns the scientific knowledge-production lifecycle, including workflow definition, deterministic knowledge projections, contract validation and state transitions. GitHub Actions **executes** the Workflow; it is not a third independently registered asset

| Location | Role |
| --- | --- |
| `workflows/life-science-knowledge.yml` | Source-aware periodic ingestion and guarded persistence |
| `workflows/validate.yml` | Reproducibility and metadata gate for pull requests |
| `workflows/life-science-evidence.yml` | Independent verification-tool CI |
| `knowledge/main.cwl` | Portable offline computational sub-workflow and regression fixture |
| `knowledge/test/` | Workflow replay inputs |
| `runtime/life_science_ecosystem_lab/` | Native knowledge projection, memory and lifecycle engine |
| `scripts/` | Provenance, world-line, write-boundary, RO-Crate checks |

**LifeMonitor:** no repository-specific `lifemonitor.yaml`; preserve the user's existing global all-branch, all-tag and issue-check settings where the app is installed. No external enrollment is implied

**Publication boundaries:** WorkflowHub, LifeMonitor and additional registries require evidence of actual external registrations; a passing GitHub test is not proof of enrollment

## Queryable, replayable graph surface

Verified knowledge projects into a deterministic graph under `data/knowledge/entities.jsonl` and `relations.jsonl` with `graph-manifest.json`. Accepted changes append events to `events.jsonl`. The search command builds a short-lived SQLite FTS5 index from the checked JSONL; it does not own authoritative state or require a resident service. Details: [public interfaces](../docs/PUBLIC_INTERFACES.md).
