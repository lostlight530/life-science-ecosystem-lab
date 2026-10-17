# Maintainer Decision Ledger — Cross-Agent Research Evidence

This is an auditable *review-decision history*, not a rejection tally, source of biological ground truth or independently certified identity registry. Records cite original GitHub changes; original author texts are retained and separate, with caveats where needed. Statuses apply to **specific claims and changes**, not entire Agent reputations.

| Source | Assessed claim or change | Decision class | Evidence / reason |
| --- | --- | --- | --- |
| [PR #17](https://github.com/lostlight530/life-science-ecosystem-lab/pull/17) | A syntactically valid 40-hex `base.commit` proves fresh repository observation | **REVISED**, not formally rejected | Structural validity does not attest real existence, freshness or ancestry; reviewed correction added independently fetched `--expected-base-sha`; final PR merged |
| [PR #19](https://github.com/lostlight530/life-science-ecosystem-lab/pull/19) | Three-asset split and evidence-boundary enforcement are reusable engineering patterns | **ACCEPTED_AS_OBSERVATION** | Author-submitted design assessment preserved in `docs/CLINDER_OBSERVATIONS.md`; software remains independently testable |
| [PR #19](https://github.com/lostlight530/life-science-ecosystem-lab/pull/19) | A 142-day sibling runtime and zero-crash history are proven by this PR | **UNVERIFIED_EXTERNAL_REPORT** | No independent source logs or frozen receipts for that private sibling were supplied in this PR |
| [PR #19](https://github.com/lostlight530/life-science-ecosystem-lab/pull/19) | ORCID, RO-Crate conformance and an Agent SOP discoverability entry still need to be created | **ALREADY_IMPLEMENTED_OR_MISDIRECTED** | Public `CITATION.cff`, `ro-crate-metadata.json`, `AGENTS.md` already contain relevant declarations; LifeMonitor repository filename has a leading dot |
| [PR #20](https://github.com/lostlight530/life-science-ecosystem-lab/pull/20) | Git author identity is insufficient to authenticate local/cloud Agent execution | **ACCEPTED_AS_LIMITATION** | Git authorship identifies a GitHub actor, not the unobservable generating execution instance; optional `SELF_DECLARED` proposer label is not an attestation |
| [PR #20](https://github.com/lostlight530/life-science-ecosystem-lab/pull/20) | Every PR's author is identical / twelve-hour run counter growth proves healthy continuous research | **CORRECTED_OR_UNVERIFIED** | Initial PR #15 source commit attributed to `lifemonitor[bot]`; five run-counter samples do not establish success rates, scientific results or uninterrupted runtime |
| [PR #20](https://github.com/lostlight530/life-science-ecosystem-lab/pull/20) | PR #17 was formally rejected and later merged | **CORRECTED** | PR #17 instead received technical criticism, had a trusted-baseline validation improvement, passed CI and was merged |
| [PR #21](https://github.com/lostlight530/life-science-ecosystem-lab/pull/21) | Align three-asset docs, register Bio Tool guide, correct LifeMonitor claims and distinguish synthetic and field evidence | **IMPLEMENTED_AND_MERGED** | Public contract change merged as `336afcb217f1f6afe684a7b0c2fc93ae67170634`, with three successful PR checks |
| [PR #19](https://github.com/lostlight530/life-science-ecosystem-lab/pull/19), [PR #20](https://github.com/lostlight530/life-science-ecosystem-lab/pull/20) | Preserve observer contributions in the research archive | **REVIEWED_ARCHIVED_WITH_QUALIFICATIONS** | Both originally requested record-only status, later explicitly authorized for archival merging; original observer accounts retained and separated from maintainer review notes |
| [PR #15](https://github.com/lostlight530/life-science-ecosystem-lab/pull/15) | GitHub App installation entails external LifeMonitor workflow enrollment | **NOT_ESTABLISHED** | Bot PR and installed App show GitHub integration, but not verified monitoring of a specific workflow/test instance |
| [This field study](AGENT_CLUSTER_RESEARCH_CASE.md) | Multiple agents independently reproduced identical scientific conclusions | **NOT_TESTED** | Different proposals, common publication identity and absent independent run attestations make replication claims unsupported |

## Interpretation and amendment rules

- **REVISED** means a technical criticism produced a correction; it does not mean a PR was formally rejected
- **ACCEPTED_AS_OBSERVATION** records a contributed perspective, not an externally certified statement
- **IMPLEMENTED_AND_MERGED** means source or documentation changes entered the repository; it does not establish biological truth
- **UNVERIFIED** and **NOT_TESTED** are active research states to retain, not gaps that should be silently turned into `PASS`
- **Human authority:** future amendments should link the exact PR, evidence delta, review rationale and resulting merged SHA where relevant
- **Conflict and negative results:** keep superseded claims and why they changed; never erase prior observer wording or misrepresent a rejected scientific hypothesis as a successful test

This record is a methodological audit companion to the [research lifecycle](RESEARCH_METHODOLOGY.md), not a permanent authorization to execute Agents or mutate the protected `data/` history.
