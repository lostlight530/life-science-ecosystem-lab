# RS12 Two Asset Lifecycle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the two approved RS12 assets: a bounded NEXUS CORTEX GitHub lifecycle and an independently usable, deterministic GitHub evidence aggregator, with LifeMonitor and WorkflowHub metadata that describe only verified capabilities

**Architecture:** The aggregator is a standard-library Python package and CLI that reads versioned source and topic profiles, acquires approved GitHub repository content through an injected transport, normalizes and classifies evidence deterministically, and emits a candidate bundle without mutating active state. The lifecycle is the orchestration and governance layer: it validates inputs, invokes the aggregator, verifies the candidate, projects permitted state, revalidates invariants and the remote world-line, and only then performs a bounded write. Active state, immutable archives, knowledge projections, memories, manifests, and receipts remain separate

**Tech Stack:** Python 3.11+ standard library, `unittest`, JSON and JSON Schema documents, GitHub Actions YAML, LifeMonitor configuration, RO-Crate JSON-LD, Bioschemas JSON-LD, Citation File Format 1.2.0, MIT license

**Spec:** `docs/superpowers/specs/2026-10-16-rs12-two-asset-lifecycle-design.md`

## Global Constraints

- The only external evidence source in the first implementation is GitHub
- Source repositories and paths must be explicitly approved by versioned profiles
- Ordinary and contract tests must not require live network access
- Runtime code must keep zero third-party dependencies
- The aggregator must never commit, push, update active knowledge, or write outside the caller-selected output root
- Existing public commands `record-integrity` and `validate-workflow-profile` must remain compatible
- Archived evidence is append-only and excluded from active aggregation, graph projection, and active digests
- A missing prior raw cache must not be interpreted as every source being newly added
- Source deletion, path movement, duplicate content, truncated trees, unavailable sources, archive collisions, and remote-main movement must have explicit deterministic outcomes
- Validation must complete after the final generated write, not before it
- The lifecycle may persist only an allowlisted stable and meaningful candidate
- No workflow may receive credentials beyond the repository-scoped `GITHUB_TOKEN`
- No WorkflowHub, LifeMonitor, bio.tools, DOI, monitoring, or scientific-validity status may be claimed without external verification
- The first implementation must not add a CWL wrapper or Workflow Run RO-Crate; those remain gated follow-on assets after the CLI and a real run are stable
- Do not create SOP content in this implementation

## Review Focus

1. Unicode normalization and line-ending determinism across Linux and Windows
2. GitHub recursive-tree truncation and partial-source behavior
3. Archive collision handling and exactly one active snapshot per source identity
4. Deletion and move propagation without false full-addition reports
5. Remote `main` movement between read-only validation and guarded application

---

## Task 1: Establish versioned domain contracts

**Files:**

- Create: `src/life_science_ecosystem_lab/evidence/__init__.py`
- Create: `src/life_science_ecosystem_lab/evidence/models.py`
- Create: `src/life_science_ecosystem_lab/evidence/diagnostics.py`
- Create: `tests/test_models.py`
- Modify: `src/life_science_ecosystem_lab/__init__.py`

- [ ] **Step 1: Write failing tests for immutable contract objects**

Add tests for these public objects and invariants:

```python
SourceIdentity(owner="example", repository="repo", ref="main")
GitTreeEntry(path="docs/a.md", object_id="a" * 40, size=12)
SourceSnapshot(...)
EvidenceRecord(...)
Diagnostic(code="SOURCE_UNAVAILABLE", severity=Severity.ERROR, message="...")
CandidateEvidenceBundle(...)
ValidationReport(valid=False, errors=(...), warnings=())
```

Verify that tuples, frozen dataclasses, canonical identifiers, and enum values cannot drift after construction. Verify that paths are POSIX-relative and source identifiers are stable under serialization

- [ ] **Step 2: Run the focused test and observe the expected import failure**

Run:

```bash
python -m unittest tests.test_models -v
```

Expected: `ModuleNotFoundError` or missing public object failures

- [ ] **Step 3: Implement the smallest typed contract layer**

Define frozen dataclasses and enums for:

