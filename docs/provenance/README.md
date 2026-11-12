# Provenance evidence registry — dated source cutoffs and correction history

[Full-first-day classification](../taxonomy/README.md) · [Original 2026-10-30 historical reconstruction](../REPOSITORY_HISTORY_AND_PROVENANCE.md) · [Open claims](../CLAIM_VERIFICATION_GAPS.md) · [Evidence authority](../PROVENANCE.md)

This is a **living index of separately frozen historical observations**, not a claim that the original October 30 denominator still describes current GitHub reality. Preserve original JSON, original source names, historical failures and correction history. The first section below belongs to the original October 30 bounded observation only.

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

## Later causal source reconstruction · 2026-10-31

[Independent failure causal audit](FAILURE_CAUSAL_REPLAY_2026-10-31.md) · [Privacy-minimized JSON](failure-causal-replay-2026-10-31.json) · [Offline regression](../../tests/test_failure_causal_replay.py). This is a separately dated source-level reconstruction: eight failed Git heads violate the same historical document-inventory contract, while PR #43 supplies an inverse excess-entry case and correction; public February predecessor Git/Run evidence is distinguishable from unverified private Jules execution. This addition neither replaces frozen archives nor changes production Knowledge.

## Subsequent 2026-10-31 pre-PR review: exact 563 → 587 population

The [2026-10-31 read-only review](POST_REVIEW_OBSERVATION_2026-10-31.md) and [source-graded additive JSON](post-review-observation-2026-10-31.json) reconcile **all 563 previous IDs**, with **24 new successful Run IDs (16 push / 8 PR), zero previously observed IDs missing**, for 587 currently visible IDs (546 success / 41 cancelled). The already observed 31 scheduled Runs and 48 successful scheduled Jobs were rechecked; no new scheduled event or accepted Knowledge Receipt is in this delta. The [offline replay](../../tests/test_post_review_evidence_delta.py) reconstructs all 531 → 547 → 563 → 587 populations and keeps the earlier eight failed-run records as conflicting-time observations, not erased history. This is a **pre-PR cutoff** at main `1fe2fb530de3e62b7ca27e7493909313f733f934` and deliberately leaves the exact original API retrieval UTC instant `null`. Later PR and push checks must be recorded in a new observation, not appended retroactively to this population. Existing 2026-10-30 snapshots, errata and production `data/` remain unchanged

The adjacent [public research lesson](../lessons/2026-10-31-observation-without-claim-promotion.md) documents a falsifiable **NO_CHANGE_REQUIRED** decision: newly visible successful engineering checks do not themselves advance a scientific claim or justify a new production write

## Independently re-collected full root-to-current census · 2026-10-31 UTC-bounded window

[First-day-to-current reconstruction](FULL_HISTORY_REPLAY_2026-10-31.md) · [Full normalized Git/PR/Actions source rows](full-history-census-2026-10-31.json) · [Independent offline hash and population replay](../../tests/test_full_history_census_replay.py) · [Public failure and governance lessons](../lessons/2026-10-31-cloud-history-replay.md)

