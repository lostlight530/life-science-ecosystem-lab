# Evidence-backed failure atlas for research software · 2026-11-15

**Scope:** portable engineering and scientific-evidence lessons extracted from the publicly inspectable history of one life-sciences research software repository, 2026-10-16 through 2026-11-15 (Asia/Shanghai). **Not** a list of biological failures, a claim to have observed every private or vanished execution, a new research result, or an institutional certification.

**通用定位：** 这份错误经验库面向任何长期运行的科研软件、开放科学基础设施、异构 Agent 协作与自动化研究系统。把错误视为可以定位、证伪、复现和修订的工程证据，而不是按红灯数量制造经验；保留原始失败、修复过程、审核分歧与未知，不改变正式科研历史。

[Full source classification](../taxonomy/FULL_HISTORY_CLASSIFICATION_2026-11-15.md) · [Machine census](../taxonomy/full-history-classification-2026-11-15.json) · [Native 849→868 evidence](../provenance/POST_849_TO_868_RECONCILIATION_2026-11-15.md) · [Earlier correction register](../taxonomy/CORRECTION_REGISTER_2026-11-03.md) · [Eight-stage method](../RESEARCH_METHODOLOGY.md) · [Agent review decisions](../AGENT_REVIEW_DECISIONS.md)

## The transferable invariant

> A successful action is only evidence for its **own typed contract**, at its own **identity, revision, authority, execution surface, time and verification grade**.

A diagnostic record should identify: **claim → falsifier → frozen source → actual observation → competing explanations → smallest repair → independent oracle → residual uncertainty → human decision → later replay**. A claim without a real independent oracle remains a proposal or an unknown; it does not become true through documentation, CI, an Agent assertion or a public registry pointer.

### Evidence types that must never be collapsed

| Object | Evidence of | Not evidence of |
| --- | --- | --- |
| Git Commit, Tree and Blob | A specific version and exact bytes of repository source | A scientific experiment, Agent runtime identity or production acceptance |
| PR and review | Proposal, review and merge/disposition history | Execution of a named Agent, scientific validation, or acceptance when closed-unmerged |
| Actions Run | A triggered workflow instance and overall result | Success or execution of every Job |
| Actions Job / Step | A specific execution gate, skip, cancellation, warning or failure | Every promised outcome outside that Job or its actual trigger |
| Artifact | A produced and retained execution output, conditional on its exact bytes | Durable accepted Knowledge state |
| Receipt + event chain + accepted Git commit | A versioned, authorized native production state transition | Novel biological truth or external certification |
| Test oracle / adversarial fixture | A bounded software-contract outcome | Validity of the scientific method or specimen |
| External provider record | What that particular provider reports at a documented observation time | Automatically synchronized status on all other providers |
| Agent self-label or Git author | A declared contributor or Git actor | Independent execution-instance authentication |

The five accepted Knowledge events recorded by 2026-11-09 are not five new biological discoveries. Four events have DOCUMENT_TEXT_UNCHANGED change classification. A 17-entity / 26-SOURCE_MATCH graph describes extractive matches, not validated causal biological relationships.

## A. Evidence population, statistical correctness and disappearing history

### F01 — Counters are not identity sets

**Observed:** two dated GitHub Actions snapshots could both show 531 visible Runs while containing different Run IDs; later consecutive censuses advanced through 547, 598, 849 and 868. **Mechanism:** a fixed-size or partially refreshed API result can gain IDs as others become unavailable. **Detection:** reconcile exact immutable IDs as retained, added, missing and changed, with complete pagination and a pinned old population. **Repair:** preserve both snapshots and add a dated difference, never silently replace the original. **Residual unknown:** a missing API record does not reveal provider retention, deletion actor or cause.

Evidence: [October census reconciliation](../provenance/RECONCILIATION_2026-10-30.md), [original research lesson](2026-10-30-evidence-census-and-runtime-quality.md), [849→868 delta](../provenance/post-849-to-868-observation-2026-11-15.json).

