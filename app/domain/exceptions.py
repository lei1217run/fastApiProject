"""
     在领域模型定义几种异常，通过应用层将对应的异常抛出去
    【输入适配器】只需要捕获到相关的领域模型异常即可

    1. 定义领域异常基类 DomainException, 同时定义错误类型模板和消息模板

"""
from typing import ParamSpec

p = ParamSpec('p')


class DomainException(Exception):
    TYPE = "domain_internal_server_error"
    MESSAGE = "Domain_Internal_Server_Error"

    def __init__(self, message: str | None = None, **kwargs: p.kwargs):
        self._message: str = message
        self._kwargs: dict = kwargs
        super().__init__(message)

    """
        定义一个message属性，可以返回传入的message
        或者通过关键字来自定义格式化生成message
    """

    @property
    def message(self) -> str:
        return self._message or self.MESSAGE.format(**self._kwargs)

    def __str__(self):
        return self.message


class ValidateFieldValue(DomainException):
    TYPE = "invalid_field_value"
    MESSAGE = "Invalid value {field_value} for field {field_name}"


class UserNotFound(DomainException):
    TYPE = "user_not_found"
    MESSAGE = "User {user_id} Not Found"


class PostNotFound(DomainException):
    TYPE = "post_not_found"
    MESSAGE = "Post {post_id} Not Found"


class Forbidden(DomainException):
    TYPE = "forbidden"
    MESSAGE = "You are not allowed to perform this action"

