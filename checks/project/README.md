# Project custom checks — repository authority only

This directory holds **our own** declared repository contract: the explicit `manifest.json` inventory of the three installed research-software CLIs, native workflows, provenance rules, project publications and accepted source/data entrypoints. Its checks do not impersonate an institution or copy upstream default configuration.

The `project-custom` daily job records per-file SHA-256, entrypoint presence, local public documentation and metadata validity, fail-closed synthetic/provenance test results, current Git-accepted state and bounded independent Knowledge Quality. It never changes `data/`, external registration, source approvals or platform account settings.

Our root-level `lifemonitor.yaml` is a repository-scoped LifeMonitor configuration using the official filename. It enables this repository's issue checks while leaving branch/tag tracking, registry updates and visibility unspecified so account-wide settings remain authoritative. The project check inspects this local file only; it never changes LifeMonitor account settings. Our `ro-crate-metadata.json`, the project's `metadata/` and the three CLIs remain project-owned artifacts. Upstream official requirements and public reachability observations are owned by `checks/institutional/` and checked independently.

Failures in required project files or the actual validation process must fail the custom CI job; unrelated external site timeouts must not be able to turn our project validation status into a false failure or false success. Custom reports are retained in `build/daily-selfcheck/project-custom/` and a separate project Artifact, never merged into an institutional default report. Any addition to a custom check requires a reviewed PR and regression tests.

Use `python -m evidence.daily_selfcheck project --manifest checks/project/manifest.json --root . --output build/daily-selfcheck/project-custom/manifest-report.json` locally; the installed GitHub Action executes stronger existing tests alongside it.

## Bounded custom daily check registry

`checks/project/daily_checks.json` selects **reviewed, built-in check IDs only**, not arbitrary commands or executable snippets. The fixed ten blocking checks cover manifest, tests, documentation, public metadata, RO-Crate, publication boundary, accepted state, knowledge, graph and knowledge quality. These checks cannot be omitted or downgraded through JSON. The optional `ecosystem_preflight` is explicitly advisory and does not certify external registry acceptance.

`python -m evidence.daily_custom_runner --root . --registry checks/project/daily_checks.json --output build/daily-selfcheck/project-custom/execution-report.json` executes each selected check in a separate, bounded subprocess and records per-check `PASS / FAIL / TIMEOUT / ERROR`. Failure of one check does **not** skip the remaining checks. The final exit code remains nonzero if any mandatory check fails. For an advisory failure the aggregate result is `PASS_WITH_ADVISORY`, not an unqualified PASS.

The compact execution receipt records the registry SHA-256, GitHub execution identity where supplied by Actions, check durations, outcome and hashes of captured logs, **never raw stderr/stdout**. Existing detailed JSON diagnostics remain separate files in the same project Artifact. Institutional public endpoint observations remain strictly in the other job and Artifact. Changes to known check commands or mandatory gate membership require a reviewed code change and regression tests, rather than arbitrary manifest-level execution.
