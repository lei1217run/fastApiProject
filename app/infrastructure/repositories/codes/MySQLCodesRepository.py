from sqlalchemy import select

from app.domain.models.codes import Codes
from app.domain.repositories import CodesRepository

from app.infrastructure.persistences.mysql.database import DatabaseSQLAlchemy
from app.infrastructure.utils.decorators import injectable


@injectable(name="CodesRepository", override_target="codes_repository")
class MySQLCodesRepository(CodesRepository):
    def __init__(self, database: DatabaseSQLAlchemy):
        self.SessionLocal = database.SessionLocal

    async def create(self, post: Codes) -> Codes:
        pass

    async def get_code_by_id(self, code_id: int) -> Codes:
        pass

    async def delete(self, post_id: int) -> None:
        pass

    async def get_codes_by_abbreviation(self, abbreviation: str) -> list[Codes]:
        pass

    async def update(self, post: Codes) -> Codes:
        pass

    async def get_codes(self, offset=0, limit=10) -> list[Codes]:
        async with self.SessionLocal() as session:
            async with session.begin():
                q = select(Codes).filter(Codes.id >= 0).offset(offset).limit(limit)
                codes = await session.execute(q)
            return codes.scalars().all()


