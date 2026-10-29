# Cross-asset evidence replay and claim adjudication

[Documentation index](README.md) · [Research methodology](RESEARCH_METHODOLOGY.md) · [Understanding results](VERIFYING_RESULTS.md) · [Production operations](PRODUCTION_OPERATIONS.md)

This is a **read-only, reproducible research review protocol** for three established independent assets, the separately packaged experimental Framework and human/Agent contributions. It adds no runtime, Workflow, Tool, CI gate, accepted data write, scientific result or institutional accreditation. All commands below use existing public entrypoints.

The invariant research cycle is **DEFINE → PIN → QUALIFY → EXECUTE → EVALUATE → AUDIT → REVIEW → REPLAY**. This document asks a practical question: *given an apparently successful report, which independently inspectable bytes, identities, observations and negative controls would actually support or refute the exact claim?*

## 1 — Freeze the unit of analysis

A claim about one file is not a claim about a repository, release, Agent, run, registry entry or biological sample. Record these fields separately before executing a test.

| Dimension | Minimum record | Inadmissible substitute |
| --- | --- | --- |
| Claim | Exact falsifiable proposition; subject; scope; time window; non-claim | “The system is verified” |
| Research unit | File, version, workflow run, sample, source document, or separately observed contribution | Heterogeneous unit totals |
| Source | URL, immutable revision and path, retrieved-byte SHA-256, license | Mutable branch or syntactically valid SHA alone |
| Method | Software checkout, package version, parameters, profile and failure semantics | Tool family name |
| Execution | UTC observation, actor evidence, command, run ID/attempt, artifact and conclusion | Git author or Agent self-label |
| Comparator | Predeclared expected observation, negative controls, oracle independence, denominator and abstention rule | Green check without reference |
| Decision | Claim-specific scope, reviewer authority, dissent, unresolved risk | Automatic scientific approval from a JSON status |
| Replay | Immutable inputs, repeat commands, expected and observed comparison, non-replayable parts | A regenerated narrative |

A digest proves local byte identity only after the source bytes were independently acquired and hashed. A link to a Git blob does not by itself prove the source author is scientifically correct.

## 2 — Six evidence surfaces that cannot substitute for each other

| Surface | Useful proof | It cannot prove |
| --- | --- | --- |
| Knowledge Workflow | Source versions, source-linked projection, graph, accepted state and receipt | Biological or causal inference |
| Evidence Tool | Static software/document/metadata reports and proposal-shape checks | Scientific validity or external registry acceptance |
| Bio Tool | Bounded FASTA/PDB observations, counts, input digest and warnings | Protein prediction, geometry or function |
| Experimental Framework | Declared software lineage and local byte-contract verdict | Executed multi-omics research or validated scientific findings |
| External Agent | Original proposals, edits, criticisms and review record | Independently authenticated runtime identity from Git attribution |
| Registry or monitor | Exactly what a service exposed at a dated observation | Other services' authorization, performance or certification |

Do not add or average PASS, WARN, FAIL, INDETERMINATE, native APPLIED, registry ACCEPTED and an authorized scoped claim decision. Each has a different owner and meaning. A command exit code of 0 can coexist with a Tool WARN or Framework INDETERMINATE.

## 3 — Read-only local replay

Use Python 3.11+ and a checkout at an **explicit immutable commit**. Outputs go under ignored build/ and never overwrite original files, Git internals or accepted data/. Installing dependencies may require a network; the synthetic/local computations do not.

~~~sh
git rev-parse HEAD
git status --short
python -m pip install -e .
python -m unittest discover -s tests -v
ls-evidence inspect --root . --output build/inspection.json --markdown build/inspection.md --sarif build/inspection.sarif
ls-evidence audit-docs --root . --files evidence/profiles/docs.json --output build/docs-audit.json
ls-knowledge state verify --repository-root . --require-accepted
ls-knowledge graph verify --dir data/knowledge --knowledge data/knowledge/current.json
~~~

The tests and accepted-state verifier check engineering/data consistency, not method suitability or biological truth. The documentation auditor verifies **local** references; it does not check upstream HTTP status.

### Portable Knowledge replay with a synthetic fixture

~~~sh
python -m pip install cwltool
mkdir -p build/replay
cwltool --no-container --outdir build/replay .github/knowledge/main.cwl .github/knowledge/test/workflow-job.yml
ls-knowledge knowledge verify --candidate build/replay/candidate.json --topics evidence/profiles/topics.json --knowledge build/replay/knowledge.json
ls-knowledge graph project --knowledge build/replay/knowledge.json --output-dir build/replay-graph
ls-knowledge graph verify --dir build/replay-graph --knowledge build/replay/knowledge.json
ls-knowledge graph search --dir build/replay-graph --query workflow --limit 5 --hops 1
~~~

This reproduces a **synthetic computational path**: it does not retrieve fresh approved sources, apply a native production write or infer biological causality. SOURCE_MATCH denotes topic/document matching only.

### Real local biological file processing, without biological inference

~~~sh
ls-bio protein-fasta --input .github/bio/test/example.fasta --output build/replay-fasta.json
ls-bio protein-pdb --input .github/bio/test/example.pdb --output build/replay-pdb.json
~~~

Independently hash the exact input bytes and compare their digest to the report; inspect residue counts and warnings. A parser's success is not a benchmark of structure prediction or folding accuracy. Such claims require appropriate independent experimental references and metrics.

### Separate, unreleased experimental Framework

