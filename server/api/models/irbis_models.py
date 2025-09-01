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

from api.models.models import Base, UserQueries


class PersonRegions(Base):
    __tablename__ = 'person_regions'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    person_id: Mapped[int] = mapped_column(
        ForeignKey('irbis_person.id', ondelete='CASCADE'),
        nullable=False
    )
    region_id: Mapped[int] = mapped_column(
        ForeignKey('region_subjects.id', ondelete='CASCADE'),
        nullable=False,
    )

    person: Mapped['IrbisPerson'] = relationship(back_populates='person_regions')
    region: Mapped['RegionSubject'] = relationship(back_populates='person_regions')


class RegionSubject(Base):
    __tablename__ = 'region_subjects'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    subject_number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    person_regions: Mapped[List['PersonRegions']] = relationship(
        back_populates='region',
        cascade='all, delete-orphan'
    )
    court_general_full: Mapped['CourtGeneralJurFullTable'] = relationship(
        back_populates='region',
        cascade='all, delete-orphan'
    )
    arbitration_court_full: Mapped['ArbitrationCourtFullTable'] = relationship(
        back_populates='region',
        cascade='all, delete-orphan'
    )


class ProcessType(Base):
    __tablename__ = 'process_types'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    code: Mapped[str] = mapped_column(String(1), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    court_general_jur_fulls: Mapped[List['CourtGeneralJurFullTable']] = relationship(back_populates='process_type')


class PersonRoleType(Base):
    __tablename__ = 'person_role_types'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    short_name: Mapped[str] = mapped_column(String(1), nullable=True)
    russian_name: Mapped[str] = mapped_column(String(100), nullable=False)


class IrbisPerson(Base):
    __tablename__ = 'irbis_person'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    query_id: Mapped[int] = mapped_column(
        ForeignKey('user_queries.query_id', ondelete='CASCADE'),
        nullable=False,
    )
    person_uuid: Mapped[str] = mapped_column(String(128))
    fullname: Mapped[str] = mapped_column(String(128))
    birth_date: Mapped[Optional[str]] = mapped_column(String(20))
    passport_series: Mapped[Optional[str]] = mapped_column(String(4))
    passport_number: Mapped[Optional[str]] = mapped_column(String(6))
    inn: Mapped[Optional[str]] = mapped_column(String(12))

    person_regions: Mapped[List['PersonRegions']] = relationship(
        back_populates='person',
        cascade='all, delete-orphan'
    )
    arbit_court_preview: Mapped[List['ArbitrationCourtPreviewTable']] = relationship(back_populates='irbis_person')
    arbit_court_full: Mapped[List['ArbitrationCourtFullTable']] = relationship(back_populates='irbis_person')
    bankruptcy_preview: Mapped['BankruptcyPreviewTable'] = relationship(back_populates='irbis_person')
    bankruptcy_full: Mapped[List['BankruptcyFullTable']] = relationship(back_populates='irbis_person')
    corruption_preview: Mapped['CorruptionPreviewTable'] = relationship(back_populates='irbis_person')
    corruption_full: Mapped[List['CorruptionFullTable']] = relationship(back_populates='irbis_person')
    court_gen_preview: Mapped[List['CourtGeneralJurPreviewTable']] = relationship(back_populates='irbis_person')
    court_gen_categorial: Mapped[List['CourtGeneralJurCategoricalTable']] = relationship(back_populates='irbis_person')
    court_gen_full: Mapped[List['CourtGeneralJurFullTable']] = relationship(back_populates='irbis_person')
    deposits_preview: Mapped[List['DepositsPreviewTable']] = relationship(back_populates='irbis_person')
    deposits_full: Mapped[List['DepositsFullTable']] = relationship(back_populates='irbis_person')
    disqualified_preview: Mapped[List['DisqualifiedPersonPreviewTable']] = relationship(back_populates='irbis_person')
    disqualified_full: Mapped[List['DisqualifiedPersonFullTable']] = relationship(back_populates='irbis_person')
    fssp_preview: Mapped[List['FSSPPreviewTable']] = relationship(back_populates='irbis_person')
    fssp_full: Mapped[List['FSSPFullTable']] = relationship(back_populates='irbis_person')
    mlindex_full: Mapped['MLIndexFullTable'] = relationship(back_populates='irbis_person')
    part_in_org_preview: Mapped[List['PartInOrgPreviewTable']] = relationship(back_populates='irbis_person')
    part_in_org_full: Mapped[List['PartInOrgFullTable']] = relationship(back_populates='irbis_person')
    tax_arrears_full: Mapped[List['TaxArrearsFullTable']] = relationship(back_populates='irbis_person')
    terror_list_preview: Mapped[List['TerrorListFullTable']] = relationship(back_populates='irbis_person')
    query: Mapped['UserQueries'] = relationship('UserQueries', back_populates='irbis_person')


class ArbitrationCourtPreviewTable(Base):
    __tablename__ = 'arbitr_court_preview'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    type: Mapped[str] = mapped_column(String(4))
    plaintiff: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    responder: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='arbit_court_preview',
    )