```python
class Severity(str, Enum): ...
class ChangeKind(str, Enum): ...
class LifecycleOutcome(str, Enum): ...

@dataclass(frozen=True)
class SourceIdentity: ...

@dataclass(frozen=True)
class GitTreeEntry: ...

@dataclass(frozen=True)
class SourceSnapshot: ...

@dataclass(frozen=True)
class EvidenceRecord: ...

@dataclass(frozen=True)
class CandidateEvidenceBundle: ...

@dataclass(frozen=True)
class ValidationReport: ...
```

Keep serialization explicit through `to_dict()` methods rather than implicit `asdict()` recursion so field names and ordering remain part of a reviewed contract

- [ ] **Step 4: Run the focused and baseline tests**

Run:

```bash
python -m unittest tests.test_models -v
python -m unittest discover -s tests -v
```

Expected: all tests pass and the six existing pilot tests remain green

- [ ] **Step 5: Commit the contract layer**

```bash
git add src/life_science_ecosystem_lab/evidence src/life_science_ecosystem_lab/__init__.py tests/test_models.py
git commit -m "feat: define evidence lifecycle contracts"
```

## Task 2: Add source and topic profile validation

**Files:**

- Create: `src/life_science_ecosystem_lab/evidence/profiles.py`
- Create: `profiles/sources.schema.json`
- Create: `profiles/topics.schema.json`
- Create: `profiles/sources.json`
- Create: `profiles/topics.json`
- Create: `tests/test_profiles.py`
- Create: `tests/fixtures/source-registry-valid.json`
- Create: `tests/fixtures/source-registry-invalid.json`
- Create: `tests/fixtures/topic-registry-valid.json`
- Modify: `src/life_science_ecosystem_lab/cli.py`

- [ ] **Step 1: Write failing profile tests**

Cover:

- required schema versions
- unique profile and source identifiers
- `owner/repository` identity validation
- explicit branch or immutable commit selection
- safe repository-relative include and exclude globs
- exclude precedence over include
- approved-source flag
- per-source trust class and rationale
- topic aliases, required terms, excluded terms, and minimum evidence thresholds
- rejection of backslashes, absolute paths, `..`, empty includes, and unknown fields

Specify public functions:

```python
def load_source_registry(path: Path) -> SourceRegistry: ...
def load_topic_registry(path: Path) -> TopicRegistry: ...
def validate_source_registry(value: Mapping[str, object]) -> list[str]: ...
def validate_topic_registry(value: Mapping[str, object]) -> list[str]: ...
```

- [ ] **Step 2: Run the focused tests and verify they fail**

```bash
python -m unittest tests.test_profiles -v
```

Expected: missing module or missing validator failures

- [ ] **Step 3: Implement strict standard-library validators**

Parse JSON using the existing deterministic JSON loader. Reject unknown fields and ambiguous configurations. Do not claim JSON Schema validation at runtime because no schema library is installed; keep the machine schemas and Python validators consistent through contract tests

- [ ] **Step 4: Add CLI validation commands without breaking old commands**

Add:

```bash
ls-ecosystem-lab validate-source-registry profiles/sources.json
ls-ecosystem-lab validate-topic-registry profiles/topics.json
```

Use exit code `0` for valid, `1` for contract violations, and `2` for I/O or malformed JSON

- [ ] **Step 5: Run focused, CLI, and full tests**

```bash
python -m unittest tests.test_profiles -v
python -m life_science_ecosystem_lab validate-source-registry profiles/sources.json
python -m life_science_ecosystem_lab validate-topic-registry profiles/topics.json
python -m unittest discover -s tests -v
```

Expected: all commands exit `0`; malformed fixtures are rejected with stable diagnostics

- [ ] **Step 6: Commit the profile contracts**

```bash
git add src/life_science_ecosystem_lab/evidence/profiles.py src/life_science_ecosystem_lab/cli.py profiles tests/test_profiles.py tests/fixtures
git commit -m "feat: add approved GitHub evidence profiles"
```

## Task 3: Implement the GitHub transport boundary

**Files:**

- Create: `src/life_science_ecosystem_lab/evidence/transport.py`
- Create: `src/life_science_ecosystem_lab/evidence/github.py`
- Create: `tests/test_github_transport.py`
- Create: `tests/fixtures/github/repository.json`
- Create: `tests/fixtures/github/commit.json`
- Create: `tests/fixtures/github/tree.json`
- Create: `tests/fixtures/github/blob.json`

