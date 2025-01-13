import uuid
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
        self.logger_manager.log(
            f"Request started: {request.method} {request.url.path} ",
            level="INFO",
            extra={"request_id": request_id},
        )

        # 调用下一个中间件或视图
        try:
            response = await call_next(request)
        except Exception as exc:
            # 记录异常日志
            self.logger_manager.log(
                f"Request error: {request.method} {request.url.path} - Error: {str(exc)}",
                level="ERROR",
                extra={"request_id": request_id},
            )
            raise

        # 记录请求完成日志
        self.logger_manager.log(
            f"Request completed: {request.method} {request.url.path} - Status: {response.status_code}",
            level="INFO",
            extra={"request_id": request_id},
        )

        # 清除日志上下文，防止污染
        self.logger_manager.clear_context()

        return response
