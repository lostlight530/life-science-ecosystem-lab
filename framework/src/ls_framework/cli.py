"""Independent deterministic CLI for the LS research software framework."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from .engine import assess


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cross-domain life-sciences software contract audit")
    parser.add_argument("command", choices=["assess"])
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-pass", action="store_true", help="Return 2 instead of 0 for INDETERMINATE")
    args = parser.parse_args(argv)
    output_target = None
    try:
        input_root = (args.root or args.bundle.parent).resolve(strict=True)
        if args.output is not None:
            candidate = args.output.resolve()
            checkout_root = Path.cwd().resolve()
            if (candidate == args.bundle.resolve() or candidate.is_relative_to(input_root)
                    or candidate.is_relative_to(checkout_root / "data")
                    or candidate.is_relative_to(checkout_root / ".git")):
                raise ValueError("report output cannot replace evidence or accepted repository state")
            output_target = candidate
        data = args.bundle.read_bytes()
        if len(data) > 256_000:
            raise ValueError("bundle exceeds 256 KB")
        def reject_duplicates(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError("duplicate JSON object key")
                result[key] = value
            return result
        bundle = json.loads(data, object_pairs_hook=reject_duplicates)
        report = assess(bundle, (args.root or args.bundle.parent).resolve(strict=True))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        report = {
            "kind": "LS_RSE_ENGINEERING_ASSESSMENT",
            "schema_version": "0.1.0",
            "status": "FAIL",
            "errors": [{"code": "INPUT_ERROR", "subject": type(error).__name__}],
            "warnings": [],
            "not_verified": ["No engineering evidence established"],
        }
    serialized = json.dumps(report, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    if output_target is not None:
        output_target.parent.mkdir(parents=True, exist_ok=True)
        output_target.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    if report["status"] == "FAIL":
        return 1
    if args.require_pass and report["status"] != "PASS":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