- [ ] **Step 1: Write failing transport tests**

Define a protocol and two implementations:

```python
class GitHubTransport(Protocol):
    def get_repository(self, identity: SourceIdentity) -> Mapping[str, object]: ...
    def get_commit(self, identity: SourceIdentity, ref: str) -> Mapping[str, object]: ...
    def get_tree(self, identity: SourceIdentity, tree_sha: str) -> Mapping[str, object]: ...
    def get_blob(self, identity: SourceIdentity, blob_sha: str) -> bytes: ...

class FixtureGitHubTransport: ...
class UrlLibGitHubTransport: ...
```

Test URL construction, percent encoding, explicit headers, timeouts, GitHub API error normalization, base64 decoding, non-UTF-8 rejection, rate-limit diagnostics, and bounded retry for `429`, `502`, `503`, and `504`

- [ ] **Step 2: Run tests and observe failure**

```bash
python -m unittest tests.test_github_transport -v
```

- [ ] **Step 3: Implement transport with dependency injection**

Use `urllib.request`, `urllib.error`, `base64`, and an injected sleeper. Never print or serialize tokens. Accept an optional token from the caller only; do not read arbitrary credential files

Treat `truncated: true` in recursive tree responses as an explicit `TREE_TRUNCATED` error. Do not silently aggregate an incomplete tree

- [ ] **Step 4: Verify deterministic fixture behavior and error paths**

```bash
python -m unittest tests.test_github_transport -v
python -m unittest discover -s tests -v
```

- [ ] **Step 5: Commit the transport boundary**

```bash
git add src/life_science_ecosystem_lab/evidence/transport.py src/life_science_ecosystem_lab/evidence/github.py tests/test_github_transport.py tests/fixtures/github
git commit -m "feat: add bounded GitHub evidence transport"
```

## Task 4: Implement deterministic path selection and text normalization

**Files:**

- Create: `src/life_science_ecosystem_lab/evidence/selection.py`
- Create: `src/life_science_ecosystem_lab/evidence/normalization.py`
- Create: `tests/test_selection.py`
- Create: `tests/test_normalization.py`

- [ ] **Step 1: Write failing selection tests**

Test sorted traversal, include matching, exclude precedence, regular-file filtering, size limits, duplicate object IDs at different paths, and rejection of unsafe paths

Public interface:

```python
def select_paths(entries: Iterable[GitTreeEntry], profile: SourceProfile) -> tuple[GitTreeEntry, ...]: ...
```

- [ ] **Step 2: Write failing normalization tests**

Cover UTF-8 decoding, UTF-8 BOM removal, CRLF and CR conversion to LF, Unicode NFC normalization, removal of no semantic bytes, final-newline normalization, and stable SHA-256 digests

Public interface:

```python
def normalize_text_bytes(value: bytes) -> str: ...
def canonical_text_bytes(value: str) -> bytes: ...
def sha256_bytes(value: bytes) -> str: ...
```

- [ ] **Step 3: Run focused tests and confirm failure**

```bash
python -m unittest tests.test_selection tests.test_normalization -v
```

- [ ] **Step 4: Implement minimal deterministic logic**

Use `PurePosixPath`, `fnmatch`, `unicodedata.normalize("NFC", ...)`, and `hashlib.sha256`. Preserve meaningful whitespace other than line-ending and single-final-newline normalization

- [ ] **Step 5: Run focused and full tests**

```bash
python -m unittest tests.test_selection tests.test_normalization -v
python -m unittest discover -s tests -v
```

- [ ] **Step 6: Commit selection and normalization**

```bash
git add src/life_science_ecosystem_lab/evidence/selection.py src/life_science_ecosystem_lab/evidence/normalization.py tests/test_selection.py tests/test_normalization.py
git commit -m "feat: select and normalize GitHub evidence"
```

## Task 5: Build source collection with complete provenance

**Files:**

- Create: `src/life_science_ecosystem_lab/evidence/collector.py`
- Create: `tests/test_collector.py`
- Create: `tests/fixtures/github/source-a-tree.json`
- Create: `tests/fixtures/github/source-a-readme.json`
- Create: `tests/fixtures/github/source-a-citation.json`

- [ ] **Step 1: Write failing collection tests**

Specify:

