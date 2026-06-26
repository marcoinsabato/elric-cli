from pathlib import Path

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


def register_seeder_in_runner(project_root: Path, snake_name: str) -> None:
    """Register a seeder in database/seeders/__main__.py."""
    runner_path = project_root / "database" / "seeders" / "__main__.py"
    import_line = f"from database.seeders.{snake_name}_seeder import run as run_{snake_name}_seeder"
    await_line = f"    await run_{snake_name}_seeder()"

    if not runner_path.exists():
        base_content = (
            "import asyncio\n\n\n"
            "async def main() -> None:\n"
            "    pass\n\n\n"
            "if __name__ == \"__main__\":\n"
            "    asyncio.run(main())\n"
        )
        write_file(str(runner_path), base_content)

    content = runner_path.read_text()

    if import_line not in content:
        content = content.replace("import asyncio", f"import asyncio\n{import_line}")

    if await_line not in content:
        if "    pass" in content:
            content = content.replace("    pass", await_line)
        else:
            marker = "async def main() -> None:\n"
            content = content.replace(marker, f"{marker}{await_line}\n")

    write_file(str(runner_path), content)


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


@app.command("request")
def make_request(name: str):
    """Generate a new request schema."""
    class_base_name = to_pascal_case(name).removesuffix("Request")
    snake_base_name = to_snake_case(name).removesuffix("_request")

    context = {
        "class_name": class_base_name,
        "snake_name": snake_base_name,
        "kebab_name": to_kebab_case(snake_base_name),
    }

    content = render_template(get_stub_path("request"), context)
    output_path = get_project_root() / "app" / "schemas" / "requests" / f"{snake_base_name}_request.py"

    write_file(str(output_path), content)
    typer.secho(f"✓ Created request schema: {output_path}", fg=typer.colors.GREEN)


@app.command("response")
def make_response(name: str):
    """Generate a new response schema."""
    class_base_name = to_pascal_case(name).removesuffix("Response")
    snake_base_name = to_snake_case(name).removesuffix("_response")

    context = {
        "class_name": class_base_name,
        "snake_name": snake_base_name,
        "kebab_name": to_kebab_case(snake_base_name),
    }

    content = render_template(get_stub_path("response"), context)
    output_path = get_project_root() / "app" / "schemas" / "responses" / f"{snake_base_name}_response.py"

    write_file(str(output_path), content)
    typer.secho(f"✓ Created response schema: {output_path}", fg=typer.colors.GREEN)


@app.command("model")
def make_model(
    name: str,
    migration: bool = typer.Option(False, "--migration", "-m", help="Also create a migration"),
    route: bool = typer.Option(False, "--route", "-r", help="Also create a route"),
    controller: bool = typer.Option(False, "--controller", "-c", help="Also create a controller"),
    request: bool = typer.Option(False, "--request", help="Also create a request schema"),
    response: bool = typer.Option(False, "--response", help="Also create a response schema"),
):
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

    if route:
        make_route(name)
    if controller:
        make_controller(name)
    if request:
        make_request(name)
    if response:
        make_response(name)
    if migration:
        make_migration(f"create_{snake_name}")


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


@app.command("seeder")
def make_seeder(
    name: str,
    register: bool = typer.Option(False, "--register", help="Also register the seeder in database/seeders/__main__.py"),
):
    """Generate a new database seeder."""
    class_name = to_pascal_case(name).removesuffix("Seeder")
    snake_name = to_snake_case(name).removesuffix("_seeder")

    context = {
        "class_name": class_name,
        "snake_name": snake_name,
        "kebab_name": to_kebab_case(name),
    }

    content = render_template(get_stub_path("seeder"), context)
    project_root = get_project_root()
    output_path = project_root / "database" / "seeders" / f"{snake_name}_seeder.py"

    write_file(str(output_path), content)
    typer.secho(f"✓ Created seeder: {output_path}", fg=typer.colors.GREEN)

    if register:
        register_seeder_in_runner(project_root, snake_name)
        typer.secho("✓ Registered seeder in database/seeders/__main__.py", fg=typer.colors.GREEN)
