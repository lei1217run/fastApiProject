import asyncio

from app.infrastructure.persistences.mysql.database import DataBaseSQLAlchemy


async def test_database():
    database = DataBaseSQLAlchemy(
        host="localhost",
        user="root",
        password="123456",
        port=3307,
        database="feature",)

    async with database.engine.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT 42;")
            result = await cursor.fetchone()
            assert result == (42,)

asyncio.run(test_database())