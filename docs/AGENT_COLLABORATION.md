# External Agent research handoff · optional interoperability

The Life Science Ecosystem Lab has **two peer software assets**, not an embedded Agent orchestration service. The existing [Knowledge Workflow](../.github/README.md) is authoritative for approved-source ingestion, native topic matching, graph projection, accepted `data/` state, receipts and Git-based replay; the independent [Evidence Tool](../evidence/README.md) is a reusable validator and inspector. Neither requires an LLM API or an Agent scheduler.

## Three deliberately separate clocks

| Plane | Scheduler or executor | Authority | Where the contract lives |
| --- | --- | --- | --- |
| Native knowledge maintenance | GitHub Actions schedule or authorized manual `persist=true` | Approved GitHub source registry, native topic rules and guarded `data/` writes | [Native production Workflow](../.github/workflows/life-science-knowledge.yml) |
| Independent Evidence Tool | CLI or separate Tool CI | Stateless verification/report paths, not the knowledge ledger | [Evidence Tool](../evidence/README.md) |
| External research Agent (Jules, GPT scheduled tasks, other systems) | **Its own** user-authorized task cadence | Research/discovery/proposals only; no implicit write authority | [Agent SOP](../.github/agent-handoff/SOP.md), [task template](../.github/agent-handoff/TASK_TEMPLATE.md) |

No recurring external-Agent schedule is created by this repository, and no native `workflow_dispatch` is triggered merely by creating an Agent handoff.

## Optional handoff lifecycle

`External network research → Source citations and uncertainties → PROPOSAL_ONLY handoff → Shape validation → Human review / PR → Independent software checks → Ordinary native acceptance (only when separately authorized)`

A handoff is **not** a native evidence candidate. It cannot be imported as `data/inputs/current/candidate.json` and does not automatically expand `evidence/profiles/sources.json` or `topics.json`. Proposals may request new research keywords or sources, but those modifications need ordinary reviewed changes and native tests. The Agent does not redefine the native topic taxonomy simply because it searched an additional term.

## Files and minimum executable interface

- [Root AGENTS.md](../AGENTS.md): repository-level instruction boundary for multiple external Agents
- [SOP](../.github/agent-handoff/SOP.md): fresh-run, research, evidence, uncertainty, review and closeout steps
- [Task template](../.github/agent-handoff/TASK_TEMPLATE.md): reusable research instruction without creating an in-repo Agent service
- [Example JSON](../.github/agent-handoff/example-handoff.json): synthetic proposal sample; not an accepted research claim
- `evidence/agent_handoff.py`: standalone standard-library-only shape and authority check

Run the optional proposal validation:

```sh
python -m evidence validate-handoff \
  --input .github/agent-handoff/example-handoff.json \
  --topics evidence/profiles/topics.json
```

Successful output is `AGENT_HANDOFF_SHAPE_VALID_PROPOSAL_ONLY`, never `EVIDENCE_VERIFIED` or `APPLIED`. This check requires a bounded JSON envelope, known native topic references, unverified cited observations, safe proposed file paths, mandatory human review and no proposed direct `data/` mutation. GitHub file citations using `/blob/` must include a frozen 40-character commit SHA. Other HTTPS citations are not independently retrieved by this check, so a valid envelope is still only a **proposal**.

A meaningful research handoff may be `NO_FINDINGS` with zero findings or proposals. A scheduler must not fabricate a finding to claim a completed research unit. Unknown or unverified claims require independent human/tool review before any source or topic registry change.

## Cache and durable-state hygiene

The tracked repository was checked for common Python caches, build products, log files and temporary directories. No tracked generated trash was found at the time of the audit. Keep reproducible local intermediates under ignored `build/` or `.agent-work/`; do **not** delete `data/`, `evidence/field-tests/`, accepted receipts, manifests, historical research observations or their immutable Git commits.

Runner-local workspaces and hosted Actions artifact retention are separate from Git-tracked files. `.gitignore` cannot erase remotely stored workflow artifacts, Actions caches or historical Git objects. No automatic cache deletion is part of the Agent handoff.

## Evidence limitations

`SOURCE_MATCH` is a topic/document lexical relationship, not a life-science result. Agent-generated explanations, registration claims and research interpretations cannot be promoted to accepted production facts without independent checks. Explicitly preserve source licensing, credential safety, counterevidence, reproducible steps and the boundary between public source citation and republication of full source text.

[Production Operations](PRODUCTION_OPERATIONS.md) · [Provenance](PROVENANCE.md) · [Understanding Verification](VERIFYING_RESULTS.md)
