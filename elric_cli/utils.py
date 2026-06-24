import re
from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Template


def to_snake_case(name: str) -> str:
    """Convert PascalCase or camelCase to snake_case."""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def to_pascal_case(name: str) -> str:
    """Convert snake_case or kebab-case to PascalCase."""
    # If already in PascalCase, return as is
    if name and name[0].isupper() and "_" not in name and "-" not in name:
        return name
    words = re.split(r"[_-]", name)
    return "".join(word.capitalize() for word in words)


def to_kebab_case(name: str) -> str:
    """Convert PascalCase or snake_case to kebab-case."""
    return to_snake_case(name).replace("_", "-")


def get_timestamp() -> str:
    """Get timestamp for migrations in format: YYYYMMDDHHMMSS."""
    return datetime.now().strftime("%Y%m%d%H%M%S")


def render_template(stub_path: str, context: dict[str, Any]) -> str:
    """Render a Jinja2 template with the given context."""
    with open(stub_path, "r") as f:
        template_content = f.read()
    
    template = Template(template_content)
    return template.render(**context)


def ensure_directory(path: str) -> None:
    """Create directory if it doesn't exist."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def write_file(path: str, content: str) -> None:
    """Write content to file, creating directory if needed."""
    ensure_directory(path)
    with open(path, "w") as f:
        f.write(content)


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def get_stub_path(stub_name: str) -> str:
    """Get the full path to a stub file."""
    return str(get_project_root() / "stubs" / f"{stub_name}.stub.py")


# Model configurations
AVAILABLE_MODELS = {
    # Anthropic models
    "claude-3-5-sonnet-20241022": "anthropic",
    "claude-3-5-sonnet": "anthropic",
    "claude-3-opus-20240229": "anthropic",
    "claude-3-opus": "anthropic",
    "claude-3-sonnet-20240229": "anthropic",
    "claude-3-haiku-20240307": "anthropic",
    "claude-3-haiku": "anthropic",
    
    # OpenAI models
    "gpt-4o": "openai",
    "gpt-4o-mini": "openai",
    "gpt-4-turbo": "openai",
    "gpt-4": "openai",
    "gpt-3.5-turbo": "openai",
    
    # Google models
    "gemini-1.5-pro": "google",
    "gemini-1.5-flash": "google",
    "gemini-pro": "google",
    
    # Cohere models
    "command-r-plus": "cohere",
    "command-r": "cohere",
    "command": "cohere",
}

# Default model
DEFAULT_MODEL = "gpt-4o"

# Provider to LangChain class mapping
PROVIDER_LLM_MAP = {
    "anthropic": {
        "import": "langchain_anthropic import ChatAnthropic",
        "class": "ChatAnthropic"
    },
    "openai": {
        "import": "langchain_openai import ChatOpenAI",
        "class": "ChatOpenAI"
    },
    "google": {
        "import": "langchain_google_genai import ChatGoogleGenerativeAI",
        "class": "ChatGoogleGenerativeAI"
    },
    "cohere": {
        "import": "langchain_cohere import ChatCohere",
        "class": "ChatCohere"
    }
}

# Agent types
AGENT_TYPES = {
    "simple": "agent_simple",
    "chat": "agent_chat",
    "tool": "agent_tool",
    "react": "agent_react",
    "planner": "agent_planner",
    "streaming": "agent_streaming",
}


def get_provider_from_model(model: str) -> str:
    """Get the provider name from a model name."""
    if model in AVAILABLE_MODELS:
        return AVAILABLE_MODELS[model]
    
    # Try to detect provider from model name prefix
    model_lower = model.lower()
    if "claude" in model_lower:
        return "anthropic"
    elif "gpt" in model_lower:
        return "openai"
    elif "gemini" in model_lower:
        return "google"
    elif "command" in model_lower:
        return "cohere"
    
    # Default to OpenAI
    return "openai"


def get_llm_config(model: str) -> dict[str, str]:
    """Get LLM import and class name for a given model."""
    provider = get_provider_from_model(model)
    return PROVIDER_LLM_MAP.get(provider, PROVIDER_LLM_MAP["openai"])


def validate_model(model: str) -> bool:
    """Check if a model is in the list of known models."""
    return model in AVAILABLE_MODELS


def get_available_models() -> list[str]:
    """Get list of all available models."""
    return list(AVAILABLE_MODELS.keys())


def get_agent_stub_name(agent_type: str) -> str:
    """Get the stub file name for a given agent type."""
    return AGENT_TYPES.get(agent_type, "agent_simple")
