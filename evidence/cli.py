"""Independent command-line entry point for the Life Science Evidence Tool."""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from .aggregation import aggregate_evidence
from .collector import collect_sources
from .discovery import discover_repositories
from .documentation import audit_documents, write_report
from .github import GitHubTransportError, UrlLibGitHubTransport
from .profiles import load_source_registry, load_topic_registry
from .validation import validate_candidate_bundle


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="ls-evidence")
    commands = root.add_subparsers(dest="command", required=True)
    collect = commands.add_parser("collect", help="Collect approved GitHub source documents")
    collect.add_argument("--sources", type=Path, required=True)
    collect.add_argument("--output", type=Path, required=True)
    agg = commands.add_parser("aggregate", help="Compute deterministic candidate evidence")
    agg.add_argument("--input", type=Path, required=True)
    agg.add_argument("--topics", type=Path, required=True)
    agg.add_argument("--previous", type=Path)
    agg.add_argument("--output", type=Path, required=True)
    check = commands.add_parser("validate", help="Verify provenance and candidate digests")
    check.add_argument("--bundle", type=Path, required=True)
    audit = commands.add_parser("audit-docs", help="Check internal links in research software docs")
    audit.add_argument("--root", type=Path, default=Path('.'))
    audit.add_argument("--files", type=Path, required=True, help="JSON file containing a documents array")
    audit.add_argument("--output", type=Path, required=True)
    find = commands.add_parser("discover", help="Find unapproved GitHub topic candidates")
    find.add_argument("--topic", required=True)
    find.add_argument("--limit", type=int, default=20)
    find.add_argument("--output", type=Path, required=True)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == 'collect':
            sources = load_source_registry(args.sources)
            now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
            result = collect_sources(sources, UrlLibGitHubTransport(token=os.environ.get('GITHUB_TOKEN')), retrieved_at=now)
            payload = list(result.records)
            if not payload:
                raise ValueError('no approved source documents were collected')
        elif args.command == 'aggregate':
            records = json.loads(args.input.read_text(encoding='utf-8'))
            if not isinstance(records, list):
                raise ValueError('input must be JSON array')
            topics = load_topic_registry(args.topics)
            old = json.loads(args.previous.read_text(encoding='utf-8')) if args.previous else None
            payload = aggregate_evidence(records, topics, old)
        elif args.command == 'validate':
            value = json.loads(args.bundle.read_text(encoding='utf-8'))
            result = validate_candidate_bundle(value)
            if not result.valid:
                raise ValueError('; '.join(result.errors))
            print('EVIDENCE_VERIFIED')
            return 0
        elif args.command == 'audit-docs':
            manifest = json.loads(args.files.read_text(encoding='utf-8'))
            if not isinstance(manifest, dict) or not isinstance(manifest.get('documents'), list) or not all(isinstance(x,str) for x in manifest['documents']):
                raise ValueError('documentation manifest must contain a string array: documents')
            report = audit_documents(args.root, manifest['documents'])
            write_report(report, args.output)
            print('DOCUMENTATION_' + ('PASS' if not report.issues else 'FAIL'))
            return 0 if not report.issues else 1
        elif args.command == 'discover':
            payload = discover_repositories(args.topic, limit=args.limit)
        else:
            raise ValueError('unsupported evidence action')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')
        print(args.output)
        return 0
    except (OSError, ValueError, GitHubTransportError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