class ArbitrationCourtFullTable(Base):
    __tablename__ = 'arbitr_court_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    court_name_val: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(String(1))
    case_date: Mapped[str] = mapped_column(String(128))
    case_id: Mapped[str] = mapped_column(String(128))
    inn: Mapped[Optional[str]] = mapped_column(String(128))
    name: Mapped[str] = mapped_column(String(128))
    case_type_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('arbitr_court_case_types.id', ondelete='SET NULL'), 
        nullable=True,
    )
    address_val: Mapped[str] = mapped_column(String(128))
    region_id: Mapped[int] = mapped_column(ForeignKey('region_subjects.id', ondelete='CASCADE'), nullable=True)
    case_number: Mapped[str] = mapped_column(String(128), nullable=True)
    search_type: Mapped[str] = mapped_column(String(4), nullable=True)

    irbis_person: Mapped['IrbisPerson'] = relationship(back_populates='arbit_court_full')
    region: Mapped['RegionSubject'] = relationship(back_populates='arbitration_court_full')
    oponents: Mapped[List['ArbitrationCourtOpponents']] = relationship(back_populates='arbitration_court_full')


class ArbitrationCourtOpponents(Base):
    __tablename__ = 'arbitr_court_oponents'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    arbitration_court_full_id: Mapped[int] = mapped_column(
        ForeignKey(
            'arbitr_court_full.id',
            ondelete='CASCADE',
        ),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(128))

    arbitration_court_full: Mapped['ArbitrationCourtFullTable'] = relationship(
        back_populates='oponents',
    )
    case_type: Mapped[Optional['ArbitrationCourtCaseTypes']] = relationship(
        'ArbitrationCourtCaseTypes',
        back_populates='arbitration_court_cases',
    )


class ArbitrationCourtCaseTypes(Base):
    __tablename__ = 'arbitr_court_case_types'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    code: Mapped[int] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(128))

    arbitration_court_cases: Mapped[List['ArbitrationCourtFullTable']] = relationship(
        'ArbitrationCourtFullTable',
        back_populates='case_type',
    )


class BankruptcyPreviewTable(Base):
    __tablename__ = 'bankruptcy_preview'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)

    name: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    inn: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='bankruptcy_preview')


class BankruptcyFullTable(Base):
    __tablename__ = 'bankruptcy_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    first_name: Mapped[str] = mapped_column(String(128))
    second_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128))
    birth_date: Mapped[str] = mapped_column(String(128))
    born_place: Mapped[str] = mapped_column(String(256))
    inn: Mapped[str] = mapped_column(String(128))
    ogrn: Mapped[str] = mapped_column(String(128))
    snils: Mapped[str] = mapped_column(String(128))
    old_name: Mapped[Optional[str]] = mapped_column(String(128))
    category_name: Mapped[str] = mapped_column(String(128))
    location: Mapped[str] = mapped_column(String(256))
    region_name: Mapped[str] = mapped_column(String(128))
    information: Mapped[str] = mapped_column(String(256))
    link: Mapped[str] = mapped_column(String(256))

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='bankruptcy_full',
    )


class CorruptionPreviewTable(Base):
    __tablename__ = 'corruption_preview'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='corruption_preview',
    )


class CorruptionFullTable(Base):
    __tablename__ = 'corruption_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    key: Mapped[str] = mapped_column(String(256))
    full_name: Mapped[str] = mapped_column(String(256))
    organization: Mapped[str] = mapped_column(String(256))
    position: Mapped[str] = mapped_column(String(256))
    normative_act: Mapped[str] = mapped_column(String(256))
    application_date: Mapped[str] = mapped_column(String(128))
    publish_date: Mapped[str] = mapped_column(String(128))
    excluded_reason: Mapped[str] = mapped_column(String(256))

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='corruption_full',
    )


class CourtGeneralJurPreviewTable(Base):
    __tablename__ = 'court_general_preview'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    search_type: Mapped[str] = mapped_column(String(128))
    court_type: Mapped[str] = mapped_column(String(1))
    plan: Mapped[Optional[int]] = mapped_column(Integer, nullable=False, default=0)
    deff: Mapped[Optional[int]] = mapped_column(Integer, nullable=False, default=0)
    declarant: Mapped[Optional[int]] = mapped_column(Integer, nullable=False, default=0)
    face: Mapped[Optional[int]] = mapped_column(Integer, nullable=False, default=0)
    lawyer: Mapped[Optional[int]] = mapped_column(Integer, nullable=False, default=0)

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='court_gen_preview',
    )