### F02 — Latest clean history cannot rewrite earlier failures

**Observed:** the original frozen 531-Run population contained eight failed parent Runs, while later currently visible populations can have zero failed parent Runs. Additional PR #55, #64 and #71 engineering failures later became unavailable or were retained in separate dated records. **Mechanism:** API visibility is time-scoped, and different populations have different denominators. **Detection:** store IDs, observation cutoff, status, original evidence grade and direct lookup outcomes. **Repair:** keep earlier negative observations and explicitly label unavailable original logs. **Do not infer:** malicious deletion, erased failure, GitHub fault or a currently failed pipeline without new evidence.

Evidence: [October failure causal replay](../provenance/FAILURE_CAUSAL_REPLAY_2026-10-31.md), [November 6 visibility example](2026-11-06-visible-history-and-scientific-nonclaims.md), [November 10 repaired-gate lesson](2026-11-10-repair-success-does-not-erase-failed-gates.md).

### F03 — Joining history to today's workflow name can falsify attribution

**Observed:** a stable workflow identifier was mapped to its current name, incorrectly labeling **134 historical Run records**. **Mechanism:** the workflow name is time-varying metadata, not an immutable property of all executions. **Detection:** read each Run's historical own name/path/ID and compare to the flattened index. **Repair:** append a source-pinned erratum; preserve old raw records. **Transfer:** any temporal join from an event to a mutable dimension requires as-of keys or immutable event attributes.

Evidence: [run-name and median erratum](../provenance/RUN_NAME_AND_MEDIAN_ERRATUM_2026-10-30.md).

### F04 — Arithmetic can be wrong even when every CI check is green

**Observed:** two previously reported scheduled-run offset medians were corrected by independent re-sorting. **Mechanism:** copied aggregates, inconsistent denominators and unsorted samples are not validated by source-file existence tests. **Detection:** recompute from atomic observations and print the ordered population, units and statistic definition. **Repair:** version the corrected derived projection without altering the original witness. **Transfer:** test metrics against their source rows, not only a hardcoded expected constant.

Evidence: [statistical correction](../provenance/RUN_NAME_AND_MEDIAN_ERRATUM_2026-10-30.md), [daily quality archive](../provenance/NATIVE_DAILY_QUALITY_2026-10-30.md).

### F05 — Trigger duplicates are not independent experiments

**Observed:** branch push, pull_request and merged-main push can produce multiple distinct successful Runs for one underlying documentation change. **Mechanism:** GitHub CI trigger grain differs from research experiment grain. **Detection:** retain event, head SHA, branch, workflow, Run and actual work performed. **Repair:** distinguish CI execution count, independent scientific replicate, and native accepted event. **Transfer:** never publish a quantity without an explicit unit-of-analysis contract.

Evidence: [November 8 evidence census](../provenance/POST_768_TO_788_RECONCILIATION_2026-11-08.md).

### F06 — Observation clock, logical date and schedule intent are different

**Observed:** scheduled Runs routinely appeared several hours after the cron's nominal UTC time; one dated source comparison also reported a one-hour discrepancy between API time and Runner log timestamps. **Mechanism:** cron, Run created_at, Job started_at, Runner log time, observation clock and Asia/Shanghai logical date represent distinct events. **Detection:** store each clock, timezone, source and provenance independently; only compute the literal nominal-to-created gap. **Repair:** annotate the clock type, align populations and preserve conflicting readings. **UNKNOWN:** real scheduler dispatch time, queue duration and platform cause without suitable telemetry.

Evidence: [November 1 clock boundary](2026-11-01-run-identity-and-clock-boundaries.md), [November 4 scheduling lesson](2026-11-04-cron-offset-observation-and-conditional-jobs.md), [849→868 scheduled offsets](../provenance/post-849-to-868-observation-2026-11-15.json).

### F07 — A not-yet-visible scheduled Run is not a missed execution

