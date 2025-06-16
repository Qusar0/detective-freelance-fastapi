import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base


class UserQueries(Base):
    __tablename__ = 'user_queries'

    query_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    query_unix_date: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
    )
    query_status: Mapped[Optional[str]] = mapped_column(Text)
    query_title: Mapped[Optional[str]] = mapped_column(Text)
    query_created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
    )
    query_category: Mapped[Optional[str]] = mapped_column(Text)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    user: Mapped['Users'] = relationship(
        'Users',
        back_populates='user_queries',
    )
    balance_histories: Mapped['BalanceHistory'] = relationship(
        'BalanceHistory',
        back_populates='query',
        cascade='all, delete-orphan',
    )
    text_dates: Mapped['TextData'] = relationship(
        'TextData',
        back_populates='query',
        cascade='all, delete-orphan',
    )
    queries_balances: Mapped['QueriesBalance'] = relationship(
        'QueriesBalance',
        back_populates='query',
        cascade='all, delete-orphan',
    )

    events: Mapped['Events'] = relationship('Events', back_populates='query')

    def __str__(self):
        return f"Запрос ({self.query_id})"
