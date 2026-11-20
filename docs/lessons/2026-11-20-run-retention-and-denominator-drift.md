# Public failure lesson · Run retention changes the visible denominator, not historical outcomes (2026-11-20)

[Source-pinned 889→915 audit](../provenance/POST_889_TO_915_RECONCILIATION_2026-11-20.md) · [Machine Run/Job witnesses](../provenance/post-889-to-915-observation-2026-11-20.json) · [Unmodified November 17 failed-Run archive](../provenance/post-868-to-889-observation-2026-11-17.json) · [Earlier frozen/live oracle correction](2026-11-17-frozen-history-vs-live-accepted-state.md)

## DEFINE → PIN

**Falsifiable claim:** a larger current GitHub Actions Run count and a green current dashboard might seem to show that the earlier four failed Runs have been fixed or never existed. A durable observer must test Run identities, not subtract two dashboard totals.

The November 17 *frozen* source enumerated **889 unique Run IDs, including four failures**. The November 20 *currently visible* API enumerated **915**, of which **864 success / 51 cancelled / 0 failure**. The source main and latest Run-created cutoff are fixed in the adjoining audit. The four historical failure IDs were directly re-queried and each returned HTTP 404; individual API responses do not attest deletion attribution or intent.

## QUALIFY → EXECUTE → EVALUATE

Set reconciliation, based on exact IDs and separately frozen cutoffs:

```text
frozen IDs (889)
  minus old IDs no longer visible (4, historically failed)
  plus post-frozen new IDs (30, each currently successful)
  = current visible IDs (915)
```

The 30 new parent Runs contain **63 latest-attempt Jobs: 62 successful, one conditionally skipped**. The skip is the Bio `pinned-field` Job of a successful Push Run; the Workflow condition explicitly excludes the field Job on ordinary Push. Meanwhile, the current scheduled subset contains **76 Runs and 118 latest-attempt successful Jobs**: institutional and project self-checks, continuity, weekly Knowledge and weekly Bio are separate time bases and must not be collapsed into “76 experiments”.

The count of `failure` **in the current API population** is zero. The count of historically **observed failures in the dated source** remains four. These are different estimands, and neither an observed deletion nor a later passing check changes the historical verdict.

## AUDIT → REVIEW → REPLAY

**Failure mode:** treating a retention-sensitive API list as a monotonic append-only ledger, then claiming fewer failures or greater reliability without joining immutable Run IDs and source timestamps.

**Portable correction:** retain an append-only, privacy-limited independent ledger that stores original Run/attempt/Job identities, historical conclusions, exact source cutoff and explicit absences on later re-query. Use offline consistency tests for the frozen record, and independently validate current accepted state from live Git and its Receipts. Do not make an old snapshot unit test assert that the current Run API must forever contain the same set, or that future authorized `data/` appends are illegal.

**Negative controls:** [cancelled Run `43210854941`](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43210854941) retained a failed Repository contracts Job, while [successful Run `43266573648`](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43266573648) retained a skipped Bio Job. Parent conclusion, child conclusion, historical visibility and production acceptance are orthogonal. The earlier November 17 frozen-test failure is already explained in its own separate causal lesson; do not count repeated red badges as different defects without a causal test.

**Explicit nonclaims:** no claim about the technical deletion actor or reason is deduced from HTTP 404; no complete runner-log recovery, universal CI availability, scientific result, provider registry certification, or biological validity is proven. Private reports and identifying context are not part of this public source-scoped evidence.

**Reusable invariant:** A historical outcome remains an observation with its original time and evidence identity, even if a provider no longer serves that Run. A later recovery or disappearing dashboard record does not rewrite history