**Observed:** earlier same-day cutoffs occurred before a nominally due daily Run appeared in the queried API population. **Mechanism:** the sample window can end before observable execution. **Detection:** compare the query cutoff and latest confirmed scheduled Run; revisit at a later bounded cutoff. **Repair:** classify NOT_YET_VISIBLE or UNKNOWN instead of FAIL. **Transfer:** absence in a partial observation is not evidence of absence in the real system.

Evidence: [November 3 scoped audit](2026-11-03-native-success-is-not-universal-execution.md).

## B. Runtime contracts, hidden failure and incomplete execution

### F08 — A successful parent Run may contain a skipped scientific Job

**Observed:** Bio Tool main-branch push Runs succeeded with offline=success and pinned-field=skipped because the versioned event guard excludes ordinary push. The 2026-11-12 post-merge Run **43266573648** again shows this pattern. **Mechanism:** success is an aggregate parent conclusion with conditional branches. **Detection:** inspect each Run's Job ID, attempt, conclusion, triggering event and versioned condition. **Repair:** count the executed offline work and skipped field work separately; never impute execution to a skipped Job.

Evidence: [November 2 conditional Job explanation](2026-11-02-job-gates-and-evidence-visibility.md), [849→868 exact Job ledger](../provenance/post-849-to-868-observation-2026-11-15.json).

### F09 — A cancelled parent Run may contain an actual failed Job

**Observed:** Run [43210854941](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43210854941) had overall conclusion cancelled while Repository contracts **failed** on four path-governance tests involving unclassified root RELEASE_POLICY.md. Other payload Jobs succeeded; the final validation gate was cancelled. **Mechanism:** parent termination and child execution outcomes are different grains. **Detection:** query jobs and inspect the actual failed assertion lines, not the badge. **Repair:** classify the root path through an authorized review or revert it, verify a final successful PR and main check, and retain the original failed Job. **Transfer:** no parent status should overwrite a more informative child counterexample.

Evidence: [November 13 failure replay](2026-11-13-fail-closed-paths-and-cancelled-jobs.md), [bounded 807→849 audit](../provenance/POST_807_TO_849_RECONCILIATION_2026-11-13.md).

### F10 — Missing log bytes do not alter the API's known Job status

**Observed:** a skipped Job was identifiable by Jobs API while its log fetch returned BlobNotFound/404. **Mechanism:** an unavailable diagnostic body differs from a Job outcome. **Detection:** preserve response status and source failure separately. **Repair:** avoid inventing a traceback or converting skipped to failed; label cause unknown. **Transfer:** information loss in a lower-level diagnostic surface must not silently rewrite a higher-level typed observation.

Evidence: [November 2 bounded visibility](2026-11-02-job-gates-and-evidence-visibility.md).

### F11 — Repair success does not make the failed intermediate revision disappear

**Observed:** intermediate PR #55 and PR #71 revisions triggered genuine regression failures before their corrected heads passed; a later repair PR #74 restored the admitted path boundary. **Mechanism:** multiple versions of one change proposal have different outcomes. **Detection:** pin head SHA and Run/Job for each attempt, with original oracle and corrected version. **Repair:** prefer a locally validated coherent patch and a single reviewable candidate push; retain correction lineage. **Transfer:** the revision graph is part of the research record, not administrative noise.

Evidence: [frozen/live repair follow-up](2026-11-02-frozen-history-vs-live-state.md), [failed gate repair](2026-11-10-repair-success-does-not-erase-failed-gates.md), [cancelled gate example](2026-11-13-fail-closed-paths-and-cancelled-jobs.md).

### F12 — Runtime and assertion should not share unrestricted authority

**Observed:** native Knowledge production uses distinct validate and apply Jobs, guarded main/head comparison, constrained data path writes, actual Git commits, receipts and remote state verification. **Mechanism:** a successful collection or validation step alone cannot grant production permission. **Detection:** separately check authorization, source revision, write boundary, event chain, terminal applied state and remote SHA. **Repair:** fail closed at each authority boundary and leave proposals/observations read-only by default. **Transfer:** correctness, admissibility, state mutation and scientific truth are separate responsibilities.

