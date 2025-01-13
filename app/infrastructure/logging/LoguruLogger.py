import sys
import uuid

from loguru import logger

from app.infrastructure.logging.base_logger import BaseLogger

# 全局配置 loguru 的 logger
logger.remove()
logger.add(
    sys.stdout,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        " | <magenta>[{extra[logger_name]}]</magenta> | <yellow>[{extra[request_id]}]</yellow>"
    ),
    enqueue=True,
)


class LoggerManager(BaseLogger):
    def __init__(self, name: str = "default"):
        """
        初始化 LoggerManager，并绑定 loguru 的 logger 实例到当前对象。

        Args:
            name: 日志名称，用于标识不同的 logger 实例。
        """
        self.name = name
        self.logger = logger.bind(logger_name=name, request_id=None)

    def get_logger(self):
        """返回绑定到实例的 logger"""
        return self.logger

    def bind_context(self, **kwargs):
        """
        动态绑定上下文信息。

        Args:
            kwargs: 要绑定的上下文信息。
        """
        self.logger = self.logger.bind(**kwargs)

    def log(self, message: str, level: str = "INFO", **kwargs):
        """
        通用日志记录方法，支持动态指定日志级别。

        Args:
            message: 日志信息。
            level: 日志级别（默认是 INFO）。
            kwargs: 额外的上下文参数。
        """
        level = level.upper()
        if level not in {"INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"}:
            raise ValueError(f"Invalid log level: {level}")
        log_func = getattr(self.logger, level.lower(), self.logger.info)
        log_func(message, **kwargs)

    def clear_context(self):
        """清除上下文信息"""
        self.logger = self.logger.bind()

    def domain_log(self, message: str, level: str = "INFO", **kwargs):
        """记录领域层日志"""
        self.log(message, level=level, context="domain", **kwargs)

    def application_log(self, message: str, level: str = "INFO", **kwargs):
        """记录应用层日志"""
        self.log(message, level=level, context="application", **kwargs)

    def infrastructure_log(self, message: str, level: str = "INFO", **kwargs):
        """记录基础设施层日志"""
        self.log(message, level=level, context="infrastructure", **kwargs)


# logger1 = LoggerManager(name="hello")
# logger1.bind_context(request_id=1)
# logger1.log("hello world")

