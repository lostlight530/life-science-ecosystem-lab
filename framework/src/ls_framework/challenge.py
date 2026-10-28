"""Reproducible adversarial challenge for the LS cross-domain software contract.

The challenge is about software-engineering error detection, not biological
validity, data-set benchmarking, or a verified scientific observation.
All cases derive from one synthetic fixture, without network or external tools.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Callable

from .engine import assess, canonical_digest
from .paths import resolve_report_target, write_report_atomically

Mutation = Callable[[dict[str, Any]], None]


def _sha_swap(b: dict[str, Any]) -> None:
    b["assets"][0]["sha256"] = b["assets"][1]["sha256"]


def _wrong_scope(b: dict[str, Any]) -> None:
    b["scope"] = "ALL_SCIENCES"


def _unknown_domain(b: dict[str, Any]) -> None:
    b["assets"][0]["domain"] = "astrophysics"


def _narrow_method(b: dict[str, Any]) -> None:
    b["steps"][0]["supported_domains"] = ["genomics", "life_sciences_integrative"]


def _missing_lineage(b: dict[str, Any]) -> None:
    b["steps"] = []


def _empty_bundle(b: dict[str, Any]) -> None:
    b["steps"] = []
    b["assets"] = []


def _multiple_producers(b: dict[str, Any]) -> None:
    second = copy.deepcopy(b["steps"][0])
    second["id"] = "second-producer"
    b["steps"].append(second)


def _cycle(b: dict[str, Any]) -> None:
    original = b["steps"][0]
    b["steps"].append({
        "id": "cycle-step",
        "method": copy.deepcopy(original["method"]),
        "inputs": ["a-integrated"],
        "outputs": ["a-genomics"],
        "supported_domains": ["life_sciences_integrative", "genomics"],
        "outcome": "SUCCEEDED",
    })


def _escaping_path(b: dict[str, Any]) -> None:
    b["assets"][0]["path"] = "../outside.json"


def _unverified_external(b: dict[str, Any]) -> None:
    del b["assets"][0]["path"]


def _failed_step(b: dict[str, Any]) -> None:
    b["steps"][0]["outcome"] = "FAILED"


def _unknown_input(b: dict[str, Any]) -> None:
    b["steps"][0]["inputs"][0] = "missing-asset"


def _unlinked_asset(b: dict[str, Any]) -> None:
    b["steps"][0]["outputs"] = ["a-imaging"]
    b["steps"][0]["inputs"] = ["a-genomics"]
    b["steps"][0]["supported_domains"] = ["genomics", "microscopy"]


def _claim(b: dict[str, Any]) -> None:
    b["claims"] = [{
        "id": "unverified-claim",
        "statement": "Synthetic data establish a biological result",
        "evidence": ["a-integrated"],
        "authority": "PROPOSAL_ONLY",
    }]


def _authority_escalation(b: dict[str, Any]) -> None:
    _claim(b)
    b["claims"][0]["authority"] = "ACCEPTED"


def _method_checksum(b: dict[str, Any]) -> None:
    b["steps"][0]["method"]["sha256"] = "not-a-sha256"


def _missing_method_output(b: dict[str, Any]) -> None:
    b["steps"][0]["outputs"] = []


def _metabolomics_metadata(b: dict[str, Any]) -> None:
    """Legal domain rename only; the files are still synthetic JSON."""
    b["assets"][0]["domain"] = "metabolomics"
    b["steps"][0]["supported_domains"] = [
        "metabolomics", "microscopy", "life_sciences_integrative",
    ]


# Reviewed cases are explicit, deterministic and independent of a single assay.
# Each expected finding is an engine contract assertion, not ground truth about biology.
CASES: tuple[tuple[str, Mutation | None, str, str | None], ...] = (
    ("nominal_contract", None, "PASS", None),
    ("renamed_supported_domain", _metabolomics_metadata, "PASS", None),
    ("swapped_file_digest", _sha_swap, "FAIL", "LOCAL_DIGEST_MISMATCH"),
    ("out_of_scope", _wrong_scope, "FAIL", "INVALID_BUNDLE_CONTRACT"),
    ("unreviewed_domain", _unknown_domain, "FAIL", "UNREVIEWED_DOMAIN"),
    ("method_domain_gap", _narrow_method, "FAIL", "METHOD_DOMAIN_MISMATCH"),
    ("missing_lineage", _missing_lineage, "FAIL", "MISSING_LINEAGE_STEPS"),
    ("empty_evidence", _empty_bundle, "FAIL", "EMPTY_ASSET_SET"),
    ("duplicate_producer", _multiple_producers, "FAIL", "MULTIPLE_PRODUCERS"),
    ("lineage_cycle", _cycle, "FAIL", "LINEAGE_CYCLE"),
    ("path_escape", _escaping_path, "FAIL", "UNSAFE_PATH"),
    ("external_unverified", _unverified_external, "INDETERMINATE", None),
    ("failed_execution_declaration", _failed_step, "INDETERMINATE", "NON_SUCCESSFUL_EXECUTION_RECORDED"),
    ("unknown_asset_reference", _unknown_input, "FAIL", "UNKNOWN_ASSET_REFERENCE"),
    ("unlinked_asset", _unlinked_asset, "INDETERMINATE", "UNLINKED_ASSET"),
    ("scientific_proposal", _claim, "INDETERMINATE", "SCIENTIFIC_CLAIM_NOT_ADJUDICATED"),
    ("science_authority_escalation", _authority_escalation, "FAIL", "SCIENTIFIC_AUTHORITY_ESCALATION"),
    ("invalid_method_digest", _method_checksum, "FAIL", "INVALID_METHOD_IDENTITY"),
    ("missing_step_output", _missing_method_output, "FAIL", "INVALID_STEP_PORTS"),
)


def run_challenge(bundle: dict[str, Any], root: Path) -> dict[str, Any]:
    """Run all fixed contract challenges; a missing expected detection is FAIL."""
    results: list[dict[str, Any]] = []
    for case_id, mutation, expected_status, expected_finding in CASES:
        candidate = copy.deepcopy(bundle)
        try:
            if mutation is not None:
                mutation(candidate)
            assessment = assess(candidate, root)
            observed = assessment["status"]
            observed_codes = sorted(
                {entry["code"] for entry in assessment["errors"] + assessment["warnings"]}
            )
            correct = (observed == expected_status and
                       (expected_finding is None or expected_finding in observed_codes))
        except (KeyError, IndexError, TypeError, ValueError, RecursionError):
            observed = "ERROR"
            observed_codes = ["CASE_EXECUTION_ERROR"]
            correct = False
        results.append({
            "id": case_id,
            "case_bundle_sha256": canonical_digest(candidate),
            "expected_status": expected_status,
            "expected_finding": expected_finding,
            "observed_status": observed,
            "observed_findings": observed_codes,
            "matched": correct,
        })
    mismatches = [item["id"] for item in results if not item["matched"]]
    return {
        "kind": "LS_RSE_CONTRACT_CHALLENGE",
        "schema_version": "0.1.0",
        "benchmark_type": "SYNTHETIC_SOFTWARE_CONTRACT_MUTATION",
        "source_bundle_sha256": canonical_digest(bundle),
        "status": "FAIL" if mismatches else "PASS",
        "counts": {
            "cases": len(results),
            "matched": len(results) - len(mismatches),
            "mismatched": len(mismatches),
            "expected_fail": sum(x["expected_status"] == "FAIL" for x in results),
            "expected_indeterminate": sum(x["expected_status"] == "INDETERMINATE" for x in results),
            "expected_pass": sum(x["expected_status"] == "PASS" for x in results),
        },
        "mismatches": mismatches,
        "cases": results,
        "nonclaims": [
            "These are synthetic software-contract mutations, not life-sciences samples",
            "Agreement with authored expectations is not an independent accuracy estimate",
            "No biological inference, method execution attestation or certification was performed",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline synthetic LS software-contract challenge")
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    output_target = None
    try:
        input_root = args.root.resolve(strict=True)
        output_target = resolve_report_target(args.output, args.bundle, input_root)
        payload = args.bundle.read_bytes()
        if len(payload) > 256_000:
            raise ValueError("bundle exceeds 256 KB")

        def no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            unique: dict[str, Any] = {}
            for key, value in pairs:
                if key in unique:
                    raise ValueError("duplicate JSON object key")
                unique[key] = value
            return unique

        def reject_nonfinite(value: str) -> None:
            raise ValueError(f"non-finite JSON number: {value}")

        bundle = json.loads(
            payload,
            object_pairs_hook=no_duplicate_keys,
            parse_constant=reject_nonfinite,
        )
        if not isinstance(bundle, dict):
            raise ValueError("bundle root must be JSON object")
        required_keys = {"kind", "schema_version", "scope", "assets", "steps", "claims"}
        if set(bundle) != required_keys:
            raise ValueError("bundle shape does not match the challenge contract")
        if not all(isinstance(bundle[key], list) for key in ("assets", "steps", "claims")):
            raise ValueError("bundle collections must be JSON arrays")
        result = run_challenge(bundle, input_root)
    except (OSError, ValueError, TypeError, KeyError, IndexError, RecursionError):
        result = {
            "kind": "LS_RSE_CONTRACT_CHALLENGE",
            "schema_version": "0.1.0",
            "status": "FAIL",
            "mismatches": ["INPUT_ERROR"],
        }
    output = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    if output_target is not None:
        try:
            write_report_atomically(output_target, output)
        except OSError as error:
            result = {
                "kind": "LS_RSE_CONTRACT_CHALLENGE",
                "schema_version": "0.1.0",
                "status": "FAIL",
                "mismatches": ["OUTPUT_ERROR"],
                "error_type": type(error).__name__,
            }
            output = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
            print(output, end="")
            return 1
    print(output, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
