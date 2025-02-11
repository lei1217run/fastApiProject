from abc import ABC, abstractmethod

from app.domain.models.codes import Codes


class CodesRepository(ABC):

    @abstractmethod
    async def create(self, post: Codes) -> Codes: ...

    @abstractmethod
    async def get_code_by_id(self, code_id: int) -> Codes: ...

    @abstractmethod
    async def update(self, post: Codes) -> Codes: ...

    @abstractmethod
    async def delete(self, post_id: int) -> None: ...

    @abstractmethod
    async def get_codes(self, offset: int, limit: int) -> list[Codes]: ...

    @abstractmethod
    async def get_codes_by_abbreviation(self, abbreviation: str) -> list[Codes]: ...