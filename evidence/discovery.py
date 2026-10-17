"""Read-only GitHub topic discovery. Results are never promoted to approved sources."""
from __future__ import annotations

import json
import os
import re
from typing import Any, Callable
from urllib.parse import urlencode
from urllib.request import Request, urlopen


TOPIC = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def discover_repositories(topic: str, *, limit: int = 20,
                          retrieve: Callable[[str], dict[str, Any]] | None = None) -> dict[str, Any]:
    if TOPIC.fullmatch(topic) is None:
        raise ValueError("GitHub topic must be lowercase alphanumeric with hyphens")
    if not 1 <= limit <= 50:
        raise ValueError("discovery limit must be between 1 and 50")
    url = "https://api.github.com/search/repositories?" + urlencode({
        "q": f"topic:{topic} archived:false fork:false", "sort": "updated", "order": "desc", "per_page": limit
    })
    def request(url: str) -> dict[str, Any]:
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "ls-evidence/0.3"}
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        with urlopen(Request(url, headers=headers), timeout=20) as response:
            return json.load(response)
    data = (retrieve or request)(url)
    candidates = []
    for item in data.get("items", [])[:limit]:
        if not isinstance(item, dict):
            continue
        repository = item.get("full_name")
        if not isinstance(repository, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            continue
        candidates.append({"repository": repository, "url": f"https://github.com/{repository}",
                           "description": str(item.get("description") or "")[:300],
                           "default_branch": str(item.get("default_branch") or ""),
                           "approved": False, "status": "DISCOVERY_ONLY"})
    return {"schema_version": "1.0.0", "topic": topic, "source": "GitHub repository search",
            "promotable_without_review": False, "candidates": candidates}