Evidence: [native operations contract](../PRODUCTION_OPERATIONS.md), [actual accepted field audit](../NATIVE_CONTINUITY_FIELD_AUDIT.md).

## C. Historical state, immutable snapshots and live-state regressions

### F13 — Frozen evidence is not a forever-live assertion

**Observed:** old offline audit tests pinned three or four accepted events, then rejected legitimate fourth/fifth native accepted events as though new state were corruption. **Mechanism:** a dated truth was coupled to a moving HEAD. **Detection:** distinguish frozen evidence at old SHA from authorized current state; rerun both old and new integrity oracles. **Repair:** assert immutable historical prefix and receipts at pinned revisions, and check the full current event chain with live native verification. **Do not:** rewrite old JSON, lower standards to file existence, or change formal production data to satisfy the stale test.

Evidence: [November 2 repair](2026-11-02-frozen-history-vs-live-state.md), [November 9 repeat](2026-11-09-frozen-tests-vs-native-continuity.md).

### F14 — The opposite mistake: replacing integrity with file existence

**Observed:** a partial historical test repair exempted mutable production files from old SHA comparisons but tested them only via is_file; this was too weak. **Mechanism:** correcting a false rejection can accidentally create a false acceptance. **Detection:** independently verify pinned Git Tree Blob IDs, immutable Receipt bytes and current chain/digest/graph semantics, including a synthetic mutation that must fail. **Repair:** keep historical Tree evidence immutable and use the actual accepted-state verifier for the moving data. **Transfer:** every repair needs positive and negative controls against both error directions.

Evidence: [historical production Tree guards](../provenance/historical-production-tree-guards-2026-11-02.json), [source-cited lesson](2026-11-02-frozen-history-vs-live-state.md).

### F15 — Changed source identity is not necessarily changed scientific content

**Observed:** October 19/26 and November 2/9 native receipts report DOCUMENT_TEXT_UNCHANGED while distinct verified candidate/evidence/knowledge identities were persisted. **Mechanism:** bootstrap classification, upstream source revision and provenance-envelope changes can cause an accepted engineering transition despite unchanged selected text. **Detection:** separately compare selected source-text digest, upstream commit/ref, input/profile digest, Knowledge object, event and receipt. **Repair:** trace the acceptance predicate and replay identical candidates in a disposable state root. **OPEN DECISION:** whether the first metadata-only bootstrap transition is useful requires reviewer policy, not retrospective rewriting of the event.

Evidence: [native acceptance causal audit](../NATIVE_CONTINUITY_FIELD_AUDIT.md), [open claim L02](../CLAIM_VERIFICATION_GAPS.md).

### F16 — Current tree alone cannot classify the complete file history

**Observed:** 2026-11-07 had 309 live tracked paths and 47 ancestor-only paths; by the 2026-11-15 source cutoff there are 331 current paths and **53** witnessed ancestor-only paths. The six additional retired identities are .editorconfig, CODE_OF_CONDUCT.md, OPEN_RESEARCH.md, RELEASE_POLICY.md, RESEARCH_TEMPLATE.md, and docs/taxonomy/current-exact-path-classifications.json. **Mechanism:** intermediate main commits can introduce and subsequently retire files before the current head. **Detection:** enumerate parent-closed reachable commits, distinct Git Trees, exact Blob names and witness versions; compare to the current tree. **Repair:** use HISTORICAL_ONLY and versioned witnesses, do not reintroduce retired root paths or edit the original 47-path archive. **Boundary:** branches never merged to main are a separate unaccepted proposal history.

Evidence: [November 7 full governance](../taxonomy/COMPLETE_FILE_GOVERNANCE_2026-11-07.md), [new root-to-Nov15 ledger](../taxonomy/full-history-classification-2026-11-15.json).

