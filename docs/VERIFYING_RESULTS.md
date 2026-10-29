# Understanding verification results

This project's independent Workflow, two Tools and separate experimental Framework produce **bounded engineering evidence**, not clinical/biological correctness or external platform certification. Determine *exactly which artifact, version, command and check* supports a statement.

For an end-to-end **read-only replay with negative controls and claim-level review fields**, see [Cross-asset evidence replay](EVIDENCE_REPLAY_PROTOCOL.md). For cross-service identity, version and standards compatibility, see [Interoperability review](INTEROPERABILITY_REVIEW.md). These guides add no new executable guarantee.

## Six independent evidence surfaces

| Evidence level | Observable result | Does **not** establish |
| --- | --- | --- |
| Local Tool inspection | JSON + optional Markdown and SARIF, PASS / WARN / FAIL | A scientific conclusion, remote website reachability, full standards conformance |
| Evidence collection/aggregation | Approved source revision, object identity, digests, diagnostics, candidate eligibility | The scientific meaning of the source documents is correct |
| Computational knowledge replay | Deterministic knowledge JSON, source-linked JSONL and FTS5 queries on a specific input | That the synthetic fixture is a live GitHub observation or causal inference |
| Bio Tool data audit | Deterministic protein FASTA amino-acid composition and ambiguity counts, or first-model PDB observed C-alpha residue inventory, plus input SHA-256 | Sequence correctness, folding accuracy, molecular geometry, biological interpretation or clinical suitability |
| Independent Framework assessment | Exact local-byte check, method-domain declarations, typed lineage findings and synthetic adversarial cases | That method execution actually occurred, a biological sample was identified, or a scientific claim was accepted |
| GitHub native durable lifecycle | Completed scheduled/authorized job **plus** accepted `data/` commit and state verification | That third-party registries accepted or independently reproduced the software |

## Required pull-request verdict

The required validation workflow starts four independent domains on every pull request and `main` push: `Repository contracts`, `Knowledge Workflow`, `Evidence Tool` and `Portable package`. Their diagnostic artifacts use failure-safe upload steps, but the checks themselves are not allowed to continue on error. The aggregate `validate` check preserves the existing required-check name and succeeds only when all four domain results are `success`

A failed domain does not cancel or skip the other domains, so one run can expose multiple independent defects. A canceled workflow is not converted into a passing verdict. No contributor identity, GitHub App or Bot account receives a bypass. External service reachability and registry acceptance remain outside this required local verdict

Framework changes additionally run the independent `standalone-framework` Linux check and `windows-cross-platform` check. The Windows check is evidence that repository line-ending policy preserves exact fixture bytes and deterministic output; it does not expand the required aggregate verdict or claim scientific portability

## Framework evidence levels and strict abstention

`ls-framework assess` defaults to exit 0 for `PASS` **or** `INDETERMINATE`; an abstention is not an affirmative verification. The optional `--require-pass` returns exit 2 for `INDETERMINATE` and 1 for `FAIL`, allowing downstream automation to refuse incomplete evidence. The JSON `status` and `not_verified` fields are authoritative within the narrow engineering contract, not scientific truth.

The independent Framework's two JSON-reporting entrypoints write via temporary sibling files and replace the destination only after the new report has been flushed. In an ordinary failed write or failed replacement, this avoids truncating an existing complete report; no claim is made about power-loss durability or concurrent writers. The output path still passes the existing refusal guard, and reports remain local engineering evidence rather than accepted production state.

The Framework metric `declared_cross_domain_steps` counts distinct-domain crossings across the **union of each step's input and output assets**, including a one-input transformation. It does not count verified executions: a failed or unknown declared step may still contribute to this descriptive metric, while the report retains an `INDETERMINATE` outcome and the relevant warning. For outcome interpretation, prefer `status`, `errors`, `warnings` and `not_verified` over a metric name alone.

Both `ls-framework assess` and `python -m ls_framework.challenge` use the shared report-path guard. It rejects destinations replacing the input bundle, lying inside the selected input evidence root, or targeting a discovered Git checkout's `data/` / `.git/`. Git roots are discovered from ancestors of the current working directory, input root, bundle and destination, including when launched from a checkout subdirectory. This is a refusal guard, **not** a general filesystem sandbox; other output paths and concurrent filesystem races remain outside its assurance. See [independent Framework assurance](../framework/docs/ASSURANCE.md).

## Tool report decisions

`ls-evidence inspect` returns **0** for PASS or WARN; **1** for FAIL; **2** for invalid usage or inspect errors. The static preflight now distinguishes root `CITATION.cff` from recognized alternative citation guides (`CITATIONS.md`, `CITATION.md`, `CITATION.txt`); finding a guide remains WARN rather than an unsupported CFF PASS. A service repository is not required to include a workflow's root RO-Crate metadata. Nested crates are not assessed by the root-level rule. Read the `status`, `findings`, `scope` and `unverified` keys in the JSON report instead of assuming exit code 0 means scientific verification. Do not report `WARN` as certified success.

`ls-evidence audit-docs` checks pinned **local Markdown links**. The listed external URLs are inventory records and are **not** confirmed reachable. It returns an error if a local link is missing, unsafe or unsupported.

## Graph claims and reproducibility

