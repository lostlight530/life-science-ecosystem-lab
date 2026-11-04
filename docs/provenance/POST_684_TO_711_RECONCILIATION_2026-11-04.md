# Post-684 to 711 GitHub Actions and native quality reconciliation · 2026-11-04

[Machine-readable, source-pinned 27-Run delta](post-684-to-711-observation-2026-11-04.json) · [Previous frozen 673→684 cutoff](POST_673_TO_684_RECONCILIATION_2026-11-03.md) · [First-day provenance taxonomy](../taxonomy/README.md) · [Public failure lesson](../lessons/2026-11-04-cron-offset-observation-and-conditional-jobs.md) · [Independent offline regression](../../tests/test_post_684_run_delta.py)

**Scope and cutoff:** a read-only, pre-publication GitHub API census against `main=0728c19d32492d2932bffbab9045e7aeedcbd667`. Eight Actions pages reported **100/100/100/100/100/100/100/11 = 711 unique currently visible Run IDs**. The exact individual API request UTC instants were not independently recorded and remain **UNKNOWN**. These 711 are not an all-time guaranteed history and exclude the PR and push checks created to publish this document.

## DEFINE → PIN → QUALIFY: keep independent identities and a frozen denominator

The preceding archived census contained **684** Run IDs. Rebuilding that population from the independently archived 598-Run full-history source and its six additive deltas, then joining the new eight-page API response by numeric Run ID, yields **684 old IDs retained, zero previously visible IDs missing and 27 new unique IDs**. The 27 new records are all `success`: **16 push, nine pull_request and two schedule**, with a current visible population of **670 success / 41 cancelled / zero currently visible failure**. Trigger categories now total **364 push / 303 pull_request / 40 schedule / four workflow_dispatch**. Earlier October 30 archived failures and later PR #55 interim failures are **not erased** by this new visibility snapshot.

The main source point has **253 parent-closed, main-reachable Git commits back to root `00009a38bc136a7c245270770b005e4e102a870d`**, **60 PRs (58 merged, #29 and #32 closed-unmerged, none open)**, **283 tracked Git blobs**, nine current Workflow YAML definitions and GitHub Releases `v0.4.0` / `v0.5.0`. Historical February predecessor engineering remains a *different repository lineage*; a PR title containing an Agent name is not proof of that Agent's actual execution surface.

## EXECUTE → EVALUATE: Run, Job, schedule, Artifact and accepted production

The **27** new GitHub latest-attempt Job API reads contain **54 Jobs: 51 success, three conditionally skipped, zero failure**. All three skips are Bio Tool `pinned-field` Jobs on merged-main push Runs `41573113868`, `41575989806` and `41576421725`. Equivalent `pinned-field` jobs succeeded on PR Runs `41573009904`, `41575886687` and `41576302737`. This follows the `life-science-bio.yml` event guard; a successful Bio Run therefore **does not mean all conditional Jobs ran**.

| New scheduled run (UTC 2026-11-03) | Actual latest-attempt Jobs | GitHub API `created_at` | Nominal cron (UTC) | Difference |
| --- | --- | --- | --- | --- |
| [Daily institutional/project self-check #41604262360](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41604262360) | Institutional defaults **Success**, project custom **Success** | 08:34:18 | 01:41:00 | +06:53:18 |
| [Knowledge continuity #41632276154](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41632276154) | `verify` **Success** | 12:01:44 | 04:17:00 | +07:44:44 |

These are clock differences **between YAML cron and GitHub API run creation**, **not measured Runner queue time**, proof of a GitHub platform fault, or evidence that the workflow never ran. They are large enough to merit preservation and later comparison. The review does not change scheduling or silently count a pending next-day run as failed.

Read-only evidence retained by GitHub from the new scheduled runs:

- Daily institutional-defaults artifact **13215048896** (`sha256:986a014a3239a1c80a77ae39e7d9dc1009f8dfa0bf105a88f571c795fe924d5b`) and project-custom artifact **13214669224** (`sha256:53abf8e698aabc65a85c8daf2f119ef0a18b9ae990a9f5586697d532a71d7e90`), with two successful Jobs
- Continuity artifact **13228223974** (`sha256:17b1939f7d5014494eceed55e5fed3a69ab546615e2865f1abd807c555c8cf2d`), with successful state, knowledge and graph verification and the log marker `KNOWLEDGE_QUALITY_PASS`
- These are **GitHub-reported ZIP digests**, not independently rehashed download bytes; the user-facing report must not promote them to a locally verified hash attestation
- The previously frozen **38** scheduled Runs / **59** successful scheduled Jobs plus the **two** new scheduled Runs / **three** successful Jobs give **40** scheduled Runs / **62** directly reviewed successful Jobs over those two adjacent observation populations

**Native production is independently unchanged:** four Git-backed `APPLIED` Receipts, four linked `events.jsonl` events and three archived Candidate snapshots. The last accepted execution is `gh-41436556408-1` on **2026-11-02**, marked `DOCUMENT_TEXT_UNCHANGED`. The original source-linked graph has 17 entities and 26 `SOURCE_MATCH` relationships; neither an updated source pin nor a daily Quality PASS proves a new scientific proposition.

## AUDIT → REVIEW → REPLAY: negative controls and non-claims

Preserve the **eight failures** in the original 531-Run October 30 observation and the **three separately documented PR #55 intermediate failures** without assigning an unverified deletion cause. Preserve the previously documented clock inconsistency and the differences between a workflow's current display name, its historical run name and its YAML path. The latest API's zero visible failures cannot falsify a correctly scoped older failing census.

The November 3 institutional Job executed a public read-only URL check and the separate custom Job reported its eleven project checks as `PASS`. Neither asserts that LS Login, WorkflowHub, LifeMonitor, bio.tools, OpenEBench or Zenodo accepted or endorsed the software; provider-owned live states remain **UNKNOWN** where they were not independently observed. Official institution pointers and this project's custom files must not be merged into one certification result.

**Disposition:** `OBSERVED_OPERATIONAL_DELTA` for 27 new Runs, three conditional skips and two delayed-from-cron scheduled observations; `NO_CHANGE_REQUIRED` for Knowledge Workflow, Evidence Tool, Bio Tool, Framework, nine Actions definitions, accepted `data/`, releases and registry metadata; `NO_NEW_VERIFIED_SCIENTIFIC_CLAIM` for research conclusions. Existing snapshot JSONs and correction history are immutable, and any checks generated by this reporting PR belong to a later census.

**Replay boundary:** `python -m unittest discover -s tests -p 'test_post_684_run_delta.py' -v` validates the frozen Run-ID reconstruction, scheduled clock arithmetic and accepted-state file counts offline; it does **not** rerun GitHub's historical hosted Jobs, original provider URLs, or private Agent actions.
