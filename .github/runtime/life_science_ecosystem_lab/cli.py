from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .integrity import build_record_manifest, write_manifest
from .knowledge import build_knowledge, verify_knowledge
from evidence.profiles import load_source_registry, load_topic_registry
from .lifecycle.orchestrator import apply_lifecycle
from .lifecycle.state import StateRoots, verify_state
from .workflow_profile import validate_workflow_profile_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ls-knowledge")
    commands = parser.add_subparsers(dest="command", required=True)

    integrity = commands.add_parser("record-integrity")
    integrity.add_argument("input", type=Path)
    integrity.add_argument("--output", type=Path, required=True)

    profile = commands.add_parser("validate-workflow-profile")
    profile.add_argument("profile", type=Path)

    sources = commands.add_parser("validate-source-registry")
    sources.add_argument("registry", type=Path)

    topics = commands.add_parser("validate-topic-registry")
    topics.add_argument("registry", type=Path)

    knowledge = commands.add_parser("knowledge")
    knowledge_commands = knowledge.add_subparsers(dest="knowledge_command", required=True)
    knowledge_build = knowledge_commands.add_parser("build")
    knowledge_build.add_argument("--candidate", type=Path, required=True)
    knowledge_build.add_argument("--topics", type=Path, required=True)
    knowledge_build.add_argument("--output", type=Path, required=True)
    knowledge_verify = knowledge_commands.add_parser("verify")
    knowledge_verify.add_argument("--candidate", type=Path, required=True)
    knowledge_verify.add_argument("--topics", type=Path, required=True)
    knowledge_verify.add_argument("--knowledge", type=Path, required=True)

    lifecycle = commands.add_parser("lifecycle")
    lifecycle_commands = lifecycle.add_subparsers(dest="lifecycle_command", required=True)
    apply = lifecycle_commands.add_parser("apply")
    apply.add_argument("--candidate", type=Path, required=True)
    apply.add_argument("--repository-root", type=Path, required=True)
    apply.add_argument("--logical-date", required=True)
    apply.add_argument("--validated-head", required=True)
    apply.add_argument("--current-head", required=True)
    apply.add_argument("--knowledge", type=Path)
    apply.add_argument("--topics", type=Path)

    state = commands.add_parser("state")
    state_commands = state.add_subparsers(dest="state_command", required=True)
    verify = state_commands.add_parser("verify")
    verify.add_argument("--repository-root", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "record-integrity":
            manifest = build_record_manifest(args.input)
            write_manifest(manifest, args.output)
            print(json.dumps(manifest, sort_keys=True))
            return 0
        if args.command == "validate-source-registry":
            load_source_registry(args.registry)
            print("source registry is valid")
            return 0
        if args.command == "validate-topic-registry":
            load_topic_registry(args.registry)
            print("topic registry is valid")
            return 0
        if args.command == "knowledge":
            candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
            topic_registry = json.loads(args.topics.read_text(encoding="utf-8"))
            if args.knowledge_command == "build":
                value = build_knowledge(candidate, topic_registry)
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
                print(str(args.output))
            else:
                knowledge_value = json.loads(args.knowledge.read_text(encoding="utf-8"))
                verify_knowledge(candidate, topic_registry, knowledge_value)
                print("knowledge provenance and content verified")
            return 0
        if args.command == "lifecycle" and args.lifecycle_command == "apply":
            candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
            if not isinstance(candidate, dict):
                raise ValueError("candidate bundle must be a JSON object")
            receipt = apply_lifecycle(
                candidate,
                StateRoots(args.repository_root.resolve()),
                logical_date=args.logical_date,
                validated_head=args.validated_head,
                current_head=args.current_head,
                knowledge=json.loads(args.knowledge.read_text(encoding="utf-8")) if args.knowledge else None,
                topic_registry=json.loads(args.topics.read_text(encoding="utf-8")) if args.topics else None,
            )
            print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
            return 0 if receipt["outcome"] in {"APPLIED", "NO_MEANINGFUL_DELTA"} else 1
        if args.command == "state" and args.state_command == "verify":
            report = verify_state(StateRoots(args.repository_root.resolve()))
            if not report.valid:
                for error in report.errors:
                    print(error, file=sys.stderr)
                return 1
            print("state is valid")
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
