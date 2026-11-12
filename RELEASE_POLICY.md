# Release and Archival Policy

This repository distinguishes the evolving `main` branch, the exact repository archive, and the citation target for the three established independently callable research-software assets. These objects overlap, but they are not interchangeable.

## Repository archive — v0.5.0 (2026-10-31)

The repository-level `v0.5.0` release is an immutable snapshot containing:

- the three established assets: Life Science Knowledge Workflow, Life Science Evidence Tool, and Protein File Audit;
- the separately packaged experimental Life Sciences Cross-Domain Software Engineering Framework `0.1.0`;
- the associated evidence replay, provenance, and reproducibility controls described by the release record.

Exact archive identity:

- GitHub Release: [v0.5.0](https://github.com/lostlight530/life-science-ecosystem-lab/releases/tag/v0.5.0)
- GitHub release published: `2026-10-31T15:55:03Z`
- Tagged source commit: [`3afea285b3660f9482c935c13160705eecfb332a`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/3afea285b3660f9482c935c13160705eecfb332a)
- Zenodo version record: [10.5281/zenodo.23839899](https://doi.org/10.5281/zenodo.23839899)
- Zenodo concept DOI (all repository versions): [10.5281/zenodo.23447088](https://doi.org/10.5281/zenodo.23447088)
- Zenodo record created: `2026-10-31T15:55:08Z`

The Zenodo version record identifies the GitHub tag `v0.5.0` as its source reference. Cite the version DOI when referring to this exact repository snapshot; use the concept DOI when referring to the repository software family across versions.

## Separate citation target — v0.4.0 three-asset baseline

The current `CITATION.cff` deliberately identifies the earlier `0.4.0` baseline for the three established callable assets:

- Citation version: `0.4.0`
- Date released: `2026-10-18`
- Exact version DOI: [10.5281/zenodo.23447089](https://doi.org/10.5281/zenodo.23447089)
- Concept DOI: [10.5281/zenodo.23447088](https://doi.org/10.5281/zenodo.23447088)

Do not silently replace this citation target with the repository-level `v0.5.0` archive. The latter adds a separately packaged experimental Framework and has a different exact-version DOI. When a result depends on the three-asset v0.4.0 baseline, cite its version DOI; when a result depends on the broader v0.5.0 repository snapshot, cite the v0.5.0 version DOI.

The existing `codemeta.json` package metadata version `0.4.0` is also preserved by this policy update. It is not silently promoted to `0.5.0` merely because a repository-level archive exists; its intended package/component scope must remain explicit.

## Current main and historical preservation

- `main` is the evolving repository state, not an immutable release.
- The `v0.5.0` tag and its Zenodo version DOI identify only the snapshot at the recorded commit.
- Later changes to `main` are not part of the archived `v0.5.0` record.
- Do not move or rewrite the tag or alter the published archive to represent later changes.
- Publish a new reviewed release and a new version DOI only when a new repository snapshot is intentionally archived.
- The experimental Framework remains a software-engineering assurance tool; its presence in the archive does not establish biological validity, clinical utility, or scientific validation.

## Citation and reuse

- Use `CITATION.cff` for the declared three-asset v0.4.0 citation target.
- Use the v0.5.0 version DOI for the exact repository archive described above.
- Use the concept DOI for the repository family across versions.
- Record the exact Git tag/commit, environment, inputs, commands, and observed outcomes when reproducing a result.
- Preserve the distinction between software tests, workflow execution, registry presence, external review, and scientific validation.