```python
def collect_sources(
    registry: SourceRegistry,
    transport: GitHubTransport,
    *,
    retrieved_at: datetime,
) -> CollectionResult: ...
```

Assert every collected record includes:

- source profile ID and version
- owner and repository
- requested ref and resolved commit SHA
- tree SHA
- path and blob SHA
- raw byte size
- normalized SHA-256
- retrieval timestamp in UTC
- selection-rule identifier
- trust class
- collector software version

Test all-or-explicit-partial behavior, source unavailability, missing required paths, truncated tree rejection, duplicate selected paths, and stable ordering independent of API response order

- [ ] **Step 2: Run the focused tests and observe failure**

```bash
python -m unittest tests.test_collector -v
```

- [ ] **Step 3: Implement collection without writing state**

Return in-memory snapshots and diagnostics only. The collector must not know active-state or archive paths

- [ ] **Step 4: Verify provenance completeness and stability**

```bash
python -m unittest tests.test_collector -v
python -m unittest discover -s tests -v
```

- [ ] **Step 5: Commit collection**

```bash
git add src/life_science_ecosystem_lab/evidence/collector.py tests/test_collector.py tests/fixtures/github
git commit -m "feat: collect GitHub evidence with provenance"
```

## Task 6: Implement explainable aggregation and change classification

**Files:**

- Create: `src/life_science_ecosystem_lab/evidence/aggregation.py`
- Create: `src/life_science_ecosystem_lab/evidence/change_detection.py`
- Create: `src/life_science_ecosystem_lab/evidence/bundles.py`
- Create: `src/life_science_ecosystem_lab/evidence/validation.py`
- Create: `schemas/candidate-evidence.schema.json`
- Create: `tests/test_aggregation.py`
- Create: `tests/test_change_detection.py`
- Create: `tests/test_bundles.py`

- [ ] **Step 1: Write failing aggregation tests**

Specify:

```python
def aggregate_evidence(
    snapshots: Sequence[SourceSnapshot],
    topics: TopicRegistry,
    previous: CandidateEvidenceBundle | None = None,
) -> CandidateEvidenceBundle: ...
```

Test exact-token, alias, required-term, excluded-term, and path-weight rules. Each accepted topic contribution must identify the source record and matched rule. Scores must be integer or fixed rational values, never floating-point accumulations

- [ ] **Step 2: Write failing change-classification tests**

Cover `added`, `modified`, `removed`, `moved`, `unchanged`, and `unknown_baseline`

Required safety property: `previous is None` yields `unknown_baseline`, not a synthetic full-addition set

Deletion of a previously present path must survive into the candidate bundle. A moved record must be detected only when normalized content identity is equal and the old path disappeared

- [ ] **Step 3: Write failing canonical bundle tests**

The bundle must contain:

```text
schema_version
run_id
profile_digest
algorithm_version
sources
records
changes
diagnostics
input_digest
output_digest
projection_eligible
```

Test recursive canonical JSON, sorted mappings, no NaN or Infinity, deterministic list ordering, digest self-consistency, and tamper detection

- [ ] **Step 4: Run the focused tests and observe failure**

```bash
python -m unittest tests.test_aggregation tests.test_change_detection tests.test_bundles -v
```

- [ ] **Step 5: Implement the deterministic engine**

Keep ranking rules visible in the topic profiles. Emit diagnostics for excluded evidence and unmet thresholds. `projection_eligible` may be true only when all required sources are complete, no error diagnostic exists, and the bundle validates

- [ ] **Step 6: Run focused and full tests**

```bash
python -m unittest tests.test_aggregation tests.test_change_detection tests.test_bundles -v
python -m unittest discover -s tests -v
```

- [ ] **Step 7: Commit aggregation and bundle logic**

```bash
git add src/life_science_ecosystem_lab/evidence/aggregation.py src/life_science_ecosystem_lab/evidence/change_detection.py src/life_science_ecosystem_lab/evidence/bundles.py src/life_science_ecosystem_lab/evidence/validation.py schemas/candidate-evidence.schema.json tests/test_aggregation.py tests/test_change_detection.py tests/test_bundles.py
git commit -m "feat: aggregate and compare evidence deterministically"
```

## Task 7: Add active state and immutable archive management

**Files:**

