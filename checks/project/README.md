# Project custom checks — repository authority only

This directory holds **our own** declared repository contract: the explicit `manifest.json` inventory of the three installed research-software CLIs, native workflows, provenance rules, project publications and accepted source/data entrypoints. Its checks do not impersonate an institution or copy upstream default configuration.

The `project-custom` daily job records per-file SHA-256, entrypoint presence, local public documentation and metadata validity, fail-closed synthetic/provenance test results, current Git-accepted state and bounded independent Knowledge Quality. It never changes `data/`, external registration, source approvals or platform account settings.

Our root-level `lifemonitor.yaml` is a repository-scoped LifeMonitor configuration using the official filename. It enables this repository's issue checks while leaving branch/tag tracking, registry updates and visibility unspecified so account-wide settings remain authoritative. The project check inspects this local file only; it never changes LifeMonitor account settings. Our `ro-crate-metadata.json`, the project's `metadata/` and the three CLIs remain project-owned artifacts. Upstream official requirements and public reachability observations are owned by `checks/institutional/` and checked independently.

Failures in required project files or the actual validation process must fail the custom CI job; unrelated external site timeouts must not be able to turn our project validation status into a false failure or false success. Custom reports are retained in `build/daily-selfcheck/project-custom/` and a separate project Artifact, never merged into an institutional default report. Any addition to a custom check requires a reviewed PR and regression tests.

Use `python -m evidence.daily_selfcheck project --manifest checks/project/manifest.json --root . --output build/daily-selfcheck/project-custom/manifest-report.json` locally; the installed GitHub Action executes stronger existing tests alongside it.
