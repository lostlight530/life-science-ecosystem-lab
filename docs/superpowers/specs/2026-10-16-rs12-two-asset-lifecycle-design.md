# RS12 Two Asset Lifecycle Design

## Document status

- Date: 2026-10-16
- Repository: `lostlight530/life-science-ecosystem-lab`
- Source baseline: `23e104fdb92b4221a90e1ead745dfa2cd40b1c99`
- Status: design for review
- Scope: two executable assets, one GitHub evidence source boundary, and the applicable Life Science workflow standards

## 1 Decision

RS12 will contain two separately testable but composable software assets

1. `NEXUS CORTEX Life Cycle — life-science-ecosystem-lab`
   - A GitHub Actions workflow that applies the bounded lifecycle proven in `welcome-to-github` and `zero-entropy-lab`
   - It validates, collects, projects, rebuilds, reasons over, verifies, and conditionally persists repository state
   - Its external evidence boundary is GitHub only

2. `Life Science GitHub Evidence Aggregator`
   - A Python library and CLI for deterministic search, selection, normalization, aggregation, comparison, and classification of evidence from approved GitHub repositories
   - It emits candidate evidence and diagnostics but never writes active knowledge directly
   - It is invoked by the lifecycle workflow and remains independently executable and testable

The lifecycle workflow is the orchestrator and governance boundary

The aggregator is the replaceable data-processing component

The current `Research Record Integrity Tool` and `Workflow Integration Profile Validator` are useful primitives but do not represent the final two-asset architecture

## 2 Evidence basis

### 2.1 Verified repository facts

The remote `main` branch at the recorded baseline contains a small Python package, deterministic JSON hashing, workflow profile validation, six unit-level checks, and `.github/workflows/validate.yml`

The baseline does not contain the following assets

- a NEXUS lifecycle workflow
- a GitHub evidence source registry
- a search and aggregation engine
- an active and archived evidence state model
- `lifemonitor.yaml`
- Workflow RO-Crate metadata
- Workflow Testing RO-Crate metadata
- Workflow Run RO-Crate provenance
- a CWL adapter

Successful validation of the baseline proves only that its existing pilot contracts pass

It does not prove WorkflowHub registration, LifeMonitor monitoring, RO-Crate conformance, bio.tools eligibility, or operation of the proposed lifecycle

### 2.2 Verified lineage facts

The current `welcome-to-github` and `zero-entropy-lab` lifecycle workflows share these verified properties

- scheduled and manual execution
- a read-only validation job
- a separately guarded apply job
- explicit runtime and ledger validation
- profile-driven GitHub document harvesting
- evidence projection and canonicalization
- context or memory rebuilding
- bounded reasoning and evolution stages
- final graph and runtime verification
- a path allowlist for writes
- a main-branch world-line check before persistence
- persistence only for a stable meaningful candidate
- machine manifests and human-readable receipts

RS12 reuses this lifecycle contract, not either repository's subject matter, archived data, graph, or internal memory

### 2.3 Verified official standards snapshot

This design uses the following current official specifications as checked on 2026-10-16

| Standard or service | Version or current contract | Consequence for RS12 |
|---|---|---|
| Workflow RO-Crate | 1.1 using RO-Crate 1.3 terminology | The crate must identify one main workflow as `File`, `SoftwareSourceCode`, and `ComputationalWorkflow`, declare `programmingLanguage`, and declare a license |
| Workflow Testing RO-Crate | 0.2 | A valid Workflow RO-Crate must mention at least one `TestSuite`; a GitHub Actions test instance uses `https://api.github.com` and a `repos/<OWNER>/<REPO>/actions/workflows/<FILE>` resource |
| Workflow Run RO-Crate | 0.6 | Run provenance uses a `CreateAction` whose instrument is the main workflow; input and output values can be linked to `FormalParameter` entities |
| Bioschemas ComputationalWorkflow | 1.0-RELEASE | Workflow metadata should expose accurate creator, license, input, output, programming language, and version information |
| Bioschemas ComputationalTool | 1.0-RELEASE | The aggregator can be described as a computational tool, but this metadata alone does not establish registry eligibility |
| Bioschemas FormalParameter | 1.0-RELEASE | Inputs and outputs represented in RO-Crate must use stable names and accurate types |
| LifeMonitor repository configuration | current JSON Schema at `https://api.lifemonitor.eu/integrations/github/config/schema.json` | Only `name`, `public`, `issues`, and `push` are permitted at the root; branch and tag rules use `name`, `update_registries`, `enable_notifications`, and optional `lifemonitor_instance` |
| Citation File Format | 1.2.0 | The repository must provide versioned, machine-readable citation metadata with the actual authorship and ORCID |
| EDAM | stable ontology | Terms must be selected from the stable ontology and must describe real operations, data, formats, or topics; terms are not inferred from project branding |
| SPDX | current license list and identifiers | License metadata uses a valid SPDX identifier and the repository includes the complete license text |

