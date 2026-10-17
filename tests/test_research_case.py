"""Same methodological envelope must apply across unrelated research domains."""
from __future__ import annotations

import copy
import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from evidence.cli import main as evidence_main
from evidence.research_case import STAGES, research_case_shape_report, validate_research_case

ROOT = Path(__file__).resolve().parents[1]
SOFTWARE_COMMIT = "57f328acbcf051a44c2ba1c376952af57a84c68e"


def specimen(domain: str, input_name: str) -> dict:
    stages = {name: {"state": "PENDING"} for name in STAGES}
    stages["DEFINE"] = {"state": "REPORTED", "evidence_refs": ["protocol:research-question"]}
    stages["PIN"] = {"state": "REPORTED", "evidence_refs": ["input:sha256"]}
    return {
        "schema_version": "1.0.0", "kind": "RESEARCH_CASE_PROPOSAL",
        "case_id": "replaceable-" + input_name,
        "domain": domain, "question": "Can the supplied input be processed under a reproducible method?",
        "authority": "PROPOSAL_ONLY", "stages": stages,
        "inputs": [{"name": "input_one", "scope": "LOCAL_FIXTURE",
                    "sha256": hashlib.sha256(input_name.encode()).hexdigest(), "format": "local fixture"}],
        "method": {"name": "reference-adapter", "version": "1.0.0", "role": "DATA_QA",
                   "software_commit": SOFTWARE_COMMIT,
                   "parameters_sha256": hashlib.sha256(b"{}").hexdigest()},
        "execution": {"state": "NOT_RUN"},
        "evaluation": {"state": "NOT_EVALUATED", "metrics": []},
        "limitations": ["No domain truth or external execution is established by this proposal"],
        "review": {"authority": "HUMAN_REQUIRED", "status": "PENDING"},
    }


class MethodologyContractTests(unittest.TestCase):
    def test_same_core_contract_for_unrelated_scientific_research(self):
        for domain, name in (("Protein sequence method", "protein"), ("Scientific workflow version audit", "workflow")):
            with self.subTest(domain=domain):
                case = specimen(domain, name)
                result = research_case_shape_report(case)
                self.assertEqual(result["status"], "PASS", result["errors"])
                self.assertEqual(result["methodology"], list(STAGES))
                self.assertEqual(result["assurance"], "PROPOSAL_SHAPE_ONLY")
                self.assertEqual(result, research_case_shape_report(copy.deepcopy(case)))

    def test_agent_cannot_self_approve_or_skip_review(self):
        example = specimen("Independent scientific process", "assay")
        for value in ("ACCEPTED", "AUTOMATICALLY_VERIFIED"):
            case = copy.deepcopy(example)
            case["authority"] = value
            self.assertFalse(validate_research_case(case).valid)
        case = copy.deepcopy(example)
        case["review"] = {"authority": "AGENT", "status": "APPROVED"}
        self.assertFalse(validate_research_case(case).valid)

    def test_methodology_stage_names_are_fixed_not_domain_dependent(self):
        case = specimen("Any domain", "generic")
        case["stages"].pop("REPLAY")
        self.assertFalse(validate_research_case(case).valid)
        case["stages"]["SCORE_PROTEIN"] = {"state": "REPORTED"}
        self.assertFalse(validate_research_case(case).valid)

    def test_claims_of_execution_require_reproducibility_digests(self):
        case = specimen("Any domain", "generic")
        case["execution"] = {"state": "REPORTED_RUN"}
        self.assertFalse(validate_research_case(case).valid)
        case["execution"].update({
            "environment_sha256": hashlib.sha256(b"python 3.12").hexdigest(),
            "report_sha256": hashlib.sha256(b"test output").hexdigest(),
        })
        self.assertTrue(validate_research_case(case).valid)
        case["evaluation"] = {"state": "REPORTED_UNVERIFIED", "metrics": [
            {"name": "availability", "value": 0.95, "unit": "proportion", "reference_type": "NONE"}
        ]}
        self.assertTrue(validate_research_case(case).valid)
        self.assertEqual(research_case_shape_report(case)["assurance"], "PROPOSAL_SHAPE_ONLY")

    def test_false_nonfinite_metric_and_reference_free_accuracy_claim_shape(self):
        case = specimen("Generic", "generic")
        case["execution"] = {"state": "REPORTED_RUN", "environment_sha256": "a" * 64,
                             "report_sha256": "b" * 64}
        case["evaluation"] = {"state": "REPORTED_UNVERIFIED", "metrics": [
            {"name": "score", "value": float("nan"), "unit": "fraction", "reference_type": "PEER_MODEL"}
        ]}
        self.assertFalse(validate_research_case(case).valid)
        case["evaluation"]["metrics"][0]["value"] = 0.5
        self.assertTrue(validate_research_case(case).valid)
        self.assertIn("scientific conclusions", " ".join(research_case_shape_report(case)["not_verified"]))

    def test_unpinned_external_source_rejected(self):
        case = specimen("Generic", "generic")
        case["inputs"][0].update({"scope": "PINNED_EXTERNAL", "uri": "https://github.com/test/example",
                                  "revision": "main"})
        self.assertFalse(validate_research_case(case).valid)
        case["inputs"][0]["revision"] = "1" * 40
        self.assertTrue(validate_research_case(case).valid)

    def test_reported_stage_needs_evidence_and_blocked_stage_needs_reason(self):
        case = specimen("Generic", "generic")
        case["stages"]["AUDIT"] = {"state": "REPORTED"}
        self.assertFalse(validate_research_case(case).valid)
        case["stages"]["AUDIT"] = {"state": "BLOCKED", "reason": "Missing independent validator"}
        self.assertTrue(validate_research_case(case).valid)

    def test_installed_evidence_cli_returns_bounded_report_without_promotion(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "case.json"
            out = Path(tmp) / "report.json"
            inp.write_text(json.dumps(specimen("Independent workflow", "independent")))
            with redirect_stdout(io.StringIO()) as printed:
                rc = evidence_main(["validate-research-case", "--input", str(inp), "--output", str(out)])
            self.assertEqual(rc, 0)
            self.assertIn("PROPOSAL_SHAPE_ONLY", printed.getvalue())
            self.assertEqual(json.loads(out.read_text())["status"], "PASS")
            bad = specimen("Independent workflow", "independent")
            bad["review"]["status"] = "APPROVED"
            inp.write_text(json.dumps(bad))
            with redirect_stdout(io.StringIO()):
                rc = evidence_main(["validate-research-case", "--input", str(inp), "--output", str(out)])
            self.assertEqual(rc, 1)
            self.assertIn("human-authoritative", " ".join(json.loads(out.read_text())["errors"]))


if __name__ == "__main__":
    unittest.main()
