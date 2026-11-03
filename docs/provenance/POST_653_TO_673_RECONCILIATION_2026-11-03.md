# Post-653 GitHub run reconciliation and native quality closure · 2026-11-03

[Immutable 20-Run source-derived delta](post-653-to-673-observation-2026-11-03.json) · [Prior 653-Run cutoff](POST_640_TO_653_AND_NATIVE_ACCEPTANCE_2026-11-02.md) · [Independent offline falsifier](../../tests/test_post_653_run_delta.py) · [Public operational lesson](../lessons/2026-11-03-native-success-is-not-universal-execution.md)

**Observation boundary:** read-only GitHub repository, Git Tree, PR, Release, Actions and latest-attempt Jobs API observations assembled on 2026-11-03 Asia/Shanghai (assembly completed at `2026-11-03T03:09:22.200Z`). Source main was independently pinned as `22d6965e7236e058680fca529e8fc98faa17d5d9` before creating the review branch. The individual HTTP request timestamps are **UNKNOWN**; the assembly time is not the request time, and a GitHub Run's `created_at` is not a scheduler queue-duration measurement. This review PR and its CI lie **outside** the frozen 673-Run denominator.

## DEFINE → PIN → QUALIFY

Question: following the four-event native production lineage and the PR #55 / #56 corrections, do the later visible GitHub runs preserve prior identities, and do their per-Job results support another accepted scientific claim or a warranted executable-system change?

PIN the original October 30 raw census and subsequent additive 598 → 614 → 628 → 640 → 653 observations without rewriting any frozen record. The LS Git root remains `00009a38bc136a7c245270770b005e4e102a870d` on 2026-10-16; the independently documented February 15–16 predecessor engineering activity is **separate cross-repository evidence**, not LS Git ancestry or attested private Agent execution. QUALIFY Git commits, PRs, Runs, Jobs, formal accepted `data/`, external registries and scientific results as non-interchangeable evidence objects.

## EXECUTE → EVALUATE: old/new comparable census

Seven complete GitHub Actions pages returned `100/100/100/100/100/100/73` = **673 unique visible Run IDs**. All **653** IDs in the previous frozen cumulative population remained visible; exactly **20** previously unrecorded IDs were returned, with **14 push + 6 pull_request + 0 schedule** and all 20 Run conclusions equal to `success`. Exact identities, head SHAs, workflows, UTC event dates and conclusions are in the adjacent immutable JSON. The currently visible population comprises **632 successful / 41 cancelled / 0 failed** Runs, by trigger **340 push / 291 PR / 38 schedule / 4 workflow_dispatch**.

| Comparable GitHub object | 653-Run source cutoff | New 673-Run cutoff | Difference and meaning |
| --- | ---: | ---: | --- |
| Main-reachable Git commits | 247 | **249** | +2 merged PR commits, not new scientific experiments |
| PR objects | 54 | **56** | +2, PR #55 and #56 merged; #29 / #32 still closed-unmerged; zero open |
| Tracked Git blobs | 265 | **270** | +5; file-tree contents, not study count |
| Workflow definitions | 9 | **9** | Unchanged; Actions are execution infrastructure |
| Currently visible GitHub Runs | 653 | **673** | +20 successful, all PR-related development/integration |
| Visible scheduled Runs / their successful Jobs | 38 / 59 | **38 / 59** | No added scheduled run in this observation window |
| Accepted native Receipts / event lines / Candidate archives | 4 / 4 / 3 | **4 / 4 / 3** | No additional native production acceptance |
| GitHub Releases | 2 | **2** | `v0.4.0`, `v0.5.0` remain separate from external versions |

New PR #55 addressed a real frozen-history/live-state regression after native acceptance #4; PR #56 restored the original historical Git Blob verification against **pinned historical Trees** and added a live Receipt-tamper negative control. Do not reduce those corrections to `CI green`: they repair symmetric risks of rejecting valid new production and accepting corrupted current evidence. Neither PR changed accepted data, native tool runtime, Framework or schedule configurations.

## AUDIT: direct Job evidence and scheduled chronology

