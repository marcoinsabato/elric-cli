import asyncio

import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy import select

from app.providers.database import AsyncSessionLocal
from app.utils.api_key import create_api_key_record
from database.models.api_key import ApiKey

app = typer.Typer(help="API key management commands")
console = Console()


@app.command("create")
def create_apikey(name: str = typer.Argument(..., help="Name for the API key")):
    """Create a new API key."""
    async def _create():
        async with AsyncSessionLocal() as session:
            api_key_record, key = await create_api_key_record(name, session)
            
            console.print("\n[bold green]✓ API Key created successfully![/bold green]\n")
            console.print(f"[bold]ID:[/bold]         {api_key_record.id}")
            console.print(f"[bold]Name:[/bold]       {api_key_record.name}")
            console.print(f"[bold]Prefix:[/bold]     {api_key_record.prefix}")
            console.print(f"[bold]Created:[/bold]    {api_key_record.created_at}")
            console.print(f"[bold]Active:[/bold]     {api_key_record.is_active}\n")
            console.print(f"[bold yellow]🔑 API Key:[/bold yellow] {key}\n")
            console.print("[bold red]⚠️  IMPORTANT:[/bold red] Save this key securely!")
            console.print("   This is the only time you'll see the full key.\n")
    
    try:
        asyncio.run(_create())
    except Exception as e:
        typer.secho(f"✗ Failed to create API key: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


@app.command("list")
def list_apikeys():
    """List all API keys."""
    async def _list():
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ApiKey).order_by(ApiKey.created_at.desc())
            )
            api_keys = result.scalars().all()
            
            if not api_keys:
                console.print("[yellow]No API keys found.[/yellow]")
                return
            
            table = Table(title="API Keys")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Prefix", style="yellow")
            table.add_column("Active", style="magenta")
            table.add_column("Created", style="blue")
            table.add_column("Last Used", style="white")
            
            for key in api_keys:
                table.add_row(
                    str(key.id)[:8] + "...",
                    key.name,
                    key.prefix,
                    "✓" if key.is_active else "✗",
                    key.created_at.strftime("%Y-%m-%d %H:%M"),
                    key.last_used_at.strftime("%Y-%m-%d %H:%M") if key.last_used_at else "-",
                )
            
            console.print(table)
            console.print(f"\n[bold]Total API keys:[/bold] {len(api_keys)}")
    
    try:
        asyncio.run(_list())
    except Exception as e:
        typer.secho(f"✗ Failed to list API keys: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


@app.command("revoke")
def revoke_apikey(key_id: str = typer.Argument(..., help="API key ID to revoke")):
    """Revoke an API key by ID."""
    async def _revoke():
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ApiKey).where(ApiKey.id == key_id)
            )
            api_key = result.scalar_one_or_none()
            
            if not api_key:
                console.print(f"[red]✗ API key not found: {key_id}[/red]")
                raise typer.Exit(1)
            
            api_key.is_active = False
            session.add(api_key)
            await session.commit()
            
            console.print(f"[green]✓ API key revoked: {api_key.name}[/green]")
    
    try:
        asyncio.run(_revoke())
    except typer.Exit:
        raise
    except Exception as e:
        typer.secho(f"✗ Failed to revoke API key: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)
