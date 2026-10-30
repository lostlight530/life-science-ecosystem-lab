# Public research-software experience: time-scoped evidence and runtime quality

[Post-merge exact recheck](../provenance/POST_MERGE_RECHECK_2026-10-30.md) · [Earlier error taxonomy](2026-10-30-error-detection-and-audit.md) · [Eight-stage scientific method](../RESEARCH_METHODOLOGY.md)

**Published after privacy minimization, 2026-10-30.** No private conversations, personal biographies, contact information, precise location, Agent prompt text, account details, secret values, unpublished correspondence or unverifiable identity attributions are included.

## Repeatable lessons grounded in public sources

1. **API census is time-bound:** 531 visible runs in one snapshot and 531 in another did not mean the IDs were identical; a later snapshot contained 547 IDs. Use set reconciliation keyed by immutable Run ID, not total-count subtraction alone. Keep earlier failure evidence in version control even when later API listings omit it
2. **A stable numeric workflow ID can have multiple historic names:** reconstruct time-specific names from individual Run objects; a single ID-to-current-name lookup created 134 incorrect historical labels in an earlier report
3. **Green structural CI is not a proof of correct statistics:** sorted 28-run source data contradict two originally published medians, which must be corrected through a derived and testable projection rather than rewriting the original observation
4. **Success and execution coverage differ:** one completed Bio workflow's field Job was `skipped` while its offline Job succeeded. Report each Job's status and do not translate conditional nonexecution to field-research success
5. **Cron offset is not causal attribution:** comparison of intended UTC cron to GitHub run creation is informative but cannot prove queue delay, dropped dispatch, platform defect or execution start. Do not call a partial day's not-yet-visible run a failure
6. **Accepted research state is not CI activity:** three genuine Knowledge Git acceptance receipts differ from 28 successful scheduled runs and 547 visible Actions runs. Source-version movement without text change is not scientific novelty
7. **Negative evidence must remain visible:** the first historical eight failed runs and later unrecoverable observations must survive subsequent green samples, while missing Run IDs never justify guessing a deletion actor or motive
8. **Keep research artifacts and private context separate:** publish public Run IDs, SHA, observation clocks, reproducer, non-sensitive diagnostic summaries and uncertainty; exclude private personal and third-party records

## Contract for future auditors

At each observation, record UTC time, reference main SHA, complete pagination, exact Run IDs, query URLs, final conclusions, observation grade, loss/retention caveats and distinction between scheduled, manual, PR and push. For real production, require an actual Git commit and accepted `data/receipts`. For numerical summaries, recompute from primary per-run observations and include denominator and rounding.

Use independent tests as falsifiers. Rejected or unknown outcomes belong in the evidence record. Do not equate an Agent self-description with verified execution, a passing test with science, or an external registry link with certification.

**Outcome:** a reusable evidence-governance case study and additive archival correction, not a claim of biological discovery, external institutional approval, full historical Runner-log recovery or an implemented change to any core software asset.
