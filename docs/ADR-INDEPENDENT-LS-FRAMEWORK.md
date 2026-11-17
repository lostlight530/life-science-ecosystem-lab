# ADR: independent life-sciences cross-domain software engineering framework

## 中文专业内容对应 / Chinese technical counterpart

**本文件确切边界 / Actual subject:** 实验性的独立 Framework 只验证软件工程合同，非第四个 Tool、非 0.4 归档组成物、非生物学裁决器

**English owning title:** ADR: independent life-sciences cross-domain software engineering framework

**可核验证据 / Required evidence:** 单独固定执行者、准确源码版本、具体输入 bytes、来源授权、实际命令与返回数据，以及人工接受或拒绝的记录，缺失的外部来源和历史运行日志保持未知 / Preserve independent actor, revision, input, source eligibility, execution and human disposition identities, a documentation check never proves biological truth

| English source section / 原文章节 | 中文专业定位 / Chinese subject map |
| --- | --- |
| Context | 该软件研究对象的实现机制与限制 |
| Implemented architecture decision | 该软件研究对象的实现机制与限制 |
| Explicit engineering invariants | 该软件研究对象的实现机制与限制 |
| Research method and assessment | 该软件研究对象的实现机制与限制 |
| Standards relationship | 标准对照与符合性限制 |

**四资产分界 / Four-asset boundary:** 原生 Knowledge Workflow 是唯一受门禁约束的 `data/` 接受路径，Evidence CLI、Bio CLI 和独立 Framework 不会因为组合调用而继承写入授权 / Only the guarded native lifecycle owns accepted knowledge writes, no peer asset or Agent proposal inherits that authority


Decision proposed: 2026-10-19
Implementation merged: 2026-10-20 via PR #30 at main commit 20b3cdd03eb1df690ab26ddb2816121df3af54a7
Status: IMPLEMENTED SOFTWARE ASSET · EXPERIMENTAL RESEARCH VALIDATION

PR #29 supplied the original draft and was closed without merging. PR #30 incorporated and hardened the implementation. A merged software implementation does not constitute scientific claim acceptance or external certification

## Context

The current repository separates three software assets: Knowledge Workflow, Evidence Tool and Bio Tool
Cross-domain life-sciences **software engineering** requires a different independent concern: versioned contracts, asset identity, method declarations, lineage, deterministic audits, bounded execution states and negative results across heterogeneous research software

It is not a demand for a biology-specific inference algorithm or universal scientific truth engine

## Implemented architecture decision

Introduce `framework/` at repository root as an independently installable package with its own CLI, fixtures, tests, validation workflow and versioned report structure
The experimental Framework is a fourth independent entity **not** a fourth Tool, not a workflow, and not another scheduling infrastructure
Retain the existing three assets, their independent entrypoints and their read/write boundaries

Do not silently revise official institutional standards, native `data/` acceptance, research profiles, or claimed certifications

## Explicit engineering invariants

1. Core validator imports no existing LS package, external LLM, Agent, GitHub scheduler or network client
2. Data bytes are verified only when actually available and the digest matches; other references remain declarations
3. Input is data, never executed as shell/Python/source instructions or arbitrary URL requests
4. Identity, provenance and execution claims are separately typed; a claimed successful run is not proof of execution
5. Cross-domain software lineage is not a cross-domain biological finding
6. Scientific claims are proposal-only and never accepted or certified by the Framework
7. No production `data/` writes, source/profile expansion or runtime permission escalation
8. Fail-closed bounded input, negative tests and deterministic output are mandatory
9. Human review of methods, evidence and research contributions remains independent of software test status
10. Independent package and CI are checked without creating hard runtime dependencies among assets
11. Byte-addressed text fixtures use repository-pinned LF checkout and must pass on Linux and Windows
12. A multi-asset bundle without explicit lineage steps fails closed rather than receiving a vacuous green verdict

## Research method and assessment

Keep the fixed DEFINE → PIN → QUALIFY → EXECUTE → EVALUATE → AUDIT → REVIEW → REPLAY lifecycle
Use life-sciences domains as replaceable testing contexts for *shared software contracts*
Compare with basic schema validation and domain-specific validators using independently reviewed frozen cases
Measure detectability of software-contract violations, false positives, failures to reject, replay agreement and method-interface drift

Version 0.1.0 evaluates engineering contract shape and local-file identity only
It does not claim biological validity, scientific conclusion correctness, independent experimental replication, medical fitness or cross-domain analysis success

This experimental version post-dates the frozen repository `v0.4.0` release. It is not covered by the existing Zenodo software DOI, WorkflowHub workflow DOI, LifeMonitor object, bio.tools record or OpenEBench synchronization record

## Standards relationship

ISA, W3C PROV-O, ECO, RO-Crate and BioCompute are externally governed references
They are not redefined, endorsed, or officially certified by this project
Future adapters require explicit independent tests and version pins before their interoperability can be claimed
