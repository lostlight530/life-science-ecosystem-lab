# Life Science Evidence Tool

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
