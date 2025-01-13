from typing import Type
from fastapi import status, FastAPI
from fastapi.responses import ORJSONResponse

from app.domain import exceptions as exceptions_domain

# 1. 引入领域异常基础类型
DomainExceptionType = Type[exceptions_domain.DomainException]

# 2. 定义一个领域异常的字典映射异常状态码
EXCEPTION_STATUS_MAPPING: dict[DomainExceptionType, int] = {
    exceptions_domain.PostNotFound: status.HTTP_404_NOT_FOUND,
    exceptions_domain.UserNotFound: status.HTTP_404_NOT_FOUND,
    exceptions_domain.ValidateFieldValue: status.HTTP_400_BAD_REQUEST,
    exceptions_domain.Forbidden: status.HTTP_403_FORBIDDEN,
}


# 3. 利用装饰器来集中处理异常
def setup_exception_handler(app: FastAPI) -> None:
    # 捕获自定义的领域内异常
    # Todo: 异常日志应该写入日志文件
    @app.exception_handler(exceptions_domain.DomainException)
    def domain_exception_handler(_, exc: exceptions_domain.DomainException) -> ORJSONResponse:
        return ORJSONResponse(
            content={"error": exc.message, "type": exc.TYPE},
            status_code=EXCEPTION_STATUS_MAPPING.get(exc.TYPE, status.HTTP_500_INTERNAL_SERVER_ERROR),
        )

    @app.exception_handler(Exception)
    def exception_handler(_, exc: Exception) -> ORJSONResponse:
        return ORJSONResponse(
            content={"error": str(exc), "type": "internal_type_error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
