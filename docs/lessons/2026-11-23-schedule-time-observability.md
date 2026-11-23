# Public research lesson · Schedule-time observability without scheduler causality (2026-11-23)

[Source-pinned 932→939 review](../provenance/POST_932_TO_939_SCHEDULE_QUALITY_2026-11-23.md) · [83 Run clock witness](../provenance/post-932-to-939-schedule-quality-2026-11-23.json) · [Offline regression](../../tests/test_post_932_schedule_quality.py)

## DEFINE → PIN

**Problem:** native GitHub `schedule` Run `created_at` is frequently hours after its nominal UTC cron clock. This is a **time-of-observation** issue requiring independent monitoring, not an established scientific data failure. Pin `main` at `e5997e4221b6218d0315db9f146c33b289d6f8d7`, the exact nine workflow definitions and the GitHub Run ID and timestamp for each of 83 currently visible scheduled runs. Prior frozen 932 Run census ends 2026-11-22 12:40:38 UTC.

## QUALIFY → EXECUTE → EVALUATE

Reconstruct clock differences as `Run.created_at UTC - nominal Cron on the same UTC calendar day`. Check that the event is `schedule`, classify by actual workflow, and check each expected day **only between that workflow's first and last visible scheduled date**. Verify the Run outcome and separately the latest-attempt Job outcomes. Do **not** turn a partly elapsed current-day observation into a missed-run claim.

Across the 83 visible scheduled Runs: Daily 36, Continuity 37, Weekly Knowledge 5, Friday Bio 5. The inspection observed 129 successful latest-attempt Jobs, with no missing expected days within the four observed date spans. Offset medians: Daily **06:28:50**, Continuity **07:18:45**, Knowledge **08:01:14**, Bio **07:06:25**. The clock records are replayable offline; the 129 individual scheduled Job IDs are **not** frozen in this addendum, so their aggregate has a narrower replay boundary.

GitHub [official troubleshooting documentation](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows) allows that scheduled events can be delayed at high-load periods, and [schedule-event documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) distinguishes scheduled intent from actual trigger. These are **possible platform mechanisms**, not an attribution of this repository's observed delays. The observed jobs succeeded, but that does not prove deadline or upstream data-cutoff compliance.

## AUDIT → REVIEW → REPLAY

- Use four distinct identities where available: nominal UTC Cron (intent), Run `created_at` (API object), Job `started_at` (runner), production logical/observation cutoff and Receipt (scientific state). Here **Job start clocks are not exhaustively archived**.
- Check Run ID + attempt + Job ID; a successful parent may contain `skipped` children, and a cancelled parent may contain a failed Job.
- Preserve earlier four historical failure IDs even when their individual REST reads return HTTP 404, without assuming who removed them.
- Keep institution-reference self-checks separate from project-custom observations. Do not shift Cron merely to make displayed offsets smaller, infer availability, or bypass validated Knowledge apply to compensate for delays.
- GitHub protections, approval policy, external platforms, source registries, active Workflow schedules and formally accepted `data/` remain unchanged.

**Disposition:** `CLOCK_DRIFT_OBSERVED / SCHEDULER_CAUSE_UNKNOWN / NATIVE_JOBS_SUCCESS / ACCEPTED_DATA_UNCHANGED / MONITORING_REPLAYABLE / NOT_SCIENTIFIC_ACCEPTANCE`. This lesson introduces no new native task, provider commitment, scheduling SLA, approval or external certification.
