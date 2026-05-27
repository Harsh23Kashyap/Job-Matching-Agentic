# Hooks

Pluggable parsers and explainers · LLM layer is optional; rule/template fallbacks always work.

## Files

| File | Purpose |
|------|---------|
| `llm_parser.py` | `LlmParser` · resume/JD field extraction via Ollama or OpenAI |
| `parser_factory.py` | `create_llm_parser(settings)` · picks provider from env |
| `parser.py` | `JsonParser` · Pydantic-only validation (no LLM) |
| `explainer.py` | `RuleExplainer` · template `why_ranked` bullets |
| `grounded_explainer.py` | Optional LLM explanations when `explain_mode=llm` |

## LLM fallback chain

1. `OPENAI_API_KEY` set → OpenAI (`gpt-4o-mini`)
2. Else → Ollama (`OLLAMA_BASE_URL`, default `llama3.2`)
3. Unavailable → manual form + regex contact extraction from cleaned text

Used by: resume upload, JD parse/upload, resume coach suggestions.
