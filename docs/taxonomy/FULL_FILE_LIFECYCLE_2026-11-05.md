# Complete first-day-to-current file lifecycle · 2026-11-05

[Complete machine-readable file / Commit / PR / Tree register](full-file-lifecycle-2026-11-05.json) · [Frozen 2026-11-03 274-file baseline](file-register-2026-11-03.json) · [2026-11-04 additive 13-file classification](post-2026-11-04-source-classification.json) · [Historical corrections](CORRECTION_REGISTER_2026-11-03.md) · [Offline falsifier](../../tests/test_full_file_lifecycle_2026_11_05.py) · [Public lesson](../lessons/2026-11-05-historical-paths-and-byte-identity.md)

**DEFINE / PIN:** source repository `lostlight530/life-science-ecosystem-lab`, Git root `00009a38bc136a7c245270770b005e4e102a870d` (2026-10-16), source `main=18c33998a78ff64537d993bd7d7408c5a5da0cf3` before this report's publishing PR, review day 2026-11-05 Asia/Shanghai. A separate February predecessor is historical context, not an LS Git ancestor. Exact timestamps for individual GitHub API requests were not independently captured. This is a GitHub-observed, read-only research-software lineage report, not official GitHub certification or new scientific production.

## QUALIFY / EXECUTE · exhaustive source objects, not only today's directory

