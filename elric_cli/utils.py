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
