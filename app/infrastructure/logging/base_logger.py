# app/infrastructure/logging/logger_interface.py

from abc import ABC, abstractmethod


class BaseLogger(ABC):
    @abstractmethod
    def log(self, message: str, level: str = "INFO", **kwargs):
        """通用日志记录方法"""
        pass

    @abstractmethod
    def domain_log(self, message: str, level: str = "INFO", **kwargs):
        """记录领域层日志"""
        pass

    @abstractmethod
    def application_log(self, message: str, level: str = "INFO", **kwargs):
        """记录应用层日志"""
        pass

    @abstractmethod
    def infrastructure_log(self, message: str, level: str = "INFO", **kwargs):
        """记录基础设施层日志"""
        pass

    @abstractmethod
    def bind_context(self, **kwargs): ...

    @abstractmethod
    def clear_context(self): ...


