# Run Your App Locally

From your generated project directory:

```bash
# 1) install dependencies
uv sync

# 2) configure environment
cp .env.example .env

# 3) start local infrastructure
docker compose -f docker/docker-compose.yml up -d db redis

# 4) run migrations
elric migrate

# 5) start app
elric serve
```

Open:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- OpenAPI: `http://localhost:8000/openapi.json`

