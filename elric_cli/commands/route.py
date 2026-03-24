import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Route management commands")
console = Console()


@app.command("list")
def list_routes():
    """List all registered routes in the FastAPI application."""
    try:
        from app import create_app
        
        app_instance = create_app()
        
        table = Table(title="Registered Routes")
        table.add_column("Method", style="cyan")
        table.add_column("Path", style="green")
        table.add_column("Name", style="yellow")
        
        routes = []
        for route in app_instance.routes:
            if hasattr(route, "methods"):
                for method in route.methods:
                    if method != "HEAD":
                        routes.append({
                            "method": method,
                            "path": route.path,
                            "name": route.name or "-",
                        })
        
        routes.sort(key=lambda x: (x["path"], x["method"]))
        
        for route in routes:
            table.add_row(route["method"], route["path"], route["name"])
        
        console.print(table)
        console.print(f"\n[bold]Total routes:[/bold] {len(routes)}")
        
    except Exception as e:
        typer.secho(f"✗ Failed to list routes: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)
