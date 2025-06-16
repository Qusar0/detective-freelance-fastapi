from typing import Optional

from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from server.api.models.models import Base


class Blacklist(Base):
    __tablename__ = 'blacklist'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    refresh_token: Mapped[Optional[str]] = mapped_column(String(255))
    