- Create: `src/life_science_ecosystem_lab/lifecycle/__init__.py`
- Create: `src/life_science_ecosystem_lab/lifecycle/state.py`
- Create: `tests/test_state.py`
- Create: `data/inputs/current/.gitkeep`
- Create: `data/inputs/archive/.gitkeep`
- Create: `data/state/.gitkeep`
- Create: `data/knowledge/.gitkeep`
- Create: `data/memories/.gitkeep`
- Create: `data/receipts/.gitkeep`

- [ ] **Step 1: Write failing state-transition tests**

Specify:

```python
def load_active_bundle(state_root: Path) -> CandidateEvidenceBundle | None: ...
def plan_state_transition(bundle: CandidateEvidenceBundle, roots: StateRoots) -> StateTransition: ...
def apply_state_transition(transition: StateTransition) -> None: ...
def verify_state_invariants(roots: StateRoots) -> ValidationReport: ...
```

Test:

- exactly one active snapshot per source identity
- byte-identical archive collision is idempotent
- different bytes at an existing archive identity fail deterministically
- archive files never enter the active digest
- archive traversal is impossible from active loaders
- path roots cannot escape the repository
- current replacement stages the previous current bytes into a date-partitioned immutable archive
- a failed transition leaves current and archive unchanged
- source deletion propagates into active state and knowledge candidates

- [ ] **Step 2: Run state tests and confirm failure**

```bash
python -m unittest tests.test_state -v
```

- [ ] **Step 3: Implement plan-then-apply transitions**

Generate every target and digest before replacing any active file. Use temporary files inside the target root and `Path.replace()` for final local atomicity. Do not delete pre-existing archive content

- [ ] **Step 4: Run state and full tests**

```bash
python -m unittest tests.test_state -v
python -m unittest discover -s tests -v
```

- [ ] **Step 5: Commit state management**

```bash
git add src/life_science_ecosystem_lab/lifecycle src/life_science_ecosystem_lab/lifecycle/state.py tests/test_state.py data
git commit -m "feat: add bounded active and archive state"
```

## Task 8: Add lifecycle validation, projection, receipts, and CLI surfaces

**Files:**

- Create: `src/life_science_ecosystem_lab/lifecycle/orchestrator.py`
- Create: `src/life_science_ecosystem_lab/lifecycle/guard.py`
- Create: `src/life_science_ecosystem_lab/lifecycle/projection.py`
- Create: `src/life_science_ecosystem_lab/lifecycle/receipt.py`
- Create: `schemas/lifecycle-manifest.schema.json`
- Create: `schemas/lifecycle-receipt.schema.json`
- Create: `tests/test_lifecycle.py`
- Create: `tests/test_projection.py`
- Create: `tests/test_cli.py`
- Modify: `src/life_science_ecosystem_lab/cli.py`
- Modify: `src/life_science_ecosystem_lab/__main__.py`

- [ ] **Step 1: Write failing projection tests**

Test canonical knowledge projection, deterministic memory summaries, dangling source references, duplicate entity keys, and exclusion of archives. Keep projections explicitly derived and rebuildable from active records

- [ ] **Step 2: Write failing lifecycle outcome tests**

Specify:

```python
def validate_candidate(bundle: CandidateEvidenceBundle, roots: StateRoots) -> ValidationReport: ...
def prepare_lifecycle_run(request: LifecycleRequest) -> LifecyclePlan: ...
def apply_lifecycle_plan(plan: LifecyclePlan) -> LifecycleReceipt: ...
```

Test all required outcomes:

- `VALIDATED_READ_ONLY`
- `NO_MEANINGFUL_DELTA`
- `APPLIED`
- `CONFLICTED_WORLD_LINE_NO_APPLY`
- `VALIDATION_FAILED`
- `SOURCE_UNAVAILABLE`

The apply function must require the validated source head SHA and an independently supplied current remote head SHA. A mismatch must not write

- [ ] **Step 3: Write failing CLI tests**

Add CLI contracts:

```bash
ls-ecosystem-lab evidence collect --sources ... --output ...
ls-ecosystem-lab evidence aggregate --input ... --topics ... --output ...
ls-ecosystem-lab evidence validate --bundle ...
ls-ecosystem-lab lifecycle validate --candidate ... --repository-root ...
ls-ecosystem-lab lifecycle apply --candidate ... --repository-root ... --validated-head ... --current-head ...
ls-ecosystem-lab state verify --repository-root ...
```

