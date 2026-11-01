# Public lessons: conditional Jobs and bounded evidence visibility · 2026-11-02

[Exact GitHub Run delta](../provenance/post-628-to-640-observation-2026-11-02.json) · [Audit and state boundary](../provenance/POST_628_TO_640_RECONCILIATION_2026-11-02.md) · [Independent replay](../../tests/test_post_628_run_delta.py) · [Historical negative evidence](../provenance/FAILURE_CAUSAL_REPLAY_2026-10-31.md)

Privacy-preserving lesson from public repository IDs, published logs and machine-readable Git evidence only; no private Agent prompts, original third-party datasets, personal contact records, credentials or sensitive payloads are reproduced.

## Failure modes, detection and correction

1. **Run Success masks conditional Job Skip.** A Bio Push Run can be green while `pinned-field` is `skipped`; its `offline` Job truly succeeded. Inspect the Run's Jobs array and each Job `conclusion` before claiming a real pinned-source scientific-data audit. Compare the PR event's separate successful `pinned-field` Job instead of filling the gap with inferred success.

2. **A transient or inaccessible log is not a failed run.** GitHub Jobs API recorded `skipped` for Job `124835593035`, but a log retrieval returned `BlobNotFound/404`. Preserve both the readable Job status and the failed log read with cause `UNKNOWN`. Never rewrite `skipped` to `failure`, invent the missing traceback or infer that missing bytes were deleted by an actor.

3. **Repeated event-trigger CI is not repeated science.** Six intermediate branch pushes, three PR checks and three merged-main checks produced 12 distinct successful Run IDs. They are engineering observations attached to specific source commits, not twelve accepted research executions. The formal accepted-state denominator remains exactly three Receipts and three chained events.

4. **An immutable observation needs exact identity, not just a new total.** A 628-to-640 API count can conceal losses if old IDs disappear. Compare all 628 archived IDs and report missing IDs explicitly. In this observation the intersection is 628, the missing set is empty and the added set contains 12 unique IDs; old JSON archives remain frozen.

5. **A warning and an unverified root cause remain visible.** Current Runner messages warn about Node.js 20 actions being run under Node.js 24, while observed relevant Jobs still succeed. The prior November 1 API-to-log one-hour clock discrepancy is not resolved merely because subsequent Jobs passed. Keep warnings, clock sources and causal uncertainty separate from functional failures.

6. **Different registry versions have separate owners.** A GitHub v0.5.0 Release and a WorkflowHub listing of v0.4.0 do not by themselves imply corrupted synchronization. Record the source, object identifier, release/update clock and platform-specific publication status; report current full cross-platform parity as `UNKNOWN` unless directly verified.

## Minimal falsifiable replay

The accompanying offline test reads the frozen 598-row root census, the next 16 and 14 rows and this 12-row observation, checks uniqueness, total counts, triggers, the 35/54 scheduled Job denominator, newest Job outcomes, three accepted Receipts/events and ten Git Blob identities from local file bytes. It does not perform network calls or infer biological validity.

**Scientific boundary:** `NO_NEW_VERIFIED_CLAIM` · **Operational decision:** `NO_CHANGE_REQUIRED` for three science assets, Framework, Actions and accepted `data/` · **Public record:** append-only, source-pinned and reviewable.
