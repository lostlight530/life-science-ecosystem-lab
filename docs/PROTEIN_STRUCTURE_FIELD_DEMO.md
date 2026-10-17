# Protein structure prediction · Real external-Agent, Tool and Workflow field demo

**Date:** 2026-10-17 · **Authority:** read-only live research and isolated lifecycle demonstration, never direct production `data/` modification

## Scope and software authority

This field case uses the existing optional Agent protocol (`AGENTS.md`, `.github/agent-handoff/SOP.md`), independent `ls-evidence` CLI, native `ls-knowledge` source/topic transforms, JSONL graph + FTS5 search, portable synthetic CWL and an isolated copy of accepted Git-tracked state. The Agent handoff is `PROPOSAL_ONLY`; it never self-approves an observation or invokes production persistence.

The protein prediction question here is **3D structure prediction**, not general protein property prediction, folding accuracy certification, or variant-fitness prediction. ProteinGym remains a separate `protein-variant-effects` topic.

## The six actually checked public GitHub sources

| Repository | Role | Reuse boundary |
| --- | --- | --- |
| [AlphaFold 2](https://github.com/google-deepmind/alphafold) | Published structure prediction code | Code license is distinct from pretrained model parameters and benchmark datasets |
| [OpenFold](https://github.com/aqlaboratory/openfold) | Trainable structure model and example FASTA/PDB | Small examples are not the full training dataset |
| [ProteinNet](https://github.com/aqlaboratory/proteinnet) | CASP-based training/validation/test dataset description and links | README is not the full ProteinNet data corpus |
| [CASP15](https://github.com/Bhattacharya-Lab/CASP15) | Historical predicted PDBs and published benchmark summaries | No independent GDT-TS/TM-score recalculation in this demo |
| [AlphaFold 3](https://github.com/google-deepmind/alphafold3) | Source code and a small example inference-input JSON | Model weights/outputs carry additional use terms; none downloaded |
| [ProteinGym Base](https://github.com/ProteinGym/proteingym-base) | Variant-effect dataset infrastructure and sequence/structure examples | This is not direct 3D structure prediction accuracy |

Source and topic files: [`sources.json`](../evidence/profiles/research/protein_structure/sources.json), [`topics.json`](../evidence/profiles/research/protein_structure/topics.json). These scoped profiles use the same native collection and keyword matching code, but **do not alter the weekly production source and topic registries**. All six source refs are immutable Commit SHAs.

## Seven individual GitHub data samples

See [`sample-manifest.json`](../evidence/profiles/research/protein_structure/sample-manifest.json). The read-only sample checker fetches pinned Git commit trees and blob objects via GitHub API, confirms the path, blob SHA-1, declared size and SHA-256, then validates bounded FASTA sequences, PDB atomic coordinates or AlphaFold 3 protein input JSON. It records **metadata only**. Samples include OpenFold FASTA + PDB, CASP15 AlphaFold2 + ESMFold predictions, AlphaFold3 ubiquitin JSON and ProteinGym FASTA + computational PDB.

**An accessible GitHub example is not equivalent to a downloaded complete dataset.** This case does not run AlphaFold, OpenFold or ESMFold, train a model, validate experimental ground truth, use a GPU, or score structural prediction quality.

## Verified real-world execution and permanent evidence index

- Actual successful read-only Actions run: [#38997600043](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/38997600043)
- GitHub Artifact ID: `12087234359`, SHA-256: `f557f2a58cf6231d61bdb3414f7471372016e9eedbd549b30be0dee2959c8463` (independently checked against ZIP bytes)
- [Bounded, Git-tracked field observation index](../evidence/field-tests/2026-10-17-protein-structure-demo.json) records source run, Merkle-like evidence digests, graph counts, 7 audited sample identities, 5 discovery-only candidates, isolated two-event ledger and the no-change replay
- Real external software findings: OpenFold 2 PASS / 2 WARN; ProteinNet 1 PASS / 3 WARN, neither is a scientific or standards certification
- Core source evidence: 6 pinned GitHub repositories, 10 records, 0 diagnostics, four topic coverages, 12 graph nodes and 21 `SOURCE_MATCH` edges

The short-retention Artifact includes original bounded JSON/Markdown/SARIF reports; the tracked index is durable but is **not** an archived full source corpus and does not contain raw protein samples. To independently verify the ZIP digest, download the specific GitHub Artifact and compute SHA-256 locally.

## Repeat the full demonstration

[GitHub Actions: Protein Structure External Agent and Native Workflow Demo](https://github.com/lostlight530/life-science-ecosystem-lab/actions/workflows/protein-structure-agent-demo.yml) runs on the dedicated experiment branch (push) or by manual dispatch. Its `contents: read` permission prevents publishing accepted production changes. Steps:

1. Regress both assets and validate the external Agent proposal shape, frozen protein-source registry and four native topic IDs
2. Run advisory live discovery without registering any returned candidates
3. Collect, aggregate and independently validate real GitHub blobs; produce source-cited knowledge, JSONL graph, graph check and live FTS5 query
4. Verify seven real pinned examples from GitHub objects, inspect fixed OpenFold and ProteinNet checkouts with the independent Tool, and emit JSON/Markdown/SARIF
5. Replay portable CWL with **synthetic** frozen fixture (different from the live GitHub evidence), proving the separately executable computational interface
6. Copy accepted main `data/` to an ignored sandbox, accept protein topic evidence there, archive the older candidate and append a linked event, then reapply the unchanged candidate and require `NO_MEANINGFUL_DELTA`
7. Validate every result and upload only bounded summaries, source identities, hashes, reports and diagnostics; **exclude raw retrieved upstream source and accepted snapshots**

Success is a verified software demonstration, not an accepted production protein-research knowledge update. An explicit separately authorized native run/registry governance would be required to make this the ongoing topic.

## Evidence and distinctions

The field summary is generated by `.github/scripts/protein_structure_demo_summary.py`; it rejects missing live source results, empty search, broken event linkage or failed no-change replay. The sample auditor is `.github/scripts/protein_structure_sample_audit.py`. The external Agent handoff is [pinned proposal JSON](../.github/agent-handoff/protein-structure-2026-10-17.json), validated by `ls-evidence validate-handoff` but not auto-promoted.

The Evidence Tool reports WARN when optional metadata are missing; structural identity PASS does not certify scientific validity or third-party registration. Large ProteinNet/PSBench datasets, external restricted model parameters, licensing of individual structure files and benchmark performance must be independently assessed before future reuse.

[Agent collaboration](AGENT_COLLABORATION.md) · [Production operations](PRODUCTION_OPERATIONS.md) · [Verification limits](VERIFYING_RESULTS.md)
