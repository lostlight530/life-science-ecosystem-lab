"""Bounded GitHub REST transport using only the Python standard library."""

from __future__ import annotations

import base64
import json
import binascii
import time
from typing import Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from .models import SourceIdentity


class GitHubTransportError(RuntimeError):
    pass


class UrlLibGitHubTransport:
    def __init__(
        self,
        *,
        token: str | None = None,
        timeout: float = 20.0,
        attempts: int = 3,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        self._token = token
        self._timeout = timeout
        self._attempts = attempts
        self._sleeper = sleeper

    def _request(self, path: str) -> Mapping[str, object]:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "life-science-ecosystem-lab/0.2",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        last_error: Exception | None = None
        for attempt in range(self._attempts):
            try:
                request = Request(f"https://api.github.com{path}", headers=headers)
                with urlopen(request, timeout=self._timeout) as response:
                    value = json.load(response)
                if not isinstance(value, dict):
                    raise GitHubTransportError("GitHub response must be an object")
                return value
            except HTTPError as exc:
                last_error = exc
                if exc.code not in {429, 502, 503, 504} or attempt + 1 == self._attempts:
                    raise GitHubTransportError(f"GitHub HTTP {exc.code} for {path}") from exc
            except URLError as exc:
                last_error = exc
                if attempt + 1 == self._attempts:
                    raise GitHubTransportError(f"GitHub network error for {path}: {exc.reason}") from exc
            self._sleeper(float(2**attempt))
        raise GitHubTransportError(str(last_error))

    @staticmethod
    def _repo(identity: SourceIdentity) -> str:
        return f"/{quote(identity.owner, safe='')}/{quote(identity.repository, safe='')}"

    def get_repository(self, identity: SourceIdentity) -> Mapping[str, object]:
        return self._request(f"/repos{self._repo(identity)}")

    def get_commit(self, identity: SourceIdentity, ref: str) -> Mapping[str, object]:
        return self._request(f"/repos{self._repo(identity)}/commits/{quote(ref, safe='')}")

    def get_tree(self, identity: SourceIdentity, tree_sha: str) -> Mapping[str, object]:
        return self._request(f"/repos{self._repo(identity)}/git/trees/{quote(tree_sha, safe='')}?recursive=1")

    def get_blob(self, identity: SourceIdentity, blob_sha: str) -> bytes:
        value = self._request(f"/repos{self._repo(identity)}/git/blobs/{quote(blob_sha, safe='')}")
        if value.get("encoding") != "base64" or not isinstance(value.get("content"), str):
            raise GitHubTransportError("GitHub blob is not base64 encoded")
        try:
            return base64.b64decode(str(value["content"]), validate=False)
        except (ValueError, binascii.Error) as exc:
            raise GitHubTransportError("GitHub blob contains invalid base64") from exc
