from app.application.dic import DIC
from app.application.post_service import PostService
from app.infrastructure.persistences.memory_db.database import database
from app.infrastructure.repositories import MemoryUserRepository, MemoryPostRepository

"""
    应用的生命周期函数
"""


async def application_startup():
    # 实例化输出型适配器
    user_repository = MemoryUserRepository(database=database)
    post_repository = MemoryPostRepository(database=database)

    DIC.post_service = PostService(
        user_repository=user_repository,
        post_repository=post_repository)




