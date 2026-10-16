"""Reject all repository writes outside versioned lifecycle data roots."""
from __future__ import annotations

import argparse
import sys
from life_science_ecosystem_lab.lifecycle.guard import check_write_boundary


def rejected_paths(paths: list[str]) -> list[str]:
    return check_write_boundary(paths)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args(argv)
    paths = args.paths or [s for s in sys.stdin.read().splitlines() if s]
    rejected = rejected_paths(paths)
    if rejected:
        print("WRITE_BOUNDARY_REJECTED: " + ", ".join(rejected), file=sys.stderr)
        return 1
    print(f"WRITE_BOUNDARY_OK: {len(paths)} paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
