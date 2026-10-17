# Contributing to the Life Science Ecosystem Lab

Changes to **knowledge behavior** belong in `.github/` and changes to **provenance/documentation verification** in `evidence/`

1. Describe the research question, approved source documents and expected observable output
2. Add or update deterministic fixtures; new sources remain untrusted until explicit approval in `evidence/profiles/sources.json`
3. Run `python -m unittest discover -s tests -v`, `python .github/scripts/check_rocrate.py` and `python -m evidence audit-docs --root . --files evidence/profiles/docs.json --output build/docs-audit.json`
4. When changing CWL interfaces or the canonical Actions workflow, update RO-Crate, Bioschemas and examples in the same PR
5. Include reproducible inputs, resulting output diffs, a reasoned impact assessment and documented uncertainty
6. Never include real patient records, personal access tokens, unsupported biological claims or unreviewed external credentials

**PR checks** require verified source identity, state ownership, failure transparency and data-only persisted writes. Approval to change a source profile is distinct from successful automated tests

## Research-software inspection contributions

For Tool issues, submit a public immutable source revision or a minimal synthetic fixture, CLI invocation, expected contract and sanitized report. For graph/search changes, include deterministic JSONL/FTS5 fixtures and provenance checks. Do not include private research plans, credentials or personally identifying/health data. Neither agent output nor a passing schema check is an accepted scientific conclusion. See [maintenance policy](docs/MAINTENANCE.md).
