import asyncio

import sqlalchemy as sa
from sqlalchemy import select
from uvloop import loop

from app.infrastructure.persistences.mysql.database import SQLAlchemyWithAioMySql, Database, DatabaseSQLAlchemy


async def test_database():
    database = Database(
        host="localhost",
        user="root",
        password="123456",
        port=3307,
        database="feature", )

    await database.connect()

    async with database.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("show tables;")
            result = await cursor.fetchall()
            print(result)


async def test_database_sa():
    metadata = sa.MetaData()

    tbl = sa.Table(
        "test",
        metadata,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100)),
    )

    database = SQLAlchemyWithAioMySql(
        host="localhost",
        user="root",
        password="123456",
        port=3307,
        database="feature", )

    await database.create_engine()

    async with database.engine.acquire() as conn:
        async with conn.begin() as cursor:
            # await cursor.execute("SELECT 42;")
            result = await conn.execute(tbl.select())
            async for res in result:
                print(res)


async def test_database_sa_2():
    metadata = sa.MetaData()

    tbl = sa.Table(
        "codes",
        metadata,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("abbrev", sa.String(100)),
    )

    database = DatabaseSQLAlchemy(
        host="localhost",
        user="test",
        password="test",
        port=3307,
        database="metrics_platform", )

    await database.connect()

    async with database.engine.connect() as conn:
        await conn.execute(tbl.select())
        result = await conn.execute(tbl.select().filter(tbl.c.id >= 1))
        for res in result:
            print(res.id, res.abbrev)

    async with database.SessionLocal() as session:
        async with session.begin():
            result = await session.execute(tbl.select())
            for res in result:
                print(res.id, res.abbrev)

async def test_database_sa_3():
    from app.domain.models.codes import Codes
    database = DatabaseSQLAlchemy(
        host="localhost",
        user="test",
        password="test",
        port=3307,
        database="metrics_platform", )

    await database.connect()

    async with database.SessionLocal() as session:
        async with session.begin():
            q = select(Codes).filter(Codes.id >= 3)
            # result = await session.execute(Codes.__table__.select())
            result = await session.execute(q)
            for res in result:
                print(res)
                print(res[0].__repr__())

# asyncio.run(test_database_sa())

asyncio.run(test_database_sa_3())