### F17 — Same Blob SHA supports byte identity, not semantic rename intent

**Observed:** 19 earlier historical paths shared exact bytes with current paths at a previous source cutoff. **Mechanism:** content equality is not a recorded author intention, equivalent interface or semantic compatibility. **Detection:** compare the original Git Blob SHA and witnessed paths, then independently inspect changes and callsites before asserting a migration. **Repair:** keep BYTE_IDENTICAL_CURRENT_PATH and UNKNOWN_SEMANTIC_SUCCESSOR as separate classes. **Transfer:** never infer a rename or equivalence solely from similar labels or matching output.

Evidence: [November 5 full lifecycle](../taxonomy/FULL_FILE_LIFECYCLE_2026-11-05.md), [historical file lesson](2026-11-05-historical-paths-and-byte-identity.md).

### F18 — Cleaning an apparently generated file can destroy evidence

**Observed:** tracked production receipts, candidate archives, snapshots and project-owned provenance JSON are generated-looking but intentionally retained. Six structural .gitkeep files are not research results, and retired historical paths are not deletion candidates in the live tree. **Mechanism:** deletion by filename stereotype ignores source authority and reproducibility. **Detection:** classify each current path as software, validated state, immutable evidence, living guide, fixture, or cache; verify actual byte identity and references. **Repair:** remove only positively identified tracked garbage after scope review, not frozen history, real state or structural placeholders. **Transfer:** garbage collection needs an explicit retention contract and proof of non-authority.

Evidence: [November 7 cleanup classification](../taxonomy/COMPLETE_FILE_GOVERNANCE_2026-11-07.md).

## D. Contracts, security, software quality and negative controls

### F19 — Documentation inventories can fail in two symmetric directions

**Observed:** one path-inventory audit caught omitted public Markdown; another attempt added an out-of-scope nested document to an exact direct-child inventory. Later root-path additions violated closed allowlists. **Mechanism:** the inventory's discovery scope, registered set and governance admission policy diverged. **Detection:** compute exact registered-vs-discovered set differences and distinguish omissions from phantom/unauthorized entries. **Repair:** define the public-document scope once, register allowed Markdown in evidence/profiles/docs.json, and reject unjustified new root paths. **Do not:** widen every glob or delete old evidence to make a test green.

Evidence: [first error taxonomy](2026-10-30-error-detection-and-audit.md), [November 13 path gate](2026-11-13-fail-closed-paths-and-cancelled-jobs.md).

### F20 — A syntactically valid identity may not be an authentic identity

**Observed:** PR #17's 40-hex base commit could be well-formed without attesting freshness, ancestry or actual existence; a reviewed trusted expected-base comparison was required. **Mechanism:** syntax validation is not an authority check. **Detection:** fetch the independent source and match the claim to a reviewer-pinned expected SHA. **Repair:** keep self-declared base and verified reviewer baseline separate, fail closed on conflict. **Transfer:** a UUID, hash-looking token, structured schema or claimed timestamp is never by itself provenance attestation.

Evidence: [review decision ledger](../AGENT_REVIEW_DECISIONS.md), [Agent handoff contract](../../.github/agent-handoff/SOP.md).

### F21 — Byte identity and schema integrity can expose upstream mistakes

**Observed:** a past pinned field-case checksum was corrected against source bytes, and source-outage paths were designed to abstain rather than silently use partial material. **Mechanism:** human-copied digests, untrusted input paths and partial source acquisition are error-prone. **Detection:** recompute exact SHA over actual bytes, pin revision/size/license and inject absence, corruption or partial-read cases. **Repair:** reject mismatches and do not project incomplete required observations into accepted state. **Transfer:** FAIL, INDETERMINATE and missing input need typed output, not fabricated default values.

