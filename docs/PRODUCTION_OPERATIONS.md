# Native production operations and verification

This runbook describes the **actual production entrypoint**. Unlike the [real-world read-only drill](LIVE_EVIDENCE_DRILL.md), this workflow can accept a source-cited knowledge snapshot into `data/`.

## Native GitHub Actions invocation

1. Open [Life Science Knowledge Workflow — Native Lifecycle](https://github.com/lostlight530/life-science-ecosystem-lab/actions/workflows/life-science-knowledge.yml)
2. Select **Run workflow**, choose `main`, select a reviewed profile and leave `persist=false` for observation only
3. `native` reads `evidence/profiles/sources.json` and `evidence/profiles/topics.json`; `protein_structure` reads the isolated research profile and can never enter the `apply` job
4. Examine `build/workflow-profile.json`, source diagnostics and the resulting `life-science-verified-knowledge` Artifact before authorizing persistence
5. To accept a production candidate, start a new run from `main` with **profile `native` and `persist=true`**. The scheduled Monday maintenance always resolves `native` and remains eligible for guarded persistence
6. In the native persistence run, verify **both** job conclusions: `validate` succeeded; `apply` succeeded (it must not say `skipped`)
7. Confirm the `Persist guarded state` step created or consciously skipped a `data/` commit. The `Verify remote accepted state matches local commit` step must succeed
8. Read the actual remote `main` commit and inspect `data/inputs/current/candidate.json`, `data/knowledge/current.json`, `data/knowledge/events.jsonl`, `data/memories/current.json` and `data/receipts/gh-<RUN_ID>-<RUN_ATTEMPT>.json`
9. From the accepted revision, run:

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
| Isolated `protein_structure` profile succeeds | Reviewed field profile produced bounded artifacts | **No** |
| `NO_MEANINGFUL_DELTA` | No meaningful candidate difference, verified existing accepted state | **No new snapshot** |
| `CONFLICTED_WORLD_LINE_NO_APPLY` | The validated branch and actual main diverged | **No** |
| `EXISTING_STATE_INVALID_NO_APPLY` | Previous accepted state is damaged | **No** |
| `apply` success, data commit exists, remote SHA and state checks pass | GitHub has accepted the specific computational evidence snapshot | **Yes, bounded engineering evidence** |

Do not infer scientific validity, clinical correctness, third-party standards certification, WorkflowHub registration, LifeMonitor enrollment or live execution of external scientific workflows

For three concrete production accepts, linked GitHub runs, receipt/commit checks, stable selected-text comparison and no-delta ambiguity, consult the [Native Continuity Field Audit](NATIVE_CONTINUITY_FIELD_AUDIT.md). It is a historical field observation, **not** a reason to re-run `persist=true` or alter accepted data. The current `NO_MEANINGFUL_DELTA` gate requires (1) equal candidate `input_digest`, (2) equal `profile_digest`, and (3) equal accepted and proposed Knowledge objects when Knowledge is supplied. An identical selected-text digest alone does not meet this gate: a bootstrap change-classification transition changes the candidate output digest and Knowledge identity even with unchanged source text. See the separate temporary-root regression in `tests/test_native_acceptance_causality.py` for the corresponding stable-repeat no-write control.

## Security and retention boundaries

- Only `validate` uses `contents: read`; the separate guarded `apply` job uses `contents: write`
- GitHub Actions with `GITHUB_TOKEN` does not recursively trigger ordinary push workflows on the bot's state commit (per [GitHub's documented semantics](https://docs.github.com/en/actions/concepts/security/github_token))
- The world's validated Git SHA is checked twice before the write and the pushed commit is checked again afterward
- Failed validation retains only bounded diagnostics and documentation-audit results for 14 days; successful validation may provide more extensive source text in a **short-retention** Artifact
- Approved upstream repositories are public but source text may remain subject to original copyright notices and reuse terms; maintain the immutable source identity, license reference and retention decision before republication

[Verification](VERIFYING_RESULTS.md) · [Maintenance](MAINTENANCE.md) · [Provenance](PROVENANCE.md)
