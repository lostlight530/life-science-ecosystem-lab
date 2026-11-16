# LS Framework Contract Challenge 001

## 中文专业证据对应 / Chinese evidence counterpart

**历史或实现对象 / Exact subject:** 合成突变的反例检验仅支持 hand-authored 软件合同回归，需另行设计有统计效力的独立领域实验

**Original English title:** LS Framework Contract Challenge 001

**证据对象 / Evidence object:** GitHub PR/Run、Tool/Framework 合同、真实研究结果、Agent 自报身份及人工复核应按所属来源和日期分别存放，过去的 failed、closed-unmerged 与 unknown 不能被新文档擦除 / Preserve original objects, chronology, failed and unmerged dispositions, and independently witnessed source evidence

| English original section | 中文阅读定位 |
| --- | --- |
| Falsifiable hypothesis | 可证伪命题 |
| Independent execution | 实际独立执行条件 |
| Test design | 测试设计 |
| Current evaluation limits | 当前结果的局限 |
| Standards references and ownership | 证据与限界条件 |

**状态 / Status:** 这是中英双语文档校准，没有新运行任何实验、外部机构验证或生产数据接受 / This is documentation clarification, not new scientific execution, external certification or production acceptance


Status: **synthetic software-engineering challenge**, not a scientific benchmark or a verified integration of genomics/imaging pipelines

## Falsifiable hypothesis

Given a frozen, locally byte-verified example declaring life-sciences software artifacts from genomics and microscopy, the independent Framework should reject invalid provenance/lineage/method-domain contracts, preserve indeterminate evidence, and produce identical outputs when replayed against identical bytes

The test deliberately does **not** assess correctness of biological labels, experimental samples, assays, gene expression, microscopy pixels or clinical decisions

## Independent execution

Install only the Framework distribution, from the repository root, then run:

```sh
python -m pip install --no-deps -e ./framework
python -m unittest discover -s framework/tests -v
python -m ls_framework.challenge --bundle framework/fixtures/software-cross-domain.json --root framework/fixtures --output build/framework-challenge.json
```

The report includes the input digest, exact case digests, expected versus observed statuses and finding codes, missed cases, and declared nonclaims, without network calls, external LLMs, timestamps or production writes

The challenge fails closed for malformed objects. Its report path cannot replace the input bundle, write inside the selected evidence root or target a discovered repository `data/` / `.git/` tree, including when invoked from a checkout subdirectory. Non-finite and excessively nested JSON return a structured input failure; output-write failures return a structured output failure. These guards are not a general filesystem sandbox and do not eliminate concurrent filesystem races. Input-shape failures remain machine-readable and must not be interpreted as completed challenge cases

## Test design

- Nominal and controlled domain-renaming cases ensure that the contract does not hard-code one assay
- Deliberately swapped SHA-256, out-of-scope domain, undeclared method-domain applicability, illegal paths and missing asset references are expected to **FAIL**
- Empty bundles, multi-asset bundles without lineage, multiple producers, cyclic lineage and missing outputs are expected to **FAIL**
- External objects with only declared checksums, failed execution declarations, disconnected lineages and scientific proposals are expected to be **INDETERMINATE**
- Scientific-acceptance escalation in user-provided evidence is expected to **FAIL**
- A deliberately damaged reference bundle must cause the challenge to fail, to verify the harness is not vacuously green

The independent test oracle is a *declared engineering specification*, not an annotation of biological ground truth. Its correctness may be revised through normal review with versioned test changes

## Current evaluation limits

The challenge has intentionally synthetic data, authored mutation cases and authored expected findings. A green report demonstrates that this set of regression scenarios agrees with the current contract implementation. It **does not** establish population-level sensitivity/specificity, false positive rates on real datasets, cross-domain biological integration, independent execution attestation or compliance with any external standard

Subsequent research should freeze independent publicly reusable examples from distinct life-sciences software systems, compare a schema-only baseline with domain-aware validators and the Framework, and record disagreements or failure as valid outcomes

## Standards references and ownership

- [FAIR4RS principles](https://doi.org/10.1038/s41597-022-01710-x): unique software/version identifiers, metadata, interoperability and reuse
- [W3C PROV-O](https://www.w3.org/TR/prov-o/): Entity, Activity and Agent vocabulary for qualified provenance
- [ISA investigation/study/assay model](https://isa-specs.readthedocs.io/en/latest/isamodel.html): research metadata categories
- [RO-Crate specification](https://www.researchobject.org/ro-crate/specification): research object metadata packaging
- [GA4GH Data Repository Service](https://www.ga4gh.org/product/data-repository-service-drs/): standardized data-object retrieval

These are independently maintained references, not specifications or validation results issued by LS Framework. This challenge does not claim conformance to FAIR4RS, PROV-O, ISA, RO-Crate or DRS

Reference selection reviewed on 2026-10-25; adoption of new external versions requires separate version pins, tests and decisions
