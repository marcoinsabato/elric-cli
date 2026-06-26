import typer

from elric_cli.utils import run_with_project_environment

app = typer.Typer(help="Database utility commands")


@app.command("seed")
def db_seed() -> None:
    """Run database seeders."""
    try:
        result = run_with_project_environment(["python", "-m", "database.seeders"])
        if result.returncode == 0:
            typer.echo(result.stdout)
            typer.secho("✓ Database seeded", fg=typer.colors.GREEN)
            return
        typer.secho("✗ Database seeding failed", fg=typer.colors.RED)
        typer.echo(result.stderr)
        raise typer.Exit(result.returncode)
    except FileNotFoundError:
        typer.secho("✗ uv not found. Make sure it's installed.", fg=typer.colors.RED)
        raise typer.Exit(1)
    except RuntimeError as e:
        typer.secho(f"✗ {e}", fg=typer.colors.RED)
        raise typer.Exit(1)