This is a **new** bounded read from `2026-10-31T06:48:12Z` through `06:49:02Z`, pinned to `bc33c75efeee341194f1d2eec804565ed58a90bb`, not a rewrite of any earlier snapshot. The API exposed **242 parent-closed main commits, 50 PRs (48 merged / #29 and #32 closed unmerged), 247 tracked blobs, and 598 distinct visible Runs (557 success / 41 cancelled)**. All 587 IDs from the immediately preceding report remain visible with unchanged event, workflow identity, created time and terminal conclusion; the **11 new** successes consist only of PR #50 development/merge checks. All 31 observed scheduled Runs and 48 successful Jobs were separately re-read; the 3 accepted Knowledge Receipts are unchanged. The older different 531-Run snapshot with 8 failures remains authoritative for that **dated** observation

Frozen archive and production `data/` Git Blob SHA guards are recomputed from raw local bytes by independent CI. This report also distinguishes the observed non-enforced public branch settings from unavailable admin protection detail, as well as external registry object-level `UNKNOWN` status. The current record is a **source cutoff before its own documentation PR**, so later PR/CI activity cannot be retroactively inserted into the 598 observed rows

## Follow-up 2026-11-01 read-only observation: exact 614 → 628 population

[New source-graded reconciliation](POST_614_TO_628_RECONCILIATION_2026-11-01.md) · [14-Run machine delta](post-614-to-628-observation-2026-11-01.json) · [Independent offline regression](../../tests/test_post_614_run_delta.py) · [Public lessons](../lessons/2026-11-01-run-identity-and-clock-boundaries.md)

A seven-page API observation at the pinned pre-publication `main=3afea285b3660f9482c935c13160705eecfb332a` retained **all 614 earlier Run IDs** and added **14 success** records (nine push, three PR, two schedule), yielding 628 currently visible (587 success / 41 cancelled). November 1 scheduled verification adds three successful Jobs and their three separate Artifacts, reaching 35 observed scheduled Runs / 54 successful Jobs; the three formally accepted Knowledge Receipts and two input archives are unchanged. GitHub `v0.5.0` exists, but this is not an external registry update or a biological claim. A cross-clock one-hour timestamp discrepancy between a Run API object and its Runner log is preserved as `UNKNOWN`, with no claimed scheduler root cause. Prior failures, errata and immutable source snapshots remain intact. Publishing this report may itself generate later PR/CI runs, which are excluded from this frozen source cutoff

## 2026-11-02 · Fourth accepted native cycle and frozen-history test boundary

[Source-graded 640 → 653 reconciliation](POST_640_TO_653_AND_NATIVE_ACCEPTANCE_2026-11-02.md) · [13-Run machine-readable delta](post-640-to-653-observation-2026-11-02.json) · [Independent replay](../../tests/test_post_640_run_delta.py) · [Public regression lesson](../lessons/2026-11-02-frozen-history-vs-live-state.md)

This new pre-PR source cutoff preserves all 640 prior Run identities and adds 13 successful records, reaching 653 currently visible (612 success / 41 cancelled). A real November 2 native schedule completed its `validate` and `apply` Jobs and pushed the **fourth** accepted Knowledge receipt and event; the later continuity Job verified it. Source document text, 17 graph nodes and 26 citation edges were unchanged. Historic snapshot tests that assumed the mutable live `data/` would always contain exactly three accepted receipts were repaired without editing old observations or formal data. Current external registry parity, activation delays and scientific truth remain independently unverified.

## 2026-11-03 · Post-653 to 673 Run identities and native quality closure

[Source-graded 653 → 673 reconciliation](POST_653_TO_673_RECONCILIATION_2026-11-03.md) · [20-Run machine-readable delta](post-653-to-673-observation-2026-11-03.json) · [Independent offline falsifier](../../tests/test_post_653_run_delta.py) · [Public operational lesson](../lessons/2026-11-03-native-success-is-not-universal-execution.md)

All 653 previously frozen identities remain visible in the new seven-page API census; 20 additional successful PR-related Runs yield 673 visible Runs (632 success / 41 cancelled), with no new scheduled or accepted production events in the bounded observation. All 38 visible scheduled Runs have 59 directly checked successful Jobs. The 20 new PR-related Runs have 36 successful and two conditionally skipped Jobs. Native accepted Knowledge remains four Receipts and four linked events; no novel biological result or third-party scientific certification is established. Earlier failures, PR #55's unavailable intermediate Run IDs, clock uncertainties, unprotected main settings and external synchronization limits remain separately recorded. This frozen cutoff predates its own publishing PR and follow-up CI.

## 2026-11-03 · Post-PR #57 673 → 684, and complete first-day classification

[New 11-Run/21-Job source evidence](post-673-to-684-observation-2026-11-03.json) · [Source-cutoff reconciliation](POST_673_TO_684_RECONCILIATION_2026-11-03.md) · [Complete 250/57/274 classification](../taxonomy/README.md) · [Historic name correction register](../taxonomy/CORRECTION_REGISTER_2026-11-03.md)

Every earlier 673 Run ID remains visible in the new source collection. Eleven new successful PR #57 development/PR/merged-main Runs include 20 successful Jobs and one conditionally skipped Bio Job. The 684-Run cutoff does not include the subsequent classification PR and its CI; original frozen observations remain untouched.


## 2026-11-04 · Post-684 to 711 native Run and scheduled-Job audit

[New 27-Run GitHub-source delta](post-684-to-711-observation-2026-11-04.json) · [Human-readable analysis](POST_684_TO_711_RECONCILIATION_2026-11-04.md) · [Independent offline test](../../tests/test_post_684_run_delta.py) · [Public falsifiable lesson](../lessons/2026-11-04-cron-offset-observation-and-conditional-jobs.md)

At the pinned pre-publication `main=0728c19d32492d2932bffbab9045e7aeedcbd667`, all 684 prior source-derived Run IDs remained visible and 27 new successes appeared, for 711 visible Runs (670 success / 41 cancelled). The 27 new Runs had 51 successful and three conditionally skipped Jobs; the two new scheduled Runs had three successful Jobs, with substantial *nominal cron → API created_at* offsets whose causal mechanism remains UNKNOWN. Current formal Knowledge acceptance remains four Receipts and four linked events, with no new scientific result or registry approval. The frozen historical failures and earlier evidence are preserved; subsequent reporting PR/CI activity is outside this cutoff.

## 2026-11-05 · 721 → 730 visible GitHub Runs and Nov 4 native scheduling

[Source-pinned nine-Run JSON](post-721-to-730-observation-2026-11-05.json) · [Analysis](POST_721_TO_730_RECONCILIATION_2026-11-05.md) · [Regression](../../tests/test_post_721_run_delta.py) · [Lesson](../lessons/2026-11-05-cron-jobs-evidence-boundaries.md)

The Nov 5 read-only census found all 721 previously frozen Runs retained and nine new successful Runs, including two scheduled checks and 20 Jobs (19 success, one conditional Bio skip). Current API visibility is 730 Runs, not all-time immutable history. Two nominal cron-to-created offsets remain observation-only with UNKNOWN cause; four accepted Knowledge events, original negative evidence, external provider authority and scientific nonclaims remain unchanged. This publishing PR's own CI belongs to a later cutoff.

## 2026-11-05 · Complete historical file-path and blob-identity audit

[Full source-pinned 256-Commit / 235-Tree / 294-current / 47-historical-only file audit](../taxonomy/FULL_FILE_LIFECYCLE_2026-11-05.md) · [Machine-readable complete register](../taxonomy/full-file-lifecycle-2026-11-05.json) · [Offline falsifier](../../tests/test_full_file_lifecycle_2026_11_05.py)

This is an additive **file-identity provenance** review, independent from the dated 721→730 Run review. Historical-only paths are not missing current production, and 19 exact Git Blob reuses are byte-level matches, not proven semantic migrations. Git version identity, external Agent identity, native acceptance, and institutional scientific validity remain separate objects. The original historical baselines, errors and correction history are not rewritten.

## 2026-11-05 · After PR #64, 730 → 750 Actions and complete file-source delta

[20-Run/46-Job machine ledger](post-730-to-750-observation-2026-11-05.json) · [Source and failure review](POST_730_TO_750_RECONCILIATION_2026-11-05.md) · [Offline regression](../../tests/test_post_730_run_delta.py)

At source-pinned post-merge main `c2ac76e630e11d723a15a56b5c36d0118fdbe491`, exactly one main Commit and four new paths extend the complete prior Git file lineage: 256→257 Commits, 294→298 tracked files, 47 prior historical-only paths retained. The 730 earlier Run IDs all remain visible among 750, with 20 new Runs and 46 Jobs (39 success, five failure, two conditional skip). Four genuine PR #64 development failures came from a repaired Git Blob NUL-header hashing test; no archived byte rewrite or new scientific acceptance is inferred. All earlier snapshots and formal `data/` remain unchanged

## 2026-11-06 · 750 → 758 visible Runs with disappeared historical failures

[Exact full 758-ID JSON and 46 scheduled Run references](post-750-to-758-observation-2026-11-06.json) · [Read-only reconciliation](POST_750_TO_758_RECONCILIATION_2026-11-06.md) · [Regression](../../tests/test_post_750_run_delta.py) · [Public failure-mode lesson](../lessons/2026-11-06-visible-history-and-scientific-nonclaims.md)

The previous 750 archived IDs were independently reconstructed and compared to 758 currently visible unique GitHub API Runs: 746 old IDs retained, 12 new successful Runs, and four historically **failed** PR #64 Runs now inaccessible (direct HTTP 404, cause UNKNOWN). The current visible denominator has 717 success / 41 cancelled / zero presently visible failure; it does **not** erase the frozen historical failure records. All 46 currently visible scheduled Runs / 72 Jobs are successful by individual Jobs API; Nov 6 Bio and daily self-check both ran with distinct Jobs and reported Artifacts, but nominal cron offsets and scientific nonclaims remain explicit. Four accepted production Receipts, three archive Candidates, native execution code, and external certification status are unchanged

## 2026-11-07 · 758 → 768 visible Runs, native continuity and closed-unmerged PR boundary

[Ten-Run and 20-Job source observation](post-758-to-768-observation-2026-11-07.json) · [Reconciliation](POST_758_TO_768_RECONCILIATION_2026-11-07.md) · [Independent offline falsifier](../../tests/test_post_758_run_delta.py) · [Public governance lesson](../lessons/2026-11-07-closed-branch-is-not-main-acceptance.md)

At pinned main `5965f81d133623ea01cd826f25a5c1e48770b6fa`, all 758 previous visible Run IDs were retained and ten new successful Runs appeared (19 successful Jobs, one expected Bio push skip), yielding 768 API-visible Runs: 727 success and 41 cancelled. The added Nov 6 Continuity Run independently passed state, source-linked Knowledge and graph quality checks; dated scheduled-Job evidence now covers 47 Runs / 73 successful Jobs across source cutoffs. Main has 259 root-reachable Commits, 305 tracked Git Blob paths, and 67 PRs: 64 merged, #29/#32/#67 closed-unmerged, none open. PR #67's two green branch Evidence pushes do not make its OSF or file-governance proposals accepted on main. Four production Receipts / four events, older unavailable failures, current provider authority and scientific nonclaims remain unchanged. This frozen cutoff excludes this documentation PR and its own CI

## Additive 2026-11-08 · 768→788 Run / 42 Job and schedule-causality review

[Run/Job/clock machine census](post-768-to-788-observation-2026-11-08.json) · [Review and daily native table](POST_768_TO_788_RECONCILIATION_2026-11-08.md) · [Offline falsifier](../../tests/test_post_768_run_delta.py) · [De-identified public lesson](../lessons/2026-11-08-green-checks-are-not-scientific-acceptance.md)

At pinned main `503c340f9d5d4b34b8aacb6df6fd680567445b00`, all 768 prior API-visible Run identities remain present and 20 new successful Run objects are observed, with 40 successful Jobs and two Bio push-only conditional skips. This source cutoff has 788 visible Runs (747 success, 41 cancelled), 51 scheduled Runs with 79 Jobs independently checked across successive dated audits, 261 main-reachable Commits, 312 Git Blobs and 69 PRs (66 merged / three closed-unmerged / none open). Nov 7–8 daily dual-plane and continuity runs succeeded, but nominal-cron-to-created gaps of several hours have **UNKNOWN** cause. Four formal Receipts and chained events remain unchanged. Original vanished failures and correction records are preserved. This review does not modify accepted `data/`, the three software assets, Framework, Actions or provider registrations. The publishing PR and its own checks are excluded from the frozen counts
## Additive 2026-11-09 · 788→798 native Run/Job, fifth accepted Knowledge event and frozen-test gate correction

[Source-pinned ten-Run/22-Job ledger](post-788-to-798-observation-2026-11-09.json) · [Bounded quality review](POST_788_TO_798_RECONCILIATION_2026-11-09.md) · [Offline falsifier](../../tests/test_post_788_run_delta.py) · [De-identified failure-mode lesson](../lessons/2026-11-09-frozen-tests-vs-native-continuity.md)

At pinned native main `a1918caeabbd23bc962e9c0c8e05e67a2d0be479`, all 788 previously visible Runs persist among 798 (757 success, 41 cancelled), with 21 successful and one conditionally skipped Job among ten new Runs. Nov 9 daily self-check, scheduled native Knowledge (both validate/apply), and subsequent independent continuity all passed, with nominal-to-created offsets that have UNKNOWN causal explanation. The native guarded run 42611716908 genuinely accepted fifth Receipt/event and a fourth historical Candidate archive while reporting DOCUMENT_TEXT_UNCHANGED, so there is no supported new biological conclusion. Three old dated regression assertions incorrectly capped mutable accepted state at four; only those offline tests and public bounded evidence are repaired. Historic errors and earlier source snapshots are not rewritten; the publishing PR and its CI are outside this frozen source population

## Additive 2026-11-10 · 798→807 repaired gate, daily checks and unchanged accepted state

[Source-pinned nine-Run/20-Job ledger](post-798-to-807-observation-2026-11-10.json) · [Bounded reconciliation](POST_798_TO_807_RECONCILIATION_2026-11-10.md) · [Offline falsifier](../../tests/test_post_798_run_delta.py) · [Public failure-mode lesson](../lessons/2026-11-10-repair-success-does-not-erase-failed-gates.md)

At pinned main `7008c32d0224aa0fdbe25bbc4614d4988f212669`, all 798 previous visible Run identities remain among 807 (766 success / 41 cancelled). Nine new visible successes contain 19 successful Jobs and one contractually skipped main-push Bio pinned-field Job. November 10 daily dual-plane self-check and independent accepted-state continuity succeeded, with nominal-to-created offsets whose cause remains UNKNOWN. Four earlier failed PR #71 Runs preserved by the prior report now return 404; their later disappearance does not erase the negative gate evidence. Formal research state remains five Receipts, five chained events, four archives, 17 entities and 26 relations, with no new native apply or scientific claim. The update is documentation and offline verification only; no Workflow, Tool, Framework, schedule, accepted data, Release, DOI or external registration changes.

## 2026-11-13 · Additive 807→849 Run/Job and gate-closure audit

[42-Run / 103-Job source ledger](post-807-to-849-observation-2026-11-13.json) · [Bounded quality reconciliation](POST_807_TO_849_RECONCILIATION_2026-11-13.md) · [Offline falsifier](../../tests/test_post_807_run_delta.py) · [Fail-closed public lesson](../lessons/2026-11-13-fail-closed-paths-and-cancelled-jobs.md)

At pinned main `4bc0ad701f2a9f7ebae4e4aecf1d7aa7e867334d`, all 807 previous visible Run IDs remain present among 849 (32 new successful and ten new cancelled Runs). The 42 newly inspected latest-attempt Run/Job results comprise 73 success, three skip, 26 cancel and one failure across 103 Jobs, including a failed Repository contracts Job inside cancelled Run 43210854941 for the unclassified RELEASE_POLICY.md intermediate root path. Final PR #74 checks confirm repair without erasing that failure. Four new scheduled daily/continuity runs on Nov 11–12 passed their individual Jobs with unknown cron-to-created offset causes. Accepted Knowledge remains five receipts/five events/four archives and 17 extractive entities/26 SOURCE_MATCH relations; no newly verified biological result or external certification. This evidence-only addendum never alters the three assets, Framework, schedules, historical frozen snapshots, formal data, Release or DOI.
