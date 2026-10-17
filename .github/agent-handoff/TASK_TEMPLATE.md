# Optional external Agent research task

Copy into your own task system or issue/PR; **do not** create a new GitHub Actions schedule for this template

**Task identifier:** <stable-id>
**Research question:** <falsifiable investigation>
**Scope:** <domain or hypothesis; not an automatic native topic-registry change>
**Time window / cutoff:** <UTC ISO date range>
**Read-only sources:** <public repositories, official standards or external citations>
**Allowed actions:** network research, local evidence inspection, draft and reviewed PR
**Disallowed actions:** bypass source registry, directly mutate accepted `data/`, invoke `persist=true`, claim enrollment or biological verification without proof
**Desired deliverables:** source URLs + immutable Git revision when possible, findings vs uncertainty, proposed improvements and review steps
**World-line anchor:** new handoff JSON declares `base: {commit, observed_at}` (immutable base SHA + UTC observation instant) — see SOP fresh-state protocol; local shape validation does not prove GitHub freshness, and the reviewer must supply an independently fetched `--expected-base-sha` for equality check
**Output:** structured handoff JSON, optional review Markdown, exact issue/PR/CI references or `NO_FINDINGS`
**When incomplete:** report `BLOCKED` with evidence and next check; do not fabricate success
**Schedule:** set separately in Jules / GPT / other Agent scheduler, if desired
**Review owner:** repository maintainer; no implicit automatic approval

Run `ls-evidence validate-handoff --input <handoff.json> --topics evidence/profiles/topics.json` for machine-readable proposal shape checks
