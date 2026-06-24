import typer

from elric_cli.utils import run_with_project_environment


def serve(
    host: str = typer.Option("0.0.0.0", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    reload: bool = typer.Option(True, help="Enable auto-reload"),
):
    """Start the development server with uvicorn."""
    typer.secho(f"Starting server on {host}:{port}...", fg=typer.colors.BLUE)

    cmd = [
        "uvicorn",
        "app:create_app",
        "--factory",
        "--host",
        host,
        "--port",
        str(port),
    ]

    if reload:
        cmd.append("--reload")

    try:
        result = run_with_project_environment(cmd, capture_output=False)
        if result.returncode != 0:
            typer.secho("✗ Failed to start server", fg=typer.colors.RED)
            raise typer.Exit(result.returncode)
    except KeyboardInterrupt:
        typer.secho("\n✓ Server stopped", fg=typer.colors.GREEN)
    except FileNotFoundError:
        typer.secho("✗ uv not found. Make sure it's installed.", fg=typer.colors.RED)
        raise typer.Exit(1)
    except RuntimeError as e:
        typer.secho(f"✗ {e}", fg=typer.colors.RED)
        raise typer.Exit(1)
