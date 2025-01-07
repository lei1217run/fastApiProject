"""
    输出型适配器： 使用内存的的User仓库适配器

    注入数据库客户端，之前写好的Database对象
"""
from app.domain.models.user import User
from app.domain.repositories import UserRepository
from app.infrastructure.persistences.memory_db.database import Database


class MemoryUserRepository(UserRepository):
    def __init__(self, database: Database):
        self._database = database

    async def get_by_id(self, user_id: int) -> User | None:
        if not (user_data := self._database.users.get(user_id)):
            return None
        return self._build_user_model(user_data)

    @staticmethod
    def _build_user_model(user_data: dict) -> User:
        return User(
            user_id=user_data.get('user_id'),
            email=user_data.get('email'),
            created_at=user_data.get('created_at'),
            updated_at=user_data.get('updated_at'),
        )
