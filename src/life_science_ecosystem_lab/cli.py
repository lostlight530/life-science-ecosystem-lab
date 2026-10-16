from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .integrity import build_record_manifest, write_manifest
from .workflow_profile import validate_workflow_profile_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ls-ecosystem-lab")
    commands = parser.add_subparsers(dest="command", required=True)

    integrity = commands.add_parser("record-integrity")
    integrity.add_argument("input", type=Path)
    integrity.add_argument("--output", type=Path, required=True)

    profile = commands.add_parser("validate-workflow-profile")
    profile.add_argument("profile", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "record-integrity":
            manifest = build_record_manifest(args.input)
            write_manifest(manifest, args.output)
            print(json.dumps(manifest, sort_keys=True))
            return 0
        errors = validate_workflow_profile_file(args.profile)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("workflow profile is valid")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

