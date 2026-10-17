# Provenance policy

Each product must preserve the source identity needed to reproduce its result

Minimum evidence includes the repository, immutable commit, source path, content digest, schema version, validation command, and final status

Mutable branches may be used for development but must not be recorded as frozen execution identities

## Snapshot versus execution identities

The evidence candidate `run_id` is a **content-derived snapshot identifier** (prefixes of input and topic-profile digests), not a unique execution ID. Accepted receipts include `snapshot_id` and `execution_id`, and are written under `data/receipts/<execution_id>.json`. A historical snapshot may recur as A → B → A without overwriting its earlier receipt. Production supplies `gh-<GITHUB_RUN_ID>-<GITHUB_RUN_ATTEMPT>` explicitly; the local CLI allows `ls-knowledge lifecycle apply --execution-id <id>` or supplies a local UUID when unspecified. The accepted event ledger uses the execution identity as its unique `run_id` and records the snapshot identity separately. Legacy event entries remain verifiable.

Accepted `change_kind` distinguishes `INITIAL_SNAPSHOT`, `TOPIC_PROFILE_CHANGE`, `DOCUMENT_CONTENT_OR_SELECTION_CHANGE`, and `DOCUMENT_TEXT_UNCHANGED`. The last label means the selected source ID/repository/path/content-SHA256 tuples are unchanged even if Git revision or other provenance metadata has changed. **It does not claim that scientific meaning or source quality was verified**.

External states use explicit terms: `not-connected`, `prepared`, `submitted`, `accepted`, and `verified`

Authentication success, linked accounts, local metadata, or a passing unit test must not be represented as registry acceptance, institutional affiliation, scientific validity, or authorization for sensitive data

