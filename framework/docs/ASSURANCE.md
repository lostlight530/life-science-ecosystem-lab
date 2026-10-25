# Framework assurance model — independent life-sciences software engineering

Status: project-owned experimental software assurance description, not an official institutional specification or a scientific truth verifier

## Focus and object model

The Framework is an independent peer to Knowledge Workflow, Evidence Tool and Bio Tool. Its cross-domain scope refers to software engineering across heterogeneous **life-sciences** research systems. It does not aggregate all scientific disciplines, create another Tool, execute biology algorithms or claim that synthetic genomics/imaging fixtures represent actual biological measurements.

## Version 0.1.0 assurance matrix

| Software question | What is checked | What is not checked |
| --- | --- | --- |
| Is the research-software envelope well-formed? | Bounded JSON shape, identifiers and allowed declared domain categories | Official ISA/PROV-O/RO-Crate conformance or unrestricted life-science coverage |
| Are file bytes exactly the declared local bytes? | SHA-256 and input-root containment for supplied local paths | Correct laboratory specimen or origin authenticity |
| Do software-artifact links form a valid graph? | Missing asset references, cycles, duplicate producers and empty multi-asset lineage | Whether a causal, analytical or biological relation is real |
| Do method declarations cover stated domains? | Declared method IDs, version/digest shapes, allowed domain sets | Whether the method exists, ran, is suitable or was correctly implemented |
| Can uncertainty and negative execution be reported? | Contract FAIL and incomplete-evidence INDETERMINATE; proposal-only scientific claims | Independent experimental review, institutional certification or authorization |
| Can assessment replay? | Canonical input digest, deterministic output, Linux/Windows pinned bytes | Cross-laboratory reproducibility or scientific replication |

## Engineering evidence levels and authority

1. Available local bytes and contract structure can be tested independently by the Framework
2. Method ID, success outcome, reference source and claimed software lineage are **declarations**, not witnessed events
3. Biological sample identity, scientific model validity, assay suitability, statistical inference and causal claims require separate domain evidence
4. Production acceptance, registry certification, peer review and institution endorsement are outside the Framework's authority

PASS is limited to supported engineering checks and cannot be laundered into scientific truth. INDETERMINATE is a valid refusal to overclaim, not proof of false science. A negative experimental result and a missing experiment must never be silently merged.

## Safe invocation and machine consumers

Install `./framework` independently and use the frozen fixture; no Agent, network or GitHub Actions runtime is required. The CLI prints its JSON report in all ordinary outcomes; optional `--output` must not point into input-root data or the checkout's accepted `data/` and `.git/` directories. Other user-specified output paths are not an OS sandbox, and may replace an existing file, so use dedicated `build/` scratch paths.

`ls-framework assess` returns 0 for both PASS and INDETERMINATE by default, and 1 for FAIL. With `--require-pass`, INDETERMINATE returns 2. Consumers must always inspect the JSON status and `not_verified` fields.

## Falsifiable next experiment — NOT YET EXECUTED

Freeze independent real-world software-artifact cases from at least two different life-science domains, versioned references, annotation rules, intended failure mutations, analysis criteria, and separate baseline checks **before** producing detection metrics. Compare (A) JSON Schema-only validation, (B) selected external domain tools and (C) Framework contracts. Track detection, false rejection, abstention fidelity, bytewise cross-platform replay, and unsupported cases. Preserve failures and negative results; never claim improved sensitivity without an independently labelled test corpus.

Current synthetic genomics/microscopy fixtures test **declared software contract composition only**; they are not real omics integration, ground-truth biological validation, or external adoption.

## External references versus our custom contracts

- [FAIR4RS, RDA recommendation](https://doi.org/10.15497/RDA00068): distinct component and version identities
- [W3C PROV-O](https://www.w3.org/TR/prov-o/): standardized provenance entity/activity/agent concepts
- [RO-Crate 1.3](https://www.researchobject.org/ro-crate/specification/1.3/index.html): current generic community research-object packaging, independently versioned from this repository's reviewed Workflow RO-Crate 1.1
- [ISA investigation/study/assay model](https://isa-specs.readthedocs.io/en/latest/isamodel.html): experiment description concepts
- [FORCE11 software citation guidance](https://github.com/force11/force11-sciwg/blob/master/guidance/software_citation_checklist_for_developers.md): citation provenance and exact versions

None of these standards has certified this Framework; names and hyperlinks identify references, not implementation or adoption claims.

## Fixed method and governance

DEFINE → PIN → QUALIFY → EXECUTE → EVALUATE → AUDIT → REVIEW → REPLAY remains the research lifecycle, with distinct software validation, evidence validity, method applicability and scientific claims. The released three-asset v0.4.0 DOI and the later experimental Framework v0.1.0 remain separate versioned software identities.
