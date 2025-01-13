from app.domain.models.post import Post
from app.domain.models.user import User
from app.domain.repositories import PostRepository
from app.infrastructure.persistences.mysql.database import Database


class MySQLPostRepository(PostRepository):
    def __init__(self, database: Database) -> None:
        self.connection_pool = database.pool

    async def create(self, post: Post) -> Post:
        async with self.connection_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    query="INSERT INTO posts (title, post_id, user_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
                    args=(post.title,
                          post.post_id,
                          post.user.user_id,
                          post.created_at,
                          post.updated_at),
                )
                post.post_id = cursor.lastrowid
        return post

    async def get_by_id(self, post_id: int) -> Post | None:
        async with self.connection_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    query="SELECT post_id, user_id, title, created_at,updated_at FROM posts WHERE post_id = %s",
                    args=(post_id,)
                )
                post_data = await cursor.fetchone()
        return self._build_post_model(post_data) if post_data else None

    async def update(self, post: Post) -> Post:
        if not (modified_fields := self._serialize(post=post, partial=True)):
            return post

        async with self.connection_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    query=f"UPDATE posts SET {','.join([f'`{key}` = %s' for key in modified_fields.keys()])} where post_id = %s",
                    args=tuple(modified_fields.values()) + (post.post_id,),
                )
        return post

    async def delete(self, post_id: int) -> None:
        try:
            async with self.connection_pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(
                        query=f"DELETE FROM posts WHERE post_id = %s",
                        args=(post_id,)
                    )
        except KeyError:
            return None

    async def get_posts(self) -> list[Post]:
        async with self.connection_pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    query="SELECT post_id, user_id, title, created_at,updated_at FROM posts"
                )
                posts_data = await cursor.fetchall()
        return [self._build_post_model(post) for post in posts_data]

    # 序列化
    # partial 只返回更新的信息
    @staticmethod
    def _serialize(post: Post, partial: bool = False) -> dict:
        if not partial:
            return {
                "post_id": post.post_id,
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