Primary sources

- <https://about.workflowhub.eu/Workflow-RO-Crate/1.1/>
- <https://w3id.org/ro/wftest/0.2>
- <https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/>
- <https://bioschemas.org/profiles/ComputationalWorkflow/1.0-RELEASE>
- <https://bioschemas.org/profiles/ComputationalTool/1.0-RELEASE>
- <https://bioschemas.org/profiles/FormalParameter/1.0-RELEASE>
- <https://lifemonitor.eu/lm_wft_best_practices_github_app>
- <https://api.lifemonitor.eu/integrations/github/config/schema.json>
- <https://citation-file-format.github.io/>
- <https://edamontology.org/>
- <https://spdx.dev/learn/handling-license-info/>

## 3 Claims and non-claims

### 3.1 Claims the implementation may make after verification

- deterministic processing of approved GitHub sources
- explicit source commit, tree, blob, and normalized-content identities
- reproducible selection and aggregation for a fixed source snapshot and profile
- append-only preservation of superseded snapshots
- separation of current state from archived state
- machine-readable workflow, test, citation, license, and run metadata
- continuous execution of declared tests through GitHub Actions
- a guarded and reviewable persistence boundary

### 3.2 Claims the implementation must not make

- biological interpretation
- clinical or diagnostic validity
- institutional endorsement from ELIXIR, Life Science RI, WorkflowHub, or LifeMonitor
- bio.tools acceptance before an entry is reviewed and accepted
- LifeMonitor monitoring merely because `lifemonitor.yaml` exists
- WorkflowHub registration merely because an RO-Crate exists
- FAIR compliance as a binary status
- semantic understanding by an algorithm when the implementation performs deterministic matching and classification
- support for arbitrary internet sources

## 4 Architecture

### 4.1 Component boundaries

```text
Approved GitHub source profiles
        |
        v
GitHub Source Adapter
        |
        v
Life Science GitHub Evidence Aggregator
  select -> normalize -> aggregate -> compare -> classify
        |
        v
Candidate Evidence Bundle
        |
        v
NEXUS CORTEX Life Cycle
  validate -> harvest -> project -> canonicalize -> rebuild
  -> ingest -> reason -> evolve -> verify -> boundary check
  -> world-line check -> guarded persistence -> receipt
        |
        +--> current evidence and active ledgers
        +--> immutable archive
        +--> run manifest and human receipt
```

The source adapter knows how to read GitHub

The aggregator knows how to transform evidence

The lifecycle knows when a candidate is valid and whether it may be persisted

No component may bypass the next boundary

### 4.2 GitHub source boundary

Every external source must be declared in a versioned profile

Required source identity

```yaml
profile_id: workflow-ro-crate-specification
repository: workflowhub-eu/about
source_class: official-specification
primary_owner: rs12
status: core
cadence: daily
default_branch_policy: repository-default
documents:
  - Workflow-RO-Crate/**
ignore_patterns:
  - "**/fixtures/**"
  - "**/mock/**"
  - "**/generated/**"
topics:
  - workflow-ro-crate
trust_level: primary
promotion_approved: true
```

The committed profile is the authorization boundary

Repository discovery may propose a profile candidate, but a discovered repository is not automatically approved or harvested

### 4.3 Source provenance

Every selected GitHub document must retain

- repository owner and name
- default branch observed at retrieval
- commit SHA
- tree SHA
- path
- blob SHA
- normalized-content SHA-256
- retrieval time in UTC
- source profile ID and profile version
- selection rule that matched the path
- trust class
- processing software version

The content digest does not replace the Git object identities

All identities are retained because a blob can appear in multiple commits and the same normalized content can result from distinct source bytes

### 4.4 State separation

