# Getting started

This guide is for someone who just cloned the public repository. It gives **separate starting points** for three established peer software assets and the experimental independent Framework. No model API key, Skills package, persistent database server or remote execution service is required.

## Prerequisites

Python 3.11+; a Git checkout; optional `cwltool` for the portable computational replay. Install commands assume a shell in the **repository root**. Use a Python virtual environment if you want isolation.

```sh
python -m pip install -e .
ls-evidence --help
ls-knowledge --help
ls-bio --help
```

One Python distribution intentionally supplies **three independent commands**; it is not two separately published PyPI packages.

## Path A — Evidence Tool only (offline)

Inspect any local public research-software checkout without importing or running that project's code:

```sh
ls-evidence inspect --root . --output build/inspection.json --markdown build/inspection.md --sarif build/inspection.sarif
```

The output files are local to your checkout, under ignored `build/`. For a different project, set `--root /path/to/other/repository`. The tool does **not** modify that target repository. A `WARN` report can still exit successfully; a `FAIL` report returns exit code 1. Neither constitutes scientific validity or full Bioschemas/RO-Crate conformance.

Audit this project's documented local links:

```sh
ls-evidence audit-docs --root . --files evidence/profiles/docs.json --output build/docs-audit.json
```

## Path B — Knowledge Workflow computational replay (offline data)

Install the portable CWL reference runner (one-time dependency installation may require network):

```sh
python -m pip install cwltool
mkdir -p build/replay
cwltool --no-container --outdir build/replay .github/knowledge/main.cwl .github/knowledge/test/workflow-job.yml
ls-knowledge knowledge verify --candidate build/replay/candidate.json --topics evidence/profiles/topics.json --knowledge build/replay/knowledge.json
ls-knowledge graph project --knowledge build/replay/knowledge.json --output-dir build/graph
ls-knowledge graph verify --dir build/graph --knowledge build/replay/knowledge.json
ls-knowledge graph search --dir build/graph --query workflow --limit 5 --hops 1
```

The workflow job is **synthetic** and replayable: this does not contact LifeMonitor, WorkflowHub or approved GitHub sources, and it does not update tracked `data/` state. The searchable graph currently holds evidenced topic-to-source links, not independently inferred biological facts.

## Path C — Read-only observation of approved public GitHub sources

Network access is required; a `GITHUB_TOKEN` environment variable may be provided using standard secure environment configuration to reduce public API rate-limit failures. Never commit the token. Source selection is governed by `evidence/profiles/sources.json`, not by live topic search.

```sh
ls-evidence collect --sources evidence/profiles/sources.json --output build/records.json --diagnostics-output build/source-diagnostics.json
ls-evidence aggregate --input build/records.json --topics evidence/profiles/topics.json --diagnostics build/source-diagnostics.json --output build/candidate.json
ls-evidence validate --bundle build/candidate.json
ls-knowledge knowledge build --candidate build/candidate.json --topics evidence/profiles/topics.json --output build/knowledge.json
ls-knowledge graph project --knowledge build/knowledge.json --output-dir build/live-graph
ls-knowledge graph verify --dir build/live-graph --knowledge build/knowledge.json
```

Collection can fail if GitHub is unreachable, a required repository/ref/path is unavailable, or no approved documents can be retrieved. Partial observations are **not** automatically eligible for durable persistence. These commands only create ignored local outputs. Do not infer external registration or completed production knowledge maintenance from their success.

## Path D — Bio Tool molecular file analysis (offline, independent)

The third component performs actual bioinformatics data processing on supplied files and never runs model inference.

```sh
ls-bio protein-fasta --input .github/bio/test/example.fasta --output build/bio-fasta.json
ls-bio protein-pdb --input .github/bio/test/example.pdb --output build/bio-pdb.json
```

The output contains input SHA-256, residue statistics and explicit uncertainty boundaries. Read [the Bio Tool contract](../bio_tool/README.md) before using external sequences or coordinates. The portable CWL adapters and a separate read-only pinned-source CI are in `.github/bio/` and `.github/workflows/life-science-bio.yml`.

## Path E — Experimental Framework (offline, independent)

The life-sciences software-engineering Framework is separately packaged from the three root commands. This synthetic contract experiment checks JSON software-artifact lineage and local SHA-256; it does not perform cross-omics scientific analysis:

```sh
python -m pip install --no-deps -e ./framework
python -m unittest discover -s framework/tests -v
ls-framework assess --bundle framework/fixtures/software-cross-domain.json --root framework/fixtures --output build/framework/assessment.json
```

Its `PASS` is only an engineering-contract verdict. See [Framework](../framework/README.md) and [ADR](ADR-INDEPENDENT-LS-FRAMEWORK.md)

The repository pins text files to LF bytes because the fixture SHA-256 values are byte identities. The dedicated Framework workflow runs on Linux and Windows. If an older Windows checkout predates `.gitattributes`, create a fresh checkout before diagnosing digest mismatches

## Native GitHub Actions and persistence

- [Knowledge lifecycle](../.github/workflows/life-science-knowledge.yml): scheduled weekly on Mondays at 03:23 UTC using the `native` profile; manual dispatch can select the reviewed `native` or isolated `protein_structure` profile
- Explicit manual `profile=native` plus `persist=true` on `main`, and eligible scheduled native runs, may write only to `data/` after all verification, write-boundary and remote-head guards. Isolated profiles are artifact-only even if a caller requests persistence
- [Independent Tool CI](../.github/workflows/life-science-evidence.yml) checks the Evidence Tool; [integration CI](../.github/workflows/validate.yml) checks CWL, graph, contracts, crate and documentation

Before treating a run as successful durable knowledge, inspect its actual run event, conclusion, persisted commit and artifacts; see [Understanding Verification](VERIFYING_RESULTS.md).

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `ls-knowledge`, `ls-evidence` or `ls-bio` not found | Run `python -m pip install -e .` in your active Python environment |
| `cwltool` not found | Install the optional `cwltool` reference runner |
| GitHub collect fails | Network, source registry, source ref/path and API rate limit |
| `projection_eligible=false` | Inspect source diagnostics; do not treat missing documents as verified deletions |
| No `data/knowledge/current.json` | A real, accepted native lifecycle run has not yet persisted it |
| FTS5 unavailable | Your Python SQLite build must include SQLite FTS5 support |
| Inspection reports `WARN` | Review the missing/optional evidence; it is not equivalent to an error or proof |
| Framework fixture digest mismatch on Windows | Confirm the checkout includes root `.gitattributes`; use a fresh checkout so the LF byte contract is applied |

[Documentation index](README.md) · [Public Interfaces](PUBLIC_INTERFACES.md) · [Scope](SCOPE.md)
