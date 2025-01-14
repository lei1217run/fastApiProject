from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from starlette.concurrency import iterate_in_threadpool
from starlette.requests import Request
from starlette.responses import Response

from normal.config.config import config
from normal import routers


def create_app() -> FastAPI:
    #  生命周期钩子函数
    async def app_startup(application: FastAPI) -> None:
        print("App starting up.")

    async def app_shutdown(application: FastAPI) -> None:
        print("App shutting down.")

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

    @app.middleware("http")
    async def log_request(request: Request, call_next):
        print(f"Request started: {request.method} {request.url.path}")
        # 获取路径参数
        path_params = dict(request.path_params)  # 路径参数
        # 获取查询参数
        query_params = dict(request.query_params)  # 查询参数
        print(f"Path params: {path_params}")
        print(f"Query params: {query_params}")
        body = None
        try:
            body = await request.json()
        except Exception:
            try:
                body = await request.form()
            except Exception:
                body = await request.body()
                body = body.decode('utf-8') if body else "Unable to parse request body"

        print(f"Request body: {body}")
        response: Response = await call_next(request)
        print(dir(response))
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        print(f"response_body={response_body[0].decode()}")
        return response
    return app
