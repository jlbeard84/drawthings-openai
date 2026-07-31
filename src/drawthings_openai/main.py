from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from drawthings_openai.grpc_client import ImageClient
from drawthings_openai.routes import loras, models
from drawthings_openai.settings import settings


@asynccontextmanager  # type: ignore
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with ImageClient(
        target=settings.server_target,
        is_insecure=settings.insecure_server,
        timeout=settings.server_timeout,
    ) as client:
        app.state.image_client = client
        yield


def create_app() -> FastAPI:
    app = FastAPI(title="DrawThings OpenAI API", version="0.0.1", lifespan=lifespan)

    app.include_router(models.router)
    app.include_router(loras.router)

    return app


app = create_app()
