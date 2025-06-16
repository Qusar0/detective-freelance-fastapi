import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base


class Events(Base):
    __tablename__ = 'events'

    event_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    event_type: Mapped[Optional[str]] = mapped_column(String(50))
    event_status: Mapped[Optional[str]] = mapped_column(String(50))
    query_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('user_queries.query_id', ondelete='CASCADE'),
        nullable=False,
    )
    created_time: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True),
    )
    additional_data: Mapped[Optional[dict]] = mapped_column(JSONB)

    query: Mapped['UserQueries'] = relationship(
        'UserQueries',
        back_populates='events',
    )

    def __str__(self):
        return f"Событие ({self.event_id})"
