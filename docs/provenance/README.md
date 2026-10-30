# Frozen 2026-10-30 GitHub provenance census

[Full origin-to-present history](../REPOSITORY_HISTORY_AND_PROVENANCE.md) · [Open claims](../CLAIM_VERIFICATION_GAPS.md) · [Provenance and authorities](../PROVENANCE.md)

**Observed:** `2026-10-29T16:24:03.499Z` UTC / 2026-10-30 Asia/Shanghai · **Reference main:** [`05ab6b2dc98dfe13581b5ae1bedcd11a58dbbb77`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/05ab6b2dc98dfe13581b5ae1bedcd11a58dbbb77)

This is a **project-authored, non-production, read-only GitHub API observation**, not an official GitHub archive certification or a life-science result. GitHub API paging was read while the `main` SHA was checked unchanged. It uses public records only, with no private credentials, original CI logs, private third-party observations, or full upstream copyrighted source bodies.

| Immutable JSON snapshot | API surface | Fixed count |
| --- | --- | --- |
| [`commits-2026-10-30.json`](commits-2026-10-30.json) | `/repos/lostlight530/life-science-ecosystem-lab/commits?per_page=100&page=1..3` | 234 reachable main commits, SHA + parent edges + dates + subjects |
| [`pull-requests-2026-10-30.json`](pull-requests-2026-10-30.json) | `/repos/lostlight530/life-science-ecosystem-lab/pulls?state=all&per_page=100&page=1` | 42 PR objects, 40 merged, #29 and #32 closed without merge |
| [`action-runs-2026-10-30.json`](action-runs-2026-10-30.json) | `/repos/lostlight530/life-science-ecosystem-lab/actions/runs?per_page=100&page=1..6` | 531 visible workflow runs, 483 success / 8 failure / 40 cancelled |

Every JSON includes `observed_at_utc`, `reference_main_sha`, `source_urls`, `returned_count` and explicit `provenance_limit`; unique IDs and the parent-closed main DAG are checked in the independent [offline archive test](../../tests/test_repository_provenance_archive.py). These files are stored under `docs/provenance/`, **not** the production-authoritative `data/`.

## Later append-only reconciliation · 2026-10-30

The initial three JSON objects above are frozen at the original cutoff and **must not** be overwritten. The [subsequent reconciliation](RECONCILIATION_2026-10-30.md) and [daily run quality](NATIVE_DAILY_QUALITY_2026-10-30.md) add versioned observations rather than editing those observations. New complementary files:

- [History delta](history-delta-2026-10-30.json): one additional main commit and PR #43, resulting in 235 commits / 43 PRs on the pre-update main
- [Later 531-run compact index](actions-visible-index-2026-10-30.json): no actor identity fields, each unique visible run with observed event/date/status
- [Set reconciliation](action-run-reconciliation-2026-10-30.json): eight previous failures absent from new API results, eight newer runs, three separately classified lower-grade observations
- [Daily native quality ledger](native-daily-quality-2026-10-30.json): 15 Shanghai calendar days and 28 scheduled-run Job checks, with accepted Knowledge writes distinguished from read-only checks
- [Offline reconstruction test](../../tests/test_provenance_observation_reconciliation.py): verifies both snapshots and the derived daily schedule without network access
- [Privacy-minimized methodological lessons](../lessons/2026-10-30-error-detection-and-audit.md): falsifiable error classes and evidence tier boundaries

A current API total is an observation-specific count, not an all-time verdict. Missing run records are **not** evidence of a specific deletion actor or motive.

## Offline, read-only repeat

~~~sh
python -m unittest discover -s tests -p test_repository_provenance_archive.py -v
python - <<'PY'
from pathlib import Path
import json
base = Path("docs/provenance")
for name in ("commits", "pull-requests", "action-runs"):
    data = json.loads((base / f"{name}-2026-10-30.json").read_text())
    print(name, data["observed_at_utc"], data["returned_count"])
PY
~~~

This reproduces the **archived structural census**, not historical network calls, final truth of self-attributed Agent identities, continuous live CI monitoring, independent scientific experiments or original expired artifacts. To check a later reality, use the documented original URLs and record a **new** UTC observation with old and new values, rather than replacing the old snapshot.