```text
data/inputs/current
    exactly one canonical active snapshot per source document

data/inputs/archive/YYYY/MM
    append-only superseded snapshots

data/state
    observed source state and run checkpoints

data/knowledge
    active normalized entities and relations only

data/memories
    bounded generated summaries and decisions

data/receipts
    run manifests and human-readable receipts
```

Archive paths are excluded from active ingestion, graph construction, current hashes, and current search results

An existing archive path may never be overwritten with different bytes

### 4.5 Candidate evidence bundle

The aggregator emits a versioned bundle rather than writing knowledge directly

Required fields

```json
{
  "schema_version": "1.0.0",
  "run_id": "uuid",
  "profile_digest": "sha256",
  "algorithm_version": "semver-or-commit",
  "sources": [],
  "records": [],
  "changes": [],
  "diagnostics": [],
  "input_digest": "sha256",
  "output_digest": "sha256",
  "projection_eligible": false
}
```

`projection_eligible` is computed only after schema validation, provenance validation, duplicate detection, deletion propagation, and deterministic digest verification

It does not authorize persistence

## 5 Asset one NEXUS CORTEX Life Cycle

### 5.1 Canonical executable

`.github/workflows/nexus-life-cycle.yml`

The canonical executable is a GitHub Actions workflow and will be represented in WorkflowHub as workflow type `Other` unless WorkflowHub introduces a specific GitHub Actions type

No abstract CWL will be presented as the executable identity of this asset

### 5.2 Jobs

The workflow contains two jobs

#### Validate

- runs on pull requests, relevant pushes, and manual dispatch
- has read-only repository permission
- compiles and tests the lifecycle and aggregator
- validates source profiles and JSON Schemas
- validates active ledgers without rewriting them
- validates Workflow RO-Crate and Workflow Testing RO-Crate structure
- validates `lifemonitor.yaml` against the pinned official schema snapshot
- proves the working tree remains unchanged
- publishes a validation receipt

#### Apply

- runs only on `main` for the schedule or an explicit manual `apply=true`
- records the starting main SHA
- performs every validation gate before collection
- invokes the aggregator through its public CLI
- projects only eligible candidate evidence
- canonicalizes active state
- rebuilds context and produces bounded outputs
- repeats tests and invariant checks after the last generated write
- enforces the write allowlist
- fetches and compares the current remote main SHA
- commits only a meaningful staged delta
- refuses to push if main moved
- publishes a manifest and receipt regardless of outcome

### 5.3 Required outcomes

- `VALIDATED_READ_ONLY`
- `NO_MEANINGFUL_DELTA`
- `APPLIED`
- `CONFLICTED_WORLD_LINE_NO_APPLY`
- `VALIDATION_FAILED`
- `SOURCE_UNAVAILABLE`

An unavailable required source fails the run

An unavailable optional source produces a degraded candidate that is not eligible for automatic persistence unless the profile explicitly permits partial evidence

### 5.4 Permissions and supply chain

- validation uses `contents: read`
- apply uses only `contents: write`
- no broad organization, issue, pull request, package, or identity permission is requested
- third-party GitHub Actions are pinned to immutable commit SHAs
- Python runtime dependencies remain empty for the first implementation unless an approved plan adds one
- no workflow receives LS Login, WorkflowHub, LifeMonitor, ORCID, or other external credentials
- the built-in GitHub token is used only for GitHub evidence access and the guarded main update

## 6 Asset two Life Science GitHub Evidence Aggregator

### 6.1 Public interfaces

Library interface

```python
collect(profile, transport) -> SourceSnapshot
aggregate(snapshots, topic_profile) -> CandidateEvidenceBundle
validate(bundle) -> ValidationReport
```

CLI interface

```text
ls-ecosystem-lab evidence collect --profiles profiles/sources.json --output build/snapshots
ls-ecosystem-lab evidence aggregate --snapshots build/snapshots --topics profiles/topics.json --output build/candidate.json
ls-ecosystem-lab evidence validate build/candidate.json
```

The CLI uses nonzero exit status for invalid profiles, incomplete required provenance, source failures, invalid bundles, and digest mismatches

### 6.2 Search semantics

Search is deterministic matching over approved GitHub repository trees and document contents

It is not an unbounded web search and does not require a language model

The first algorithm version supports

