# Causal failure reconstruction and cross-repository predecessor evidence · 2026-10-31

[Methodology](../RESEARCH_METHODOLOGY.md) · [Historical reconciliations](RECONCILIATION_2026-10-30.md) · [Machine evidence](failure-causal-replay-2026-10-31.json) · [Offline regression](../../tests/test_failure_causal_replay.py)

**Type:** project-owned, privacy-minimized research-method correction; **source base:** LS `928aa525551822be7b33061ea70f169ea0961970`; **date:** 2026-10-31 Asia/Shanghai. No exact fresh HTTP observation instant was captured: the JSON explicitly uses `utc_observed_at: null`. This is not a reconstructed original GitHub runner log, proof of private Jules execution, new accepted Knowledge or new scientific result.

## 1. Question, falsifier and grading

Question: Why were eight originally archived Evidence Tool `push` runs failed, and can the suspected documentation-inventory contract violation be demonstrated from the *exact historical Git trees and manifest blobs*, even when original runner logs are no longer available?

**Independent Git reconstruction:** for each run's `head_sha`, retrieve the historical tree (`git/trees/{sha}?recursive=1`) and `evidence/profiles/docs.json` at that commit; compute the set of directly contained `*.md` files in the **historical test's** `PUBLIC_DOC_DIRS`, compare to the manifest. The invariant test blob SHA is `4ab741a26d1f9aaf592029427f5b127e951336c8` and Evidence Workflow blob SHA is `0b6d4d99adbb9bd552fcbd0cf47378b12388004b` throughout the contrasted versions. The workflow runs `python -m unittest discover -s tests -v`.

**Falsifiers:** a pinned tree/manifest returning different paths or digest; a changed historical test or workflow blob; evidence that the failed job never executed this test; or an independently recovered log showing a different failure attribution. The set mismatch establishes a deterministic violation, **not** the complete original Job traceback.

## 2. Eight original failures: one omission pattern, repeated

