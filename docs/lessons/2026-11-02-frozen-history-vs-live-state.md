# Public lesson: frozen provenance is not a live-state invariant · 2026-11-02

[New API identity delta](../provenance/post-640-to-653-observation-2026-11-02.json) · [Evidence review](../provenance/POST_640_TO_653_AND_NATIVE_ACCEPTANCE_2026-11-02.md) · [Regression](../../tests/test_post_640_run_delta.py)

An immutable October snapshot reported three accepted Knowledge Receipts and three graph events. On November 2, the native weekly `validate → apply → push → remote verify` chain legitimately created a fourth `APPLIED` event and a third Candidate archive, while the Knowledge graph still had 17 entities and 26 source-match edges.

**Failure mode:** archived-census unit tests used `assert len(current_receipts) == 3` and compared older Git Blob SHA guards to mutable `data/knowledge/current.json` and `events.jsonl`. The historical report was correct at capture time, but a current-state assertion silently made valid future production impossible without a red test.

**Detection:** compare the frozen 640-Run observation and previous test source against GitHub Run `41436556408`, `gh-41436556408-1`, main Commit `b11c4be4` and continuity Run `41445992506`. Do not treat CI success on the **pre-apply** commit as proof that a later data commit cannot expose this regression.

**Correction:** retain the old fixed denominator, original historical records and immutable Receipt SHA guards. Assert ordered historical event/Receipt prefixes against evolving live state and independently validate the full latest event chain. Never silently rewrite frozen JSON to match today's count or weaken the actual native integrity checks.

**Extra controls:** a successful Bio Push can contain a skipped `pinned-field`; interpret Job-level conclusions. GitHub Run `created_at` is not queue duration. An old failed Run disappearing from the visible API is a retention/visibility observation, not proof of error removal or operator wrongdoing. External Agent research remains proposal-only, third-party registries remain independently owned, and `DOCUMENT_TEXT_UNCHANGED` remains a revision-only accepted event — **not** new scientific evidence.

Falsifier: `python -m unittest discover -s tests -p 'test_post_640_run_delta.py' -v` plus the full suite and native `state verify`. Existing Core/Framework/Actions/data contracts remain untouched.

## 2026-11-02 follow-up: preserve both old SHA evidence and live integrity

The initial PR #55 repair made future accepted versions possible, but in two older regression files the mutable-path branch of the old SHA guard had become only `is_file()`. That is insufficient by itself. A subsequent **independent, read-only Git Tree API recheck** at commits `bc33c75efeee341194f1d2eec804565ed58a90bb` and `efc8355c130cbb54111f3a0907fdec79f116a122` matched all **20 of 20** pinned historical production path/SHA pairs. The cross-time evidence is stored separately in [historical production tree guards](../provenance/historical-production-tree-guards-2026-11-02.json), with its request clock marked unknown. The existing 2026-10-31 and 640-Run snapshot files are unchanged.

The updated regressions check historical SHA pairs against that separately observed old Tree, continue checking immutable frozen source and Receipt bytes, and require **actual native accepted-state verification** against the latest `data/`. A synthetic temporary-data negative test changes only an isolated Receipt digest and must be rejected. This prevents two symmetric failures: wrongly rejecting a legitimate next native `APPLIED` event, and wrongly accepting tampered live evidence because only files' existence was checked.

Three PR #55 intermediate branch checks ([41449357390](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41449357390), [41449363257](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41449363257), [41449370818](https://github.com/lostlight530/life-science-ecosystem-lab/actions/runs/41449370818)) were real unintended engineering failures while partial fixes were pushed. Their logs, exact SHA, correction and successful final PR/merged-main checks remain in [PR #55](https://github.com/lostlight530/life-science-ecosystem-lab/pull/55). They are not negative scientific results and must not be erased or reassigned to the pre-PR 653-Run census. The procedural correction is to publish the fully prepared patch as **one candidate commit** rather than pushing intermediate test changes.
