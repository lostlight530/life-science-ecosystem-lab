"""Untrusted optional Agent-origin label shared by research proposal envelopes.

Proposer fields identify who *claims* to have performed the work, not who
authenticated to GitHub, which runtime executed it or who reviewed it.
"""
from __future__ import annotations

from typing import Any


def proposer_errors(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["proposer must be an object of self-declared identity fields"]
    fields = {"agent_label", "execution_surface", "assertion"}
    if set(value) != fields:
        return ["proposer must contain only agent_label, execution_surface and assertion"]
    if value["assertion"] != "SELF_DECLARED":
        return ["proposer assertion must be SELF_DECLARED; proposals cannot self-attest identity"]
    for key, limit in (("agent_label", 96), ("execution_surface", 180)):
        item = value[key]
        if (not isinstance(item, str) or not item.strip()
                or len(item) > limit or "\x00" in item):
            return [f"proposer.{key} must be a bounded nonempty text field"]
    return []
