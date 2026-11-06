# Post-750 GitHub Run reconciliation and scheduled research quality · 2026-11-06

[Machine-readable source ID set](post-750-to-758-observation-2026-11-06.json) · [Frozen predecessor](POST_730_TO_750_RECONCILIATION_2026-11-05.md) · [Independent offline falsifier](../../tests/test_post_750_run_delta.py) · [Public failure-mode lesson](../lessons/2026-11-06-visible-history-and-scientific-nonclaims.md)

**DEFINE → PIN → QUALIFY:** 2026-11-06 Asia/Shanghai review · remote `main=bafb9ce5049764a102d4f23ac0c30c397442c194` · root `00009a38bc136a7c245270770b005e4e102a870d` (2026-10-16) · live GitHub API pages, Job endpoints and bounded logs. Individual HTTP acquisition timestamps were not captured; GitHub `created_at` is **not** the audit observation timestamp. This is an append-only engineering observation, not a scientific result

## EXECUTE → EVALUATE · complete visible Run identities, not a net-count guess

All **750** previously archived IDs were reconstructed through the original 598 baseline and successive immutable JSON deltas, then compared against eight current GitHub API pages with **758 distinct visible IDs**, with the entire current ID set retained in the machine JSON

| Source-based population | Count |
| --- | ---: |
| Previous visible set | 750 |
| Prior IDs still visible | **746** |
| Prior IDs no longer visible | **4** |
| New distinct Run IDs | **12** |
| Current API-visible Runs | **758** |
| Current success / failure / cancelled | **717 / 0 / 41** |
| New Jobs success / failure / skipped | **23 / 0 / 1** |

The four previous **failed** Run IDs `42010968246`, `42010981438`, `42010981442` and `42010981547` are absent from the current eight-page Run list and direct Run lookups returned **HTTP 404**. They remain evidenced as failures in the frozen 750-Run archive and its PR #64 Git Blob NUL-header test correction. The reason for present API inaccessibility is **UNKNOWN**, not evidence that failures never happened, were erased by any named actor or were scientific failures

The 12 new successes comprise four PR #65 development Evidence pushes, three PR checks, three post-merge main checks and two Nov 6 scheduled checks. All 12 were matched to concrete Job IDs; the sole skipped Job is Bio `pinned-field` on its `push` event, as permitted by the versioned workflow guard. This is not a failed job or a successful field re-execution

## AUDIT · daily and periodic native execution, first available schedule to current

The GitHub scheduled-run endpoint currently exposes **46 schedule Runs and 72 successful Jobs**, each independently checked at the Jobs API: 20 daily self-check Runs (two separate institutional/project Jobs each), 20 continuity Runs (one verification Job), three weekly Knowledge Runs (validate + apply), and three weekly Bio QA Runs (offline + pinned-field). Each visible scheduled Run is Success, but success is scoped to the declared Job and its checks; it does not certify scientific discovery, platform approval or complete upstream accessibility

The Nov 6 [daily self-check](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42188093525) has institutional and project Jobs both successful. Its project log records 11 check categories with PASS, including accepted state, knowledge, graph and publication boundary; two independent artifacts are reported, IDs `13488332933` and `13488597032`. Per-endpoint official HTTP results are not inferred from the green Job

The Nov 6 [Bio QA](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42194936143) has both `offline` and `pinned-field` successful. Its offline log reports 252 passing Python tests and deterministic FASTA/PDB/CWL replay, with an expected FASTA `WARN_UNCERTAIN_RESIDUES` quality signal rather than an unqualified scientific PASS. The pinned-field log reports `VERIFIED_PINNED_BLOBS_AND_ANALYZED_BIO_DATA 6`; this count refers to that Job's analyzed pinned examples, **not** every historically audited sample or six verified scientific hypotheses. Artifacts: `13490634456`, `13490518987`

The nominal Nov 6 daily cron `01:41 UTC` precedes its GitHub-created time `08:29:54 UTC` by **06:48:54**. The Bio Friday cron `02:19 UTC` precedes its created time `09:25:25 UTC` by **07:06:25**. These are schedule-intent-to-API-record differences, **not measured runner queue times**. The dispatch cause is UNKNOWN; both Runs executed on Nov 6 local Shanghai date

## REVIEW → REPLAY · Git origin and scientific authority

`main` exposes **258 root-reachable Commits**, **301 tracked files**, **65 PR objects** (63 merged, #29/#32 closed without merge, no open PR), and two releases `v0.4.0` / `v0.5.0`. PR #65 contributes one main Commit following PR #64, three added paths and three modified paths; the pre-existing 47 historical-only paths and prior frozen records are not reclassified as new deletions

Four formal Knowledge `APPLIED` Receipts (Oct 17, Oct 19, Oct 26, Nov 2), four linked events and three archived Candidates remain unchanged. Three later events have `DOCUMENT_TEXT_UNCHANGED` change kind: formal state transition is not a new verified scientific discovery. No new `data/` acceptance, protein-folding result or external provider certification is observed in this window

Original February 15–16 workflow collaboration remains **author-supplied predecessor attribution**, not an LS Git ancestor or independently authenticated Agent execution. No live WorkflowHub, LifeMonitor, bio.tools, OpenEBench, Zenodo or LS Login acceptance state is promoted by this GitHub-only census; attempts to read several provider pages did not give authoritative fresh status

**Disposition:** `HISTORY_RECONCILED_WITH_FOUR_CURRENTLY_INACCESSIBLE_FAILURES` · `SCHEDULED_JOBS_VERIFIED` · `NO_ACCEPTED_RESEARCH_DATA_CHANGE` · `NO_NEW_VERIFIED_SCIENTIFIC_CLAIM`

**Replay:** `python -m unittest discover -s tests -p 'test_post_750_run_delta.py' -v` verifies both frozen and new identity sets and authority counts offline, not the historical execution of already-completed cloud Jobs
