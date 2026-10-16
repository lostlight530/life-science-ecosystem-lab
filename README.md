# Life Science Ecosystem Lab

**Two independently testable research-software assets: a knowledge-first computational workflow and an evidence-verification tool**

1. **Source-Grounded Life Science Workflow Knowledge Cartography** — a CWL v1.2 computational workflow that creates a source-cited knowledge map covering research workflow registration, monitoring and testing, and reproducible metadata; it carries explicit gaps when the evidence is absent or only one source agrees
2. **Life Science GitHub Evidence Aggregator** — a Python CLI that reads only approved GitHub repositories, captures exact source commits/tree/blob identities, normalizes selected documentation, classifies observable changes and verifies stable candidate digests

The first asset is the research product; the second is the reproducibility and evidence boundary. Deterministic keyword matching and extracts are **not** semantic/biological inference

## Run the knowledge workflow

Python 3.11+ with no mandatory third-party **runtime** dependencies; the CWL workflow itself uses the `cwltool` reference runner:

```sh
python -m pip install cwltool
cwltool --no-container workflow/main.cwl test/workflow-job.yml
```

See [the workflow guide](workflow/README.md) for offline/online replay, exact outputs and evidence limitations

## Run the standalone verification tool

```sh
export PYTHONPATH=src
python -m life_science_ecosystem_lab validate-source-registry profiles/sources.json
python -m life_science_ecosystem_lab validate-topic-registry profiles/topics.json
python -m life_science_ecosystem_lab evidence collect --sources profiles/sources.json --output build/records.json
python -m life_science_ecosystem_lab evidence aggregate --input build/records.json --topics profiles/topics.json --output build/candidate.json
python -m life_science_ecosystem_lab evidence validate --bundle build/candidate.json
python -m life_science_ecosystem_lab knowledge build --candidate build/candidate.json --topics profiles/topics.json --output build/knowledge.json
python -m life_science_ecosystem_lab knowledge verify --candidate build/candidate.json --topics profiles/topics.json --knowledge build/knowledge.json
python -m unittest discover -s tests -v
```

This repository was created October 16, 2026, carrying forward the February 15–16 Jules workflow origin. It has an MIT license, `CITATION.cff`, Workflow RO-Crate and Workflow Testing RO-Crate metadata, an offline CWL job, regression tests, and CI. `scripts/build_rocrate.py` packages the described workflow for external inspection

## Safety and claim boundary

- GitHub is the **only** approved online source type. New repositories found by topic search are discovery candidates, not automatically approved sources
- Weekly GitHub Actions runs generate and upload knowledge **read-only**; manual `persist=true` additionally requires strict main-branch head and data-only write guards
- LifeMonitor all-branches/all-tags/issue-check defaults remain untouched: **no** repository-specific `lifemonitor.yaml` override
- No biological interpretation, clinical validity, live registry publishing, WorkflowHub registration, LifeMonitor monitoring confirmation, or full standards certification is asserted

See [Scope](docs/SCOPE.md), [Provenance](docs/PROVENANCE.md), and [Design](docs/superpowers/specs/2026-10-16-rs12-two-asset-lifecycle-design.md)