- path glob selection
- ignore globs
- exact normalized terms
- case-folded token terms
- declared aliases
- required and excluded term groups
- repository and layer grouping
- duplicate detection by Git blob and normalized SHA-256
- change classification as added, modified, removed, moved, or unchanged
- source-priority ordering from the profile
- evidence-strength classification from declared trust and provenance completeness

Scores must be explainable as named rule contributions

No opaque relevance score is used as a persistence gate

### 6.3 Network abstraction

The production transport reads GitHub repository metadata, commits, trees, and blobs

Tests use a fixture transport and never depend on live GitHub

The transport interface makes local replay possible without changing aggregation logic

### 6.4 Write behavior

The aggregator may write only to its caller-supplied output directory

It does not commit, push, open pull requests, publish releases, update registries, or modify active ledgers

## 7 Standards conformance model

RS12 will not use a single `compliant: true` flag

Every standard is recorded with one of four states

- `REQUIRED`
- `CONDITIONAL`
- `NOT_APPLICABLE`
- `EXTERNAL_VERIFICATION_REQUIRED`

### 7.1 Required before first release

| Requirement | Verification |
|---|---|
| Public version-controlled repository | Git remote and release source commit |
| SPDX-compatible license | license identifier plus full `LICENSE` text |
| CFF 1.2.0 citation metadata | schema validation and consistency with release version |
| Workflow RO-Crate 1.1 | structural validation against RO-Crate 1.3 context and profile requirements |
| Workflow Testing RO-Crate 0.2 | structural validation plus exact GitHub Actions test resource |
| LifeMonitor repository configuration | validation against the official JSON Schema snapshot |
| Bioschemas ComputationalWorkflow 1.0 metadata | required and recommended fields checked for the NEXUS workflow |
| Bioschemas ComputationalTool 1.0 metadata | accurate fields checked for the aggregator |
| FormalParameter 1.0 metadata | stable names and accurate types for declared inputs and outputs |
| Deterministic fixtures | repeated execution produces byte-identical normalized output |
| Negative tests | invalid provenance, path escape, archive overwrite, source deletion, and digest mismatch fail deterministically |
| Provenance | commit, tree, blob, content digest, tool version, profile digest, and run identity |

### 7.2 Conditional

| Item | Decision |
|---|---|
| CWL adapter | Add a thin CWL `CommandLineTool` only after the CLI interface is stable and cwltool validation is included; it represents the aggregator invocation, not the NEXUS GitHub Action |
| Workflow Run RO-Crate 0.6 | Generate after the execution output contract is stable; do not fabricate run entities before a real run exists |
| EDAM annotations | Add only terms verified against the stable ontology and justified by actual inputs, outputs, and operations |
| CodeMeta | Generate or maintain only if a consuming registry requires it; CFF remains the citation source of truth |
| Software Heritage or DOI links | Add only after those external records exist and resolve to the exact release |

### 7.3 Not applicable in the first release

- clinical and healthcare data standards
- patient or sensitive data governance
- GA4GH service compatibility
- laboratory SOP metadata
- Galaxy, Nextflow, or Snakemake layout rules
- container metadata
- ontology terms for biological analysis that the software does not perform

### 7.4 External verification required

- WorkflowHub import and final public metadata
- WorkflowHub workflow type presentation
- LifeMonitor enrollment and observed test status
- registry version propagation
- DOI minting
- bio.tools acceptance

These are external states and cannot be proven by repository files alone

## 8 Registry strategy

### 8.1 WorkflowHub and LifeMonitor

The initial WorkflowHub asset is the NEXUS lifecycle

- title: `NEXUS CORTEX Life Cycle — life-science-ecosystem-lab`
- canonical executable: `.github/workflows/nexus-life-cycle.yml`
- workflow type: `Other`
- source: exact GitHub release or commit URL
- maturity before production evidence: `work-in-progress`

The Workflow Testing RO-Crate points to `.github/workflows/validate.yml` as the GitHub Actions test instance, not to the lifecycle schedule itself

The first `lifemonitor.yaml` policy is

```yaml
name: "NEXUS CORTEX Life Cycle — life-science-ecosystem-lab"
public: true
issues:
  check: true
push:
  branches:
    - name: "main"
      update_registries: []
      enable_notifications: true
  tags:
    - name: "v*.*.*"
      update_registries: ["wfhub"]
      enable_notifications: true
```

