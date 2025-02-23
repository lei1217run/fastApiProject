
from app.application.container import AppContainer, register_injectables
from app.application.post_service import PostService
from app.config.config import config
from app.infrastructure.persistences.memory_db.database import database
from app.infrastructure.persistences.mysql.database import Database
from app.infrastructure.repositories import MemoryUserRepository, MySQLPostRepository, LoggerManager

from app.application.dic import DIC

"""
    应用的生命周期函数
"""

async def application_startup():
    print("Starting application startup")
    # Load and register injectables
    global DIC  # type: AppContainer
    DIC = AppContainer()
    DIC.config.update(config.as_dict())
    # Initialize the database connection
    mysql_database = DIC.database_signal()
    await mysql_database.connect()

    data_base = DIC.database()
    await data_base.connect()

    register_injectables(DIC)
    print(f"DIC initialized: {DIC}, in application_startup")

async def application_startup_old():
    # 引入配置文件
    mysql_config = config["database"]["mysql"]
    mysql_database = Database(
        host=mysql_config["host"],
        user=mysql_config["user"],
        password=mysql_config["password"],
        database=mysql_config["dbname"],
        port=mysql_config["port"],
    )
    # 初始化连接池
    await mysql_database.connect()

    # 实例化输出型适配器
    user_repository = MemoryUserRepository(database=database)
    post_repository = MySQLPostRepository(database=mysql_database)
    # post_repository = MemoryPostRepository(database=database)

    DIC.logger_manager = LoggerManager(name="application")

    DIC.post_service = PostService(
        user_repository=user_repository,
        post_repository=post_repository, )

    DIC.mysql_database = mysql_database


async def application_shutdown():
    # if DIC.mysql_database:
    #     await DIC.mysql_database.close_connection()
    if DIC.database_signal:
        await DIC.database_signal().close_connection()
    if DIC.database:
        await DIC.database().close_connection()


async def application_health_check():
    # await DIC.mysql_database.check_connection()
    await DIC.database_signal().check_connection()