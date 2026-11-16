# External Agent research handoff · optional interoperability

## 中文专业内容对应 / Chinese technical counterpart

**本文件确切边界 / Actual subject:** 异构 Agent 可以提交 proposal-only 研究与 PR，但 GitHub 账户署名不能独立证明不同 Agent Runtime 的真实身份

**English owning title:** External Agent research handoff · optional interoperability

**可核验证据 / Required evidence:** 单独固定执行者、准确源码版本、具体输入 bytes、来源授权、实际命令与返回数据，以及人工接受或拒绝的记录，缺失的外部来源和历史运行日志保持未知 / Preserve independent actor, revision, input, source eligibility, execution and human disposition identities, a documentation check never proves biological truth

| English source section / 原文章节 | 中文专业定位 / Chinese subject map |
| --- | --- |
| Three deliberately separate clocks | 该软件研究对象的实现机制与限制 |
| Pull-request gate participation | 该软件研究对象的实现机制与限制 |
| Optional handoff lifecycle | 该软件研究对象的实现机制与限制 |
| Files and minimum executable interface | 该软件研究对象的实现机制与限制 |
| Cache and durable-state hygiene | 该软件研究对象的实现机制与限制 |
| Evidence limitations | 该软件研究对象的实现机制与限制 |
| Independent reviewer base check | 该软件研究对象的实现机制与限制 |
| Heterogeneous multi-Agent research submissions | 该软件研究对象的实现机制与限制 |

**四资产分界 / Four-asset boundary:** 原生 Knowledge Workflow 是唯一受门禁约束的 `data/` 接受路径，Evidence CLI、Bio CLI 和独立 Framework 不会因为组合调用而继承写入授权 / Only the guarded native lifecycle owns accepted knowledge writes, no peer asset or Agent proposal inherits that authority


The frozen `v0.4.0` Life Science Ecosystem Lab release has **three peer software assets**, not an embedded Agent orchestration service. The current source tree also has one separately packaged experimental [Framework](../framework/README.md) for software-contract assessment. The independent [Bio Tool](../bio_tool/README.md) processes supplied protein FASTA/PDB files without an Agent. The existing [Knowledge Workflow](../.github/README.md) is authoritative for approved-source ingestion, native topic matching, graph projection, accepted `data/` state, receipts and Git-based replay; the independent [Evidence Tool](../evidence/README.md) is a reusable validator and inspector. None requires an LLM API or an Agent scheduler.

## Three deliberately separate clocks

| Plane | Scheduler or executor | Authority | Where the contract lives |
| --- | --- | --- | --- |
| Native knowledge maintenance | GitHub Actions schedule or authorized manual `persist=true` | Approved GitHub source registry, native topic rules and guarded `data/` writes | [Native production Workflow](../.github/workflows/life-science-knowledge.yml) |
| Independent Evidence Tool | CLI or separate Tool CI | Stateless verification/report paths, not the knowledge ledger | [Evidence Tool](../evidence/README.md) |
| External research Agent (Jules, GPT scheduled tasks, other systems) | **Its own** user-authorized task cadence | Research/discovery/proposals only; no implicit write authority | [Agent SOP](../.github/agent-handoff/SOP.md), [task template](../.github/agent-handoff/TASK_TEMPLATE.md) |

No recurring external-Agent schedule is created by this repository, and no native `workflow_dispatch` is triggered merely by creating an Agent handoff.

## Pull-request gate participation

An external Agent or GitHub App may propose ordinary branch changes and receive the same required validation as any human contributor. Validation is based on repository content, not `github.actor`, provider identity or LS affiliation. The independent gate domains continue running after a sibling failure and the final verdict fails unless all required domains succeed

This is execution access, not trust transfer. Passing CI does not authorize accepted `data/` writes, source/topic expansion, scientific promotion or an external registration claim. LifeMonitor and registry availability are not required CI dependencies; they evaluate public assets through their own interfaces and schedules

## Optional handoff lifecycle

`External network research → Source citations and uncertainties → PROPOSAL_ONLY handoff → Shape validation → Human review / PR → Independent software checks → Ordinary native acceptance (only when separately authorized)`

