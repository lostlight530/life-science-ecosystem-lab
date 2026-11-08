# Post-768 → 788 native GitHub audit · Jobs, clocks and accepted-state continuity (2026-11-08)

[Machine-readable source observation](post-768-to-788-observation-2026-11-08.json) · [Frozen 768-run predecessor](post-758-to-768-observation-2026-11-07.json) · [Offline regression](../../tests/test_post_768_run_delta.py) · [Public failure-mode lesson](../lessons/2026-11-08-green-checks-are-not-scientific-acceptance.md)

**DEFINE / PIN / QUALIFY:** 2026-11-08 Asia/Shanghai review; immutable source `main=503c340f9d5d4b34b8aacb6df6fd680567445b00`, root `00009a38bc136a7c245270770b005e4e102a870d`. GitHub eight Actions pages, three main Commit pages, all PRs, recursive Tree, each new Run's latest-attempt Job list, selected scheduled Job logs, Artifact lists and four accepted `data/` Receipts were reviewed. The original February 15–16 predecessor is historical self-attribution, **not** an independently recovered LS Git ancestor or Agent runtime attestation. Individual HTTP acquisition clocks were not recorded, so GitHub Run `created_at` must not be treated as observation, dispatch or runner time

## EXECUTE / EVALUATE · comparable populations

| Unit | Previous 2026-11-07 snapshot | This source cutoff | Interpretation |
| --- | ---: | ---: | --- |
| API-visible distinct Actions Runs | 768 | **788** | All 768 prior IDs retained; 20 new |
| Visible outcomes | 727 success / 41 cancelled | **747 success / 41 cancelled** | All 20 added Runs succeeded; old red history remains in frozen archives |
| Event categories: schedule / push / PR / dispatch | 47 / 396 / 321 / 4 | **51 / 406 / 327 / 4** | No duplicate scientific-experiment inference |
| Added latest-attempt Jobs | — | **40 success / 2 skipped / 0 failed** | 42 Jobs for 20 Runs, two Bio post-merge push gates skipped by design |
| Main-reachable Commits | 259 | **261** | Exactly PR #68 and #69 merged since prior main |
| Main tracked blobs | 305 | **312** | Historical current-tree count, not 312 scientific datasets |
| PR objects: merged / closed-unmerged / open | 64 / 3 / 0 | **66 / 3 / 0** | #29, #32 and #67 remain closed-unmerged |
| Formal Knowledge receipts / events / input archives | 4 / 4 / 3 | **4 / 4 / 3** | No fifth production acceptance |

The 20 added Run IDs and all 42 Job IDs, branches, source commits, outcomes and GitHub creation clocks are in the machine record. PR #68/#69 and their branch, PR, and main push checks are **software change review** — not independent biological experiments. The two skipped Jobs are Bio `pinned-field` on `push` Runs [42343880958](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42343880958) and [42369007585](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42369007585); the pinned-field gate is intentionally restricted to PR, schedule or dispatch. No inference that those two pushes re-audited external protein samples is allowed

## AUDIT · daily native Runs and time provenance

| Shanghai day | Class | Run / separately verified Job evidence | GitHub created_at UTC | Nominal UTC | Created−nominal |
| --- | --- | --- | --- | --- | --- |
| Nov 7 | Institutional + project self-check | [42352695753](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42352695753) · 2 success | 07:46:53 | 01:41:00 | **06:05:53** |
| Nov 7 | Accepted-state continuity | [42366998260](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42366998260) · 1 success | 11:09:45 | 04:17:00 | **06:52:45** |
| Nov 8 | Institutional + project self-check | [42460920843](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42460920843) · 2 success | 07:58:17 | 01:41:00 | **06:17:17** |
| Nov 8 | Accepted-state continuity | [42475429538](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42475429538) · 1 success | 11:22:01 | 04:17:00 | **07:05:01** |

The official-reference and project-owned custom Jobs run independently. Nov 8 project log reports all eleven local bounded checks `PASS`; institutional log records `INSTITUTIONAL_PUBLIC_DEFAULTS_SELF_CHECK PUBLIC_HTTP_READ_ONLY`, **not** external-provider accreditation or unqualified availability. Continuity logs report `state is valid`, `knowledge provenance and content verified`, graph integrity (17 entities, 26 SOURCE_MATCH relations, four events) and `KNOWLEDGE_QUALITY_PASS`. Nov 8 job log and artifacts were retrieved: institutional `13609710915`, custom `13610205011`, continuity `13615495908`. For Nov 7 corresponding artifact IDs are `13565884988`, `13566580021`, `13571927477`. Job logs include non-fatal Node.js runtime deprecation warnings; no failure or specific provider outage is inferred

Across **dated** audits, schedule coverage is now 51 visible scheduled Runs with 79 separately checked successful Jobs (prior 47/73 + new 4/6), not a single-session re-download of all historical logs and not an expected-cadence success rate. The several-hour gaps are `created_at − nominal cron`; trigger/dispatch/queue/runner causal attribution remains **UNKNOWN**. Friday Bio QA [42194936143](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42194936143) and Monday native production [41436556408](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41436556408) remain prior separately audited schedule/acceptance objects — this new 20-Run window contains **no new Bio Friday schedule or native Monday production schedule**

## AUDIT / REVIEW · state and negative controls

The current Git Blob identities of `data/knowledge/events.jsonl`, `data/knowledge/current.json`, `data/knowledge/graph-manifest.json` and last receipt remain unchanged from the previous accepted state. Four receipts correspond to Oct 17, Oct 19, Oct 26, Nov 2 `APPLIED`, with the latter three `DOCUMENT_TEXT_UNCHANGED`: provenance-version acceptance is not new biological content. `data/inputs/archive/` has three actual saved Candidate snapshots. No manual `persist=true` call was made by this review

Keep the older disappeared failed Run IDs, including `42010968246`, `42010981438`, `42010981442`, `42010981547`, explicitly as historical negative evidence with cause of unavailability **UNKNOWN**. Present 747 green Runs are not a deletion or rewriting of the frozen failure observations. An unmerged #67 OSF-related branch cannot be upgraded into a registry or scientific acceptance claim by later green branch checks. GitHub main reports `protected=false` with public rulesets `[]` at this read, so green CI is not independent server-enforced review policy

External-provider states are separate: the two GitHub releases `v0.4.0` and `v0.5.0` exist, while WorkflowHub, bio.tools, OpenEBench, Zenodo and LifeMonitor require their own object-specific version/clock/approval evidence. This run did not independently reauthenticate any private external-provider account or verify a new external approval

## REPLAY / disposition

The [offline falsifier](../../tests/test_post_768_run_delta.py) reconstructs the prior 768 IDs from the frozen 758-ID census and next ten Run records, verifies all 20 new Run and 42 Job identities, four schedule offsets, frozen accepted Blob IDs, and the absence of a fifth Receipt. It does **not** rerun historical GitHub workflows or validate scientific conclusions

**Disposition:** `NO_PRODUCTION_CHANGE` · `DOCUMENTATION_AND_TEST_ONLY`. The historical 309-path taxonomy is frozen at its old source cutoff; its regression now explicitly permits subsequent scoped provenance/lesson/test paths while still checking all pinned archive and accepted-data bytes. No modifications to Knowledge Workflow, Evidence Tool, Bio Tool, Framework, native schedules, formal `data/`, releases or external provider state
