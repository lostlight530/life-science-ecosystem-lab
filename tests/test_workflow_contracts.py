import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WorkflowContractTests(unittest.TestCase):
    def test_cwl_installs_tool_instead_of_staging_repo_root(self):
        cwl = (ROOT / ".github" / "knowledge" / "main.cwl").read_text(encoding="utf-8")
        job = (ROOT / ".github" / "knowledge" / "test" / "workflow-job.yml").read_text(encoding="utf-8")
        self.assertNotIn("python_package", cwl + job)
        for command in ("aggregate", "validate", "knowledge", "verify-knowledge"):
            doc = (ROOT / ".github" / "knowledge" / "tools" / f"{command}.cwl").read_text(encoding="utf-8")
            self.assertNotIn("python_package", doc)

    def test_cwl_executes_peer_tool_not_legacy_nested_command(self):
        for command in ("aggregate", "validate"):
            doc = (ROOT / ".github" / "knowledge" / "tools" / f"{command}.cwl").read_text(encoding="utf-8")
            self.assertIn("baseCommand: [python3, -m, evidence]", doc)
            self.assertNotIn("  - evidence\n", doc)

    def test_lifecycle_has_split_permissions_and_ordered_guards(self):
        text = (ROOT / ".github" / "workflows" / "life-science-knowledge.yml").read_text(encoding="utf-8")
        self.assertIn("validate:", text)
        self.assertIn("apply:", text)
        self.assertIn("needs: validate", text)
        self.assertIn("contents: read", text)
        self.assertIn("contents: write", text)
        self.assertIn("check_write_boundary.py", text)
        self.assertIn("verify_world_line.py", text)
        self.assertLess(text.index("evidence collect"), text.index("evidence aggregate"))
        self.assertLess(text.index("lifecycle apply"), text.index("Final validation"))
        uses = re.findall(r"uses:\s*[^@\s]+@([^\s#]+)", text)
        self.assertTrue(uses)
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{40}", value) for value in uses))

    def test_native_write_requires_manual_or_schedule_and_checks_remote_after_push(self):
        workflow = (ROOT / ".github" / "workflows" / "life-science-knowledge.yml").read_text(encoding="utf-8")
        self.assertNotIn("  push:", workflow)
        self.assertIn("github.event_name == 'schedule'", workflow)
        self.assertIn("inputs.persist == true", workflow)
        self.assertIn("Verify remote accepted state matches local commit", workflow)
        self.assertIn('verify_world_line.py --validated-head "$(git rev-parse HEAD)"', workflow)
        self.assertIn("Preserve bounded diagnostics on validation failure", workflow)
        self.assertIn("if: failure()", workflow)
        self.assertIn("build/source-diagnostics.json", workflow)

    def test_knowledge_profiles_are_closed_and_only_native_can_persist(self):
        workflow = (ROOT / ".github" / "workflows" / "life-science-knowledge.yml").read_text(encoding="utf-8")
        self.assertIn("profile:", workflow)
        self.assertIn("- native", workflow)
        self.assertIn("- protein_structure", workflow)
        self.assertIn("python -m evidence.workflow_profiles", workflow)
        self.assertIn("$LS_SOURCES_PROFILE", workflow)
        self.assertIn("$LS_TOPICS_PROFILE", workflow)
        self.assertIn("inputs.profile == 'native'", workflow)
        self.assertIn("build/workflow-profile.json", workflow)

    def test_daily_institutional_observation_is_not_gated_by_project_contract_tests(self):
        text = (ROOT / ".github" / "workflows" / "life-science-daily-selfcheck.yml").read_text(encoding="utf-8")
        institutional = text.split("  institutional-defaults:", 1)[1].split("  project-custom:", 1)[0]
        project = text.split("  project-custom:", 1)[1]
        self.assertIn("test_institutional_selfcheck.py", institutional)
        self.assertNotIn("test_project_selfcheck.py", institutional)
        self.assertNotIn("unittest discover -s tests -v", institutional)
        self.assertIn("python -m evidence.daily_custom_runner", project)
        self.assertIn("checks/project/daily_checks.json", project)
        runner = (ROOT / "evidence" / "daily_custom_runner.py").read_text(encoding="utf-8")
        self.assertIn('"regression": [py, "-m", "unittest", "discover", "-s", "tests", "-v"]', runner)
        self.assertIn("all original required validation gates", runner)
        self.assertIn("for entry in checks:", runner)
        self.assertNotIn("needs:", institutional)
        self.assertNotIn("needs:", project)
        self.assertIn("permissions:\n  contents: read", text)
        self.assertIn("persist-credentials: false", institutional)
        self.assertNotIn("workflow_profiles", text)
        self.assertNotIn("protein_structure", text)

    def test_validation_workflow_checks_profiles_and_caches(self):
        text = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
        self.assertIn("validate-source-registry", text)
        self.assertIn("validate-topic-registry", text)
        self.assertIn("Generated cache files are not allowed", text)

    def test_required_validation_domains_are_independent_and_actor_neutral(self):
        text = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
        jobs = text.split("jobs:", 1)[1]
        verdict = jobs.split("  gate-verdict:", 1)[1]
        independent = jobs.split("  gate-verdict:", 1)[0]
        for job in ("repository-contracts", "knowledge-workflow", "evidence-tool", "portable-package"):
            self.assertIn(f"  {job}:\n", independent)
            block = independent.split(f"  {job}:\n", 1)[1]
            self.assertNotIn("\n    needs:", block.split("\n  ", 1)[0])
        self.assertNotIn("github.actor", text)
        self.assertNotIn("continue-on-error", text)
        self.assertNotIn("\n    paths:", text.split("jobs:", 1)[0])
        self.assertIn(
            "needs: [repository-contracts, knowledge-workflow, evidence-tool, portable-package]",
            verdict,
        )
        self.assertIn("name: validate", verdict)
        self.assertIn("if: ${{ !cancelled() }}", verdict)

    def test_validation_retains_diagnostics_without_weakening_verdict(self):
        text = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count("if: ${{ always() }}"), 4)
        self.assertIn("Repository contracts result", text)
        self.assertIn("Knowledge Workflow result", text)
        self.assertIn("Evidence Tool result", text)
        self.assertIn("Portable package result", text)
        self.assertIn("exit 1", text.split("  gate-verdict:", 1)[1])


if __name__ == "__main__":
    unittest.main()
