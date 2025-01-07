import re
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.exceptions import ValidateFieldValue
from app.domain.models.base import BaseModel

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$")


@dataclass(kw_only=True)
class User(BaseModel):
    user_id: int
    email: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @staticmethod
    def validate_email(email: str | None) -> str | None:
        if email is not None and not re.match(EMAIL_REGEX, email):
            raise ValidateFieldValue(field_name="email", field_value=email)
        return email
