# Life Sciences Cross-Domain Research Software Engineering Framework

**Experimental independent software-engineering framework · v0.1.0**

This is the repository-root `framework/` peer, not part of `evidence/`, `bio_tool/`, or the native Knowledge Workflow runtime

**Scope:** life-sciences software interoperability, not biological inference, laboratory sample verification, scientific certification, clinical advice, or a universal science framework

## Independent installation

Python 3.11+, with no runtime dependencies, no LLM, no network and no upstream tools

```sh
python -m pip install --no-deps -e ./framework
python -m unittest discover -s framework/tests -v
ls-framework assess --bundle framework/fixtures/software-cross-domain.json --root framework/fixtures --output build/framework/assessment.json --require-pass
```

The synthetic fixture declares a genomics input, microscopy input, and integration artifact, then checks their **local file digests**, domain declarations, method identities, lineage and path boundaries

The repository pins text checkout to LF through root `.gitattributes` and runs this contract on Linux and Windows. This is required because fixture SHA-256 values identify exact bytes, not text after platform-specific newline conversion

It does **not** perform a genomic/imaging analysis, authenticate any scientific sample, attest the execution of the declared method, or establish biological truth

## Input contract

One bounded JSON bundle contains exactly kind, schema_version, scope, assets, steps and claims

- Assets require stable id, reviewed life-science domain, kind, declared SHA-256, source id/version and optional path
- Local paths must stay inside the explicit input root and the bytes must match the SHA-256
- An asset with no local path is a **source declaration**, not independently verified data
- A step declares a method identifier/version/digest, inputs, outputs, supported domains and stated execution outcome
- A bundle with multiple assets requires at least one explicit lineage step; otherwise it fails with `MISSING_LINEAGE_STEPS`
- Step identities, reported success and method digests are **declarations**, not independent execution attestation
- A scientific claim may be represented only as `PROPOSAL_ONLY`, never accepted by the framework

## Output contract

- `PASS`: software-contract structure and accessible local byte checks passed, without claims or warnings
- `FAIL`: malformed, unsafe or contradictory software contract, or failed local-byte verification
- `INDETERMINATE`: unverifiable external declarations, unfinished/failed steps, or proposed scientific claims

The report preserves canonical input digest, typed findings, bounded metrics and explicit nonclaims
`PASS` is never scientific validity, verified method execution or authority to write `data/`

## Governance

This proposed fourth independent *framework* entity is additive to the existing three assets and does not create a fourth Tool
Framework contracts can be consumed by other software, but it cannot promote a proposal to approved sources, production data, third-party registration or scientific fact

The Framework is not included in the repository's frozen `v0.4.0` Zenodo release or WorkflowHub Knowledge Workflow record. A future Framework release or registration would require a separate reviewed version and evidence record

See [the independent ADR](../docs/ADR-INDEPENDENT-LS-FRAMEWORK.md) and independent `.github/workflows/life-science-framework.yml`

## CI consumers, evidence safety and abstention

The default command returns exit code 0 for a well-formed `PASS` **or** `INDETERMINATE` report, 1 for `FAIL`. With `--require-pass`, an `INDETERMINATE` report exits 2 to keep incomplete evidence from being misread as affirmative verification. Always inspect the JSON status; even `PASS` does not attest method execution or scientific correctness.

The `--output` destination cannot resolve to the input bundle, any location inside the declared input root, or the checkout's `data/` or `.git/` when invoked from the repository root. Store reports under ignored `build/` or a dedicated scratch folder. This guard is **not a general OS filesystem sandbox**: user-controlled output paths elsewhere can replace existing files.

Read the [assurance model and falsification matrix](docs/ASSURANCE.md), including explicit limits of synthetic cross-domain fixtures and standards references.
