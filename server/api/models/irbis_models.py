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

from server.api.models.models import Base, UserQueries


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
    court_general_full: Mapped[List['CourtGeneralJurFullTable']] = relationship(
        back_populates='region',
        cascade='all, delete-orphan'
    )
    arbitration_court_full: Mapped[List['ArbitrationCourtFullTable']] = relationship(
        back_populates='region',
        cascade='all, delete-orphan'
    )
    part_in_org_organizations: Mapped[List['PartInOrgOrganizationTable']] = relationship(
        back_populates='region',
        cascade='all, delete-orphan',
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

    arbitr_court_fulls: Mapped[List['ArbitrationCourtFullTable']] = relationship(back_populates='role')


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
    pledges_preview: Mapped[List['PledgesPreviewTable']] = relationship(back_populates='irbis_person')
    pledges_full: Mapped[List['PledgeFullTable']] = relationship(back_populates='irbis_person')
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
    court_name_val: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    role_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('person_role_types.id', ondelete='CASCADE'),
        nullable=True
    )
    case_date: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    case_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    inn: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    case_type_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('arbitr_court_case_types.id', ondelete='SET NULL'),
        nullable=True,
    )
    address_val: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    region_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('region_subjects.id', ondelete='CASCADE'),
        nullable=True
    )
    case_number: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    search_type: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)

    irbis_person: Mapped['IrbisPerson'] = relationship(back_populates='arbit_court_full')
    region: Mapped['RegionSubject'] = relationship(back_populates='arbitration_court_full')
    oponents: Mapped[List['ArbitrationCourtOpponents']] = relationship(back_populates='arbitration_court_full')
    case_type: Mapped[Optional['ArbitrationCourtCaseTypes']] = relationship(back_populates='arbitration_court_cases')
    role: Mapped[Optional['PersonRoleType']] = relationship(back_populates='arbitr_court_fulls')


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
    )
    name: Mapped[str] = mapped_column(String(128))

    arbitration_court_full: Mapped['ArbitrationCourtFullTable'] = relationship(
        back_populates='oponents',
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
    first_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    second_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    birth_date: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    born_place: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    inn: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    ogrn: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    snils: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    old_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    category_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    region_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    information: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    link: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    search_type: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)

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
    full_name: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    organization: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    position: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    normative_act: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    application_date: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    publish_date: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    excluded_reason: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

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
    case_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    region_id: Mapped[int] = mapped_column(ForeignKey('region_subjects.id', ondelete='CASCADE'), nullable=False)
    court_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    process_type_id: Mapped[str] = mapped_column(ForeignKey('process_types.id', ondelete='CASCADE'), nullable=False)
    start_date: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    end_date: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    review: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    judge: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    articles: Mapped[Optional[list[str]]] = mapped_column(JSONB, nullable=True)
    papers: Mapped[Optional[list[str]]] = mapped_column(String, nullable=True)
    papers_pretty: Mapped[Optional[list[str]]] = mapped_column(String, nullable=True)
    links: Mapped[Optional[dict[str, list[str]]]] = mapped_column(JSONB, nullable=True)
    match_type_id: Mapped[Optional[int]] = mapped_column(ForeignKey(
        'match_types.id',
        ondelete='CASCADE'),
        nullable=True
    )

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

    role: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    face: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    papers: Mapped[Optional[list[str]]] = mapped_column(String, nullable=True)
    papers_pretty: Mapped[Optional[list[str]]] = mapped_column(String, nullable=True)

    case: Mapped['CourtGeneralJurFullTable'] = relationship(back_populates='faces')


class CourtGeneralProgressTable(Base):
    __tablename__ = 'court_general_progress'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[int] = mapped_column(ForeignKey('court_general_full.id', ondelete='CASCADE'))

    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    progress_date: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    resolution: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    case: Mapped['CourtGeneralJurFullTable'] = relationship(back_populates='progress')


class PledgesPreviewTable(Base):
    __tablename__ = 'pledges_preview'

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
        back_populates='pledges_preview',
    )


