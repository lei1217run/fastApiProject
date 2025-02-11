from datetime import datetime

from pydantic import BaseModel


class CodeView(BaseModel):
    code_id: int | None = None
    code_type: str | None = None
    abbreviation: str | None = None
    description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_deleted: bool | None = None
    deleted_at: datetime | None = None
    deleted_by: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    version: int | None = None
    status: int | None = None
    status_name: str | None = None
    status_description: str | None = None