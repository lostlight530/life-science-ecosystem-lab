# Standards mapping and external status

[Documentation index](README.md) · [Understanding results](VERIFYING_RESULTS.md)

This document lists supported *software-interface mappings*, not certifications.

| Standard / service | Repository interface | Meaning |
| --- | --- | --- |
| Workflow RO-Crate 1.1 | `ro-crate-metadata.json` | Main native lifecycle is identified; CWL 1.2 computational replay is a separate portable artifact |
| Workflow Testing RO-Crate 0.2 | RO-Crate testing records | Links to executable tests and GitHub Actions test resources; structural preflight only |
| CWL 1.2 | `.github/knowledge/main.cwl` | Offline, reference-runner-tested computational sub-workflow |
| Bioschemas | `metadata/bioschemas-*.jsonld` | Separately named workflow and tool identities; self-description is not third-party certification |
| Citation File Format 1.2.0 | `CITATION.cff` | Frozen v0.4.0 three-asset software citation and Zenodo DOI |
| CodeMeta 3.0 | `codemeta.json` | Current repository component inventory, including the later experimental Framework boundary |
| W3C PROV-O / SKOS | Source and relationship export vocabulary guidance | Internal JSONL is not claimed to be RDF or PROV-O/SHACL conformant |
| FAIR4RS | External research software principles for identity, interoperable interfaces and reuse | Framework's project-defined contract is not independently audited for FAIR4RS conformance |
| ISA investigation/study/assay | External multi-omics research metadata model | Framework does not parse or validate full ISA investigations or scientific study designs |
| GA4GH Data Repository Service (DRS) | External standard for logical data-object retrieval | Framework does not expose a DRS endpoint or claim GA4GH compliance |
| Software Heritage SWHID | Optional immutable source object identifier | Only use real computed/archived identifiers, never invent them |
| WorkflowHub | External public workflow record | Version 2 of WorkflowHub 2347 is publicly verified as CWL with DOI `10.48546/workflowhub.workflow.2347.2`; this does not prove automatic LifeMonitor synchronization or scientific validity |
| LifeMonitor | Installed GitHub App + root `lifemonitor.yaml` + private local WTROC upload | Workflow `cc202b33-cd3e-48cc-8004-8e8db87bd200`, suite `05f4e427-ebcc-4650-ab97-2348c0788a32` and test instance `18d116e5-3806-4103-950a-8b65ab75d7f4` were maintainer-observed with one passing test on 2026-10-18 |
| bio.tools + EDAM | `bio_tool/`, `metadata/biotools-protein-audit.draft.json` | Actual FASTA/PDB processing and reviewed EDAM mappings correspond to the maintainer-observed record `biotools:life-science-protein-file-audit`; API verification and curation status remain separate |
| OpenEBench | Synchronized tool-monitor record | The tool ID was maintainer-observed as an active metadata record with upstream `validated=0`; this is synchronization evidence, not an OpenEBench benchmark or scientific validation |
| Zenodo | Repository software release | DOI `10.5281/zenodo.23447089` identifies the frozen GitHub `v0.4.0` three-asset release; it is not the WorkflowHub workflow DOI and does not include the later experimental Framework |

The [external interoperability review](INTEROPERABILITY_REVIEW.md) provides a dated, source-linked compatibility and independent-object comparison worksheet, including the separation between Workflow Testing RO-Crate and Workflow Run RO-Crate. It does not upgrade any pinned descriptor or certify a new service state.

## Current external RO-Crate release versus reviewed project pins

