from typing import List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Double,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal


class Base(DeclarativeBase):
    pass


class BalanceHistory(Base):
    __tablename__ = 'balance_history'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    transaction_type: Mapped[Optional[str]] = mapped_column(String(30))
    amount: Mapped[Optional[float]] = mapped_column(Double(53))
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    query_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('user_queries.query_id'),
        nullable=False,
    )

    query: Mapped['UserQueries'] = relationship(
        'UserQueries',
        back_populates='balance_histories',
    )


class Blacklist(Base):
    __tablename__ = 'blacklist'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    refresh_token: Mapped[Optional[str]] = mapped_column(String(255))


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
        ForeignKey('user_queries.query_id'),
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


class Keywords(Base):
    __tablename__ = 'keywords'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    word: Mapped[Optional[str]] = mapped_column(String(75))
    word_language: Mapped[Optional[str]] = mapped_column(String(5))
    word_type: Mapped[Optional[str]] = mapped_column(String(20))


class PaymentHistory(Base):
    __tablename__ = 'payment_history'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    transaction_id: Mapped[Optional[int]] = mapped_column(Integer)
    currency: Mapped[Optional[str]] = mapped_column(Text)
    payment_amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    operation_type: Mapped[Optional[str]] = mapped_column(Text)
    invoice_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('users.id'),
        nullable=False,
    )
    email: Mapped[Optional[str]] = mapped_column(Text)
    date_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ip_address: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped['UserQueries'] = relationship(
        'Users',
        back_populates='payment_histories',
    )


class ProhibitedSites(Base):
    __tablename__ = 'prohibited_sites'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    site_link: Mapped[Optional[str]] = mapped_column(String(100))


class QueriesBalance(Base):
    __tablename__ = 'queries_balance'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    query_id: Mapped[int] = mapped_column(
        ForeignKey('user_queries.query_id'),
        nullable=False,
    )
    balance: Mapped[decimal.Decimal] = mapped_column(Numeric)
    transaction_date: Mapped[datetime.datetime] = mapped_column(DateTime(True))

    query: Mapped['UserQueries'] = relationship(
        'UserQueries',
        back_populates='queries_balances',
    )


class ServicesBalance(Base):
    __tablename__ = 'services_balance'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    service_name: Mapped[Optional[str]] = mapped_column(String)
    balance: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)


class TelegramNotifications(Base):
    __tablename__ = 'telegram_notifications'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    chat_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True)

    user: Mapped['UserQueries'] = relationship(
        'Users',
        back_populates='telegram_notification',
    )


class TextData(Base):
    __tablename__ = 'text_data'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    query_id: Mapped[int] = mapped_column(
        ForeignKey('user_queries.query_id'),
        nullable=False,
    )
    query_data: Mapped[Optional[str]] = mapped_column(Text)

    query: Mapped['UserQueries'] = relationship(
        'UserQueries',
        back_populates='text_dates',
    )


class UserBalances(Base):
    __tablename__ = 'user_balances'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    balance: Mapped[Optional[float]] = mapped_column(Double(53))

    user: Mapped['Users'] = relationship(
        'Users',
        back_populates='user_balance',
    )


class UserQueries(Base):
    __tablename__ = 'user_queries'

    query_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
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

    user_role: Mapped['UserRole'] = relationship(
        'UserRole',
        back_populates='users',
    )
    user_balance: Mapped['UserBalances'] = relationship(
        'UserBalances',
        back_populates='user',
        cascade='all, delete-orphan',
    )
    user_queries: Mapped['UserQueries'] = relationship(
        'UserQueries',
        back_populates='user',
        cascade='all, delete-orphan',
    )
    payment_histories: Mapped['PaymentHistory'] = relationship(
        'PaymentHistory',
        back_populates='user',
        cascade='all, delete-orphan',
    )
    telegram_notification: Mapped['TelegramNotifications'] = relationship(
        'TelegramNotifications',
        back_populates='user',
        cascade='all, delete-orphan',
    )
