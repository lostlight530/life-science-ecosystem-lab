"""Standalone bioinformatics file-analysis CLI for independently supplied data."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from .protein import analyze_fasta, analyze_pdb


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="ls-bio", description="Bounded protein FASTA and PDB C-alpha data-quality analysis")
    sub = root.add_subparsers(dest="command", required=True)
    for command in ("protein-fasta", "protein-pdb"):
        action = sub.add_parser(command)
        action.add_argument("--input", type=Path, required=True)
        action.add_argument("--output", type=Path, required=True)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.input.resolve() == args.output.resolve():
            raise ValueError("output path must differ from input path")
        result = analyze_fasta(args.input) if args.command == "protein-fasta" else analyze_pdb(args.input)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
        print(f"{result['kind']} {result['status']}")
        return 0
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
