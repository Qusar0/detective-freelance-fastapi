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


# IRBIS TABLES!
class PersonsUUID(Base):
    __tablename__ = 'persons_uuid'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    query_id: Mapped[int] = mapped_column(
        ForeignKey('user_queries.query_id', ondelete='CASCADE'),
        nullable=False,
    )

    person_uuid: Mapped[str] = mapped_column(String(64))

    arbit_court_preview: Mapped[List['ArbitrationCourtPreviewTable']] = relationship(back_populates='uid_relation')
    arbit_court_full: Mapped[List['ArbitrationCourtFullTable']] = relationship(back_populates='uid_relation')
    bankruptcy_preview: Mapped['BankruptcyPreviewTable'] = relationship(back_populates='uid_relation')
    bankruptcy_full: Mapped[List['BankruptcyFullTable']] = relationship(back_populates='uid_relation')
    corruption_preview: Mapped['CorruptionPreviewTable'] = relationship(back_populates='uid_relation')
    corruption_full: Mapped[List['CorruptionFullTable']] = relationship(back_populates='uid_relation')
    court_gen_preview: Mapped[List['CourtGeneralJurPreviewTable']] = relationship(back_populates='uid_relation')
    court_gen_categorial: Mapped[List['CourtGeneralJurCategoricalTable']] = relationship(back_populates='uid_relation')
    # arbit_court_preview: Mapped[List['ArbitrationCourtPreviewTable']] = relationship(
    #     'ArbitrationCourtPreviewTable', back_populates='uid_relation')
    deposits_preview: Mapped[List['DepositsPreviewTable']] = relationship(back_populates='uid_relation')
    # arbit_court_preview: Mapped[List['DepositsFullTable']] = relationship(
    #     'DepositsFullTable', back_populates='uid_relation')
    disqualified_full: Mapped[List['DisqualifiedPersonFullTable']] = relationship(back_populates='uid_relation')
    fssp_preview: Mapped[List['FSSPPreviewTable']] = relationship(back_populates='uid_relation')
    fssp_full: Mapped[List['FSSPFullTable']] = relationship(back_populates='uid_relation')
    mlindex_full: Mapped['MLIndexFullTable'] = relationship(back_populates='uid_relation')
    part_in_org_preview: Mapped[List['PartInOrgPreviewTable']] = relationship(back_populates='uid_relation')
    # mlindex_full: Mapped[List['MLIndexFullTable']] = relationship(
    #     'MLIndexFullTable', back_populates='uid_relation')
    # mlindex_full: Mapped[List['MLIndexFullTable']] = relationship(
    #     'MLIndexFullTable', back_populates='uid_relation')
    terror_list_preview: Mapped[List['TerrorListFullTable']] = relationship(back_populates='uid_relation')


class ArbitrationCourtPreviewTable(Base):
    __tablename__ = 'arbitr_court_preview'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    type: Mapped[str] = mapped_column(String(4))
    plaintiff: Mapped[int] = mapped_column(Integer)
    responder: Mapped[int] = mapped_column(Integer)

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='arbit_court_preview')


class ArbitrationCourtFullTable(Base):
    __tablename__ = 'arbitr_court_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    court_name_val: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(1))
    case_date: Mapped[str] = mapped_column(String(64))
    case_id: Mapped[str] = mapped_column(String(64))
    inn: Mapped[Optional[int]] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(64))
    case_type: Mapped[str] = mapped_column(String(1))
    response_id: Mapped[str] = mapped_column(String(64))
    address_val: Mapped[str] = mapped_column(String(64))

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='arbit_court_full')


class BankruptcyPreviewTable(Base):
    __tablename__ = 'bankruptcy_preview'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    name: Mapped[int] = mapped_column(Integer)
    inn: Mapped[int] = mapped_column(Integer)

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='bankruptcy_preview')


class BankruptcyFullTable(Base):
    __tablename__ = 'bankruptcy_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    first_name: Mapped[str] = mapped_column(String(64))
    second_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))
    birth_date: Mapped[str] = mapped_column(String(64))
    born_place: Mapped[str] = mapped_column(String(256))
    inn: Mapped[str] = mapped_column(String(64))
    ogrn: Mapped[str] = mapped_column(String(64))
    snils: Mapped[str] = mapped_column(String(64))
    old_name: Mapped[Optional[str]] = mapped_column(String(64))
    category_name: Mapped[str] = mapped_column(String(64))
    location: Mapped[str] = mapped_column(String(256))
    region_name: Mapped[str] = mapped_column(String(64))
    information: Mapped[str] = mapped_column(String(256))
    link: Mapped[str] = mapped_column(String(256))

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='bankruptcy_full')


