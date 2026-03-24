import subprocess

import typer

from elric_cli.utils import get_project_root


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
        "--host", host,
        "--port", str(port),
    ]
    
    if reload:
        cmd.append("--reload")
    
    try:
        subprocess.run(cmd, cwd=get_project_root())
    except KeyboardInterrupt:
        typer.secho("\n✓ Server stopped", fg=typer.colors.GREEN)
    except FileNotFoundError:
        typer.secho("✗ Uvicorn not found. Make sure it's installed.", fg=typer.colors.RED)
        raise typer.Exit(1)
