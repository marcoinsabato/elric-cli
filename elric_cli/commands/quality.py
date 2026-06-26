import typer

from elric_cli.utils import run_with_project_environment


def lint() -> None:
    """Run Ruff lint with auto-fix."""
    try:
        result = run_with_project_environment(["ruff", "check", "--fix", "."])
        typer.echo(result.stdout)
        if result.returncode != 0:
            typer.echo(result.stderr)
            raise typer.Exit(result.returncode)
    except FileNotFoundError:
        typer.secho("✗ uv not found. Make sure it's installed.", fg=typer.colors.RED)
        raise typer.Exit(1)
    except RuntimeError as e:
        typer.secho(f"✗ {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


def format_code() -> None:
    """Run Ruff formatter."""
    try:
        result = run_with_project_environment(["ruff", "format", "."])
        typer.echo(result.stdout)
        if result.returncode != 0:
            typer.echo(result.stderr)
            raise typer.Exit(result.returncode)
    except FileNotFoundError:
        typer.secho("✗ uv not found. Make sure it's installed.", fg=typer.colors.RED)
        raise typer.Exit(1)
    except RuntimeError as e:
        typer.secho(f"✗ {e}", fg=typer.colors.RED)
        raise typer.Exit(1)
