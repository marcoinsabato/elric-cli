import typer

from elric_cli.utils import run_with_project_environment

app = typer.Typer(help="Database migration commands")


def run_alembic_command(args: list[str]) -> None:
    """Run an Alembic command."""
    try:
        result = run_with_project_environment(["alembic", *args])
        
        if result.returncode == 0:
            typer.echo(result.stdout)
        else:
            typer.secho(f"✗ Command failed", fg=typer.colors.RED)
            typer.echo(result.stderr)
            raise typer.Exit(1)
    except FileNotFoundError:
        typer.secho("✗ uv not found. Make sure it's installed.", fg=typer.colors.RED)
        raise typer.Exit(1)
    except RuntimeError as e:
        typer.secho(f"✗ {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


@app.callback(invoke_without_command=True)
def migrate_up(ctx: typer.Context):
    """Run all pending migrations (alembic upgrade head)."""
    if ctx.invoked_subcommand is not None:
        return
    typer.secho("Running migrations...", fg=typer.colors.BLUE)
    run_alembic_command(["upgrade", "head"])
    typer.secho("✓ Migrations completed", fg=typer.colors.GREEN)


@app.command("rollback")
def migrate_rollback():
    """Rollback the last migration (alembic downgrade -1)."""
    typer.secho("Rolling back last migration...", fg=typer.colors.BLUE)
    run_alembic_command(["downgrade", "-1"])
    typer.secho("✓ Rollback completed", fg=typer.colors.GREEN)


@app.command("fresh")
def migrate_fresh():
    """Drop all tables and re-run all migrations."""
    confirm = typer.confirm(
        "⚠️  This will DROP ALL TABLES and re-run migrations. Continue?",
        abort=True,
    )
    
    if confirm:
        typer.secho("Dropping all tables...", fg=typer.colors.BLUE)
        run_alembic_command(["downgrade", "base"])
        
        typer.secho("Running all migrations...", fg=typer.colors.BLUE)
        run_alembic_command(["upgrade", "head"])
        
        typer.secho("✓ Fresh migration completed", fg=typer.colors.GREEN)


@app.command("status")
def migrate_status():
    """Show current migration status (alembic current)."""
    typer.secho("Current migration status:", fg=typer.colors.BLUE)
    run_alembic_command(["current"])
