from app.application.dic import DIC
from app.application.post_service import PostService
from app.config.config import config
from app.infrastructure.persistences.memory_db.database import database
from app.infrastructure.persistences.mysql.database import Database
from app.infrastructure.repositories import MemoryUserRepository, MySQLPostRepository

"""
    应用的生命周期函数
"""


async def application_startup():
    # 引入配置文件
    mysql_config = config["database"]["mysql"]
    mysql_database = Database(
        host=mysql_config["host"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["dbname"],
    )
    # 初始化连接池
    await mysql_database.connect()

    # 实例化输出型适配器
    user_repository = MemoryUserRepository(database=database)
    post_repository = MySQLPostRepository(database=mysql_database)
    # post_repository = MemoryPostRepository(database=database)

    DIC.post_service = PostService(
        user_repository=user_repository,
        post_repository=post_repository)

    DIC.mysql_database = mysql_database


async def application_shutdown():
    if DIC.mysql_database:
        await DIC.mysql_database.close_connection()


async def application_health_check():
    await DIC.mysql_database.check_connection()
