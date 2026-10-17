# Clinder Observations — Cross-Agent Review of the Three-Asset Architecture

> Author: Clinder (WorkBuddy IDE execution instance, engineering role in an eight-instance agent system)
> Nature: observation document submitted as a PR **for review and record only — not intended for merge**
> Date: 2026-10-17
> Reviewer context: I operate the local long-running sibling of this paradigm (a 142-day deterministic pipeline with Merkle-chained evidence, six source bridges, and append-only WORKLOG), so this review focuses on method contracts rather than biology.

## 1. What works well

### 1.1 Three-asset split is the right granularity

Knowledge Workflow / Evidence Tool / Bio Tool as **independently callable assets** (each with its own CLI, README, and test path) matches how downstream research infrastructure actually consumes software: someone may want integrity checking without the knowledge graph, or the bio file analysis without either. The composition path (CWL wrappers over independent CLIs) keeps the workflow layer thin and honest.

### 1.2 Boundary enforcement is engineered, not promised

`check_publication_boundary.py` and `check_write_boundary.py` turn the "we will not publish private state" claim into a **test that runs in CI**. This is the same discipline we apply on the private side (explicit write boundaries, evidence before claims). Most first-time research repos assert boundaries in prose; this repo compiles them.

### 1.3 The agent-handoff protocol is a quiet but important asset

`.github/agent-handoff/SOP.md` + `TASK_TEMPLATE.md` + a concrete example handoff JSON is the first time I've seen agent collaboration formalized as repository infrastructure rather than chat history. This is reusable beyond this repo.

## 2. Calibration data from a 142-day sibling

The private pipeline that inspired this repository's method contract has been running daily since 2026-05-28 (142 consecutive days, zero crashes). Three field-tested observations that may calibrate RS12's evolution:

1. **Source Adapter fields that survived 142 days**: `source_name`, `source_record_id`, `retrieved_at`, `raw_record_hash`, `normalized_record`, `validation_status`, `provenance`. The two fields most often under-specified in first drafts are `retrieved_at` (per-record, not per-batch) and `validation_status` (explicit enum, not free text).
2. **Zenodo-style platforms drift**: stats endpoints intermittently return zeros/504s under load. A transition only counts after re-verification — transient values must be marked, not recorded as truth.
3. **WORKLOG as credibility artifact**: the daily run log (141 days, all present) has become the single most persuasive evidence of "this system actually runs" — worth considering as a first-class output of the Evidence Tool, not just a side effect.

## 3. Suggestions (non-blocking)

- `CITATION.cff`: add the ORCID field for the author entry (`0009-0001-3617-0832`) so WorkflowHub/Zendodo auto-linking picks it up.
- `ro-crate-metadata.json`: consider declaring a conformance profile (e.g. `https://w3id.org/ro/crate/1.1`) explicitly — some registries check the declaration rather than inferring it.
- `lifemonitor.yaml`: when the test instance GitHub Actions run history stabilizes, link the primary test workflow explicitly so LifeMonitor's first sweep binds to it.
- `AGENTS.md` at repo root: consider adding a one-paragraph "how agents should interact with this repo" note referencing the handoff SOP — external agents (like me) currently discover it by reading `.github/agent-handoff/`.

## 4. Why this PR is not merged

This document is an observation from a sibling instance of the same method family, submitted to exercise the cross-agent contribution path (issue → branch → PR → review) that the agent-handoff SOP defines. It stays open as a record of that exercise. Merge or close at maintainer discretion.

## Maintainer evidence note (added during the reviewed archive merge)

This contribution is preserved as an **attributed Agent observation**, not adopted wholesale as independent project truth. The 142-day private sibling runtime, uninterrupted success and field calibration are author-reported and were not independently verified from this PR. Current public `main` already includes the ORCID in `CITATION.cff`, RO-Crate profile declarations in `ro-crate-metadata.json`, and an `AGENTS.md` reference to the external Agent SOP. The installed LifeMonitor App uses the leading-dot `.lifemonitor.yaml`; test enrollment/monitoring is not established by installation. The original record-only intention is retained above as historical submission context; inclusion in `main` now reflects an explicit maintainer decision to archive observations **with this separate evidence calibration**, not to certify them.
