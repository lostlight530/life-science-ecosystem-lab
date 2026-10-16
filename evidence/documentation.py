"""Deterministic, repository-local scientific-software documentation maintenance checks.

External links are inventory entries, not mistaken for verified online endpoints
No remote resource is requested, modified or registered by this module
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

_INLINE_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
_REFERENCE_LINK = re.compile(r"(?m)^\s*\[[^\]]+\]:\s*(\S+)")
_FENCE = re.compile(r"(?ms)^```.*?^```\s*$")


@dataclass(frozen=True)
class DocumentationAudit:
    scanned: tuple[str, ...]
    external_links: tuple[str, ...]
    issues: tuple[str, ...]

    def as_dict(self) -> dict:
        return {"schema_version": "1.0.0", "status": "PASS" if not self.issues else "FAIL",
                "scanned": list(self.scanned), "external_links": list(self.external_links),
                "issues": list(self.issues)}


def audit_documents(root: Path, documents: list[str]) -> DocumentationAudit:
    root = root.resolve()
    issues: list[str] = []
    scanned: list[str] = []
    external: set[str] = set()
    for relative in sorted(set(documents)):
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or not path.is_file() or path.suffix.lower() != ".md":
            issues.append(f"DOCUMENT_MISSING_OR_UNSAFE: {relative}")
            continue
        scanned.append(relative)
        text = _FENCE.sub("", path.read_text(encoding="utf-8"))
        for token in [*_INLINE_LINK.findall(text), *_REFERENCE_LINK.findall(text)]:
            destination = token.strip().split(' "', 1)[0].strip("<>")
            if not destination or destination.startswith(("#", "mailto:", "data:")):
                continue
            parsed = urlsplit(destination)
            if parsed.scheme in ("http", "https") and parsed.netloc:
                external.add(f"{parsed.scheme}://{parsed.netloc}{parsed.path}")
                continue
            if parsed.scheme or destination.startswith("//"):
                issues.append(f"LINK_SCHEME_UNSUPPORTED: {relative} -> {destination}")
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root) or not target.exists():
                issues.append(f"BROKEN_LOCAL_LINK: {relative} -> {destination}")
    return DocumentationAudit(tuple(scanned), tuple(sorted(external)), tuple(sorted(issues)))


def write_report(report: DocumentationAudit, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report.as_dict(), indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
