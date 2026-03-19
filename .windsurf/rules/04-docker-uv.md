---
trigger: glob
globs: ["docker/**", "Dockerfile*", "docker-compose*.yml", "pyproject.toml", ".env*"]
---

# Docker, uv & Environments

## uv — Package Manager

- Always use `uv` to manage dependencies. Never run `pip install` directly.
- To add a dependency: `uv add <package>`
- To add a dev dependency: `uv add --dev <package>`
- To run commands in the virtualenv: `uv run <command>`
- The `uv.lock` file must always be committed — it guarantees reproducible builds.
- Never edit `pyproject.toml` manually for dependencies — use `uv add` / `uv remove`.

```bash
# CORRECT
uv add httpx
uv run pytest tests/

# WRONG
pip install httpx
python -m pytest tests/
```

## Environment Variables

- `.env` is gitignored — never commit it.
- `.env.example` is the canonical reference — update it every time you add a new variable.
- All variables go through `config/settings.py` (Pydantic Settings). Never use `os.environ` in application code.
- Different values per environment: `.env` for local dev → Docker env vars for production.
- In production, variables are injected via `docker-compose.prod.yml` or the cloud provider's secrets manager.

```python
# CORRECT — always via Settings
from config.settings import get_settings
settings = get_settings()
db_url = settings.DATABASE_URL

# WRONG
import os
db_url = os.environ["DATABASE_URL"]
```

## Dockerfile — Development

- The dev image mounts the code as a volume for hot-reload.
- Uvicorn runs with `--reload` in development.
- Do not install production-only dependencies in the dev image.

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . .
CMD ["uv", "run", "uvicorn", "app:create_app", "--factory", "--reload", "--host", "0.0.0.0"]
```

## Dockerfile — Production (multi-stage)

- Always use a multi-stage build: `builder` stage + `production` stage.
- The `builder` stage installs dependencies with `uv sync --frozen --no-dev`.
- The `production` stage copies only `.venv` from the builder — minimal final image.
- The app must never run as `root` in production. Always use a non-privileged user.
- Use Gunicorn with `UvicornWorker` in production.
- Note: `uvicorn.workers` module is deprecated in uvicorn >=0.42. Use the separate `uvicorn-worker` package instead.

```dockerfile
# Builder stage
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.12-slim AS production
WORKDIR /app
COPY --from=builder /app/.venv ./.venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
RUN adduser --disabled-password --no-create-home appuser
USER appuser
# Requires: uv add uvicorn-worker gunicorn
CMD ["gunicorn", "app:create_app", "--factory", \
     "--worker-class", "uvicorn_worker.UvicornWorker", \
     "--workers", "4", "--bind", "0.0.0.0:8000"]
```

## Healthcheck

- Every service in `docker-compose.yml` must have a `healthcheck` configured.
- The app depends on `db` and `redis` with `condition: service_healthy`.
- The app's `/health` endpoint is used as the healthcheck by the load balancer.

```yaml
# CORRECT
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U elric"]
  interval: 5s
  timeout: 3s
  retries: 5
```

## If the App Does Not Reflect Changes

- In development with a mounted volume: uvicorn `--reload` should reload automatically.
- If not: `docker compose restart app` or `docker compose up --build`.
- If dependencies changed: `docker compose up --build` to rebuild the image.