This repository-level configuration prevents the user's global `all branches` and `all tags` setting from turning experimental branches and non-release tags into registry versions

The registry update remains inactive until the LifeMonitor configuration validator accepts the file and the user explicitly authorizes production integration

### 8.2 bio.tools

The aggregator is not automatically eligible for bio.tools

The official curator guidance scopes bio.tools to bioinformatics software with well-defined data-processing functions and EDAM-described operations, inputs, and outputs

Processing GitHub repository evidence about Life Science software is not by itself biological or bioinformatics data processing

Therefore the first release will prepare accurate Bioschemas ComputationalTool metadata but will mark bio.tools status as `EXTERNAL_VERIFICATION_REQUIRED`

A bio.tools submission is permitted only after a curator-facing scope review confirms that the implemented function is in scope and accurate EDAM annotations exist

## 9 Repository layout

```text
life-science-ecosystem-lab/
├── .github/workflows/
│   ├── validate.yml
│   └── nexus-life-cycle.yml
├── docs/
│   ├── architecture/
│   ├── standards/
│   └── superpowers/specs/
├── profiles/
│   ├── sources.schema.json
│   ├── sources.json
│   ├── topics.schema.json
│   └── topics.json
├── schemas/
│   ├── candidate-evidence.schema.json
│   ├── lifecycle-manifest.schema.json
│   ├── lifecycle-receipt.schema.json
│   └── workflow-profile.schema.json
├── src/life_science_ecosystem_lab/
│   ├── evidence/
│   │   ├── transport.py
│   │   ├── github.py
│   │   ├── selection.py
│   │   ├── normalization.py
│   │   ├── aggregation.py
│   │   └── validation.py
│   ├── lifecycle/
│   │   ├── guard.py
│   │   ├── projection.py
│   │   ├── state.py
│   │   └── receipt.py
│   └── cli.py
├── data/
│   ├── inputs/current/
│   ├── inputs/archive/
│   ├── knowledge/
│   ├── memories/
│   ├── state/
│   └── receipts/
├── ro-crate/
│   ├── workflow/ro-crate-metadata.json
│   ├── testing/ro-crate-metadata.json
│   └── runs/examples/
├── metadata/
│   ├── bioschemas-workflow.jsonld
│   ├── bioschemas-tool.jsonld
│   └── standards-status.json
├── tests/
│   ├── contracts/
│   ├── fixtures/github/
│   ├── expected/
│   └── integration/
├── workflows/
│   └── evidence-aggregator.cwl
├── CITATION.cff
├── LICENSE
├── lifemonitor.yaml
├── pyproject.toml
└── README.md
```

The CWL file and run crate directory are created only when their conditional gates are met

No `sops/` directory is created in this phase

## 10 Validation strategy

### 10.1 Unit tests

- profile schema and semantic validation
- safe repository-relative paths
- glob selection and ignore precedence
- Unicode and line-ending normalization
- stable canonical JSON
- duplicate detection
- added, modified, removed, moved, and unchanged classification
- deterministic evidence-strength rules
- content and bundle digests
- error propagation

### 10.2 Contract tests

- incomplete Git identities are rejected
- a truncated Git tree is rejected
- two profiles cannot own the same source identity ambiguously
- an unapproved source is rejected
- an existing archive collision with different bytes is rejected
- archive paths cannot enter active search or projection
- source deletion propagates into the candidate bundle
- current snapshots have exactly one canonical path
- output paths cannot escape the requested root
- a final validation pass produces no new write

### 10.3 Workflow tests

- validation job has no write permission
- apply job cannot run from a non-main ref
- apply requires schedule or explicit manual approval
- world-line movement prevents persistence
- empty semantic delta produces no commit
- unexpected write paths fail the run
- tests run again after generated writes
- GitHub Actions references are pinned

### 10.4 Metadata tests

- CFF schema and repository facts agree
- license identifiers agree across CFF, Python metadata, RO-Crate, and `LICENSE`
- ORCID uses its canonical HTTPS form
- Workflow RO-Crate main entity exists and has the required types
- WTROC test suite references the validation workflow
- the LifeMonitor resource exactly names the repository and workflow file
- Bioschemas entities use released profile URLs
- every EDAM URI is present in the pinned stable term set
- status metadata never upgrades an external state without evidence