~~~sh
python -m pip install --no-deps -e ./framework
python -m unittest discover -s framework/tests -v
ls-framework assess --bundle framework/fixtures/software-cross-domain.json --root framework/fixtures --output build/framework/assessment.json
python -m ls_framework.challenge --bundle framework/fixtures/software-cross-domain.json --root framework/fixtures --output build/framework/challenge.json
~~~

Read status, errors, warnings and not_verified. Declared domain transitions are not proof that an external method ran. The experimental Framework 0.1.0 is not covered by the historically frozen three-asset v0.4.0 release. [Framework assurance](../framework/docs/ASSURANCE.md) documents bounded status and output-path semantics.

## 4 — Negative, missing and change controls

Declare a comparator and expected status **before** looking at outcomes. Mutated test objects must be disposable copies under build/, never edits to accepted data/, existing fixtures, registered profiles or the remote branch.

| Control | Defensible check | Unsupported inference |
| --- | --- | --- |
| Identical frozen repeat | Substantive deterministic outputs match, excluding documented volatile fields | Independent biological replication |
| One-byte mutation | Known digest violation is detected on a pinned input | A biological hypothesis is false |
| Missing/truncated required source | Block/refuse projection according to source rules | Source material was deleted upstream |
| Optional source outage | Preserve source diagnostics and fail-closed eligibility | Missing source equals zero evidence |
| Same text, different source revision | Distinguish provenance-only from text change | New scientific knowledge |
| Inconsistent copied graph | Verifier rejects altered structure/hash | Source author's statements are false |
| No meaningful delta | No fabricated accepted event or receipt | Each scheduled run has generated a discovery |
| Absent scientific comparator | A claim is blocked or inconclusive despite software PASS | Negative scientific result |
| Framework incomplete lineage | Fails or abstains within the declared contract | A scientific method did not execute |
| Agent self-description alone | Identity/run independence remains unverified | Agent research did not occur |
| Two registry fields diverge | Dated discrepancy with field-mapping uncertainty | Importer malfunction or scientific failure |

For a **completed** longitudinal field comparison of three native accepted runs, including a metadata-only acceptance ambiguity and a provenance-only upstream revision, see [Native Continuity Field Audit](NATIVE_CONTINUITY_FIELD_AUDIT.md). For longitudinal claims, compare **separate real native runs** and keep event, outcome, attempt, validated SHA, accepted receipt, remote Git commit and time window per run. Count success, failed, cancelled, no-change and superseded attempts separately. A synthetic second apply in an isolated directory is not a second production event.

## 5 — An experiment on method transfer that may fail

The hypothesis concerns **transfer of the eight review stages**, not transfer of one biological algorithm or shared JSON field names. Pre-register two genuinely different contexts—for example protein-file reports versus computational workflow provenance, or independently sourced genomics and imaging software contracts.

1. Freeze licensed input objects, identity, software versions, expected observations, exclusions and case-selection criteria before running anything
2. Choose independent, domain-appropriate comparators: byte/format reference for file audits, versioned registry evidence for metadata, known-invalid declared lineage for Framework, real Git receipts for durable state
3. Partition expected conformant, expected invalid, legitimately indeterminate and unavailable cases; report excluded and failed cases rather than dropping them
4. Where a **pre-reviewed ground-truth engineering verdict** exists, report true pass, true reject, false pass, false reject and abstentions with IDs and denominators. Never score unlabeled samples as negatives
5. Report per-domain and across-domain results separately, including uncertainty, missed detection, false rejection and instances where the method is inapplicable
6. Distinguish a reproducible software contract from a scientific claim; two agreeing Agent narratives are not independent experimental oracles
7. Stop with NO_FINDINGS, BLOCKED or a negative result when warranted, retaining the original protocol, revisions and dissent

A generalizability result is **not established** until an independently inspectable frozen case set, actual runs, comparator decisions, all outcomes and replay procedure exist. Current synthetic Framework fixtures and Bio Tool example inputs establish only their stated local properties.

## 6 — Claim-specific review record

Complete these fields in a PR or independent research log after obtaining real evidence. This is a **worksheet**, not a new machine schema or acceptance gate.

~~~text
Exact claim / unit / time window UTC:
Falsifier / alternative hypothesis / explicit non-claim:
Source URL, immutable Git commit and path, license:
Acquired bytes SHA-256 and independent acquisition evidence:
Software version / commit / command / selected profile:
Run ID / attempt / event / observed UTC / artifact identity:
Reference oracle, its independence and sampling denominator:
Expected versus observed status, fields, warnings and missingness:
Negative controls, blocked cases, dissent and uncertainty:
What can be replayed; what cannot:
Reviewer, authority, scoped decision and outstanding evidence:
~~~

External Agent handoffs remain PROPOSAL_ONLY. Code merge, production knowledge APPLIED, external registry acceptance and human review of a claim are distinct authority decisions; none can be delegated by this Markdown file.

## 7 — Where to independently verify changing facts

- [Production operations](PRODUCTION_OPERATIONS.md), current remote main, Git-tracked data/knowledge/events.jsonl and data/receipts/ for real accepted state
- [Live evidence drill](LIVE_EVIDENCE_DRILL.md) and [protein field case](PROTEIN_STRUCTURE_FIELD_DEMO.md) for **dated** observations and the synthetic/real distinction
- [Agent cohort research case](AGENT_CLUSTER_RESEARCH_CASE.md) with the [decision ledger](AGENT_REVIEW_DECISIONS.md) for review-specific agent claims, not persistent Agent trust grades
- [Interoperability review](INTEROPERABILITY_REVIEW.md) and [standards status](STANDARDS.md) for separately owned external versions, registries and clocks

A completed replay may justify a narrow engineering statement. It cannot by itself manufacture, certify or accept a scientific finding.
