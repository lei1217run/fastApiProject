from app.domain.models.post import Post
from app.domain.models.user import User
from app.domain.repositories import PostRepository
from app.infrastructure.persistences.memory_db.database import Database


class MemoryPostRepository(PostRepository):
    def __init__(self, database: Database) -> None:
        self._database = database

    async def create(self, post: Post) -> Post:
        post_data = self._serialize(post)
        self._database.posts[post_data['post_id']] = post_data
        post.post_id = post_data['post_id']
        return post

    async def get_by_id(self, post_id: int) -> Post | None:
        if not (post := self._database.posts.get(post_id)):
            return None
        return self._build_post_model(post)

    async def update(self, post: Post) -> Post:
        if not post.modified_fields:
            return post
        self._database.posts[post.post_id].update(self._serialize(post, True))
        return post

    async def delete(self, post_id: int) -> None:
        try:
            self._database.posts.pop(post_id)
        except KeyError:
            return None

    async def get_posts(self) -> list[Post]:
        return [self._build_post_model(post) for post in self._database.posts.values()]

    # 序列化
    # partial 只返回更新的信息
    def _serialize(self, post: Post, partial: bool = False) -> dict:
        if not partial:
            return {
                "post_id": post.post_id or self._generate_id(),
                "title": post.title,
                "created_at": post.created_at,
                "updated_at": post.updated_at,
                "user_id": post.user.user_id,
            }
        else:
            data = {}
            modified_data = post.modified_fields
            for field in modified_data:
                match field:
                    case 'title':
                        data[field] = post.title
                    case _:
                        pass
            return data

    def _generate_id(self) -> int:
        return len(self._database.posts) + 1

    # 反序列化
    @staticmethod
    def _build_post_model(post: dict) -> Post:
        return Post(
            title=post['title'],
            post_id=post['post_id'],
            created_at=post['created_at'],
            updated_at=post['updated_at'],
            user=User(user_id=post['user_id']),
        )
