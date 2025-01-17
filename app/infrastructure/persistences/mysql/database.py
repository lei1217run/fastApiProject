import aiomysql
from aiomysql.sa import create_engine
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

__all__ = ("Database", "DatabaseSQLAlchemy", "SQLAlchemyWithAioMySql")

from sqlalchemy.orm import sessionmaker

"""
    issues: aiomysql.sa not supported for SQLAlchemy 2.0, so we need to use aiomysql directly, or use SQLAlchemy only
    See~See: https://github.com/aio-libs/aiomysql/issues/818
"""


class Database:
    def __init__(self, host: str, user: str, password: str, database: str, autocommit: bool = True, port: int = 3306,
                 pool_minsize: int = 1, pool_maxsize: int = 10, charset: str = 'utf8mb4', pool_recycle: int = 3600,
                 wait_timeout: int = 30):
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._autocommit = autocommit
        self._port = port
        self._pool_minsize = pool_minsize
        self._pool_maxsize = pool_maxsize
        self._charset = charset
        self._wait_timeout = wait_timeout
        self._pool_recycle = pool_recycle
        self.pool = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self._host,
            user=self._user,
            password=self._password,
            db=self._database,
            autocommit=self._autocommit,
            port=self._port,
            charset=self._charset,
            minsize=self._pool_minsize,
            maxsize=self._pool_maxsize,
            cursorclass=aiomysql.cursors.DictCursor,
            connect_timeout=1,
            pool_recycle=self._pool_recycle,
            init_command=f"SET wait_timeout = {self._wait_timeout}",
        )

    async def check_connection(self):
        async with self.pool.acquire() as conn:
            await conn.ping(reconnect=True)

    async def init_connection(self):
        try:
            await self.connect()
            await self.check_connection()
        except Exception as e:
            raise e

    async def close_connection(self):
        if self.pool:
            self.pool.terminate()
            await self.pool.wait_closed()
            self.pool = None


class DatabaseSQLAlchemy:
    def __init__(self, host: str, user: str, password: str, database: str,
                 autocommit: bool = True, port: int = 3307,
                 pool_size: int = 10, pool_recycle: int = 3600,
                 wait_timeout: int = 30, charset: str = 'utf8mb4', echo: bool = False):
        self._charset = charset
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._autocommit = autocommit
        self._port = port
        self._pool_size = pool_size
        self._pool_recycle = pool_recycle
        self._wait_timeout = wait_timeout
        self._echo = echo
        self.engine = None
        self.SessionLocal = None

    def create_engine_url(self):
        # return f"mysql+aiomysql://{self._user}:{self._password}@{self._host}:{self._port}/{self._database}"
        return f"mysql+asyncmy://{self._user}:{self._password}@{self._host}:{self._port}/{self._database}?charset={self._charset}"

    async def connect(self):
        self.engine = create_async_engine(
            self.create_engine_url(),
            echo=self._echo,
            pool_size=self._pool_size,
            pool_recycle=self._pool_recycle,
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def check_connection(self):
        async with self.engine.connect() as conn:
            await conn.execute("SELECT 1")

    async def init_connection(self):
        try:
            await self.connect()
            await self.check_connection()
        except Exception as e:
            raise e

    async def close_connection(self):
        if self.engine:
            await self.engine.dispose()


class SQLAlchemyWithAioMySql:
    # not used
    def __init__(self, host: str, user: str, password: str, database: str, autocommit: bool = True, port: int = 3306,
                 pool_minsize: int = 1, pool_maxsize: int = 10, charset: str = 'utf8mb4', pool_recycle: int = 3600,
                 wait_timeout: int = 30):
        self.engine = None
        self._host = host
        self._user = user
        self._password = password
        self._database = database
        self._autocommit = autocommit
        self._port = port
        self._pool_minsize = pool_minsize
        self._pool_maxsize = pool_maxsize
        self._charset = charset
        self._wait_timeout = wait_timeout
        self._pool_recycle = pool_recycle

    async def create_engine(self):
        self.engine = await create_engine(
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            db=self._database,
            autocommit=self._autocommit,
            minsize=self._pool_minsize,
            maxsize=self._pool_maxsize,
            pool_recycle=self._pool_recycle,
            init_command=f"SET wait_timeout = {self._wait_timeout}",
            echo=True,
        )
