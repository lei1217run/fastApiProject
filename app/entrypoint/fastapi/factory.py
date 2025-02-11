from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI


from app.application import application_startup, application_shutdown
from app.config.config import config

from app.entrypoint.fastapi.exceptions import setup_exception_handler
from app.entrypoint.fastapi.middleware.LoggingMiddleware import LoggingMiddleware
from app.infrastructure.logging.LoguruLogger import LoggerManager

"""

"""

def create_app() -> FastAPI:

    entry_logger = LoggerManager(name="entrypoint", log_config=config)

    #  生命周期钩子函数
    async def app_startup(application: FastAPI) -> None:
        application.state.logger.log(message="App starting up.")
        await application_startup()
        from app.application import DIC
        application.container = DIC
        # 在加载路由之前绑定依赖注入容器到模块
        # import app.entrypoint.fastapi.routers.codes

        # Todo: 此处有深坑, 需要深入阅读wire的源码 print(application.container.declarative_parent)
        application.container.declarative_parent = None # 显示注释掉基类，因子容器的provides.keys() 多于Appcontainer这个基类
        # Todo: 此处绑定的package是可以优化到配置文件中的
        application.container.wire(packages=["app.entrypoint.fastapi.routers",], )

        # Delay the import of routers module until after DIC is initialized
        print(f"application.container initialized: {application.container}, and starting routers",  )
        from app.entrypoint.fastapi import routers
        for route in routers.routers:
            application.include_router(route)

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

    # 异常装饰器
    setup_exception_handler(app)

    # 添加全局日志中间件
    app.add_middleware(LoggingMiddleware, logger_manager=entry_logger)

    return app
