# OSF Registration / preregistration readiness crosswalk · source-reviewed 2026-11-07

[Registration preparation](README.md) · [Case-neutral study plan](RESEARCH_STUDY_PLAN_TEMPLATE.md) · [Project method](../RESEARCH_METHODOLOGY.md)

**Status: `NOT_SUBMITTED`, `NO_OSF_REGISTRATION_ID_VERIFIED`**. This is an internally authored crosswalk based on OSF's [registration guidance](https://help.osf.io/article/330-welcome-to-registrations) and [template metadata description](https://osf-partner-support.helpscoutdocs.com/article/519-cor-template-basics), not a replicated official OSF schema or a validation result from OSF

## Critical timing disclosure

Research-software development and source observations in this Git repository were already underway on **2026-10-16** and the four accepted Knowledge snapshots were produced on **2026-10-17, 10-19, 10-26 and 11-02**. Earlier demonstrations, corrections, Actions Runs, benchmark-style synthetic challenges and source inspections must be marked **pre-existing / retrospective**. They must not be declared unknown future outcomes in a preregistered confirmatory analysis

Prospective preregistration is only defensible for a separately frozen *future study* with genuinely unobserved relevant outcomes and pre-committed design and analysis. OSF also permits registrations for ongoing or completed research when their temporal status is disclosed, but those do not become prospective by backdating a Git file

## Official fields and this repository's evidence

| OSF guidance dimension | Source-anchored local material | Readiness and unresolved contract |
| --- | --- | --- |
| Title, description, category, subject, tags | This repo's `README.md`, `docs/SCOPE.md` | **STUDY_SPECIFIC_PENDING**; repository title is not automatically the study's title |
| Contributors and affiliations (if applicable), licensing | `CITATION.cff`, `LICENSE`, `codemeta.json` | **REVIEW_REQUIRED**; contributors and affiliations must be authorized and accurately attributed for *this* study |
| Study status and timing | Historical Git root, [complete history](../taxonomy/README.md), [native receipts](../PRODUCTION_OPERATIONS.md) | **HISTORICAL_DISCLOSURE_REQUIRED**; exact future plan freeze and relevant outcome-blinding must be documented |
| Research question(s) and falsifiable hypotheses or explicitly exploratory objectives | [Eight-stage contract](../RESEARCH_METHODOLOGY.md) | **STUDY_SPECIFIC_PENDING**; the invariant method is not a biological hypothesis |
| Design, observational/simulation/experimental unit, eligibility and sampling frame | Replaceable case profile and [evidence replay](../EVIDENCE_REPLAY_PROTOCOL.md) | **STUDY_SPECIFIC_PENDING**; source/example fixtures are not a sampled population |
| Primary/secondary outcomes, variable operationalization, instruments | Three independent asset interfaces and planned case-specific records | **STUDY_SPECIFIC_PENDING**; SOURCE_MATCH edges are not verified biological outcomes |
| Exclusion, data-quality, missingness, conflicts, stopping rule and deviations | Source qualification and fail-closed methods in [provenance policy](../PROVENANCE.md) | **STUDY_SPECIFIC_PENDING**; identify measurable and pre-declared rules |
| Planned analyses and decision thresholds, effect estimates and uncertainty | [Framework challenge](../../framework/docs/CONTRACT_CHALLENGE.md) is an *existing software demonstration* | **STUDY_SPECIFIC_PENDING**; do not invent sample sizes, p-values, comparators, performance targets or tests |
| Computing environment, version pin, data provenance and replay plan | Git SHAs, structured provenance, [maintenance](../MAINTENANCE.md) | **REUSABLE_CAPABILITY_EXISTS**; freeze an actual study version and specify dependencies |
| Data permissions, privacy and release/embargo decision | [Scope and security](../SCOPE.md) · [Security](../../SECURITY.md) | **STUDY_SPECIFIC_PENDING**; no private clinical/personal data or unlicensed upstream datasets by default |
| Planned vs exploratory analyses, negative findings and amendments | [Claim review](../CLAIM_VERIFICATION_GAPS.md) · [replay protocol](../EVIDENCE_REPLAY_PROTOCOL.md) | **PROCEDURE_EXISTS**; case-specific predecision + subsequent amendment record still needed |
| Actual OSF template selection, account-side submission, Registration URL/DOI | Official OSF provider | **NOT_SUBMITTED / NOT_VERIFIED**; never synthesize a URL, identifier or registration approval |

These columns map *requirements and reusable evidence*, not an assertion that the actual OSF Preregistration questionnaire is filled or platform-validated. Form selection is case-dependent (e.g. OSF Preregistration, Open-Ended, Simulation Studies, Secondary Data) and must follow the current template shown in the actual OSF Registration workflow

## Pre-submission falsifiability gate

A reviewer must be able to answer **all** of these in the frozen study-specific draft before submitting:

1. What independent claim is being tested, what would refute it, and what is excluded from the claim
2. What were the study's first relevant observations/analyses and was this plan genuinely fixed before those observations
3. Which versioned inputs, permissions, units, sample size or stopping rules, inclusion/exclusion rules, primary outcome and comparator are committed in advance
4. Which methods, decision thresholds, uncertainty estimates, negative controls and missing-data contingencies will be used *without choosing after looking at outcomes*
5. Which observed results are already known, what analysis is confirmatory versus exploratory, and what amendments would be publicly dated
6. Which human contributors approve the actual study plan, and which OSF provider record (if any) confirms submission, later approval and updates

**Fail closed:** an unanswered dimension remains `TBD` in the local planning template, not silently `PASS`. A valid software CI test cannot declare a future OSF study preregistered

## OSF 2026 service boundary

OSF Projects will no longer accept new Project/Component creation after 2026-11-16 and become read-only on 2027-02-19, while Registrations continue. Registration attachments cannot simply be overwritten to rewrite an original research plan; OSF supports dated registration updates and linked research outputs. See [official transition](https://help.osf.io/article/759-details-of-osf-projects-transition) and [OSF guide](https://help.osf.io/article/330-welcome-to-registrations)
