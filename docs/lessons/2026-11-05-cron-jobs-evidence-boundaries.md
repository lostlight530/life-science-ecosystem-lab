# Public lesson · successful Runs do not imply every Job ran (2026-11-05)

[Exact 721→730 Run/Job evidence](../provenance/post-721-to-730-observation-2026-11-05.json) · [Interpretation](../provenance/POST_721_TO_730_RECONCILIATION_2026-11-05.md)

**Scheduling attribution:** 2026-11-04 daily and continuity schedules succeeded but were created +06:19:20 and +07:58:47 after their nominal UTC cron. Preserve separate clocks for cron intent, API Run creation, actual Job start and project logical date. No GitHub outage, measured queue latency or missed execution follows from these differences alone.

**Conditional non-execution:** Bio `push` Run 41779069740 passed with `offline=success`, `pinned-field=skipped`, by the Workflow's event condition; the PR's Bio Run 41778963873 had `pinned-field=success`. The correct proof unit is **Run ID + attempt + Job ID + versioned event guard**, not just the green workflow badge.

**Retained negative evidence:** three earlier reported failing Run IDs returned 404 again despite the current 730 visible Run objects having zero visible failures. An unavailable API object is not a zero failure count for the historical observation or evidence about its deletion cause. Preserve dated archives and correction history.

**Scientific boundary:** the 255-commit Git chain records software lineage; the four accepted Knowledge Receipts record controlled state transitions. Neither guarantees original scientific correctness, four biological discoveries, or external registry approval.

**Repair procedure:** reconstruct prior identity sets, fetch all current result pages, compare IDs, fetch Jobs and artifact identities, calculate UTC clock differences from versioned YAML, retain unknowns and old failures, append a source-pinned observation, and run a minimal offline test. Do not change production `data/`, native schedule or scientific claims to make the report look complete.
