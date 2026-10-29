# Native production continuity: three-run field audit

[Documentation index](README.md) · [Production operations](PRODUCTION_OPERATIONS.md) · [Evidence replay](EVIDENCE_REPLAY_PROTOCOL.md) · [Understanding results](VERIFYING_RESULTS.md)

**Review:** 2026-10-30 (Asia/Shanghai). **Frozen repository baseline:** [main at a2755a3be47f54f7a1c9ce3629b9f6112316cd5f](https://github.com/lostlight530/life-science-ecosystem-lab/commit/a2755a3be47f54f7a1c9ce3629b9f6112316cd5f). This is a **read-only, historical, independently inspectable engineering case**, not new production data, a new CI gate, scientific discovery or live-monitoring status. All three commits and linked GitHub Actions runs below were fetched and compared independently; the results are bounded to the selected approved-source corpus and these exact run attempts.

## 1 — Research question and falsifier

**Question:** Did three separate native GitHub Actions executions produce traceable accepted Git state, and did later accepts represent changed selected source text, changed upstream provenance or changed candidate bookkeeping?

**Falsifier:** Any absent/unreachable run, non-successful validate/apply job, missing receipt, missing Git data commit, broken event sequence, or claimed source-text difference not supported by the 15 selected record content digests would invalidate the respective narrow claim. A complete history of every possible failed or skipped workflow run is **not** established by checking these three successful accepted runs.

A native Git **APPLIED** outcome, a candidate **DOCUMENT_TEXT_UNCHANGED** classification, identical source-text digests and an external scientific result are **different claims**. In particular, the identity of an execution, an input snapshot, an evidence bundle, a knowledge projection, a source revision and a Git acceptance commit must remain separate.

## 2 — Pinned execution and accepted-state evidence

| Native logical date | GitHub execution / trigger | Pre-apply validated HEAD | Accepted Git commit | Receipt / ledger classification |
| --- | --- | --- | --- | --- |
| 2026-10-17 | [38995485443 / attempt 1](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/38995485443), `workflow_dispatch` | `edf667abe44788f026b2cf21d12c03adc97df2b8` | [`b2d1d31f715275823f7ea0440d0a14a552f35e2a`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/b2d1d31f715275823f7ea0440d0a14a552f35e2a) | `INITIAL_SNAPSHOT`; `APPLIED` |
| 2026-10-19 | [39227185707 / attempt 1](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/39227185707), `schedule` | `c09d4f3d0a8ebe28970dd511c7ab1e96f2ee0ea6` | [`6fc2c8266fcfe3655b4e8df704817b5a40fb5f14`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/6fc2c8266fcfe3655b4e8df704817b5a40fb5f14) | `DOCUMENT_TEXT_UNCHANGED`; `APPLIED` |
| 2026-10-26 | [40297059874 / attempt 1](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/40297059874), `schedule` | `c1d58b52f35fe31c475c4cec3c78f1178d66eab8` | [`25722539226349079cda66a5390185c2399d174c`](https://github.com/lostlight530/life-science-ecosystem-lab/commit/25722539226349079cda66a5390185c2399d174c) | `DOCUMENT_TEXT_UNCHANGED`; `APPLIED` |

All three run APIs reported **completed/success**, with both `validate` and `apply` jobs **success**. The receipt files `data/receipts/gh-38995485443-1.json`, `gh-39227185707-1.json` and `gh-40297059874-1.json` each report `APPLIED`. GitHub commit file lists confirm that these writes changed only paths under `data/`. This verifies three **distinct native production accepts**, not a claim about all scheduled runs or unobserved attempts.

The accepted `data/knowledge/events.jsonl` at the third commit has **three** events linked by `previous_event_sha256`: `c19b627cf53dc8782e00dc5a754a134371eab9f6df61114c42d9e6a8bdbc7` → `f2aff42d3fd54263fecd9ae5b268f2c690d6ef83417266e8b443b74cf98bdea0` → `0676729da2ab4de058b216e5dd01bf5a5e9de667d204d77e79918bda273034b5`. These are stored event identities; use the existing strict verifier for structural validation rather than treating a visually matching string as proof of hash correctness.

At the latest accepted revision, `data/knowledge/graph-manifest.json` declares **17 entities, 26 SOURCE_MATCH edges**, with **15 selected documents, four approved GitHub source repositories and three configured topics**. These represent a bounded extractive document/subject map, **not 26 validated scientific relationships**.

## 3 — The unexpected distinction: selected text versus accepted event

| Observation | Oct 17 → Oct 19 | Oct 19 → Oct 26 |
| --- | --- | --- |
| Selected document population | 15 → 15 | 15 → 15 |
| Selected `records[].content_sha256` | 15/15 unchanged | 15/15 unchanged |
| Selected upstream revision identities | All four repositories unchanged | One changed: `seek4science/seek` |
| `candidate.input_digest` | Same: `0fc7d508fa5afb89eb9eec424869ae107ab28ff2419f124cafe8f88e6f483005` | Changed to `4a9aeb43c99dadb6edf602daf776b3630bf42d05ee8b6d0e832c5b162dbd51f2` |
| `candidate.changes[].kind` | All 15 `unknown_baseline` became `unchanged` | All 15 continued `unchanged` |
| Accepted `candidate.output_digest` | `5c3ee4aaea44…` → `06d0a853514d…` | `06d0a853514d…` → `0a20ce424193…` |
| Accepted snapshot ID | Same: `0fc7d508fa5afb89-787471b78dfe37c2` | New: `4a9aeb43c99dadb6-787471b78dfe37c2` |
| Actual outcome | New `APPLIED` receipt, event and Git commit | New `APPLIED` receipt, event, Git commit and prior-input archive |

The single upstream revision shift on October 26 was `seek4science/seek` from `e47e21f6517ae0a0808c18b733ec7bdbea64e593` to `65b13b4b5675d64c50a8ab87d675033ca07a70b5`. The selected `seek/README.md` content digest remained equal. This supports **provenance/revision movement without a selected-document text change**, not evidence of an altered scientific method or biological result.

### Source-level causal explanation of the October 19 acceptance

This mechanism can now be traced directly through the **current reviewed implementations**, rather than only inferred from recorded objects:

1. `evidence/aggregation.py::aggregate_evidence()` sets `changes[].kind=unknown_baseline` when no previous candidate is supplied. On the next native scheduled observation, `--previous data/inputs/current/candidate.json` supplies the accepted prior candidate and the unchanged 15 selected texts are labeled `unchanged`
2. `aggregate_evidence()` computes `input_digest` from canonical selected **records**, but computes `output_digest` from the complete candidate envelope, **including** `changes[]`. Thus October 17 and October 19 have the same input/profile digests and different candidate output digests
3. `.github/runtime/life_science_ecosystem_lab/knowledge.py::build_knowledge()` embeds `candidate.output_digest` as `evidence_bundle_digest` in Knowledge and signs the full Knowledge object. Even with identical extracted source text, October 19's Knowledge object is unequal to October 17's Knowledge object
4. `.github/runtime/life_science_ecosystem_lab/lifecycle/orchestrator.py::apply_lifecycle()` returns `NO_MEANINGFUL_DELTA` only when **all three** hold: active `input_digest` equals the candidate input digest; active `profile_digest` equals the new profile digest; and the prior accepted Knowledge object equals the supplied Knowledge object (when one is supplied)
5. On October 19 the third predicate failed: the implementation therefore issued `APPLIED` with the *descriptive* `DOCUMENT_TEXT_UNCHANGED` change kind and wrote an execution-specific receipt/event. This is **expected under the existing software predicate**, not an unexplained failure of GitHub Actions

Once the `unchanged` change labels themselves stabilize, a repeat with identical selected records, profile and Knowledge takes the **no-delta** path and does not write another receipt/event. The new [isolated regression](../tests/test_native_acceptance_causality.py) characterizes both this transition and the provenance-only revision path **using synthetic records and a temporary data root**, without modifying production state.

The **engineering cause** of October 19's event is now explained, but the **policy question remains open**: should a bootstrap bookkeeping reclassification that changes a candidate envelope but not selected texts or upstream commits qualify as a meaningful durable acceptance? Changing that policy would require a separate authorized runtime change, migration/replay analysis and governance review. Do **not** silently relabel the historical receipt as `NO_MEANINGFUL_DELTA`, rewrite accepted `data/`, or claim scientific novelty from the event.

The Oct 26 `data/memories/current.json` marks `workflow-monitoring` as `UPDATED` while all three topics still have `MULTI_SOURCE` coverage. A status transition in extractive knowledge metadata is **not** a measurement of new scientific findings.

The two prior accepted candidates are preserved as real files under `data/inputs/archive/2026/10/` in the latest tree; the archive is not a cache to clean.

## 4 — Independent, read-only command replay

Use a **full-history** checkout containing all three accepted commits; a shallow clone may need to fetch the required history. Install the current CLI in a disposable environment, but distinguish validation under current code from validation under each historical commit. All commands below only read Git objects or accepted state:

~~~sh
git fetch origin main
git show b2d1d31f715275823f7ea0440d0a14a552f35e2a:data/receipts/gh-38995485443-1.json
git show 6fc2c8266fcfe3655b4e8df704817b5a40fb5f14:data/receipts/gh-39227185707-1.json
git show 25722539226349079cda66a5390185c2399d174c:data/receipts/gh-40297059874-1.json
git show 25722539226349079cda66a5390185c2399d174c:data/knowledge/events.jsonl
git diff --name-only 6fc2c8266fcfe3655b4e8df704817b5a40fb5f14^ 6fc2c8266fcfe3655b4e8df704817b5a40fb5f14
ls-knowledge state verify --repository-root . --require-accepted
ls-knowledge graph verify --dir data/knowledge --knowledge data/knowledge/current.json
~~~

The two `ls-knowledge` invocations inspect the **currently checked-out** accepted state, not a historical commit passed as an argument. Use an isolated worktree at a pinned commit to replay its state with matching code, without writing to the original checkout. No `persist=true` invocation is needed.

This optional standard-library comparison reads the three historical Git objects and **asserts** the observed selected-text/provenance differences. It does not mutate repository paths or independently authenticate the scientific content:

~~~sh
python - <<'PY'
import json, subprocess
commits = [
    "b2d1d31f715275823f7ea0440d0a14a552f35e2a",
    "6fc2c8266fcfe3655b4e8df704817b5a40fb5f14",
    "25722539226349079cda66a5390185c2399d174c",
]
def obj(rev, path):
    raw = subprocess.check_output(["git", "show", f"{rev}:{path}"])
    return json.loads(raw)
bundles = [obj(c, "data/inputs/current/candidate.json") for c in commits]
receipts = [obj(c, f"data/receipts/gh-{rid}-1.json")
            for c, rid in zip(commits, [38995485443, 39227185707, 40297059874])]
def indexed(bundle):
    return {(r["source_id"], r["path"]): r for r in bundle["records"]}
a, b, c = [indexed(x) for x in bundles]
assert len(a) == len(b) == len(c) == 15
assert a.keys() == b.keys() == c.keys()
assert all(a[k]["content_sha256"] == b[k]["content_sha256"] == c[k]["content_sha256"]
           for k in a)
assert all(a[k]["commit"] == b[k]["commit"] for k in a)
revision_changes = [k for k in b if b[k]["commit"] != c[k]["commit"]]
assert revision_changes == [("seek", "README.md")]
assert bundles[0]["input_digest"] == bundles[1]["input_digest"]
assert bundles[1]["input_digest"] != bundles[2]["input_digest"]
assert [r["change_kind"] for r in receipts] == [
    "INITIAL_SNAPSHOT", "DOCUMENT_TEXT_UNCHANGED", "DOCUMENT_TEXT_UNCHANGED"
]
assert all(r["outcome"] == "APPLIED" for r in receipts)
print("PASS: three accepted historical receipts; 15 unchanged text digests; "
      "one upstream revision-only change on seek/README.md")
PY
~~~

A `PASS` here validates the **specific asserted relationships in already accepted repository objects**. It does not replace independent source re-acquisition, the native state verifier, the GitHub run API, a scientific comparator, or a comprehensive test of all possible no-change scenarios.

## 5 — Scheduling and verification gaps

The workflow at the two scheduled-run input commits declares `23 3 * * 1` (Monday 03:23 UTC). The GitHub run API reports `run_started_at` **2026-10-19 09:03:15 UTC** and **2026-10-26 09:06:46 UTC**. This is a directly observed difference between nominal cron and actual reported run starts, **not a verified root-cause attribution**. GitHub documents that [scheduled events can be delayed or dropped](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows); a cron value is not a run-start SLA. Do not shift the logical research date based on an assumed dispatch time, or rewrite the existing schedule as part of this review.

GitHub also documents that [push events caused by the workflow's `GITHUB_TOKEN` normally do not start new push workflows](https://docs.github.com/en/actions/concepts/security/github_token). Thus an accepted data commit must be checked through its own run, remote Git revision, receipt, event chain and **separately observed** post-acceptance checks; do not assume every data-only write automatically re-triggered the ordinary push CI.

Read-only synthetic regression focused on the three-gate acceptance predicate:

~~~sh
python -m unittest discover -s tests -p 'test_native_acceptance_causality.py' -v
~~~

This test exercises the existing implementation on disposable input and temporary accepted state. It is **not** a re-execution of the historical network acquisition and does not change the native schedule or its authority.

The three accepted events are evidence of **real continuity**, not exhaustive proof of long-term reliability, idempotence on identical candidate metadata, failure recovery, third-party monitoring, domain transfer or scientific validity. A next no-delta field audit should freeze the exact current candidate/profile/runtime, keep run/attempt and stored outputs separate, execute read-only or isolated comparisons and retain both a positive and negative control before requesting any code or governance change.

## 6 — Decision and authority

**Supported:** three distinct accepted native Git snapshots, two real scheduled accepts, one manual initial accept, three linked stored events, 15 stable selected document contents across these accepts, and an upstream SEEK revision-only change in the last interval.

**Resolved at implementation level, not policy level:** the October 19 metadata-only acceptance follows the three-predicate no-delta guard and envelope-to-knowledge digest propagation. **Unresolved:** whether a bootstrap metadata-only acceptance should remain intentionally meaningful; whether all other scheduled and failed runs meet durability goals; why the scheduled runs began hours after their nominal cron; how historical artifacts compare byte-for-byte after their 14-day retention; and whether any independent scientific oracle supports a domain claim.

**Not claimed:** newly discovered biology, an externally certified workflow, completion of a cross-domain benchmark, automatic external service metadata synchronization, or a new software behavior from this documentation.

Any decision to change production idempotence or event emission must be reviewed in a **separate, explicitly authorized implementation change** with regression fixtures, a migration strategy for accepted history and failure-safe rollout. This case itself does not edit the Workflow, Evidence/Bio Tools, Framework, source/topic registries, production `data/`, or externally governed accounts.