A handoff is **not** a native evidence candidate. It cannot be imported as `data/inputs/current/candidate.json` and does not automatically expand `evidence/profiles/sources.json` or `topics.json`. Proposals may request new research keywords or sources, but those modifications need ordinary reviewed changes and native tests. The Agent does not redefine the native topic taxonomy simply because it searched an additional term.

## Files and minimum executable interface

- [Root AGENTS.md](../AGENTS.md): repository-level instruction boundary for multiple external Agents
- [SOP](../.github/agent-handoff/SOP.md): fresh-run, research, evidence, uncertainty, review and closeout steps
- [Task template](../.github/agent-handoff/TASK_TEMPLATE.md): reusable research instruction without creating an in-repo Agent service
- [Example JSON](../.github/agent-handoff/example-handoff.json): synthetic proposal sample; not an accepted research claim
- `evidence/agent_handoff.py`: standalone standard-library-only shape and authority check

Run the optional proposal validation:

```sh
python -m evidence validate-handoff \
  --input .github/agent-handoff/example-handoff.json \
  --topics evidence/profiles/topics.json
```

Successful output is `AGENT_HANDOFF_SHAPE_VALID_PROPOSAL_ONLY`, never `EVIDENCE_VERIFIED` or `APPLIED`. This check requires a bounded JSON envelope, known native topic references, unverified cited observations, safe proposed file paths, mandatory human review and no proposed direct `data/` mutation. GitHub file citations using `/blob/` must include a frozen 40-character commit SHA. Other HTTPS citations are not independently retrieved by this check, so a valid envelope is still only a **proposal**.

A meaningful research handoff may be `NO_FINDINGS` with zero findings or proposals. A scheduler must not fabricate a finding to claim a completed research unit. Unknown or unverified claims require independent human/tool review before any source or topic registry change.

## Cache and durable-state hygiene

The tracked repository was checked for common Python caches, build products, log files and temporary directories. No tracked generated trash was found at the time of the audit. Keep reproducible local intermediates under ignored `build/` or `.agent-work/`; do **not** delete `data/`, `evidence/field-tests/`, accepted receipts, manifests, historical research observations or their immutable Git commits.

Runner-local workspaces and hosted Actions artifact retention are separate from Git-tracked files. `.gitignore` cannot erase remotely stored workflow artifacts, Actions caches or historical Git objects. No automatic cache deletion is part of the Agent handoff.

## Evidence limitations

`SOURCE_MATCH` is a topic/document lexical relationship, not a life-science result. Agent-generated explanations, registration claims and research interpretations cannot be promoted to accepted production facts without independent checks. Explicitly preserve source licensing, credential safety, counterevidence, reproducible steps and the boundary between public source citation and republication of full source text.

[Production Operations](PRODUCTION_OPERATIONS.md) · [Provenance](PROVENANCE.md) · [Understanding Verification](VERIFYING_RESULTS.md)

## Independent reviewer base check

An optional handoff `base: {commit, observed_at}` is agent-supplied provenance metadata; structural validation alone does **not** verify that the commit exists or is fresh. Reviewers can supply the independently fetched current target default-branch SHA:

```sh
ls-evidence validate-handoff --input .github/agent-handoff/example-handoff.json --topics evidence/profiles/topics.json --expected-base-sha <trusted-current-default-branch-sha>
```

Matching SHA indicates declared equality to that independently chosen review baseline, not experimental validation, Git ancestry, authorship, or a claim that upstream scientific methods and measurements are correct. A stale older anchor must be re-reviewed against current runtime and data contracts, rather than silently treated as a fresh run. Historical no-base schema 1.0.0 handoffs remain shape-valid without `--expected-base-sha`.

## Heterogeneous multi-Agent research submissions

A locally run IDE Agent, a cloud research observer and a desktop engineering Agent can each submit different kinds of research work via PR. Their GitHub submissions are auditable even when the `lostlight530` Git credential is shared. Use the optional `proposer` fields (`agent_label`, `execution_surface`, `assertion: "SELF_DECLARED"`) only as claims of origin, never as verified execution attestations. Reviewers should preserve unverified/superseded claims and record meaningful corrections without replacing the contributor's original words.

See [Agent cohort research case](AGENT_CLUSTER_RESEARCH_CASE.md) and [review decision ledger](AGENT_REVIEW_DECISIONS.md). The proposal/review path is research collaboration, not a transfer of `data/` write authority, automated source registry permission or biological scientific proof.
