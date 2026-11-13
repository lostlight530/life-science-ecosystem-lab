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
7. For a structural documentation change, update `docs/README.md` **and** the authoritative documentation inventory `evidence/profiles/docs.json`. CI checks every Markdown file in the repository's public guide, Agent handoff, self-check and Framework documentation directories, including `.github/pull_request_template.md`; external URLs remain inventory-only, not live link verification

The required validation workflow is actor-neutral. Do not add contributor-specific bypasses, blanket `continue-on-error`, or external registry/network calls as merge prerequisites. Its independent domains all run before the aggregate verdict, so address every failed domain reported by the same run rather than relying on an earlier failure to hide later checks

### 中文贡献与引用核对 / Bilingual evidence and version review

涉及长期数据或软件版本的 PR 应给出资产范围、准确修订号、实际测试与退出状态、原始／派生证据、引用版本及未测范围；不要把一次模型输出当作独立复现，不要公开私人或个人级生物医学资料；README 修改不授权更改已经接受的 `data/` 和旧 Actions 结果

Contributions affecting longitudinal evidence or releases must identify asset scope, exact revision, actual test/exit state, raw versus derived evidence, cited version and untested limits. Model output is not independent reproduction; do not publish private or person-level biomedical information. README edits do not authorize modifying accepted `data/` or historical runs

## Review boundaries

- PR tests and static inspection cannot establish biological truth, full external standards certification, publication or registry acceptance
- External Agents may independently contribute via normal GitHub review; they are not runtime requirements or trusted decision authorities
- Repository sources, private plans, internal research methods, credentials, unpublished texts, personal/health information and nonpublic URLs must **not** be submitted to this public repository, issues or CI logs
- Maintainers accept source and state changes under independent provenance, world-line and write-boundary checks, not merely because a proposed solution runs

[Verification results](docs/VERIFYING_RESULTS.md) · [Maintenance and privacy](docs/MAINTENANCE.md) · [Security](SECURITY.md)

## Research and cross-registry review obligations

When proposing a scientific-method or provenance clarification, specify the **exact falsifiable claim** and the alternatives it must discriminate. Distinguish software correctness, evidence integrity, method suitability and scientific evaluation as four separate responsibilities. Use the [research methodology review contract](docs/RESEARCH_METHODOLOGY.md) for bounded outcomes and the [cross-platform provenance worksheet](docs/PROVENANCE.md) for upstream/downstream source comparisons.

Include fixed source and method identities, direct observation times, input bytes or digests, control cases, measurement units, numerator/denominator where relevant, excluded/missing cases, failures, replay boundaries and a responsible reviewer. Preserve disagreements and negative results. Agent-proposed text or schema-valid handoffs remain proposals, not identity attestation or automatic scientific approval.

A documentation-only change must keep the existing Workflow, Evidence Tool, Bio Tool, experimental Framework runtime, source/topic registries, accepted data and historical release metadata unmodified. Verify the **actual** PR check conclusions before merging; do not install an extra external-service or Agent gate to make a prose obligation look executable.
