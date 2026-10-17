"""Read-only verification of *pinned* public protein examples in GitHub.

No upstream model code, predictions, training, weights, or bulk datasets run.
The resulting artifact contains digests and structural metadata, not raw sequences.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

MAX_BYTES = 400_000
HEX40 = re.compile(r"[0-9a-f]{40}")
SAFE_PATH = re.compile(r"[A-Za-z0-9_.\-/]+")
FORMATS = {"FASTA", "PDB", "JSON"}
ROLES = {"example_sequence", "predicted_structure", "benchmark_prediction", "inference_input", "variant_effect_example"}


def request(url: str) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "life-science-protein-demo"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        return json.load(response)


def parse_sample(raw: bytes, kind: str) -> dict:
    content = raw.decode("utf-8")
    if kind == "FASTA":
        rows = [x.strip() for x in content.splitlines() if x.strip()]
        if not rows or not rows[0].startswith(">"):
            raise ValueError("FASTA header missing")
        sequence = "".join(x for x in rows if not x.startswith(">"))
        if not sequence or re.fullmatch(r"[A-Za-z*.\-]+", sequence) is None:
            raise ValueError("invalid FASTA sequence")
        return {"sequence_length": len(sequence), "format_verified": True}
    if kind == "PDB":
        atoms = [row for row in content.splitlines() if row.startswith(("ATOM  ", "HETATM"))]
        if not atoms:
            raise ValueError("PDB lacks ATOM/HETATM records")
        for row in atoms:
            if len(row) < 54:
                raise ValueError("truncated PDB coordinate record")
            for span in ((30, 38), (38, 46), (46, 54)):
                float(row[span[0]:span[1]])
        return {"atom_records": len(atoms), "format_verified": True}
    if kind == "JSON":
        data = json.loads(content)
        if not isinstance(data, dict) or not isinstance(data.get("sequences"), list):
            raise ValueError("not a compatible protein input example")
        proteins = [x["protein"] for x in data["sequences"] if isinstance(x, dict) and isinstance(x.get("protein"), dict)]
        if not proteins or not all(re.fullmatch(r"[A-Z]+", p.get("sequence", "")) for p in proteins):
            raise ValueError("missing protein sequences in prediction input")
        return {"protein_chains": len(proteins), "sequence_lengths": [len(p["sequence"]) for p in proteins], "format_verified": True}
    raise ValueError("unsupported format")


def audit(manifest: dict) -> dict:
    if manifest.get("kind") != "PINNED_PROTEIN_RESEARCH_DATA_SAMPLE_MANIFEST":
        raise ValueError("invalid sample manifest identity")
    samples = manifest.get("samples")
    if not isinstance(samples, list) or not (1 <= len(samples) <= 20):
        raise ValueError("bounded samples required")
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    ids = set()
    for sample in samples:
        if sample["id"] in ids or not isinstance(sample["id"], str):
            raise ValueError("duplicate sample ID")
        ids.add(sample["id"])
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", sample["repository"]):
            raise ValueError("invalid repository")
        if not HEX40.fullmatch(sample["commit"]) or not HEX40.fullmatch(sample["blob_sha"]):
            raise ValueError("unpinned sample")
        if (not SAFE_PATH.fullmatch(sample["path"]) or sample["path"].startswith("/")
                or ".." in sample["path"].split("/")):
            raise ValueError("unsafe sample path")
        if sample["format"] not in FORMATS or sample["role"] not in ROLES:
            raise ValueError("unrecognized sample class")
        if not (0 < sample["bytes"] <= MAX_BYTES):
            raise ValueError("sample outside bounded size")
        grouped[(sample["repository"], sample["commit"])].append(sample)
    observations = []
    for (repo, commit), subset in sorted(grouped.items()):
        tree = request(f"https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1")
        if tree.get("truncated") or not isinstance(tree.get("tree"), list):
            raise ValueError("GitHub source tree missing or truncated")
        entries = {row["path"]: row for row in tree["tree"] if row.get("type") == "blob"}
        for sample in subset:
            path, blob = sample["path"], sample["blob_sha"]
            obj = entries.get(path)
            if not obj or obj.get("sha") != blob or obj.get("size") != sample["bytes"]:
                raise ValueError(f"commit tree identity mismatch: {repo}:{path}")
            git_blob = request(f"https://api.github.com/repos/{repo}/git/blobs/{blob}")
            if git_blob.get("encoding") != "base64" or git_blob.get("sha") != blob:
                raise ValueError("unexpected GitHub blob envelope")
            raw = base64.b64decode(git_blob["content"], validate=False)
            if len(raw) != sample["bytes"]:
                raise ValueError("raw object size mismatch")
            checksum = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            if checksum != blob:
                raise ValueError("raw Git blob identity mismatch")
            details = parse_sample(raw, sample["format"])
            observations.append({
                "id": sample["id"], "repository": repo, "commit": commit,
                "path": path, "blob_sha": blob,
                "bytes": len(raw), "content_sha256": hashlib.sha256(raw).hexdigest(),
                "format": sample["format"], "role": sample["role"], **details,
            })
    return {
        "schema_version": "1.0.0",
        "kind": "PINNED_GITHUB_PROTEIN_SAMPLE_AUDIT",
        "status": "VERIFIED_GIT_OBJECT_AND_FILE_FORMAT",
        "verified_count": len(observations),
        "samples": sorted(observations, key=lambda x: x["id"]),
        "bounds": [
            "Does not recalculate benchmark quality metrics",
            "Does not verify a biological prediction against experimental ground truth",
            "Does not infer license rights to redistribute data or model weights",
            "No protein inference, GPU training or external code execution"
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = audit(json.loads(args.manifest.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "verified_count": result["verified_count"],
                      "sample_ids": [x["id"] for x in result["samples"]]}, sort_keys=True))


if __name__ == "__main__":
    main()
