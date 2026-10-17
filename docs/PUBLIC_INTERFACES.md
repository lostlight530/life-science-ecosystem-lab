# Public software interfaces

[First-use commands](GETTING_STARTED.md) · [Result interpretation](VERIFYING_RESULTS.md) · [Documentation index](README.md)

The repository publishes three peer software assets under one source-code and release identity.
All three are usable by researchers and ordinary programs. None depends on a configured model, a prompt package, or an external Agent.

## Knowledge Workflow (`.github/`)

- Production scheduler: `.github/workflows/life-science-knowledge.yml` (GitHub Actions)
- Portable computational part: `.github/knowledge/main.cwl` (CWL 1.2)
- CLI: `ls-knowledge` (or `python -m life_science_ecosystem_lab`)
- Inputs: approved GitHub source registry, topic registry, verified evidence candidate
- Outputs: source-cited knowledge JSON, JSONL graph projection, bounded graph-search responses, reproducible receipts
- Durable authority: repository `data/` and accepted Git history, **not** a transient SQLite index
- Accepted receipt identity: `snapshot_id` identifies content; `execution_id` identifies the actual GitHub/local attempt; `change_kind` describes what changed. Use `ls-knowledge state verify --repository-root . --require-accepted` for a production acceptance claim

Commands:

```sh
ls-knowledge graph project --knowledge build/knowledge.json --output-dir build/graph
ls-knowledge graph verify --dir build/graph --knowledge build/knowledge.json
ls-knowledge graph search --dir build/graph --query monitoring --limit 10 --hops 1
```

The graph projection currently represents directly traceable `SOURCE_MATCH` links between research topics and fixed-commit source documents. It must not be presented as inferred biological or causal knowledge. The FTS5 search index is built locally on demand and is not a network service or privileged database.

## Research Software Evidence Tool (`evidence/`)

- Package and CLI: `evidence` / `ls-evidence`, independently installed using this repository's `pyproject.toml`
- Existing capabilities: approved GitHub source collection, deterministic aggregation, verification, read-only topic discovery and documentation link audits
- External-object interface: `ls-evidence inspect --root <local-repository> --output <report.json> [--markdown report.md] [--sarif report.sarif]`
- Inputs: local research software repository folder (no code is executed); optional standards descriptors within it
- Outputs: machine-readable JSON, human-readable Markdown and SARIF 2.1.0 findings
- Validation boundary: structural static preflight of local references and metadata. External registration, scientific claims, execution reproducibility and full standard conformance remain explicitly unverified

The Tool never writes into the inspected research repository. It only writes the caller-specified report paths. Its checks are useful for Life Science workflows and other research software, but eligibility for bio.tools is **not** claimed.

## Independent Protein Bio Tool (`bio_tool/`)

- Package and CLI: `bio_tool` / `ls-bio`; separate command from `ls-evidence` and `ls-knowledge`
- Inputs: bounded protein FASTA and first-model PDB coordinate files, caller-supplied local paths
- Operations: residue composition and uncertain code summaries; per-chain observed C-alpha residue inventory
- Outputs: deterministic JSON quality reports with input SHA-256, explicit status and scientific limits
- Portable adapters: `.github/bio/protein-fasta.cwl` and `.github/bio/protein-pdb.cwl`
- Registry proposal: `metadata/biotools-protein-audit.draft.json`, using real EDAM concepts; no external accession claimed
- No inference, folding model, molecular geometry validation, full sequence alignment or external upload; see [Bio Tool](../bio_tool/README.md)

## Composition

The Knowledge Workflow may call Evidence as an external command, and independent researchers or CWL tools can call Bio Tool on supplied protein files. Evidence can inspect an unrelated repository without importing the knowledge runtime or relying on its scheduler. All three exchange explicit CLI/file contracts, with their own CI and documentation.

External researchers and Agents may use human- or machine-readable outputs independently. They are not an internal runtime stage and cannot promote findings to accepted knowledge without repository governance and independent verification.