The community [RO-Crate specification index](https://www.researchobject.org/ro-crate/specification.html) identifies [RO-Crate 1.3](https://www.researchobject.org/ro-crate/specification/1.3/index.html), published 2026-06-22, as the current long-term generic release (verified 2026-10-25). This repository still implements **separately reviewed** Workflow RO-Crate 1.1 and Workflow Testing RO-Crate 0.2 interfaces for its released workflow and LifeMonitor records. A generic 1.3 update does not itself authorize a WorkflowHub/LifeMonitor contract migration.

### Compatibility watch: generic crates, workflow profiles and run evidence

The [RO-Crate 1.3 release notes](https://www.researchobject.org/ro-crate/blog/2026-06-23/announcing-ro-crate-1-3) explicitly change the JSON-LD context bindings for `ComputationalWorkflow`, `FormalParameter`, `input` and `output` to `https://bioschemas.org/terms/`. A context change affects the expanded RDF term identities used by consumers; it must not be treated as a cosmetic version-string edit or retroactively applied to the archived `v0.4.0` crate. These namespace changes alone do not establish that this repository's pinned files failed their declared earlier-version preflight.

The [Workflow Run RO-Crate changelog](https://www.researchobject.org/workflow-run-crate/profiles/changelog.html) documents its **0.6** profiles (2026-09-07) against generic RO-Crate **1.3** and Workflow RO-Crate **1.1**. **Workflow Run RO-Crate 0.6 is not Workflow Testing RO-Crate 0.2**: run provenance and declared CI test suites are different evidence objects. This repository currently claims the latter's bounded structural test metadata, not a newly verified Workflow Run RO-Crate 0.6 artifact or independent execution attestation.

Any future migration must first pin the target generic context and specific profile together, inspect expanded term mappings, build and validate a versioned candidate on frozen inputs, check WorkflowHub/LifeMonitor consumer behavior as an **external** acceptance question, and obtain normal review before changing released descriptors. Existing accepted `data/`, registered archives and DOIs remain historical objects; a local preflight or green CI cannot rewrite their past versions.

The [RDA FAIR4RS Recommendation](https://doi.org/10.15497/RDA00068) and [FORCE11 software citation checklist](https://github.com/force11/force11-sciwg/blob/master/guidance/software_citation_checklist_for_developers.md) distinguish component-specific and version-specific software identities. The earlier `v0.4.0` Zenodo DOI does not encompass or certify the later experimental Framework 0.1.0. [W3C PROV-O](https://www.w3.org/TR/prov-o/) models provenance with entities, activities and agents; similarly named local JSON fields are **not** proof of interoperable PROV-O RDF or independently attested method execution.

Reference documents:

- [Workflow RO-Crate 1.1](https://about.workflowhub.eu/Workflow-RO-Crate/1.1/)
- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [W3C SKOS](https://www.w3.org/TR/skos-reference)
- [bio.tools Curators Guide](https://biotools.readthedocs.io/en/latest/curators_guide.html)
- [CodeMeta](https://github.com/codemeta/codemeta)
- [Software Heritage SWHID](https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html)

Do not replace GitHub Actions as the native scheduler just to meet external WorkflowHub conventions. External workflow registration should instead describe the actual portable executable and its test relationship honestly.

## Local readiness and external acceptance

Use `ls-evidence audit-ecosystem --root . --output build/interop.json` before considering external services. This command never logs in or changes a public registry. The existing RO-Crate root identifies the native GitHub Actions lifecycle while the portable CWL sub-workflow is a separate entity: a standalone `.crate.zip` with executable CWL as the **main workflow** is built reproducibly by `.github/scripts/build_portable_workflow_crate.py` and tested in CI. Local readiness remains distinct from the external records listed below.

| Service | Specific independent criterion | Current repo scope |
| --- | --- | --- |
| WorkflowHub | Workflow RO-Crate 1.1 requires a typed main workflow, programmingLanguage, license, and a ZIP with root metadata; registry entry is created only by an actual upload/registration | Public version 2 identifies the portable CWL workflow, release commit and deterministic archive hash |
| LifeMonitor | Workflow Testing RO-Crate links main workflow, test suite, test instance, and compatible CI service; monitoring requires actual enrollment | A private direct local WTROC upload is enrolled and its GitHub Actions test instance was maintainer-observed passing on 2026-10-18 |
| bio.tools | Curator scope requires actual bioinformatics data-processing operations and appropriate EDAM topic/operation/input/output terms | The independent FASTA/PDB processor has the maintainer-observed ID `life-science-protein-file-audit`; record existence does not establish independent API verification or curation approval |
| OpenEBench | A synchronized monitoring record and a scientific benchmark are different evidence objects | The synchronized tool record is observed, but `validated=0` and no performance benchmark or scientific result is claimed |
| Zenodo | DOI metadata must correspond to an actually archived release | Record 23447089 corresponds to `v0.4.0`; the later experimental Framework remains outside that frozen release |

Evidence gates are `LOCAL_PREFLIGHT → SUBMITTED → ACCEPTED → EXTERNALLY_VERIFIED`; platform submission is a separate user-authorized action and requires a stable public record URL. Neither an identity connection nor a completed local preflight is accepted registration, and external adoption requires separately sourced use evidence.

References: [Workflow RO-Crate 1.1](https://about.workflowhub.eu/Workflow-RO-Crate/1.1/), [WorkflowHub metadata submission](https://about.workflowhub.eu/docs/registering_workflows/complete-workflow-metadata/), [LifeMonitor test monitoring](https://lifemonitor.eu/lm_test_monitoring), [LifeMonitor WTROC guide](https://lifemonitor.eu/making_a_wtroc), [bio.tools curator guide](https://biotools.readthedocs.io/en/latest/curators_guide.html).

## Portable CWL package

```sh
python .github/scripts/build_portable_workflow_crate.py build/life-science-portable.cwl.crate.zip
```

The portable archive declares CWL as its main workflow, includes synthetic replay fixtures, and excludes accepted production `data/` and private information. GitHub Actions remains the native owner of live observations and guarded persistence. The WTROC uses LifeMonitor's documented `GithubService`, `https://api.github.com` instance URL and repository workflow resource form. A direct local upload was observed with a passing monitored test instance on 2026-10-18. WorkflowHub 2347.2 is a separate public record; the failed registry-import attempt and successful local upload must not be presented as automatic synchronization.

## Third independently callable Bio Tool

`ls-bio protein-fasta` and `ls-bio protein-pdb` implement actual biological data processing, separately from software inspection and source-grounded knowledge generation. The repository-side `metadata/biotools-protein-audit.draft.json` preserves the metadata corresponding to the maintainer-observed record `biotools:life-science-protein-file-audit` and uses EDAM operation_2403 / operation_2406, data_2976 / data_1460 / data_2955, and format_1929 / format_1476 for the supported formats. The filename is retained to avoid needless path churn; it is a repository-side metadata source, not a claim that the registry exported or independently validated these exact bytes. The related OpenEBench object proves that a record was synchronized into that service at the observed time, while its `validated=0`, absent version and absent benchmark results keep validation and performance explicitly unclaimed.
