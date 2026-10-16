"""Cross-platform text and digest normalization."""

from __future__ import annotations

import hashlib
import unicodedata


def normalize_text_bytes(value: bytes) -> str:
    text = value.decode("utf-8-sig", errors="strict")
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    return text.rstrip("\n") + "\n"


def canonical_text_bytes(value: str) -> bytes:
    return (unicodedata.normalize("NFC", value).rstrip("\n") + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()
