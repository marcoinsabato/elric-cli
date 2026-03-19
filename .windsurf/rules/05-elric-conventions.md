---
trigger: glob
globs: ["**/*.py"]
---

# Elric Conventions

These conventions are specific to the Elric framework. Follow them in every file of the project.

## CLI — Golden Rule

**Never create framework component files manually.** Always use the CLI:

| Component | Command |
|---|---|
| Agent | `uv run elric make:agent AgentName` |
| Chain | `uv run elric make:chain ChainName` |
| Tool | `uv run elric make:tool ToolName` |
| Route | `uv run elric make:route RouteName` |
| Controller | `uv run elric make:controller ControllerName` |
| Schema | `uv run elric make:schema SchemaName` |
| Model | `uv run elric make:model ModelName` |
| Migration | `uv run elric make:migration description` |
| Job | `uv run elric make:job JobName` |
| Exception | `uv run elric make:exception ExceptionName` |
| Test | `uv run elric make:test TestName` |

## File Structure

- One component per file. Never put more than one class in the same file (except models with their related Pydantic response classes).
- The file name must match the class name in `snake_case`.
  - `ChatAgent` → `app/agents/chat_agent.py`
  - `ApiKeyMiddleware` → `app/middleware/api_key.py`
  - `CreatePostRequest` → `app/schemas/create_post_request.py`

## Base Classes — Always Extend

- Agents → `BaseAgent` from `app/agents/base_agent.py`
- Chains → `BaseChain` from `app/chains/base_chain.py`
- Tools → `BaseTool` from `app/tools/base_tool.py`
- Exceptions → `ElricException` from `app/exceptions/base.py`

## Routing

- Each router in `app/routes/` handles a single domain (e.g. `chat.py`, `users.py`).
- Routers are registered in `app/__init__.py` via `app.include_router()`.
- Before adding a new route: run `uv run elric route:list` to verify it does not already exist.
- Always prefix API routes with `/api/v1/`.

```python
# CORRECT
router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def create_chat(
    request: CreateChatRequest,
    session: AsyncSession = Depends(get_session),
    api_key: ApiKey = Depends(get_current_api_key),
) -> ChatResponse:
    ...
```

## Controllers

- Controllers contain no business logic — they delegate to agents, chains, or services.
- Controllers never handle exceptions — they let them propagate to `GlobalExceptionHandler`.
- Every controller imports its request and response schemas from `app/schemas/`.

## Auth — API Key

- Every protected endpoint must declare `api_key: ApiKey = Depends(get_current_api_key)`.
- The `/health` endpoint is the only route excluded from authentication.
- Never hardcode API keys in the codebase. Always use `config/settings.py`.

## Logging

- Never use `print()`. Ever.
- Never use the standard `logging` module — always use `structlog`.
- The `trace_id` is automatically available in the context — never pass it explicitly between functions.

```python
# CORRECT
import structlog
log = structlog.get_logger()

async def run_agent(input: dict) -> dict:
    log.info("agent.run.started", agent=self.name, input_keys=list(input.keys()))
    result = await self._execute(input)
    log.info("agent.run.completed", agent=self.name)
    return result

# WRONG
print(f"Running agent with input: {input}")
```

## Testing

- Always generate with: `uv run elric make:test TestName`
- Use `pytest-asyncio` for all tests involving async operations.
- Use fixtures in `tests/conftest.py` for DB session, HTTP client, and test data.
- Every new component must have at least one unit test.
- Run tests with: `uv run pytest tests/ -x -q`

```python
# CORRECT — async test with fixture
@pytest.mark.asyncio
async def test_chat_agent_returns_response(db_session: AsyncSession) -> None:
    agent = ChatAgent()
    result = await agent.run({"message": "hello"})
    assert "reply" in result
    assert isinstance(result["reply"], str)
```

## Ruff — Formatter and Linter

- Always run `uv run ruff check --fix .` and `uv run ruff format .` before finalizing changes.
- Never suppress ruff warnings without an explicit justification.
- Ruff >=0.15.6 introduces the 2026 style guide — lambda bodies are now parenthesized. Do not override this behavior.
