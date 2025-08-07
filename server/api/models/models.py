import datetime
import decimal
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Double,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship, mapped_column, DeclarativeBase


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
        ForeignKey('user_queries.query_id', ondelete='CASCADE'),
        nullable=False,
    )

    query: Mapped['UserQueries'] = relationship(
        'UserQueries',
        back_populates='balance_histories',
    )

    def __str__(self):
        return f"История баланса ({self.id})"


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
    query_id: Mapped[int] = mapped_column(
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

    def __str__(self):
        return f"История пополнения ({self.id})"


class ProhibitedSites(Base):
    __tablename__ = 'prohibited_sites'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    site_link: Mapped[Optional[str]] = mapped_column(String(100))

    def __str__(self):
        return f"Запрещенный сайт ({self.site_link})"


class QueriesBalance(Base):
    __tablename__ = 'queries_balance'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    query_id: Mapped[int] = mapped_column(
        ForeignKey('user_queries.query_id', ondelete='CASCADE'),
        nullable=False,
    )
    balance: Mapped[decimal.Decimal] = mapped_column(Numeric)
    transaction_date: Mapped[datetime.datetime] = mapped_column(DateTime(True))

    query: Mapped['UserQueries'] = relationship(
        'UserQueries',
        back_populates='queries_balances',
    )

    def __str__(self):
        return f"Баланс запроса ({self.id})"


class ServicesBalance(Base):
    __tablename__ = 'services_balance'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    service_name: Mapped[Optional[str]] = mapped_column(String)
    balance: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    balance_threshold: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)

    def __str__(self):
        return f"Баланс сервиса ({self.id})"


class TelegramNotifications(Base):
    __tablename__ = 'telegram_notifications'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    chat_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True)

    user: Mapped['UserQueries'] = relationship(
        'Users',
        back_populates='telegram_notification',
    )

    def __str__(self):
        return f"Телеграм уведомления ({self.id})"


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


class UserBalances(Base):
    __tablename__ = 'user_balances'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    balance: Mapped[Optional[float]] = mapped_column(Double(53))

    user: Mapped['Users'] = relationship(
        'Users',
        back_populates='user_balance',
    )

    def __str__(self):
        return f"Баланс пользователя ({self.id})"


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
    query_data: Mapped['QueriesData'] = relationship(
        'QueriesData',
        back_populates='query',
        cascade='all, delete-orphan',
    )

    events: Mapped['Events'] = relationship('Events', back_populates='query')

    def __str__(self):
        return f"Запрос ({self.query_id})"


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
    default_language_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('languages.id'),
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
    default_language: Mapped['Language'] = relationship(
        'Language',
        back_populates='users_with_default_language'
    )

    def __str__(self):
        return f"{self.email}"


class Language(Base):
    __tablename__ = 'languages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    english_name: Mapped[str] = mapped_column(String(100), nullable=False)
    russian_name: Mapped[str] = mapped_column(String(100), nullable=False)

    country_links: Mapped[List['CountryLanguage']] = relationship(
        back_populates='language',
        cascade='all, delete-orphan'
    )

    users_with_default_language: Mapped[List['Users']] = relationship(
        'Users',
        back_populates='default_language'
    )


class Countries(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    language_links: Mapped[List['CountryLanguage']] = relationship(
        back_populates='country',
        cascade='all, delete-orphan'
    )


class CountryLanguage(Base):
    __tablename__ = 'country_languages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'))
    language_id: Mapped[int] = mapped_column(ForeignKey('languages.id'))

    country: Mapped['Countries'] = relationship(back_populates='language_links')
    language: Mapped['Language'] = relationship(back_populates='country_links')


class ProhibitedPhoneSites(Base):
    __tablename__ = 'prohibited_phone_sites'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    site_link: Mapped[Optional[str]] = mapped_column(String(255))

    def __str__(self):
        return f"Запрещенный сайт для телефонов ({self.site_link})"


class QueriesData(Base):
    __tablename__ = 'queries_data'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    query_id: Mapped[int] = mapped_column(
        ForeignKey('user_queries.query_id', ondelete='CASCADE'),
        nullable=False,
    )
    title: Mapped[Optional[str]] = mapped_column(Text)
    info: Mapped[Optional[str]] = mapped_column(Text)
    link: Mapped[Optional[str]] = mapped_column(Text)
    publication_date: Mapped[Optional[str]] = mapped_column(Text)
    keyword_type: Mapped[Optional[str]] = mapped_column(Text)
    resource_type: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    query: Mapped['UserQueries'] = relationship(
        'UserQueries',
        back_populates='query_data',
    )

    def __str__(self):
        return f"Результаты запроса ({self.query_id})"