The current JSONL graph is a deterministic projection of the verified source-cited knowledge map. `SOURCE_MATCH` means a topic matched a source document; it does not prove an empirical relation. The SQLite FTS5 index is built in memory at query time and is not a second authoritative datastore.

```sh
ls-knowledge graph verify --dir build/graph --knowledge build/replay/knowledge.json
ls-knowledge graph search --dir build/graph --query workflow --limit 5 --hops 1
```

To reproduce the query, preserve the exact knowledge input and the `entities.jsonl`, `relations.jsonl` and `graph-manifest.json` outputs and record the repository commit. For accepted main-branch graph events, the append-only event-chain verification is included in state checks. Accepted receipts distinguish per-attempt `execution_id`, content-addressed `snapshot_id` and `change_kind`, so restoring an earlier source snapshot does not reuse an earlier event or receipt. `DOCUMENT_TEXT_UNCHANGED` is a selected-text comparison, not a proof of new scientific knowledge.

Prior-state validation happens **before** any accepted apply, including when the new evidence is unchanged. An invalid old ledger, current snapshot or latest receipt produces `EXISTING_STATE_INVALID_NO_APPLY`, not a new success or an implicit repair. Logical dates are validated as canonical calendar dates and snapshot IDs are bound to their input/profile digests.

An independently reconstructed [three-run native continuity field audit](NATIVE_CONTINUITY_FIELD_AUDIT.md) shows why two committed `DOCUMENT_TEXT_UNCHANGED` events are not equivalent to `NO_MEANINGFUL_DELTA`, and why a new upstream Git revision need not imply altered selected text or scientific novelty. The October 19 metadata-only acceptance remains an open policy/implementation question, not a confirmed defect.

## Native workflow reading guide

1. Check the GitHub Actions event: PR/push CI, synthetic CWL replay, manual observation and scheduled persistence are different events
2. Inspect `build/workflow-profile.json`; confirm the profile ID, authority, source/topic paths and SHA-256 values. Only `native` is persistence-eligible
3. Confirm the expected source revision and GitHub run conclusion
4. Inspect `build/source-diagnostics.json`, `projection_eligible`, and machine-readable reports
5. For durable claims, verify an actual accepted `data/` commit, current knowledge and associated receipts; **no-change, failed or conflicted runs are not new knowledge production**. `ls-knowledge state verify --repository-root . --require-accepted` rejects an empty bootstrap tree, while the ordinary state command checks only any state currently present. The strict check also binds the latest accepted graph event to the active evidence candidate, so a valid but substituted candidate cannot pass as the accepted state.
6. Treat WorkflowHub, LifeMonitor and bio.tools as externally verified states only when a genuine registry or monitoring record exists

[Getting Started](GETTING_STARTED.md) · [Provenance](PROVENANCE.md) · [Maintenance](MAINTENANCE.md)

## Cross-version knowledge review

`ls-evidence audit-knowledge` performs an offline and bounded structural audit. Its digest and graph checks are not independent extraction verification: a newly recalculated digest can authenticate the bytes of a fabricated fragment without authenticating the external passage. Use `knowledge verify` with the fixed candidate and topic registry for source-text derivation, then separately review scientific relevance. The optional labeled set measures selection performance only on precisely those supplied cases; an unlabeled run returns null precision/recall. Source revision changes with unchanged selected text never imply scientific novelty.

A separate read-only `life-science-continuity.yml` schedule can observe accepted Git state without acquiring write permission. Its success proves a single check at the recorded Git revision, not multiple-week production durability. The original production lifecycle alone owns allowed `data/` writes.

## Research claim decisions are not executable verdicts

The [research claim review contract](RESEARCH_METHODOLOGY.md) distinguishes software correctness, evidence integrity, method suitability and scientific validity. Passing one does **not** imply the others.

| Evidence available | Defensible statement | Not supported by that evidence |
| --- | --- | --- |
| One CLI check and its regression tests pass | The named software behavior passed at the identified code/input revision | The method is suitable for every research question |
| Git object, digest and path match | The specified bytes and provenance are internally consistent | The source author's biological interpretation is true |
| A domain-specific controlled comparison succeeds | A bounded metric was observed against a named reference and protocol | Generalized accuracy or independent replication outside the sample |
| Two Agent narratives agree | Their written assertions agree within the stated window | Authenticated independent runtimes or scientific consensus |
| A workflow or software registry shows a version | A platform exposed that record at a dated observation | Peer review, scientific approval or authorization for sensitive data |
| Two catalog/monitor response fields differ | A dated comparison found a difference | Importer failure or loss of the upstream data |

For quantitative evidence retain numerator, denominator, unit, observation window, sampling criteria, nulls and missingness, uncertainty and excluded attempts. A reported zero is not interchangeable with missing or unavailable data. Preserve negative controls, abstentions and contradictory evidence.

Human-review prose such as **PROPOSED**, **ENGINEERING_VERIFIED**, **SCIENTIFICALLY_EVALUATED**, **REVISED**, **NO_FINDINGS** and **BLOCKED** does not add executable status values. Actual CLI, CI and native production outcomes remain defined by the existing machine reports and Git receipts. A PR merge accepts a code/document change, not automatically every scientific assertion in its discussion.

See [cross-infrastructure provenance reconciliation](PROVENANCE.md) for a two-clock upstream/downstream procedure. An inaccessible external API during a documentation review is an unresolved observation, not proof the service is offline.
