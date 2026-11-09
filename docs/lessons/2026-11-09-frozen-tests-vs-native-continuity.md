# Public lesson · a frozen audit must not cap future accepted production (2026-11-09)

[Bounded GitHub review](../provenance/POST_788_TO_798_RECONCILIATION_2026-11-09.md) · [Source-pinned observation](../provenance/post-788-to-798-observation-2026-11-09.json) · [Offline falsifier](../../tests/test_post_788_run_delta.py)

**Observed failure mode:** an offline audit stored four accepted Knowledge Receipts and four events at its November 8 cutoff, then asserted that the *moving working tree* must always have exactly four. After an authorized scheduled native lifecycle accepted a fifth event on November 9, those assertions were stale even though the event hash chain, archival lineage and state validators passed

**Minimal repair:** preserve the original four-event prefix and immutable old Receipt Git Blob hashes; treat previous mutable `data/knowledge/current.json` and graph-manifest Git hashes as version-specific evidence, not permanent live expectations. Test the fifth acceptance's Receipt and chained event independently, while permitting future native appends. Do not modify accepted `data/` to make a frozen test pass

**Independent job-gate observation:** of the ten newly visible Runs, all ten succeeded, but one main-branch Bio `pinned-field` Job was intentionally skipped under its `push` condition. The Monday scheduled Knowledge run passed both validation and guarded apply; the downstream continuity schedule independently passed, without converting `DOCUMENT_TEXT_UNCHANGED` into a scientific discovery

**Clock and causality:** November 9's self-check, Knowledge and continuity Runs were created 06:58:54, 08:23:49 and 08:42:53 after nominal cron respectively. These are Run creation offsets, not measured queue times; without causal evidence the reason remains **UNKNOWN**

**Governance:** historical disappeared failures, unmerged PRs, external registry assertions and earlier reports stay available for review. Fix the frozen-versus-live test contract via PR and passing CI rather than force-pushing, rewriting Git history, changing production schedulers or manufacturing new findings
