# Public lesson · file-path admission and cancelled Runs can hide real failed Jobs (2026-11-13)

[Bounded source audit](../provenance/POST_807_TO_849_RECONCILIATION_2026-11-13.md) · [Machine Run/Job evidence](../provenance/post-807-to-849-observation-2026-11-13.json) · [Offline check](../../tests/test_post_807_run_delta.py)

**Observed counterexample:** an intermediate PR head introduced `RELEASE_POLICY.md` outside reviewed additive path families. Four independent frozen file-governance tests failed in the Repository contracts Job of Run [43210854941](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/43210854941), although its parent Run eventually had `cancelled` status. The other three payload Jobs succeeded and the final gate was cancelled. These conclusions differ by grain and must be preserved together.

**Correction:** use approved public evidence paths (`docs/provenance/`, `docs/lessons/`, `tests/`) and register added Markdown in `evidence/profiles/docs.json`. Review root-path additions separately rather than widening path guards or rewriting frozen JSON to obtain green checks. PR #74's successful repair cannot erase the failed intermediate Job.

**Independent falsifier:** compare the exact previous 807 Run IDs against the current 849-ID set; enumerate the 42 genuinely new Run IDs and each returned latest-attempt Job. Do not treat ten cancelled Runs as ten failures or ten successes. Keep the 1 failed Job nested within a cancelled parent, 3 conditional skips, original failed Run records, and UNKNOWN cancellation/retention causes.

**Scientific and timing boundaries:** a positive repository-path test is not a bioinformatics computation; `SOURCE_MATCH` is not scientific truth; HTTP-only institutional checks are not certification; a nominal UTC cron vs GitHub `created_at` gap does not prove a dispatch or queue mechanism; an absent external provider check cannot support a new registration claim.

**Repeatable action:** PIN main and historical archives → QUALIFY allowed paths and evidence authority → EXECUTE read-only Run/Job census → EVALUATE source-aligned sets and Jobs → AUDIT negative evidence → REVIEW the public document registry and pull-request gates → REPLAY with the offline regression, leaving formal `data/` and the three assets unchanged.
