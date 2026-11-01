# Post-628 history, native Job and scientific-boundary reconciliation · 2026-11-02

[Frozen 12-Run observation](post-628-to-640-observation-2026-11-02.json) · [Previous 628-Run snapshot](POST_614_TO_628_RECONCILIATION_2026-11-01.md) · [Original root-to-present replay](FULL_HISTORY_REPLAY_2026-10-31.md) · [Public lessons](../lessons/2026-11-02-job-gates-and-evidence-visibility.md) · [Independent offline falsifier](../../tests/test_post_628_run_delta.py)

**Source boundary:** read-only GitHub API observation reviewed on the 2026-11-02 Asia/Shanghai date, with source main `efc8355c130cbb54111f3a0907fdec79f116a122` (merged PR #53 on 2026-11-01 11:31:56 UTC). Seven paged Actions responses returned `100/100/100/100/100/100/40`. An independently recorded exact UTC HTTP-read timestamp was not furnished: **UNKNOWN**. The individual Run `created_at` values are not substituted for that clock. Publishing this observation will itself generate later Git/PR/CI records outside its fixed denominator.

## DEFINE → PIN → QUALIFY

Question: Did the 628 previously archived visible Run identities survive into a newer population, and do the additional Jobs, accepted-state guards and external-object distinctions support any new scientific assertion?

PIN [the original 598-row census](full-history-census-2026-10-31.json), the [598→614 delta](post-598-to-614-observation-2026-10-31.json) and the [614→628 delta](post-614-to-628-observation-2026-11-01.json) as immutable observations. They remain unedited, including eight archived failed Runs, 134 corrected temporal workflow-name attributions, two historical schedule median corrections and the November 1 clock conflict. QUALIFY Git commits, PR records, Run IDs, Job conclusion/steps, artifact metadata, the formally accepted `data/` Git blobs and external registrations as **different** evidence classes.

## EXECUTE → EVALUATE: observed identity and count delta

| Item | Prior fixed observation | Fresh observed population | Interpretation |
| --- | ---: | ---: | --- |
| Main-reachable Git commits | 244 | **245** | +1 PR #53 merge; parent-closed DAG to `00009a38bc136a7c245270770b005e4e102a870d` |
| PR objects | 52 | **53** | 51 merged, **#29 and #32 closed-unmerged**, zero open |
| Version-controlled Git blobs | 255 | **259** | Four files added through PR #53; untruncated tree |
| Workflow definitions | 9 | **9** | GitHub Actions are infrastructure, not a new research asset |
| Currently visible Actions Runs | 628 | **640** | All previous 628 unique Run IDs retained; 12 new unique Runs |
| Currently visible conclusions | 587 success / 41 cancelled / 0 failed | **599 / 41 / 0** | All 12 new Runs successful |
| Event types | 310 push / 279 PR / 35 schedule / 4 dispatch | **319 / 282 / 35 / 4** | +9 push, +3 PR; **no new schedule or dispatch** |
| Accepted Knowledge Receipts / events | 3 / 3 | **3 / 3** | No new production acceptance |
| Archived Candidates / Releases | 2 / 2 | **2 / 2** | No automatic Release/DOI requirement |

All 12 added Run IDs, exact per-run workflow path, head SHA, trigger and UTC source timestamp are in the linked machine record; no prior frozen page was overwritten. The 245 commits are **main-reachable Git ancestry**, not all objects on all branches. The earlier eight failed Runs remain archived historical negative evidence despite the present 640-visible set reporting zero failures.

## AUDIT: newest Jobs and schedule integrity

The 12 new Runs are exclusively PR #53 development, validation and merged-main CI: **21 successful Jobs + 1 skipped Job**, based on direct GitHub latest-attempt Jobs responses. Six branch Evidence push Runs contributed 6 successes; the three PR Runs contributed 8 successes; the three merged-main Push Runs contributed 7 successes and one conditional skip.

| Latest merged-main Run | Verified outcome / important distinction |
| --- | --- |
| [41302293885](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41302293885) · integrated validation | Five Jobs success: Evidence, Repository contracts, Knowledge, Portable package, validate; observed 204 Python regressions in Repository contracts and reproducible CWL synthetic replays |
| [41302293913](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41302293913) · Evidence | One Job success, original artifact `13082076854` and GitHub-reported ZIP SHA-256 recorded in the machine file |
| [41302294001](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41302294001) · Bio | `offline` Job success; `pinned-field` Job `skipped` by event gate, **not** Bio field validation |
| [41302202062](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41302202062) · PR Bio | `offline` and `pinned-field` Jobs both success; the field check is independent of the skipped main-Push job |

The scheduled population remains **35 completed-success Runs / 54 successful Jobs**: continuity 16, daily independent two-plane check 15×2, Knowledge weekly 2×2 and Bio weekly 2×2. The latest directly inspected daily [41287694940](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41287694940) and continuity [41301526739](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41301526739) were already included in the 628 snapshot. No further scheduled Run appeared in this observed delta; do not assert missed schedules or future run success.

A job's API `skipped` conclusion must remain `skipped` even if its enclosing Run is `success`. Retrieving that skipped Job's logs returned a `BlobNotFound/404` through the connector in this review: **log read unavailable; causal explanation UNKNOWN**, not proof that the Job secretly failed. Runner logs also include Node.js 20 compatibility/deprecation warnings without a demonstrated failing Job. The previously documented November 1 one-hour API/log timestamp conflict remains open and should not be automatically attributed to scheduler defects or DST.

## EVALUATE → AUDIT: accepted state and external independence

Ten Git Blob SHA guards for the authoritative current Candidate, accepted Knowledge/Graph/Memory and three Receipts were re-read from the untruncated live main tree; paths and identities are retained in the machine record. The three accepted Git-backed Receipts and chained `APPLIED` event lines correspond to October 17 `INITIAL_SNAPSHOT`, October 19 and 26 `DOCUMENT_TEXT_UNCHANGED`. There are two older Candidate archives. This validates bounded continuity against the recorded state **but not** scientific ontology, causal inference or a new accepted Knowledge snapshot.

Accepted Knowledge remains the four approved upstream GitHub sources / 15 selected documents / three configured topics / 17 graph entities / 26 `SOURCE_MATCH` relations. The matching edges are source citations, not 26 independently established biological discoveries. Knowledge Workflow, Evidence Tool, Bio Tool and optional Framework each retain their separate contracts; external Agents remain `PROPOSAL_ONLY`.

GitHub has two Releases (`v0.4.0`, `v0.5.0`), while a separately observed public WorkflowHub workflow page shows its own `v0.4.0` registered version. These version clocks are independent. Neither a website listing, a GitHub Release, a LifeMonitor UI badge nor bio.tools/OpenEBench records is a proof of current cross-platform parity, independent institutional endorsement or scientific validity. Direct authenticated external-registry reconciliation was not established in this review.

## REVIEW → REPLAY: disposition and limits

Run `python -m unittest discover -s tests -p 'test_post_628_run_delta.py' -v`. This independently checks frozen 598+16+14+12 Run identity closure, event/result/job arithmetic, accepted three-Receipt/three-event boundary, and current Git Blob guards without calling the network or a model. It cannot re-enact the original cloud jobs or certify their scientific outputs.

**Decision:** three research assets `NO_CHANGE_REQUIRED`; optional Framework `NO_CHANGE_REQUIRED`; Actions and schedules `NO_CHANGE_REQUIRED`; formal `data/` `NO_CHANGE_REQUIRED`; public provenance `MATERIAL_OBSERVATION_APPEND_ONLY`; biological claims `NO_NEW_VERIFIED_CLAIM`. No new DOI, Release, forced data write or external platform registration. Unknowns include exact HTTP observation instant, runner clock discrepancy causality, skipped-Job log retention mechanics, historic removed-run mechanism and current independent registry synchronization.
