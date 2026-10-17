# External Agent participation · optional, proposal-only

This repository has **two peer research software assets**: native knowledge Workflow under `.github/`, and the independent `ls-evidence` Tool under `evidence/`. No agent framework, skill, model account, API key, or external scheduler is necessary to run either asset.

Before working, read [Architecture](docs/ARCHITECTURE.md), [Agent collaboration](docs/AGENT_COLLABORATION.md), and [Verification boundaries](docs/VERIFYING_RESULTS.md). For durable accepted state, `data/` and its Git commit/receipts are authoritative, not an Agent answer or temporary workspace. The current native topic IDs, aliases, thresholds and approved sources belong exclusively to `evidence/profiles/topics.json` and `evidence/profiles/sources.json`.

**Protein field case:** the [protein structure prediction pilot](docs/PROTEIN_STRUCTURE_FIELD_DEMO.md) and [pinned Agent handoff](.github/agent-handoff/protein-structure-2026-10-17.json) demonstrate a proposal-only external Agent using isolated native source/topic profiles, with no direct production authority.

**When an external Agent conducts a new online research session:** use the independent [research SOP](.github/agent-handoff/SOP.md) and [task template](.github/agent-handoff/TASK_TEMPLATE.md). Return a human-readable evidence review and, if useful, a `EXTERNAL_AGENT_RESEARCH_HANDOFF` JSON proposal. Run `ls-evidence validate-handoff --input <file> --topics evidence/profiles/topics.json` before a proposed PR. This only validates the proposal envelope.

The Agent may independently search the web, use its own scheduling (e.g. Jules or GPT tasks), review external workflow/tool outputs, propose code/doc/source-profile edits, and submit changes for review. **Do not** automatically add discovered sources to the native registry, alter topic policy, promote findings to scientific truth, edit accepted `data/`, invoke `persist=true`, or assert external registration on the strength of an Agent report. Accepted production writes remain governed by the native workflow.

Keep local scratch under ignored `build/` or `.agent-work/`; never commit tokens, session logs, caches, internal deliberation, or downloaded private research materials. Preserve accepted snapshots, immutable provenance, receipts and field evidence, even if they look like generated files.
