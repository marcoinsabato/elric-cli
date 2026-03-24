import typer

from elric_cli.commands import apikey, make, migrate, route, serve

app = typer.Typer(
    name="elric",
    help="Elric Framework CLI - AI-first FastAPI framework",
    add_completion=False,
)

# Register command groups
app.add_typer(make.app, name="make")
app.add_typer(migrate.app, name="migrate")
app.add_typer(route.app, name="route")
app.add_typer(apikey.app, name="apikey")

# Register standalone commands
app.command()(serve.serve)


if __name__ == "__main__":
    app()