Test that all generated output stays under the supplied root and that existing pilot commands remain unchanged

- [ ] **Step 4: Run focused tests and confirm failure**

```bash
python -m unittest tests.test_projection tests.test_lifecycle tests.test_cli -v
```

- [ ] **Step 5: Implement projections, outcomes, receipts, and commands**

Receipts must include run identity, source and target heads, input and output digests, validation summary, changed allowlisted paths, outcome, and timestamps. Timestamps are provenance fields and must not influence semantic output digests

- [ ] **Step 6: Run focused and full tests**

```bash
python -m unittest tests.test_projection tests.test_lifecycle tests.test_cli -v
python -m unittest discover -s tests -v
```

- [ ] **Step 7: Commit lifecycle runtime surfaces**

```bash
git add src/life_science_ecosystem_lab/lifecycle src/life_science_ecosystem_lab/cli.py src/life_science_ecosystem_lab/__main__.py schemas/lifecycle-manifest.schema.json schemas/lifecycle-receipt.schema.json tests/test_projection.py tests/test_lifecycle.py tests/test_cli.py
git commit -m "feat: orchestrate bounded evidence lifecycle"
```

## Task 9: Implement the two GitHub Actions contracts

**Files:**

- Create: `.github/workflows/nexus-life-cycle.yml`
- Modify: `.github/workflows/validate.yml`
- Create: `scripts/check_write_boundary.py`
- Create: `scripts/verify_world_line.py`
- Create: `tests/test_workflow_contracts.py`
- Create: `tests/test_write_boundary.py`
- Create: `tests/test_world_line.py`

- [ ] **Step 1: Write failing workflow contract tests**

Parse YAML as text and narrow regular expressions because no YAML dependency is allowed. Assert:

- `workflow_dispatch` and daily schedule exist
- `validate` and `apply` jobs are distinct
- apply depends on validate
- permissions default to `contents: read`
- write permission exists only on the apply job
- concurrency group is explicit
- actions are pinned to full commit SHAs
- branch checkout is explicit
- candidate, state, projection, final validation, write-boundary, and world-line phases appear in the required order
- apply is gated on a stable meaningful candidate
- no secret other than `github.token` or `GITHUB_TOKEN` is referenced
- the last repository-mutating generation step is followed by final validation

- [ ] **Step 2: Write failing write-boundary and world-line tests**

Allow writes only under:

```text
data/inputs/current/**
data/inputs/archive/**
data/state/**
data/knowledge/**
data/memories/**
data/receipts/**
```

Explicitly reject `.github/**`, `config/**`, `schemas/**`, source code, tests, credentials, caches, and nested duplicated roots

Test clean, allowed, disallowed, deleted, renamed, and mixed diffs. Test equal and advanced remote-head cases

- [ ] **Step 3: Run focused tests and confirm failure**

```bash
python -m unittest tests.test_workflow_contracts tests.test_write_boundary tests.test_world_line -v
```

- [ ] **Step 4: Implement scripts and validation workflow**

Update validation to compile source and scripts, run all tests, validate profiles and metadata, perform deterministic double runs, check tracked and untracked caches, and verify a clean tree after tests

- [ ] **Step 5: Implement NEXUS lifecycle workflow**

Use the proven welcome/zero phase model but RS12 subject matter and paths. The workflow must:

1. check out the explicit branch with full history
2. validate runtime, profiles, and active state
3. collect GitHub evidence into a candidate staging root
4. aggregate and validate the candidate
5. project candidate knowledge and memories
6. run complete final validation
7. evaluate meaningful change
8. verify the allowlisted write boundary
9. verify the remote branch head still equals the validated head
10. commit only allowlisted generated files when meaningful and safe
11. emit a manifest and receipt before the final commit boundary

Do not use `skip ci` to avoid required validation. Prevent recursion through explicit path and actor conditions plus concurrency

- [ ] **Step 6: Run workflow contract and full tests**

```bash
python -m unittest tests.test_workflow_contracts tests.test_write_boundary tests.test_world_line -v
python -m unittest discover -s tests -v
python -m compileall -q src scripts tests
```

- [ ] **Step 7: Commit workflow implementation**

