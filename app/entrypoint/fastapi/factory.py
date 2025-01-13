from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI


from app.application import application_startup, application_shutdown
from app.config.config import config
from app.entrypoint.fastapi import routers
from app.entrypoint.fastapi.exceptions import setup_exception_handler
from app.entrypoint.fastapi.middleware.LoggingMiddleware import LoggingMiddleware
from app.infrastructure.logging.LoguruLogger import LoggerManager


def create_app() -> FastAPI:

    entry_logger = LoggerManager(name="entrypoint")

    #  生命周期钩子函数
    async def app_startup(application: FastAPI) -> None:
        application.state.logger.log(message="App starting up.")
        await application_startup()

    async def app_shutdown(application: FastAPI) -> None:
        application.state.logger.log(message="App shutting down.")
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

    app.state.logger = entry_logger

    for route in routers.routers:
        app.include_router(route)

    # 异常装饰器
    setup_exception_handler(app)

    # 添加全局日志中间件
    app.add_middleware(LoggingMiddleware, logger_manager=entry_logger)

    return app
