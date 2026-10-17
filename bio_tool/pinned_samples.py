"""Read-only Bio Tool field check of independently pinned GitHub blobs.

Only aggregate quality reports are retained; never uploads or republishes the
third-party FASTA/PDB raw content. Source commit and Git blob are verified.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import quote
from urllib.request import Request, urlopen

from .protein import analyze_fasta, analyze_pdb

HEX40 = re.compile(r"^[a-f0-9]{40}$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
MAX_RAW = 400_000


def _fetch(url: str) -> dict:
    import os
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "life-science-protein-bio-audit"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urlopen(Request(url, headers=headers), timeout=30) as response:
        value = json.load(response)
        if not isinstance(value, dict):
            raise ValueError("GitHub response must be an object")
        return value


def audit_samples(manifest: dict) -> dict:
    if manifest.get("kind") != "PINNED_PROTEIN_RESEARCH_DATA_SAMPLE_MANIFEST":
        raise ValueError("invalid manifest")
    samples = manifest.get("samples")
    if not isinstance(samples, list) or not 1 <= len(samples) <= 20:
        raise ValueError("bounded sample list required")
    results = []
    seen = set()
    for sample in sorted(samples, key=lambda item: item["id"]):
        if sample["format"] not in ("FASTA", "PDB"):
            continue
        repo, commit, blob, path = (sample[k] for k in ("repository", "commit", "blob_sha", "path"))
        if (not REPO.fullmatch(repo) or not HEX40.fullmatch(commit) or not HEX40.fullmatch(blob)
                or not isinstance(path, str) or not path or path.startswith("/")
                or "\\" in path or ".." in path.split("/")):
            raise ValueError("unsafe or unpinned sample")
        if sample["id"] in seen:
            raise ValueError("duplicate sample")
        seen.add(sample["id"])
        if not isinstance(sample.get("bytes"), int) or sample["bytes"] > MAX_RAW or sample["bytes"] <= 0:
            raise ValueError("sample size outside bounds")
        tree = _fetch(f"https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1")
        if tree.get("truncated") or not isinstance(tree.get("tree"), list):
            raise ValueError("incomplete pinned source tree")
        match = [item for item in tree["tree"] if item.get("path") == path and item.get("type") == "blob"]
        if len(match) != 1 or match[0].get("sha") != blob or match[0].get("size") != sample["bytes"]:
            raise ValueError("source tree/blob mismatch")
        obj = _fetch(f"https://api.github.com/repos/{repo}/git/blobs/{blob}")
        if obj.get("sha") != blob or obj.get("encoding") != "base64":
            raise ValueError("bad GitHub blob response")
        raw = base64.b64decode(obj["content"], validate=False)
        if len(raw) != sample["bytes"]:
            raise ValueError("GitHub raw size mismatch")
        if hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest() != blob:
            raise ValueError("Git blob identity mismatch")
        with TemporaryDirectory() as tmp:
            input_path = Path(tmp) / ("input.fa" if sample["format"] == "FASTA" else "input.pdb")
            input_path.write_bytes(raw)
            result = analyze_fasta(input_path) if sample["format"] == "FASTA" else analyze_pdb(input_path)
        results.append({
            "id": sample["id"], "repository": repo, "commit": commit, "path": path,
            "blob_sha": blob, "source_sha256": result["source_sha256"], "format": sample["format"],
            "status": result["status"], "records": result.get("record_count"),
            "residue_count": result.get("residue_count"),
            "observed_ca_count": result.get("observed_ca_count"),
            "warnings": result.get("warnings", []),
        })
    if not results:
        raise ValueError("no supported pinned samples")
    return {"schema_version": "1.0.0", "kind": "PINNED_BIO_TOOL_PROTEIN_FILE_AUDIT",
            "status": "VERIFIED_PINNED_BLOBS_AND_ANALYZED_BIO_DATA",
            "verified_count": len(results), "samples": results,
            "not_verified": ["biological ground truth", "fold accuracy", "scientific benchmark comparisons",
                             "rights to redistribute third-party sequences or coordinates"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.manifest.stat().st_size > 100_000:
            raise ValueError("manifest too large")
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = audit_samples(manifest)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        print(result["status"], result["verified_count"])
        return 0
    except (ValueError, OSError) as exc:
        print(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