```bash
git add .github/workflows/nexus-life-cycle.yml .github/workflows/validate.yml scripts tests/test_workflow_contracts.py tests/test_write_boundary.py tests/test_world_line.py
git commit -m "feat: add guarded RS12 lifecycle workflow"
```

## Task 10: Add LifeMonitor, Workflow RO-Crate, and testing metadata

**Files:**

- Create: `lifemonitor.yaml`
- Create: `ro-crate/workflow/ro-crate-metadata.json`
- Create: `ro-crate/testing/ro-crate-metadata.json`
- Create: `metadata/bioschemas-workflow.jsonld`
- Create: `metadata/bioschemas-tool.jsonld`
- Create: `metadata/standards-status.json`
- Create: `tests/test_metadata_contracts.py`
- Modify: `examples/workflow-profile.json`
- Modify: `schemas/workflow-profile.schema.json`
- Modify: `src/life_science_ecosystem_lab/workflow_profile.py`

- [ ] **Step 1: Write failing metadata contract tests**

Verify:

- `lifemonitor.yaml` follows the current schema and tracks `main`
- `main` has `update_registries: false`
- release tags use `v*.*.*` with `update_registries: true`
- notifications are enabled only where intended
- Workflow RO-Crate has one main entity typed `File`, `SoftwareSourceCode`, and `ComputationalWorkflow`
- the main entity declares `programmingLanguage` and MIT license
- testing crate includes a `TestSuite`, a GitHub Actions test instance, `https://api.github.com`, and `repos/lostlight530/life-science-ecosystem-lab/actions/workflows/validate.yml`
- Bioschemas workflow and tool documents use released profiles and distinguish the orchestrator from the aggregator
- standards status uses only `prepared`, `submitted`, `accepted`, `published`, and `verified` evidence states
- WorkflowHub maturity uses `work-in-progress` or `stable`, never the pilot-only maturity vocabulary
- bio.tools eligibility remains `external-verification-required`

- [ ] **Step 2: Run metadata tests and confirm failure**

```bash
python -m unittest tests.test_metadata_contracts -v
```

- [ ] **Step 3: Implement the metadata package**

Do not create a fake executable CWL wrapper. The Workflow RO-Crate must describe the canonical GitHub Actions file accurately and register it as WorkflowHub `Other`; it must not claim CWL executability

Correct the existing workflow profile vocabulary so internal development status and WorkflowHub maturity are separate fields. Preserve compatibility by accepting the old profile only through an explicit schema-version migration test, not by silently conflating meanings

- [ ] **Step 4: Run metadata and full tests**

```bash
python -m unittest tests.test_metadata_contracts tests.test_workflow_profile -v
python -m life_science_ecosystem_lab validate-workflow-profile examples/workflow-profile.json
python -m unittest discover -s tests -v
```

- [ ] **Step 5: Commit metadata**

```bash
git add lifemonitor.yaml ro-crate metadata examples/workflow-profile.json schemas/workflow-profile.schema.json src/life_science_ecosystem_lab/workflow_profile.py tests/test_metadata_contracts.py tests/test_workflow_profile.py
git commit -m "feat: add LS workflow monitoring metadata"
```

## Task 11: Align citation, packaging, and repository documentation

**Files:**

- Modify: `README.md`
- Modify: `docs/SCOPE.md`
- Modify: `docs/PROVENANCE.md`
- Create: `docs/ARCHITECTURE.md`
- Create: `docs/STANDARDS.md`
- Create: `docs/OPERATIONS.md`
- Modify: `CITATION.cff`
- Modify: `pyproject.toml`
- Create: `tests/test_repository_metadata.py`

- [ ] **Step 1: Write failing repository metadata tests**

Assert title, package name, version, license, author identity, asset names, command examples, source boundary, and status claims agree across `README.md`, `CITATION.cff`, `pyproject.toml`, workflow profile, RO-Crate, and Bioschemas files

Verify the README clearly distinguishes:

- the lifecycle orchestrator
- the evidence aggregator
- the two existing pilot primitives retained for compatibility
- verified local capabilities
- prepared but externally unverified integrations

- [ ] **Step 2: Run the test and observe expected mismatches**

```bash
python -m unittest tests.test_repository_metadata -v
```

- [ ] **Step 3: Update documentation and packaging**

Document the two-asset system, exact source boundary, state layout, deterministic algorithm, failure modes, lifecycle outcomes, local commands, recovery procedure, and external-verification boundaries

