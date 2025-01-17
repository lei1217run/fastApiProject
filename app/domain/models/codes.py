from sqlalchemy import Column, Integer, String, DateTime

from app.domain.models.base import BaseEntity


class Codes(BaseEntity):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True)
    code_type = Column(String(100))
    abbrev = Column(String(100))
    code_value = Column(String(100))
    code_name = Column(String(100))
    parent_code_value = Column(String(100))
    status = Column(Integer)
    is_modifier = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    description = Column(String(100))

    def __repr__(self):
        return (f"Codes(id={self.id},code_type={self.code_type}, "
                f"abbrev={self.abbrev}, "
                f"code_value={self.code_value}, "
                f"code_name={self.code_name}, "
                f"parent_code_value={self.parent_code_value}, "
                f"status={self.status}, "
                f"is_modifier={self.is_modifier}, "
                f"created_at={self.created_at}, "
                f"updated_at={self.updated_at}, "
                f"created_by={self.created_by}, "
                f"updated_by={self.updated_by}, "
                f"description={self.description})")
