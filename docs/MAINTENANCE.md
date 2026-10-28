# Research software maintenance and publication boundaries

[Documentation index](README.md) · [Verification results](VERIFYING_RESULTS.md)

## Repository maintenance

- Pull requests: run code regression, offline CWL replay, graph JSONL reconstruction and Tool inspection tests before merging
- Periodic knowledge cycle: read only approved sources, verify source identities, build knowledge and graph projections, compare to active knowledge, accept verified meaningful changes only
- Independent Tool cycle: validate the installable CLI, test isolated third-party fixtures, audit local documentation and emit a reusable machine report
- Release review: reconcile `pyproject.toml`, `CITATION.cff`, CodeMeta, Bioschemas, RO-Crate, changelog and all public links to actual released functionality
- External integration: record registration/enrollment states as prepared, submitted, accepted or externally verified; never infer acceptance from CI
- Cross-platform byte contracts: keep root `.gitattributes`, fixture digests and Linux/Windows Framework checks aligned; a Linux-only green result is insufficient for exact-byte portability

## Human-readable / machine-readable surfaces

| Human readers | Machine consumers |
| --- | --- |
| `README.md`, `docs/`, `.github/README.md`, `evidence/README.md` | `data/knowledge/*.jsonl`, JSON artifacts, RO-Crate, Bioschemas JSON-LD |
| Changes and reproducibility notes | Evidence JSON reports, receipts, SARIF and verified source identifiers |

The machine-readable external-state authority is `metadata/standards-status.json`. Human-readable summaries must not silently outrun it, and private dashboard observations must remain distinguishable from public registry verification

User-contributed research proposals, including those produced using third-party Agents, remain untrusted until independently reviewed. There is no obligatory Agent package, Skills collection, model key or hidden run dependency.

## Safe operations

Scheduled and explicitly authorized main-branch runs may write only to `data/`; PR jobs are read-only. Any source registry expansion, workflow code change or new external registry claim requires normal code review. Published artifacts must not contain tokens, hidden policies, private research notes, or internal decision histories. Git history cannot be erased merely by deleting a tracked file.

Required PR validation is contributor-neutral. Human contributors, Codex, Jules and external GitHub Apps submit through the same read-only contract jobs; maintainers must not add `github.actor` bypasses or blanket `continue-on-error`. External institutions and registries are observers rather than merge prerequisites, so their authentication, uptime and acceptance state must not be placed in required local CI

The four validation domains run independently and retain bounded diagnostics even when another domain fails. Only their aggregate verdict represents admission to the reviewed repository state. This isolation does not weaken production authority: native apply still depends on successful native validation and retains its existing world-line and `data/` write boundary

The public repository documents **observable behavior** and how to reproduce it. It does not publish internal research planning, private collaboration strategies or unsupported claims. Do not include internal documents in Git, uploaded Actions artifacts, CI logs or PR descriptions.

## Native production operation

The native Knowledge Workflow is intentionally **manual/scheduled only**. Manual dispatch may select only a profile registered in `evidence/profiles/workflow-profiles.json`; an isolated profile remains read-only. A manual `native` run is authorized through GitHub Actions on `main` with `persist=true`; otherwise the dispatcher runs read-only. The schedule always resolves `native` and retains guarded acceptance. See [Production Operations](PRODUCTION_OPERATIONS.md) for separate evidence levels and the post-push remote-HEAD verification.

After collection, the read-only validation job passes an immutable source + knowledge Artifact to the write job. The write job verifies both the validated Git SHA and the current remote main world-line before applying, checks candidate/knowledge/graph/receipts, stages only `data/`, verifies the remote SHA again, and pushes. A **post-push** verification confirms the actual remote main ref equals the local accepted commit. Any failure is not accepted production.

Failed validation uploads **diagnostics and docs-audit reports only**, when available. No private inputs or raw upstream document text are added to that failure-report Artifact. Real public upstream source content may be included in accepted `data/` snapshots under the established provenance policy, subject to source copyright/license review.

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

## Peer Framework maintenance and merge authority

The independently installed Framework has its own tests and Linux/Windows checks; this does not make its results interchangeable with Knowledge Workflow, Evidence Tool or Bio Tool outputs. The dedicated [synthetic challenge](../framework/docs/CONTRACT_CHALLENGE.md) must be reproducible and retained as a candidate, not transformed into accepted biological knowledge

Cross-domain engineering changes should identify which interface version, input bytes, method declarations, error/abstention conditions and independent domain-specific checks were examined. Baselines and oracle expectations must be versioned and revisable. Negative outcomes and missed detections belong in the report, not in an ignored CI log

### Branch protection is a separate authority plane

As observed via the public GitHub branch metadata on 2026-10-25, `main.protected=false` and no active repository rulesets were returned by the available read. This is a point-in-time repository-governance observation, **not** a property of any workflow or permission to bypass checks

The GitHub-native `validate` aggregate check fails when an internal domain fails, but that fact **alone does not prove** that GitHub's server will reject a direct push or PR merge. A maintainer with repository administration authority should separately enable and verify the intended branch protection/ruleset, including required status contexts, review policy and privileged bypass rules. The current connected GitHub App cannot modify repository administration settings. Do not mark that work completed from a passing Actions run

Any maintenance PR that changes source declarations, metadata or documentation should preserve the frozen `v0.4.0` release identity and distinguish the later experimental Framework package version `0.1.0`; never rewrite old registry records to include new software retroactively

## Documentation-only research-governance reviews

A claim-review or cross-infrastructure provenance correction may tighten **review expectations** without modifying executable capabilities. Cold-start from current remote main, enumerate proposed changed files and protect the following existing production and executable contracts when the change is explicitly documentation-only: .github/workflows/, .github/runtime/, .github/knowledge/, evidence/, bio_tool/, framework/src/, framework/tests/, data/, registered source/topic profiles, frozen release metadata and CI fixtures.

A prose policy must not silently create a new parser status, mandatory CI check, model/Agent runtime dependency, external login, data acceptance gate or repository writer. A research method described in Markdown is not implemented software until an actual independently tested and reviewed change supplies that capability.

Review repeated observations according to their **actual changes**, not the number of tasks executed:

- Identical relevant evidence: use the existing no-meaningful-delta or no-findings discipline; do not generate a research event to maintain a streak
- Source revision changed but selected content did not: retain the revision and avoid claiming a new scientific finding
- Source text, scientific method or reference changed: re-evaluate the affected claim with pinned versions and a method-specific comparator
- Required source, control or comparator unavailable: preserve a bounded blocked/indeterminate report, not a fabricated negative scientific result
- New independent counterevidence: retain the previous version, correction, dissent and responsible human review
- Third-party catalog and monitor disagree: compare original field and observation times without rewriting accepted production data or the external account

For external standard updates, pin the generic RO-Crate version, specific Workflow/Testing/Run profile, JSON-LD term mappings and consumer behavior **as separate review objects**. Do not retroactively migrate archived v0.4.0 crates, DOIs or accepted receipts merely because a newer upstream version exists.

A documentation-only merge record should include base/head SHAs, exact changed-file inventory, official reference URLs and observation dates, CI outcomes, final main SHA and remaining unknowns. Green documentation CI establishes consistency of these public contracts, **not** a newly certified scientific result.
