---
trigger: glob
globs: ["app/**/*.py", "elric_cli/**/*.py", "config/**/*.py"]
---

# Python & FastAPI

## Foundational Rules

- Always use `async def` for all I/O-bound operations (database, Redis, HTTP calls, file I/O).
- Use `def` only for pure CPU-bound functions with no I/O.
- Always use explicit return type annotations on every function and method.
- Always use type hints for all parameters. Prefer Pydantic models over raw `dict` for input/output.

```python
# CORRECT
async def get_api_key(key_id: uuid.UUID, session: AsyncSession) -> ApiKeyResponse:
    ...

# WRONG
async def get_api_key(key_id, session):
    ...
```

## FastAPI Conventions

- Use `APIRouter` for each domain — never register routes directly on the `app` instance.
- Always use `Depends()` for dependency injection (DB session, API key, settings).
- Use `HTTPException` for expected, well-defined errors in controllers.
- For unexpected errors, let them propagate to the `GlobalExceptionHandler` — never use bare `except Exception`.
- Use the `lifespan` context manager for startup/shutdown. Never use `@app.on_event`.

```python
# CORRECT — lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_redis()
    yield

# WRONG
@app.on_event("startup")
async def startup():
    ...
```

## Request & Response Schemas

- Every route must have an explicit Pydantic schema for request body and response.
- Always generate schemas with: `uv run elric make:schema SchemeName`
- Keep request schemas separate from response schemas — never reuse the same model for both.
- Use the RORO pattern (Receive an Object, Return an Object) for all controllers.

```python
# CORRECT — separate schemas
class CreateChatRequest(BaseModel):
    message: str
    session_id: uuid.UUID

class ChatResponse(BaseModel):
    reply: str
    trace_id: str
```

## Error Handling

- Never handle exceptions in controllers. Raise `ElricException` or one of its subclasses.
- The `GlobalExceptionHandler` in `app/exceptions/handler.py` handles everything centrally.
- To create new exception types: `uv run elric make:exception ExceptionName`

```python
# CORRECT
async def run_agent(request: RunAgentRequest) -> AgentResponse:
    result = await agent.run(request.input)
    if not result:
        raise NotFoundException("Agent produced no output")
    return AgentResponse(**result)

# WRONG
async def run_agent(request: RunAgentRequest) -> AgentResponse:
    try:
        result = await agent.run(request.input)
    except Exception as e:
        return {"error": str(e)}
```

## Configuration

- Never use `os.environ` directly in application code.
- Always use `get_settings()` from `config/settings.py`.

```python
# CORRECT
from config.settings import get_settings
settings = get_settings()
redis_url = settings.REDIS_URL

# WRONG
import os
redis_url = os.environ.get("REDIS_URL")
```

## Imports

- Required order: stdlib → third-party → internal (`app/`, `config/`, `database/`).
- Use absolute imports only. Never relative imports (`from ..models import ...`).

## Naming

- Files and folders: `snake_case` (e.g. `chat_agent.py`, `api_key.py`)
- Classes: `PascalCase` (e.g. `ChatAgent`, `ApiKeyMiddleware`)
- Functions and variables: `snake_case` with auxiliary verbs (e.g. `is_active`, `has_expired`, `get_session`)
- Constants: `UPPER_SNAKE_CASE`

## Content-Type Checking (FastAPI >=0.135)

- FastAPI now enforces strict Content-Type validation by default for JSON endpoints.
- If a client does not send `Content-Type: application/json`, the request will be rejected with 422.
- To disable this for a specific route (e.g. for legacy clients): `app = FastAPI(strict_content_type=False)`.
