from abc import ABC, abstractmethod

from app.domain.models.post import Post
from app.infrastructure.utils.decorators import injectable

"""
    领域层-抽象层
    用于持久化操作领域模型实例的读写操作
"""


@injectable(name="PostRepositoryEntity")
class PostRepository(ABC):

    @abstractmethod
    async def create(self, post: Post) -> Post: ...

    @abstractmethod
    async def get_by_id(self, post_id: int) -> Post: ...

    @abstractmethod
    async def update(self, post: Post) -> Post: ...

    @abstractmethod
    async def delete(self, post_id: int) -> None: ...

    @abstractmethod
    async def get_posts(self) -> list[Post]: ...