class PledgeFullTable(Base):
    __tablename__ = 'pledges_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    reg_date: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    pledge_reestr_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    pledge_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    parties: Mapped[List['PledgePartiesTable']] = relationship(
        back_populates='pledge',
        cascade='all, delete-orphan',
    )
    pledges: Mapped[List['PledgeObjectTable']] = relationship(
        back_populates='pledge',
        cascade='all, delete-orphan',
    )
    irbis_person: Mapped['IrbisPerson'] = relationship(
        'IrbisPerson',
        back_populates='pledges_full',
    )


class PledgePartiesTable(Base):
    __tablename__ = 'pledge_parties'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pledge_id: Mapped[int] = mapped_column(ForeignKey('pledges_full.id', ondelete='CASCADE'))

    # Общие поля
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    type: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)  # 'pledger' | 'pledgee'
    subtype: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)  # 'people' | 'org'

    # Только для subtype = 'people'
    birth_date: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    # Только для subtype = 'org'
    inn: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    ogrn: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    pledge: Mapped['PledgeFullTable'] = relationship(back_populates='parties')


class PledgeObjectTable(Base):
    __tablename__ = 'pledge_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pledge_id: Mapped[int] = mapped_column(ForeignKey('pledges_full.id', ondelete='CASCADE'))

    pledge_num_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    pledge_num: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    pledge_type: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    pledge: Mapped['PledgeFullTable'] = relationship(back_populates='pledges')


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
    birth_date: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    fio: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    article: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    start_date_disq: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    end_date_disq: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    bornplace: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    fio_judge: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    office_judge: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    legal_name: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    office: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

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
    ip: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    fio: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    rosp: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    type_ip: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    summ: Mapped[Optional[str]] = mapped_column(Numeric, nullable=True)
    rekv: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    end_cause: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    pristav: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    pristav_phones: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

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
    scoring: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    errors: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    progress: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    popularity_full: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    popularity_short: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)

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

    # Relationships
    org: Mapped[Optional['PartInOrgOrganizationTable']] = relationship(
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


class PartInOrgOrganizationTable(Base):
    __tablename__ = 'part_in_org_organization'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    part_id: Mapped[int] = mapped_column(
        ForeignKey('part_in_org_full.id', ondelete='CASCADE'),
        nullable=False
    )
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    inn: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    ogrn: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    okved: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    region_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('region_subjects.id', ondelete='CASCADE'),
        nullable=True,
    )

    part: Mapped['PartInOrgFullTable'] = relationship(back_populates='org')
    region: Mapped[Optional['RegionSubject']] = relationship(back_populates='part_in_org_organizations')


class PartInOrgIndividualTable(Base):
    __tablename__ = 'part_in_org_individual'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    part_id: Mapped[int] = mapped_column(
        ForeignKey('part_in_org_full.id', ondelete='CASCADE'),
        nullable=False
    )

    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    inn: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

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
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    active: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    individual: Mapped['PartInOrgIndividualTable'] = relationship(back_populates='roles')


class TaxArrearsFullTable(Base):
    __tablename__ = 'tax_arrears_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    provider: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    money_name: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)  # Например: RUB
    money_value: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), nullable=True)

    fields: Mapped[List['TaxArrearsFieldTable']] = relationship(
        back_populates='tax_arrear',
        cascade='all, delete-orphan',
    )
    irbis_person: Mapped['IrbisPerson'] = relationship(
        back_populates='tax_arrears_full',
    )


class TaxArrearsFieldTable(Base):
    __tablename__ = 'tax_arrears_fields'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tax_arrear_id: Mapped[int] = mapped_column(
        ForeignKey('tax_arrears_full.id', ondelete='CASCADE'),
        nullable=False,
    )
    type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)  # "info" или "payment"
    field_name: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Обратная связь
    tax_arrear: Mapped['TaxArrearsFullTable'] = relationship(back_populates='fields')


class TerrorListFullTable(Base):
    __tablename__ = 'terror_list_full'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    irbis_person_id: Mapped[int] = mapped_column(ForeignKey('irbis_person.id', ondelete='CASCADE'), nullable=False)
    fio: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    birth_date: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    birth_place: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

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
