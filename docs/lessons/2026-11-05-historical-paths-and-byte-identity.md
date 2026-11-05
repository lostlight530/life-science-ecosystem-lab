# Public research lesson · historical-only paths are not missing production files (2026-11-05)

[Full first-day-to-main register](../taxonomy/full-file-lifecycle-2026-11-05.json) · [Human-readable evidence audit](../taxonomy/FULL_FILE_LIFECYCLE_2026-11-05.md) · [Corrections](../taxonomy/CORRECTION_REGISTER_2026-11-03.md)

**Failure mode — only inspecting today's tree.** A 294-file `main` snapshot cannot represent every past file path. Replaying the 256 main-reachable commits' 235 distinct Git Trees revealed **47 historical-only paths**, so the observed union contains **341 path identities**. This does not measure 341 scientific outputs or prove the full set of paths in inaccessible unmerged branches.

**Failure mode — inferring a rename from a similar name.** At 19 witnessed older paths, the exact Git Blob SHA reappears at a different current path. That independently proves identical bytes at those two pinned versions. For 28 other historical paths there is no same-SHA match in the current tree; this does *not* prove deletion of the software feature or rule out a rewritten successor. Keep `HISTORICAL_ONLY`, `BYTE_IDENTICAL_CURRENT_PATH`, and `UNKNOWN_SEMANTIC_SUCCESSOR` distinct.

**Failure mode — resurrecting retired contracts.** Public history shows `.lifemonitor.yaml` was removed under a nonstandard-config correction and the mixed `tests/test_daily_selfcheck.py` was replaced by isolated test suites. Blind restoration would reintroduce obsolete conventions, not repair a missing asset. The old `src/`, `workflow/`, `profiles/` and early planning documents remain recoverable as Git evidence without becoming new production files.

**Failure mode — treating changed guidance as falsified archives.** Ten living files differ from a dated frozen classification Blob SHA; record both identities and the later change, never rewrite the source-pinned historical register. The four native `APPLIED` events remain independent of this documentation exercise.

**Reproducible method:** pin `main` and root, enumerate all reachable Commit/tree identity pairs, de-duplicate equal trees, enumerate complete non-truncated blobs at each tree, compare path membership to the current tree, record historical witness Commit/Tree/Blob, check exact-byte matches separately, and publish additive source-scoped observations through tested PR review. Preserve failure, unresolved provenance and external provider authority boundaries.
