"""Lexical tokenization: tiktoken when available, regex word tokens otherwise."""
from __future__ import annotations

import re

_FALLBACK_RE = re.compile(r"[a-z0-9]+")
_DEFAULT_ENCODING = "cl100k_base"

_encoder = None
_tiktoken_unavailable = False


def _tiktoken_encoder():
    global _encoder, _tiktoken_unavailable
    if _tiktoken_unavailable:
        return None
    if _encoder is not None:
        return _encoder
    try:
        import tiktoken

        _encoder = tiktoken.get_encoding(_DEFAULT_ENCODING)
        return _encoder
    except Exception:
        _tiktoken_unavailable = True
        return None


def tokenize_fallback(text: str) -> list[str]:
    return _FALLBACK_RE.findall(text.lower())


def tokenize(text: str) -> list[str]:
    enc = _tiktoken_encoder()
    if enc is None:
        return tokenize_fallback(text)

    try:
        ids = enc.encode(text, disallowed_special=())
        if not ids:
            return []
        tokens: list[str] = []
        for piece in enc.decode_tokens_bytes(ids):
            s = piece.decode("utf-8", errors="replace").strip().lower()
            if not s:
                continue
            sub = _FALLBACK_RE.findall(s)
            tokens.extend(sub if sub else [s])
        return tokens if tokens else tokenize_fallback(text)
    except Exception:
        return tokenize_fallback(text)
