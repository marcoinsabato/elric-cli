import subprocess
from pathlib import Path
from typing import Optional

import typer

from elric_cli.utils import (
    AGENT_TYPES,
    DEFAULT_MODEL,
    get_agent_stub_name,
    get_available_models,
    get_llm_config,
    get_project_root,
    get_provider_from_model,
    get_stub_path,
    get_timestamp,
    render_template,
    to_kebab_case,
    to_pascal_case,
    to_snake_case,
    validate_model,
    write_file,
    run_with_project_environment,
)

app = typer.Typer(help="Generate components from stubs")


@app.command("agent")
def make_agent(
    name: str,
    type: str = typer.Option("simple", "--type", "-t", help=f"Agent type: {', '.join(AGENT_TYPES.keys())}"),
    model: str = typer.Option(DEFAULT_MODEL, "--model", "-m", help="LLM model to use"),
):
    """Generate a new LangGraph agent with specified type and model."""
    class_name = to_pascal_case(name)
    snake_name = to_snake_case(name)
    
    # Validate agent type
    if type not in AGENT_TYPES:
        typer.secho(f"✗ Invalid agent type: {type}", fg=typer.colors.RED)
        typer.secho(f"  Available types: {', '.join(AGENT_TYPES.keys())}", fg=typer.colors.YELLOW)
        raise typer.Exit(1)
    
    # Validate model (warn if not in predefined list)
    if not validate_model(model):
        typer.secho(f"⚠ Warning: '{model}' is not in the predefined model list", fg=typer.colors.YELLOW)
        typer.secho(f"  Available models: {', '.join(get_available_models()[:5])}...", fg=typer.colors.YELLOW)
        typer.secho(f"  Proceeding anyway with auto-detected provider", fg=typer.colors.YELLOW)
    
    # Get LLM configuration
    llm_config = get_llm_config(model)
    provider = get_provider_from_model(model)
    
    # Get the appropriate stub
    stub_name = get_agent_stub_name(type)
    
    context = {
        "class_name": class_name,
        "snake_name": snake_name,
        "kebab_name": to_kebab_case(name),
        "model_name": model,
        "llm_import": llm_config["import"],
        "llm_class": llm_config["class"],
        "provider": provider,
    }
    
    content = render_template(get_stub_path(stub_name), context)
    output_path = get_project_root() / "app" / "ai" / "agents" / f"{snake_name}.py"
    
    write_file(str(output_path), content)
    typer.secho(f"✓ Created {type} agent: {output_path}", fg=typer.colors.GREEN)
    typer.secho(f"  Model: {model} ({provider})", fg=typer.colors.BLUE)


@app.command("chain")
def make_chain(name: str):
    """Generate a new LangChain chain."""
    class_name = to_pascal_case(name)
    snake_name = to_snake_case(name)
    
    context = {
        "class_name": class_name,
        "snake_name": snake_name,
        "kebab_name": to_kebab_case(name),
    }
    
    content = render_template(get_stub_path("chain"), context)
    output_path = get_project_root() / "app" / "ai" / "chains" / f"{snake_name}.py"
    
    write_file(str(output_path), content)
    typer.secho(f"✓ Created chain: {output_path}", fg=typer.colors.GREEN)


@app.command("tool")
def make_tool(name: str):
    """Generate a new LangChain tool."""
    class_name = to_pascal_case(name)
    snake_name = to_snake_case(name)
    
    context = {
        "class_name": class_name,
        "snake_name": snake_name,
        "kebab_name": to_kebab_case(name),
    }
    
    content = render_template(get_stub_path("tool"), context)
    output_path = get_project_root() / "app" / "ai" / "tools" / f"{snake_name}.py"
    
    write_file(str(output_path), content)
    typer.secho(f"✓ Created tool: {output_path}", fg=typer.colors.GREEN)


@app.command("route")
def make_route(name: str):
    """Generate a new FastAPI router."""
    class_name = to_pascal_case(name)
    snake_name = to_snake_case(name)
    
    context = {
        "class_name": class_name,
        "snake_name": snake_name,
        "kebab_name": to_kebab_case(name),
    }
    
    content = render_template(get_stub_path("route"), context)
    output_path = get_project_root() / "app" / "routes" / f"{snake_name}.py"
    
    write_file(str(output_path), content)
    typer.secho(f"✓ Created route: {output_path}", fg=typer.colors.GREEN)