class CorruptionPreviewTable(Base):
    __tablename__ = 'corruption_preview'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    count: Mapped[int] = mapped_column(Integer)

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='corruption_preview')


class CorruptionFullTable(Base):
    __tablename__ = 'corruption_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    key: Mapped[str] = mapped_column(String(256))
    full_name: Mapped[str] = mapped_column(String(256))
    organization: Mapped[str] = mapped_column(String(256))
    position: Mapped[str] = mapped_column(String(256))
    normative_act: Mapped[str] = mapped_column(String(256))
    application_date: Mapped[str] = mapped_column(String(64))
    publish_date: Mapped[str] = mapped_column(String(64))
    excluded_reason: Mapped[str] = mapped_column(String(256))

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='corruption_full')


class CourtGeneralJurPreviewTable(Base):
    __tablename__ = 'court_general_preview'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    search_type: Mapped[str] = mapped_column(String(64))
    court_type: Mapped[str] = mapped_column(String(1))
    plan: Mapped[Optional[int]] = mapped_column(Integer)
    deff: Mapped[Optional[int]] = mapped_column(Integer)
    declarant: Mapped[Optional[int]] = mapped_column(Integer)
    face: Mapped[Optional[int]] = mapped_column(Integer)
    lawyer: Mapped[Optional[int]] = mapped_column(Integer)

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='court_gen_preview')


class CourtGeneralJurCategoricalTable(Base):
    __tablename__ = 'court_general_category'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    type: Mapped[str] = mapped_column(String(128))
    count: Mapped[int] = mapped_column(Integer)

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='court_gen_categorial')


class CourtGeneralJurFullTable(Base):  # todo: доделать эту таблицу, она большая
    __tablename__ = 'court_general_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    headers: Mapped[Optional['CourtGeneralHeaderTable']] = relationship(
        back_populates='case', cascade="all, delete-orphan", uselist=False
    )

    faces: Mapped[List['CourtGeneralFacesTable']] = relationship(
        back_populates='case', cascade="all, delete-orphan"
    )

    progress: Mapped[List['CourtGeneralProgressTable']] = relationship(
        back_populates='case', cascade="all, delete-orphan"
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)


class CourtGeneralHeaderTable(Base):
    __tablename__ = 'court_general_header'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[int] = mapped_column(ForeignKey('court_general_full.id', ondelete='CASCADE'))

    case_number: Mapped[str] = mapped_column(String)
    region: Mapped[int] = mapped_column(Integer)
    court_name: Mapped[str] = mapped_column(String)
    process_type: Mapped[str] = mapped_column(String(1))
    start_date: Mapped[str] = mapped_column(String(64))
    end_date: Mapped[str] = mapped_column(String(64))
    review: Mapped[Optional[int]] = mapped_column(Integer)
    judge: Mapped[Optional[str]] = mapped_column(String)

    articles: Mapped[Optional[list[str]]] = mapped_column(JSONB)
    papers: Mapped[Optional[list[str]]] = mapped_column(String)
    papers_pretty: Mapped[Optional[list[str]]] = mapped_column(String)
    links: Mapped[Optional[dict[str, list[str]]]] = mapped_column(JSONB)

    case: Mapped['CourtGeneralJurFullTable'] = relationship(back_populates='headers')


class CourtGeneralFacesTable(Base):
    __tablename__ = 'court_general_faces'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[int] = mapped_column(ForeignKey('court_general_full.id', ondelete='CASCADE'))

    role: Mapped[str] = mapped_column(String)
    role_name: Mapped[str] = mapped_column(String)
    face: Mapped[str] = mapped_column(String)
    papers: Mapped[Optional[list[str]]] = mapped_column(String)
    papers_pretty: Mapped[Optional[list[str]]] = mapped_column(String)

    case: Mapped['CourtGeneralJurFullTable'] = relationship(back_populates='faces')


class CourtGeneralProgressTable(Base):
    __tablename__ = 'court_general_progress'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[int] = mapped_column(ForeignKey('court_general_full.id', ondelete='CASCADE'))

    progress_date: Mapped[str] = mapped_column(String(64))
    status: Mapped[Optional[str]] = mapped_column(String)
    note: Mapped[Optional[str]] = mapped_column(String)

    case: Mapped['CourtGeneralJurFullTable'] = relationship(back_populates='progress')


