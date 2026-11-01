# Public lessons: Run identities, temporal clocks and accepted research state · 2026-11-01

[Source-graded delta](../provenance/POST_614_TO_628_RECONCILIATION_2026-11-01.md) · [Machine snapshot](../provenance/post-614-to-628-observation-2026-11-01.json) · [Offline falsifier](../../tests/test_post_614_run_delta.py) · [Earlier negative evidence](../provenance/FAILURE_CAUSAL_REPLAY_2026-10-31.md)

This note contains only public technical identities and privacy-minimized results, not user profiles, raw external scientific files, model prompts, private communications, private Agent identity, credential material or arbitrary Runner log bodies

## Reusable failure modes and repairs

1. **Total-count equality is weaker than identity equality.** A previous observation had 614 visible Runs; the next had 628. We checked the *set of all prior 614 IDs* against seven live API pages before concluding 14 new Runs. An unchanged counter could instead hide disappearing and newly created IDs
2. **A green Run is not an executed biological field analysis.** Bio Run `41213974054` completed successfully while the `pinned-field` Job was conditionally skipped. Reconcile Job statuses and event gating, rather than applying the whole-Run conclusion to every scientific action
3. **Native continuity is not a new production acceptance.** Three new scheduled Jobs on November 1 verified institutional/public references, eleven project checks and the existing accepted Knowledge state. They did not produce a fourth `APPLIED` Receipt or new biology result
4. **Clocks are separate measurements.** The self-check Run API reports `09:10:05Z` whereas its Runner log lines are prefixed around `08:10Z`. Preserve both source readings, label the discrepancy, and leave its cause `UNKNOWN`. Cron-to-Run-created intervals must never be relabeled actual queue wait times
5. **Historical red remains meaningful.** Eight failures preserved in the earlier 531-Run archive, 134 per-run name corrections and two recalculated medians survive the latest clean live population. A vanished API record is not evidence of who deleted it or whether it was malicious
6. **A GitHub Release is not cross-registry acceptance.** GitHub `v0.5.0` points to current source main, but new GitHub publication does not update WorkflowHub, LifeMonitor, Zenodo, bio.tools or OpenEBench by implication. Their identities, versions, actual API records and review states must be independently checked

## Eight-stage transfer

**DEFINE** a bounded identity/quality question → **PIN** prior immutable observations and main SHA → **QUALIFY** Git/Run/Job/Artifact/Receipt clocks separately → **EXECUTE** the complete API census and inspect actual Job logs → **EVALUATE** set deltas, denominators, medians, skipped steps and negative results → **AUDIT** retain disagreements and past failure evidence → **REVIEW** a read-only source-backed PR with independent CI → **REPLAY** normalized JSON offline without changing production state

**Disposition:** publish a dated provenance and regression increment only; leave scientific assets, Framework, native schedules and accepted `data/` untouched. The open explanation of the November 1 clock mismatch is a real research uncertainty, not a license to infer failure or change the scheduler
