"""Deterministic GitHub evidence collection and aggregation."""

from .aggregation import aggregate_evidence
from .models import GitTreeEntry, SourceIdentity

__all__ = ["GitTreeEntry", "SourceIdentity", "aggregate_evidence"]