class DepositsPreviewTable(Base):
    __tablename__ = 'deposits_preview'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    pledge_count: Mapped[int] = mapped_column(Integer)
    pledge_type: Mapped[str] = mapped_column(String(64))
    response_id: Mapped[int] = mapped_column(Integer)

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='deposits_preview')


class DepositsFullTable(Base):  # todo: доделать эту таблицу, она большая
    __tablename__ = 'deposits_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    pledge_count: Mapped[int] = mapped_column(Integer)
    pledge_type: Mapped[str] = mapped_column(String(64))
    response_id: Mapped[int] = mapped_column(Integer)

    # Relationships
    parties: Mapped[List['DepositsPartiesTable']] = relationship(
        back_populates='deposit',
        cascade='all, delete-orphan'
    )
    pledges: Mapped[List['DepositsPledgeObjectTable']] = relationship(
        back_populates='deposit',
        cascade='all, delete-orphan'
    )


class DepositsPartiesTable(Base):
    __tablename__ = 'deposits_parties'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    deposit_id: Mapped[int] = mapped_column(ForeignKey('deposits_full.id', ondelete='CASCADE'))

    # Общие поля
    name: Mapped[str] = mapped_column(String)
    external_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(16))  # 'pledger' | 'pledgee'
    subtype: Mapped[str] = mapped_column(String(16))  # 'people' | 'org'

    # Только для subtype = 'people'
    birth_date: Mapped[str] = mapped_column(String(64))

    # Только для subtype = 'org'
    inn: Mapped[Optional[str]] = mapped_column(String(20))
    ogrn: Mapped[Optional[str]] = mapped_column(String(20))

    deposit: Mapped['DepositsFullTable'] = relationship(back_populates='parties')


class DepositsPledgeObjectTable(Base):
    __tablename__ = 'deposits_pledges'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    deposit_id: Mapped[int] = mapped_column(ForeignKey('deposits_full.id', ondelete='CASCADE'))

    pledge_id_name: Mapped[str] = mapped_column(String(64))
    pledge_id: Mapped[str] = mapped_column(String(128))
    pledge_type: Mapped[str] = mapped_column(String(128))
    external_id: Mapped[int] = mapped_column(Integer)

    deposit: Mapped['DepositsFullTable'] = relationship(back_populates='pledges')


class DisqualifiedPersonPreviewTable(Base):
    __tablename__ = 'disqualified_person_preview'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    count: Mapped[int] = mapped_column(Integer)

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='disqualified_preview')


class DisqualifiedPersonFullTable(Base):
    __tablename__ = 'disqualified_person_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    response_id: Mapped[int] = mapped_column(Integer)
    reestr_key: Mapped[str] = mapped_column(String(128))
    birth_date: Mapped[str] = mapped_column(String(64))
    fio: Mapped[str] = mapped_column(String(128))
    article: Mapped[str] = mapped_column(String(128))
    start_date_disq: Mapped[str] = mapped_column(String(64))
    end_date_disq: Mapped[str] = mapped_column(String(64))
    bornplace: Mapped[str] = mapped_column(String(128))
    fio_judge: Mapped[str] = mapped_column(String(128))
    office_judge: Mapped[str] = mapped_column(String(128))
    legal_name: Mapped[str] = mapped_column(String(128))
    office: Mapped[str] = mapped_column(String(128))
    department: Mapped[str] = mapped_column(String(128))

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='disqualified_full')


class FSSPPreviewTable(Base):
    __tablename__ = 'fssp_preview'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    response_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(128))
    type_sum: Mapped[float] = mapped_column(Numeric)
    type_count: Mapped[int] = mapped_column(Integer)

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='fssp_preview')


class FSSPFullTable(Base):
    __tablename__ = 'fssp_full'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    ip: Mapped[str] = mapped_column(String(128))
    fio: Mapped[str] = mapped_column(String(128))
    rosp: Mapped[str] = mapped_column(String(128))
    type_ip: Mapped[str] = mapped_column(String(128))
    summ: Mapped[float] = mapped_column(Numeric)
    rekv: Mapped[str] = mapped_column(String(128))
    end_cause: Mapped[str] = mapped_column(String(64))
    pristav: Mapped[str] = mapped_column(String(128))
    pristav_phones: Mapped[str] = mapped_column(String(128))
    response_id: Mapped[int] = mapped_column(Integer)

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='fssp_full')


class MLIndexFullTable(Base):
    __tablename__ = 'ml_index_full'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    scoring: Mapped[float] = mapped_column(Numeric)
    errors: Mapped[str] = mapped_column(Text)
    progress: Mapped[float] = mapped_column(Numeric)
    popularity_full: Mapped[float] = mapped_column(Numeric)
    popularity_short: Mapped[float] = mapped_column(Numeric)

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='mlindex_full')


