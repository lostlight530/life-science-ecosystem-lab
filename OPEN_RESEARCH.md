# Open Research — Life Science Ecosystem Lab

This repository publishes independently inspectable research-software assets and their supporting evidence. Open research here means that scope, inputs, methods, provenance, limitations, failures, and software versions are made reviewable; it does not mean that every repository artifact is a scientific result or that every external source is independently verified.

## Repository scope

The repository currently distinguishes three established independently callable assets from a separately packaged experimental Framework:

- [Knowledge Workflow](.github/README.md) — source-bounded knowledge collection and state transitions
- [Evidence Tool](evidence/README.md) — repository and evidence inspection
- [Bio Tool](bio_tool/README.md) — bounded processing of protein FASTA/PDB files
- [Experimental Framework](framework/README.md) — cross-domain software-contract and lineage assessment, not biological interpretation

The Framework is not a fourth established research asset. External Agents and human contributors are collaborators, not runtime dependencies or automatic authorities.

## Research and evidence principles

1. State a falsifiable question, the intended scope, and explicit non-goals before interpreting an output.
2. Identify sources by stable public URI, issuer, version or revision, publication/update date, and observation time where available.
3. Record the exact repository commit, environment, dependencies, commands, inputs or fixture identities, and observed outputs when reproducibility depends on software execution.
4. Preserve negative controls, failures, exclusions, missing data, uncertainty, and unresolved conflicts alongside positive observations.
5. Separate software correctness, evidence integrity, method suitability, and scientific evaluation. Passing tests or schema checks do not establish biological truth, clinical utility, or institutional approval.
6. Distinguish synthetic fixtures, local execution, live external effects, and independently verified observations; do not promote one evidence class into another.

## Public collaboration

Use [CONTRIBUTING.md](CONTRIBUTING.md), the repository [issue forms](.github/ISSUE_TEMPLATE/), and pull requests for bounded, reviewable changes. Proposals should identify the affected asset, observable behavior, source basis, verification performed, and remaining limitations.

Only publish material that is appropriate for a public repository. Do not submit patient or participant data, personal or health information, credentials, private URLs, unpublished source documents, internal research plans, or access-controlled records to issues, pull requests, workflows, or CI artifacts. Follow [SECURITY.md](SECURITY.md) for sensitive disclosures.

## Reproducibility and publication identity

Use [RELEASE_POLICY.md](RELEASE_POLICY.md) together with [CITATION.cff](CITATION.cff). The current citation metadata intentionally identifies the three-asset v0.4.0 baseline, while the repository-level v0.5.0 archive also includes the separately packaged experimental Framework. These are different citation scopes and version records; do not silently substitute one for the other.

Start a new bounded research record from [RESEARCH_TEMPLATE.md](RESEARCH_TEMPLATE.md). Use the [documentation index](docs/README.md), [research methodology](docs/RESEARCH_METHODOLOGY.md), [provenance guide](docs/PROVENANCE.md), and [verification guide](docs/VERIFYING_RESULTS.md) for the detailed repository-native contracts.

## Non-claims

Open publication, repository presence, a DOI, a valid schema, a passing test, an accepted pull request, or a successful workflow run does not by itself establish independent scientific reproduction, clinical safety, biological validity, full standards conformance, external registry acceptance, or publisher approval.
