"""Publish bounded real-world drill evidence without redistributing upstream source text."""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path


TARGETS = {
    "nf-core/rnaseq": "95dbcd977a74a4d1b2a3954abb90df3851014afa",
    "crs4/life_monitor": "7649406c11c5c04eebc5ca61926f5dbe30469c82",
}


def load(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--knowledge", type=Path, required=True)
    parser.add_argument("--rnaseq-report", type=Path, required=True)
    parser.add_argument("--lifemonitor-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    candidate = load(args.candidate)
    knowledge = load(args.knowledge)
    reports = {
        "nf-core/rnaseq": load(args.rnaseq_report),
        "crs4/life_monitor": load(args.lifemonitor_report),
    }
    counts = Counter(str(record["source_id"]) for record in candidate["records"])
    sources = [
        {
            "source_id": source["source_id"],
            "repository": source["repository"],
            "observed_commit": source["commit"],
            "document_count": counts[source["source_id"]],
        }
        for source in candidate["sources"]
    ]
    external = {}
    for name, report in reports.items():
        external[name] = {
            "pinned_commit": TARGETS[name],
            "status": report["status"],
            "counts": report["counts"],
            "report_sha256": report["report_sha256"],
            "observed_files": report["observed_files"],
            "findings": report["findings"],
            "unverified": report["unverified"],
        }
    diagnostics = [
        {"source_id": str(d.get("source_id", "")),
         "reason": str(d.get("reason", ""))}
        for d in candidate["diagnostics"]
    ]
    eligible = bool(candidate["projection_eligible"])
    observed = bool(candidate["records"])
    result = {
        "schema_version": "1.0.0",
        "kind": "LIVE_GITHUB_READ_ONLY_EVIDENCE_DRILL",
        "execution": {
            "repository": os.environ.get("GITHUB_REPOSITORY"),
            "ref": os.environ.get("GITHUB_REF"),
            "commit": os.environ.get("GITHUB_SHA"),
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        },
        "scope": "real public GitHub source collection plus static inspection of two pinned external repositories",
        "production_persisted": False,
        "untrusted_source_code_executed": False,
        "source_evidence": {
            "snapshot_id": candidate["run_id"],
            "input_digest": candidate["input_digest"],
            "output_digest": candidate["output_digest"],
            "eligible_for_projection": eligible,
            "records": len(candidate["records"]),
            "sources": sources,
            "diagnostics": diagnostics,
        },
        "knowledge": {
            "knowledge_digest": knowledge["knowledge_digest"],
            "source_count": knowledge["source_count"],
            "record_count": knowledge["record_count"],
            "topic_coverage": [
                {"topic_id": t["topic_id"],
                 "coverage": t["coverage"],
                 "fragments": t["fragment_count"],
                 "source_count": t["source_count"]}
                for t in knowledge["topics"]
            ],
            "node_count": len(knowledge["knowledge_graph"]["nodes"]),
            "edge_count": len(knowledge["knowledge_graph"]["edges"]),
        },
        "external_inspections": external,
        "outcome": "READ_ONLY_EVIDENCE_COMPLETE" if eligible and observed and all(r["status"] in ("PASS", "WARN", "FAIL") for r in reports.values())
        else "SOURCE_INELIGIBLE_OR_INCOMPLETE",
        "interpretation_limits": [
            "This is a live read-only observation, not an accepted main-branch knowledge commit",
            "Static inspection does not run external tools or verify biological conclusions",
            "PASS/WARN/FAIL reflect only the Evidence Tool's bounded preflight rules",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"outcome": result["outcome"], "record_count": len(candidate["records"]),
                      "sources": sources,
                      "diagnostics": diagnostics,
                      "external_status": {k: v["status"] for k, v in external.items()},
                      "knowledge": result["knowledge"]}, sort_keys=True))
    return 0 if result["outcome"] == "READ_ONLY_EVIDENCE_COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
