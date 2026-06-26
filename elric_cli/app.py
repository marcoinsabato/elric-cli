import typer

from elric_cli.commands import apikey, db, make, migrate, route, serve
from elric_cli.commands.quality import format_code, lint
from elric_cli.commands.project import new_project

app = typer.Typer(
    name="elric",
    help="Elric CLI - bootstrap and manage Elric projects",
    add_completion=False,
)

# Register command groups
app.add_typer(make.app, name="make")
app.add_typer(migrate.app, name="migrate")
app.add_typer(db.app, name="db")
app.add_typer(route.app, name="route")
app.add_typer(apikey.app, name="apikey")

# Register standalone commands
app.command()(serve.serve)
app.command("new")(new_project)
app.command("lint")(lint)
app.command("format")(format_code)


if __name__ == "__main__":
    app()
