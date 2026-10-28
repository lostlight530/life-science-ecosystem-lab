# Independent LS Framework: software engineering assurance matrix

Status: project-owned experimental contract, not a registered institutional standard or scientific truth engine

## Scope and tested evidence

`framework/` is an independently installed peer of Knowledge Workflow, Evidence Tool and Bio Tool. Cross-domain means shared **life-sciences research software engineering interfaces**, not universal scientific inference, a new Tool or real omics integration. The genomics/microscopy fixture and [Contract Challenge 001](CONTRACT_CHALLENGE.md) are synthetic software contracts.

| Question | Supported check | Unverified boundary |
| --- | --- | --- |
| Software envelope | Bounded JSON shape, allowed IDs and domain strings | Independent community-schema certification |
| Digital identity | SHA-256 of available local bytes within the selected input root | Actual biological specimen identity and upstream source authenticity |
| Software relationships | Known references, no cycles/duplicate producers, multi-asset lineage; declared cross-domain step count uses the union of input **and** output asset domains | Genuine biological or causal relationship, or executed integration |
| Method declarations | Version/digest shape and declared input/output domains | Execution attestation, algorithm correctness or method suitability |
| Uncertainty | Typed PASS/FAIL/INDETERMINATE with proposal-only scientific claims | Reviewed scientific truth and external registration |
| Replay | Deterministic report and Linux/Windows byte-oriented tests | Experimental replication or valid cross-domain biological inference |

## Consumer safety

`PASS` is a **software-contract** conclusion only. `FAIL` records a concrete violation. `INDETERMINATE` is correct abstention, neither proof of failure nor proof of scientific truth. A valid scientific negative finding must remain distinct from a missing experiment.

`ls-framework assess` exits 0 for a completed PASS or INDETERMINATE report by default. `--require-pass` instead returns 2 for INDETERMINATE (1 for FAIL). Both the assessment CLI and standalone synthetic challenge share a report-path guard that discovers Git roots from relevant ancestor paths and refuses output into the input root, repository `data/`, or `.git/`, including from checkout subdirectories. Non-finite/deeply nested JSON and output-write failures produce structured failures. Reports are written via a temporary sibling file and same-filesystem replacement, so a failed replacement should leave the previously complete report intact. This does not attest storage durability after power loss or prevent concurrent writers. This guard is not a general filesystem sandbox and does not eliminate concurrent filesystem races. Use `build/` and inspect command-specific JSON status fields.

## Pending falsifiable research, not yet demonstrated

Freeze independently annotated software-artifact cases from at least two life-sciences domains, versions, mutation operators, baseline checks and acceptance criteria before measuring validity. Compare schema-only validation, appropriate independent domain software checkers and this Framework. Report contract-violation detection, false rejects, abstention correctness and replay disagreement, including negative results. Existing synthetic challenge success is not a scientific benchmark or cross-omics finding.

## External references only

- [FAIR4RS RDA principles](https://doi.org/10.15497/RDA00068): distinguish component and software version identities
- [W3C PROV-O](https://www.w3.org/TR/prov-o/): entity/activity/agent provenance
- [RO-Crate 1.3](https://www.researchobject.org/ro-crate/specification/1.3/index.html): current generic crate specification, not the pinned Workflow RO-Crate 1.1
- [ISA Model](https://isa-specs.readthedocs.io/en/latest/isamodel.html): investigation/study/assay description
- [FORCE11 software citation](https://github.com/force11/force11-sciwg/blob/master/guidance/software_citation_checklist_for_developers.md): precise version attribution

These organizations have not certified the project-owned JSON contract. Research lifecycle remains DEFINE → PIN → QUALIFY → EXECUTE → EVALUATE → AUDIT → REVIEW → REPLAY. Framework output cannot accept native production `data/`, confer Agent identity or authorize a scientific claim.
