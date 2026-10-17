# Research software maintenance and publication boundaries

[Documentation index](README.md) · [Verification results](VERIFYING_RESULTS.md)

## Repository maintenance

- Pull requests: run code regression, offline CWL replay, graph JSONL reconstruction and Tool inspection tests before merging
- Periodic knowledge cycle: read only approved sources, verify source identities, build knowledge and graph projections, compare to active knowledge, accept verified meaningful changes only
- Independent Tool cycle: validate the installable CLI, test isolated third-party fixtures, audit local documentation and emit a reusable machine report
- Release review: reconcile `pyproject.toml`, `CITATION.cff`, CodeMeta, Bioschemas, RO-Crate, changelog and all public links to actual released functionality
- External integration: record registration/enrollment states as prepared, submitted, accepted or externally verified; never infer acceptance from CI

## Human-readable / machine-readable surfaces

| Human readers | Machine consumers |
| --- | --- |
| `README.md`, `docs/`, `.github/README.md`, `evidence/README.md` | `data/knowledge/*.jsonl`, JSON artifacts, RO-Crate, Bioschemas JSON-LD |
| Changes and reproducibility notes | Evidence JSON reports, receipts, SARIF and verified source identifiers |

User-contributed research proposals, including those produced using third-party Agents, remain untrusted until independently reviewed. There is no obligatory Agent package, Skills collection, model key or hidden run dependency.

## Safe operations

Scheduled and explicitly authorized main-branch runs may write only to `data/`; PR jobs are read-only. Any source registry expansion, workflow code change or new external registry claim requires normal code review. Published artifacts must not contain tokens, hidden policies, private research notes, or internal decision histories. Git history cannot be erased merely by deleting a tracked file.

The public repository documents **observable behavior** and how to reproduce it. It does not publish internal research planning, private collaboration strategies or unsupported claims. Do not include internal documents in Git, uploaded Actions artifacts, CI logs or PR descriptions.

## First native live-data acceptance drill

The first accepted-cycle request is intentionally a one-off `main` push trigger scoped to `evidence/field-tests/2026-10-17-first-accepted-cycle.json` and an exact merge-title prefix `ops: first-accepted-cycle-20261017`. It executes the **existing two-job Knowledge Workflow**, not a separate simulated producer: one `contents: read` job collects verified live sources and emits an Artifact; the second `contents: write` job verifies the expected main SHA, applies the guarded lifecycle, verifies the accepted knowledge/graph and writes only `data/`. Failed validation emits bounded source diagnostic artifacts without publishing upstream document text. The first-cycle trigger must be retired by removing `on.push` and the push clause after the real run; schedule and manually authorized dispatch remain.

**Scientific limitation:** an accepted Git commit is evidence that the software executed its specific source-linked computation and state checks, not that its topic matches constitute scientific truth. Approved source documents may be carried into accepted evidence state; review their licenses, notices, retention and replication before distributing derivative copies outside this repository.

## Execution and production checkpoints

- `candidate.run_id` / `receipt.snapshot_id`: content-derived snapshot identity, legitimately reused if upstream content is restored
- `receipt.execution_id`: unique execution attempt; GitHub runs use run ID and attempt ID, local invocations may provide their own bounded identifier
- `receipt.change_kind`: distinguishes first acceptance, profile changes, selected document changes and unchanged selected document text with revised provenance
- Before applying a new candidate, the lifecycle verifies the existing accepted state (including ledger and latest receipt linkage) and returns `EXISTING_STATE_INVALID_NO_APPLY` when it is damaged; it must not overwrite a broken baseline as though it were repaired
- Only canonical `YYYY-MM-DD` logical dates are valid for archive paths; candidate `run_id` must equal the digest-derived snapshot ID even if an attacker recomputes the JSON envelope digest
- After an accepted production operation, run `ls-knowledge state verify --repository-root . --require-accepted`. An empty bootstrap repository must not be described as accepted production state
- Before enabling writes, manually trigger a read-only workflow (`persist=false`) and examine diagnostics and `projection_eligible` from the artifact
- A public upstream source does not by itself authorize unrestricted republication. Before broadening inputs, review the source's license, data minimization and retention of copied text and artifacts

## Partial-observation gate

If an optional approved source fails at commit, tree, selected-document or blob retrieval, the collector discards that source's entire partial result and preserves an explicit diagnostic. Required sources missing all selected documents fail the collection rather than masquerading as an empty but successful observation. If an optional approved source cannot be retrieved, the Tool preserves an explicit diagnostic but marks the candidate as ineligible for automatic knowledge persistence. A transient missing source must not be silently converted into a document-deletion fact. The read-only artifacts remain inspectable for follow-up. Accepted graph snapshots and event chains are verified with repository state checks.
