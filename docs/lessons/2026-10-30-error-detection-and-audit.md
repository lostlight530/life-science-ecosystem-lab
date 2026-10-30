# Research software lessons · 2026-10-30

**Public, privacy-minimized engineering experience** · [Origin-to-current evidence](../provenance/RECONCILIATION_2026-10-30.md) · [Native daily run quality](../provenance/NATIVE_DAILY_QUALITY_2026-10-30.md) · [Eight-stage lifecycle](../RESEARCH_METHODOLOGY.md)

## Scope and privacy boundary

This is a reusable learning record from an open-source research-software review. It intentionally omits personal biography, contact information, personal locations, private conversations, Agent account details, unpublished session prompts, secrets, nonpublic institutional data and speculative attribution of events to named people. Links refer only to public repository PRs, public GitHub metadata or official documentation. Contributor self-identification is not required to repeat the method.

**Claim to test:** Can research software expose its own contract defects, preserve contradicting historical observations and distinguish operational continuity from scientific knowledge production?

**Boundaries:** This record tests *software assurance and research evidence governance*. Neither a failed test nor a later successful test proves protein structure accuracy, registry recognition, method transfer validity, or any biological scientific proposition.

## Error discovery is a multi-mechanism process, not a red-run count

| Class | How the error is exposed | Concrete public example | Status and limits |
| --- | --- | --- | --- |
| Invariant violation | A pre-existing executable assertion computes an observed state and compares it to a versioned admissible state | [PR #40](https://github.com/lostlight530/life-science-ecosystem-lab/pull/40) and [PR #43](https://github.com/lostlight530/life-science-ecosystem-lab/pull/43): documentation set mismatch | GitHub Job logs were observed; some failed-run logs later became unqueryable |
| Exact primary-evidence recheck | Re-read original bytes or primary artifact, then recompute expected digest | [PR #10](https://github.com/lostlight530/life-science-ecosystem-lab/pull/10): two earlier field checksum records corrected against original artifact | PR reports the correction, not an independent claim that every upstream artifact is retained forever |
| Negative/adversarial cases | Construct forged identities, malformed dates or incomplete lineage that must be rejected | [PR #8](https://github.com/lostlight530/life-science-ecosystem-lab/pull/8); [PR #30](https://github.com/lostlight530/life-science-ecosystem-lab/pull/30) | Synthetic negative evidence tests software rejection, not real-world scientific accuracy |
| Semantic counterexample | Compare a published metric definition to a minimal counterexample | [PR #38](https://github.com/lostlight530/life-science-ecosystem-lab/pull/38): one-input cross-domain output omitted from cross-domain step count | Corrects a *declaration metric*, not a claim of actual cross-omics execution |
| Fault injection | Simulate an output replacement failing and check preservation of pre-existing report | [PR #39](https://github.com/lostlight530/life-science-ecosystem-lab/pull/39): staged JSON output / atomic replacement | A simulated failure does not prove that production data corruption occurred |
| Longitudinal causal reconstruction | Pin successive accepted states and source digests, compare transitions, then trace the implementation predicate | [PR #41](https://github.com/lostlight530/life-science-ecosystem-lab/pull/41), [PR #42](https://github.com/lostlight530/life-science-ecosystem-lab/pull/42) | Establishes why metadata-only ACCEPT happened; whether it is desirable remains undecided |
| Independent governance review | Compare proposal assertion with external Git or registry authority and retain a corrected/unknown decision | [Agent decision ledger](../AGENT_REVIEW_DECISIONS.md) | Merge is not independent scientific recognition |
| Cross-snapshot evidence loss | Compare two dated API censuses by unique ID rather than trusting today's totals | [Actions reconciliation](../provenance/action-run-reconciliation-2026-10-30.json) | A vanished run and HTTP 404 do not identify deletion actor or cause |

## Two directions of the same documentation-contract test

A pre-existing repository test compares the **exact** set of approved public Markdown paths discovered under its enumerated direct-child directories against the paths declared by the governed documentation inventory

- **Omission:** a new public document exists in the scanned set but is not registered. The first eight observed failures in the October 29 UTC evidence workflow used this failure pattern. Repeated changes that did not correct the inventory recreated the same assertion
- **Overinclusion:** a nested `docs/provenance/README.md` was erroneously included in the registered set although the test enumerated only direct Markdown children of specific directories. A later PR drafting attempt generated three more failures with this inverse pattern

**What detects both:** `test_public_documentation_inventory_is_complete` is executable, objective and already existed before these particular changes. The test does not need to trust an Agent's claim about document completeness. Corrections modify the data/inventory, not the detector's oracle.

**What remains weak:** Evidence and Bio workflows both ran the *same repository-wide test*, so two red workflow labels are **not** two independent defect oracles; eleven failed runs are **not** eleven independent scientific experiments. A failure trend may reflect repetitive development rather than scientific progress.

## Two observations, one historical truth boundary

At an initial fixed cutoff the repository stored 531 public Actions records: 483 success, 8 failure, 40 cancelled. A later independent live API enumeration returned 531 *different* objects: 490 success, 0 failure, 41 cancelled. An exact set difference finds eight earlier failures not present in the later list and eight newer runs present there. Three additional intervening failed runs were previously inspected but lack a committed raw-log archive. They are preserved explicitly as **lesser-grade observer notes**, not upgraded to primary repository evidence.

**Methodological consequence:** An API response is evidence for *what the API returned when observed*, not a guarantee that its history will remain available. Retain old signed or commit-addressed snapshots, compare rather than overwrite, and archive lawful non-sensitive failure excerpts with provenance when authorization and licenses permit. Current GitHub APIs document deletion of completed workflow runs, but a vanished record does not establish who deleted it or why.

## Testable corrections to the operating method

1. **Preflight before remote commit:** check existing repository invariants, especially documentation manifests, link destinations, governed profile boundaries and offline tests before any new branch push
2. **Stop after first identical failure:** capture the exact assertion and its input state once; do not produce repeated commits until the hypothesized root cause has changed
3. **Use discriminating regression:** choose two opposed negative controls (missing entry and extraneous entry), plus a correct set, to test whether the detector rejects precisely the contract violations
4. **Separate operational observations:** scheduled / manual / push / PR, success / failure / cancelled, generated artifacts / true `APPLIED` receipts, source-text changes / provenance-only changes
5. **Record evidence tier:** direct immutable bytes and Git history; time-stamped primary API objects; independently executed replay; unarchived direct observation; secondary self-report; unknown
6. **Test uncertainty openly:** `NOT_OBSERVED`, `NOT_DUE`, `UNVERIFIED`, `NO_MEANINGFUL_DELTA`, `INDETERMINATE`, `REVISED` and rejected proposals must not be silently recoded as `PASS`
7. **Require authority at the boundary:** a scientific conclusion still needs a domain oracle, method applicability check, independent evidence and human decision; GitHub CI is not the certifier
8. **Preserve non-causal language:** a delayed schedule may be consistent with documented GitHub load, but a nominal-versus-observed time difference alone cannot prove queuing or external outage

These are reusable **research-process hypotheses and safeguards**, not a claim that all eight are already automatically enforced in every repository or by the GitHub server. Particularly, `main` was observed `protected=false` with no rulesets, which is a separate governance limitation; this review did not change settings.

## Qualifying future evidence — the eight-stage worksheet

| Stage | Minimal reproducible record | A result that must be allowed |
| --- | --- | --- |
| DEFINE | Narrow question, expected contract and falsifier | Inapplicable |
| PIN | Revision, source digest, actual observation clock and software version | Original bytes unavailable |
| QUALIFY | Source license, trust scope, independent comparator and exclusions | Rejected / insufficient |
| EXECUTE | Specific run/job ID, command, permission scope, environment and immutable inputs | Failed / cancelled / not attempted |
| EVALUATE | Measured output, counterexample and uncertainty | Negative / no meaningful delta |
| AUDIT | Exact original artifact or explicitly lower-grade record, retention limit and status history | Historical gap |
| REVIEW | Reviewer rights, contrary interpretations and decision timestamp | Deferred / disputed |
| REPLAY | Offline deterministic reproduction or independently sourced repeat, compared at the same granularity | Reproduction fails / cannot be completed |

**Promotion rule:** Software correctness, evidence validity, method applicability and scientific truth are four different obligations. A result can validly pass one and remain unknown in another.

## Falsifiers for this experience record

- If historical raw logs, when recovered, reveal another failure assertion, revise the two-pattern attribution and retain both versions
- If the exact primary run IDs become queryable again, revise the *current absence* claim at the new observation time without overwriting the original observation
- If an independent reviewer finds a different root cause or the documentation-contract test does not reliably reject both directions, amend the mechanism description
- If independent biological or cross-domain test cases show the methods inapplicable, preserve the negative transfer result rather than lowering standards to manufacture success

This page is **append-only learning**, not a runtime instruction, institutional standard, agent identity attestation, acceptance receipt, publication approval or proxy for `data/` truth

## New self-falsification case: a green archival PR can still be quantitatively wrong

An independent follow-up on the same archived observations found **134 incorrect historical run labels**, caused by joining mutable display names using only a stable GitHub workflow ID, and **two incorrect medians**, caused by not independently sorting the entire scheduled-run group. See [the source-graded erratum](../provenance/RUN_NAME_AND_MEDIAN_ERRATUM_2026-10-30.md). This is neither a platform outage nor a biological computation failure: it is an error in *our own evidence transformation*. The correct response is to retain the flawed dated index as historical evidence, publish exact Run-ID-based corrections and predeclare new offline assertions rather than erase the discrepancy.
