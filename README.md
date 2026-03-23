# Elric Framework

Opinionated Python framework for AI-first applications with FastAPI, LangGraph, and LangChain.

## Stack Tecnologico

- **FastAPI** - Web framework
- **LangGraph** - Agentic workflows
- **LangChain** - AI chains e tools
- **LangSmith** - Tracing e monitoring
- **SQLModel** - ORM (Pydantic + SQLAlchemy)
- **Alembic** - Database migrations
- **PostgreSQL** - Database relazionale
- **Redis** - Cache e rate limiting
- **Structlog** - Logging strutturato JSON
- **uv** - Package manager

## Prerequisiti

- Python 3.12+
- PostgreSQL 16+
- Redis 7+
- [uv](https://github.com/astral-sh/uv) package manager

## Setup Iniziale

### 1. Clona il repository

```bash
git clone <repository-url>
cd elric_framework
```

### 2. Installa le dipendenze

```bash
uv sync
```

### 3. Configura le variabili d'ambiente

Copia il file `.env.example` in `.env` e modifica i valori:

```bash
cp .env.example .env
```

Modifica `.env` con le tue configurazioni:

```env
# Database
DATABASE_URL=postgresql+asyncpg://elric:secret@localhost:5432/elric_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# LangSmith (opzionale)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=elric-app
```

### 4. Avvia i servizi Docker (Database e Redis)

```bash
docker compose -f docker/docker-compose.yml up -d db redis
```

Questo avvierà PostgreSQL e Redis in background.

### 5. Esegui le migrations del database

```bash
uv run alembic upgrade head
```

## Avvio dell'Applicazione

### Sviluppo locale (Raccomandato)

```bash
# Avvia database e redis in Docker
docker compose -f docker/docker-compose.yml up -d db redis

# Esegui l'app localmente con hot-reload
uv run uvicorn app:create_app --factory --reload --host 0.0.0.0 --port 8000
```

L'applicazione sarà disponibile su:

- API: http://localhost:8000
- Docs (Swagger): http://localhost:8000/docs
- Health check: http://localhost:8000/health

**Nota**: Le richieste da `localhost` non richiedono API key per facilitare lo sviluppo.

### Con Docker Compose (tutto containerizzato)

Se preferisci eseguire anche l'app in Docker:

```bash
# Avvia tutti i servizi
docker compose -f docker/docker-compose.yml up -d

# Visualizza i logs
docker compose -f docker/docker-compose.yml logs -f elric

# Ferma i servizi
docker compose -f docker/docker-compose.yml down
```

**Nota**: Se esegui l'app in Docker, modifica `.env` per usare i nomi dei servizi invece di `localhost`:

```env
DATABASE_URL=postgresql+asyncpg://elric:secret@db:5432/elric_dev
REDIS_URL=redis://redis:6379/0
```

### Produzione

```bash
uv run gunicorn app:create_app --factory -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Gestione API Keys

### Creare una nuova API Key

Crea uno script Python per generare una API key:

```python
# create_api_key.py
import asyncio
from app.providers.database import AsyncSessionLocal
from app.utils.api_key import create_api_key_record

async def main():
    async with AsyncSessionLocal() as session:
        api_key_record, key = await create_api_key_record("My App Name", session)
        print(f"✅ API Key created successfully!")
        print(f"ID: {api_key_record.id}")
        print(f"Name: {api_key_record.name}")
        print(f"Key: {key}")
        print(f"\n🔑 Save this key securely - it won't be shown again!")
        print(f"\nExample usage:")
        print(f'curl -H "X-API-Key: {key}" http://localhost:8000/docs')

if __name__ == "__main__":
    asyncio.run(main())
```

Esegui lo script:

```bash
uv run python create_api_key.py
```

**⚠️ IMPORTANTE**: Salva la chiave generata in un posto sicuro. Non verrà mostrata di nuovo.

### Usare l'API Key

L'API key è richiesta solo per richieste esterne. Le richieste da `localhost` non richiedono autenticazione per facilitare lo sviluppo.

Per testare con API key:

```bash
curl -H "X-API-Key: elk_live_xxxxx" http://your-domain.com/api/endpoint
```

**Nota**: Durante lo sviluppo locale, puoi accedere a tutti gli endpoint senza API key:

```bash
curl http://localhost:8000/docs
```

## Database Migrations

### Creare una nuova migration

```bash
uv run alembic revision --autogenerate -m "descrizione_migration"
```

### Applicare le migrations

```bash
uv run alembic upgrade head
```

### Rollback ultima migration

```bash
uv run alembic downgrade -1
```

### Verificare stato migrations

```bash
uv run alembic current
```

## Struttura del Progetto

```
elric_framework/
├── app/
│   ├── agents/          # LangGraph agents
│   ├── chains/          # LangChain chains
│   ├── tools/           # LangChain tools
│   ├── routes/          # FastAPI routes
│   ├── controllers/     # Business logic
│   ├── middleware/      # Custom middleware
│   ├── providers/       # Database, Redis, LangSmith
│   ├── schemas/         # Pydantic schemas
│   ├── exceptions/      # Custom exceptions
│   ├── jobs/            # Background jobs
│   ├── events/          # Event handlers
│   └── utils/           # Utility functions
├── config/              # Configuration
├── database/
│   ├── models/          # SQLModel entities
│   ├── migrations/      # Alembic migrations
│   └── seeders/         # Database seeders
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docker/              # Docker configs
└── stubs/               # Code generation templates
```

## Features Implementate

### ✅ Fase 1 - Scaffolding

- Struttura progetto completa
- Docker Compose per sviluppo
- Configurazione uv e pyproject.toml

### ✅ Fase 2 - App Base

- FastAPI app con lifespan
- Providers: Database (PostgreSQL), Redis, LangSmith
- Health check endpoint
- Configurazione centralizzata con Pydantic Settings

### ✅ Fase 3 - Auth + Middleware

- Autenticazione API Key con cache Redis
- Rate limiting (sliding window)
- Logging strutturato con trace_id
- Alembic configurato per migrations async

## Logging

I log sono strutturati in formato JSON (configurabile via `LOG_JSON=true/false`):

```json
{
  "timestamp": "2026-03-20T10:14:39Z",
  "level": "info",
  "event": "request.completed",
  "trace_id": "uuid-v4",
  "method": "GET",
  "path": "/health",
  "status_code": 200,
  "duration_ms": 42
}
```

Ogni richiesta ha un `trace_id` univoco propagato attraverso tutto lo stack.

## Rate Limiting

Il rate limiting usa Redis con sliding window counter:

- Default: 100 richieste per 60 secondi
- Configurabile via `RATE_LIMIT_REQUESTS` e `RATE_LIMIT_WINDOW`
- Risposta 429 quando il limite viene superato

## Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_api_key.py -v
```

## Linting e Formatting

```bash
# Check code style
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

## Troubleshooting

### Porta già in uso

```bash
# Trova il processo sulla porta 8000
lsof -i :8000

# Termina il processo
kill -9 <PID>
```

### Database connection error

Verifica che PostgreSQL sia in esecuzione:

```bash
docker compose -f docker/docker-compose.yml ps
```

### Redis connection error

Verifica che Redis sia in esecuzione:

```bash
docker compose -f docker/docker-compose.yml ps
redis-cli ping  # Dovrebbe rispondere PONG
```

## Prossime Fasi

- **Fase 4**: Error handling centralizzato
- **Fase 5**: CLI con Typer (comandi `make:*`, `migrate:*`, etc.)
- **Fase 6**: Base classes per Agents, Chains, Tools

## License

MIT
