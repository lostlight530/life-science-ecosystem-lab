# Contributing to Life Science Ecosystem Lab

The repository maintains **three established independent assets plus one experimental, separately installable Framework**, not an Agent/Skills package. Knowledge Workflow behavior belongs to [`.github/`](.github/README.md), independent evidence inspection to [`evidence/`](evidence/README.md), and bounded biological data processing to [`bio_tool/`](bio_tool/README.md). The peer [`framework/`](framework/README.md) evaluates life-sciences **cross-domain software-engineering contracts**, not biological conclusions. See the [documentation index](docs/README.md) before starting.

## Reproduce your proposed change

1. Open the relevant [issue form](.github/ISSUE_TEMPLATE/) or PR and state the *observable* problem, proposed behavior, and affected asset
2. Supply a minimal synthetic fixture or link to a **public, immutable** Git commit; new collection sources require an explicitly reviewed change to `evidence/profiles/sources.json`
3. Include the command, expected and actual output, status, error handling, and remaining verification limits
4. Run both local regression and link checks from the repo root:

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
ls-evidence audit-docs --root . --files evidence/profiles/docs.json --output build/docs-audit.json
python .github/scripts/check_rocrate.py
python .github/scripts/check_metadata.py
python .github/scripts/check_publication_boundary.py
```

5. For independent Framework changes, also run the dedicated regression and synthetic contract challenge without modifying the existing Workflow or Tools:

```sh
python -m pip install --no-deps -e ./framework
python -m unittest discover -s framework/tests -v
python -m ls_framework.challenge --bundle framework/fixtures/software-cross-domain.json --root framework/fixtures --output build/framework-challenge.json
```

These tests are synthetic software-contract evidence, **not** biological or institutional verification. For scientific research proposals, preserve falsifiable questions, fixed references, failures and unresolved limitations, and keep accepted data strictly under the existing native authority

6. Changes to CWL, GitHub Actions inputs/outputs or public descriptions must update the relevant [RO-Crate](ro-crate-metadata.json), [Bioschemas](metadata/) and documentation contracts; verify CWL with [Getting Started](docs/GETTING_STARTED.md)
6. For a structural documentation change, update `docs/README.md` **and** the authoritative documentation inventory `evidence/profiles/docs.json`. CI tests require complete coverage of public Markdown guides

The required validation workflow is actor-neutral. Do not add contributor-specific bypasses, blanket `continue-on-error`, or external registry/network calls as merge prerequisites. Its independent domains all run before the aggregate verdict, so address every failed domain reported by the same run rather than relying on an earlier failure to hide later checks

## Review boundaries

- PR tests and static inspection cannot establish biological truth, full external standards certification, publication or registry acceptance
- External Agents may independently contribute via normal GitHub review; they are not runtime requirements or trusted decision authorities
- Repository sources, private plans, internal research methods, credentials, unpublished texts, personal/health information and nonpublic URLs must **not** be submitted to this public repository, issues or CI logs
- Maintainers accept source and state changes under independent provenance, world-line and write-boundary checks, not merely because a proposed solution runs

[Verification results](docs/VERIFYING_RESULTS.md) · [Maintenance and privacy](docs/MAINTENANCE.md) · [Security](SECURITY.md)
