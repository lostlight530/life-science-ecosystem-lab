# Source-scoped native schedule quality and post-merge reconciliation · 932 → 939 · 2026-11-23

[Machine-readable observation](post-932-to-939-schedule-quality-2026-11-23.json) · [Public lesson](../lessons/2026-11-23-schedule-time-observability.md) · [Independent offline regression](../../tests/test_post_932_schedule_quality.py) · [Prior 915→932 archive](POST_915_TO_932_RECONCILIATION_2026-11-22.md)

## DEFINE / PIN · Exact boundary

- **Source main**: [`e5997e4221b6218d0315db9f146c33b289d6f8d7`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/e5997e4221b6218d0315db9f146c33b289d6f8d7), merged PR [#83](https://github.com/lostlight530/life-science-ecosystem-lab/pull/83); repository Git root `00009a38bc136a7c245270770b005e4e102a870d`.
- **Previous frozen visible-population cutoff**: 932 Runs through `2026-11-22T12:40:38Z`; source main `36cd0b14...`. Preserve the preceding JSON and failed-Run history without rewriting.
- **This observation's latest Run**: `2026-11-22T15:06:26Z`. Logical review day **2026-11-23 Asia/Shanghai**, not an assertion that UTC November 23's expected scheduled executions have completed.
- No live third-party provider, production science or actor identity is inferred from GitHub source alone.

## QUALIFY / EXECUTE · What actually changed

| Bounded measure | Prior visible | Current visible | Delta |
| --- | ---: | ---: | ---: |
| Run IDs | 932 | **939** | +7 |
| Successful parents | 881 | **888** | +7 |
| Cancelled parents | 51 | **51** | 0 |
| Currently visible failed parents | 0 | **0** | 0 (not historical absence) |
| Push / PR / schedule / dispatch | 469 / 376 / 83 / 4 | **473 / 379 / 83 / 4** | +4 / +3 / 0 / 0 |
| main-reachable Commit objects | 325 | **327** | +2 |
| Tracked Blob paths / recursive tree entries | 347 / 398 | **350 / 401** | +3 / +3 |
| PRs | 82 | **83** | +1 |

Net count difference **does not prove identity-set equality** of the old 932 and current 939. However **all seven** newly created Runs after the preceding cutoff were individually joined to latest-attempt Jobs, and all seven belong to the already merged PR #83 (not new native research production). These seven have 16 successful Jobs and one documented Bio main-Push `pinned-field=skipped` (Job `137251151786`). Neither a new Bio field result nor a new Knowledge Receipt follows from these changes.

### Seven exact post-cutoff Run / Job witnesses

| Run ID | Event | Created UTC | Jobs | Latest attempt |
| --- | --- | --- | ---: | --- |
| [45036269933](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/45036269933) | `push` | `2026-11-22T15:04:36Z` | 1 | Verify evidence CLI, source contracts and docs=success |
| [45036293705](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/45036293705) | `pull_request` | `2026-11-22T15:04:52Z` | 1 | Verify evidence CLI, source contracts and docs=success |
| [45036293717](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/45036293717) | `pull_request` | `2026-11-22T15:04:52Z` | 5 | Evidence Tool=success; Portable package=success; Knowledge Workflow=success; Repository contracts=success; validate=success |
| [45036293819](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/45036293819) | `pull_request` | `2026-11-22T15:04:53Z` | 2 | offline=success; pinned-field=success |
| [45036444609](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/45036444609) | `push` | `2026-11-22T15:06:26Z` | 5 | Evidence Tool=success; Portable package=success; Repository contracts=success; Knowledge Workflow=success; validate=success |
| [45036444668](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/45036444668) | `push` | `2026-11-22T15:06:26Z` | 2 | offline=success; pinned-field=skipped |
| [45036444708](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/45036444708) | `push` | `2026-11-22T15:06:26Z` | 1 | Verify evidence CLI, source contracts and docs=success |

## EVALUATE · Full currently visible native scheduled population

83 `schedule` Run IDs from **2026-10-17 through 2026-11-22 UTC** were re-enumerated, with 129 latest-attempt scheduled Jobs independently checked as Success. **No expected scheduled date is missing within each workflow's observed first-to-last date span**. Separate per-Run UTC clock identities, outcomes, schedules and exact missing-day logic are frozen in the JSON and offline regression.

| Workflow | Scheduled Runs | Cron UTC | Median created-minus-Cron | Observed range | Missing dates inside observed span |
| --- | ---: | --- | --- | --- | ---: |
| daily_selfcheck | 36 | `41 1 * * *` | 06:28:50 | 04:47:10–08:03:13 | 0 |
| continuity | 37 | `17 4 * * *` | 07:18:45 | 04:21:07–09:19:15 | 0 |
| knowledge | 5 | `23 3 * * 1` | 08:01:14 | 05:40:15–08:23:49 | 0 |
| bio | 5 | `19 2 * * 5` | 07:06:25 | 05:14:21–07:42:33 | 0 |

Medians of an even-sized cohort take the mean of two central observations. These are **API Run created time − nominal same-UTC-date cron**, not queue duration. A separately read Daily Run `45004651729` has `created_at == run_started_at == 2026-11-22T08:50:12Z`; this does **not** expose internal event-delivery or dispatch delay. No cause of the observed large offsets is established. GitHub's [official scheduled-workflow troubleshooting](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows) describes delayed or dropped scheduling **as a generic possibility**, not verified root-cause attribution here.

## AUDIT / REVIEW · Accepted production and nonclaims

Re-read from `main`: six consecutive accepted `APPLIED` events, six Receipt identities with matching Event output digests and checked adjacent previous-event references, 17 graph entities and 26 SOURCE_MATCH relations. The last accepted execution is `gh-43859884737-1` on 2026-11-16, `DOCUMENT_TEXT_UNCHANGED`. No seventh formal accepted Event, independent scientific replication, biological discovery, institutional registration or scientific claim promotion observed.

Four historic failed Run IDs (`43919536363`, `43919549660`, `43919549686`, `43919549907`) continue to return individual 404 on current inspection; previous frozen records survive. Separate historic cancelled parent `43210854941` contained failed Repository contracts Job `131157765073`. Neither is overwritten by the current 0 failed **visible parent** count.

**What was *not* checked:** original missing logs; 129 scheduled Job IDs as a frozen complete list (reviewed independently but only count archived here); all original SHA-256 bytes; inaccessible live external-provider registry states; all event-delivery clocks; proof of current-day missing Runs before the observation window closes. Repository branch protection is **not** changed or treated as part of this remediation.

## REPLAY · Safe disposition

`SCHEDULE_CLOCK_OBSERVED / RUN_JOB_DELTA_PINNED / NATIVE_SCHEDULE_SUCCESS / PRODUCTION_UNCHANGED / ROOT_CAUSE_UNKNOWN / NO_CRON_CHANGE / NO_SCIENTIFIC_CLAIM`

Run `python -m unittest discover -s tests -p 'test_post_932_schedule_quality.py' -v` at the merged tree to independently replay identities, cohort counts, exact 83-date cron offsets, expected-day continuity, Event prefix and historical negatives without network or external model. Software CI success only validates this bounded audit.