Evidence: [PR #10 checksum correction as recorded in prior lessons](2026-10-30-error-detection-and-audit.md), [source and state contract](../PRODUCTION_OPERATIONS.md).

### F22 — A declared cross-domain metric can have a semantic counterexample

**Observed:** PR #38 corrected a declared cross-domain-step metric that had missed a one-input step producing an asset in another domain. **Mechanism:** checking only input domains misses transitions when the output crosses the boundary. **Detection:** construct the smallest source/output-domain counterexample and compare to the metric contract. **Repair:** use the union of reviewed input and output domain declarations; keep failed/unknown executions in the declared population but abstain from claiming method success. **Nonclaim:** a fixed declaration count does not attest biological integration.

Evidence: [first error taxonomy](2026-10-30-error-detection-and-audit.md), [Framework assurance](../../framework/docs/ASSURANCE.md).

### F23 — Report writing needs bounded outputs and preservation on failure

**Observed:** PR #39 introduced failure-injection checks for staged JSON report writes; later Framework safeguards used a sibling temporary output and same-filesystem replacement. **Mechanism:** partial writes or unsafe destinations can damage a previous report, while a successful process exit may not imply affirmative PASS. **Detection:** simulate output replacement failure, illegal paths, non-finite JSON and deeply nested inputs. **Repair:** check path boundaries before writing, keep existing reports intact when ordinary replacement fails, and read the report's typed status. **Limit:** atomic replacement is not universal durability, synchronization or sandbox protection.

Evidence: [first error taxonomy](2026-10-30-error-detection-and-audit.md), [Framework assurance](../../framework/docs/ASSURANCE.md).

### F24 — Software-contract PASS is not domain validity

**Observed:** Framework's deterministic synthetic genomics/microscopy contract and FASTA/PDB processing can be replayed with negative controls, but do not independently execute the declared cross-domain biological analysis or prove protein-structure accuracy. **Mechanism:** schema/byte/lineage consistency is narrower than domain-method adequacy. **Detection:** require an independent domain oracle, frozen real non-sensitive data, external method baselines, uncertainty and falsifiers before scientific evaluation. **Repair:** publish software correctness, evidence validity, method applicability and scientific truth as separate grades. **Transfer:** a green test never bridges a missing epistemic layer.

Evidence: [independent Framework README](../../framework/README.md), [cross-asset replay](../EVIDENCE_REPLAY_PROTOCOL.md).

### F25 — Data-processing warnings are not equal to execution failures

**Observed:** a real FASTA test emitted WARN_UNCERTAIN_RESIDUES while the bounded processing and CWL replay Job passed. PDB CA parsing may pass within a narrower file-check scope. **Mechanism:** input-quality warning, parser failure, computational job status, model accuracy and scientific interpretation are different predicates. **Detection:** retain warning codes, input/sample identity, count denominator and corresponding independent Job conclusion. **Repair:** do not hide uncertain residues to produce a cleaner status, and do not call a warning a failed biological experiment. **Transfer:** preserve quality flags as first-class evidence for later interpretation.

Evidence: [October runtime quality](2026-10-30-evidence-census-and-runtime-quality.md), [Bio Tool contract](../../bio_tool/README.md).

## E. Human/Agent governance, external infrastructure and publication

### F26 — Git authorship or Agent self-label is not independent execution attestation

**Observed:** PR #19/#20 source claims required corrections about independent Agent actors, a private 142-day sibling runtime, PR #17 review disposition and one bot-originated PR. **Mechanism:** GitHub account identity, authored text, service bot and actual Agent execution surface are different. **Detection:** retain the proposer's original claim, reviewer decision, trusted platform evidence and unresolved gaps. **Repair:** accept verified software contributions without inflating Agent authentication or independent research replication. **Transfer:** an Agent can research, challenge and contribute; it cannot award itself scientific truth or production authority.

Evidence: [Agent decision ledger](../AGENT_REVIEW_DECISIONS.md), [Agent cohort case](../AGENT_CLUSTER_RESEARCH_CASE.md).

### F27 — A project's attributed prehistory is not its Git ancestry

**Observed:** a February 2026 predecessor engineering account exists separately from this repository's October 16 Git root. **Mechanism:** narrative influence and source-DAG parentage are different relationships. **Detection:** reconstruct the complete parent-closed main commit graph and cite the separately owned predecessor without retroactive merges. **Repair:** preserve predecessor as EXTERNAL_PREDECESSOR_ENGINEERING, keep private execution detail unverified. **Transfer:** trace provenance through IDs and parent edges, not themes, filenames or autobiographical attribution.

Evidence: [first-day taxonomy](../taxonomy/README.md), [original root reconstruction](../REPOSITORY_HISTORY_AND_PROVENANCE.md).

### F28 — Closed green PRs, merged commits and scientific acceptance differ

**Observed:** PR #29, #32 and #67 are closed-unmerged; #67's branch-only successful Evidence runs did not land its OSF proposals on main. **Mechanism:** branch state, CI and publication metadata are owned by different objects. **Detection:** verify merged_at, merge commit on main, changed files, subsequent CI and accepted data separately. **Repair:** classify CLOSED_UNMERGED; preserve proposal and original title without claim promotion. **Transfer:** a proposal can have value without becoming an accepted implementation or study.

Evidence: [November 7 branch boundary](2026-11-07-closed-branch-is-not-main-acceptance.md), [full PR census](../taxonomy/full-history-classification-2026-11-15.json).

### F29 — Local configuration and external provider acceptance are separate

**Observed:** GitHub App installation, repository LifeMonitor config, WorkflowHub references and GitHub releases do not certify provider-side workflow monitoring, synchrony, benchmark acceptance or biological tool registration. **Mechanism:** different providers own independent state and clocks. **Detection:** query each service's actual object ID, revision, access mode and observation time, and retain verification failures. **Repair:** classify repository-owned pointers and draft metadata separately from authoritative provider confirmations. **Transfer:** a published DOI or Release is a versioned citation object, not scientific truth.

Evidence: [institutional interoperability review](../INTEROPERABILITY_REVIEW.md), [claim gaps](../CLAIM_VERIFICATION_GAPS.md).

### F30 — Voluntary PR/CI discipline is not branch-enforced protection

**Observed:** GitHub reported main.protected=false and an empty ruleset collection during documented reviews. **Mechanism:** branch checks and human operational choices differ from server-side mandatory policy. **Detection:** explicitly inspect provider branch policy separately from green checks, while preserving access limitations. **Repair:** use independently reviewed PR procedures within current authority; propose branch policy changes only as a separate approved governance decision. **Transfer:** a procedure should never be described as an enforced control without actual control-plane evidence.

Evidence: [cloud provenance lesson](2026-10-31-cloud-history-replay.md), [open claim L04](../CLAIM_VERIFICATION_GAPS.md).

## F. General repair protocol — evidence before claims

A repair is accepted as a bounded **software repair** only when all the following are separately recorded:

1. **Claim:** exact contract and its scope, excluding irrelevant scientific and authority conclusions
2. **Counterexample:** immutable or pinned historical witness, actual identity and minimal contradictory input
3. **Oracle:** existing or explicitly versioned rule, able to reject the counterexample for the correct reason
4. **Mechanism:** demonstrated fault class, not a guessed actor or aggregate interpretation
5. **Smallest change:** only the responsible layer; no widening of write permissions or arbitrary source paths
6. **Negative control:** original defect still fails the appropriate unchanged-or-versioned oracle
7. **Positive control:** corrected case passes the same bounded oracle without suppressing warnings
8. **Temporal control:** old archived state stays frozen; legitimately evolving production is validated by a separate live oracle
9. **Review:** independent CI and human decision with actual branch/head/version identities
10. **Retention:** failure, review dissent, negative outcomes, original evidence and remaining UNKNOWN are not overwritten

**Failure-class selection matters.** A statistical error needs source-row recomputation; a wrong join needs temporal identity; a path-gate violation needs governance review; a mutable-state assertion needs source/live separation; a scientific claim needs a scientific oracle. Re-running arbitrary CI is not a universal repair.

### Corrective workflow mapped to the invariant eight stages

| Stage | Minimum handoff | Failure to avoid |
| --- | --- | --- |
| DEFINE | Falsifiable claim, unit of analysis, nonclaim | Unbounded "all green = research success" |
| PIN | Full SHA, original bytes, IDs, versioned method, time scope | Stale history silently substituted for current HEAD |
| QUALIFY | Authority, source grade, missingness, independent oracle | Self-declaration promoted to certification |
| EXECUTE | Smallest actual reproducer and permitted runtime | Conflating synthetic tests and scientific methods |
| EVALUATE | Source-computed counters, denominator, warnings, competing explanations | Wrong median, duplicate trigger, skipped Job inflation |
| AUDIT | Child failures, missing logs, immutable snapshots, correction history | Green current sample erases old negative evidence |
| REVIEW | Explicit authorizer, PR scope, CI result, accepted/not accepted state | Bypassing path governance for convenience |
| REPLAY | Old defect and repaired control under pinned/versioned oracles | Rewriting old evidence or freezing future valid production |

### Decision vocabulary

| Decision | When appropriate |
| --- | --- |
| VERIFIED_SOFTWARE_FIX | A reproducible software counterexample is fixed under independent bounded tests |
| ACCEPTED_ENGINEERING_STATE | A native guarded Git write, Receipt and event chain establish an authorized state transition |
| ACCEPTED_AS_OBSERVATION | The dated source accurately supports a scoped observation without scientific promotion |
| REVISED | Previous assertion was corrected; both original and correction remain inspectable |
| BLOCKED | An explicit governance gate or missing prerequisite prevents execution or write |
| PARTIAL | Some relevant sources or jobs were checked but the requested whole cannot be proven |
| INDETERMINATE / UNKNOWN | Evidence is insufficient, absent, contradictory or externally owned |
| NO_MATERIAL_CHANGE / NO_CHANGE_REQUIRED | A full bounded check finds no justified mutation |
| SCIENTIFICALLY_VALIDATED | **Never derive from the statuses above**; requires a separately preregistered, suitable scientific oracle and review |

## G. Reproducible reviewer checklist

- Re-read current remote main and check it stayed pinned across the observation; do not reuse historical snapshots as current
- Enumerate all reachable Commit parents and distinct Git Trees, preserving historical-only witnessed paths
- Enumerate every PR including closed-unmerged; retain original titles and separate Agent self-description from observed execution
- Enumerate every currently visible Run with complete pagination, reconcile exact prior IDs, and read actual Jobs for the new population
- Re-read scheduled definitions by version, calculate only nominal-to-created gaps, and keep dispatch/queue causes UNKNOWN
- Inspect failing Jobs inside cancelled Runs and successful Runs containing skipped Jobs; preserve warnings
- Verify current accepted production from actual data, linked Receipt/Event and guarded Git commits, not documentation claims
- Cross-check all public Markdown against the exact governed documentation registry and allowed new-path families
- Run frozen archive, current file classification, three-asset, Framework and production integrity tests without modifying production
- Merge only a reviewed and successful PR if an authorized write is warranted; retain no-change outcomes and refrain from unnecessary Release/DOI

**Privacy:** only public Git IDs, bounded error classes, typed statuses, non-sensitive diagnostics and relevant citations are retained; no private prompts, identifying biographies, credentials, unrelated personal data, copyrighted upstream scientific bodies or private provider responses.

**Bottom line:** The goal is not to make all earlier failures disappear or to increase GitHub activity. The reusable research contribution is a **testable distinction among evidence, execution, accepted state and scientific truth**, together with a failure-to-repair-to-replay chain that survives version changes, absent logs, new Agents and future legitimate production events.
