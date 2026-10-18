# Life Science Knowledge Workflow — Portable CWL Replay

[Reproduction tutorial](../../docs/GETTING_STARTED.md) · [Verification results](../../docs/VERIFYING_RESULTS.md)

**Primary research artifact:** `knowledge.json` — a deterministic, source-cited map of what approved GitHub documentation actually states about life-science workflow registration, monitoring/testing, and reproducible research-object metadata

**Separate assurance asset:** the GitHub Evidence Aggregator processes immutable source snapshots and verifies the candidate bundle before knowledge extraction; it never claims scientific truth or overwrites active knowledge on its own

## Reproducible computational workflow (CWL v1.2)

```sh
python -m pip install -e .
python -m pip install cwltool
cwltool --no-container .github/knowledge/main.cwl .github/knowledge/test/workflow-job.yml
```

Four observable steps run in order: `aggregate` → `validate` → `knowledge` → `verify_knowledge`

Inputs are `records` (GitHub snapshots with commit and blob identities), `topics` (reviewed research taxonomy), and the independently installed Python software package. Outputs include the verifiable `knowledge.json`, candidate evidence, and both validation reports. All output identities are deterministic for unchanged content and profiles

The committed `.github/knowledge/test/workflow-job.yml` is **synthetic**, allowing fully offline reproducibility and regression testing. Its dummy Git SHAs demonstrate the data contract, not a real observation; the actual source adapter is tested independently. To work with verified current GitHub sources, first run:

```sh
ls-evidence collect --sources evidence/profiles/sources.json --output build/records.json
ls-evidence aggregate --input build/records.json --topics evidence/profiles/topics.json --output build/candidate.json
PYTHONPATH=.github/runtime:. python -m life_science_ecosystem_lab knowledge build --candidate build/candidate.json --topics evidence/profiles/topics.json --output build/knowledge.json
PYTHONPATH=.github/runtime:. python -m life_science_ecosystem_lab knowledge verify --candidate build/candidate.json --topics evidence/profiles/topics.json --knowledge build/knowledge.json
```

The GitHub Actions **Life Science Knowledge Workflow — Native Lifecycle** carries out live observation, uploads independently verifiable artifacts, and performs guarded automatic persistence on its scheduled runs when the verified semantic delta is meaningful. Explicit `workflow_dispatch persist=true` is also supported on `main`; other manual runs remain read-only. Both paths enforce branch-head world-line and data-only write checks

`ro-crate-metadata.json` documents the main workflow, four CWL steps, Bioschemas FormalParameter inputs/outputs, testing suite and GitHub Actions test resource. `python .github/scripts/build_rocrate.py build/life-science-knowledge.crate.zip` builds a reproducible inspection crate. Package structure does not itself prove external registration; current records are maintained in [standards status](../../docs/STANDARDS.md)

**LifeMonitor GitHub App:** the repository-scoped [`lifemonitor.yaml`](../../lifemonitor.yaml) uses the documented root filename and keeps repository issue checks enabled. It omits `push` and `public` overrides, leaving branch/tag selection, registry updates and visibility to account-level settings. This configuration remains separate from the WTROC enrollment recorded in [standards status](../../docs/STANDARDS.md)