class PartInOrgPreviewTable(Base):
    __tablename__ = 'part_in_org_preview'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)
    filter_type: Mapped[str] = mapped_column(String(128))
    count: Mapped[float] = mapped_column(Numeric)
    part_type: Mapped[str] = mapped_column(String(128))

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='part_in_org_preview')


class PartInOrgFullTable(Base):  # todo: доделать эту таблицу, она большая (тут надо посмотреть и делать поля односложных json/еще 4 таблицы)
    __tablename__ = 'part_in_org_full'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)
    filter_type: Mapped[str] = mapped_column(String(128))
    count: Mapped[float] = mapped_column(Numeric)
    part_type: Mapped[str] = mapped_column(String(128))

    # Relationships
    org: Mapped[Optional['PartInOrgOrgTable']] = relationship(
        back_populates='part',
        cascade='all, delete-orphan',
        uselist=False
    )

    individual: Mapped[Optional['PartInOrgIndividualTable']] = relationship(
        back_populates='part',
        cascade='all, delete-orphan',
        uselist=False
    )


class PartInOrgOrgTable(Base):
    __tablename__ = 'part_in_org_org'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    part_id: Mapped[int] = mapped_column(
        ForeignKey('part_in_org_full.id', ondelete='CASCADE'),
        nullable=False
    )

    name: Mapped[str] = mapped_column(String)
    inn: Mapped[str] = mapped_column(String(20))
    ogrn: Mapped[Optional[str]] = mapped_column(String(20))
    adress: Mapped[str] = mapped_column(String(200))

    okved: Mapped[Optional[dict]] = mapped_column(JSONB)

    part: Mapped['PartInOrgFullTable'] = relationship(back_populates='org')


class PartInOrgIndividualTable(Base):
    __tablename__ = 'part_in_org_individual'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    part_id: Mapped[int] = mapped_column(
        ForeignKey('part_in_org_full.id', ondelete='CASCADE'),
        nullable=False
    )

    name: Mapped[str] = mapped_column(String)
    inn: Mapped[str] = mapped_column(String(20))

    part: Mapped['PartInOrgFullTable'] = relationship(back_populates='individual')

    roles: Mapped[List['PartInOrgRoleTable']] = relationship(
        back_populates='individual',
        cascade='all, delete-orphan'
    )


class PartInOrgRoleTable(Base):
    __tablename__ = 'part_in_org_roles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    individual_id: Mapped[int] = mapped_column(
        ForeignKey('part_in_org_individual.id', ondelete='CASCADE'),
        nullable=False
    )

    name: Mapped[str] = mapped_column(String)
    active: Mapped[bool] = mapped_column(Boolean)

    individual: Mapped['PartInOrgIndividualTable'] = relationship(back_populates='roles')


class TaxArrearsFullTable(Base):  # todo: доделать эту таблицу, она большая
    __tablename__ = 'tax_arrears_full'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    provider: Mapped[str] = mapped_column(String(128))

    money_name: Mapped[str] = mapped_column(String(8))  # Например: RUB
    money_code: Mapped[int] = mapped_column(Integer)    # Например: 643
    money_value: Mapped[float] = mapped_column(Numeric(15, 2))

    # Relationship
    fields: Mapped[List['TaxArrearsFieldTable']] = relationship(
        back_populates='arrear',
        cascade='all, delete-orphan'
    )


class TaxArrearsFieldTable(Base):
    __tablename__ = 'tax_arrears_fields'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    arrear_id: Mapped[int] = mapped_column(
        ForeignKey('tax_arrears_full.id', ondelete='CASCADE'),
        nullable=False
    )

    type: Mapped[str] = mapped_column(String(32))  # "info" или "payment"

    field_id: Mapped[str] = mapped_column(String(64))
    field_name: Mapped[str] = mapped_column(String(256))
    field_type: Mapped[str] = mapped_column(String(32))
    value: Mapped[str] = mapped_column(Text)

    # Обратная связь
    arrear: Mapped['TaxArrearsFullTable'] = relationship(back_populates='fields')


class TerrorListFullTable(Base):
    __tablename__ = 'terror_list_full'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    response_id: Mapped[str] = mapped_column(String(128))
    fio: Mapped[str] = mapped_column(String(128))
    birth_date: Mapped[str] = mapped_column(String(64))
    birth_place: Mapped[str] = mapped_column(String(128))

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='terror_list_preview')
