from typing import List, Optional

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base


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
    court_gen_full: Mapped[List['CourtGeneralJurFullTable']] = relationship(back_populates='uid_relation')
    deposits_preview: Mapped[List['DepositsPreviewTable']] = relationship(back_populates='uid_relation')
    deposits_full: Mapped[List['DepositsFullTable']] = relationship(back_populates='uid_relation')
    disqualified_full: Mapped[List['DisqualifiedPersonFullTable']] = relationship(back_populates='uid_relation')
    fssp_preview: Mapped[List['FSSPPreviewTable']] = relationship(back_populates='uid_relation')
    fssp_full: Mapped[List['FSSPFullTable']] = relationship(back_populates='uid_relation')
    mlindex_full: Mapped['MLIndexFullTable'] = relationship(back_populates='uid_relation')
    part_in_org_preview: Mapped[List['PartInOrgPreviewTable']] = relationship(back_populates='uid_relation')
    part_in_org_full: Mapped[List['PartInOrgFullTable']] = relationship(back_populates='uid_relation')
    tax_arrears_full: Mapped[List['TaxArrearsFullTable']] = relationship(back_populates='uid_relation')
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


class CourtGeneralJurFullTable(Base):
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

    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='court_gen_full')

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


class DepositsFullTable(Base):
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
    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='deposits_full')


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


class PartInOrgFullTable(Base):
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
    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='part_in_org_full')


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


class TaxArrearsFullTable(Base):
    __tablename__ = 'tax_arrears_full'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_uuid: Mapped[int] = mapped_column(ForeignKey('persons_uuid.id', ondelete='CASCADE'), nullable=False)

    provider: Mapped[str] = mapped_column(String(128))

    money_name: Mapped[str] = mapped_column(String(8))  # Например: RUB
    money_code: Mapped[int] = mapped_column(Integer)  # Например: 643
    money_value: Mapped[float] = mapped_column(Numeric(15, 2))

    # Relationship
    fields: Mapped[List['TaxArrearsFieldTable']] = relationship(
        back_populates='arrear',
        cascade='all, delete-orphan'
    )
    uid_relation: Mapped['PersonsUUID'] = relationship(
        'PersonsUUID',
        back_populates='tax_arrears_full')


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
