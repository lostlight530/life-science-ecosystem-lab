# Post-PR64 file-history and native Run closure · 2026-11-05

[Exact source-pinned JSON](post-730-to-750-observation-2026-11-05.json) · [Prior first-day full Tree register](../taxonomy/FULL_FILE_LIFECYCLE_2026-11-05.md) · [Independent offline test](../../tests/test_post_730_run_delta.py)

**DEFINE → PIN → QUALIFY:** Git origin `00009a38bc136a7c245270770b005e4e102a870d` (2026-10-16), observed main `c2ac76e630e11d723a15a56b5c36d0118fdbe491` after [PR #64](https://github.com/lostlight530/life-science-ecosystem-lab/pull/64), review day 2026-11-05 Asia/Shanghai. Exact per-request UTC collection times were not recorded. This is a read-only GitHub-source engineering observation, not a new scientific result or production acceptance

## EXECUTE · file objects from the first day to post-publishing main

The [complete historical register](../taxonomy/full-file-lifecycle-2026-11-05.json) pins **256 parent-closed main-reachable Commits, 235 distinct Git Trees, 294 currently tracked paths and 47 historical-only paths**, at pre-publication main `18c33998a78ff64537d993bd7d7408c5a5da0cf3`

The merged PR #64 produces exactly **one additional main Commit** and compares against that same prior state as follows:

| Object | Prior cutoff | New main source cutoff | Attribution boundary |
| --- | ---: | ---: | --- |
| Root-reachable Commits | 256 | **257** | One merged PR #64 commit, not one scientific experiment |
| PRs | 63 | **64** | 62 merged, #29/#32 closed-unmerged, zero open |
| Current tracked Git Blobs | 294 | **298** | Four added, four modified, zero removed paths |
| Historically witnessed, currently absent paths | 47 | **47 retained in prior record** | Not restored by PR #64, no claim of a full rescan of all historical Trees |
| Formal Knowledge Receipts | 4 | **4** | No new `APPLIED` lifecycle |

The four new paths are `docs/taxonomy/FULL_FILE_LIFECYCLE_2026-11-05.md`, its JSON register, the accompanying historical byte-identity lesson and `tests/test_full_file_lifecycle_2026_11_05.py`. The four changed paths are the living `docs/README.md`, `docs/provenance/README.md`, `docs/taxonomy/README.md` and `evidence/profiles/docs.json`

No frozen JSON, production `data/`, three scientific software assets, experimental Framework, or native Workflow YAML was changed by the publishing PR or by this append-only reconciliation

## EVALUATE · GitHub Actions 730 → 750 exact identity reconciliation

The prior frozen 730 Run IDs were reconstructed from the 598-source archive and its dated delta chain. Eight current GitHub API pages returned **750 unique visible Runs** (100 × 7 and 50), **all 730 prior IDs retained**, 20 new IDs and zero missing in this observation

| Current visible Run conclusions | Count |
| --- | ---: |
| Success | 705 |
| Failure | 4 |
| Cancelled | 41 |
| **Total** | **750** |

All 20 new Runs are individually recorded with workflow path, event, head SHA, attempt, GitHub Run ID and Jobs in the machine JSON. **46 Jobs = 39 success + 5 failure + 2 conditional skip**. The 20 Runs partition without overlap into 7 PR #63 development/merge checks, 4 failed PR #64 initial checks, 4 corrected PR #64 development checks, 3 post-merge main checks and 2 Nov 5 scheduled checks

- [Daily #41994924429](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41994924429): separate institutional reference and project-custom Jobs both successful, but neither grants external research certification
- [Continuity #42027562052](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42027562052): latest completed scheduled `verify` Job successful at the pinned main
- [Bio push #42011214672](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42011214672): `offline=success`, `pinned-field=skipped`; a green Run is not evidence that every Job executed
- [Post-merge Evidence #42011214974](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42011214974), [Bio #42011214672](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42011214672) and [integration #42011214655](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42011214655) all concluded success

## AUDIT · four failures and the corrected first-day test

The initial PR #64 head `a9b039cfd235295d55d98568c5b4c555d6b34144` generated the following **real failed** Run IDs:

- [42010968246](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42010968246) — Evidence push, failed
- [42010981438](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42010981438) — Evidence PR, failed
- [42010981442](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42010981442) — Bio PR, failed
- [42010981547](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42010981547) — integrated PR, failed

Job logs specifically showed `test_immutable_dated_json_not_silently_overwritten` asserting a false mismatch for `docs/provenance/action-run-reconciliation-2026-10-30.json`. Source comparison identified an incorrect Git Blob header: the failed version encoded printable backslash-plus-zero instead of the required NUL byte; the corrected version builds the header using `bytes((0,))`

The corrected development head `d4e6ad59ef90c2da527a6afa4b8a2b9ca8c5a105` and merged main passed their independent CI. This is an **engineering test implementation correction**, not proof that the older frozen file was altered. Keep all four original failed Run IDs and the prior unrelated historical 404 observations intact

## REVIEW → REPLAY · fixed boundaries

The accepted Knowledge state remains **four Git-backed Receipts and linked events, three archived Candidates**, latest `gh-41436556408-1`, with no new Knowledge apply. Four accepted changes are not four discoveries, and 26 `SOURCE_MATCH` edges are not verified biological relations

Provider-owned WorkflowHub, LifeMonitor, bio.tools, OpenEBench, LS Login and Zenodo statuses are not upgraded by GitHub CI. Original February predecessor claims remain separate from LS's October Git root. Agent declarations, PR authorship, Run execution and scientific review remain separate evidence objects

**Disposition:** `FIRST_DAY_TO_POST_PR64_FILE_LIFECYCLE_RECONCILED`, `HISTORICAL_FAILURES_PRESERVED`, `NO_ACCEPTED_DATA_CHANGE`, `NO_NEW_VERIFIED_SCIENTIFIC_CLAIM`

**Replay:** `python -m unittest discover -s tests -p 'test_post_730_run_delta.py' -v` validates frozen Run identity reconstruction, source-bound file differences, Job outcomes, failure classification and non-promotion of Knowledge state, but does not re-run historical GitHub Jobs or externally certify a scientific result
