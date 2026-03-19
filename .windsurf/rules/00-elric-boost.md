---
trigger: always_on
---

# Elric Boost Guidelines

The Elric Boost guidelines are specifically curated for this application. Follow them closely to ensure the best experience when building Elric applications.

## Foundational Context

This application is an Elric framework application. You are an expert with all of these packages and versions. Ensure you abide by them.

- python - 3.12
- fastapi - >=0.135.1
- uvicorn - >=0.42.0
- sqlmodel - >=0.0.37
- alembic - >=1.13
- asyncpg - >=0.31.0
- redis[asyncio] - >=5.0
- langchain - >=1.2.12
- langgraph - >=1.1.0
- langsmith - >=0.7.20
- pydantic-settings - >=2.0
- structlog - >=24.0
- typer - >=0.12
- jinja2 - >=3.1
- pytest - >=8.0
- pytest-asyncio - >=0.26
- ruff - >=0.15.6

## Skills Activation

This project has domain-specific skills available. You MUST activate the relevant skill whenever you work in that domain — don't wait until you're stuck.

- `agent-development` — Activates whenever creating or editing files in `app/agents/`, `app/chains/`, or `app/tools/`. Use when building LangGraph graphs, LangChain chains, defining tool functions, or wiring LangSmith tracing.
- `route-development` — Activates whenever creating or editing files in `app/routes/` or `app/controllers/`. Use when defining FastAPI routers, dependency injection, request schemas, or response models.
- `database-development` — Activates whenever creating or editing files in `database/models/` or `database/migrations/`. Use when defining SQLModel entities, writing Alembic migrations, or querying via async session.

## Conventions

- You must follow all existing code conventions used in this application. When creating or editing a file, check sibling files for the correct structure, approach, and naming.
- Use descriptive names for variables and functions. For example, `is_rate_limited`, `has_valid_api_key`, not `check()`.
- Use `snake_case` for all files, folders, variables, and functions. Use `PascalCase` only for class names.
- Check for existing base classes and utilities to reuse before writing new ones.

## CLI — Always Use the Elric CLI

- Use `uv run elric make:` commands to create new files (agents, chains, tools, routes, controllers, schemas, models, migrations, jobs, exceptions, tests).
- Never create these files manually — always go through the CLI to ensure stubs are applied correctly.
- Use `uv run elric route:list` to inspect registered routes before adding new ones.
- Use `uv run elric migrate:status` to check migration state before writing a new migration.

## Verification

- Do not create ad-hoc scripts to verify behavior when tests cover that functionality. Pytest tests are more important.
- Use `uv run pytest tests/ -x -q` to run the test suite.

## Application Structure & Architecture

- Stick to the existing directory structure. Do not create new top-level folders without approval.
- Do not change dependencies in `pyproject.toml` without approval.
- All configuration must go through `config/settings.py` (Pydantic Settings). Never use `os.environ` directly in application code.

## Replies

- Be concise — focus on what matters, not obvious details.

---

## Elric Boost Tools

### CLI Commands

- Before running a `uv run elric` command, verify the available subcommands with `uv run elric --help` or `uv run elric make --help` if unsure.

### Database

- Use `uv run elric migrate:status` to check current migration state.
- Use `uv run elric db:seed` to seed the database with initial data.
- Never use raw SQL. Always use SQLModel + async session.

### Debugging

- Use `uv run pytest --tb=short -x` to debug failing tests quickly.
- Inspect structlog JSON output to trace requests end-to-end via `trace_id`.
- Use the LangSmith trace UI to debug agent and chain runs when `LANGCHAIN_TRACING_V2=true`.

### Reading Logs

- All logs are structured JSON. Filter by `trace_id` to follow a single request through the full stack.
- In development, set `LOG_JSON=false` for human-readable output.

### Searching Documentation

- Always search official documentation before making implementation decisions for FastAPI, LangGraph, LangChain, LangSmith, SQLModel, or Alembic.
- Use multiple simple topic-based queries. For example: `['langgraph state', 'langgraph nodes edges']`.
- Do not include package names in queries — search by concept.
