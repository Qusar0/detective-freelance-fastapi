from typing import Optional, TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base

if TYPE_CHECKING:
    from server.api.models import UserQueries


class TextData(Base):
    __tablename__ = 'text_data'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    query_id: Mapped[int] = mapped_column(
        ForeignKey('user_queries.query_id', ondelete='CASCADE'),
        nullable=False,
    )
    file_path: Mapped[Optional[str]] = mapped_column(String(255))

    query: Mapped['UserQueries'] = relationship(
        'UserQueries',
        back_populates='text_dates',
    )

    def __str__(self):
        return f"Расположение запроса ({self.id})"