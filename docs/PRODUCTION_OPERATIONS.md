# Native production operations and verification

This runbook describes the **actual production entrypoint**. Unlike the [real-world read-only drill](LIVE_EVIDENCE_DRILL.md), this workflow can accept a source-cited knowledge snapshot into `data/`.

## Native GitHub Actions invocation

1. Open [Life Science Knowledge Workflow — Native Lifecycle](https://github.com/lostlight530/life-science-ecosystem-lab/actions/workflows/life-science-knowledge.yml)
2. Select **Run workflow**, choose `main`; leave `persist=false` for observation only
3. Examine the resulting `life-science-verified-knowledge` Artifact and source diagnostics before authorizing persistence. Only approved public sources from `evidence/profiles/sources.json` are read
4. To accept a first production candidate, start a new run from `main` with **`persist=true`**. The scheduled Monday maintenance is also authorized for guarded persistence
5. In the native run, verify **both** job conclusions: `validate` succeeded; `apply` succeeded (it must not say `skipped`)
6. Confirm the `Persist guarded state` step created or consciously skipped a `data/` commit. The `Verify remote accepted state matches local commit` step must succeed
7. Read the actual remote `main` commit and inspect `data/inputs/current/candidate.json`, `data/knowledge/current.json`, `data/knowledge/events.jsonl`, `data/memories/current.json` and `data/receipts/gh-<RUN_ID>-<RUN_ATTEMPT>.json`
8. From the accepted revision, run:

```sh
python -m life_science_ecosystem_lab state verify --repository-root . --require-accepted
python -m life_science_ecosystem_lab knowledge verify \
  --candidate data/inputs/current/candidate.json \
  --topics evidence/profiles/topics.json \
  --knowledge data/knowledge/current.json
python -m life_science_ecosystem_lab graph verify \
  --dir data/knowledge --knowledge data/knowledge/current.json
python -m life_science_ecosystem_lab graph search \
  --dir data/knowledge --query workflow --limit 5 --hops 1
```

Set `PYTHONPATH=.github/runtime:.` and install the editable project (or use `ls-knowledge`) as described in [Getting Started](GETTING_STARTED.md)

## Classification and failure interpretation

| Observed outcome | Meaning | Production acceptance |
| --- | --- | --- |
| Validation/collection fails | Approved upstream source unavailable or malformed, or a contract failed | **No** |
| `projection_eligible=false` | Partial source observation; fail-closed | **No** |
| `apply` skipped | Run was read-only or not authorized for writing | **No** |
| `NO_MEANINGFUL_DELTA` | No meaningful candidate difference, verified existing accepted state | **No new snapshot** |
| `CONFLICTED_WORLD_LINE_NO_APPLY` | The validated branch and actual main diverged | **No** |
| `EXISTING_STATE_INVALID_NO_APPLY` | Previous accepted state is damaged | **No** |
| `apply` success, data commit exists, remote SHA and state checks pass | GitHub has accepted the specific computational evidence snapshot | **Yes, bounded engineering evidence** |

Do not infer scientific validity, clinical correctness, third-party standards certification, WorkflowHub registration, LifeMonitor enrollment or live execution of external scientific workflows

## Security and retention boundaries

- Only `validate` uses `contents: read`; the separate guarded `apply` job uses `contents: write`
- GitHub Actions with `GITHUB_TOKEN` does not recursively trigger ordinary push workflows on the bot's state commit (per [GitHub's documented semantics](https://docs.github.com/en/actions/concepts/security/github_token))
- The world's validated Git SHA is checked twice before the write and the pushed commit is checked again afterward
- Failed validation retains only bounded diagnostics and documentation-audit results for 14 days; successful validation may provide more extensive source text in a **short-retention** Artifact
- Approved upstream repositories are public but source text may remain subject to original copyright notices and reuse terms; maintain the immutable source identity, license reference and retention decision before republication

[Verification](VERIFYING_RESULTS.md) · [Maintenance](MAINTENANCE.md) · [Provenance](PROVENANCE.md)
