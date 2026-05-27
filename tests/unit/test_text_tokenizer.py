from core import text_tokenizer
from core.text_tokenizer import tokenize, tokenize_fallback


def test_tokenize_fallback_lowercases_words():
    tokens = tokenize_fallback("Python 3.11 and FastAPI!")
    assert "python" in tokens
    assert "fastapi" in tokens


def test_tokenize_returns_non_empty_for_skill_text():
    tokens = tokenize("Senior Python engineer with machine learning experience")
    assert len(tokens) > 0
    assert all(isinstance(t, str) for t in tokens)


def test_tokenize_empty_string():
    assert tokenize("") == []


def test_tokenize_uses_fallback_when_tiktoken_disabled(monkeypatch):
    monkeypatch.setattr(text_tokenizer, "_tiktoken_unavailable", True)
    monkeypatch.setattr(text_tokenizer, "_encoder", None)
    tokens = tokenize("React TypeScript developer")
    assert tokens == tokenize_fallback("React TypeScript developer")
