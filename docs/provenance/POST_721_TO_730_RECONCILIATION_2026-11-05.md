# GitHub Actions 721 → 730 · native quality and historical provenance, 2026-11-05

[Machine snapshot](post-721-to-730-observation-2026-11-05.json) · [Prior frozen 721 population](../taxonomy/POST_2026-11-04_SOURCE_CLASSIFICATION.md) · [Public lesson](../lessons/2026-11-05-cron-jobs-evidence-boundaries.md) · [Offline regression](../../tests/test_post_721_run_delta.py)

**Source cutoff:** `main=b21e453b3580ec5dc7450ee4fa1a986a51d522c6` before this reporting PR, 2026-11-05 Asia/Shanghai audit day. Eight GitHub API pages yielded **730 unique visible Run IDs** (page sizes 100×7 + 30). Exact per-request observation UTC timestamps were not independently recorded. Runs created by this document's own PR are not included.

## DEFINE → PIN → QUALIFY · reconstruct independent histories

Reconstruction of frozen Run-ID sources: original 598 + deltas 16 / 14 / 12 / 13 / 20 / 11 / 27 + Nov 4 taxonomy overlay 10 = **721 distinct historical-visible IDs**. All 721 were retained in today's API result; nine new IDs appeared. Current visible outcomes **689 success / 41 cancelled / zero currently visible failures**. Events **375 push / 309 pull_request / 42 schedule / four workflow_dispatch**. These are visible GitHub Run objects, not all-time immutable history or scientific experiments.

The remote `main` ancestry was independently fetched in three GitHub commit pages: **255 reachable commits**, one root `00009a38bc136a7c245270770b005e4e102a870d`, no missing parents. There are **62 PRs** (60 merged; #29 and #32 closed without merge; zero open), **290 tracked Git blobs** and **nine native Workflow YAMLs**. February 2026 precursor engineering is separate author-supplied lineage, not an October LS Git ancestor. PR titles and authors do not authenticate external Agent execution environments.

## EXECUTE → EVALUATE · exact nine-Run, 20-Job observation

| New Run | Event / workflow | Latest-attempt Jobs |
| --- | --- | --- |
| [41827751347](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41827751347) | `schedule` · `life-science-continuity.yml` | `verify` success |
| [41796192635](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41796192635) | `schedule` · `life-science-daily-selfcheck.yml` | `Project custom — three assets and accepted evidence` success; `Institutional defaults — public read-only observations` success |
| [41779069740](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41779069740) | `push` · `life-science-bio.yml` | `offline` success; `pinned-field` skipped |
| [41779069675](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41779069675) | `push` · `validate.yml` | `Evidence Tool` success; `Knowledge Workflow` success; `Portable package` success; `Repository contracts` success; `validate` success |
| [41779069648](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41779069648) | `push` · `life-science-evidence.yml` | `Verify evidence CLI, source contracts and docs` success |
| [41778963928](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41778963928) | `pull_request` · `validate.yml` | `Evidence Tool` success; `Repository contracts` success; `Knowledge Workflow` success; `Portable package` success; `validate` success |
| [41778963873](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41778963873) | `pull_request` · `life-science-bio.yml` | `offline` success; `pinned-field` success |
| [41778963871](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41778963871) | `pull_request` · `life-science-evidence.yml` | `Verify evidence CLI, source contracts and docs` success |
| [41778908804](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41778908804) | `push` · `life-science-evidence.yml` | `Verify evidence CLI, source contracts and docs` success |

**20 Jobs: 19 success, one conditionally skipped, zero failures.** Bio `push` Run 41779069740 skipped `pinned-field` under its versioned event guard, while the PR Bio Run 41778963873 ran that Job successfully. A successful workflow is not proof that all conditional Jobs executed.

| Scheduled Run | Nominal cron UTC | Run created UTC | Observed offset | Jobs |
| --- | --- | --- | --- | --- |
| [Daily #41796192635](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41796192635) | 11-04 01:41:00 | 11-04 08:00:20 | **+06:19:20** | Institutional and project custom success |
| [Continuity #41827751347](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41827751347) | 11-04 04:17:00 | 11-04 12:15:47 | **+07:58:47** | verify success |

Offsets are **cron-to-GitHub-API-run-creation**, not measured queue durations or proof of a platform fault. Previous Nov 3 offsets +06:53:18 and +07:44:44 remain in the earlier frozen audit. Two observation days do not establish causality or warrant a schedule change.

GitHub returned three artifacts (not downloaded/rehashed): `13305123572` project-custom, `13305078688` institutional-defaults, `13320720224` accepted-knowledge-continuity; exact GitHub-reported ZIP digests are in the JSON record. Run and Job success does not itself prove every project subcheck result or independent scientific correctness; examine attached reports for more granular claims.

## AUDIT → REVIEW · retain negative history and authority boundaries

Previously reported interim failed Run IDs `41776345499`, `41776379847`, `41776461093` still return 404 from direct GitHub API lookup. Their historical lower-grade observations, the original Oct 30 failures and PR #55 negative evidence must remain preserved. **Cause of 404 unknown**: neither operator identity, deletion mechanism nor platform incident is proven. Zero currently visible failures must never rewrite older evidence.

Four formal Git-backed **`APPLIED` Receipts**, four linked events, three Candidate archives, 17 knowledge entities and 26 document-topic **`SOURCE_MATCH`** edges remain unchanged. Latest native acceptance: `gh-41436556408-1`, logical 2026-11-02, `DOCUMENT_TEXT_UNCHANGED`. No new native apply, biological discovery, benchmark or independently verified external registry acceptance is evidenced by these nine Runs. `metadata/standards-status.json` retains historical source-graded provider observations; this review did not independently verify current WorkflowHub, LifeMonitor, bio.tools, OpenEBench, LS Login or Zenodo account-side status.

**Disposition:** `OBSERVED_OPERATIONAL_DELTA` for the nine Runs, conditional Job and two clock offsets; `NO_CHANGE_REQUIRED` for the Knowledge, Evidence, Bio, experimental Framework, Actions schedule, research profiles, Releases and accepted `data/`; `NO_NEW_VERIFIED_SCIENTIFIC_CLAIM` for science.

## REPLAY

`python -m unittest discover -s tests -p 'test_post_721_run_delta.py' -v` rechecks offline identity-set reconstruction, individual Run/Job outcomes, clock arithmetic, historical negatives, accepted-state count and public doc registration. It does not replay hosted historical Jobs, recover unavailable Runs, rehash archive ZIPs or authenticate external Agent execution.
