"""Deterministic, bounded protein FASTA and PDB coordinate data audits.

These are file/sequence quality measurements, not protein structure prediction,
alignment, clinical interpretation, or biological validation.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import math
from pathlib import Path
from typing import Any

AA20 = "ACDEFGHIKLMNPQRSTVWY"
UNCERTAIN = "BXZJUO"
THREE = dict(zip(
    "ALA CYS ASP GLU PHE GLY HIS ILE LYS LEU MET ASN PRO GLN ARG SER THR VAL TRP TYR".split(),
    AA20,
))
MAX_BYTES = 8_000_000
MAX_SEQUENCES = 2000
MAX_TOTAL_RESIDUES = 1_000_000
MAX_PDB_CHAINS = 64


def _read(path: Path) -> tuple[str, str]:
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("protein input exceeds 8 MB")
    data = path.read_bytes()
    if not data or len(data) > MAX_BYTES or b"\x00" in data:
        raise ValueError("empty, oversized or binary protein input")
    try:
        value = data.decode("utf-8-sig", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("protein input is not UTF-8") from exc
    return value, hashlib.sha256(data).hexdigest()


def analyze_fasta(path: Path) -> dict[str, Any]:
    value, digest = _read(path)
    sequence_id: str | None = None
    residues: list[str] = []
    rows: list[dict[str, Any]] = []
    names: set[str] = set()
    total = 0

    def flush() -> None:
        nonlocal residues, total
        if sequence_id is None:
            return
        seq = "".join(residues)
        if not seq:
            raise ValueError("empty FASTA sequence: " + sequence_id)
        total += len(seq)
        if total > MAX_TOTAL_RESIDUES:
            raise ValueError("total FASTA residues limit exceeded")
        counts = Counter(seq)
        canonical_count = sum(counts.get(a, 0) for a in AA20)
        rows.append({
            "id": sequence_id, "length": len(seq),
            "sequence_sha256": hashlib.sha256(seq.encode("ascii")).hexdigest(),
            "canonical_residues": canonical_count,
            "uncertain_residues": len(seq) - canonical_count,
            "counts": {aa: counts[aa] for aa in sorted(counts)},
            "uncertain_positions": [i for i, aa in enumerate(seq, start=1) if aa in UNCERTAIN][:100],
            "uncertain_positions_truncated": sum(counts.get(x, 0) for x in UNCERTAIN) > 100,
        })
        residues = []

    for line in value.splitlines():
        row = line.strip()
        if not row:
            continue
        if row.startswith(">"):
            flush()
            sequence_id = row[1:].split()[0] if row[1:].strip() else ""
            if not sequence_id or len(sequence_id) > 200 or sequence_id in names:
                raise ValueError("FASTA header is blank, duplicate or too long")
            names.add(sequence_id)
            if len(names) > MAX_SEQUENCES:
                raise ValueError("too many FASTA records")
        else:
            if sequence_id is None:
                raise ValueError("FASTA requires initial header")
            if not row.isascii() or not row.isalpha():
                raise ValueError("FASTA residue line contains nonletters or stop symbols")
            normalized = row.upper()
            if any(residue not in AA20 + UNCERTAIN for residue in normalized):
                raise ValueError("FASTA contains invalid protein residue")
            residues.append(normalized)
    flush()
    if not rows:
        raise ValueError("no FASTA sequences")
    return {
        "schema_version": "1.0.0",
        "kind": "PROTEIN_FASTA_COMPOSITION_AUDIT",
        "source_sha256": digest,
        "record_count": len(rows),
        "residue_count": total,
        "records": rows,
        "status": "WARN_UNCERTAIN_RESIDUES" if any(x["uncertain_residues"] for x in rows) else "PASS",
        "scope": "Protein FASTA parsing and residue composition only",
        "not_verified": ["sequence biological identity", "sequence accuracy against external databases",
                         "protein function", "protein structure"],
    }


def analyze_pdb(path: Path) -> dict[str, Any]:
    value, digest = _read(path)
    residues: dict[str, dict[tuple[str, str], str]] = {}
    problems: list[str] = []
    seen_models = False
    in_first_model = True
    atoms = 0
    for line in value.splitlines():
        record = line[:6].strip()
        if record == "MODEL":
            if seen_models:
                break
            seen_models = True
            in_first_model = True
            continue
        if record == "ENDMDL" and seen_models:
            break
        if not in_first_model or record != "ATOM":
            continue
        if len(line) < 54:
            raise ValueError("malformed PDB ATOM record")
        for start, end in ((30, 38), (38, 46), (46, 54)):
            try:
                coordinate = float(line[start:end])
            except ValueError as exc:
                raise ValueError("malformed PDB Cartesian coordinate") from exc
            if not math.isfinite(coordinate):
                raise ValueError("nonfinite PDB Cartesian coordinate")
        if line[12:16].strip() != "CA":
            continue
        if line[16:17] not in (" ", "A"):
            continue
        chain = line[21:22].strip() or "_"
        residue = line[17:20].strip()
        serial = line[22:26].strip()
        insertion = line[26:27].strip()
        if not serial or not (serial.lstrip("-").isdigit()):
            raise ValueError("malformed PDB residue number")
        if len(residues) >= MAX_PDB_CHAINS and chain not in residues:
            raise ValueError("PDB chain count limit exceeded")
        atoms += 1
        if atoms > MAX_TOTAL_RESIDUES:
            raise ValueError("PDB CA record count exceeded")
        chain_residues = residues.setdefault(chain, {})
        key = (serial, insertion)
        aa = THREE.get(residue, "X")
        if residue not in THREE and "NONSTANDARD_RESIDUE" not in problems:
            problems.append("NONSTANDARD_RESIDUE")
        if key in chain_residues:
            if chain_residues[key] != aa:
                raise ValueError("contradictory CA residue records")
            if "DUPLICATE_CA" not in problems:
                problems.append("DUPLICATE_CA")
        else:
            chain_residues[key] = aa
    if not residues or not any(residues.values()):
        raise ValueError("PDB contains no parsable first-model protein CA records")
    rows = []
    for chain in sorted(residues):
        aa = "".join(residues[chain].values())
        rows.append({
            "chain": chain,
            "observed_ca_residues": len(aa),
            "observed_sequence_sha256": hashlib.sha256(aa.encode("ascii")).hexdigest(),
            "nonstandard_residues": aa.count("X"),
            "residue_codes": {x: c for x, c in sorted(Counter(aa).items())},
        })
    return {
        "schema_version": "1.0.0",
        "kind": "PROTEIN_PDB_CA_AUDIT",
        "source_sha256": digest,
        "model_scope": "first model only",
        "chain_count": len(rows),
        "observed_ca_count": sum(x["observed_ca_residues"] for x in rows),
        "chains": rows,
        "status": "WARN" if problems else "PASS",
        "warnings": problems,
        "not_verified": ["full protein sequence", "missing residues or coordinate completeness",
                         "chemical correctness", "steric validity", "structural quality or fold accuracy"],
    }
