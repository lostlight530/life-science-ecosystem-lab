# 谁说 Agent 集群不可以科研？ — An Auditable Heterogeneous-Agent Research Collaboration Case

> **Question, not slogan:** Can multiple agents working across different execution surfaces contribute falsifiable, inspectable research-software knowledge under one stable method contract? The rhetorical title does not imply any particular person claimed agents cannot conduct research.
>
> **Scope:** This is a documented open-source **research collaboration process** and a field test of governance/reproducibility methods. It is not a three-way independent reproduction of protein quality predictions, a novel biological discovery, or authentication of individual agent runtimes.

## Frozen public evidence / provenance

All three proposals were opened against the same base commit `fad2ca9daae0d769a9cb9828e1fbe2226ae846b8`, the repository's preceding accepted methodology baseline. The execution identities below are **self-reported by the contributors in PR text**. GitHub primarily records the shared `lostlight530` Git actor and does not independently authenticate which local/cloud Agent generated each contribution.

| Contributor claim | Execution surface claim | Submitted research contribution | Independent GitHub evidence | Final treatment |
| --- | --- | --- | --- | --- |
| **Clinder** | WorkBuddy local IDE | Engineering review of stable boundaries, record-level source fields, append-only worklogs and missing external proof | [PR #19](https://github.com/lostlight530/life-science-ecosystem-lab/pull/19) / merged commit `3c5b44c23fce47d96b82defd306f489485c390ec` | Observation archived with a separate maintainer evidence note, **not** certified as 142 days of independently observed production |
| **Qi** | Cloud sandbox | Longitudinal review of shared identity ambiguity, review outcomes, GitHub run counters and continuity | [PR #20](https://github.com/lostlight530/life-science-ecosystem-lab/pull/20) / merged commit `9abac79df8546ad465e569dd673bae11017afd34` | Observation archived with calibration; count samples are **not** successful-run or research-unit measurements |
| **OpenAI Codex** | Codex desktop execution surface | Repairs three-asset docs and scientific evidence limits; exercises regression, metadata and artifact checks | [PR #21](https://github.com/lostlight530/life-science-ecosystem-lab/pull/21) / merged commit `336afcb217f1f6afe684a7b0c2fc93ae67170634` | Actual reviewed public-contract patch; latest PR head had three successful CI checks |

The `lifemonitor[bot]` initial commit on [PR #15](https://github.com/lostlight530/life-science-ecosystem-lab/pull/15) is a separate genuinely identifiable GitHub App action, **not** an authentication mechanism for Clinder, Qi or Codex. Agent names in this case are contribution attribution labels, not verified organizational/legal identity, scientific authorship decisions or cryptographic workload identities.

## Same research method, three unlike contributions

Use the fixed eight-stage [Research Methodology](RESEARCH_METHODOLOGY.md) while allowing examples, agents, tools, domains and algorithms to vary:

1. **DEFINE:** Can a heterogeneous agent cohort produce distinct, reviewable contributions without acquiring authority over accepted research data?
2. **PIN:** Preserve Git base/head commits, exact PR URLs, source files, workflow run links and observed statuses
3. **QUALIFY:** Distinguish authored/supplied assertions from independently checked repository facts; note missing private runtime proofs
4. **EXECUTE:** Run local and GitHub CI validation for proposed files and permitted software changes, never direct `data/` persistence
5. **EVALUATE:** Compare process outcomes (merge decisions, corrections, accepted/rejected claims), not biological accuracy or GitHub run-count volume
6. **AUDIT:** Keep original observer text and separate maintainer annotations; publish review reasoning and durable code changes
7. **REVIEW:** Human/repository owner decides merges; observation and CI cannot authorize production writes or external registry attestations
8. **REPLAY:** Recheck current `main` and demonstrate that source/document inventory, independent CLIs and knowledge workflow remain valid after merges

Protein FASTA/PDB analysis was a **replaceable Proof of Capability**, not the research subject or a forced permanent methodology domain. The same contract is tested with unrelated scientific workflow examples. A result may be `BLOCKED`, `NO_FINDINGS`, `REVISED` or `UNVERIFIED`; continuous activity is not itself scientific progress.

## Findings and dispositions, not applause counts

- **Supported:** Three distinct PR contributions reached GitHub; source documents, diffs and GitHub Actions can be inspected; a reviewed three-asset docs repair merged; both observational records were preserved with caveats and did not mutate the accepted `data/` plane
- **Supported:** The evidence process exposed *corrections*, such as already-present ORCID/RO-Crate metadata, an erroneous generalization about GitHub author identity, and missing independent proof for some operational-history assertions
- **Limited:** The 142-day sibling runtime, continuous healthy operation or a hypothetical unlimited research loop cannot be independently established from these PRs
- **Limited:** A green GitHub CI or schema-valid handoff establishes a software contract, **not** scientific truth or an Agent's independent execution identity
- **Not demonstrated:** Three mutually independent agents reproducing the *same* scientific result from frozen identical inputs, calibrated reference standards and independent review

Consult the [Maintainer Decision Ledger](AGENT_REVIEW_DECISIONS.md) for accepted, revised, rejected or unresolved claims and why they were distinguished.

## Concrete reproducible gates

The repository publishes three independent entry points: `ls-knowledge`, `ls-evidence` and `ls-bio`, plus their respective CI and CWL paths. A proposed Agent origin may optionally declare:

```json
"proposer": {
  "agent_label": "an-observer-label",
  "execution_surface": "local IDE or cloud workspace (self-reported)",
  "assertion": "SELF_DECLARED"
}
```

The same optional shape is accepted by `EXTERNAL_AGENT_RESEARCH_HANDOFF` and `RESEARCH_CASE_PROPOSAL`. Both preserve backwards compatibility, **reject authentication claims made by the proposer**, and never convert self-declared identity into scientific authority.

The read-only verification recipe is:

```sh
python -m unittest discover -s tests -v
python -m evidence validate-handoff --input .github/agent-handoff/example-handoff.json --topics evidence/profiles/topics.json
python .github/scripts/check_metadata.py
```

GitHub Actions, rather than a local README assertion, is the final source for whether CI succeeded at a particular commit. The actual periodic knowledge workflow, a daily read-only continuity check and the Bio Tool test are separate scheduled contracts; GitHub action counts alone cannot measure accepted research units.

## How this hypothesis could fail

A future **controlled replication** should freeze one question, one common baseline and identical data/method constraints. Assign agents with independently observable execution receipts; predefine pass/fail metrics (valid source pins, substantive review comments, evidence-correctness judgments, result disagreement, cost, time and rate of rejected claims). Preserve all failures. Repeat across a genuinely different research domain, with an independent adjudicator.

The portability hypothesis is **weakened** if the evidence contract fails in another domain, Agent outputs cannot be reproduced or compared, or review repeatedly accepts unsupported claims; a lack of independent execution attestation limits claims of cohort independence. Failure is a legitimate research outcome, not a reason to replace an example or fabricate a positive result.

## Maintainer summary

Heterogeneous Agents can materially **participate in research** as investigators, critics and software contributors. This case provides real evidence of an auditable collaborative method. It does **not** by itself establish autonomous scientific correctness, externally certified author identity or independent multi-agent replication. Those are empirical questions for subsequent controlled work.
