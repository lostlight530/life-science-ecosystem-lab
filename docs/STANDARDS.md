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
| WorkflowHub | External publication record | `Life Science Knowledge Workflow` is externally observed as WorkflowHub 2347.1; this does not prove LifeMonitor synchronization or independent scientific validity |
| LifeMonitor | Installed GitHub App + root `lifemonitor.yaml` + uploaded WTROC | Workflow `cc202b33-cd3e-48cc-8004-8e8db87bd200` and suite `fc958fb2-1a36-48df-a978-72ace9114eb9` were externally observed with 1 Passing, 0 Some passing, 0 Failing and 0 Unavailable on 2026-10-18 |
| bio.tools + EDAM | `bio_tool/`, `metadata/biotools-protein-audit.draft.json` | Actual FASTA/PDB processing and reviewed EDAM mappings correspond to the maintainer-observed record `biotools:life-science-protein-file-audit`; API verification, curation status and OpenEBench evaluation remain separate and unverified |

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
| WorkflowHub | Workflow RO-Crate 1.1 requires a typed main workflow, programmingLanguage, license, and a ZIP with root metadata; registry entry is created only by an actual upload/registration | WorkflowHub 2347.1 is externally observed for the portable CWL workflow |
| LifeMonitor | Workflow Testing RO-Crate links main workflow, test suite, test instance, and compatible CI service; monitoring requires actual enrollment | A direct local WTROC upload is enrolled as workflow `cc202b33-cd3e-48cc-8004-8e8db87bd200`; its GitHub Actions suite was externally observed passing on 2026-10-18 |
| bio.tools | Curator scope requires actual bioinformatics data-processing operations and appropriate EDAM topic/operation/input/output terms | The independent FASTA/PDB processor has the maintainer-observed ID `life-science-protein-file-audit`; record existence does not establish independent API verification, curation approval or OpenEBench performance |

Evidence gates are `LOCAL_PREFLIGHT → SUBMITTED → ACCEPTED → EXTERNALLY_VERIFIED`; platform submission is a separate user-authorized action and requires a stable public record URL. Neither an identity connection nor a completed local preflight is accepted registration, and external adoption requires separately sourced use evidence.

References: [Workflow RO-Crate 1.1](https://about.workflowhub.eu/Workflow-RO-Crate/1.1/), [WorkflowHub metadata submission](https://about.workflowhub.eu/docs/registering_workflows/complete-workflow-metadata/), [LifeMonitor test monitoring](https://lifemonitor.eu/lm_test_monitoring), [LifeMonitor WTROC guide](https://lifemonitor.eu/making_a_wtroc), [bio.tools curator guide](https://biotools.readthedocs.io/en/latest/curators_guide.html).

## Portable CWL package

```sh
python .github/scripts/build_portable_workflow_crate.py build/life-science-portable.cwl.crate.zip
```

The portable archive declares CWL as its main workflow, includes synthetic replay fixtures, and excludes accepted production `data/` and private information. GitHub Actions remains the native owner of live observations and guarded persistence. The WTROC uses LifeMonitor's documented `GithubService`, `https://api.github.com` instance URL and repository workflow resource form. A direct local upload was externally observed with a passing monitored suite on 2026-10-18. WorkflowHub 2347.1 is a separate external record; the failed registry-import attempt and successful local upload must not be presented as automatic synchronization.

## Third independently callable Bio Tool

`ls-bio protein-fasta` and `ls-bio protein-pdb` implement actual biological data processing, separately from software inspection and source-grounded knowledge generation. The repository-side `metadata/biotools-protein-audit.draft.json` preserves the metadata corresponding to the maintainer-observed record `biotools:life-science-protein-file-audit` and uses EDAM operation_2403 / operation_2406, data_2976 / data_1460 / data_2955, and format_1929 / format_1476 for the supported formats. The filename is retained to avoid needless path churn; it is a repository-side metadata source, not a claim that the registry exported or independently validated these exact bytes. EDAM assignments, record existence, curation status, API verification and external benchmark results remain distinct evidence claims.