@app.command("controller")
def make_controller(name: str):
    """Generate a new controller."""
    class_name = to_pascal_case(name)
    snake_name = to_snake_case(name)
    
    context = {
        "class_name": class_name,
        "snake_name": snake_name,
        "kebab_name": to_kebab_case(name),
    }
    
    content = render_template(get_stub_path("controller"), context)
    output_path = get_project_root() / "app" / "controllers" / f"{snake_name}.py"
    
    write_file(str(output_path), content)
    typer.secho(f"✓ Created controller: {output_path}", fg=typer.colors.GREEN)


@app.command("schema")
def make_schema(name: str):
    """Generate a new Pydantic schema."""
    class_name = to_pascal_case(name)
    snake_name = to_snake_case(name)
    
    context = {
        "class_name": class_name,
        "snake_name": snake_name,
        "kebab_name": to_kebab_case(name),
    }
    
    content = render_template(get_stub_path("schema"), context)
    output_path = get_project_root() / "app" / "schemas" / f"{snake_name}.py"
    
    write_file(str(output_path), content)
    typer.secho(f"✓ Created schema: {output_path}", fg=typer.colors.GREEN)


@app.command("model")
def make_model(name: str):
    """Generate a new SQLModel entity."""
    class_name = to_pascal_case(name)
    snake_name = to_snake_case(name)
    
    context = {
        "class_name": class_name,
        "snake_name": snake_name,
        "kebab_name": to_kebab_case(name),
    }
    
    content = render_template(get_stub_path("model"), context)
    output_path = get_project_root() / "database" / "models" / f"{snake_name}.py"
    
    write_file(str(output_path), content)
    typer.secho(f"✓ Created model: {output_path}", fg=typer.colors.GREEN)


@app.command("migration")
def make_migration(description: str):
    """Generate a new Alembic migration."""
    try:
        result = run_with_project_environment(["alembic", "revision", "--autogenerate", "-m", description])
        
        if result.returncode == 0:
            typer.secho(f"✓ Created migration: {description}", fg=typer.colors.GREEN)
            typer.echo(result.stdout)
        else:
            typer.secho(f"✗ Failed to create migration", fg=typer.colors.RED)
            typer.echo(result.stderr)
            raise typer.Exit(1)
    except FileNotFoundError:
        typer.secho("✗ uv not found. Make sure it's installed.", fg=typer.colors.RED)
        raise typer.Exit(1)
    except RuntimeError as e:
        typer.secho(f"✗ {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


@app.command("job")
def make_job(name: str):
    """Generate a new background job."""
    class_name = to_pascal_case(name)
    snake_name = to_snake_case(name)
    
    context = {
        "class_name": class_name,
        "snake_name": snake_name,
        "kebab_name": to_kebab_case(name),
    }
    
    content = render_template(get_stub_path("job"), context)
    output_path = get_project_root() / "app" / "jobs" / f"{snake_name}.py"
    
    write_file(str(output_path), content)
    typer.secho(f"✓ Created job: {output_path}", fg=typer.colors.GREEN)


@app.command("exception")
def make_exception(name: str):
    """Generate a new custom exception."""
    class_name = to_pascal_case(name)
    snake_name = to_snake_case(name)
    
    context = {
        "class_name": class_name,
        "snake_name": snake_name,
        "kebab_name": to_kebab_case(name),
    }
    
    content = render_template(get_stub_path("exception"), context)
    output_path = get_project_root() / "app" / "exceptions" / f"{snake_name}.py"
    
    write_file(str(output_path), content)
    typer.secho(f"✓ Created exception: {output_path}", fg=typer.colors.GREEN)


@app.command("test")
def make_test(name: str):
    """Generate a new test file."""
    class_name = to_pascal_case(name)
    snake_name = to_snake_case(name)
    
    context = {
        "class_name": class_name,
        "snake_name": snake_name,
        "kebab_name": to_kebab_case(name),
    }
    
    content = render_template(get_stub_path("test"), context)
    output_path = get_project_root() / "tests" / "unit" / f"test_{snake_name}.py"
    
    write_file(str(output_path), content)
    typer.secho(f"✓ Created test: {output_path}", fg=typer.colors.GREEN)
