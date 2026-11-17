# GitHub native history and source-bound contract reconciliation · 868 → 889 · 2026-11-17

[Machine Run/Job/Commit/PR/Blob evidence](post-868-to-889-observation-2026-11-17.json) · [Prior 849→868 archive](POST_849_TO_868_RECONCILIATION_2026-11-15.md) · [Full first-day-to-Nov15 source classification](../taxonomy/FULL_HISTORY_CLASSIFICATION_2026-11-15.md) · [Failure lesson](../lessons/2026-11-17-frozen-history-vs-live-accepted-state.md) · [Independent offline replay](../../tests/test_post_868_run_delta.py)

**DEFINE / PIN.** This report studies GitHub-visible repository state at main [`93d4cfb5f26c258880a92c700ad14192400a5b17`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/93d4cfb5f26c258880a92c700ad14192400a5b17), through the last *included* Run created **2026-11-16T17:33:07Z** (2026-11-17 Asia/Shanghai). It deliberately freezes the **889-Run pre-maintenance cutoff**. Subsequent audit-branch Push/PR Runs are outside this population even when they appear in a later API response. Individual HTTP acquisition timestamps were not recorded. Nothing here is an external institution's certification or a new biological research result.

## QUALIFY · Full source identity since the Git root

- The LS Git root is [`00009a38bc136a7c245270770b005e4e102a870d`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/00009a38bc136a7c245270770b005e4e102a870d), **2026-10-16**, not the February predecessor engineering attribution. A February 15–17 Jules contribution mentioned in [PR #1](https://github.com/lostlight530/life-science-ecosystem-lab/pull/1) remains a distinct repository/actor-origin claim, not LS Git ancestry or authenticated private Agent execution
- Previous source-pinned classification: **299** main-reachable commits, **274** distinct Git Trees, **331** current tracked Blob paths. This addendum reconstructs the **three** new ancestors (`f1364419`, merge `101baf41`, native-data `93d4cfb5`) with all parent edges closed to the same root: **302 commits / 276 distinct Git Trees**
- Tracked files: **331 → 339**, eight added, zero old paths removed, twelve old Blob identities changed. New paths are two native `data/` append witnesses, one lesson, two provenance documents, two taxonomy documents and one test. Current `main` contains **339 files**, not 390 files: the recursively returned Git Tree includes directories
- PRs: **76 → 79**, now **74 merged**, four closed-unmerged **#29/#32/#67/#78**, and **#79 OPEN_DRAFT**. PR #77 merged; #78 must not be promoted to main acceptance; #79 is neither reviewed acceptance nor a software release. Exactly **three** public GitHub Releases now exist: `v0.4.0`, `v0.5.0`, `v0.5.1`. GitHub tags and independent Framework package identity are not registry acceptance or a DOI for a new scientific result
- The three established, independently callable research-software assets are Knowledge Workflow, Evidence Tool and Bio Tool; the separately packaged software-contract Framework is **experimental**. The nine native GitHub Workflow YAML files are execution infrastructure, not nine research assets. External Agents are optional proposal/review contributors and do not independently authorize production writes

## EXECUTE / EVALUATE · Reconcile exact visible Run and Job grains

| Compatible API-visible metric | Frozen 2026-11-15 | 2026-11-17 pre-maintenance cutoff | Delta |
| --- | ---: | ---: | ---: |
| Unique Run IDs | 868 | **889** | **+21**, all 868 previous IDs retained |
| Parent Run conclusions | 817 success / 51 cancelled / 0 failure | **834 success / 51 cancelled / 4 failure** | +17 success / +4 failure |
| Run events | 359 PR / 438 push / 67 schedule / 4 manual | **367 PR / 448 push / 70 schedule / 4 manual** | +8 PR / +10 push / +3 schedule |
| New latest-attempt Job conclusions | — | **34 success / 5 failure / 1 skipped** | **40 distinct Job IDs** |
| Main commits / current tracked files | 299 / 331 | **302 / 339** | +3 / +8 |
| PR objects / merged / closed-unmerged / open | 76 / 73 / 3 / 0 | **79 / 74 / 4 / 1** | +3 / +1 / +1 / +1 |
| Accepted Receipts / chained events / previous Candidate archives | 5 / 5 / 4 | **6 / 6 / 5** | +1 / +1 / +1 |

The machine JSON preserves the exact 21 new Run IDs, SHA, historical workflow names, trigger and parent conclusions, **all 40 actual latest-attempt Job IDs/conclusions** and decisive failed/skipped steps. Job-summary coverage of the 21 new Runs does **not** assert full successful-step log retention or all historical Job attempts.

**All currently visible scheduled Runs by category (independently inspected in prior complete audit):** Daily self-check 30 (60 success Jobs), continuity 31 (31), scheduled Knowledge 5 (10), scheduled Bio 4 (8). **70 scheduled Runs / 109 successful latest-attempt Jobs** from October 17 through November 16, with no missing daily calendar dates within each defined start window. This figure must not be confused with all 889 Run conclusions, all workflow executions or scientific acceptance.

### New scheduled nominal-time observations

| Date (UTC) | Scheduled Run | Nominal UTC | GitHub created_at UTC | Nominal-to-created |
| --- | --- | --- | --- | --- |
| Nov 16 | [Daily self-check 43832487384](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43832487384) | 01:41:00 | 08:35:39 | +06:54:39 |
| Nov 16 | [Knowledge 43859884737](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43859884737) | 03:23:00 | 11:40:57 | +08:17:57 |
| Nov 16 | [Continuity 43870632783](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43870632783) | 04:17:00 | 12:53:21 | +08:36:21 |

These are differences between the specified clock fields, **not** measured dispatch/queue/runner latency. Cause remains **UNKNOWN**. Schedule success does not prove the provider is online continuously.

### Sixth native production acceptance, not a sixth science finding

The new [Knowledge Run 43859884737](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43859884737) has successful **validate** and **apply** Jobs, a Git push to main `93d4cfb5`, and exact `data/receipts/gh-43859884737-1.json` plus sixth chained `data/knowledge/events.jsonl` event. Its recorded `change_kind` is **DOCUMENT_TEXT_UNCHANGED** and outcome **APPLIED**. The five-event frozen prefix remains byte-identical to the November 10 historical witness; the new event appends, not rewrites it.

Comparing the fifth and sixth accepted Candidate snapshots at **source_id+path** grain yields **15/15 identical selected document content SHA-256**. Three upstream repository revisions (CWL, SEEK, WorkflowHub) and related Git tree identities moved, while the selected LifeMonitor revision did not. The accepted knowledge graph remains **17 entities / 26 relations**, with three reviewed topics and 15 matched records. This proves bounded source-provenance continuity; it does **not** prove an altered biological claim, provider registry approval or a new scientific result.

## AUDIT · Actual failure and correction boundary

[PR #79](https://github.com/lostlight530/life-science-ecosystem-lab/pull/79) is a 23-file bilingual documentation **Draft** touching `docs/` and three Framework documentation paths, not `data/` or executable assets. Its current head `da80177131449ac55df874a64bc5174fc22c5509` produced four failed Runs:

- [43919536363](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43919536363), Evidence Push Job failed
- [43919549660](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43919549660), Repository contracts **failed** and aggregate validate **failed**, while the other three domain Jobs succeeded
- [43919549686](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43919549686), independent Evidence PR Job failed
- [43919549907](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43919549907), project-custom self-check Job failed while the independent institutional-defaults Job succeeded

The underlying repeated failure is **`tests/test_post_798_run_delta.py::test_accepted_state_unchanged_and_valid`**: frozen November 10 evidence asserts `(5 receipts, 4 archives)` against the **current mutable** repository `data/` now at `(6, 5)`. The failing tests' 290-case suite reported **one failed test**, not six corrupted receipts. This is an **as-of/time-grain contract error**, not demonstrated corruption of native accepted state.

**Correction policy:** retain the original five-event as-of numbers and frozen Blob SHA; compare that hash to the **first five events' exact original bytes**, allow verified later append-only events, and run the independent current-state verification plus receipt/archive whitelisting. Do not change historical snapshots, erase failed Jobs, edit accepted `data/`, disable the gate or fake provider verification. Independent code review/PR CI is still required before merging any repair.

Historical negative controls also remain: cancelled [Run 43210854941](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43210854941) had a failed Repository contracts Job; successful [Bio Run 43266573648](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43266573648) had a conditionally skipped `pinned-field` Job. A later green run does not delete those prior observations.

## REVIEW / REPLAY · Scientific and institutional limits

The existing institution-default checker is a bounded public HTTP observation, not LS Login, WorkflowHub, LifeMonitor, OpenEBench, FAIRDOMHub, bio.tools or Zenodo certification. Those providers' **current individual authoritative object/version/status** were not fully revalidated in this repository-only census: **UNKNOWN**. The actual private identity and unseen runtime of named Agents are also **UNKNOWN**, separate from Git authorship and reviewed PR contents.

Reproduce the two frozen-to-live contracts without requiring any LLM, API key, external Agent, network or new science data:

```sh
python -m unittest tests/test_post_798_run_delta.py -v  # only if tests package import is supported
python -m unittest discover -s tests -v
python -m unittest discover -s framework/tests -v
python -m life_science_ecosystem_lab state verify --repository-root . --require-accepted
```

Use `python -m unittest discover -s tests -p 'test_post_798_run_delta.py' -v` when a direct dotted module path is unavailable. CI also independently tests Evidence, Bio, Knowledge/CWL, Framework Linux/Windows and portable package boundaries according to their actual workflow triggers. None of these tests establishes biological truth.

**Disposition at frozen source cutoff:** `RESEARCH_NONCLAIM` / `CORRECTION_REQUIRED_FOR_CI` / `PRODUCTION_STATE_PRESERVED` / `EXTERNAL_STATUS_UNKNOWN`. The historical archive and all original correction records are append-only in intent; this document does not retroactively change older reports.
