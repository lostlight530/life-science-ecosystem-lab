"""Compare the exact validated SHA to the current, independently fetched remote main ref."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys


def verify_world_line(validated_head: str, current_head: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{40}", validated_head) and validated_head == current_head)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validated-head", required=True)
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--ref", default="refs/heads/main")
    args = parser.parse_args(argv)
    result = subprocess.run(["git", "ls-remote", "--exit-code", args.remote, args.ref], capture_output=True, text=True, check=True, timeout=30)
    lines = result.stdout.splitlines()
    current = lines[0].split()[0] if len(lines) == 1 else ""
    if not verify_world_line(args.validated_head, current):
        print(f"CONFLICTED_WORLD_LINE_NO_APPLY validated={args.validated_head} current={current}", file=sys.stderr)
        return 1
    print(f"WORLD_LINE_OK {current}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
