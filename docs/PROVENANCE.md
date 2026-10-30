# Provenance policy

The [origin-to-present historical reconstruction](REPOSITORY_HISTORY_AND_PROVENANCE.md) and [frozen GitHub REST API census](provenance/README.md) cover all 42 PR outcomes, 234 reachable main commits and 531 publicly returned run records at a precise observation cutoff. Their JSON snapshots are **project-authored, non-production historical evidence**: they do not replace Git objects, accepted `data/`, external institution records, expired Actions artifacts, direct scientific observations or reviewer authority. The [open claim/falsifier register](CLAIM_VERIFICATION_GAPS.md) keeps unknown, negative and unmerged evidence independently visible.

A [later append-only reconciliation](provenance/RECONCILIATION_2026-10-30.md) records an observed difference between two dated Actions API snapshots, including disappeared historical failures and an independent [daily native quality ledger](provenance/NATIVE_DAILY_QUALITY_2026-10-30.md). The original census is deliberately not rewritten. Per-run absence from a later API response is not evidence of its deletion mechanism or actor, and no retired-run metadata can substitute for missing original Job logs.

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

## Cross-infrastructure metadata and identity reconciliation

Scientific software distribution and monitoring systems are different authorities. Each owns its own identifier, version semantics, update clock, permission model and evidence. An upstream catalog, downstream index, workflow registration, monitoring run, immutable software release and researcher's login must never be represented by a single unqualified status.

### Independent objects to preserve

| Object | Minimum observation | Boundary |
| --- | --- | --- |
| GitHub release | Tag, immutable commit, release time, software scope and artifact identity | A mutable main-branch ZIP is not a frozen version |
| Zenodo record | Concept versus version DOI, record/revision, downloadable archive and actual release relationship | Software archive is neither a peer-reviewed article nor a scientific result |
| WorkflowHub | Workflow ID **and version**, DOI, registered executable and source-version link | Portable CWL does not replace native GitHub Actions or prove biological validation |
| LifeMonitor | Workflow, suite, test instance, observation time, visibility and observed test status | Private dashboard, enrollment and one passing test do not prove public certification or durable uptime |
| bio.tools | Tool ID, captured source fields, version, reported update time, provenance of API result | Catalog inclusion or its own validation flags do not constitute scientific benchmarking |
| OpenEBench | Exact monitor URL, tool ID, response fields and source time, independently observed retrieval time | Active metadata monitoring is not a published scientific benchmark |
| LS Login or another identity provider | Authentication and authorization facts for an identified service at a dated observation | Identity linkage does not establish institutional affiliation or rights to publish |

Different platform IDs may describe related but **not identical** versioned objects. Record the exact relationship (catalogs, references, archives, tests or monitors) and evidence for that relation. Do not equate citation identifiers, Git SHA, WorkflowHub DOI and private monitoring UUID.

### Two-sided observation worksheet (not a new machine format)

For source-to-downstream metadata comparison, a reviewer should record:

- Upstream and downstream provider, canonical URL, object identifier and version (or **unknown**)
- Actual retrieval time in UTC **for each request separately**, transport result and permission scope
- Platform-reported update/time fields **verbatim**, with their stated or unknown semantics
- Original non-sensitive JSON response or byte digest and the exact observed field set
- Field mapping, transformation or filtering evidence, distinguishing missing, null, empty and unsupported fields
- Differences, conflicting observations, access failures, competing explanations and unresolved uncertainty
- Review decision: matching, differing, unmapped or inconclusive, with the next observation criterion

**Retrieval time, source update time, downstream embedded timestamp and archival creation time are different clocks.** A downstream value older than an upstream value supports a time-bounded discrepancy, not a conclusion that its importer is broken or that the upstream record vanished. Recheck raw fields before attributing drift to cache, batch cadence, mapping or permissions.

### Dated LS cross-platform case, not a live status claim

The repository's [machine-readable standards snapshot](../metadata/standards-status.json) contains a **2026-10-18 maintainer-observed** bio.tools record and OpenEBench metadata-monitoring record for the same tool ID. At that observation, OpenEBench carried an older description and empty credits/publications/repositories fields while the upstream bio.tools record had been updated. This is a historical field-difference observation; its cause was not demonstrated.

The corresponding reference endpoints are [bio.tools API](https://bio.tools/api/tool/life-science-protein-file-audit) and [OpenEBench monitor API](https://openebench.bsc.es/monitor/tool/life-science-protein-file-audit). **Neither API supplied a directly verified October 29, 2026 response in this review.** No current synchronization result, importer schedule, curator acceptance or new benchmark is asserted. Failed access is not silently replaced by an old cache or search summary.

The [WorkflowHub workflow version 2](https://workflowhub.eu/workflows/2347?version=2), the repository [LifeMonitor configuration guide](https://lifemonitor.eu/lm_wft_best_practices_github_app) and the archived v0.4.0 software release are related but independently governed objects. The project-level lifemonitor.yaml may override account-wide settings for explicit fields; its presence is not test evidence or permission to alter global defaults. The later experimental Framework was not part of the frozen v0.4.0 release.

### Investigation without unauthorized mutation

1. Pin both object identities and retrieval times; collect lawful non-sensitive responses or their exact digests
2. Compare only documented comparable fields, retaining unknown and null separately
3. Review service-authored schema and importer documentation **before** asserting a cause
4. Keep contradictory reports, temporary HTTP failures and zero/absent distinctions, without inventing an outage or scientific finding
5. If necessary, request explanation from the platform owning the record, preserving the reply as correspondence rather than a completed data migration
6. Submit a reviewed project observation if reproducible; do not mutate the live registry or accepted data/ based only on an external difference

This policy uses the entity/activity/agent distinction described in [W3C PROV-O](https://www.w3.org/TR/prov-o/) and component/version provenance concerns emphasized by [FAIR4RS](https://doi.org/10.15497/RDA00068). It does not claim RDF serialization, standards certification or that external systems adopt LS-specific review vocabulary.
