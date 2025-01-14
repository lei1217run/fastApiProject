# app/infrastructure/logging/logger_interface.py

from abc import ABC, abstractmethod


class BaseLogger(ABC):
    @abstractmethod
    def log(self, message: str, level: str = "INFO", **kwargs):
        """通用日志记录方法"""
        pass

    @abstractmethod
    def is_detail_enabled(self) -> bool: ...

    @abstractmethod
    def bind_context(self, **kwargs): ...

    @abstractmethod
    def clear_context(self): ...


