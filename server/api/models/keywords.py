from typing import Optional

from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from server.api.models.models import Base


class Keywords(Base):
    __tablename__ = 'keywords'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    word: Mapped[Optional[str]] = mapped_column(String(75))
    word_type: Mapped[Optional[str]] = mapped_column(String(20))

    def __str__(self):
        return f"Ключевое слово ({self.word})"
