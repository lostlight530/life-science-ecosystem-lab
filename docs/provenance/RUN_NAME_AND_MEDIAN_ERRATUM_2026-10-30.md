# Independent audit erratum — historical run identity and median statistics

[Reconciliation](RECONCILIATION_2026-10-30.md) · [Corrected per-run machine evidence](run-name-attribution-audit-2026-10-30.json) · [Daily native quality](NATIVE_DAILY_QUALITY_2026-10-30.md) · [Public lessons](../lessons/2026-10-30-error-detection-and-audit.md)

**Additional observation:** 2026-10-30T01:03:32.972Z UTC, original review baseline `ab56cd79f5532623c2043f5b18f744b159f39aa3`. This document is a subsequent, privacy-minimized correction of a prior analysis, **not** a replacement for either immutable Actions observation. No actor names, personal data, secret values, private sessions or raw runner logs.

## Claim A — a stable workflow ID does not imply a historically stable name

The 531-row compact run index used a `workflow_names[workflow_id]` dictionary reconstructed from the first observed label. This loses temporal identity: the same workflow ID **386580410** appeared under three names as the repository evolved.

Comparing each exact run ID against the earlier full API snapshot, or against the later public Run API for the eight post-freeze rows, shows:

| Stored compact-index name | Individually verified run name | Inaccurate rows |
| --- | --- | ---: |
| `Validate pilot contracts` | `Validate life-science workflow and evidence contracts` | 132 |
| `Validate pilot contracts` | `Validate computational workflow and evidence contracts` | 2 |
| Correctly matched rows | Original run name | 397 |

The original source contributes **523** run names; a later public API observation contributes the other **8**, without attributing the later observation to the earlier clock. The [JSON audit](run-name-attribution-audit-2026-10-30.json) preserves all 531 run-ID/name pairs, exact source grades and 134 identified mismatches. The flawed original index remains unchanged for historical fidelity.

**Falsifier:** If a pinned source Run ID's source `name` differs from the corrected per-run entry, that correction is invalid. The offline regression checks every frozen-API Run ID and reconstructs the mismatch population. This is evidence of an **analysis transformation error**, not an error in GitHub's actual workflow execution.

## Claim B — green CI did not detect two incorrect descriptive medians

The original report treated an observed value as a median without independently sorting the full relevant population.

| Scheduled category | Actual observations | Previous reported median | Independently recomputed median |
| --- | ---: | ---: | ---: |
| Knowledge weekly native | 2 | 340.25 minutes | **342.01 minutes** |
| Daily dual-plane self-check | 12 | 295.77 minutes | **302.41 minutes** |
| Daily continuity | 13 | 311.38 minutes | 311.38 minutes |
| Weekly Bio | 1 | 314.35 minutes | 314.35 minutes |

The two-value median is the midpoint of **340.25** and **343.77**; the twelve-value median is the midpoint of the sixth and seventh values in sorted order. The [daily report](NATIVE_DAILY_QUALITY_2026-10-30.md) now shows corrected figures. Run IDs, timestamps, nominal cron, original observations, accepted receipts and production `data/` are unchanged.

These offsets compare GitHub API `created_at` with the configured cron instant. They are **not independently verified queue-start latency or evidence of GitHub platform failure**.

## Why this is a scientific software-method result, not scientific truth

A structurally valid machine-readable index can contain invalid semantic joins. A green unit-test suite can allow incorrect reported statistics if those assertions were never included in its tested contract. This additional review is a genuine independent falsification of two claims in the preceding report, and a traceable correction of source attribution.

The fixed eight-stage method applies: **DEFINE** the identity and median claims → **PIN** exact original run IDs → **QUALIFY** distinct observation clocks → **EXECUTE** per-ID source join and sorted recomputation → **EVALUATE** 134 mismatches/two arithmetic defects → **AUDIT** a new append-only JSON correction → **REVIEW** the correction via PR → **REPLAY** the offline tests.

Do not use this evidence as biological validation, external institutional certification, Agent identity attestation or authorization to change the native research workflow.
