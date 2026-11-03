# Public research lesson · native success does not imply universal execution (2026-11-03)

[Fixed source population](../provenance/post-653-to-673-observation-2026-11-03.json) · [Reconciliation and scopes](../provenance/POST_653_TO_673_RECONCILIATION_2026-11-03.md) · [Prior frozen-history failure correction](2026-11-02-frozen-history-vs-live-state.md) · [Offline falsifier](../../tests/test_post_653_run_delta.py)

**Reproducible observation:** a read-only GitHub census preserved all 653 previously archived Run IDs, returned 20 additional successful PR-related Runs, and found no new scheduled Run or production Receipt by the observation cutoff. Individual latest-attempt Jobs for those new Runs totalled 36 success and **2 skipped**; the two skipped `pinned-field` Jobs were in merged-main Bio push checks, while corresponding PR jobs had actually executed. Separately, **38 scheduled Runs carried 59 successful Jobs**.

**Failure mode 1 — wrong aggregation grain:** counting a successful Bio Run as evidence that every conditional Job executed misstates testing coverage. Always retain `Run → Job → Step`, event filters, exact Run/Job IDs, and the distinction between a successful offline suite and a skipped pinned external-source field check.

**Failure mode 2 — moving API mistaken for historical truth:** the 673 currently visible API results have zero failures, but an older source-pinned observation legitimately recorded eight failures. Three later PR #55 interim failures are separately documented and currently return 404 individually. Neither zero currently visible failures nor 404 tells who removed or retained an earlier Run; preserve negative evidence and its original observation denominator.

**Failure mode 3 — conflating creation clocks:** the November 3 daily cron had no visible Run at the early observation cutoff, after prior runs had large cron-to-created offsets. Record `NOT_YET_VISIBLE` and the cutoff instead of reporting a scheduler defect. `created_at` does not measure queue duration; an assembled report timestamp does not certify the individual HTTP request instants.

**Failure mode 4 — mistaking CI policy for server authority:** independent CI checked repository contracts, while GitHub reported an unprotected main branch and no public rulesets. Required tests and server-enforced branch protection are different controls. Never claim the latter from the former.

**Correction method:** pin an immutable prior Run-ID set, re-fetch all pages, compare identity sets before comparing totals, independently read actual Jobs, verify accepted Git/Receipt/event state through native integrity checks, and append the new observation without rewriting older witnesses. The remaining unknowns are the exact request clock, historical unavailable-run mechanism, scheduler offset cause, and external registry parity.

**Falsifier:** `python -m unittest discover -s tests -p test_post_653_run_delta.py -v` reconstructs the fixed population and checks that native live `data/` still validates, but does not claim that local test execution replays GitHub's original network/CI history. No scientific conclusion, source registry, DOI, release or automatic production event was created for this report.
