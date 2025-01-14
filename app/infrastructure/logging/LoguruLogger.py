import json
import sys

from dynaconf import Dynaconf
from loguru import logger

from app.infrastructure.logging.base_logger import BaseLogger
from app.config.config import config


# 屏蔽 uvicorn 日志
def intercept_uvicorn_logs():
    import logging
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = []
    uvicorn_logger.propagate = False


class LoggerManager(BaseLogger):
    def __init__(self, name: str = "default", log_config: Dynaconf = None):
        """
        初始化 LoggerManager，并绑定 loguru 的 logger 实例到当前对象。

        Args:
            name: 日志名称，用于标识不同的 logger 实例。
            log_config: 配置信息。
        """
        self.log_file = None
        self.name = name
        self.is_detail_model: bool | None = False
        self.enable_file_logging: bool | None = True
        self.file_log_level: str | None = "INFO"
        if log_config:
            self.init_config(log_config)
        self.logger = logger.bind(logger_name=name, request_id=None)
        self.setup_loguru()

    def init_config(self, log_config: Dynaconf):
        """
        初始化配置信息。

        Args:
            log_config: 配置信息。
        """
        assert log_config.app.log is not None, "log_config must be provided."
        self.log_file = log_config.app.log.file_name if (
            log_config.app.log.file_name) else None
        self.is_detail_model = log_config.app.log.detailed_mode if (
            log_config.app.log.detailed_mode) else False
        self.enable_file_logging = log_config.app.log.enable_file_logging if (
            log_config.app.log.enable_file_logging) else False
        self.file_log_level = log_config.app.log.level if (
            log_config.app.log.level) else "INFO"

    def is_detail_enabled(self):
        return self.is_detail_model

    def setup_loguru(self):
        logger.remove()

        self.logger.add(
            sys.stdout,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | "
                "<cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
                " | <magenta>[{extra[logger_name]}]</magenta> | <yellow>[{extra[request_id]}]</yellow>"
            ),
            enqueue=True,
        )
        if self.enable_file_logging and self.log_file is not None:
            self.logger.add(
                self.log_file,
                format=(
                    "{time:YYYY-MM-DD HH:mm:ss} | "
                    "<level>{level}</level> | "
                    "Process-{process.name}:Thread-{thread.name}:{line} - {message}"
                    " | [{extra[logger_name]}] | [{extra[request_id]}]"
                ),
                level=self.file_log_level.upper(),
                enqueue=True,
            )

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

        # 处理字典类型的消息，将其转为 JSON 字符串
        if isinstance(message, dict):
            try:
                message = json.dumps(message, ensure_ascii=False)
            except Exception as exc:
                message = f"Failed to serialize message: {str(exc)}"

        log_func = getattr(self.logger, level.lower(), self.logger.info)
        log_func(message, **kwargs)

    def clear_context(self):
        """清除上下文信息"""
        self.logger = self.logger.bind()

    def domain_log(self, message: str, level: str = "INFO", **kwargs):
        """记录领域层日志"""
        self.log(message, level=level, context="domain", **kwargs)


intercept_uvicorn_logs()

# logger1 = LoggerManager(name="hello")
# logger1.bind_context(request_id=1)
# logger1.log("hello world")
