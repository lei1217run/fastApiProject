import random
from dataclasses import dataclass, field
from datetime import datetime

__all__ = ("database", "Database")


@dataclass
class Database:
    posts: dict = field(default_factory=dict)
    users: dict = field(default_factory=dict)

    def __post_init__(self):
        self.users = {
            user_id: {
                "user_id": user_id,
                "email": f"user_{user_id}@example.com",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
            for user_id in range(1, 4)
        }

        self.posts = {
            post_id: {
                "post_id": post_id,
                "title": f"FastAPI tutorial post_{post_id}",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "user_id": random.choice(list(self.users.keys()))
            }
            for post_id in range(1, 6)
        }


database = Database()
