# Post-merge LS provenance and native execution recheck — 2026-10-30

[Origin-to-present archive](../REPOSITORY_HISTORY_AND_PROVENANCE.md) · [Previous reconciliation](RECONCILIATION_2026-10-30.md) · [Historical daily quality](NATIVE_DAILY_QUALITY_2026-10-30.md) · [Original erratum](RUN_NAME_AND_MEDIAN_ERRATUM_2026-10-30.md) · [Public lessons](../lessons/2026-10-30-evidence-census-and-runtime-quality.md)

**Observation UTC:** `2026-10-30T01:57:45.729Z` · **Pinned source main:** [`56ac4a9065d8f0ff60da6eadadfdbe44a2d26615`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/56ac4a9065d8f0ff60da6eadadfdbe44a2d26615) · **Scope:** public GitHub Actions API pages 1–6, PR metadata, commit ancestry, selected Run Jobs and existing accepted Git receipts · **Owner:** project-specific, NOT an institutional verification

## Reconstructed starting boundary

The first LS repository root is [`00009a38bc136a7c245270770b005e4e102a870d`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/00009a38bc136a7c245270770b005e4e102a870d), created October 16, 2026. The earlier February 15–16 predecessor collaboration is an author-reported historical attribution in PR #1, **not recovered Git ancestry or independently authenticated predecessor execution**.

Earlier frozen census: 234 main-reachable commits, 42 PRs and 531 visible Actions objects, **including eight failures**. Next immutable reconciliation: 235 commits, 43 PRs, and a **different** set of 531 visible Actions objects with zero failures in that *later* visible sample. This is why snapshots are not permanent all-time CI ledgers. Historical red runs and lower-grade testimony of three additional failed runs remain explicitly preserved in the earlier reconciliation.

## This new exact-ID observation

The [full 16-record machine-readable delta](post-merge-observation-2026-10-30.json) compares the latest six GitHub API pages with the earlier 531-row compact index. The API currently returned **547 unique visible Run IDs**, of which **506 success** and **41 cancelled**, classified by events as 256 push, 259 pull request, 28 schedule and 4 manual `workflow_dispatch`.

The 531 old IDs were all still present, with **zero changes to those records' event types or final conclusions**; **16 new runs** were all successful and all `push` or `pull_request` events. This is **not** a correction of the initial eight failures, which belong to a prior, different snapshot. An API response can establish what was visible at its observation time, not why older objects became unavailable.

PR #44 [merged](https://github.com/lostlight530/life-science-ecosystem-lab/pull/44) at `ab56cd79f5532623c2043f5b18f744b159f39aa3`; PR #45 [merged](https://github.com/lostlight530/life-science-ecosystem-lab/pull/45) at `56ac4a9065d8f0ff60da6eadadfdbe44a2d26615`. They are two additional commits since the 235-commit pre-update main, so that same historical main-ancestry counting rule gives **237 reachable commits** before this follow-up archival PR. GitHub PR objects then total **45**, 43 merged and #29/#32 closed without merging. An unmerged PR is a Git decision, not automatically a scientific refutation.

## Native daily quality: what was really executed

The [daily table](NATIVE_DAILY_QUALITY_2026-10-30.md) covers October 16–30 in **Asia/Shanghai**, including the partial 30th; its archived sample contains **28 observed scheduled successes** with independently inspected Job lists: Knowledge 2 weekly, continuity 13 daily, institutional/project dual self-check 12 daily and Bio 1 weekly. It does **not** establish an expected-run uptime percentage because activation times, all missing runs and queue semantics were not independently enumerated.

Only **three accepted Knowledge events** have corresponding durable production `data/receipts`: October 17 initial baseline, October 19 baseline classification transition and October 26 a revision/provenance-only change with unchanged selected document text. These are not three new scientific discoveries. There is also one manually dispatched initial production run, which must never be added to the scheduled-run denominator.

At this recheck, no October 30 scheduled `Run` was yet visible in the six pages. Even though the nominal 01:41 UTC self-check time had just passed, **NOT_OBSERVED_AS_OF_CUTOFF is not a proved failure or missed scheduled execution**. GitHub [officially documents that scheduled events can be delayed or dropped under load](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), but the recorded offset alone does not identify a mechanism for this repository.

**Latest post-merge main push Job inspection:**

| Workflow Run | Jobs actually returned | Correct narrow claim |
| --- | --- | --- |
| [Bio 40983926830](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40983926830) | `offline = success`, `pinned-field = skipped` | Offline QA succeeded; *no* new field run executed in this push |
| [Evidence 40983926822](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40983926822) | Evidence CLI/docs verification = success | Independent Tool QA passed |
| [Integration 40983926784](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40983926784) | Portable package, Knowledge Workflow, repository contracts, Evidence Tool, validate = success | The integration checks passed, not scientific validity |

A parent workflow's `success` is not proof that every conditional Job ran. Job-list evidence is distinct from the unavailable complete long-term original Runner logs.

## Correcting machine-consumer statistics without rewriting history

The original daily JSON has two incorrect derived `observed_offset_median` fields despite valid 28 per-run observations. PR #45 fixed the narrative and independently audited the arithmetic, but kept the frozen original JSON intact. The [new append-only machine correction](native-quality-corrections-2026-10-30.json) independently sorts **all** original offset rows and provides the accurate values:

| Class | Sample size | Old stored median (min) | Corrected median (min) |
| --- | ---: | ---: | ---: |
| Weekly Knowledge | 2 | 340.25 | **342.01** |
| Daily dual-plane self-check | 12 | 295.77 | **302.41** |
| Daily continuity | 13 | 311.38 | 311.38 |
| Weekly Bio | 1 | 314.35 | 314.35 |

All offsets compare the nominal cron with API `created_at` time, not an independently proven queue delay. Workflow ID is likewise *not* a temporal name identity: the previously discovered 134 renamed rows are corrected only through the separate per-Run source-graded [historical name audit](run-name-attribution-audit-2026-10-30.json).

## Eight-stage review and disclosure boundary

`DEFINE → PIN → QUALIFY → EXECUTE → EVALUATE → AUDIT → REVIEW → REPLAY`: state the observation scope, pin base HEAD and original source clocks, run exact ID-diff and full-population statistics, inspect selected Jobs, retain negatives and limits, review in PR, and rerun the offline archive test.

External [GitHub Run API documentation](https://docs.github.com/en/rest/actions/workflow-runs) and [retention policy](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) describe platform behavior, not this repository's custom settings or proof of a specific deletion cause. This document does not assert who deleted runs, why scheduling offsets occurred, how Agents internally reasoned, or whether any biological hypothesis is true.

**Scope restriction:** this PR only adds versioned project-owned evidence, privacy-minimized experiences, links and an offline regression. It does **not** change Workflow, Tool, Bio Tool, Framework, GitHub Actions YAML, official institutional defaults, LifeMonitor config, approved source/topic registers or accepted production `data/`.
