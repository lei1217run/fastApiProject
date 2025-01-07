"""
    自定义依赖注入容器
    先用dataclass 模拟dic
"""

from dataclasses import dataclass

from app.application.post_service import PostService

__all__ = ("DIC",)


@dataclass(kw_only=True)
class DependencyInjectionContainer:
    post_service: PostService | None = None


DIC = DependencyInjectionContainer()
