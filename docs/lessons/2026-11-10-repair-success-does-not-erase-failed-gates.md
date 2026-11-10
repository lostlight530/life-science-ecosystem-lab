# Public lesson · repair success does not erase failed gate evidence (2026-11-10)

[Bounded reconciliation](../provenance/POST_798_TO_807_RECONCILIATION_2026-11-10.md) · [Machine ledger](../provenance/post-798-to-807-observation-2026-11-10.json) · [Offline falsifier](../../tests/test_post_798_run_delta.py)

**Observed failure mode:** PR #71 initially exposed stale offline assumptions about a moving accepted-state ledger and valid native append paths. Four failed GitHub Runs were recorded after the prior 798-Run cutoff. After a bounded repair, later checks passed, the PR merged, and those four failed Run endpoints subsequently returned 404.

**Correction method:** preserve the failed IDs, their previously observed gate meaning and the exact repair head in additive evidence. Verify the repair with new PR and merged-main Jobs. Never rewrite the older report, convert a missing Run into a success, or claim that a green final head proves the branch never failed.

**Scientific boundary:** these were repository-history regression failures, not corrupted accepted research data, a failed protein computation or a biological counter-result. Current formal state remains five Receipts, five events and four archives, with no new scientific claim.

**Clock and provider boundary:** GitHub API visibility can change. A later 404 proves only that the endpoint is unavailable at the later observation. Without provider evidence, deletion, retention expiry, cleanup actor and platform cause remain **UNKNOWN**.

**Reusable rule:** evaluate original failure, repair and final acceptance as separate objects. Green successor evidence can validate a correction while the original negative evidence remains part of the audit trail.
