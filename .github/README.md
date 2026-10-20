# Life Science Knowledge Workflow

[First-use tutorial](../docs/GETTING_STARTED.md) · [Public interfaces](../docs/PUBLIC_INTERFACES.md) · [Verification limits](../docs/VERIFYING_RESULTS.md)

**Canonical runtime:** [`.github/workflows/life-science-knowledge.yml`](workflows/life-science-knowledge.yml)

This directory owns the scientific knowledge-production lifecycle, including workflow definition, deterministic knowledge projections, contract validation and state transitions. GitHub Actions **executes** the Knowledge Workflow; it is not a fourth independently callable asset

| Location | Role |
| --- | --- |
| `workflows/life-science-knowledge.yml` | Reviewed-profile ingestion, verification and native-only guarded persistence |
| `workflows/life-science-daily-selfcheck.yml` | Fixed daily institutional/project assurance with versioned project-owned checks |
| `workflows/protein-structure-agent-demo.yml` | Isolated protein profile, Agent proposal and full-stack field demonstration |
| `workflows/validate.yml` | Reproducibility and metadata gate for pull requests |
| `workflows/life-science-evidence.yml` | Independent verification-tool CI |
| `workflows/life-science-framework.yml` | Independent Linux and Windows checks for the experimental Framework |
| `knowledge/main.cwl` | Portable offline computational sub-workflow and regression fixture |
| `knowledge/test/` | Workflow replay inputs |
| `runtime/life_science_ecosystem_lab/` | Native knowledge projection, memory and lifecycle engine |
| `scripts/` | Provenance, world-line, write-boundary, RO-Crate checks |

The required `validate.yml` workflow uses four actor-neutral, read-only domains: repository contracts, Knowledge Workflow replay, Evidence Tool checks and portable package replay. The domains have no inter-job dependency, so one failure does not suppress the remaining evidence. The aggregate `validate` check preserves the historical required-check name, reports all four results and fails unless every domain succeeds. Scheduled research checks and guarded native persistence remain separate workflows, not prerequisites for pull-request execution

**LifeMonitor:** [`lifemonitor.yaml`](../lifemonitor.yaml) uses the documented root-level config path and enables repository issue checks. It leaves branch/tag tracking, registry updates and visibility unspecified so account-wide settings remain authoritative. Current enrollment evidence is maintained in the single [standards status](../docs/STANDARDS.md) record

**Publication boundaries:** WorkflowHub, LifeMonitor and additional registries require evidence of actual external records; a passing GitHub test is not proof of enrollment. WorkflowHub 2347.2, the private LifeMonitor object, Zenodo release DOI, bio.tools identity and OpenEBench synchronization are separate evidence objects recorded in [standards status](../docs/STANDARDS.md)

**Experimental Framework:** [`../framework/`](../framework/README.md) is a separately installed software-contract package added after the frozen `v0.4.0` three-asset release. Its dedicated workflow preserves the existing Linux check and adds a Windows exact-byte replay check. It is not the WorkflowHub executable, a fourth Tool or a production writer

## Three different customization boundaries

- The Knowledge Workflow can manually select a reviewed `native` or `protein_structure` source/topic profile. Schedules always use `native`, and the `apply` job is structurally unavailable to every non-native profile
- The Daily Self-Check custom plane means repository-owned, version-controlled checks. It has no research-profile selector and cannot approve sources or produce knowledge
- The protein field demo resolves the reviewed `protein_structure` profile and exercises its proposal, pinned samples, external software inspection and isolated lifecycle replay. Changes to that content or method require ordinary reviewed repository changes

All three use explicit configuration, but none accepts arbitrary commands, paths or unreviewed sources at dispatch time

## Queryable, replayable graph surface

Verified knowledge projects into a deterministic graph under `data/knowledge/entities.jsonl` and `relations.jsonl` with `graph-manifest.json`. Accepted changes append events to `events.jsonl`. The search command builds a short-lived SQLite FTS5 index from the checked JSONL; it does not own authoritative state or require a resident service. Details: [public interfaces](../docs/PUBLIC_INTERFACES.md).
