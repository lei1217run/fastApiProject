from app.domain.repositories import CodesRepository
from app.infrastructure.utils.decorators import injectable


@injectable(name="CodesService", override_target="codes_service")
class CodesService:
    def __init__(self, codes_repository: CodesRepository):
        self.codes_repository = codes_repository

    async def get_codes(self, offset: int, limit: int):
        return await self.codes_repository.get_codes(offset, limit)

