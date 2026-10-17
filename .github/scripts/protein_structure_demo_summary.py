"""Summarize one actual external-Agent / Tool / Workflow protein domain demonstration."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    root = a.root
    candidate = load(root / "candidate.json")
    knowledge = load(root / "knowledge.json")
    samples = load(root / "sample-audit.json")
    inspection = load(root / "openfold-inspection.json")
    sample_inspection = load(root / "proteinnet-inspection.json")
    search = load(root / "graph-search.json")
    first = load(root / "simulated-apply.json")
    second = load(root / "simulated-repeat.json")
    diagnostics = load(root / "diagnostics.json")
    discovery_status = (root / "discovery-status.txt").read_text(encoding="utf-8").strip()
    discovered = load(root / "discovery.json") if (root / "discovery.json").exists() else {"candidates": []}
    discovery_count = len(discovered.get("candidates", []))
    if any(item.get("approved") is not False or item.get("status") != "DISCOVERY_ONLY" for item in discovered.get("candidates", [])):
        raise ValueError("advisory discovery cannot approve proposed repositories")
    simulated = root / "simulated" / "data"
    events = [json.loads(x) for x in (simulated / "knowledge" / "events.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    archives = sorted((simulated / "inputs" / "archive").rglob("*.json"))
    sources = [
        {"repository": s["repository"], "commit": s["commit"], "source_id": s["source_id"]}
        for s in candidate["sources"]
    ]
    if not candidate.get("projection_eligible") or diagnostics:
        raise ValueError("source collection incomplete, fail-closed")
    if not isinstance(search.get("results"), list) or not search["results"]:
        raise ValueError("actual graph search returned no rows")
    if samples.get("verified_count") != 7:
        raise ValueError("sample audit incomplete")
    if first.get("outcome") != "APPLIED" or first.get("change_kind") != "TOPIC_PROFILE_CHANGE":
        raise ValueError("isolated state transition did not apply as predicted")
    if second.get("outcome") != "NO_MEANINGFUL_DELTA":
        raise ValueError("isolated no-change replay failed")
    if len(events) != 2 or len(archives) != 1:
        raise ValueError("isolated event/archival contract was not demonstrated")
    if events[1]["previous_event_sha256"] != events[0]["event_sha256"]:
        raise ValueError("event hash chain has a broken link")
    result = {
        "schema_version": "1.0.0",
        "kind": "EXTERNAL_AGENT_PROTEIN_STRUCTURE_FULL_STACK_FIELD_DEMO",
        "outcome": "READ_ONLY_REAL_SOURCES_AND_ISOLATED_LIFECYCLE_VERIFIED",
        "execution": {"run_id": os.environ.get("GITHUB_RUN_ID"), "attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
                      "head_sha": os.environ.get("GITHUB_SHA"), "event": os.environ.get("GITHUB_EVENT_NAME")},
        "external_agent": {"handoff": "PROPOSAL_ONLY", "shape_checked": True,
                           "research_topic": "protein structure prediction; variant effects kept distinct",
                           "authority": "NO_AUTOMATIC_PROMOTION"},
        "native_tool": {"source_count": len(sources), "record_count": len(candidate["records"]),
                        "snapshot_id": candidate["run_id"], "evidence_digest": candidate["output_digest"],
                        "source_diagnostics": diagnostics, "sources": sources, "discovery_status": discovery_status, "unapproved_discovery_candidates": discovery_count,
                        "inspection": {"OpenFold": {"status": inspection["status"], "counts": inspection["counts"]},
                                       "ProteinNet": {"status": sample_inspection["status"], "counts": sample_inspection["counts"]}}},
        "native_workflow": {"knowledge_digest": knowledge["knowledge_digest"],
                            "topic_coverage": [{"topic": x["topic_id"],"status":x["coverage"],
                                                "fragments":x["fragment_count"],"sources":x["source_count"]} for x in knowledge["topics"]],
                            "graph_nodes":len(knowledge["knowledge_graph"]["nodes"]),
                            "graph_edges":len(knowledge["knowledge_graph"]["edges"]),
                            "fts5_search_hits":len(search["results"]),
                            "offline_cwl_replay": True},
        "pinned_data_samples": {"count":samples["verified_count"],
                                "objects":[{"id":x["id"],"repository":x["repository"],"commit":x["commit"],
                                            "blob_sha":x["blob_sha"],"sha256":x["content_sha256"],
                                            "format":x["format"],"role":x["role"],"bytes":x["bytes"]}
                                           for x in samples["samples"]]},
        "isolated_lifecycle": {"first_outcome":first["outcome"],"change_kind":first["change_kind"],
                               "replay_outcome":second["outcome"],"archived_previous_snapshots":len(archives),
                               "event_count":len(events),"chain_verified":True,
                               "persistent_main_mutation":False},
        "not_claimed": ["protein structure inference or training","biological correctness or benchmark-score validation",
                        "full CASP/ProteinNet dataset acquisition","external registration","production data acceptance"],
    }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"outcome":result["outcome"],"sources":len(sources),
                      "records":len(candidate["records"]), "sample_objects":samples["verified_count"],
                      "search_hits":len(search["results"]), "isolated_events":len(events)},sort_keys=True))


if __name__ == "__main__":
    main()
