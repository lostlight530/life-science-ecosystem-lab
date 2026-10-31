# Research lessons: cloud census replay across source-time boundaries · 2026-10-31

[Full origin audit](../provenance/FULL_HISTORY_REPLAY_2026-10-31.md) · [Machine population](../provenance/full-history-census-2026-10-31.json) · [Executable falsifier](../../tests/test_full_history_census_replay.py) · [Earlier failure correction](../provenance/FAILURE_CAUSAL_REPLAY_2026-10-31.md)

**Public and privacy-minimized**: this note uses public repository object IDs, no personal biography, private correspondence, credentials, prompts, institution-internal records, raw third-party data or original unrelated Runner log bodies

## What independently attempting to falsify earlier reports taught us

- **A self-reviewed 587-run report was only a temporal cutoff**: a fresh six-page cloud read returned 598 IDs. Exact union and field comparison found the old 587 unchanged, plus 11 newly observable successful PR/push checks. Adding 11 is an observation update, not a correction of an arithmetic error or 11 new studies
- **A green present does not erase a red past**: an earlier, different 531-ID frozen snapshot contained eight failed workflow runs which are no longer visible in the current API population. A locally versioned archive retains those negative observations. The causal source-level repro and absent original Runner logs remain distinct evidence grades
- **A run is not a Job, a Job is not an accepted state**: 31 observed scheduled Runs contained 48 successful Jobs. Only two scheduled Knowledge Runs actually wrote accepted Knowledge snapshots, alongside one initial manually authorized write. A later Bio `pinned-field` Job may be skipped under a push while `offline` passes. One whole-run green badge cannot certify every scientific or field activity
- **Saved summaries should be adversarially rechecked**: earlier errors arose from a 134-row temporal workflow-name join and two wrongly calculated medians. This review instead keyed names by actual Run ID, rebuilt the population through every dated delta, and independently sorted all 31 schedule offsets
- **Git ancestry, PR acceptance and external registry state have different owners**: all 242 main commits form a parent-closed DAG reaching the October root; 50 PRs include two unmerged proposals; one v0.4.0 Release and WorkflowHub item do not prove that bio.tools/OpenEBench/Zenodo just synchronized
- **Procedural governance is not server-enforced governance**: `protected=false` and no public Rulesets were observable, while branch-protection details were inaccessible. Voluntarily waiting for a successful PR is meaningful process evidence, not proof of an immutable required-status or admin bypass contract
- **Immutable-by-reference is independently testable**: store authoritative Git Blob SHA for the frozen snapshots and `data/`, and rehash the actual bytes with the Git object format during offline CI. Testing only a manually copied count would fail to detect archive replacement
- **Cloud APIs do not themselves preserve an exact query clock**: bracket the read interval with a real UTC clock and record the individual API request timestamp as unknown. Commit time, runner start and API `created_at` are different things

## Eight-stage reproducible method

**DEFINE** one falsifiable observation claim → **PIN** root SHA, main HEAD, UTC observation window and prior ID population → **QUALIFY** Git/PR/Run/Job/Receipt source grades → **EXECUTE** fetch every API page and re-read each scheduled Job → **EVALUATE** compute set differences, graph closure and medians → **AUDIT** preserve historical negatives and biological warning semantics → **REVIEW** isolated documentation/test PR and independent CI → **REPLAY** verify canonical Blob identities and exact populations from committed bytes

The negative control is not allowed to disappear when the present API yields zero failures. An unregistered clinical or scientific relation is not allowed to become an accepted fact because local parsing tests pass

**Disposition:** preserve legacy files, publish only dated and minimally normalized public provenance, require independent CI for the extra offline verification, and keep software/production data untouched unless a real reproducible defect requires a separate authorized intervention. Additional GitHub executions after this cutoff require a subsequent dated delta rather than altering it
