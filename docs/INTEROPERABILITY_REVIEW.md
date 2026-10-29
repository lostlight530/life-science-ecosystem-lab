# External interoperability: versioned standards and evidence review

[Documentation index](README.md) · [Standards mapping](STANDARDS.md) · [Cross-asset replay](EVIDENCE_REPLAY_PROTOCOL.md) · [Provenance](PROVENANCE.md)

**Review date:** 2026-10-29. This is a project-owned **read-only compatibility and evidence worksheet**, not an official profile, certification report or a claim that external registries were modified. Official upstream publications govern their standards; this repository governs only its own versioned implementation, historical releases and reviews.

**Observation discipline:** Official *documentation* was checked as public reference on this review date. Direct live responses from the project-specific bio.tools API, OpenEBench monitoring API and WorkflowHub workflow page were **not independently retrieved in this review**. Previously documented platform records remain **dated historical observations**, not current external statuses. A documentation page being reachable is not a test of a registered object, service uptime, authorization or scientific fitness.

## 1 — Separate the standards before discussing upgrades

| Source authority / pinned specification | What the external source defines | Repository reality and review obligation |
| --- | --- | --- |
| [RO-Crate 1.3](https://www.researchobject.org/ro-crate/specification/1.3/index.html) — 2026-06-22 | Generic RO-Crate metadata model and JSON-LD context | A current generic release is not a permission to rewrite frozen v0.4.0 descriptors or registered records |
| [Workflow RO-Crate 1.1](https://about.workflowhub.eu/Workflow-RO-Crate/1.1/) | Specialized workflow packaging: Root Data Entity, main workflow, programmingLanguage and crate license | The native GitHub lifecycle is distinct from the separately packaged executable CWL sub-workflow; verify the specific proposed mainEntity, not its label alone |
| [Workflow Testing RO-Crate 0.2](https://w3id.org/ro/wftest/0.2) and [LifeMonitor WTROC guidance](https://lifemonitor.eu/making_a_wtroc) | Test suite and test instance relationships for workflow monitoring | Test metadata and a CI test reference describe tests; a passing job alone is not enrollment, scientific reproduction or authorization |
| [Workflow Run RO-Crate 0.6](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/) and [2026-09-07 changelog](https://www.researchobject.org/workflow-run-crate/profiles/changelog.html) | Capturing a particular execution's provenance; profile 0.6 aligns with generic RO-Crate 1.3 and Workflow RO-Crate 1.1 | **Not** the same as Workflow Testing RO-Crate 0.2; no Workflow Run 0.6 artifact is claimed solely by existing GitHub receipts |
| [CWL v1.2](https://www.commonwl.org/v1.2/) | Portable descriptions of executable computational steps | A reference-runner replay of synthetic inputs does not replace GitHub Actions scheduling, source selection, permissions or guarded persistence |
| [bio.tools curator guide](https://biotools.readthedocs.io/en/latest/curators_guide.html) | Bioinformatics application software scope and function-specific EDAM topic, operation, data, format conventions | Bio Tool's FASTA/PDB file audit has real bounded processing; Evidence Tool software inspection is **not** automatically a bioinformatics data-analysis operation |
| [W3C PROV-O](https://www.w3.org/TR/prov-o/) | RDF provenance concepts for entities, activities and agents | Similar names in local receipts do not establish compliant RDF serialization or authenticated Agent execution |
| [FAIR4RS Recommendation](https://doi.org/10.15497/RDA00068) | Principles and guidance for FAIR research software | Source citation and local structure cannot on their own certify complete adoption, practical reuse or scientific trust |

**Version-specific compatibility is an engineering constraint.** Workflow RO-Crate 1.1 explicitly targets generic RO-Crate 1.3 and documents updated Bioschemas term mappings. Workflow Run RO-Crate 0.6 likewise aligns with these versions. This does not imply that a project using earlier pinned testing metadata is broken; evaluate each declared profile, its JSON-LD expansion, generated archive, consumer and expected version separately.

## 2 — Non-cosmetic JSON-LD migration question

The RO-Crate 1.3 context changes the expanded IRIs for **ComputationalWorkflow, FormalParameter, input and output** to the bioschemas.org/terms/ vocabulary. [RO-Crate 1.3 announcement](https://www.researchobject.org/ro-crate/blog/2026-06-23/announcing-ro-crate-1-3) and the [Workflow Run profile changelog](https://www.researchobject.org/workflow-run-crate/profiles/changelog.html) explain why older and newer contexts may expand differently.

A migration requires **all** of the following before changing any implementation: (a) target generic release plus explicit workflow/testing/run profile versions; (b) old and proposed JSON-LD expanded IRI comparison on frozen crates; (c) existing local structural checks and executable CWL replay; (d) consumer-facing validation by the relevant service or documented procedure; (e) review of release/version identity and previously accepted artifacts; and (f) an authorized PR with a rollback strategy.

Do not infer equivalence from JSON property spelling or change a context string without testing its RDF term identities. Do not reinterpret an archived v0.4.0 version DOI as covering the separately packaged experimental Framework 0.1.0.

## 3 — Six independent institutional interfaces

| Service | Owned object and authoritative observation | What remains separately unproven |
| --- | --- | --- |
| [LS Login](https://lifescience-ri.eu/ls-login/) | A federated account identity, service-local authorization and potentially group/VO attributes | Institutional affiliation, permission to publish, or a scientific endorsement from login alone |
| [WorkflowHub](https://about.workflowhub.eu/docs/) | Registered workflow ID **and version**, source link, workflow type and version DOI | Live registration changes, equivalence with a GitHub Actions job, automatic LifeMonitor enrollment |
| [LifeMonitor](https://lifemonitor.eu/making_a_wtroc) | Workflow identity, test suite/instance, visibility, actual observed monitored outcome and time | Public validation from a private local upload, durable uptime or biological reproducibility |
| [OpenEBench](https://openebench.readthedocs.io/en/latest/how_to/2_explore_monitoring_data.html) | Distinct monitoring, benchmark and metadata records with their own fields and clocks | Scientific evaluation or quality certification from a catalog entry or confidence label |
| [FAIRDOMHub/SEEK](https://fairdomhub.org/) | Research assets, investigation/study/assay objects and their own versions/permissions | This repository having created such an object merely because SEEK is used as a source reference |
| [bio.tools](https://biotools.readthedocs.io/en/latest/curators_guide.html) | Tool ID, data/operation annotations, source/update timestamp and curation status if known | Tool being benchmarked, curated or externally tested simply because a listing exists |

A service referenced by LS Login is not automatically accessible; a person's LS Login account does not confer edit rights to each registered workflow or data object. bio.tools, OpenEBench, WorkflowHub, Zenodo, GitHub and a private monitoring dashboard have distinct identities and acceptance mechanisms. See [dated project status](../metadata/standards-status.json) for currently recorded, **historically scoped** observations.

## 4 — Reconcile independently owned software records

The released source and external objects are not aliases for one universal version:

| Object | Persist the real identity | Audit rule |
| --- | --- | --- |
| Repository checkout | Full Git commit SHA and exact file bytes | A branch name is a mutable pointer |
| GitHub release | Tag, linked immutable commit, release time and released component set | A later Framework commit cannot retroactively enter v0.4.0 |
| Zenodo archive | Concept versus version DOI and their actual resolved record/version links | DOI existence is not proof of scientific peer review |
| WorkflowHub workflow | Workflow ID, version, type, version DOI and associated executable | A portable CWL crate is not the native GitHub write-state scheduler |
| LifeMonitor | Workflow UUID, suite UUID, test instance ID, visibility, independently observed run outcome and time | A private dashboard record is not a public, continuous monitoring claim |
| bio.tools | Tool ID, reported version, actually retrieved fields and source timestamp | Catalog record and curator review are distinct |
| OpenEBench | Tool ID, monitoring endpoint, actual observed field values, retrieval time and embedded upstream timestamp | ACTIVE/ultimate-like service labels cannot be promoted to scientific certification |
| Experimental Framework | Independent package version and code commit | It is not included in the frozen three-asset publication |

The repository's historical public WorkflowHub 2347 version 2 / DOI 10.48546/workflowhub.workflow.2347.2, v0.4.0 Zenodo version DOI 10.5281/zenodo.23447089, and maintainer-observed tool record biotools:life-science-protein-file-audit refer to **different objects**. Do not aggregate registry counts or treat one record as a third-party audit of the others.

## 5 — Source-to-downstream metadata discrepancy review

For a claimed bio.tools → OpenEBench propagation difference, freeze **two** independent observations and their permissions, not one conflated timestamp. The [bio.tools API](https://bio.tools/api/tool/life-science-protein-file-audit) and [OpenEBench monitor API](https://openebench.bsc.es/monitor/tool/life-science-protein-file-audit) are the object-specific reference endpoints; availability and current content must be checked at a new observation.

| Field or clock | Preserve per object | Invalid conclusion |
| --- | --- | --- |
| Actual retrieval time | Separate UTC time and HTTP/permission outcome for each request | Upstream update time equals retrieval time |
| Record identity/version | ID, actual version/null/unknown, immutable source when available | A matching tool label guarantees version equality |
| Description, credits, publications, repositories | Exact non-sensitive field values, present/absent/null/empty status, mapping policy | Empty downstream list proves upstream lacked the information |
| Embedded update/time | Service-specific raw value and documented meaning or unknown | Older timestamp alone proves importer failure |
| Comparative result | MATCH / DIFFERENCE / UNMAPPED / INCONCLUSIVE as **human worksheet labels** | Declaring an automated data sync repair or scientific validation |
| Next observation | Exact field or official answer that would resolve uncertainty | Quietly deleting conflicting historical snapshots |

A timestamp discrepancy permits competing explanations such as asynchronous import, caching, transformed fields, filtering or access scope. Without importer-specific evidence, **do not choose a cause**. Revisit original responses, map only comparable fields and retain negative/missing results. These worksheet labels are not new CLI statuses.

**Access result in this review:** the project-specific bio.tools, OpenEBench and WorkflowHub URLs did not yield directly accessible live object data during this check. Therefore no October 29 field-by-field synchronization verdict, new registration, curation approval, manual refresh, benchmark or DOI change is asserted. The repository's 2026-10-18 maintainer-observed records remain historical.

## 6 — Acceptance is a chain of separate decisions

1. **Local specification and code checks** — identify a pinned implementation, run local validators, retain errors and abstentions
2. **Independent software/evidence replay** — reconstruct the same bounded result from identified inputs, without presuming scientific truth
3. **Domain suitability review** — evaluate sampling, uncertainty, negative controls, an appropriate oracle and scientific interpretation separately
4. **Human/repository review** — authorize a specific code change, source admission or claim; preserve dissent and unresolved limits
5. **External action** — submission or registration only with user/service authorization and a real service-side receipt
6. **External observation** — inspect the service's actual object/version/status at a known time; never infer it from a local README
7. **Future change review** — compare immutable historical versions; treat no-change and unavailable data as real outcomes

No step retroactively upgrades previous evidence. An upstream standard, a green CI run, a GitHub App installation, a DOI and a source-linked graph edge belong to different assurance surfaces.

## 7 — Operational boundary and references

This protocol requires **zero changes** to .github/workflows/, .github/runtime/, .github/knowledge/, evidence/ executable Tool code, bio_tool/, framework/src/, tested fixture bytes, accepted data/, source/topic registries, installed external services or account permissions.

- [Workflow RO-Crate 1.1](https://about.workflowhub.eu/Workflow-RO-Crate/1.1/)
- [RO-Crate 1.3 recommendation](https://www.researchobject.org/ro-crate/specification/1.3/index.html)
- [Workflow Run RO-Crate 0.6 changelog](https://www.researchobject.org/workflow-run-crate/profiles/changelog.html)
- [LifeMonitor WTROC documentation](https://lifemonitor.eu/making_a_wtroc)
- [bio.tools curator guidance](https://biotools.readthedocs.io/en/latest/curators_guide.html)

This is a cross-infrastructure review **method**, not an assertion that those organizations certify LS. New scientific cases, parsers, reference datasets or formal version migrations require separate reviewed implementation and independent evidence.
