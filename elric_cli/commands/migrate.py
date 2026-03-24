import subprocess

import typer

from elric_cli.utils import get_project_root

app = typer.Typer(help="Database migration commands")


def run_alembic_command(args: list[str]) -> None:
    """Run an Alembic command."""
    try:
        result = subprocess.run(
            ["alembic"] + args,
            cwd=get_project_root(),
            capture_output=True,
            text=True,
        )
        
        if result.returncode == 0:
            typer.echo(result.stdout)
        else:
            typer.secho(f"✗ Command failed", fg=typer.colors.RED)
            typer.echo(result.stderr)
            raise typer.Exit(1)
    except FileNotFoundError:
        typer.secho("✗ Alembic not found. Make sure it's installed.", fg=typer.colors.RED)
        raise typer.Exit(1)


@app.command()
def migrate():
    """Run all pending migrations (alembic upgrade head)."""
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
