# Universal research-software engineering lessons · 2026-10-16 to 2026-11-15

> Reviewed, project-owned synthesis from the repository's origin-to-current history. This does not replace dated evidence, original failure records, correction registers or scientific data.
>
> DEFINE → PIN → QUALIFY → EXECUTE → EVALUATE → AUDIT → REVIEW → REPLAY. Evidence before claims. Preserve failures, uncertainty, disagreement and provenance.

## 1. Scope and reuse boundary

This handbook consolidates reusable methods from the repository's evolution across Git identity, PR disposition, Actions execution, historical reconstruction, file governance, production state, Knowledge Workflow, Evidence Tool, Bio Tool, experimental Framework, external Agent collaboration, institutional services, publication metadata and scientific claim boundaries. Protein FASTA/PDB, protein-structure workflow and knowledge graph are replaceable examples, not the permanent research objective. This is a project-authored engineering reference, not an institutional standard, certification, novelty claim or scientific result.

## 2. Identity and authority: never collapse evidence grains

| Object | Establishes | Does not establish |
|---|---|---|
| Commit / Tree / Blob | Versioned source identity | Experiment or scientific result |
| PR | Proposal and merge disposition | Accepted feature unless merged to selected base |
| Agent self-description | Claimed actor/contribution | Authenticated runtime identity |
| Actions Run | One workflow execution and attempt | All Jobs executed or scientific success |
| Job / Step | Nested execution result | Whole-system or research validity |
| Artifact | Run-associated output | Durable state unless committed and verified |
| Candidate / Proposal | Unaccepted input | Formal knowledge or production fact |
| Receipt / Event | Execution-specific acceptance evidence | Independent scientific replication |
| Accepted data state | Durable project-owned state | Truth of a biological claim |
| SOURCE_MATCH | Deterministic topic/document match | Biological or causal relation |
| Tool QA | Bounded software/input behavior | Scientific model validation |
| Provider record | Provider-owned object at a time/version | Local authority, endorsement or synchronization |

Every report names object grain, source, version, time basis, status and nonclaim.

## 3. Historical failure and correction catalogue

### 3.1 Origin and actor attribution

Failure: predecessor engineering, private scheduled tasks, public Git history and repository ancestry are collapsed into one origin story. Lesson: derive origin from the actual Git root and parent closure; describe predecessor work as external lineage. PR titles, commit subjects and conversation do not authenticate private Agent runtime.

### 3.2 PR disposition

Failure: all closed PRs counted as merged; branch-only files treated as main content; closed-unmerged proposals called scientific rejections. Lesson: preserve original number/title and distinguish OPEN, CLOSED_UNMERGED and MERGED using state, merged_at, base/head SHA and merge SHA. Closed-unmerged means disposition, not acceptance and not necessarily scientific rejection.

### 3.3 Run identity, names and clocks

Failure: Run names treated as stable identity; UTC, Shanghai logical date, cron and created_at mixed; historical names rewritten to match current YAML. Lesson: identify execution by Run ID, attempt, workflow path, head SHA, event and created/started/completed timestamps. Preserve observed names. A cron-to-created_at gap is an observation, not a causal explanation.

### 3.4 Run success concealing failed Jobs or skips

Failure: parent success means every Job executed; cancelled means all failed or harmless; skipped counted as pass; attempts mixed. Lesson: descend Run → attempt → Job → Step. A cancelled parent may contain a failed Job; a successful parent may contain a skipped Job. Distinguish success, failure, cancelled, skipped, neutral, timed_out, action_required and unknown. Use logs where available; expired logs permit only bounded reconstruction from pinned historical Trees and invariant test/workflow Blobs.

### 3.5 Historical API absence

Failure: an old Run absent from today's API is said to be deleted by a named actor or never existed; current zero visible failures refutes an older snapshot. Lesson: freeze each returned population with observed_at, query, page count, IDs, URLs and omissions. Reconcile by set difference. Missing means unavailable in this observation, not a deletion explanation. Preserve archived failures.

### 3.6 Historical tests coupled to mutable state

Failure: old commit Tree compared against today's mutable manifest or remote state. Lesson: pin historical head SHA, Tree, manifest Blob, test Blob and workflow Blob. Live-state integrity is a separate current test. Never rewrite frozen evidence to make an old assertion pass.

### 3.7 Inventory completeness and path admission

Failure: nested Markdown omitted; direct-child globs assumed recursive; new root-level files bypass reviewed additive families; tests weakened to accept them. Lesson: specify path scope exactly, enumerate governed documents, register every public Markdown path, and review root-level additions separately. Correct inventory or add narrow classification; do not widen allowlists casually.