Do not add marketing claims about AI, biological interpretation, clinical use, platform acceptance, or registry visibility

- [ ] **Step 4: Run documentation and full tests**

```bash
python -m unittest tests.test_repository_metadata -v
python -m unittest discover -s tests -v
```

- [ ] **Step 5: Commit documentation alignment**

```bash
git add README.md docs CITATION.cff pyproject.toml tests/test_repository_metadata.py
git commit -m "docs: document RS12 lifecycle and evidence tool"
```

## Task 12: Verify end-to-end determinism and repository hygiene

**Files:**

- Create: `tests/test_end_to_end.py`
- Create: `tests/fixtures/e2e/repository-state.json`
- Create: `tests/fixtures/e2e/expected-bundle.json`
- Create: `tests/fixtures/e2e/expected-receipt.json`
- Modify: `.gitignore`

- [ ] **Step 1: Write the end-to-end fixture test**

Use `FixtureGitHubTransport` to execute:

```text
profile validation
→ source collection
→ normalization
→ aggregation
→ candidate validation
→ projection
→ state-transition planning
→ guarded apply
→ final invariant verification
→ manifest and receipt verification
```

Run it twice into separate temporary roots and assert byte-identical semantic bundles and projections. Normalize only provenance timestamps in receipt comparison. Then mutate one fixture and assert a minimal explainable change set

- [ ] **Step 2: Run the end-to-end test and fix only exposed contract defects**

```bash
python -m unittest tests.test_end_to_end -v
```

- [ ] **Step 3: Run the complete local verification matrix**

```bash
python -m compileall -q src scripts tests
python -m unittest discover -s tests -v
python -m life_science_ecosystem_lab validate-source-registry profiles/sources.json
python -m life_science_ecosystem_lab validate-topic-registry profiles/topics.json
python -m life_science_ecosystem_lab validate-workflow-profile examples/workflow-profile.json
git status --short
```

Expected: compilation and tests pass, all validators exit `0`, and only intentionally changed tracked files appear before commit

- [ ] **Step 4: Enforce cache and generated-artifact hygiene**

Use one PowerShell process to inspect exact workspace paths. Remove only caches generated by this task after confirming their resolved paths are inside this worktree. Do not remove source data, credentials, database sidecars, or unknown temporary files

Verify no tracked or untracked `__pycache__`, `*.pyc`, `.pytest_cache`, temporary databases, build outputs, candidate staging roots, or generated receipts remain

- [ ] **Step 5: Commit end-to-end verification**

```bash
git add tests/test_end_to_end.py tests/fixtures/e2e .gitignore
git commit -m "test: verify deterministic RS12 lifecycle"
```

## Task 13: Perform final branch audit before any remote action

**Files:**

- Review only: all branch changes against the recorded baseline

- [ ] **Step 1: Re-read the applicable repository instructions and design constraints**

Confirm no project-level `AGENTS.md`, `AGENTS.override.md`, or `.specify/memory/constitution.md` appeared during implementation

- [ ] **Step 2: Inspect the complete change surface**

```bash
git status --short --branch
git diff --stat 23e104fdb92b4221a90e1ead745dfa2cd40b1c99..HEAD
git diff --name-status 23e104fdb92b4221a90e1ead745dfa2cd40b1c99..HEAD
git log --oneline --decorate 23e104fdb92b4221a90e1ead745dfa2cd40b1c99..HEAD
```

Reject unrelated frontend, Pages, archived-history rewrites, credentials, caches, lock files, dependency changes, or generated runtime state

- [ ] **Step 3: Repeat the final verification after the last write**

```bash
python -m compileall -q src scripts tests
python -m unittest discover -s tests -v
git diff --check
git status --short --branch
```

If verification creates files, clean only known generated files and repeat the complete final verification. Do not claim completion until the final run leaves the tree in the expected state

- [ ] **Step 4: Produce a release-readiness report without publishing**

Record:

- baseline and branch head SHAs
- implemented asset identities
- exact tests and results
- LifeMonitor and WorkflowHub metadata status
- conditional assets not implemented
- external verifications still required
- known risks and rollback method

Do not push, open a pull request, register with WorkflowHub, connect LifeMonitor, create a release, merge, or deploy without separate explicit authorization

