# Reusable Research Methodology Contract

This repository is a **research software engineering methodology demonstrator**, not a fixed biological benchmark or a catalog whose scientific significance is measured by the number of supported assays. An illustrative domain can be exchanged without replacing the methods for provenance, reproducibility, evaluation and human authority.

## Stable lifecycle

| Stage | Required methodological question | Evidence boundary |
| --- | --- | --- |
| DEFINE | What is the falsifiable question, scope and planned non-claim? | Research question; no result assumed |
| PIN | Which immutable inputs, licenses and software revisions are in scope? | Digests, source identities and frozen versions |
| QUALIFY | Are inputs and methods suitable and quality-limited? | Missingness, provenance and known limitations |
| EXECUTE | Was a bounded method run in an identified environment? | Invocations, versions, runtime and output identities |
| EVALUATE | What metric, unit, reference and uncertainty applies? | Experimental reference vs peer model vs simulation separated |
| AUDIT | Can another party inspect source, method, results and failures? | Inspectable receipts and independently checkable evidence |
| REVIEW | Who can approve a claim, a registry change and a production write? | Human/repository governance, not Agent self-certification |
| REPLAY | Does repeat execution or a later version change the outcome? | Idempotence, version differences and explicit uncertainty |

The **eight stage names and required audit boundaries remain invariant**. Domain adapters, algorithms, datasets, measurable properties and examples vary. A method may fail or be inapplicable in a given case; reasons and evidence must be retained rather than overwritten with `PASS`.

## Three independently callable software assets

- **Knowledge Workflow** manages approved-source ingestion, extractive graph, longitudinal state transitions, receipts and Git-backed replay. Its `data/` acceptance is never delegated to a research case.
- **Evidence Tool** provides the reusable method contract interface `ls-evidence validate-research-case`, alongside source, software, knowledge and interoperability audits.
- **Bio Tool** is one executable scientific data-processing adapter family. Its FASTA/PDB methods are concrete field proofs, not the definition or full scope of the methodology; new experimental domains require real implementations and independent benchmarks.

External Agents may formulate hypotheses, search methods, organize source evidence, draft runnable protocols and recommend reviews. Their contribution remains `PROPOSAL_ONLY`. No shape validator can certify real experimental execution or peer review.

## Domain-neutral, proposal-only validation

The `RESEARCH_CASE_PROPOSAL` v1.0.0 JSON envelope must declare domain, question, input SHA-256 and format, frozen method version/software commit/parameter digest, stages, execution state, metrics with units and reference type (if run), limitations, and pending human review. The same validator handles scientific workflow software and biological data processing without branching on the domain label.

```sh
ls-evidence validate-research-case --input path/to/research-case.json --output build/case-shape-report.json
python -m unittest discover -s tests -p 'test_research_case.py' -v
```

`PASS` means **proposal structure only**, never real input digest verification, method appropriateness, execution proof, statistical validity, scientific novelty, clinical applicability, independent registration or approval. For an executed case, downstream adapters and reviewers must verify the actual bytes, outputs and method-specific measurements separately; the contract deliberately cannot know the scientific meaning of every possible metric.

## Replaceable examples and genuine generalizability

The current fixed protein examples illustrate data-quality computation and pinned Git identity; the scientific-workflow corpus illustrates evidence/knowledge lifecycle and replay. These prove specific contracts in particular cases—not generalized biological or scientific correctness. Replacing the examples to test transferability must retain fixed core gates while documenting new failure modes, negative controls, reference sets, measurement limitations and independent reviewer evidence. Example choice can vary; **sampling and scientific conclusions still require an explicit, reproducible design**.

Synthetic fixtures are permitted only for labeled software-contract regression. They cannot be presented as field samples, external observations, benchmark ground truth or evidence for a scientific conclusion. A field case described as real must bind the actual source bytes to an immutable source identity and digest, preserve licensing and measurement limits, and retain negative or failed outcomes without substituting fabricated success data.

## Cross-version durability

Distinguish document revision-only change from changed source content, method version from data version, and rerun execution identity from accepted content identity. Log unverified hypotheses separately from measured outcomes. Never infer durable scheduled production from one green CI run. A DOI, workflow registry identifier, external GitHub App installation or software citation describes a different layer from scientific method validation.

This is a publicly reproducible software research method, not an assertion of unpublished experimental results.

## Heterogeneous Agent cohort as a replaceable research case

[Three actual public Agent contributions](AGENT_CLUSTER_RESEARCH_CASE.md) form a study of proposal provenance, attribution, review, correction and integration under the **same fixed eight-stage method**. This is a research-software collaboration field case; it does not prove that three authenticated independent Agent runtimes reproduced a biological ground truth. The [decision ledger](AGENT_REVIEW_DECISIONS.md) distinguishes revised technical claims, validated engineering changes, observer-only statements and remaining unknowns. The research question and falsification plan may be transferred to another domain without changing the underlying method.

## Life-sciences cross-domain *software* interoperability experiment

The independent [Framework](../framework/README.md) deliberately separates the subject of a software-engineering test from the biology of the example. In the first study the testable property is whether diverse life-sciences software artifacts can share a typed, bounded, versioned dependency contract

DEFINE states the falsifiable interoperability failure; PIN freezes input bytes, contract and oracle versions; QUALIFY determines what was actually observed; EXECUTE invokes only the offline contract evaluator; EVALUATE compares explicit expected and observed machine statuses; AUDIT examines false acceptance, false rejection and skipped cases; REVIEW preserves authority and dissent; REPLAY compares timestamp-free reports

