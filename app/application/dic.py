"""
    自定义依赖注入容器
    1. 先用dataclass 模拟dic
    2. 引入依赖注入包之后直接初始值为None
"""

__all__ = ("DIC",)

DIC = None # type: # AppContainer

# @dataclass(kw_only=True)
# class DependencyInjectionContainer:
#     post_service: PostService | None = None
#     mysql_database: Database | None = None
#     logger_manager: BaseLogger | None = None
