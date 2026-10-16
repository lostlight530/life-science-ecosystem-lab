# Source-Grounded Life Science Workflow Knowledge Cartography

**Primary research artifact:** `knowledge.json` — a deterministic, source-cited map of what approved GitHub documentation actually states about life-science workflow registration, monitoring/testing, and reproducible research-object metadata

**Separate assurance asset:** the GitHub Evidence Aggregator processes immutable source snapshots and verifies the candidate bundle before knowledge extraction; it never claims scientific truth or overwrites active knowledge on its own

## Reproducible computational workflow (CWL v1.2)

```sh
python -m pip install cwltool
cwltool --no-container workflow/main.cwl test/workflow-job.yml
```

Four observable steps run in order: `aggregate` → `validate` → `knowledge` → `verify_knowledge`

Inputs are `records` (GitHub snapshots with commit and blob identities), `topics` (reviewed research taxonomy), and `python_package` (`src/`). Outputs include the verifiable `knowledge.json`, candidate evidence, and both validation reports. All output identities are deterministic for unchanged content and profiles

The committed `test/workflow-job.yml` is **synthetic**, allowing fully offline reproducibility and regression testing. Its dummy Git SHAs demonstrate the data contract, not a real observation; the actual source adapter is tested independently. To work with verified current GitHub sources, first run:

```sh
PYTHONPATH=src python -m life_science_ecosystem_lab evidence collect --sources profiles/sources.json --output build/records.json
PYTHONPATH=src python -m life_science_ecosystem_lab evidence aggregate --input build/records.json --topics profiles/topics.json --output build/candidate.json
PYTHONPATH=src python -m life_science_ecosystem_lab knowledge build --candidate build/candidate.json --topics profiles/topics.json --output build/knowledge.json
PYTHONPATH=src python -m life_science_ecosystem_lab knowledge verify --candidate build/candidate.json --topics profiles/topics.json --knowledge build/knowledge.json
```

The GitHub Actions **Build Workflow Knowledge and Validate Evidence** workflow carries out this live observation read-only and uploads results as Actions artifacts. Persistence requires manual `workflow_dispatch` with `persist=true` and a successful branch-head world-line check

`ro-crate-metadata.json` documents the main workflow, four CWL steps, Bioschemas FormalParameter inputs/outputs, testing suite and GitHub Actions test resource. `python scripts/build_rocrate.py build/life-science-knowledge.crate.zip` builds a reproducible inspection crate. The package is prepared for review but is **not** a claim of WorkflowHub registration, LifeMonitor enrollment, or full third-party validator certification

**LifeMonitor GitHub App:** no `lifemonitor.yaml` override is committed, so its account-level all-branches/all-tags/issue-check defaults remain in place where the App is installed
