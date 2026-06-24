import shutil
import subprocess
from pathlib import Path

import typer

DEFAULT_TEMPLATE_REPO = "https://github.com/marcoinsabato/elric-template.git"


def new_project(
    name: str = typer.Argument(..., help="Project name"),
    directory: Path = typer.Option(Path("."), "--directory", "-d", help="Directory where project will be created"),
    install: bool = typer.Option(True, "--install/--no-install", help="Run `uv sync` after project creation"),
    keep_git: bool = typer.Option(False, "--keep-git", help="Keep template .git history"),
):
    """Create a new Elric project from a remote template repository."""
    template_repo = DEFAULT_TEMPLATE_REPO

    target_path = (directory / name).resolve()
    if target_path.exists() and any(target_path.iterdir()):
        typer.secho(f"✗ Target directory is not empty: {target_path}", fg=typer.colors.RED)
        raise typer.Exit(1)
    if target_path.exists() and not target_path.is_dir():
        typer.secho(f"✗ Target path is not a directory: {target_path}", fg=typer.colors.RED)
        raise typer.Exit(1)

    clone_command = ["git", "clone", "--depth", "1"]
    clone_command.extend([template_repo, str(target_path)])

    typer.secho(f"Creating project: {name}", fg=typer.colors.BLUE)
    typer.secho(f"Template: {template_repo}", fg=typer.colors.BLUE)
    typer.secho(f"Destination: {target_path}", fg=typer.colors.BLUE)

    try:
        clone_result = subprocess.run(clone_command, capture_output=True, text=True)
    except FileNotFoundError:
        typer.secho("✗ Git not found. Install git and retry.", fg=typer.colors.RED)
        raise typer.Exit(1)

    if clone_result.returncode != 0:
        typer.secho("✗ Failed to clone template repository.", fg=typer.colors.RED)
        if clone_result.stderr:
            typer.echo(clone_result.stderr.strip())
        raise typer.Exit(1)

    if not keep_git:
        git_dir = target_path / ".git"
        if git_dir.exists() and git_dir.is_dir():
            shutil.rmtree(git_dir)

    if install:
        typer.secho("Installing dependencies with uv sync...", fg=typer.colors.BLUE)
        try:
            install_result = subprocess.run(["uv", "sync"], cwd=target_path, capture_output=True, text=True)
        except FileNotFoundError:
            typer.secho("⚠ uv not found. Skip install and run `uv sync` manually.", fg=typer.colors.YELLOW)
            install_result = None
        if install_result and install_result.returncode != 0:
            typer.secho("⚠ Dependency installation failed. You can run `uv sync` manually.", fg=typer.colors.YELLOW)
            if install_result.stderr:
                typer.echo(install_result.stderr.strip())

    typer.secho("✓ Project created successfully!", fg=typer.colors.GREEN)
    typer.echo("")
    typer.secho("Next steps:", fg=typer.colors.BLUE)
    typer.echo(f"  cd {target_path}")
    if not install:
        typer.echo("  uv sync")
    typer.echo("  cp .env.example .env")
    typer.echo("  docker compose -f docker/docker-compose.yml up -d db redis")
    typer.echo("  elric migrate")
    typer.echo("  elric serve")
