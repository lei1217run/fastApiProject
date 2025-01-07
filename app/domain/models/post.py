from dataclasses import dataclass, field
from datetime import datetime

from app.domain.exceptions import ValidateFieldValue
from app.domain.models.base import BaseModel
from app.domain.models.user import User


@dataclass(kw_only=True)
class Post(BaseModel):
    title: str
    post_id: int | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    user: User | None = field(default=None)

    @staticmethod
    def validate_title(value: str) -> str:
        if len(value.strip()) == 0:
            raise ValidateFieldValue(field_name="title", field_value=value)
        return value.strip()


# post = Post(title="test", post_id=1)
# #post.title = ""
#
# post.title ="update title"
#
# assert post.modified_fields == {"title": {"old_value": "test", "new_value": "update title"} }