Source distinctions: Git commits are version objects; PRs are proposed/reviewed changes (including unmerged negatives); Actions are particular CI/scheduled/manual runs; the three production `data/receipts` are **distinct accepted Knowledge events**; WorkflowHub, LifeMonitor, Zenodo, bio.tools and OpenEBench own separate external objects and clocks. Never combine their counts into a fabricated scientific KPI.

**Known omissions:** inaccessible branches/forks, deleted or unavailable runs, expired Actions artifacts, private account records, unverified February predecessor sources, third-party API responses unavailable during this session, all future runs and the publishing PR itself. The snapshot is a dated lower-scoped observation of **what GitHub returned**, not a permanent full reconstruction of every unpublished operation.

[Native accepted-state evidence](../NATIVE_CONTINUITY_FIELD_AUDIT.md) · [External interoperability](../INTEROPERABILITY_REVIEW.md)

## Independently reviewed erratum for the second observation

The [historical workflow-name and median erratum](RUN_NAME_AND_MEDIAN_ERRATUM_2026-10-30.md) documents **134 mislabeled compact-index rows** from collapsing different run names under one workflow ID, and corrects two reported schedule medians. The original index remains unchanged; the [new per-run source-graded correction](run-name-attribution-audit-2026-10-30.json) must be used when a historically precise workflow name is required.

## Post-merge 547-run observation and append-only numerical corrections

The [post-merge record](POST_MERGE_RECHECK_2026-10-30.md) (source main `56ac4a9065d8f0ff60da6eadadfdbe44a2d26615`, observed 2026-10-30 01:57:45 UTC) reconciles the existing 531-index to **547** visible Run IDs with **16 new successes and zero missing previous IDs**. Preserve the original contradictory historical failure census. The [machine JSON delta](post-merge-observation-2026-10-30.json) stores exact new IDs with public Git SHAs, events and status but no actor details. The [append-only statistical projection](native-quality-corrections-2026-10-30.json) recalculates the two originally incorrect medians from the complete 28-row schedule source rather than editing that original JSON. [Public methodological experience](../lessons/2026-10-30-evidence-census-and-runtime-quality.md) and [offline regression](../../tests/test_post_merge_evidence_delta.py) document the limitation that success, accepted production state and scientific validity are different objects. This is **project-owned research**, not an external platform or institutional endorsement.

## Later completed October 30 schedule observation

The [post-schedule read-only closeout](POST_SCHEDULE_OBSERVATION_2026-10-30.md) was observed **after** the three scheduled jobs for the local October 30 calendar date returned. It pins pre-review main `5da107dfe8521fbf2a1a2f5653ce6aea23bfc1dc`, reconciles the 547 previous Run IDs with 563 currently visible IDs (**16 new, 0 missing in this specific comparison**), and independently verifies the observed 31 scheduled workflow results against **48 successful Jobs**. Current visible outcomes were 522 success, 41 cancelled and no currently visible failure; the earlier frozen eight failures must **not** be erased. The new report also preserves Bio's `WARN_UNCERTAIN_RESIDUES`, nominal-cron versus API-created-time differences, three unchanged accepted Knowledge Receipts, and current external-object retrieval limitations. All original frozen API snapshots and correction artifacts remain unchanged; this page is an index, not accepted `data/`.

### Offline 563-run identity replay (post-schedule additive evidence)

The subsequent [16-run machine delta](post-schedule-observation-2026-10-30.json) and [independent offline replay test](../../tests/test_post_schedule_provenance_replay.py) check the 531 → 547 → 563 **exact unique Run-ID population**, outcomes and trigger totals, the 28 + 3 observed scheduled Runs, 43 + 5 observed scheduled Jobs, and four independently re-sorted cron-versus-`created_at` medians. The [post-schedule narrative](POST_SCHEDULE_OBSERVATION_2026-10-30.md) remains the human-readable companion. The precise original post-schedule API-request time was not saved, so the JSON explicitly uses `observed_at_utc: null`; it does not invent a timestamp or retroactively modify the frozen source observations. The re-fetched source fields do not attest to deleted run history, runner-log byte retention, scientific accuracy or a new accepted `data/` event.

```sh
python -m unittest discover -s tests -p 'test_post_schedule_provenance_replay.py' -v
```