### 3.8 Naming, classification and cleanup

Failure: filenames cosmetically renamed, old records overwritten, similar paths assumed duplicates, generated-looking files deleted without authority checks. Lesson: use a stable category overlay and dated names for new snapshots. Preserve old paths and byte identities. Classify by primary responsibility, role, evidence authority and retention. Deletion requires positive proof that an item is disposable and not a receipt, fixture, archived failure, replay input or historical witness.

### 3.9 Blob equality and semantic successors

Failure: byte-identical content at a new path automatically called a rename; similar paths imply update; absence from main treated as cache deletion. Lesson: record byte identity separately from semantic relationship. Rename detection is heuristic absent explicit history. Git-tracked cleanup does not inspect Actions caches, artifacts, forks, private branches or local scratch.

### 3.10 Green CI and server policy

Failure: green CI presented as proof branch protection, required reviews or server-side merge gates are enforced. Lesson: CI and repository policy are separate control planes. Inspect branch protection/rulesets independently. A passing check is not required unless repository policy says so.

### 3.11 Schedule and conditional execution

Failure: local clock slot interpreted as scheduler dispatch; UTC cron read as local time; conditional skip counted as execution. Lesson: derive schedules from workflow YAML, use UTC for GitHub cron, map logical timezone separately, inspect conditions, and classify expected-but-skipped Jobs explicitly. created_at is not the scheduler dispatch instant.

### 3.12 Knowledge delta and formal persistence

Failure: unchanged source text means no state change; provenance-only commit described as new science; candidate generation treated as production acceptance. Lesson: distinguish content, source revision, metadata, candidate, graph projection and accepted-state deltas. Acceptance requires guarded write path, execution-specific Receipt, append-only Event, validated snapshot and Git world-line continuity.

### 3.13 Hashes and state continuity

Failure: schema validity or one digest proves all files agree; event head accepted without predecessor check. Lesson: validate schema, canonical serialization, file digest, manifest linkage, event sequence, previous-event digest, snapshot/source identity and current Tree together. Hashes prove byte integrity under a scheme, not scientific truth or source authenticity by themselves.

### 3.14 SOURCE_MATCH semantics

Failure: topic/document matches described as biological relations, causality or discovery. Lesson: SOURCE_MATCH means configured topic matched a source document under a deterministic rule. It is not entity resolution, causality, consensus or scientific validation.

### 3.15 Agent proposal and review

Failure: schema pass described as fact verification; consensus becomes truth; self-identified Agent gains write authority; review and acceptance merged. Lesson: separate proposal, observation, validation, review, authorization, acceptance and publication. Agents may investigate and challenge but cannot self-approve truth or production writes. Preserve disagreement and negative evidence.

### 3.16 Asset boundaries

Failure: Knowledge Workflow, Evidence Tool and Bio Tool merged into one pipeline; Framework described as a fourth mature biological asset; Actions counted as research products. Lesson: preserve three peer research-software assets with independent entry points, tests and responsibilities. Framework remains a separate experimental software-contract asset; Actions are native infrastructure.

### 3.17 Bioinformatics scope

Failure: FASTA composition, ambiguous-residue warnings or PDB C-alpha inventory presented as structure prediction, folding validation, geometry verification or function inference. Lesson: report only what implementation directly observes. Record input digest, parser/version, model/chain/residue selection, warnings and limitations. Clean parsing is not molecular correctness.

### 3.18 External metadata and institutional services

Failure: source metadata update described as downstream sync; directory entry as approval; login as resource authorization; DOI and release clocks mixed. Lesson: maintain provider-owned state per service with object ID, version, observation time, response and access boundary. Distinguish submitted, saved, visible, curated, indexed, synchronized and accepted.

### 3.19 Metrics and badges

Failure: n/a becomes zero citations; downloads become users; views become adoption; provider counts combined. Lesson: retain metric definition, unit, source, observation window, deduplication and coverage. Missing is not zero. DOI, badge, profile or registration does not imply usage, endorsement or impact.

### 3.20 Release clocks and correction integrity

Failure: GitHub Release, Python package, Framework, registry and DOI treated as synchronized; reports silently edited; later success erases earlier failure. Lesson: keep version clocks and immutable identifiers separate. Append corrections with original claim, corrected claim, reason, source, scope, date and residual uncertainty. Never rewrite frozen snapshots.

## 4. Eight-stage operating contract

