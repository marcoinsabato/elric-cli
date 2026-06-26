# Project Structure and Conventions

## Core structure

- `app/routes`: HTTP route modules
- `app/controllers`: request orchestration
- `app/ai`: agents, chains, tools
- `app/middleware`: auth/logging/rate-limit middleware
- `database/models`: SQLModel entities
- `database/migrations`: Alembic revisions

## Conventions

- Keep routes thin
- Put orchestration in controllers
- Keep reusable logic in AI/service modules
- Use generated files as the default starting point

