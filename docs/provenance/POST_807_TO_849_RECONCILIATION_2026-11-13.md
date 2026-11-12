# Post-807 → 849 Actions, Job and research provenance reconciliation · 2026-11-13

[Machine ledger](post-807-to-849-observation-2026-11-13.json) · [Frozen prior baseline](post-798-to-807-observation-2026-11-10.json) · [Offline replay](../../tests/test_post_807_run_delta.py) · [Public lesson](../lessons/2026-11-13-fail-closed-paths-and-cancelled-jobs.md)

## DEFINE → PIN → QUALIFY

Read-only observation 2026-11-12T17:05:11.163Z UTC (2026-11-13 Asia/Shanghai), pinned source main `4bc0ad701f2a9f7ebae4e4aecf1d7aa7e867334d`, tree `e449d35488fe3a663650dd71b106bc3f02ced96c`, root `00009a38bc136a7c245270770b005e4e102a870d`. The complete nine-page currently visible Actions census, all 42 new Run latest-attempt Job listings, current main PR/Git identities, accepted receipts and selected actual logs were checked. Individual HTTP acquisition timestamps were not recorded. This is not a claim of institutional or scientific certification.

## EXECUTE → EVALUATE · strict comparable counts

| Unit | Previous 2026-11-10 cutoff | Current source cutoff |
| --- | --- | --- |
| API-visible Run IDs | 807 | **849** (807 old retained, 42 new) |
| Run conclusions | 766 success / 41 cancelled | **798 success / 51 cancelled** (32 success + 10 cancelled) |
| Triggered Runs | 56 schedule / 414 push / 333 PR / 4 dispatch | **60 / 431 / 354 / 4** |
| New latest-attempt Jobs | — | **73 success / 3 skipped / 26 cancelled / 1 failed = 103** |
| Root-reachable Git commits | 264 | **295**, closed parent ancestry, unique root Oct 16 |
| Main tracked Git Blob paths | 323 | **327**, path count not scientific output count |
| PR objects | 71 | **74**: 71 merged, #29/#32/#67 closed-unmerged, zero open |
| Accepted receipts / events / prior archives | 5 / 5 / 4 | **5 / 5 / 4**, no native production acceptance |

Prior frozen source files are not rewritten. The machine ledger contains 849 currently visible Run IDs and full 42-Run latest-attempt Job identities so retained, new, cancelled, skipped and failed sets can be recomputed offline. A GitHub Run being cancelled does not mean its constituent Jobs all failed, all passed, or all never ran.

## Daily schedule quality: two independent self-check planes

Nominal UTC cron is 01:41 daily self-check, 04:17 continuity, Monday 03:23 Knowledge and Friday 02:19 Bio QA. The offsets below measure nominal cron to GitHub Run created_at, not proven dispatch/queue/runner delay causes.

| Shanghai day | Workflow | Run | Nominal UTC | Created UTC | Gap | Latest-attempt Job results |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-11 | Institutional + project self-check | [42986640895](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/42986640895) | 01:41 | 08:23:24 | +06:42:24 | Institutional defaults — public read-only observations: success; Project custom — three assets and accepted evidence: success |
| 2026-11-11 | Accepted-state continuity | [43016063251](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43016063251) | 04:17 | 11:56:21 | +07:39:21 | verify: success |
| 2026-11-12 | Institutional + project self-check | [43186230480](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43186230480) | 01:41 | 08:50:19 | +07:09:19 | Institutional defaults — public read-only observations: success; Project custom — three assets and accepted evidence: success |
| 2026-11-12 | Accepted-state continuity | [43222080700](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43222080700) | 04:17 | 12:53:31 | +08:36:31 | verify: success |

Nov 11–12 scheduled self-check Jobs succeeded separately for institutional public-defaults observation and project custom checks. The latest project-custom runner printed eleven PASS results; institutional execution printed PUBLIC_HTTP_READ_ONLY, which does not prove every upstream service is healthy or authorize institutional changes. Latest Nov 12 continuity log printed 'state is valid', 'knowledge provenance and content verified', 17 entities / 26 source matches / five events, and KNOWLEDGE_QUALITY_PASS. No additional daily Knowledge/Bio schedule was due within this cutoff.

## AUDIT → REVIEW · negative evidence and correction history

[Run 43210854941](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43210854941) was cancelled at the Run grain but contained a failed Repository contracts Job. Actual log assertions included UNCLASSIFIED_NEW_PATH and NEW_PATH_REQUIRES_REVIEWED_CLASS for the intermediate unclassified root `RELEASE_POLICY.md` (four frozen-governance tests). Package, Knowledge and Evidence Jobs passed on that run while the final validation Job was cancelled. Thus **zero currently visible failed Runs is not zero failed Jobs**.

PR [#73](https://github.com/lostlight530/life-science-ecosystem-lab/pull/73) and [#74](https://github.com/lostlight530/life-science-ecosystem-lab/pull/74) completed review, rollback and boundary repair; final main no longer tracks the rejected root path. Main-head checks succeeded in Repository contracts, Knowledge Workflow, Evidence Tool and Portable package. Existing `validate.yml` has `cancel-in-progress: true`; actual reason for individual cancellations is not independently established and stays UNKNOWN.

GitHub Actions logs showed nonfatal deprecation warnings (Node.js 20 / forced Node.js 24). No production source/profile, Runtime, Framework, workflow schedule, accepted data, external registration or Release was changed by this review. Current branch protection is false from the main branch API; successful CI does not imply server-enforced approval.

Native Knowledge's latest accepted event remains Nov 9, gh-42611716908-1 with DOCUMENT_TEXT_UNCHANGED → APPLIED. There remain five receipts, five linked events and four prior Candidate archives. The 17 entities and 26 SOURCE_MATCH relations describe extractive source matching, not 26 validated biological relationships. WorkflowHub, LifeMonitor, OpenEBench, bio.tools, Zenodo and LS Login provider-side current states were not independently rechecked; repository metadata/links are not fresh provider acceptance evidence.

Historical February precursor Agent attribution is separate from the GitHub root on 2026-10-16 and from authenticated execution evidence. Earlier vanished failed Runs retain their original dated negative evidence; current API visibility alone does not establish deletion cause.

## REPLAY and decision

Run `python -m unittest discover -s tests -p 'test_post_807_run_delta.py' -v` and full repository/three-asset/portable CI on the review branch; inspect individual Jobs, exact changed paths, current branch HEAD and CI before any merge. This source cutoff excludes the current review PR and its Actions.

**Disposition: MATERIAL_PUBLIC_EVIDENCE_DELTA; NATIVE_ASSETS_AND_PRODUCTION_NO_CHANGE_REQUIRED; SCIENTIFIC/EXTERNAL_CLAIM_NOT_PROMOTED**
