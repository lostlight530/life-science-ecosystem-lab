# Public failure lesson · Frozen as-of tests must not reject valid native appends (2026-11-17)

[Source-scoped 868→889 Run/Job and Git replay](../provenance/POST_868_TO_889_RECONCILIATION_2026-11-17.md) · [Machine evidence](../provenance/post-868-to-889-observation-2026-11-17.json) · [November 10 original frozen report](../provenance/POST_798_TO_807_RECONCILIATION_2026-11-10.md) · [General failure atlas](2026-11-15-generalizable-research-software-failure-catalog.md) · [Offline falsifier](../../tests/test_post_868_run_delta.py)

## DEFINE · Claim, counterexample, competing explanations

**The failed claim** was implicit in `tests/test_post_798_run_delta.py`: because a November 10 GitHub evidence snapshot contained exactly **5 production Receipts, 5 chained Events and 4 previous-Candidate archives**, the **live** repository's `data/` must continue to have exactly that population. This conflates a frozen historical cardinality with an authorized append-only state machine. It is not a requirement of the scientific method or the source-identity contract.

**Falsifier observed:** the sixth native Knowledge Workflow [Run 43859884737](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43859884737) passed its `validate` and `apply` Jobs, wrote exact `data/` paths at [main `93d4cfb5`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/93d4cfb5f26c258880a92c700ad14192400a5b17), and appended `gh-43859884737-1` to the previously five-event hash chain. CI at [PR #79](https://github.com/lostlight530/life-science-ecosystem-lab/pull/79) subsequently failed the old assertion at line 105, reporting `(6, 5) != (5, 4)` after 290 tests, one failing test.

The evidence supports **test oracle temporal scope drift**. It does not support claiming a damaged Receipt, a malicious Agent write, broken GitHub scheduling, a new biological result, or an upstream registry failure. Verify these competing explanations independently rather than guessing a cause from the red badge.

## PIN / QUALIFY · Preserve both identities

| Identity | Historical as-of | Current verified Git state | Required rule |
| --- | --- | --- | --- |
| GitHub Run population | 807 at Nov 10, 868 at Nov 15 | 889 pre-repair Nov 17 | Date-source-pin; no live counter in frozen test |
| Receipt/event/archive population | 5 / 5 / 4 | 6 / 6 / 5 | Historical prefix immutable; native append permitted |
| Knowledge event hash | Five-event ledger Blob in old JSON | Six-event ledger Blob in current Git | Compare *exact first five line bytes* with old Blob SHA |
| Sixth accepted write | Not present at frozen cutoff | `gh-43859884737-1` APPLIED | Validate Receipt ↔ event ↔ prior archive ↔ accepted Git |
| Scientific result | 0 new verified claims | 0 new verified claims from this snapshot | Do not equate accepted source metadata with biology |

Git version, native run identity, candidate output digest, selected document content SHA, accepted event and Review decision must remain separate. The 15 selected source documents have unchanged content hashes despite upstream repository revision changes.

## EXECUTE / EVALUATE · Smallest evidence-preserving correction

- Keep the November 10 archive's `(5, 5, 4)`, latest event identity, latest Receipt identity and original Git Blob hashes exactly as written
- Slice the live `data/knowledge/events.jsonl` into its **first five original byte lines**, compute Git Blob SHA-1 and compare to the frozen five-line digest; verify the frozen fifth event and Receipt, not the live *last* event
- Permit `len(events) >= 5` under **independent** current `verify_state(require_accepted=True)` and the repository's `authorized_native_append_paths()` guard, which verifies every present Receipt ↔ Event identity, archive ancestry and permitted path set
- Keep structural relations `receipt count == event count` and `archive count == event count - 1`; don't replace a bad fixed `5` with an equally brittle fixed `6`
- Add an independent six-event source-scoped regression using the sixth event/Receipt original Blob identity, while leaving future seventh+ legal native append possible

This is an **offline verification test correction**, not permission to change the Knowledge Workflow, the Evidence/Bio implementations, `framework/` runtime, GitHub Actions schedule, external provider data, or formal `data/`.

## AUDIT / REVIEW · Preserve failed jobs and negative controls

The 21-run delta contains **4 failed parent Runs** and **5 failed latest-attempt Jobs**. The aggregate `validate` Job failed in addition to Repository contracts, while other independent domain Jobs succeeded. Bio `pinned-field` was **skipped** in a successful Push Run. A prior cancelled parent Run [43210854941](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43210854941) still contains a failed Repository contracts Job. None may be erased by a later passing CI attempt.

The user-facing draft PR can be reviewed only after its **own current head** passes required checks. Passing a separate Framework check does not override failing Repository contracts or independent Evidence Tool CI. A green offline suite is software-contract evidence, not human/organizational review and not a scientific finding.

## REPLAY · A portable research failure pattern

Use this sequence for any evidence-driven long-running system:

**Pin a historical as-of witness → classify immutable bytes vs legitimate mutable state → reproduce the exact failed assertion → keep the original witness → test historical prefix and current state as independent oracles → preserve the red Job → rerun the actual owning CI → record residual UNKNOWN.**

Avoid three anti-patterns: patching old numbers in historical JSON, changing formal source state to satisfy test fixtures, and suppressing required checks because the next native run has succeeded. The correct success criterion is **frozen evidence remains reproducible while legitimate future state transitions remain accepted**.

**Limits:** Repo-specific observation; no external provider object status, private Agent runtime attestation, biological truth or universal statistical reliability conclusion is established.
