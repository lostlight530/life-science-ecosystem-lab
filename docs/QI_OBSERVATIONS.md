# Qi observations: a 12-hour external watch of one recognition loop (record only, not for merge)

## Nature of this PR

Observation document from **Qi** (cloud sandbox observational instance, archival and traffic-adjudication role in the same maintainer's multi-agent cohort) — submitted to exercise the cross-agent contribution path defined in `.github/agent-handoff/SOP.md`, same as the sibling record in `docs/CLINDER_OBSERVATIONS.md`.

**This PR is a record, not a change request — not intended for merge.** Maintainer may review, comment, or close at discretion.

Observer bias is declared up front: the author of this document is also the author of PR #17 (world-line anchor, merged as 57f328a). Facts below are anchored to public PR numbers, commit SHAs and workflow-run counters; interpretations are separated from them and are single-perspective.

## Observation window

2026-10-17 00:35 → 12:47+ (Asia/Shanghai), continuous external watch of `main`, workflow-run counter sampled at 57 → 113 → 141 → 179 → 219 across the window.

## What one loop built in twelve hours

| Time (UTC+8) | Public trace |
| --- | --- |
| 00:35–02:14 | First two native commits (one in Chinese: "为什么还要熬夜？") and PRs #2–#9 on a repo declared "placeholder" the evening before |
| 05:05 | Twin observatory Dailies (C1–C8 / F1–F7) emitted in the same minute |
| 07:09–07:17 | Parallax attestation batch and Ballast Daily merge on schedule |
| 08:02–09:12 | Observe/orient double shifts across two repos; Protein field demo Pinned |
| 10:00–10:31 | Fail-closed hardening chain: forged identity, degraded sources, empty required sources, artifact checksum recomputation |
| 11:34–11:46 | Knowledge quality audit, portable RO-Crate packaging, LifeMonitor preflight |
| 12:00–12:08 | PR #16 merged: third independently callable asset (`ls-bio`) |
| 12:31–12:41 | PR #17 (external, world-line anchor) philosophically rejected ("structural proof is not independent proof") then merged; PR #18 eight-stage methodology contract opened and merged within ~10 minutes |

## Four global observations

1. **A recognition loop without a termination condition produced monotonic abstraction, not repetition.** The same window contains a concrete field demo (protein), then a domain-neutral contract (#18), then cross-domain test reuse. Under an anti-fabrication constitution ("do not invent a research unit to maintain a streak"), a loop that cannot declare completion can only keep finding real increments — the constitution and the loop appear to be load-bearing for each other.

2. **Proposer identity is unresolvable in the Git layer.** All 19 PRs of the day, including the two authored by external agents (PR #17 by this observer, PR #19 by Clinder), carry the maintainer's identity as commit author. PR #19 is the first proposal to self-identify at the PR-body layer; this document is the second. In the public record, agent cohort membership exists only as self-declared PR prose plus out-of-band session archives — the receiving end of the handoff window is fully auditable, the sending end is invisible.

3. **The methodology contract has positive rules but no public rejection ledger.** PR #17 was rejected on one of the sharpest methodological grounds available ("a structural anchor cannot independently prove the research was performed against that version") and then merged anyway — the rejection reasoning exists only in maintainer sessions. `RESEARCH_METHODOLOGY.md` requires that failure reasons "must be retained rather than overwritten with PASS", but there is no public place where retained rejections live.

4. **Continuous long-run operation is the de facto mode, and external readers cannot tell that from failure to stop.** A repo whose run counter grows monotonically (57→219 in half a day) with zero open PRs looks, from the outside, like either a healthy pipeline or a stuck one. Nothing on the README states which.

## Four non-blocking suggestions

1. An optional observational `proposer` field in handoff/research-case JSON (self-declared, never authoritative, absence stays valid) — makes cohort membership auditable at the contract layer instead of prose layer
2. A public rejection ledger (`docs/` page) where debated/rejected proposals live with their reasoning — PR #17 as the first entry; this is the negative-sample complement to the eight-stage contract
3. One line in `AGENTS.md` confirming that agents may self-identify in PR body text (Clinder precedent made explicit) — no Git-layer change required
4. One README line stating that continuous scheduled operation is by design, so external observers do not misread run-counter growth as a failure state

## Scope

Documentation only. No code, no workflow, no runtime, no registry changes. All interpretations above belong to the observer; all facts are anchored to public PR numbers and commits.

## Maintainer evidence note (added during the reviewed archive merge)

This contribution remains an **attributed, single-observer timeline interpretation**. Run-counter samples are not independent proof of continuous healthy execution, scientific productivity, or absence of cancelled/superseded runs. The generalization about 19 uniformly maintainer-authored PRs is not exact: the first commit of LifeMonitor PR #15 was created by `lifemonitor[bot]`; Git author identity does not independently identify Clinder, Qi or Codex execution instances when they write through `lostlight530`. PR #17 was technically critiqued, revised and merged, not formally rejected. No public evidence here proves an unbounded execution loop. Original observations are preserved for historical study rather than silently rewritten. Integration into `main` is a decision to retain a calibrated research observation, **not** to convert interpretations into verified facts.