- DEFINE: state one falsifiable question, object scope, non-goals, decision and scientific/software boundary; specify a falsifier.
- PIN: freeze Commit/Tree/Blob, provider object/version, Run/attempt/Job, dataset checksum, tool version, schema, clock and cutoff; record query and omissions.
- QUALIFY: check authority, completeness, temporal comparability, permissions, privacy, schema, input integrity and limitations; mark UNKNOWN rather than filling gaps.
- EXECUTE: use least privilege, deterministic steps, pinned inputs, bounded resources and explicit write guards; keep external Agents separate from native authority.
- EVALUATE: compare declared criteria and prior baseline with identical units/population; separate software correctness, evidence validity, method applicability and scientific truth.
- AUDIT: inspect nested Jobs/Steps, logs, failures, skips, cancellations, warnings, data writes, permissions, provenance and contradictions.
- REVIEW: independently challenge source identity, assumptions, causal attribution, claims, path classification and authorization; record disagreement.
- REPLAY: replay pinned inputs independently where feasible; state what was replayed and what cannot be recreated.

## 5. Required evidence envelope

Every material report identifies: claim ID and exact wording; claim class; source authority; observation time/timezone; version and source IDs; input checksum; method/parameters; expected result and falsifier; actual result including warning/failure/skip/unknown; independent validation; authorization/persistence state; replay boundary; correction history; explicit nonclaims.

## 6. Naming and classification convention

- New dated lessons: docs/lessons/YYYY-MM-DD-short-topic.md
- New dated provenance: docs/provenance/YYYY-MM-DD-short-topic.md or established POST cutoff-to-cutoff form
- New taxonomy inventory: docs/taxonomy/scope-YYYY-MM-DD.json with human-readable explanation when needed
- Corrections append to correction register or dated erratum; never overwrite frozen snapshots
- Link from relevant index and register every public Markdown path in evidence/profiles/docs.json
- Do not rename paths for style; classify by role and evidence authority
- Preserve original case and established filename families

## 7. Primary classification vocabulary

KNOWLEDGE_WORKFLOW; EVIDENCE_TOOL; BIO_TOOL; EXPERIMENTAL_FRAMEWORK; GITHUB_NATIVE_INFRASTRUCTURE; ACCEPTED_PRODUCTION_STATE; HISTORICAL_PROVENANCE; PUBLIC_RESEARCH_LESSONS; AGENT_PROPOSAL_AND_REVIEW; SCIENTIFIC_FIELD_CASE; OFFICIAL_REFERENCE_OBSERVATION; PROJECT_CUSTOM_CHECKS; EXTERNAL_INTEROPERABILITY_AND_IDENTITY; VALIDATION_AND_REGRESSION; PUBLIC_GOVERNANCE_AND_METHOD; REPOSITORY_GOVERNANCE; BUILD_AND_REPOSITORY_CONFIG. Each file has one primary category. Multiple workflow uses do not justify duplicate identities.

## 8. Retained correction families

The original correction register and dated reports remain authoritative for incident detail. This synthesis retains origin/Agent attribution; Git/PR/Run/Job/Receipt grain; closed-unmerged PRs; asset/Framework/Actions identity; nested Markdown omissions; living-index versus frozen-snapshot confusion; stale totals; Run-name and median errata; historical failures missing from current API; temporary branch checks; mutable-live-state coupling; structural placeholders; SOURCE_MATCH semantics; Agent proposal authority; bounded FASTA/PDB QA; provider/identity/DOI/release clocks; cancelled parents containing failed Jobs; and successful repairs that do not erase prior failures.

## 9. Pre-write gate

- [ ] Pin main SHA and Tree immediately before branching
- [ ] Inspect open PRs, target paths and current Blob identities
- [ ] Confirm every new path belongs to an approved family
- [ ] Register every public Markdown path in docs manifest
- [ ] Keep formal data, assets, Framework runtime and Action schedules unchanged unless separately authorized
- [ ] Preserve historical evidence and negative records
- [ ] Run offline regression and documentation audit
- [ ] Inspect PR diff against exact intended paths
- [ ] Require independent review and CI before merge
- [ ] Explain skipped Jobs; never label them pass
- [ ] Merge only after required gates and explicit authority

## 10. Nonclaims

This synthesis is not a replacement for incident-specific evidence. It does not reconstruct every historical Tree, private Agent run, expired artifact, inaccessible branch, external provider state or local untracked file. It changes no formal data, software asset, Framework runtime, Action schedule or scientific conclusion.
