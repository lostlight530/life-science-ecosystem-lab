"""Shared refusal guard for LS Framework report destinations.

This guard protects known evidence and repository-state paths. It is not a
filesystem sandbox and cannot eliminate races with concurrent filesystem writes.
"""
from __future__ import annotations

from pathlib import Path


def _resolve(path: Path) -> Path:
    try:
        return Path(path).resolve()
    except (OSError, RuntimeError) as error:
        raise ValueError("report path cannot be safely resolved") from error


def _repository_roots(*anchors: Path) -> set[Path]:
    """Find Git checkout roots by walking ancestors of every relevant path."""
    roots: set[Path] = set()
    for anchor in anchors:
        current = _resolve(anchor)
        while True:
            try:
                has_git_marker = (current / ".git").exists()
            except OSError:
                has_git_marker = False
            if has_git_marker:
                roots.add(current)
            parent = current.parent
            if parent == current:
                break
            current = parent
    return roots


def resolve_report_target(
    output: Path | None,
    bundle: Path,
    input_root: Path,
    *,
    cwd: Path | None = None,
) -> Path | None:
    """Resolve output and refuse overwriting the bundle, input tree, or repo state.

    Git roots are discovered from the working directory, input root, bundle path,
    and resolved destination. This remains effective when the command runs from a
    repository subdirectory or when its inputs live outside the checkout.
    """
    if output is None:
        return None

    target = _resolve(output)
    source = _resolve(bundle)
    root = _resolve(input_root)
    if target == source:
        raise ValueError("report output cannot replace the input bundle")

    working_root = _resolve(cwd or Path.cwd())
    protected_roots = [root]
    for checkout in _repository_roots(working_root, root, source, target):
        protected_roots.extend((checkout / "data", checkout / ".git"))

    for protected in protected_roots:
        protected_path = _resolve(protected)
        if target == protected_path or target.is_relative_to(protected_path):
            raise ValueError(
                "report output cannot replace evidence or accepted repository state"
            )

    return target
