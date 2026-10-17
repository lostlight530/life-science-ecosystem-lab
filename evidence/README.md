# Life Science Evidence Tool

[Start here](../docs/GETTING_STARTED.md) · [Tool output and status](../docs/VERIFYING_RESULTS.md) · [Public API](../docs/PUBLIC_INTERFACES.md)

Independent and reusable tool for GitHub-source provenance, change detection, documentation maintenance and reproducible verification

The tool shares a repository with the [knowledge workflow](../.github/README.md) but **does not rely on the workflow scheduler for its own validation**. Its code is in this directory, its root package is `evidence`, and its console entry point is `ls-evidence`

## Standalone CLI

```sh
python -m pip install -e .
ls-evidence discover --topic bioinformatics-workflow --output build/discovery.json
ls-evidence audit-docs --root . --files evidence/profiles/docs.json --output build/docs-audit.json
ls-evidence collect --sources evidence/profiles/sources.json --output build/records.json
ls-evidence aggregate --input build/records.json --topics evidence/profiles/topics.json --output build/candidate.json
ls-evidence validate --bundle build/candidate.json
```

`discover` is **advisory only**: returned projects are unapproved and must be reviewed and placed in the versioned source registry before harvesting. The normal collector never searches the internet for undocumented new sources

`audit-docs` verifies a pinned inventory of local Markdown references and preserves a machine-readable report. It inventories external links but **does not mark them reachable**; remote content and external registry records need separate live verification. No issue, PR, workflow, release or registry is edited by the tool

Source records carry approved repository, commit, tree, blob, path, normalized SHA-256, trust, selection rule and observation time. Aggregation excludes observation time from semantic identity, supports cross-repository path uniqueness and produces a verifiable evidence candidate. Failed provenance checks must block projection

### Verification boundary

- The source registry (`profiles/sources.json`) is the authority for permitted repos and documents
- GitHub topic search can propose but never automatically approve a source
- Validation is independent of the scientific meaning of the content
- The tool can write only to the specified output path, not `main`, active ledgers, registries or workflow definitions
- GitHub Actions runs the tool independently in `../.github/workflows/life-science-evidence.yml`

This is research software **about** workflow evidence, not a biological analysis tool or claim of bio.tools eligibility

## Optional external Agent research proposal

`ls-evidence validate-handoff --input .github/agent-handoff/example-handoff.json --topics evidence/profiles/topics.json` checks the bounded, proposal-only research handoff envelope without importing an Agent framework, searching the web, certifying claims or granting access to accepted `data/`. `AGENT_HANDOFF_SHAPE_VALID_PROPOSAL_ONLY` means format and permission boundaries were checked, **not** that its cited research is accepted. See [Agent collaboration](../docs/AGENT_COLLABORATION.md).

## Independent research software inspection

Inspect a local third-party research software project **without** scheduling the knowledge Workflow or executing third-party code:

```sh
ls-evidence inspect --root /path/to/research-software --output build/report.json --markdown build/report.md --sarif build/report.sarif
```

This checks local README/citation availability, RO-Crate main-entity links and basic Bioschemas JSON-LD identities when present. It records missing optional metadata as warnings and deliberately does **not** certify bio.tools eligibility, external registrations, scientific truth or workflow execution. It leaves the inspected project untouched. See [public interfaces](../docs/PUBLIC_INTERFACES.md).

## Degraded source observations

The collector can emit optional-source diagnostics with `--diagnostics-output`; pass these to `aggregate --diagnostics`. A source-unavailable diagnostic remains machine-readable, and the candidate becomes `projection_eligible=false`: partial observations are not accepted into the durable corpus automatically.

## Offline cross-version quality and interoperability checks

```sh
ls-evidence audit-knowledge --knowledge data/knowledge/current.json --output build/quality.json
ls-evidence audit-knowledge --knowledge build/new-knowledge.json --previous data/knowledge/current.json --labels build/review-labels.json --output build/version-quality.json
ls-evidence audit-ecosystem --root . --output build/interop.json
```

`audit-knowledge` validates a bounded knowledge-map envelope, content digest, citation identity, graph projection and coverage counts. With `--previous` it records additions, removals, content changes, source-revision-only changes and topic coverage transitions without automatically inferring scientific novelty. Optional `--labels` accepts `{"schema_version":"1.0.0","cases":[{"topic_id":"workflow-registration","repository":"owner/repo","path":"README.md","relevant":true}]}` for a fixed, reviewer-supplied precision/recall sample; no labels means no precision/recall claim. The audit cannot independently prove upstream excerpt correctness without the complete validated candidate or scientific truth in any case. Exit code 0 means structural PASS, not scientific certification.

`audit-ecosystem` reviews local WorkflowHub RO-Crate/CWL packaging, LifeMonitor test metadata and tool/software descriptors. Its `NOT_VERIFIED` external statuses are intentional until actual registry, monitoring and third-party usage evidence exists. Its result is a local preflight, never platform certification or automatic registration.
