# Source-scoped GitHub provenance & native quality · 915 → 932 · 2026-11-22

[17-Run / 31-Job evidence JSON](post-915-to-932-observation-2026-11-22.json) · [Previous frozen review](POST_889_TO_915_RECONCILIATION_2026-11-20.md) · [Retention / denominator failure lesson](../lessons/2026-11-20-run-retention-and-denominator-drift.md) · [Eight-stage method](../RESEARCH_METHODOLOGY.md)

**DEFINE / PIN.** Bounded public GitHub research-software maintenance observation, not a biological experiment. Source `main` [`36cd0b14a8d0dd13fd36a506be2d85e6e500c79f`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/36cd0b14a8d0dd13fd36a506be2d85e6e500c79f), original root `00009a38bc136a7c245270770b005e4e102a870d` (2026-10-16), latest included Run created **2026-11-22T12:40:38Z**. Ten current GitHub Actions pages, five main commit pages, current Git tree, 82 PR objects, three Releases, 17 new Run latest-attempt Jobs and accepted `data/` state were independently read. Individual request acquisition timestamps were not recorded. The later PR and its resulting Actions are deliberately excluded.

## QUALIFY · Attribution, original negatives and software assets

- Main reaches one root through **325 Git commits with all parents present**, 347 tracked Blob paths / 51 directory entries, **398 recursive Git entries**. Prior Nov 20 frozen observation: 317 commits, 343 Blob paths / 394 total entries. These are Git object metrics, not biological experiments
- **82 PRs**: 78 merged, four closed-unmerged **#29/#32/#67/#78**, zero open. Public Releases remain `v0.4.0`, `v0.5.0` and `v0.5.1`
- Knowledge Workflow, Evidence Tool and Bio Tool are **three independent established software assets**. `framework/` is an experimental separate engineering-contract implementation. Nine native GitHub Workflow YAML files are execution infrastructure, not nine assets. External Agent self-attribution does not establish independent identity or production authority
- Four historically failed Run IDs (**43919536363 / 43919549660 / 43919549686 / 43919549907**) remain frozen failure evidence even though all four returned **404** on fresh individual lookup. Neither deletion cause nor actor is established

## EXECUTE · Compare the previous 915 and current 932 API populations

| Measure | Frozen previous visible | Current visible | Interpretation |
| --- | ---: | ---: | --- |
| Parent Run IDs | 915 | **932** | Net +17 |
| Success | 864 | **881** | +17 |
| Cancelled | 51 | **51** | No visible numerical change |
| Failure in currently visible population | 0 | **0** | Not historically zero |
| Scheduled Runs | 76 | **83** | +7 |
| Push / PR / schedule / manual | 462 / 373 / 76 / 4 | **469 / 376 / 83 / 4** | +7 / +3 / +7 / 0 |

Exactly **17 post-cutoff Run IDs**: **7 push / 3 pull_request / 7 schedule**, all parents successful. Their **31 latest-attempt Jobs contain 30 success and 1 skipped**. The Bio Push [Run 44673561781](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/44673561781) succeeded with offline verification, but Job `136079944159` (`pinned-field`) was conditionally `skipped`. A successful parent does not imply all children ran. The count difference and post-cutoff IDs do **not** independently prove an exact set join of the older 915 IDs; preserve the previous frozen archive rather than overwriting it.

## EVALUATE · Per-day native execution and schedule clocks

Prior scoped audit: **76 scheduled Runs / 118 latest-attempt successful Jobs**. Seven new scheduled Runs add **11 successful Jobs** for **83 scheduled Runs / 129 Job successes** in the current bounded population. Workflow totals: Daily self-check **36**, accepted-state continuity **37**, weekly Knowledge **5**, Friday Bio QA **5**.

| UTC day | Native workflow | Run ID | Run created UTC | Nominal Cron → created offset |
| --- | --- | ---: | --- | --- |
| 2026-11-20 | Daily | [44708588937](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/44708588937) | 09:11:21 | +07:30:21 |
| 2026-11-20 | Bio QA | [44715660705](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/44715660705) | 10:01:33 | +07:42:33 |
| 2026-11-20 | Continuity | [44741605920](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/44741605920) | 13:07:51 | +08:50:51 |
| 2026-11-21 | Daily | [44886413448](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/44886413448) | 08:46:06 | +07:05:06 |
| 2026-11-21 | Continuity | [44905603255](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/44905603255) | 12:46:58 | +08:29:58 |
| 2026-11-22 | Daily | [45004651729](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/45004651729) | 08:50:12 | +07:09:12 |
| 2026-11-22 | Continuity | [45023517759](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/45023517759) | 12:40:38 | +08:23:38 |

Exact native Cron clocks are 01:41 UTC (Daily), 04:17 UTC (Continuity), 03:23 UTC Monday (Knowledge), and 02:19 UTC Friday (Bio). These **created_at minus nominal cron** gaps are observations of schedule offset, **not independently measured queue latency**, and their cause remains **UNKNOWN**.

## AUDIT · Research-state quality and nonclaims

Current `main/data` contains six Git-accepted Receipts / six `APPLIED` Event records with consistent `previous_event_sha256` adjacency, plus five archived previous Candidates. Last accepted Run [`gh-43859884737-1`](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43859884737) is dated 2026-11-16, `DOCUMENT_TEXT_UNCHANGED`. Persistent Knowledge graph has **17 entities / 26 `SOURCE_MATCH` relations**. No seventh acceptance, new bio experiment or independently verified scientific discovery is observed in the newly inspected period. Event-field chain readback is less than a full independent byte/digest verification.

The three scientific software assets, Framework, approved sources/topics, Actions schedules, and formal `data/` were not modified by this audit. Synthetic CWL replay, protein FASTA/PDB metadata quality, Agent proposals, provider registry pages and scientific acceptance are distinct evidence authorities.

## REVIEW / REPLAY · Corrections, uncertainty and disposition

- Preserve earlier 404 historical failure identities and the cancelled-parent/failed-Job and successful-parent/skipped-Job counterexamples. A currently green list does not revise old outcomes
- Do not infer a scheduler bug, GitHub provider outage or any actor from observed Cron clock offsets or unavailable historical Runs
- Offline verify this **frozen** JSON through `python -m unittest discover -s tests -p test_post_915_run_delta.py -v`; future live Run growth and legitimate new native accepts must not invalidate an old source-cutoff observation
- Individual API acquisition times, exact old-ID set persistence, original expired Runner logs and current external bio.tools / WorkflowHub / OpenEBench / Zenodo / LifeMonitor provider state are **UNKNOWN** unless separately witnessed
- This source-scoped engineering review does not issue new Releases, DOI, registry claims, production writes or biological conclusions

**Disposition:** `PROVENANCE_DELTA_DOCUMENTED / PRODUCTION_STATE_UNCHANGED / SCIENTIFIC_NONCLAIM / EXTERNAL_PARTIAL`