| Scope / identity | Source-based observation | Important exclusion |
| --- | ---: | --- |
| Git Commit SHA + parent DAG | **256** main-reachable commits, one root, parent-closed | Not all unmerged branches, private activity or Agent execution attestations |
| Git Tree SHA | **235 distinct trees** read across the reachable DAG, zero observed truncation/failed reads | Two commits may have an identical tree; Git Commit is not a unique file-state identity |
| GitHub PR number | **63** (61 merged, #29/#32 closed-unmerged, none open) | Proposal is not scientific acceptance; titles do not prove who operated an Agent |
| Tracked path + current Git Blob SHA | **294 current files** | Paths are not individual experiments or unique content revisions |
| Historical-only path + witnessed Git Tree + Git Blob SHA | **47 paths absent from current tree** | Absence is not proof of operator, cause, permanent deletion or no successor |
| Distinct observed path names in current + historical-only union | **341** | Not a number of code files created or a software-size KPI |
| Public Markdown document registry | **73/73** current source Markdown paths registered at cutoff | The reporting PR adds two Markdown documents to a later cutoff |

All 256 Git Commit IDs, 256 Commit→Tree associations and parent edges, all 63 PR identifiers/titles/status, all 294 current paths/blob SHAs/categories and all 47 historical-only paths with witness Commit/Tree/Blob are serialized individually. Every file seen only in a historical tree is retained as a **historical path identity**; no old version is silently restored to current `main`.

## EVALUATE · precisely what changed from the frozen registers

The source-pinned 2026-11-03 274-file register plus the later 13-file overlay covers **287 paths**, all still present at this cutoff. The new snapshot adds **seven** current paths (the publication artifacts of PR #62/#63), for 294. Of the 287 earlier classified paths, **277 retain the recorded Git Blob SHA** and **ten changed content since their historical cutoff**. The ten are living repository guidance, documentation indexes, the docs registry and a test:

`AGENTS.md`, `CHANGELOG.md`, `README.md`, `docs/MAINTENANCE.md`, `docs/PROVENANCE.md`, `docs/README.md`, `docs/provenance/README.md`, `docs/taxonomy/README.md`, `evidence/profiles/docs.json`, `tests/test_repository_experience.py`

These changes are **version differences, not automatic evidence tampering**. Frozen Git Blob identities remain in the old registers; the new ledger records both old SHA and observed current SHA for each changed living path. The 274-file historical baseline is not rewritten. Every new path is in a reviewed family: `docs/provenance/`, `docs/taxonomy/`, `docs/lessons/` or `tests/`. The nine current Workflow YAML paths remain a fixed, separate execution-infrastructure set. Historical `data/` is governed by native approval and must not be changed by retrospective file reporting.

## AUDIT · 47 historical-only paths and evidence grades

A broad early-project tree witness (Commit `18b91a27c09f85ab8c28a6d3a500908ca0216877`) contains **43** paths absent from current `main`: old `src/life_science_ecosystem_lab/`, `workflow/`, `profiles/`, `schemas/`, `examples/`, `scripts/`, `.github/workflows/nexus-life-cycle.yml` and two `docs/superpowers/` design records. Four additional ancestor-state witnesses record `.lifemonitor.yaml`, `bio_tool/tabular.py`, `tests/test_daily_selfcheck.py`, and `evidence/field-tests/2026-10-17-first-accepted-cycle.json`. These 47 names are absent from the current 294-path tree.

Of these, **19 historical paths have an exactly matching Git Blob SHA at another current path**. This is direct byte-identity evidence, for example `examples/records/input.json` ↔ `evidence/examples/records/input.json`, `scripts/check_write_boundary.py` ↔ `.github/scripts/check_write_boundary.py`, and early Evidence modules ↔ `evidence/`. It establishes identical bytes for those pinned versions, **not** a proven Git rename event, full semantic equivalence or preservation of identical runtime behavior. The other **28** lack exact content matches against the current tree at the chosen witness version; possible rewrite, relocation, removal, or integration remains subject to file-level source review.

Specific causal clues from public Git history:

- `.lifemonitor.yaml`: Commit `f92fd977e11e49887dedfef7ac3734a849fd321d` is titled *fix: remove nonstandard LifeMonitor config filename*. Current `lifemonitor.yaml` is the active repository-specific configuration; old/official naming must not be resurrected
- `tests/test_daily_selfcheck.py`: Commit `39b41f87b95442d78e30aa36adc8c2701af6d0dc` is titled *test: replace mixed self-check tests with isolated plane suites*. The old file is historical and the current independent institutional/project test paths govern the live design
- `bio_tool/tabular.py` and the first-accepted-cycle JSON: historical Git Tree witnesses exist; an exact current-byte counterpart was not found. Do not infer the meaning of their disappearance merely from the file name
- `docs/superpowers/` design files: first-day architecture material remains reachable through historical Git, but is not the current runtime contract

No personal notes, secret tokens, private Agent records, large upstream source bodies or claimed science results are copied into this public register.

## REVIEW / REPLAY · acceptance and rollback boundaries

This report only evaluates **Git file identities and public software maintenance evidence**. The three independent scientific software assets (Knowledge, Evidence, Bio), the experimental Framework, nine native Workflow definitions and formal accepted `data/` are **unchanged** by this review. The accepted Knowledge state remains four Git-backed Receipts, four linked `APPLIED` events, three archived Candidates, 17 knowledge entities and 26 `SOURCE_MATCH` document/topic edges. They are not four scientific discoveries or 26 validated biological relationships. Provider-owned WorkflowHub, LifeMonitor, bio.tools, OpenEBench, Zenodo and LS Login statuses have independent authority; none is newly certified here.

**Disposition:** `COMPLETE_CURRENT_AND_MAIN_ANCESTOR_TREE_CLASSIFICATION_AT_18c33998a78f`, `NO_CHANGE_REQUIRED` for native assets and formal production, `HISTORICAL_ONLY_PATHS_PRESERVED` for 47 paths, `NO_NEW_VERIFIED_SCIENTIFIC_CLAIM` for science. The publishing PR itself adds later files excluded from the 294-path cutoff, which must still satisfy repository classification guards.

**Offline replay:** `python -m unittest discover -s tests -p 'test_full_file_lifecycle_2026_11_05.py' -v`. It validates the pinned ledger, current filesystem registration, source categories, parent closure and exact matching SHA relationships. It cannot replace 235 fresh remote Tree GETs, reconstruct private execution surfaces, or verify external scientific truth.
