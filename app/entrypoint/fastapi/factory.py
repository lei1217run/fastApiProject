from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.application import application_startup, application_shutdown
from app.config.config import config
from app.entrypoint.fastapi import routers


def create_app() -> FastAPI:
    #  生命周期钩子函数
    async def app_startup(application: FastAPI) -> None:
        print("App starting up.")
        await application_startup()

    async def app_shutdown(application: FastAPI) -> None:
        print("App shutting down.")
        await application_shutdown()

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        await app_startup(application)
        yield
        await app_shutdown(application)

    # application init
    app: FastAPI = FastAPI(
        title=config.app.title,
        version=config.app.version,
        description=config.app.description,
        lifespan=lifespan,
    )

    for route in routers.routers:
        app.include_router(route)
    return app
