# Public lesson · green current census can conceal genuine historical failures (2026-11-06)

[Identity-preserving machine census](../provenance/post-750-to-758-observation-2026-11-06.json) · [Reconciliation](../provenance/POST_750_TO_758_RECONCILIATION_2026-11-06.md)

**Failure mode:** a stored prior GitHub API census reported 750 Runs, including four PR #64 validation failures. The latest eight-page API result contains 758 Runs and zero currently visible failures, but this is **not** eight new executions. Reconstructing all prior 750 IDs and comparing with all current 758 identifies exactly **12 new successful Run IDs and four prior failed Run IDs currently missing**; each of the four direct lookups returned HTTP 404

**Correction:** record the immutable prior snapshot, the exact absent IDs, the current ID population, the independently observed Job conclusions and the fact that the 404 cause remains UNKNOWN. Do not overwrite the old failed counts, or retroactively label absent objects as never executed

**Scheduling boundary:** Friday Bio and daily self-check succeeded with separate Job and Artifact identities, despite long differences between nominal cron and GitHub API created time. Green workflow status, exact scheduling, upstream availability, Bio FASTA uncertainty warnings and independently validated science are different facts

**Repair discipline:** derive Run identity deltas with set difference, not total-count subtraction; preserve old failures and negative evidence; test exact identities offline; do not mutate `data/`, agents' claimed identities, official registry metadata or native workflow scheduling to manufacture continuity
