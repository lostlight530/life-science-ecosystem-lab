# Public lesson · a closed, green branch is not an accepted research revision (2026-11-07)

[Source-pinned Run and Job identities](../provenance/post-758-to-768-observation-2026-11-07.json) · [Reconciliation](../provenance/POST_758_TO_768_RECONCILIATION_2026-11-07.md)

**Observed failure mode:** PR #67 closed without merge on 2026-11-06 16:21:39 UTC (2026-11-07 Asia/Shanghai). Its two later Evidence push Runs (42249767693, 42251678739) succeeded on the independent `maintenance/2026-11-07-osf-registration-and-file-governance` branch. Those runs do not prove a PR review gate, integration on `main`, acceptance of its 16 changed files, an OSF registration or an approved research study. The PR title calls its work out of scope; its actual closure rationale is not independently established by a reviewer comment

**Correction method:** compare the current Git tree and exact PR `merged_at`/state with Run `head_branch`, `head_sha`, event and per-Job conclusion. Count historical PR #29, #32 and #67 as closed-unmerged while retaining their original existence and proposed changes. A green branch CI signal must not be promoted into Git-accepted software, scientific authority or external-provider status

**Continuity distinction:** the additional scheduled Continuity Run 42215956253 verified the four accepted Knowledge events and source-cited 17-node/26-relation graph, without creating a fifth formal receipt. Its nominal 04:17 UTC cron and 12:12:59 UTC GitHub `created_at` differ by 07:55:59; that is not measured runner queue time or proven scheduler fault

**Replay discipline:** anchor old 758 Run identities, derive the ten new IDs by set difference, verify 19 successful Jobs and one explicitly skipped Bio `pinned-field` Job. Keep previously disappeared failed Run IDs in their frozen records. A reported total without identity-preserving reconciliation can conceal real failures or duplicate accepted-state claims

**No authority change:** no formal `data/` edit, workflow schedule change, software asset change, framework change, external account operation or scientific claim is made by this audit
