# Daily Research Self-Check — Institutional Defaults vs Project Custom

The repository executes one scheduled, **read-only** GitHub Actions workflow with **two completely separate jobs, configurations, reports and Artifacts**. This is a scheduled research-software health *check*, not a new fourth software product, an automatically accepted scientific result or an external platform's own official monitor.

## Schedule and behavior

- **Daily at 01:41 UTC** (09:41 Asia/Shanghai), plus optional manual `workflow_dispatch`
- On pull requests the institutional checker runs **only its own offline contract tests**, avoiding unrequested contacts to external institutions
- The institutional job runs `tests/test_institutional_selfcheck.py`; project-manifest and LifeMonitor repository-config tests run in the sibling project job. There is no `needs` dependency between jobs, so a project-only contract failure cannot suppress scheduled institutional observations
- On actual schedule (or manual dispatch with `live_public_institutions: true`) the institutional job makes at most six bounded, anonymous, read-only GET requests against exact allowlisted public service URLs, without following redirects, access tokens or user account state
- The custom job verifies local file SHA-256s, three public CLI entrypoints, the current source/topic and scientific metadata rules,  full Python regression tests, docs links, RO-Crate structure, publication boundary, accepted Git state, knowledge map and graph, and Knowledge Quality
- Two jobs have `contents: read`, independent results and **no production writes**, no external registration, no privileged Agent execution and no user credentials

## Institutional public defaults (external reference plane)

**Location:** `checks/institutional/defaults.json` and `checks/institutional/README.md` only. These are *maintainer-curated official public URLs*, **not authentic copies of the institutions' files or settings**. Any official change still requires verifying the live upstream authoritative document.

Monitored public pointers: LS Login, WorkflowHub, LifeMonitor, OpenEBench, FAIRDOMHub and bio.tools. An entry's HTTP 200 only establishes that one public GET response was observed; 3xx, 401/403, 5xx and temporary transport errors are recorded without converting them into unsupported service-availability or registration verdicts. The daily JSON explicitly lists the unverified claims.

**Daily report:** `build/daily-selfcheck/institutional-defaults/report.json` → Artifact `institutional-defaults`, 30 days

This is **not** LifeMonitor's own recurring test monitoring, official WorkflowHub enrollment, LS Login account authorization, bio.tools curation, official uptime monitoring or an OpenEBench benchmark result.

## Our project custom contract (repository authority plane)

**Location:** `checks/project/manifest.json` and `checks/project/README.md`; these are **our files**. They define required software paths, workflow links and metadata acceptance checks, and cannot include `checks/institutional/`.

**Daily reports:** `build/daily-selfcheck/project-custom/*` → Artifact `project-custom`, 30 days

This job fails if a mandatory local file is missing/unsafe, one of the three CLI entrypoints disappears, a source/metadata/documentation contract fails, accepted state or graph validation fails, or repository regression tests fail. It does **not** mark project compliance based on whether a remote institution returned HTTP 200. It uses the previously agreed native three assets and accepted `data/` without changing them.

## Reproduce both checks locally

```sh
PYTHONPATH=.github/runtime:. python -m evidence.daily_selfcheck institutional --catalogue checks/institutional/defaults.json --output build/daily-selfcheck/institutional-defaults/report.json
PYTHONPATH=.github/runtime:. python -m evidence.daily_selfcheck project --root . --manifest checks/project/manifest.json --output build/daily-selfcheck/project-custom/file-contract.json
PYTHONPATH=.github/runtime:. python -m unittest discover -s tests -p 'test_institutional_selfcheck.py' -v
PYTHONPATH=.github/runtime:. python -m unittest discover -s tests -p 'test_project_selfcheck.py' -v
```

The first command is intentionally offline by default. To observe the six public endpoints, add `--live` deliberately.

GitHub Actions run log and 30-day artifacts are the operational receipt. Daily recurrence is proved only after actual scheduled runs are recorded: successful one-off CI and a cron expression alone are not evidence that a day-after-day scheduled run already occurred. Scheduled GitHub Actions may be delayed.

## Ownership, change control and non-claims

- **External publisher:** owns its specification, institutional policy, uptime status, identity and service registration
- **This project:** owns its manifest, self-check implementation, public scientific software and accepted Git state
- **Independent Agent/human reviewer:** can suggest edits through reviewed PR, but no automatic acceptance or custom overwrite of institutional settings
- **Known limitation:** a metadata preflight or successful 128+ unit tests is still not experimental biological validation or acceptance by an external registry
- **Non-goal:** mixing official, custom, synthetic and real observations into a single undifferentiated PASS

The independent existing `life-science-continuity.yml` daily accepted-state check remains in place; this new daily self-check complements it rather than replacing its original production-state role.
