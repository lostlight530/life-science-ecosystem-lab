# Understanding verification results

This project's independent Workflow and Tool produce **bounded engineering evidence**, not clinical/biological correctness or external platform certification. Determine *exactly which artifact, version, command and check* supports a statement.

## Four distinct levels

| Evidence level | Observable result | Does **not** establish |
| --- | --- | --- |
| Local Tool inspection | JSON + optional Markdown and SARIF, PASS / WARN / FAIL | A scientific conclusion, remote website reachability, full standards conformance |
| Evidence collection/aggregation | Approved source revision, object identity, digests, diagnostics, candidate eligibility | The scientific meaning of the source documents is correct |
| Computational knowledge replay | Deterministic knowledge JSON, source-linked JSONL and FTS5 queries on a specific input | That the synthetic fixture is a live GitHub observation or causal inference |
| GitHub native durable lifecycle | Completed scheduled/authorized job **plus** accepted `data/` commit and state verification | That third-party registries accepted or independently reproduced the software |

## Tool report decisions

`ls-evidence inspect` returns **0** for PASS or WARN; **1** for FAIL; **2** for invalid usage or inspect errors. Read the `status`, `findings`, `scope` and `unverified` keys in the JSON report instead of assuming exit code 0 means scientific verification. Do not report `WARN` as certified success.

`ls-evidence audit-docs` checks pinned **local Markdown links**. The listed external URLs are inventory records and are **not** confirmed reachable. It returns an error if a local link is missing, unsafe or unsupported.

## Graph claims and reproducibility

The current JSONL graph is a deterministic projection of the verified source-cited knowledge map. `SOURCE_MATCH` means a topic matched a source document; it does not prove an empirical relation. The SQLite FTS5 index is built in memory at query time and is not a second authoritative datastore.

```sh
ls-knowledge graph verify --dir build/graph --knowledge build/replay/knowledge.json
ls-knowledge graph search --dir build/graph --query workflow --limit 5 --hops 1
```

To reproduce the query, preserve the exact knowledge input and the `entities.jsonl`, `relations.jsonl` and `graph-manifest.json` outputs and record the repository commit. For accepted main-branch graph events, the append-only event-chain verification is included in state checks. Accepted receipts distinguish per-attempt `execution_id`, content-addressed `snapshot_id` and `change_kind`, so restoring an earlier source snapshot does not reuse an earlier event or receipt. `DOCUMENT_TEXT_UNCHANGED` is a selected-text comparison, not a proof of new scientific knowledge.

## Native workflow reading guide

1. Check the GitHub Actions event: PR/push CI, synthetic CWL replay, manual observation and scheduled persistence are different events
2. Confirm the expected source revision and GitHub run conclusion
3. Inspect `build/source-diagnostics.json`, `projection_eligible`, and machine-readable reports
4. For durable claims, verify an actual accepted `data/` commit, current knowledge and associated receipts; **no-change, failed or conflicted runs are not new knowledge production**. `ls-knowledge state verify --repository-root . --require-accepted` rejects an empty bootstrap tree, while the ordinary state command checks only any state currently present. The strict check also binds the latest accepted graph event to the active evidence candidate, so a valid but substituted candidate cannot pass as the accepted state.
5. Treat WorkflowHub, LifeMonitor and bio.tools as externally verified states only when a genuine registry or monitoring record exists

[Getting Started](GETTING_STARTED.md) · [Provenance](PROVENANCE.md) · [Maintenance](MAINTENANCE.md)
