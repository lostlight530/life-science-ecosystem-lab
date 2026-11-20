# Source-pinned native quality and Git reconciliation · frozen 889 → visible 915 · 2026-11-20

[Machine-readable 30-Run / 63-Job witness](post-889-to-915-observation-2026-11-20.json) · [Prior immutable 868→889 archive](POST_868_TO_889_RECONCILIATION_2026-11-17.md) · [Public retention lesson](../lessons/2026-11-20-run-retention-and-denominator-drift.md) · [Eight-stage method](../RESEARCH_METHODOLOGY.md)

**DEFINE / PIN.** This is a GitHub repository and scientific-software maintenance *observation*, not a new biological experiment. The public repository is `lostlight530/life-science-ecosystem-lab`; source `main` is [`fe03f5bd935c0d64b90fb217feac40f0f15ce078`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/fe03f5bd935c0d64b90fb217feac40f0f15ce078), after [merged PR #81](https://github.com/lostlight530/life-science-ecosystem-lab/pull/81). The last included GitHub Run was created **2026-11-20T03:59:54Z**. We retrieved all ten pages of currently visible Runs and all four pages of main commits. Individual HTTP acquisition timestamps were not captured. All clocks below are UTC unless specified; the review logical day is **2026-11-20 Asia/Shanghai**.

## QUALIFY · Four incompatible evidence authorities

- **Git ancestry** starts at [root `00009a38bc136a7c245270770b005e4e102a870d`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/00009a38bc136a7c245270770b005e4e102a870d) on **2026-10-16**. The February predecessor/Jules attribution in PR #1 is distinct and does not extend this repository's Git DAG or authenticate a private Agent run
- **Current repository:** 317 unique main-reachable commits with all parents resolved to the one root; 289 distinct Git Trees; 343 tracked Blob paths (394 recursive Git Tree entries including directories). Compared with the previous pinned 302 / 276 / 339, the respective changes are **+15 commits, +13 distinct trees, +4 living paths**. These are engineering identities, not research experiment counts
- **PR and release population:** 81 PR objects, 77 merged, four closed-unmerged **#29/#32/#67/#78**, zero open. [#80](https://github.com/lostlight530/life-science-ecosystem-lab/pull/80) corrected frozen-test/live-state drift, [#79](https://github.com/lostlight530/life-science-ecosystem-lab/pull/79) merged bilingual professional documentation, and [#81](https://github.com/lostlight530/life-science-ecosystem-lab/pull/81) linked the existing `v0.5.1` archive without modifying scientific data. Public GitHub Releases remain exactly `v0.4.0`, `v0.5.0`, `v0.5.1`
- **Asset ownership:** Knowledge Workflow, Evidence Tool and Bio Tool remain three independently callable established software assets. The separately installed `framework/` is an experimental software-contract Framework; the nine native Workflow YAMLs are execution infrastructure, not nine products. External Agents are proposal/review collaborators, not runtime or registry authorities

## EXECUTE · Compare frozen population with the actual current API

| Unit and source | Frozen 2026-11-17, 889 Runs | Current API at bounded cutoff | Interpretation |
| --- | ---: | ---: | --- |
| Currently/frozen visible unique Run IDs | 889 | **915** | The two populations differ by additions **and** historical disappearance |
| Parent success | 834 | **864** | +30 successful new Runs |
| Parent cancelled | 51 | **51** | Same number; not equivalent to all Jobs passing |
| Parent failure in the respective visible population | 4 | **0** | **Four old failed Runs no longer appear**, not four repaired outcomes |
| Scheduled Runs | 70 | **76** | +6, all successful in current visible population |
| Parent event counts: PR / push / schedule / manual | 367 / 448 / 70 / 4 | **373 / 462 / 76 / 4** | Deleted Run events and added events must be reconciled separately |

**Exact set arithmetic:** `889 − 4 unavailable historical failure IDs + 30 post-cutoff new unique Run IDs = 915 currently visible`. The frozen 889 source, the newly observed 30 IDs, and the four unavailable IDs are separate sets. New Runs comprise **15 push + 9 pull_request + 6 schedule**, all parent `success`; their **63 latest-attempt Jobs comprise 62 success + 1 skipped**, not 63 success. The skipped [Bio pinned-field Job `133728607991`](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43990225775) was conditionally omitted on a Push run; the Bio offline Job succeeded. Every new Run ID, SHA, event, time and Job ID is retained in the adjacent machine record.

**Historical failed identity preservation:** IDs [43919536363](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43919536363), [43919549660](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43919549660), [43919549686](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43919549686) and [43919549907](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43919549907) were recorded as `failure` with specific failed/skipped Jobs in the November 17 archived JSON. Their **individual GitHub GET requests now return 404**. This independently establishes present unavailability but does **not** identify the actor, deletion reason, missing original logs or any scientific interpretation. Keep the frozen failed Job IDs and causal repair evidence as historical truth; do not overwrite their verdicts

## EVALUATE · Daily native execution, latest-attempt Jobs, and clock boundaries

Every currently visible `schedule` Run was enumerated and its latest-attempt Jobs independently inspected:

| Native schedule | Run count | Job count | Latest-attempt Job outcomes |
| --- | ---: | ---: | --- |
| Daily self-check (institutional defaults and project custom independent) | 33 | 66 | 66 success |
| Daily accepted-state continuity verification | 34 | 34 | 34 success |
| Weekly Knowledge native lifecycle | 5 | 10 | 10 success; validate and guarded apply separated |
| Friday Bio QA | 4 | 8 | 8 success; offline and pinned-field separated |
| **All currently visible scheduled** | **76** | **118** | **118 success** |

The daily self-check's reviewed cron is `01:41 UTC`, continuity `04:17 UTC`, Knowledge Monday `03:23 UTC`, Bio Friday `02:19 UTC`. The actual scheduled Runs observed span October 17–November 19 UTC. **No November 20 schedule result is presumed absent or failed from an incomplete observation day.**

| Scheduled day | Run ID | Type | Created UTC | Nominal-to-created offset |
| --- | --- | --- | --- | --- |
| Nov 17 | `44058293652` | self-check | 09:44:13 | +08:03:13 |
| Nov 17 | `44094378063` | continuity | 13:36:15 | +09:19:15 |
| Nov 18 | `44273143027` | self-check | 09:08:36 | +07:27:36 |
| Nov 18 | `44311104573` | continuity | 13:10:59 | +08:53:59 |
| Nov 19 | `44496929532` | self-check | 09:29:48 | +07:48:48 |
| Nov 19 | `44533617045` | continuity | 13:27:23 | +09:10:23 |

These are `created_at − nominal cron clock` differences, **not** measured GitHub scheduler queue or runner latency. Cause is **UNKNOWN**. A parent's success never erases nested negative controls: cancelled [Run `43210854941`](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43210854941) contains failed Repository contracts Job `131157765073`; successful [Bio Run `43266573648`](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43266573648) contains skipped pinned-field Job `131351616613`.

## AUDIT · Accepted research data and scientific non-claims

Read-back of current `main/data` confirms **six Git-backed Receipts**, **six ordered chained `APPLIED` Events**, and **five previous Candidate archives**. Every later Event's `previous_event_sha256` matches its predecessor in the current `events.jsonl` sequence. Latest native execution [`gh-43859884737-1`](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43859884737) was November 16, with successful `validate` and `apply` and `change_kind=DOCUMENT_TEXT_UNCHANGED`. The accepted graph remains **17 entities and 26 `SOURCE_MATCH` relations**. Historical source re-pinning without selected-text change is **not** a new biological discovery. Full byte-digest/replay assurance still belongs to the repository's own state verification tests and immutable Git objects, not to merely counting receipts.

The three established tools and independent Framework were not modified by this read-only observation. Historical Agent proposals, software-contract Challenges, synthetic CWL replay, real sample formats, research-data analysis, external registry entries and scientific or institutional certification retain their different assurance levels.

## REVIEW / REPLAY · Corrections and remaining unknowns

- **Earlier correction:** PR #80 fixed a November 10 frozen-cardinality assertion incorrectly applied to an authorized sixth live Event; this is a temporal test-oracle error, not proof of data corruption. Preserve its failed PR #79 intermediate checks and the historical correction chain
- **Public provider state:** [WorkflowHub workflow 2347](https://workflowhub.eu/workflows/2347) exposes a versioned `v0.4.0` CWL record with `Work-in-progress` and `Tests Passing` labels, which are *provider-specific record fields*, not external scientific validation. Fresh individual bio.tools, OpenEBench, Zenodo/DOI and LifeMonitor state is **UNKNOWN** unless independently re-read with object-specific evidence. No new external writes or enrollments are asserted
- **Privacy and retention:** only public Run, Job, Git, PR and source-scoped diagnostic facts are published. No private discussion, personal deletion attribution, credentials, Agent prompts, unpublished study plans or raw third-party scientific data are included
- **Operational state:** no source registry, Knowledge/Evidence/Bio runtime, Framework source, native schedule, accepted `data/`, release or DOI changes are required. This source-pinned review does not itself execute new biological measurements or grant a write/claim permission

**Recheck:** `python -m unittest discover -s tests -p 'test_post_889_run_delta.py' -v` tests this *frozen* ledger offline, while full project CI tests independently check current runtime/software contracts. The review disposition is **PROVENANCE_DELTA_DOCUMENTED / PRODUCTION_STATE_UNCHANGED / SCIENTIFIC_NONCLAIM / EXTERNAL_PARTIAL**. If a newer Run arrives, produce a new separately dated observation rather than silently changing this denominator
