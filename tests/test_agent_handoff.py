"""Offline tests for bounded optional external-Agent handoff contracts."""
import copy
import contextlib
import io
import json
import unittest
from pathlib import Path

from evidence.agent_handoff import validate_agent_handoff
from evidence.cli import main as evidence_main

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / ".github/agent-handoff/example-handoff.json"
TOPICS = {t["id"] for t in json.loads((ROOT / "evidence/profiles/topics.json").read_text())["topics"]}


class AgentHandoffTests(unittest.TestCase):
    def setUp(self):
        self.value = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def verdict(self, value=None):
        return validate_agent_handoff(self.value if value is None else value, known_topics=TOPICS)

    def test_example_is_valid_but_not_authorized(self):
        self.assertTrue(self.verdict().valid, self.verdict().errors)
        self.assertEqual(self.value["authority"], "PROPOSAL_ONLY")

    def test_unrelated_native_lifecycle_is_not_changed(self):
        workflow = (ROOT / ".github/workflows/life-science-knowledge.yml").read_text()
        self.assertIn("inputs.persist == true", workflow)
        self.assertNotIn("agent-handoff", workflow)

    def test_missing_or_unknown_topic_is_rejected(self):
        value = copy.deepcopy(self.value)
        value["task"]["topic_ids"].append("unapproved-agent-research")
        self.assertFalse(self.verdict(value).valid)

    def test_rejects_self_certification_or_write_authority(self):
        for field, replacement in [("authority", "ACCEPTED"), ("result", "APPLIED")]:
            with self.subTest(field=field):
                value = copy.deepcopy(self.value)
                value[field] = replacement
                self.assertFalse(self.verdict(value).valid)
        value = copy.deepcopy(self.value)
        value["observations"][0]["status"] = "VERIFIED"
        self.assertFalse(self.verdict(value).valid)

    def test_github_blob_must_be_immutable(self):
        value = copy.deepcopy(self.value)
        value["observations"][0]["source_url"] = "https://github.com/crs4/life_monitor/blob/master/README.md"
        self.assertFalse(self.verdict(value).valid)

    def test_proposals_cannot_modify_accepted_data(self):
        for path in ("data/knowledge/current.json", "../secrets.txt", "/tmp/secrets", "docs\\..\\unsafe"):
            with self.subTest(path=path):
                value = copy.deepcopy(self.value)
                value["proposed_changes"][0]["path"] = path
                self.assertFalse(self.verdict(value).valid)

    def test_unreviewed_proposal_rejected(self):
        value = copy.deepcopy(self.value)
        value["proposed_changes"][0]["review_required"] = False
        self.assertFalse(self.verdict(value).valid)

    def test_no_findings_can_be_honest_and_empty(self):
        value = copy.deepcopy(self.value)
        value["result"] = "NO_FINDINGS"
        value["observations"] = []
        value["proposed_changes"] = []
        self.assertTrue(self.verdict(value).valid)

    def test_no_findings_cannot_hide_observations(self):
        value = copy.deepcopy(self.value)
        value["result"] = "NO_FINDINGS"
        self.assertFalse(self.verdict(value).valid)

    def test_installed_tool_cli_accepts_only_a_proposal(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = evidence_main(["validate-handoff", "--input", str(EXAMPLE),
                                  "--topics", str(ROOT / "evidence/profiles/topics.json")])
        self.assertEqual(code, 0)
        self.assertIn("AGENT_HANDOFF_SHAPE_VALID_PROPOSAL_ONLY", out.getvalue())
        self.assertNotIn("EVIDENCE_VERIFIED", out.getvalue())

    def test_rejects_malformed_input(self):
        self.assertFalse(validate_agent_handoff([]).valid)
        self.assertFalse(validate_agent_handoff({"kind": "OTHER"}).valid)

    def test_valid_world_line_anchor_is_accepted(self):
        value = copy.deepcopy(self.value)
        value["base"] = {
            "commit": "809be73fed2c452a9edbc5cd02e08a8809336eac",
            "observed_at": "2026-10-17T03:46:00Z",
        }
        self.assertTrue(self.verdict(value).valid, self.verdict(value).errors)

    def test_future_base_timestamp_is_rejected(self):
        value = copy.deepcopy(self.value)
        value["base"] = {
            "commit": "809be73fed2c452a9edbc5cd02e08a8809336eac",
            "observed_at": "2099-01-01T00:00:00Z",
        }
        verdict = self.verdict(value)
        self.assertFalse(verdict.valid)
        self.assertTrue(any("observed_at" in e for e in verdict.errors))

    def test_bad_base_commit_is_rejected(self):
        value = copy.deepcopy(self.value)
        value["base"] = {"commit": "809be73", "observed_at": "2026-10-17T03:46:00Z"}
        verdict = self.verdict(value)
        self.assertFalse(verdict.valid)
        self.assertTrue(any("base.commit" in e for e in verdict.errors))

    def test_missing_base_stays_backward_compatible(self):
        self.assertTrue(self.verdict().valid)

    def test_observation_timestamp_is_validated_when_present(self):
        good = copy.deepcopy(self.value)
        good["observations"][0]["observed_at"] = "2026-10-17T03:46:00Z"
        self.assertTrue(self.verdict(good).valid, self.verdict(good).errors)
        bad = copy.deepcopy(self.value)
        bad["observations"][0]["observed_at"] = "2026-10-17 03:46:00"
        verdict = self.verdict(bad)
        self.assertFalse(verdict.valid)
        self.assertTrue(any("observed_at" in e for e in verdict.errors))


    def test_trusted_reviewer_expected_baseline_match(self):
        self.assertTrue(validate_agent_handoff(
            self.value, known_topics=TOPICS,
            expected_base_commit=self.value["base"]["commit"]).valid)

    def test_stale_agent_baseline_is_rejected_when_reviewer_has_newer_head(self):
        verdict = validate_agent_handoff(
            self.value, known_topics=TOPICS,
            expected_base_commit="272f6dfb5f805a180f9c2d7004ca7288591278e9")
        self.assertFalse(verdict.valid)
        self.assertTrue(any("STALE_BASE" in e for e in verdict.errors))

    def test_legacy_optional_base_requires_anchor_for_trusted_comparison(self):
        old = copy.deepcopy(self.value)
        del old["base"]
        self.assertTrue(self.verdict(old).valid)
        verdict = validate_agent_handoff(old, known_topics=TOPICS,
                                         expected_base_commit="2" * 40)
        self.assertFalse(verdict.valid)
        self.assertTrue(any("requires a declared base" in e for e in verdict.errors))

    def test_invalid_trusted_reviewer_baseline_rejected(self):
        verdict = validate_agent_handoff(self.value, known_topics=TOPICS,
                                         expected_base_commit="main")
        self.assertFalse(verdict.valid)
        self.assertTrue(any("40-hex trusted" in e for e in verdict.errors))

    def test_trusted_base_cli_is_distinct_from_shape_only_verdict(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "handoff.json"
            path.write_text(json.dumps(self.value))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = evidence_main(["validate-handoff", "--input", str(path),
                    "--topics", str(ROOT / "evidence/profiles/topics.json"),
                    "--expected-base-sha", self.value["base"]["commit"]])
            self.assertEqual(code, 0)
            self.assertIn("TRUSTED_BASE_MATCH", out.getvalue())
            with contextlib.redirect_stderr(io.StringIO()):
                code = evidence_main(["validate-handoff", "--input", str(path),
                    "--topics", str(ROOT / "evidence/profiles/topics.json"),
                    "--expected-base-sha", "3" * 40])
            self.assertEqual(code, 2)

    def test_optional_agent_proposer_is_self_declared_not_authenticated(self):
        value = copy.deepcopy(self.value)
        self.assertTrue(self.verdict(value).valid)
        value["proposer"] = {
            "agent_label": "Clinder", "execution_surface": "Local WorkBuddy IDE",
            "assertion": "SELF_DECLARED"
        }
        self.assertTrue(self.verdict(value).valid, self.verdict(value).errors)
        value["proposer"]["assertion"] = "GITHUB_VERIFIED"
        verdict = self.verdict(value)
        self.assertFalse(verdict.valid)
        self.assertTrue(any("SELF_DECLARED" in err for err in verdict.errors))
        value["proposer"]["assertion"] = "SELF_DECLARED"
        value["proposer"]["agent_label"] = ""
        self.assertFalse(self.verdict(value).valid)


if __name__ == "__main__":
    unittest.main()
