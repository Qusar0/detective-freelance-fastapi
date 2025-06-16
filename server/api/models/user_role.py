from typing import List

from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base


class UserRole(Base):
    __tablename__ = 'user_role'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    role_name: Mapped[str] = mapped_column(String(50))

    users: Mapped[List['Users']] = relationship(
        'Users',
        back_populates='user_role',
    )

    def __str__(self):
        return f"{self.role_name}"