class CourtGeneralJurCategoricalTable(Base):
    __tablename__ = 'court_general_category'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    type: Mapped[str] = mapped_column(String(512))
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='court_gen_categorial',
    )


class CourtGeneralJurFullTable(Base):
    __tablename__ = 'court_general_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    case_number: Mapped[str] = mapped_column(String)
    region_id: Mapped[int] = mapped_column(ForeignKey('region_subjects.id', ondelete='CASCADE'), nullable=False)
    court_name: Mapped[str] = mapped_column(String)
    process_type_id: Mapped[str] = mapped_column(ForeignKey('process_types.id', ondelete='CASCADE'), nullable=False)
    start_date: Mapped[str] = mapped_column(String(128))
    end_date: Mapped[str] = mapped_column(String(128))
    review: Mapped[Optional[int]] = mapped_column(Integer)
    judge: Mapped[Optional[str]] = mapped_column(String)
    articles: Mapped[Optional[list[str]]] = mapped_column(JSONB)
    papers: Mapped[Optional[list[str]]] = mapped_column(String)
    papers_pretty: Mapped[Optional[list[str]]] = mapped_column(String)
    links: Mapped[Optional[dict[str, list[str]]]] = mapped_column(JSONB)
    match_type_id: Mapped[int] = mapped_column(ForeignKey('match_types.id', ondelete='CASCADE'), nullable=True)

    faces: Mapped[List['CourtGeneralFacesTable']] = relationship(
        back_populates='case',
        cascade="all, delete-orphan",
    )
    progress: Mapped[List['CourtGeneralProgressTable']] = relationship(
        back_populates='case',
        cascade="all, delete-orphan",
    )
    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='court_gen_full',
    )
    match_type: Mapped[Optional['MatchType']] = relationship(
        'MatchType',
        back_populates='court_cases',
    )
    region: Mapped['RegionSubject'] = relationship(back_populates='court_general_full')
    process_type: Mapped['ProcessType'] = relationship(back_populates='court_general_jur_fulls')


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

    name: Mapped[Optional[str]] = mapped_column(String)
    progress_date: Mapped[Optional[str]] = mapped_column(String(128))
    resolution: Mapped[Optional[str]] = mapped_column(String)

    case: Mapped['CourtGeneralJurFullTable'] = relationship(back_populates='progress')


class DepositsPreviewTable(Base):
    __tablename__ = 'deposits_preview'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    pledge_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pledge_type: Mapped[str] = mapped_column(String(128))
    response_id: Mapped[int] = mapped_column(Integer)

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='deposits_preview',
    )


class DepositsFullTable(Base):
    __tablename__ = 'deposits_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    pledge_count: Mapped[int] = mapped_column(Integer)
    pledge_type: Mapped[str] = mapped_column(String(128))
    response_id: Mapped[int] = mapped_column(Integer)

    # Relationships
    parties: Mapped[List['DepositsPartiesTable']] = relationship(
        back_populates='deposit',
        cascade='all, delete-orphan',
    )
    pledges: Mapped[List['DepositsPledgeObjectTable']] = relationship(
        back_populates='deposit',
        cascade='all, delete-orphan',
    )
    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='deposits_full',
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
    birth_date: Mapped[str] = mapped_column(String(128))

    # Только для subtype = 'org'
    inn: Mapped[Optional[str]] = mapped_column(String(20))
    ogrn: Mapped[Optional[str]] = mapped_column(String(20))

    deposit: Mapped['DepositsFullTable'] = relationship(back_populates='parties')


class DepositsPledgeObjectTable(Base):
    __tablename__ = 'deposits_pledges'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    deposit_id: Mapped[int] = mapped_column(ForeignKey('deposits_full.id', ondelete='CASCADE'))

    pledge_id_name: Mapped[str] = mapped_column(String(128))
    pledge_id: Mapped[str] = mapped_column(String(512))
    pledge_type: Mapped[str] = mapped_column(String(512))
    external_id: Mapped[int] = mapped_column(Integer)

    deposit: Mapped['DepositsFullTable'] = relationship(back_populates='pledges')


class DisqualifiedPersonPreviewTable(Base):
    __tablename__ = 'disqualified_person_preview'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)

    count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='disqualified_preview',
    )


