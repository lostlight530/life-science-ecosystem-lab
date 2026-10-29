# Frozen 2026-10-30 GitHub provenance census

[Full origin-to-present history](../REPOSITORY_HISTORY_AND_PROVENANCE.md) · [Open claims](../CLAIM_VERIFICATION_GAPS.md) · [Provenance and authorities](../PROVENANCE.md)

**Observed:** `2026-10-29T16:24:03.499Z` UTC / 2026-10-30 Asia/Shanghai · **Reference main:** [`05ab6b2dc98dfe13581b5ae1bedcd11a58dbbb77`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/05ab6b2dc98dfe13581b5ae1bedcd11a58dbbb77)

This is a **project-authored, non-production, read-only GitHub API observation**, not an official GitHub archive certification or a life-science result. GitHub API paging was read while the `main` SHA was checked unchanged. It uses public records only, with no private credentials, original CI logs, private third-party observations, or full upstream copyrighted source bodies.

| Immutable JSON snapshot | API surface | Fixed count |
| --- | --- | --- |
| [`commits-2026-10-30.json`](commits-2026-10-30.json) | `/repos/lostlight530/life-science-ecosystem-lab/commits?per_page=100&page=1..3` | 234 reachable main commits, SHA + parent edges + dates + subjects |
| [`pull-requests-2026-10-30.json`](pull-requests-2026-10-30.json) | `/repos/lostlight530/life-science-ecosystem-lab/pulls?state=all&per_page=100&page=1` | 42 PR objects, 40 merged, #29 and #32 closed without merge |
| [`action-runs-2026-10-30.json`](action-runs-2026-10-30.json) | `/repos/lostlight530/life-science-ecosystem-lab/actions/runs?per_page=100&page=1..6` | 531 visible workflow runs, 483 success / 8 failure / 40 cancelled |

Every JSON includes `observed_at_utc`, `reference_main_sha`, `source_urls`, `returned_count` and explicit `provenance_limit`; unique IDs and the parent-closed main DAG are checked in the independent [offline archive test](../../tests/test_repository_provenance_archive.py). These files are stored under `docs/provenance/`, **not** the production-authoritative `data/`.

## Offline, read-only repeat

~~~sh
python -m unittest discover -s tests -p test_repository_provenance_archive.py -v
python - <<'PY'
from pathlib import Path
import json
base = Path("docs/provenance")
for name in ("commits", "pull-requests", "action-runs"):
    data = json.loads((base / f"{name}-2026-10-30.json").read_text())
    print(name, data["observed_at_utc"], data["returned_count"])
PY
~~~

This reproduces the **archived structural census**, not historical network calls, final truth of self-attributed Agent identities, continuous live CI monitoring, independent scientific experiments or original expired artifacts. To check a later reality, use the documented original URLs and record a **new** UTC observation with old and new values, rather than replacing the old snapshot.

Source distinctions: Git commits are version objects; PRs are proposed/reviewed changes (including unmerged negatives); Actions are particular CI/scheduled/manual runs; the three production `data/receipts` are **distinct accepted Knowledge events**; WorkflowHub, LifeMonitor, Zenodo, bio.tools and OpenEBench own separate external objects and clocks. Never combine their counts into a fabricated scientific KPI.

**Known omissions:** inaccessible branches/forks, deleted or unavailable runs, expired Actions artifacts, private account records, unverified February predecessor sources, third-party API responses unavailable during this session, all future runs and the publishing PR itself. The snapshot is a dated lower-scoped observation of **what GitHub returned**, not a permanent full reconstruction of every unpublished operation.

[Native accepted-state evidence](../NATIVE_CONTINUITY_FIELD_AUDIT.md) · [External interoperability](../INTEROPERABILITY_REVIEW.md)
