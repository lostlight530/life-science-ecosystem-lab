# Provenance policy

Each product must preserve the source identity needed to reproduce its result

Minimum evidence includes the repository, immutable commit, source path, content digest, schema version, validation command, and final status

Mutable branches may be used for development but must not be recorded as frozen execution identities

## Snapshot versus execution identities

The evidence candidate `run_id` is a **content-derived snapshot identifier** (prefixes of input and topic-profile digests), not a unique execution ID. Accepted receipts include `snapshot_id` and `execution_id`, and are written under `data/receipts/<execution_id>.json`. A historical snapshot may recur as A → B → A without overwriting its earlier receipt. Production supplies `gh-<GITHUB_RUN_ID>-<GITHUB_RUN_ATTEMPT>` explicitly; the local CLI allows `ls-knowledge lifecycle apply --execution-id <id>` or supplies a local UUID when unspecified. The accepted event ledger uses the execution identity as its unique `run_id` and records the snapshot identity separately. Legacy event entries remain verifiable.

Accepted `change_kind` distinguishes `INITIAL_SNAPSHOT`, `TOPIC_PROFILE_CHANGE`, `DOCUMENT_CONTENT_OR_SELECTION_CHANGE`, and `DOCUMENT_TEXT_UNCHANGED`. The last label means the selected source ID/repository/path/content-SHA256 tuples are unchanged even if Git revision or other provenance metadata has changed. **It does not claim that scientific meaning or source quality was verified**.

External states use explicit terms: `not-connected`, `prepared`, `submitted`, `accepted`, and `verified`

Authentication success, linked accounts, local metadata, or a passing unit test must not be represented as registry acceptance, institutional affiliation, scientific validity, or authorization for sensitive data


## Cross-component evidence and authority boundaries

An evidence identifier proves only the object and operation it names. Keep each independent product's evidence separate rather than converting a local success status into a cross-system certification.

| Producer or observer | Minimum independently inspectable object | What the object cannot attest |
| --- | --- | --- |
| Knowledge Workflow | Approved source/ref/path and content digest; candidate/snapshot identity; accepted Git commit, event and execution-specific receipt when persistence actually occurred | Scientific semantics of a matched passage, independent replication, or a new finding after `NO_MEANINGFUL_DELTA` |
| Evidence Tool | Versioned inspection/validation inputs and structured finding/report; upstream Git identity where collected | Execution of third-party scientific code, external standards certification or biological validity |
| Bio Tool | Input FASTA/PDB file bytes or fixed digest, parser invocation and bounded JSON composition/residue findings | Protein folding accuracy, input biological provenance, molecular geometry or clinical meaning |
| Experimental Framework | Versioned bundle and oracle, locally available byte hashes, declared method/lineage contract and `PASS`/`FAIL`/`INDETERMINATE` report | Actual method execution, nonlocal bytes, scientific result acceptance or a release covered by the frozen `v0.4.0` DOI |
| External Agent or maintainer observation | Dated original source, declared execution surface, fixed revision or artifact where available, review/decision record | Automatically verified Agent identity, acceptance of a proposal, account privileges or scientific truth |

For a cross-component research statement, reviewers should record which row produced each piece of evidence, the immutable revision or bytes actually checked, and the remaining gap between **observation**, **software validation**, **method suitability**, **independent scientific evaluation**, **human approval**, and **external registration**. These are different proof obligations, not a score to add together. The stable lifecycle is [DEFINE → PIN → QUALIFY → EXECUTE → EVALUATE → AUDIT → REVIEW → REPLAY](RESEARCH_METHODOLOGY.md). `PROPOSAL_ONLY`, `INDETERMINATE`, failures and negative findings must remain retrievable without being promoted to accepted `data/`.

The [FAIR4RS v1.0 Recommendation](https://doi.org/10.15497/RDA00068) motivates version-specific research-software identities; [W3C PROV-O](https://www.w3.org/TR/prov-o/) supplies a provenance vocabulary. The table above is a **project-owned review contract**, not a PROV-O serialization, FAIR4RS conformance certification or externally adopted standard.