The [synthetic mutation challenge](../framework/docs/CONTRACT_CHALLENGE.md) establishes only regression performance over hand-authored examples. If later experiments use real public omics, image or clinical-adjacent data software, they require appropriately licensed, non-sensitive, independently reviewed fixtures and domain-appropriate validation; no sample or scientific claim is promoted solely from the Framework's green contract verdict

## Claim admission and falsification review — non-executable policy

The fixed eight-stage methodology is not a promise that every domain supports the same biological measurements. The following is a **human-review protocol**, not a new CLI, schema, CI gate, research result or delegation of approval authority.

### Claim review record

Before judging a substantive proposition, identify all of its independently reviewable parts:

| Field | What must be stated | Invalid substitute |
| --- | --- | --- |
| Exact claim | Proposition, scope, subject/population, observation period and proposed non-claim | Calling a whole Agent or repository verified |
| Falsifier | A plausible contrary observation and an alternative explanation | Treating a passing CI job as the scientific hypothesis |
| Frozen inputs | Source identity, exact object, byte digest, version, license and inclusion/exclusion rule | A mutable branch as a frozen scientific input |
| Method | Algorithm, version, parameters, intended operating range and prerequisites | A method name with no suitability check |
| Execution | Who or what ran which version, on which surface, with identified outputs | An Agent narrative in lieu of an execution record |
| Evaluation | Baseline, independent reference, metric, unit, denominator, uncertainty and negative controls | Cherry-picked successful output without a comparator |
| Decision | Reviewer, reasoning, dissent, limitations, exact outcome and authority | Schema-valid Handoff interpreted as scientific approval |
| Replay | Which bytes and decisions can be independently repeated, and which cannot | Reproducing JSON serialization as scientific replication |

A negative or inconclusive result can be scientifically useful. A case that lacks an appropriate reference may be sound research documentation while its scientific inference remains unsupported.

### Four orthogonal proof obligations

| Obligation | What it checks | What it does not prove |
| --- | --- | --- |
| **Software correctness** | An implementation respects declared input/output, status, failure and deterministic tests on identified inputs | Its algorithm is suitable for the scientific question |
| **Evidence integrity** | Identified objects, digests, provenance, receipts and transformations are consistent and inspectable | The source author is correct or the method was appropriate |
| **Method suitability** | Sampling, assumptions, measurement design, controls and known bias fit the specific question | The observed scientific result has already been independently reproduced |
| **Scientific validity** | Domain-relevant comparison, a justified reference, limitations, uncertainty and falsification actually support a bounded scientific proposition | A general biological conclusion, clinical use or permanent certification |

These are independent proof obligations, **not** additive scores. In particular, a syntactically valid Git SHA is not a verified Git object; a valid FASTA/PDB file is not a correct fold; a source-linked topic match is not a biological causal relationship; successful Framework output is not proof that a declared external computation happened.

### Review language and state mapping

The following are **prose labels for decisions, not implemented machine enums**:

- **PROPOSED:** explicit falsifiable question and protocol; no accepted result
- **OBSERVED:** dated source or execution evidence with scope and provenance
- **ENGINEERING_VERIFIED:** the identified code/evidence contract passed on pinned inputs, no scientific inference
- **SCIENTIFICALLY_EVALUATED:** a domain-appropriate comparison was performed; positive, negative and inconclusive outcomes remain possible
- **REVIEW_ACCEPTED_WITH_SCOPE:** an authorized review accepted an exact bounded statement, not the Agent as a permanent trusted authority
- **REVISED / CONTRADICTED:** a prior assertion was revised or refuted, preserving original and correction
- **INDETERMINATE / BLOCKED:** required source, comparator, method or execution evidence is unavailable or inadequate
- **NO_FINDINGS:** the declared bounded inquiry ended without a supported finding, and without manufacturing a new result

The existing production **APPLIED** outcome concerns Git-accepted knowledge state, not scientific endorsement. External registry **ACCEPTED** is a status belonging to that service. Neither is an alias of REVIEW_ACCEPTED_WITH_SCOPE.

### Evaluation design, controls and stopping

Before examining experimental outcomes, specify unit of analysis (source document, file, repository, version, run, sample or independently observed Agent contribution), comparator, explicit pass/fail or abstention criteria, treatment of missing data and conditions for stopping. For a ratio, preserve **numerator and denominator**; for a repeated-run statistic, preserve window, successful, failed, timed-out, canceled, no-change and superseded attempts separately.

A corrupted digest is a valid negative control for an integrity checker, **not** proof that a biological hypothesis failed. A deliberately malformed FASTA/PDB input tests parser rejection, not model accuracy. Two agreeing Agent texts demonstrate agreement of statements, not independently authenticated execution or independent scientific replication.

An experiment must be allowed to stop with BLOCKED, NO_FINDINGS or an inconclusive decision. Do not expand a dataset, select a different metric or invent a repository change merely to maintain apparent research continuity. Preserve conflicting observations and reviewer disagreement. Distinguish hypothesis development from the versioned protocol used to evaluate a particular hypothesis.

### Cross-domain transferability experiment

To test that this method genuinely transfers, hold the eight review stages and authority rules constant while varying domain data, algorithms, expected failures and measurement methods. Report what is invariant, what requires domain adaptation, and which limitations invalidate a proposed transfer. Compare error classification, refusal behavior, provenance recoverability and **independent review of exact scoped claims**, not matching JSON key names alone.

This review policy is project-owned. External [FAIR4RS v1.0](https://doi.org/10.15497/RDA00068) recommends version-specific research software identities and detailed provenance, while [W3C PROV-O](https://www.w3.org/TR/prov-o/) distinguishes entities, activities and agents. Neither reference accredits LS or makes these Markdown review labels an implemented formal standard.
