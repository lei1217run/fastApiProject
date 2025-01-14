import json
import uuid

from starlette.concurrency import iterate_in_threadpool

from app.infrastructure.logging.base_logger import BaseLogger
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    自定义日志中间件，用于记录每个请求的生命周期日志。
    """

    def __init__(self, app, logger_manager: BaseLogger):
        """
        初始化日志中间件。

        Args:
            app: FastAPI 实例。
            logger_manager: 日志管理器实例。
        """
        super().__init__(app)
        self.logger_manager = logger_manager

    async def dispatch(self, request: Request, call_next):
        """
        拦截请求，记录请求开始和完成日志。

        Args:
            request: 请求对象。
            call_next: 调用下一个中间件或视图的回调。

        Returns:
            Response: 响应对象。
        """
        # 生成唯一的请求 ID
        request_id = str(uuid.uuid4())
        self.logger_manager.bind_context(request_id=request_id)

        # 记录请求开始日志
        log_data = {
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host,
            # 获取路径参数
            "path_params": dict(request.path_params),  # 路径参数
            # 获取查询参数
            "query_params": dict(request.query_params)  # 查询参数
        }

        # 如果开启了详细模式，记录请求入参
        if self.logger_manager.is_detail_enabled():
            try:
                body = await request.json()
            except Exception as exc:
                try:
                    body = await request.form()
                except Exception as exc1:
                    body = await request.body()
            body = body.decode('utf-8') if body else "Unable to parse request body"
            log_data["request_body"] = body
        # 记录请求开始日志
        self.logger_manager.log(
            message=f"Request started: {log_data}",
            level="INFO",
        )

        # 调用下一个中间件或视图
        try:
            response: Response = await call_next(request)
        except Exception as exc:
            # 记录异常日志
            self.logger_manager.log(
                message=f"Request error: {request.method} {request.url.path} - Error: {str(exc)}",
                level="ERROR"
            )
            raise

        if self.logger_manager.is_detail_enabled():
            try:
                response_body = [chunk async for chunk in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body))
                print(f"response_body={response_body[0].decode()}")

                # Restore body iterator
                log_data["response_body"] = (
                    response_body[0].decode()
                    if response_body
                    else "Empty response body"
                )
            except Exception as exc:
                log_data["response_body"] = "Unable to parse response body {}".format(str(exc))

        # 记录请求完成日志
        log_data["status_code"] = response.status_code
        self.logger_manager.log(
            message=f"Request completed: {log_data}",
            level="INFO",
        )

        # 清除日志上下文，防止污染
        self.logger_manager.clear_context()

        return response
