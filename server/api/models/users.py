import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql import func

from server.api.models.models import Base

if TYPE_CHECKING:
    from server.api.models import UserRole, UserBalances, UserQueries, PaymentHistory, TelegramNotifications


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    is_confirmed: Mapped[bool] = mapped_column(
        Boolean,
        server_default=text('false'),
    )
    user_role_id: Mapped[int] = mapped_column(
        ForeignKey('user_role.id'),
        nullable=False,
    )
    password: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(String(80))
    created: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True),
        default=func.now()
    )
    confirmation_date: Mapped[Optional[int]] = mapped_column(Integer)
    last_visited: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(True),
        onupdate=func.now(),
        nullable=True
    )

    user_role: Mapped['UserRole'] = relationship(
        'UserRole',
        back_populates='users',
    )
    user_balance: Mapped['UserBalances'] = relationship(
        'UserBalances',
        back_populates='user',
        cascade='all, delete-orphan',
    )
    user_queries: Mapped[List['UserQueries']] = relationship(
        'UserQueries',
        back_populates='user',
        cascade='all, delete-orphan',
    )
    payment_histories: Mapped[List['PaymentHistory']] = relationship(
        'PaymentHistory',
        back_populates='user',
        cascade='all, delete-orphan',
    )
    telegram_notification: Mapped['TelegramNotifications'] = relationship(
        'TelegramNotifications',
        back_populates='user',
        cascade='all, delete-orphan',
    )

    def __str__(self):
        return f"{self.email}"
