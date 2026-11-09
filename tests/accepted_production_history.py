"""Test-only authority bridge: frozen file ledgers vs verified new native data/ appends.

Never admits arbitrary unpinned data/ paths. Works on offline, current Git bytes,
checks every accepted Receipt/event and reconstructed previous-Candidate archive.
"""
import json
from pathlib import Path

from life_science_ecosystem_lab.lifecycle.state import StateRoots, verify_state


def authorized_native_append_paths(root: Path) -> set[str]:
    verification = verify_state(StateRoots(root), require_accepted=True)
    if not verification.valid:
        raise AssertionError("CURRENT_ACCEPTED_STATE_INVALID: " + str(verification.errors))

    ledger = root / "data/knowledge/events.jsonl"
    events = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()
              if line.strip()]
    if not events:
        raise AssertionError("NO_ACCEPTED_EVENTS")

    receipt_dir = root / "data/receipts"
    actual_receipts = {path.relative_to(root).as_posix()
                       for path in receipt_dir.glob("*.json")}
    expected_receipts: set[str] = set()
    for i, event in enumerate(events):
        run_id = event["run_id"]
        if not isinstance(run_id, str) or not run_id.startswith("gh-"):
            raise AssertionError("UNRECOGNIZED_ACCEPTANCE_RUN")
        if event["outcome"] != "APPLIED":
            raise AssertionError("NON_ACCEPTED_LEDGER_EVENT")
        if i and event["previous_event_sha256"] != events[i - 1]["event_sha256"]:
            raise AssertionError("EVENT_CHAIN_BROKEN")
        receipt_path = f"data/receipts/{run_id}.json"
        expected_receipts.add(receipt_path)
        receipt = json.loads((root / receipt_path).read_text(encoding="utf-8"))
        for receipt_field, event_field in (
            ("execution_id", "run_id"),
            ("snapshot_id", "snapshot_id"),
            ("output_digest", "evidence_digest"),
            ("logical_date", "logical_date"),
            ("change_kind", "change_kind"),
        ):
            if receipt.get(receipt_field) != event.get(event_field):
                raise AssertionError("RECEIPT_EVENT_MISMATCH: " + receipt_field)
        if receipt.get("outcome") != "APPLIED":
            raise AssertionError("NON_APPLIED_RECEIPT")

    if actual_receipts != expected_receipts:
        raise AssertionError("UNRECONCILED_RECEIPT_PATHS")

    archive_root = root / "data/inputs/archive"
    actual_archives = {path.relative_to(root).as_posix()
                       for path in archive_root.rglob("*.json")}
    expected_archives: set[str] = set()
    for previous, accepted in zip(events, events[1:]):
        year, month, _ = accepted["logical_date"].split("-")
        archive = ("data/inputs/archive/" + year + "/" + month + "/" +
                   previous["snapshot_id"] + "-" + previous["evidence_digest"][:12] + ".json")
        archived = json.loads((root / archive).read_text(encoding="utf-8"))
        if (archived.get("run_id") != previous["snapshot_id"] or
                archived.get("output_digest") != previous["evidence_digest"]):
            raise AssertionError("ARCHIVED_PREVIOUS_CANDIDATE_MISMATCH")
        expected_archives.add(archive)
    if actual_archives != expected_archives:
        raise AssertionError("UNRECONCILED_ARCHIVE_PATHS")

    return expected_receipts | expected_archives