| Archived failed Run | Immutable head prefix | Expected direct-child docs | Recorded | Contradiction |
| --- | --- | ---: | ---: | --- |
| [40907559247](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40907559247) | [2402f64ff8dd](https://github.com/lostlight530/life-science-ecosystem-lab/commit/2402f64ff8ddc35e6c8bf0596ec7ca1fd57d9fec) | 38 | 37 | Replay guide missing |
| [40907729879](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40907729879) | [ada828cec321](https://github.com/lostlight530/life-science-ecosystem-lab/commit/ada828cec3218d9c15969c864f9fdab37abafa18) | 39 | 37 | Replay + interoperability guides missing |
| [40907800054](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40907800054) | [9467431d6079](https://github.com/lostlight530/life-science-ecosystem-lab/commit/9467431d60794691ebb236144b48089ec6290f75) | 39 | 37 | Replay + interoperability guides missing |
| [40907810044](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40907810044) | [605d7d76fc6b](https://github.com/lostlight530/life-science-ecosystem-lab/commit/605d7d76fc6b7f7fd108dfbdd0851ab7803cc455) | 39 | 37 | Replay + interoperability guides missing |
| [40907818486](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40907818486) | [a9d1f107beb0](https://github.com/lostlight530/life-science-ecosystem-lab/commit/a9d1f107beb01236e36a31d694e12857d8a74a10) | 39 | 37 | Replay + interoperability guides missing |
| [40907827214](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40907827214) | [dea3993fb574](https://github.com/lostlight530/life-science-ecosystem-lab/commit/dea3993fb574f80c14b44b6a38ae123fc5f229e9) | 39 | 37 | Replay + interoperability guides missing |
| [40907834368](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40907834368) | [29fbb406f09f](https://github.com/lostlight530/life-science-ecosystem-lab/commit/29fbb406f09f4cd759e0f9ede2ccb090a7c5d673) | 39 | 37 | Replay + interoperability guides missing |
| [40907843653](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40907843653) | [36bedd5b2f26](https://github.com/lostlight530/life-science-ecosystem-lab/commit/36bedd5b2f26ce863308acb936f2525a6d60638c) | 39 | 37 | Replay + interoperability guides missing |

All eight trees contain more controlled direct-child public Markdown files than the unchanged manifest blob `dc288726933beab5956d7bbd50954a25ea10ff99` records. The first commit introduces `docs/EVIDENCE_REPLAY_PROTOCOL.md`; the second adds `docs/INTEROPERABILITY_REVIEW.md`. Later documentation/link changes did not update the manifest in those intermediate commits.

**Minimal correction / positive control:** `a2755a3be47f54f7a1c9ce3629b9f6112316cd5f`, accepted through [PR #40](https://github.com/lostlight530/life-science-ecosystem-lab/pull/40), reconstructs `39 / 39` and no differences. The test and Evidence Workflow blobs remained unchanged. The change fixed the input-to-contract mismatch rather than bypassing the rejecting assertion.

## 3. Three later reported failures: the reverse pattern

The previously observed three failed Run IDs (`40912577732`, `40912637281`, `40912637202`) were not archived with full original Job logs; individual Run requests later returned HTTP 404. Do **not** assign a specific archived Job traceback or a deletion reason to these records.

The independently retrievable [PR #43](https://github.com/lostlight530/life-science-ecosystem-lab/pull/43) commit sequence is a causal counterexample:

- `b03b45bca42a3528380092a077c142f76696e605` (16:32:20 UTC): historical tree contains **42** selected direct-child documents, but inventory lists **43**; the excess `docs/provenance/README.md` is nested one level below `docs` and **outside** the `glob("*.md")` scope
- `1af56cd8c18ac59f9099166b329b1ae964b8fecf` (16:33:21 UTC): only inventory changes; reconstructed selection is **42 / 42**, no mismatch
- Subsequent [Evidence success](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40912737378) and [repository validation success](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40912747485) establish the positive execution boundary; neither is a restored log for the missing failed runs

Thus the **known code-level defect class** is an exact-set contract violation in two opposite directions: omission and over-inclusion. The archived 8 and lower-grade 3 observations are **not eleven independent biological failures**.

## 4. Cross-repository provenance: what changed in the evidentiary claim

[LS PR #1](https://github.com/lostlight530/life-science-ecosystem-lab/pull/1) historically attributed a February 15–16 Jules collaboration. Previously the LS Git repository itself had no independently recoverable predecessor commit. On this review, the separate public `lostlight530/welcome-to-github` repository provided independent evidence for related *engineering activity*:

| Source | Verified narrow observation |
| --- | --- |
| [Welcome PR #21](https://github.com/lostlight530/welcome-to-github/pull/21) (Feb 15) | Git-merged append-only JSONL Knowledge structure and learner; PR includes Jules-created task attribution, **not** independent private-agent attestation |
| [Welcome PR #22](https://github.com/lostlight530/welcome-to-github/pull/22) (Feb 15) | `.github/workflows/brain-evolution.yml` and `brain-integrity.yml` were added |
| [Welcome PR #30](https://github.com/lostlight530/welcome-to-github/pull/30) (Feb 15) | Separate underscore-named `brain_evolution.yml` and Harvester were added |
| [Scheduled Run 22047521121](https://github.com/lostlight530/welcome-to-github/actions/runs/22047521121) (Feb 16, 01:55:09 UTC) | `brain-evolution.yml`, `daily-evolution` Job **success** |
| [Welcome PR #40](https://github.com/lostlight530/welcome-to-github/pull/40) (Feb 16) | Separate `brain_evolution.yml` was edited after an attributed non-trigger report; proposed scheduling mechanism remains **unproved** |
| [Manual Run 22090424419](https://github.com/lostlight530/welcome-to-github/actions/runs/22090424419) (Feb 17, 08:00:23 UTC) | `brain_evolution.yml`, `evolve-and-harvest` Job **success** |

**Do not conflate** hyphen `brain-evolution.yml` with underscore `brain_evolution.yml`. The former's scheduled success cannot disprove a report that the latter failed to trigger. Both historical log-download attempts returned HTTP 410 while their Run/Job summary objects were retrievable. A GitHub PR task attribution is not private Jules execution attestation.

**Amended finding:** independently identifiable February *public Git/PR/workflow activity* exists in another repository, supporting a bounded historical context. There is no established shared Git ancestor, byte-identical transfer, specific LS implementation inheritance or authenticated private-Agent execution. The LS repository still begins October 16, 2026.

## 5. Failure science and retention, not failure accumulation

The eight-stage cycle is unchanged. Every incident review should produce a **claim-specific causal case**: immutable input version → invariant oracle → observed contradiction → alternative hypotheses → minimum correction → positive and negative controls → independent replay → remaining unknowns.

Separate the existence of archived failures, the mechanics of a deterministic violated contract and the detailed original log trace. Repo-maintainer choices to delete old GitHub Actions runs are ordinary lifecycle decisions; an API 404, without an authenticated audit record, cannot identify actor, reason or mechanism. Retain the **minimal source-graduated explanation** necessary to understand and falsify the failure, without copying sensitive logs or converting GitHub's temporary runtime records into mandatory permanent retention.

**No effect:** production `data/`, accepted receipts, archive JSON from October 30, frozen `v0.4.0`, installed Tools/Framework logic, external institution states, Cron, branch settings or an external account.