For **all 38 visible scheduled Runs**, a fresh latest-attempt GitHub Jobs read returned **59 successes**, with zero skipped/failed Jobs in that specifically scheduled set: 16 daily self-check Runs each with 2 successful independent institutional/project Jobs; 17 continuity Runs each with 1 successful `verify`; 3 weekly Knowledge Runs each with `validate` and `apply` successful; and 2 weekly Bio Runs each with `offline` and `pinned-field` successful.

The **20 newly visible PR-related Runs** yielded **38 latest-attempt Jobs**: **36 success / 2 skipped / 0 failure**. In particular the two merged-main Bio push Runs [41450087249](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41450087249) and [41453175179](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41453175179) each had `offline=success` and `pinned-field=skipped` by the declared event gate. Their PR Bio runs [41449867703](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41449867703) and [41453009000](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41453009000) had both Jobs successful. **Run success must never be promoted into proof that a skipped Job executed.**

The latest merged-main [integrated CI Run 41453175001](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41453175001) had five successful Jobs; its Repository contracts log reported **214 Python tests passed**, **37 experimental Framework tests passed**, and local RO-Crate, metadata and publication-boundary preflights (not external certification). The latest merged-main Evidence and Bio Runs were also successful at their executed Jobs.

The Nov 2 native weekly [Knowledge Run 41436556408](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41436556408) already accepted the fourth real event. [Continuity Run 41445992506](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41445992506) subsequently succeeded. The native latest receipt is `gh-41436556408-1`, outcome `APPLIED`, change kind `DOCUMENT_TEXT_UNCHANGED`. The four approved GitHub sources and fifteen selected files still project to three topics, seventeen graph entities and twenty-six `SOURCE_MATCH` edges: neither the fourth acceptance nor source-version movements prove a new biological claim.

The Nov 3 daily cron (`01:41 UTC`) had not generated a visible new Run at the **early** API assembly cutoff; prior observations show substantial cron-to-created offsets, so this is **NOT_YET_VISIBLE / UNKNOWN**, not an established missed schedule. Do not launch a duplicate schedule to manufacture a pass. The historical Nov 1 API/Runner clock discrepancy and delay causality remain unresolved.

## AUDIT: negative evidence, registry authority and operational risk

The October 30 frozen census preserves **eight failed Runs**, even though none appears in today's currently visible 673. PR #55's documented three unintended intermediate failing branch checks (IDs `41449357390`, `41449363257`, `41449370818`) each returned **404** on direct current individual Run fetch. This establishes present unavailability, **not** the deletion actor, retention reason, error disappearance or scientific failure. Their original correction trail remains in [the preceding lesson](../lessons/2026-11-02-frozen-history-vs-live-state.md) and PR #55; do not silently add these three to the older fixed eight or misattribute them to the 653 snapshot.

Direct GitHub main metadata reported `protected=false`, and the repository ruleset endpoint returned `[]`; green CI therefore remains a tested engineering gate, **not proven server-enforced merge/write protection**. Administrative protection requires separate owner action and independent verification.

An external public [WorkflowHub workflow #2347](https://workflowhub.eu/workflows/2347) page continues to display registered version 2 / v0.4.0 and `Work-in-progress` with a `Tests Passing` badge. This is the external workflow object's displayed status, not the current GitHub v0.5.0 version, a scientific certification or a new release. A fresh independent API read of the bio.tools, OpenEBench and Zenodo tool/record endpoints was unavailable here, and LifeMonitor's authenticated account state was not accessed; their present synchronization remains **UNKNOWN**. Existing registered-object metadata and versioned source remain intact.

## REVIEW → REPLAY: disposition

**Three peer scientific software assets: NO_CHANGE_REQUIRED** · **Optional independent Framework: NO_CHANGE_REQUIRED** · **Native workflows/schedules: NO_CHANGE_REQUIRED** · **Accepted production `data/`: NO_MANUAL_CHANGE** · **Public provenance: APPEND_ONLY** · **New science claims / DOI / Releases: NONE**

Replay the [new isolated offline unit tests](../../tests/test_post_653_run_delta.py), then the full repo CI, independent Bio/Evidence and integrated validation on the PR head. The archive tests old ID identity closure and arithmetic, while native `verify_state(require_accepted=True)` separately checks the evolving actual production ledger; historical evidence and live-state validation must never be conflated. Leave independent first-party and third-party records alone unless a specific source-verified defect warrants a separately authorized fix.
