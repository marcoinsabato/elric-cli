from app.providers.database import AsyncSessionLocal


async def run() -> None:
    """Seed {{ snake_name }} data."""
    async with AsyncSessionLocal() as session:
        # TODO: add {{ snake_name }} seed records
        await session.commit()
