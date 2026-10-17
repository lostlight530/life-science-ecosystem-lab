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
from .inspection import inspect_repository, write_reports
from .agent_handoff import validate_agent_handoff
from .knowledge_quality import audit_knowledge
from .interoperability import audit_ecosystem
from .aggregation import canonical_bytes
from .normalization import sha256_bytes


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="ls-evidence")
    commands = root.add_subparsers(dest="command", required=True)
    collect = commands.add_parser("collect", help="Collect approved GitHub source documents")
    collect.add_argument("--sources", type=Path, required=True)
    collect.add_argument("--output", type=Path, required=True)
    collect.add_argument("--diagnostics-output", type=Path)
    agg = commands.add_parser("aggregate", help="Compute deterministic candidate evidence")
    agg.add_argument("--input", type=Path, required=True)
    agg.add_argument("--topics", type=Path, required=True)
    agg.add_argument("--previous", type=Path)
    agg.add_argument("--output", type=Path, required=True)
    agg.add_argument("--diagnostics", type=Path)
    check = commands.add_parser("validate", help="Verify provenance and candidate digests")
    check.add_argument("--bundle", type=Path, required=True)
    audit = commands.add_parser("audit-docs", help="Check internal links in research software docs")
    audit.add_argument("--root", type=Path, default=Path('.'))
    audit.add_argument("--files", type=Path, required=True, help="JSON file containing a documents array")
    audit.add_argument("--output", type=Path, required=True)
    inspect = commands.add_parser("inspect", help="Static, nonexecuting external research software preflight")
    inspect.add_argument("--root", type=Path, required=True)
    inspect.add_argument("--output", type=Path, required=True)
    inspect.add_argument("--markdown", type=Path)
    inspect.add_argument("--sarif", type=Path)
    handoff = commands.add_parser("validate-handoff", help="Validate an optional, proposal-only external Agent research handoff")
    handoff.add_argument("--input", type=Path, required=True)
    handoff.add_argument("--topics", type=Path, required=True, help="Current native topic registry; does not authorize new topics")
    eco = commands.add_parser("audit-ecosystem", help="Local WorkflowHub/LifeMonitor/bio.tools interoperability preflight, not registration")
    eco.add_argument("--root", type=Path, default=Path("."))
    eco.add_argument("--output", type=Path, required=True)
    quality = commands.add_parser("audit-knowledge", help="Review knowledge structure, cross-version drift and optional relevance labels")
    quality.add_argument("--knowledge", type=Path, required=True)
    quality.add_argument("--previous", type=Path, help="Previously accepted knowledge map, never a hidden live fetch")
    quality.add_argument("--labels", type=Path, help="Optional user-supplied labeled topic/document examples")
    quality.add_argument("--output", type=Path, required=True)
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
            if args.diagnostics_output:
                args.diagnostics_output.parent.mkdir(parents=True, exist_ok=True)
                args.diagnostics_output.write_text(json.dumps(list(result.diagnostics), indent=2, sort_keys=True) + "\n", encoding="utf-8")
            if not payload:
                raise ValueError('no approved source documents were collected')
        elif args.command == 'aggregate':
            records = json.loads(args.input.read_text(encoding='utf-8'))
            if not isinstance(records, list):
                raise ValueError('input must be JSON array')
            topics = load_topic_registry(args.topics)
            old = json.loads(args.previous.read_text(encoding='utf-8')) if args.previous else None
            payload = aggregate_evidence(records, topics, old)
            if args.diagnostics:
                diagnostics = json.loads(args.diagnostics.read_text(encoding="utf-8"))
                if not isinstance(diagnostics, list) or not all(isinstance(i, dict) for i in diagnostics):
                    raise ValueError("diagnostics must be an array of objects")
                payload["diagnostics"] = diagnostics
                # Partial observations may be inspected, but must not overwrite
                # the durable knowledge corpus while a source was unavailable
                payload["projection_eligible"] = not bool(diagnostics)
                body = dict(payload)
                body.pop("output_digest", None)
                payload["output_digest"] = sha256_bytes(canonical_bytes(body))
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
        elif args.command == 'inspect':
            report = inspect_repository(args.root)
            write_reports(report, args.output, markdown=args.markdown, sarif=args.sarif)
            print('INSPECTION_' + report['status'])
            return 1 if report["status"] == "FAIL" else 0
        elif args.command == 'audit-ecosystem':
            payload = audit_ecosystem(args.root)
        elif args.command == 'audit-knowledge':
            def bounded_json(path: Path) -> object:
                if path.stat().st_size > 12_000_000:
                    raise ValueError('input exceeds 12MB bounded audit limit')
                return json.loads(path.read_text(encoding='utf-8'))
            current = bounded_json(args.knowledge)
            previous = bounded_json(args.previous) if args.previous else None
            labels = bounded_json(args.labels) if args.labels else None
            payload = audit_knowledge(current, previous=previous, labels=labels)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')
            print('KNOWLEDGE_QUALITY_' + payload['status'])
            return 1 if payload["status"] == "FAIL" else 0
        elif args.command == 'validate-handoff':
            value = json.loads(args.input.read_text(encoding='utf-8'))
            topics = load_topic_registry(args.topics)
            verdict = validate_agent_handoff(value, known_topics={item["id"] for item in topics.topics})
            if not verdict.valid:
                raise ValueError("; ".join(verdict.errors))
            print("AGENT_HANDOFF_SHAPE_VALID_PROPOSAL_ONLY")
            return 0
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