class DisqualifiedPersonFullTable(Base):
    __tablename__ = 'disqualified_person_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    response_id: Mapped[int] = mapped_column(Integer)
    reestr_key: Mapped[str] = mapped_column(String(512))
    birth_date: Mapped[str] = mapped_column(String(128))
    fio: Mapped[str] = mapped_column(String(512))
    article: Mapped[str] = mapped_column(String(512))
    start_date_disq: Mapped[str] = mapped_column(String(128))
    end_date_disq: Mapped[str] = mapped_column(String(128))
    bornplace: Mapped[str] = mapped_column(String(512))
    fio_judge: Mapped[str] = mapped_column(String(512))
    office_judge: Mapped[str] = mapped_column(String(512))
    legal_name: Mapped[str] = mapped_column(String(512))
    office: Mapped[str] = mapped_column(String(512))
    department: Mapped[str] = mapped_column(String(512))

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='disqualified_full',
    )


class FSSPPreviewTable(Base):
    __tablename__ = 'fssp_preview'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    response_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(512))
    type_sum: Mapped[float] = mapped_column(Numeric)
    type_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='fssp_preview',
    )


class FSSPFullTable(Base):
    __tablename__ = 'fssp_full'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    ip: Mapped[str] = mapped_column(String(512))
    fio: Mapped[str] = mapped_column(String(512))
    rosp: Mapped[str] = mapped_column(String(512))
    type_ip: Mapped[str] = mapped_column(String(512))
    summ: Mapped[float] = mapped_column(Numeric)
    rekv: Mapped[str] = mapped_column(String(512))
    end_cause: Mapped[str] = mapped_column(String(128))
    pristav: Mapped[str] = mapped_column(String(512))
    pristav_phones: Mapped[Optional[str]] = mapped_column(String(512))
    response_id: Mapped[Optional[int]] = mapped_column(Integer)

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='fssp_full',
    )


class MLIndexFullTable(Base):
    __tablename__ = 'ml_index_full'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    scoring: Mapped[float] = mapped_column(Numeric)
    errors: Mapped[str] = mapped_column(Text)
    progress: Mapped[float] = mapped_column(Numeric)
    popularity_full: Mapped[float] = mapped_column(Numeric)
    popularity_short: Mapped[float] = mapped_column(Numeric)

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='mlindex_full',
    )


class PartInOrgPreviewTable(Base):
    __tablename__ = 'part_in_org_preview'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    filter_type: Mapped[str] = mapped_column(String(512))
    count: Mapped[float] = mapped_column(Numeric, nullable=False, default=0)
    part_type: Mapped[str] = mapped_column(String(512))

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='part_in_org_preview',
    )


class PartInOrgFullTable(Base):
    __tablename__ = 'part_in_org_full'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    filter_type: Mapped[str] = mapped_column(String(512))
    count: Mapped[float] = mapped_column(Numeric)
    part_type: Mapped[str] = mapped_column(String(512))

    # Relationships
    org: Mapped[Optional['PartInOrgOrgTable']] = relationship(
        back_populates='part',
        cascade='all, delete-orphan',
        uselist=False,
    )
    individual: Mapped[Optional['PartInOrgIndividualTable']] = relationship(
        back_populates='part',
        cascade='all, delete-orphan',
        uselist=False,
    )
    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='part_in_org_full',
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


class TaxArrearsFullTable(Base):
    __tablename__ = 'tax_arrears_full'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    provider: Mapped[str] = mapped_column(String(512))
    money_name: Mapped[str] = mapped_column(String(8))  # Например: RUB
    money_code: Mapped[int] = mapped_column(Integer)  # Например: 1283
    money_value: Mapped[float] = mapped_column(Numeric(15, 2))

    # Relationship
    fields: Mapped[List['TaxArrearsFieldTable']] = relationship(
        back_populates='arrear',
        cascade='all, delete-orphan',
    )
    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='tax_arrears_full',
    )


class TaxArrearsFieldTable(Base):
    __tablename__ = 'tax_arrears_fields'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    arrear_id: Mapped[int] = mapped_column(
        ForeignKey('tax_arrears_full.id', ondelete='CASCADE'),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(String(32))  # "info" или "payment"
    field_id: Mapped[str] = mapped_column(String(128))
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
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    response_id: Mapped[str] = mapped_column(String(512))
    fio: Mapped[str] = mapped_column(String(512))
    birth_date: Mapped[str] = mapped_column(String(128))
    birth_place: Mapped[str] = mapped_column(String(512))

    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='terror_list_preview',
    )


class MatchType(Base):
    __tablename__ = 'match_types'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    court_cases: Mapped[List['CourtGeneralJurFullTable']] = relationship(
        'CourtGeneralJurFullTable',
        back_populates='match_type'
    )
