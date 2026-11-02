# Public lesson: frozen provenance is not a live-state invariant · 2026-11-02

[New API identity delta](../provenance/post-640-to-653-observation-2026-11-02.json) · [Evidence review](../provenance/POST_640_TO_653_AND_NATIVE_ACCEPTANCE_2026-11-02.md) · [Regression](../../tests/test_post_640_run_delta.py)

An immutable October snapshot reported three accepted Knowledge Receipts and three graph events. On November 2, the native weekly `validate → apply → push → remote verify` chain legitimately created a fourth `APPLIED` event and a third Candidate archive, while the Knowledge graph still had 17 entities and 26 source-match edges.

**Failure mode:** archived-census unit tests used `assert len(current_receipts) == 3` and compared older Git Blob SHA guards to mutable `data/knowledge/current.json` and `events.jsonl`. The historical report was correct at capture time, but a current-state assertion silently made valid future production impossible without a red test.

**Detection:** compare the frozen 640-Run observation and previous test source against GitHub Run `41436556408`, `gh-41436556408-1`, main Commit `b11c4be4` and continuity Run `41445992506`. Do not treat CI success on the **pre-apply** commit as proof that a later data commit cannot expose this regression.

**Correction:** retain the old fixed denominator, original historical records and immutable Receipt SHA guards. Assert ordered historical event/Receipt prefixes against evolving live state and independently validate the full latest event chain. Never silently rewrite frozen JSON to match today's count or weaken the actual native integrity checks.

**Extra controls:** a successful Bio Push can contain a skipped `pinned-field`; interpret Job-level conclusions. GitHub Run `created_at` is not queue duration. An old failed Run disappearing from the visible API is a retention/visibility observation, not proof of error removal or operator wrongdoing. External Agent research remains proposal-only, third-party registries remain independently owned, and `DOCUMENT_TEXT_UNCHANGED` remains a revision-only accepted event — **not** new scientific evidence.

Falsifier: `python -m unittest discover -s tests -p 'test_post_640_run_delta.py' -v` plus the full suite and native `state verify`. Existing Core/Framework/Actions/data contracts remain untouched.
