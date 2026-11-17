# Real-world life-science read-only field drill · 2026-10-17

## 中文专业证据对应 / Chinese evidence counterpart

**历史或实现对象 / Exact subject:** 2026-10-17 只读现场演练记录真实 GitHub Source 和 Actions 操作，不意味着后续平台状态或者生物学证明

**Original English title:** Real-world life-science read-only field drill · 2026-10-17

**证据对象 / Evidence object:** GitHub PR/Run、Tool/Framework 合同、真实研究结果、Agent 自报身份及人工复核应按所属来源和日期分别存放，过去的 failed、closed-unmerged 与 unknown 不能被新文档擦除 / Preserve original objects, chronology, failed and unmerged dispositions, and independently witnessed source evidence

| English original section | 中文阅读定位 |
| --- | --- |
| Actual GitHub Actions runs | 实际观察的 Actions 运行 |
| Real live-source results | 真实来源的时点观察 |
| Independent external software preflight | 外部软件预检 |
| Rerun without data writes | 证据与限界条件 |

**状态 / Status:** 这是中英双语文档校准，没有新运行任何实验、外部机构验证或生产数据接受 / This is documentation clarification, not new scientific execution, external certification or production acceptance


This is **observed external-source field evidence**, not a synthetic CWL fixture, a product claim, a registry registration, or an accepted main-branch knowledge snapshot.

## Actual GitHub Actions runs

- [Initial read-only field run #38993852474](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/38993852474) — actual source collection and two third-party inspections; surfaced overly broad citation and root-RO-Crate warnings
- [Corrected real-world rerun #38994004639](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/38994004639) — same real sources, narrowed warning statements and recognized `CITATIONS.md`
- [Checked-in compact field evidence index](../evidence/field-tests/2026-10-17-live-readonly.json) — anchored run, observed commit IDs, input/output and graph digests, report hashes and limitations
- The GitHub run has a short-retention ZIP Artifact containing inspection JSON, Markdown, SARIF, diagnostics and graph manifest. **The ZIP is not a production release or frozen long-term upstream corpus**

## Real live-source results

| Approved public source | Observed immutable commit | Selected documents |
| --- | --- | ---: |
| `workflowhub-eu/about` | `3b30f0c9e0f750929c3c4a310f1212af498b0c0c` | 11 |
| `crs4/life_monitor` | `7649406c11c5c04eebc5ca61926f5dbe30469c82` | 2 |
| `seek4science/seek` | `e47e21f6517ae0a0808c18b733ec7bdbea64e593` | 1 |
| `common-workflow-language/cwl-v1.2` | `979083396fee912fca8ef778174216d317338a00` | 1 |

Results: **4/4 sources, 15 selected documents, zero source diagnostics**, eligible source bundle, 3 topic maps labeled `MULTI_SOURCE`, 17 graph nodes and 26 `SOURCE_MATCH` edges. Graph edges document deterministic topic matching, not an empirical or causal relation. The two real reports below are both **WARN**, not certification.

## Independent external software preflight

| External repository and pinned version | Findings | What the field test established |
| --- | --- | --- |
| [nf-core/rnaseq](https://github.com/nf-core/rnaseq/tree/95dbcd977a74a4d1b2a3954abb90df3851014afa) | 2 PASS, 2 WARN, 0 FAIL | README exists; RO-Crate mainEntity points to the existing `main.nf`; `CITATIONS.md` exists although `CITATION.cff` does not; no inspected root Bioschemas descriptor |
| [crs4/life_monitor](https://github.com/crs4/life_monitor/tree/7649406c11c5c04eebc5ca61926f5dbe30469c82) | 1 PASS, 3 WARN, 0 FAIL | README exists; no root `CITATION.cff`, root RO-Crate or inspected root Bioschemas descriptor. The service has nested workflow/crate examples; absence of a root workflow RO-Crate is not proof of absent RO-Crate support |

The real `nf-core/rnaseq` result exposed the danger of claiming "citation metadata absent" when a project uses a recognized `CITATIONS.md` convention and README DOI. The Evidence Tool now describes the alternative precisely while keeping a CFF-conformance warning.

## Rerun without data writes

After this workflow is merged to the default branch, use **GitHub Actions → Life Science Live Evidence Drill — Read Only → Run workflow**. No `persist` input or `contents: write` permission exists here. The push trigger is intentionally restricted to the one dedicated experimental branch. The workflow:

1. Uses the installed project CLI with a read-only GitHub token to collect from the four approved sources and validate the aggregate candidate
2. Builds/verifies the real source-cited knowledge map, JSONL graph and bounded FTS5 search
3. Checks out two **pinned external repository commits**, then applies `ls-evidence inspect` **without executing their code**
4. Uploads only bounded metadata, diagnostics and inspection reports, **not the collected full upstream text and not a `data/` production commit**

Check `source-diagnostics.json`, `eligible_for_projection`, and each report `status`. A successful field run is evidence of **read-only observed behavior only**. A durable production run requires separate authorization, state verification and an accepted `data/` Git commit.

[Verification](VERIFYING_RESULTS.md) · [Provenance](PROVENANCE.md) · [Maintenance](MAINTENANCE.md)
