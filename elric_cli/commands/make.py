import subprocess
from pathlib import Path

import typer

from elric_cli.utils import (
    get_project_root,
    get_stub_path,
    get_timestamp,
    render_template,
    to_kebab_case,
    to_pascal_case,
    to_snake_case,
    write_file,
)

app = typer.Typer(help="Generate components from stubs")


@app.command("agent")
def make_agent(name: str):
    """Generate a new LangGraph agent."""
    class_name = to_pascal_case(name)
    snake_name = to_snake_case(name)
    
    context = {
        "class_name": class_name,
        "snake_name": snake_name,
        "kebab_name": to_kebab_case(name),
    }
    
    content = render_template(get_stub_path("agent"), context)
    output_path = get_project_root() / "app" / "ai" / "agents" / f"{snake_name}.py"
    
    write_file(str(output_path), content)
    typer.secho(f"✓ Created agent: {output_path}", fg=typer.colors.GREEN)


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
        result = subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", description],
            cwd=get_project_root(),
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            typer.secho(f"✓ Created migration: {description}", fg=typer.colors.GREEN)
            typer.echo(result.stdout)
        else:
            typer.secho(f"✗ Failed to create migration", fg=typer.colors.RED)
            typer.echo(result.stderr)
            raise typer.Exit(1)
    except FileNotFoundError:
        typer.secho("✗ Alembic not found. Make sure it's installed.", fg=typer.colors.RED)
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
