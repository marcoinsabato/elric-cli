from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.providers.database import init_db
from app.providers.langsmith import init_langsmith
from app.providers.redis import close_redis, init_redis
from app.routes import health
from config.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_redis()
    init_langsmith()
    yield
    await close_redis()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Elric App",
        lifespan=lifespan,
        docs_url="/docs" if settings.APP_DEBUG else None,
    )

    app.include_router(health.router)

    return app