### 10.5 Live checks

Live GitHub checks are separated from deterministic tests

They confirm connectivity and current source identity but do not replace fixture-based tests

WorkflowHub, LifeMonitor, and bio.tools are never called from ordinary pull request validation

## 11 Error and degradation policy

| Condition | Result |
|---|---|
| Required GitHub source unavailable | fail collection, preserve current state, write no candidate to active data |
| Optional source unavailable | record diagnostic, candidate is degraded, automatic projection disabled unless explicitly allowed by profile |
| Rate limit exhausted | fail with retry metadata; do not silently omit sources |
| Truncated repository tree | fail that source; do not treat the partial tree as complete |
| Invalid UTF-8 | decode with an explicit documented policy and record the replacement count, or reject according to the source profile |
| Schema mismatch | fail before projection |
| Archive collision | fail without overwrite |
| Main branch moved | keep the verified candidate only as a run artifact and do not push |
| Metadata validator unavailable | classify validation as unavailable, not passed |

Retries are bounded and only cover transient network classes

Semantic validation failures are not retried

## 12 Versioning and identity

```text
Git commit
    exact implementation and source state

Release tag vMAJOR.MINOR.PATCH
    verified software release

WorkflowHub version
    external version of the registered NEXUS workflow

LifeMonitor tracked version
    monitored branch or release test identity

Aggregator algorithm version
    transformation contract recorded in every candidate bundle
```

The first production release requires a clean commit, passing final GitHub Actions run, matching citation version, matching RO-Crate version, and an explicit user decision to publish

Metadata edits and workflow executable changes are treated separately because WorkflowHub currently documents workflow versioning as experimental and notes that metadata updates do not necessarily update existing RO-Crate metadata

## 13 Migration from the current pilot

The migration keeps verified primitives and replaces the incorrect product framing

Keep and adapt

- canonical JSON serialization
- SHA-256 manifest generation
- safe repository-relative path validation
- explicit registry and monitoring status vocabulary
- standard-library-only runtime
- the current test and hygiene discipline

Replace or extend

- replace `Research Record Integrity Tool` as the public second product with the GitHub Evidence Aggregator
- turn workflow profile validation into one standards-validation component
- add the lifecycle package, source profiles, state separation, and guarded apply workflow
- add official metadata and monitoring artifacts only after their validators are in place
- rewrite the README so it names the two real assets and their evidence boundaries

No existing public history is rewritten

## 14 Implementation phases and acceptance gates

### Phase 1 Deterministic aggregator core

Acceptance

- fixture transport and GitHub transport share one interface
- source and topic profiles validate
- fixed fixtures produce byte-identical candidate bundles
- deletions, duplicates, moves, and provenance failures are tested
- the CLI writes only to the requested output root

### Phase 2 Bounded lifecycle

Acceptance

- read-only and apply paths are separate
- every lifecycle phase has an explicit input and output
- state, current evidence, archive, knowledge, and receipts are isolated
- final verification and write boundary checks pass
- main movement produces no push

### Phase 3 LS metadata and monitoring package

Acceptance

- Workflow RO-Crate 1.1 metadata validates
- WTROC 0.2 metadata identifies `.github/workflows/validate.yml`
- Bioschemas workflow and tool JSON-LD use released profiles
- CFF, SPDX license, Python metadata, and RO-Crate agree
- `lifemonitor.yaml` validates against the official schema
- external states remain `prepared`, not `verified`

### Phase 4 Optional CWL and run provenance

Acceptance

- the stable aggregator CLI has a thin CWL adapter
- the adapter runs against fixed fixtures with byte-identical output
- a real run generates a Workflow Run RO-Crate 0.6 package
- the crate links declared parameters to actual run objects and results

### Phase 5 External integration

Requires separate user authorization

Acceptance

- WorkflowHub imports the exact release identity
- LifeMonitor displays the expected GitHub Actions test instance
- branch and tag behavior matches repository policy
- public metadata matches the source release
- any bio.tools submission has prior scope confirmation and accurate EDAM annotations

## 15 Completion definition

The architecture is complete only when both assets can be understood, invoked, tested, versioned, and replaced independently

The implementation is release-ready only when all required repository checks pass and all external integrations are still accurately classified as either verified or unverified

The project succeeds by producing inspectable research software contracts, not by maximizing the number of standards files or registry records
