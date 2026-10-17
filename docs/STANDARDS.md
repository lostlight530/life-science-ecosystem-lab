# Standards mapping and external status

[Documentation index](README.md) · [Understanding results](VERIFYING_RESULTS.md)

This document lists supported *software-interface mappings*, not certifications.

| Standard / service | Repository interface | Meaning |
| --- | --- | --- |
| Workflow RO-Crate 1.1 | `ro-crate-metadata.json` | Main native lifecycle is identified; CWL 1.2 computational replay is a separate portable artifact |
| Workflow Testing RO-Crate 0.2 | RO-Crate testing records | Links to executable tests and GitHub Actions test resources; structural preflight only |
| CWL 1.2 | `.github/knowledge/main.cwl` | Offline, reference-runner-tested computational sub-workflow |
| Bioschemas | `metadata/bioschemas-*.jsonld` | Separately named workflow and tool identities; self-description is not third-party certification |
| Citation File Format 1.2.0 | `CITATION.cff` | Repository-level software citation |
| CodeMeta 3.0 | `codemeta.json` | Machine-readable research software metadata and peer asset pointers |
| W3C PROV-O / SKOS | Source and relationship export vocabulary guidance | Internal JSONL is not claimed to be RDF or PROV-O/SHACL conformant |
| Software Heritage SWHID | Optional immutable source object identifier | Only use real computed/archived identifiers, never invent them |
| WorkflowHub | External publication opportunity | Not registered/accepted unless confirmed externally |
| LifeMonitor | Installed GitHub App + `.lifemonitor.yaml` | Genuine Bot PR #15 accepted; global branch/tag tracking retained; test enrollment and periodic monitoring separate |
| bio.tools + EDAM | `bio_tool/`, `metadata/biotools-protein-audit.draft.json` | Actual FASTA/PDB processing, reviewed EDAM operations/data/formats and unsubmitted candidate; accession and eligibility require registry verification |

Reference documents:

- [Workflow RO-Crate 1.1](https://about.workflowhub.eu/Workflow-RO-Crate/1.1/)
- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [W3C SKOS](https://www.w3.org/TR/skos-reference)
- [bio.tools Curators Guide](https://biotools.readthedocs.io/en/latest/curators_guide.html)
- [CodeMeta](https://github.com/codemeta/codemeta)
- [Software Heritage SWHID](https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html)

Do not replace GitHub Actions as the native scheduler just to meet external WorkflowHub conventions. External workflow registration should instead describe the actual portable executable and its test relationship honestly.
## Local readiness and external acceptance

Use `ls-evidence audit-ecosystem --root . --output build/interop.json` before considering external services. This command never logs in or changes a public registry. The existing RO-Crate root identifies the native GitHub Actions lifecycle while the portable CWL sub-workflow is a separate entity: a standalone `.crate.zip` with executable CWL as the **main workflow** is built reproducibly by `.github/scripts/build_portable_workflow_crate.py` and tested in CI, while full third-party profile conformance and registration remain independently unverified.

| Service | Specific independent criterion | Current repo scope |
| --- | --- | --- |
| WorkflowHub | Workflow RO-Crate 1.1 requires a typed main workflow, programmingLanguage, license, and a ZIP with root metadata; registry entry is created only by an actual upload/registration | Local RO-Crate and CWL plus synthetic tests; external entry unverified |
| LifeMonitor | Workflow Testing RO-Crate links main workflow, test suite, test instance, and compatible CI service; monitoring requires actual enrollment | GitHub Actions testing and WTROC-related metadata; enrollment and monitoring unverified |
| bio.tools | Curator scope requires actual bioinformatics data-processing operations and appropriate EDAM topic/operation/input/output terms | Independent static research software inspection; domain eligibility and EDAM annotations not asserted |

Evidence gates are `LOCAL_PREFLIGHT → SUBMITTED → ACCEPTED → EXTERNALLY_VERIFIED`; platform submission is a separate user-authorized action and requires a stable public record URL. Neither an identity connection nor a completed local preflight is accepted registration, and external adoption requires separately sourced use evidence.

References: [Workflow RO-Crate 1.1](https://about.workflowhub.eu/Workflow-RO-Crate/1.1/), [WorkflowHub metadata submission](https://about.workflowhub.eu/docs/registering_workflows/complete-workflow-metadata/), [LifeMonitor test monitoring](https://lifemonitor.eu/lm_test_monitoring), [LifeMonitor WTROC guide](https://lifemonitor.eu/making_a_wtroc), [bio.tools curator guide](https://biotools.readthedocs.io/en/latest/curators_guide.html).

## Portable CWL package

```sh
python .github/scripts/build_portable_workflow_crate.py build/life-science-portable.cwl.crate.zip
```

The portable archive declares CWL as its main workflow, includes synthetic replay fixtures, and excludes accepted production `data/` and private information. GitHub Actions remains the native owner of live observations and guarded persistence. The LifeMonitor GitHub App supports repository checks and can assist with workflow test enrollment when installed by the repository owner. Installation, monitoring and WorkflowHub records require separate external confirmation. Avoid overriding existing LifeMonitor global settings with a repository-specific configuration until its effect is reviewed.

## Third independently callable Bio Tool

`ls-bio protein-fasta` and `ls-bio protein-pdb` implement actual biological data processing, separately from software inspection and source-grounded knowledge generation. The unsubmitted `metadata/biotools-protein-audit.draft.json` uses EDAM operation_2403 / operation_2406, data_2976 / data_1460 / data_2955, and format_1929 / format_1476 for the supported formats. EDAM assignments are semantic descriptors, not third-party certification, and must be independently checked during bio.tools registration.
