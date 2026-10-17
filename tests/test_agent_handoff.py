"""Offline tests for bounded optional external-Agent handoff contracts."""
import copy
import json
import unittest
from pathlib import Path

from evidence.agent_handoff import validate_agent_handoff

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

    def test_rejects_malformed_input(self):
        self.assertFalse(validate_agent_handoff([]).valid)
        self.assertFalse(validate_agent_handoff({"kind": "OTHER"}).valid)


if __name__ == "__main__":
    unittest.main()
