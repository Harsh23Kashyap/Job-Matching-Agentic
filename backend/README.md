# Backend

Python FastAPI service for the multi-agent job matching system.

## Run

```bash
cd backend
source .venv/bin/activate
uvicorn main:create_app --factory --reload --port 8001
```

API docs: http://localhost:8001/docs

## Entry points

| File | Role |
|------|------|
| `main.py` | Uvicorn factory · `create_app()` |
| `bootstrap.py` | Wires agents, stores, event bus; loads corpus |
| `config.py` | Settings from env (`.env.example`) |
| `demo_seed.py` | Demo accounts on startup when `SEED_DEMO=true` |

## Modules

| Folder | Purpose |
|--------|---------|
| [agents/](agents/README.md) | Candidate, Employer, Matchmaking agents |
| [auth/](auth/README.md) | Session auth and ownership links |
| [benchmarks/](benchmarks/README.md) | Evaluation drivers and regression |
| [bus/](bus/README.md) | In-process event bus |
| [contracts/](contracts/README.md) | Shared Pydantic models |
| [core/](core/README.md) | Scoring, embeddings, resume/JD processing |
| [gateway/](gateway/README.md) | FastAPI app and HTTP routes |
| [hooks/](hooks/README.md) | LLM parser, rule explainer |
| [stores/](stores/README.md) | Chroma/Qdrant and SQLite persistence |

## Dependencies

Install: `pip install -r requirements-min.txt`

Optional: Ollama for local LLM parsing, or set `OPENAI_API_KEY` in `.env`.
