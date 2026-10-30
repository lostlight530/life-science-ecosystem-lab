# Origin-to-current provenance reconciliation · 2026-10-30

[Original frozen census](README.md) · [Daily native quality](NATIVE_DAILY_QUALITY_2026-10-30.md) · [Public research lessons](../lessons/2026-10-30-error-detection-and-audit.md) · [Open claims](../CLAIM_VERIFICATION_GAPS.md)

## Authority, scope, and the two different start dates

- **Historical antecedent, not Git ancestry:** PR #1 attributes a predecessor collaboration to February 15–16, 2026; no original predecessor task or immutable bytes have been independently recovered from the LS Git repository
- **Verifiable LS repository origin:** October 16, 2026, 10:35:54 UTC; first root commit `00009a38bc136a7c245270770b005e4e102a870d`
- **First immutable census:** October 29, 2026, 16:24:03.499 UTC, main `05ab6b2dc98dfe13581b5ae1bedcd11a58dbbb77`: 234 main-reachable commits, 42 PRs (40 merged; #29 and #32 closed without merge), 531 visible Actions runs (483 success, 8 failure, 40 cancelled)
- **New public read-only observation:** October 30, 2026, 00:49:52.775 UTC, main `ae1ac9c1e42ca707b1f44f5cc46b15c787b05899`: 235 main-reachable commits, 43 PRs (41 merged; 2 closed-unmerged), 531 visible Actions run objects (490 success, 0 failure, 41 cancelled)
- A different **prior, intervening live inspection** observed 542 runs (490 success, 11 failure, 41 cancelled); three of those failed runs were not present at the earlier frozen cutoff and are not re-fetchable now. These observations have lower archival strength than the committed original 531-row API snapshot

These are **observation-specific denominators**, not additive independent CI executions or an all-time success percentage. A green current listing does not make previously observed failures false.

## Read-only chain of custody

| Layer | Stored immutable or dated source | What was actually checked |
| --- | --- | --- |
| Git ancestry | [Frozen commit census](commits-2026-10-30.json) and [later delta](history-delta-2026-10-30.json) | 234 previous main-reachable records and one subsequent squash-merge commit, latest parent pinned to original census main; closed PRs are not accepted code |
| PR decisions | [Frozen 42 PRs](pull-requests-2026-10-30.json) and [PR #43 delta](history-delta-2026-10-30.json) | 43 total, 41 merged, #29 and #32 closed-unmerged |
| Actions initial observation | [Original 531 run records](action-runs-2026-10-30.json) | Run IDs, results, timestamps and source SHA as returned at the fixed cutoff |
| Actions later observation | [Privacy-minimized 531 run index](actions-visible-index-2026-10-30.json) | Run ID, workflow ID, event, UTC creation time, conclusion; 531 distinct IDs, actor fields excluded |
| Observation comparison | [Exact set reconciliation](action-run-reconciliation-2026-10-30.json) | Eight old runs absent, eight newly visible runs, without altering either census |
| Native productivity and checks | [Daily quality ledger](native-daily-quality-2026-10-30.json) | 28 individually identifiable scheduled successes plus 1 manual native run; per-day local clock, nominal cron offset and production receipts |

For all files here, **project-owned API observations are not official archival certification**, cannot authenticate Agent runtime identity, and are not third-party scientific findings.

## The discrepancy: eleven historical failures, zero now visible

The original snapshot contains eight failure IDs, all from the independent Evidence Tool workflow on October 29 UTC, around 16:02–16:04. The later observation is missing those same eight IDs while adding seven successful runs and one cancelled run. The [machine-readable diff](action-run-reconciliation-2026-10-30.json) records every exact ID in both sets and pins the two observation times.

An intervening, directly observed GitHub API review contained three additional failures around 16:32 UTC from the later PR #43 development attempt. Their IDs are recorded separately with `PRIOR_ASSISTANT_SESSION_DIRECT_API_AND_LOG_OBSERVATION_NOT_RETRIEVABLE_NOW` status; those original Job logs were **not** committed and must not be described as independently recoverable evidence. Their summary is lower-grade retrospective testimony.

Previous direct Job-log inspection found all eleven failures were assertions from the same repository experience test, `test_public_documentation_inventory_is_complete`:

- **First eight:** new public Markdown documents entered the controlled scan without being listed in the approved documentation inventory; repetitive commits triggered the same failure. The later merged [PR #40](https://github.com/lostlight530/life-science-ecosystem-lab/pull/40) registered the relevant documents
- **Later three:** the PR #43 draft incorrectly included `docs/provenance/README.md`, a nested path not enumerated by the test's direct-child Markdown glob; a one-file inventory correction resulted in passing PR and post-merge checks. [PR #43](https://github.com/lostlight530/life-science-ecosystem-lab/pull/43) preserves the accepted change but not full deleted-run logs
- Both are **documentation-inventory contract failures**, not eleven distinct biological computation failures, nor independent replication across Evidence and Bio: both invoked the same root repository test

At the later observation, direct retrieval of selected missing run IDs returned GitHub `404`. GitHub [documents deletion of completed runs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/delete-a-workflow-run), but **no authenticated delete audit log, actor attribution, reason, or proof of mechanism was obtained**. Do not assert who deleted or why. GitHub also documents [temporary artifact/log retention](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository); this is a separate issue from whether a particular run itself is still queryable.

**Falsifier for the claim that a run is presently absent:** independent, authorized GET of that exact run ID returning a valid complete run response at the same controlled observation would overturn the narrow absence observation. **Falsifier for root-cause attribution:** retained original logs identifying a different failing assertion would require correction. Missing source data remains `UNVERIFIED`, not invented.

## Scientific software interpretation and limits

An invariant that rejects inconsistent metadata is a demonstrated **engineering fail-closed control**, not verification of scientific validity. A single repeated assertion can produce eleven red runs without representing eleven distinct defects. A once-green current CI list is a selection-dependent view, not the long-run denominator. Neither scheduled runs nor source-revision-only accepted events should be counted as new scientific findings.

GitHub Actions is **native execution infrastructure**, not a fourth research software asset. Knowledge Workflow, Evidence Tool and Bio Tool retain independent responsibilities; the experimental Framework is distinct, and was not retroactively in the frozen v0.4.0 release. Accepted Knowledge has three actual Git receipts, not 531 production research units.

The methodological loop used here is **DEFINE → PIN → QUALIFY → EXECUTE → EVALUATE → AUDIT → REVIEW → REPLAY**. In particular, REVIEW must keep explicit unresolved outcomes: no reliable deletion attribution, no proved cause for delayed cron dispatch, no independently recovered February predecessor evidence, and no biological truth oracle for a document-inventory test.

## Reproduce offline, without rewriting the historical archives

```sh
python -m unittest discover -s tests -p 'test_repository_provenance_archive.py' -v
python -m unittest discover -s tests -p 'test_provenance_observation_reconciliation.py' -v
```

The first test deliberately asserts the **old** 234 / 42 / 531 census; the second asserts the **dated new** 235 / 43 / 531 and calculates the old/new run-ID set difference. Neither test calls GitHub, edits `data/`, certifies institutions, or triggers a native production apply.

**Change boundary:** docs and a separate offline test only. No workflow YAML, installed Tools, Framework implementation, source/topic registry, existing frozen archives, accepted `data/`, account settings or external institutional objects were changed in this research update.

## Independently discovered run-name identity defect and numerical correction

A subsequent audit found that the compact index's `workflow_names` dictionary conflated historical names for the same workflow ID, **mislabeling 134 of the 531 run rows**, without changing their Run IDs or outcomes. The [independent per-run correction](run-name-attribution-audit-2026-10-30.json) and [auditable erratum](RUN_NAME_AND_MEDIAN_ERRATUM_2026-10-30.md) restore time-specific labels, while preserving the original index and its negative evidence. The same review recomputed two incorrect medians in the daily-quality report (correct: 342.01 and 302.41 minutes). This illustrates that successful CI can coexist with a false temporal join or arithmetic claim.
