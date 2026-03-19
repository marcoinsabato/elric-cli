---
trigger: glob
globs: ["app/agents/**/*.py", "app/chains/**/*.py", "app/tools/**/*.py"]
---

# Agents, Chains & Tools — LangGraph / LangChain / LangSmith

- IMPORTANT: Activate the `agent-development` skill whenever working in `app/agents/`, `app/chains/`, or `app/tools/`.
- CRITICAL: Always search official LangGraph and LangChain documentation before implementing new patterns — APIs evolve quickly across major versions.

## Package Versions in Use

- `langgraph` >=1.1.0 — stable 1.x API, breaking changes from 0.x
- `langchain` >=1.2.12 — stable 1.x API, breaking changes from 0.x
- `langsmith` >=0.7.20

## Agents — LangGraph

- Every agent must extend `BaseAgent` from `app/agents/base_agent.py`. Never instantiate `StateGraph` directly in a controller.
- Always generate the file with: `uv run elric make:agent AgentName`
- The `build_graph()` method must return an uncompiled `StateGraph`. Compilation happens inside `run()`.
- Always use `ainvoke()` — never `invoke()` in an async context.
- Always define state as a `TypedDict` or dataclass — never use a raw `dict` as state.

```python
# CORRECT — typed state
from typing import TypedDict

class ChatState(TypedDict):
    messages: list[str]
    context: str
    output: str | None

class ChatAgent(BaseAgent):
    name = "chat_agent"

    def build_graph(self) -> StateGraph:
        graph = StateGraph(ChatState)
        graph.add_node("process", self._process)
        graph.add_node("respond", self._respond)
        graph.add_edge("process", "respond")
        graph.set_entry_point("process")
        return graph

    async def _process(self, state: ChatState) -> ChatState:
        ...
```

## Chains — LangChain

- Every chain must extend `BaseChain` from `app/chains/base_chain.py`.
- Always generate with: `uv run elric make:chain ChainName`
- Use `ainvoke()` — never `invoke()` or the deprecated `run()`.
- Always define `PromptTemplate` as a class attribute, not inline inside a method.
- Always use an explicit `output_parser` — never do manual string parsing of the output.

```python
# CORRECT
class SummarizeChain(BaseChain):
    name = "summarize_chain"

    prompt = PromptTemplate.from_template(
        "Summarize the following text in {language}:\n\n{text}"
    )

    async def run(self, text: str, language: str = "English") -> str:
        chain = self.prompt | self.llm | StrOutputParser()
        return await chain.ainvoke({"text": text, "language": language})
```

## Tools — LangChain

- Always generate with: `uv run elric make:tool ToolName`
- Use the `@tool` decorator from LangChain or extend `BaseTool`.
- Every tool must have a docstring — LangChain uses it as the description passed to the LLM.
- Use `args_schema` with a Pydantic model to validate tool inputs.
- Tools must be pure functions — no undeclared side effects.

```python
# CORRECT
class SearchInput(BaseModel):
    query: str
    max_results: int = 5

@tool(args_schema=SearchInput)
async def search_documents(query: str, max_results: int = 5) -> list[dict]:
    """Search internal documents by semantic similarity."""
    ...
```

## LangSmith Tracing

- Tracing is enabled automatically by `app/providers/langsmith.py` when `LANGCHAIN_TRACING_V2=true`.
- Do not add manual tracing in controllers — `BaseAgent` and `BaseChain` handle it.
- To attach custom metadata to a run, use `langsmith.trace()` as a context manager.
- In development, use the LangSmith UI to inspect input/output for every graph node.
- In production, every run is automatically tagged with the `trace_id` from the HTTP request.

## LangGraph Node Naming

- Use descriptive `snake_case` names for all nodes: `validate_input`, `fetch_context`, `generate_response`.
- Never use generic names like `step1`, `process`, `node`.
- Conditional edge routers (`add_conditional_edges`) must use a named router function.

```python
# CORRECT
graph.add_conditional_edges(
    "validate_input",
    self._route_by_intent,           # explicit named router function
    {"chat": "generate_response", "search": "fetch_context"}
)

# WRONG
graph.add_conditional_edges("process", lambda x: x["type"], {...})
```

## LangGraph 1.x Notes

- `StateGraph` now supports `interrupt_before` and `interrupt_after` for human-in-the-loop — prefer these over manual checkpointing.
- Use `MemorySaver` for in-process state persistence during development; replace with a persistent checkpointer in production.
- `CompiledGraph.stream()` and `CompiledGraph.astream()` are the preferred way to stream node outputs to clients.
