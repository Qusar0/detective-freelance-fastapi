from dataclasses import dataclass
from typing import Optional

from celery import shared_task

from server.api.IRBIS_parser.arbitration_court import ArbitrationCourt
from server.api.IRBIS_parser.bankruptcy import Bankruptcy
from server.api.IRBIS_parser.corruption import Corruption
from server.api.IRBIS_parser.court_of_general_jurisdiction import CourtGeneralJurisdiction
from server.api.IRBIS_parser.deposits import Deposits
from server.api.IRBIS_parser.disqualified_persons import DisqualifiedPersons
from server.api.IRBIS_parser.fssp import FSSP
from server.api.IRBIS_parser.ml_index import MLIndex
from server.api.IRBIS_parser.participation_in_organization import ParticipationOrganization
from server.api.IRBIS_parser.tax_arrears import TaxArrears
from server.api.IRBIS_parser.terror_list import TerrorList
from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS
from server.tasks.base.base import BaseSearchTask
from server.tasks.celery_config import (
    get_event_loop,
)
from server.tasks.logger import SearchLogger

from server.api.models.models import (
    ArbitrationCourtPreviewTable, ArbitrationCourtFullTable, BankruptcyPreviewTable,
    BankruptcyFullTable, CorruptionPreviewTable, CorruptionFullTable,
    CourtGeneralJurPreviewTable, CourtGeneralJurCategoricalTable, DepositsPreviewTable, DisqualifiedPersonPreviewTable,
    DisqualifiedPersonFullTable, FSSPPreviewTable, FSSPFullTable, MLIndexFullTable, PartInOrgPreviewTable,
    TerrorListFullTable
)


@dataclass
class IrbisSearchParameters:
    query_id: int
    price: float

    first_name: str
    last_name: str
    regions: list[int]
    second_name: Optional[str] = None
    birth_date: Optional[str] = None
    passport_series: Optional[str] = None
    passport_number: Optional[str] = None
    inn: Optional[str] = None

    def __post_init__(self):
        if len(self.regions) > 2:
            raise ValueError


class IrbisSearchTask(BaseSearchTask):
    def __init__(self, search_filters: IrbisSearchParameters):
        super().__init__(search_filters.query_id, search_filters.price)
        self.person = BaseAuthIRBIS(
            first_name=search_filters.first_name,
            last_name=search_filters.last_name,
            regions=search_filters.regions,
            second_name=search_filters.second_name,
            birth_date=search_filters.birth_date,
            passport_series=search_filters.passport_series,
            passport_number=search_filters.passport_number,
            inn=search_filters.inn
        )

        self.logger = SearchLogger(self.query_id, 'search_irbis.log')

    async def _process_search(self, db):
        person_uuid = await self.person.get_person_uuid()
        arbitr_preview_name, arbitr_preview_inn, arbitr_full = await self._arbitration_court_data(person_uuid)
        bankruptcy_preview, bankruptcy_full = await self._bankruptcy_data(person_uuid)
        corruption_preview, corruption_full = await self._corruption_data(person_uuid)
        court_gen_preview, court_gen_category, court_gen_full = await self._court_of_gen_jur_data(person_uuid)
        deposits_preview, deposits_full = await self._deposits_data(person_uuid)
        disqualified_full = await self._disqualified_pers_data(person_uuid)
        fssp_preview, fssp_full = await self._fssp_data(person_uuid)
        mlindex_full = await self._ml_index_data(person_uuid)
        part_in_org_preview, part_in_org_full = await self._part_in_org_data(person_uuid)
        tax_areas_full = await self._tax_areas_data(person_uuid)
        terror_list_full = await self._terror_list_data(person_uuid)

    async def _update_balances(self, db):
        pass

    async def _arbitration_court_data(self, person_uuid: str):
        data_preview_name, data_preview_inn = await ArbitrationCourt.get_data_preview(person_uuid)
        full_data = await ArbitrationCourt.get_full_data(person_uuid, 1, 50, 'all')

        arbitr_preview_name = ArbitrationCourtPreviewTable(type="name", plaintiff=data_preview_name["P"],
                                                           responder=data_preview_name["R"])
        arbitr_preview_inn = ArbitrationCourtPreviewTable(type="inn", plaintiff=data_preview_inn["P"],
                                                          responder=data_preview_inn["R"])
        arbitr_full = []
        for item in full_data:
            obj = ArbitrationCourtFullTable(
                court_name_val=item.get("court_name_val", None),
                role=item.get("role", None),
                case_date=item.get("case_date", None),
                case_id=item.get("case_id", None),
                inn=item.get("inn", None),
                name=item.get("name", None),
                case_type=item.get("case_type", None),
                response_id=item.get("id", None),
                address_val=item.get("address_val", None)
            )
            arbitr_full.append(obj)

        return arbitr_preview_name, arbitr_preview_inn, arbitr_full

    async def _bankruptcy_data(self, person_uuid: str):
        data_preview_name, data_preview_inn = await Bankruptcy.get_data_preview(person_uuid)
        full_data_fio = await Bankruptcy.get_full_data(person_uuid, 1, 50, 'name')
        full_data_inn = await Bankruptcy.get_full_data(person_uuid, 1, 50, 'inn')
        bankruptcy_preview = BankruptcyPreviewTable(name=data_preview_name, inn=data_preview_inn)
        bankruptcy_full = []
        for item in full_data_fio:
            obj = BankruptcyFullTable(
                first_name=item.get("first_name", None),
                second_name=item.get("second_name", None),
                last_name=item.get("last_name", None),
                birth_date=item.get("birth_date", None),
                born_place=item.get("born_place", None),
                inn=item.get("inn", None),
                ogrn=item.get("ogrn", None),
                snils=item.get("snils", None),
                old_name=item.get("old_name", None),
                category_name=item.get("category_name", None),
                location=item.get("location", None),
                region_name=item.get("region_name", None),
                information=item.get("information", None),
                link=item.get("link", None)
            )
            bankruptcy_full.append(obj)
        for item in full_data_inn:
            obj = BankruptcyFullTable(
                first_name=item.get("first_name", None),
                second_name=item.get("second_name", None),
                last_name=item.get("last_name", None),
                birth_date=item.get("birth_date", None),
                born_place=item.get("born_place", None),
                inn=item.get("inn", None),
                ogrn=item.get("ogrn", None),
                snils=item.get("snils", None),
                old_name=item.get("old_name", None),
                category_name=item.get("category_name", None),
                location=item.get("location", None),
                region_name=item.get("region_name", None),
                information=item.get("information", None),
                link=item.get("link", None)
            )
            bankruptcy_full.append(obj)

        return bankruptcy_preview, bankruptcy_full

    async def _corruption_data(self, person_uuid: str):
        data_preview = await Corruption.get_data_preview(person_uuid)
        full_data = await Corruption.get_full_data(person_uuid, 1, 50)
        corruption_preview = CorruptionPreviewTable(count=data_preview)
        corruption_full = []
        for item in full_data:
            obj = CorruptionFullTable(
                key=item.get("key", None),
                full_name=item.get("full_name", None),
                organization=item.get("organization", None),
                position=item.get("position", None),
                normative_act=item.get("normative_act", None),
                application_date=item.get("application_date", None),
                publish_date=item.get("publish_date", None),
                excluded_reason=item.get("excluded_reason", None)
            )
            corruption_full.append(obj)
        return corruption_preview, corruption_full

    async def _court_of_gen_jur_data(self, person_uuid: str):
        full_fio_data_preview, short_fio_data_preview = await CourtGeneralJurisdiction.get_data_preview(
            person_uuid, "", "all"
        )

        court_gen_preview = []
        for key, item in full_fio_data_preview.items():
            obj = CourtGeneralJurPreviewTable(
                search_type="full",
                court_type=key,
                plan=item.get("plan", None),
                deff=item.get("deff", None),
                declarant=item.get("declarant", None),
                face=item.get("face", None),
                lawyer=item.get("lawyer", None)
            )
            court_gen_preview.append(obj)
        for key, item in short_fio_data_preview.items():
            obj = CourtGeneralJurPreviewTable(
                search_type="short",
                court_type=key,
                plan=item.get("plan", None),
                deff=item.get("deff", None),
                declarant=item.get("declarant", None),
                face=item.get("face", None),
                lawyer=item.get("lawyer", None)
            )
            court_gen_preview.append(obj)

        category_data = await CourtGeneralJurisdiction.get_category_result(
            person_uuid, 'allData', '', 'all'
        )

        court_gen_category = []
        for item in category_data:
            obj = CourtGeneralJurCategoricalTable(
                type=item.get("type", None),
                count=item.get("count", None),
            )
            court_gen_category.append(obj)

        full_data = await CourtGeneralJurisdiction.get_full_data(
            person_uuid=person_uuid,
            page=1,
            rows=50,
            filter0='allData',
            filter_text='',
            strategy='all'
        )
        court_gen_full = []
        return court_gen_preview, court_gen_category, court_gen_full

    async def _deposits_data(self, person_uuid: str):
        data_preview = await Deposits.get_data_preview(person_uuid)
        full_data = await Deposits.get_full_data(person_uuid, 1, 50)

        deposits_preview = []
        for item in data_preview:
            obj = DepositsPreviewTable(
                pledge_count=item.get("pledge_count", None),
                pledge_type=item.get("pledge_type", None),
                response_id=item.get("id", None)
            )
            deposits_preview.append(obj)

        deposits_full = []
        return deposits_preview, deposits_full

    async def _disqualified_pers_data(self, person_uuid: str):
        data_preview = await DisqualifiedPersons.get_data_preview(person_uuid)
        full_data = await DisqualifiedPersons.get_full_data(person_uuid, 1, 50)

        disqualified_full = []
        for item in full_data:
            obj = DisqualifiedPersonFullTable(
                response_id=item.get("id", None),
                reestr_key=item.get("reestr_key", None),
                birth_date=item.get("birth_date", None),
                fio=item.get("fio", None),
                article=item.get("article", None),
                start_date_disq=item.get("start_date_disq", None),
                end_date_disq=item.get("end_date_disq", None),
                bornplace=item.get("bornplace", None),
                fio_judge=item.get("fio_judge", None),
                office_judge=item.get("office_judge", None),
                legal_name=item.get("legal_name", None),
                office=item.get("office", None),
                department=item.get("department", None)
            )
            disqualified_full.append(obj)
        return disqualified_full

    async def _fssp_data(self, person_uuid: str):
        data_preview = await FSSP.get_data_preview(person_uuid)
        data_full = await FSSP.get_full_data(person_uuid, 1, 50)

        fssp_preview = []
        for item in data_preview:
            obj = FSSPPreviewTable(
                response_id=item.get("id", None),
                type=item.get("type", None),
                type_sum=item.get("type_sum", None),
                type_count=item.get("type_count", None)
            )
            fssp_preview.append(obj)

        fssp_full = []
        for item in data_full:
            obj = FSSPFullTable(
                ip=item.get("ip", None),
                fio=item.get("fio", None),
                rosp=item.get("rosp", None),
                type_ip=item.get("type_ip", None),
                summ=item.get("summ", None),
                rekv=item.get("rekv", None),
                end_cause=item.get("end_cause", None),
                pristav=item.get("pristav", None),
                pristav_phones=item.get("pristav_phones", None),
                response_id=item.get("id", None)
            )
            fssp_full.append(obj)
        return fssp_preview, fssp_full

    async def _ml_index_data(self, person_uuid: str):
        full_data = await MLIndex.get_full_data(person_uuid)
        mlindex_full = MLIndexFullTable(
            scoring=full_data.get("scoring", 0),
            errors="\n".join(full_data.get("errors", [])),
            progress=full_data.get("progress", 0),
            popularity_full=full_data.get("popularity", dict()).get("full", 0),
            popularity_short=full_data.get("popularity", dict()).get("short", 0),
        )
        return mlindex_full

    async def _part_in_org_data(self, person_uuid: str):
        data_preview_all, data_preview_selected = await ParticipationOrganization.get_data_preview(person_uuid)
        full_data = await ParticipationOrganization.get_full_data(
            person_uuid,
            1,
            50,
            'all'
        )
        part_in_org_preview = []
        part_in_org_full = []
        for item in data_preview_all:
            obj = PartInOrgPreviewTable(
                filter_type="all",
                count=item.get("count", None),
                part_type=item.get("type", None)
            )
            part_in_org_preview.append(obj)
        for item in data_preview_selected:
            obj = PartInOrgPreviewTable(
                filter_type="selected",
                count=item.get("count", None),
                part_type=item.get("type", None)
            )
            part_in_org_preview.append(obj)
        return part_in_org_preview, part_in_org_full

    async def _tax_areas_data(self, person_uuid: str):
        full_data = await TaxArrears.get_full_data(person_uuid)

        tax_areas_full = []
        return tax_areas_full

    async def _terror_list_data(self, person_uuid: str):
        data_preview = await TerrorList.get_data_preview(person_uuid)
        full_data = await TerrorList.get_full_data(person_uuid, 1, 50)
        terror_list_full = []
        for item in full_data:
            obj = TerrorListFullTable(
                response_id=item.get("id", None),
                fio=item.get("fio", None),
                birth_date=item.get("birth_date", None),
                birth_place=item.get("birth_place", None)
            )
            terror_list_full.append(obj)
        return terror_list_full


@shared_task(bind=True, acks_late=True)
def start_search_by_irbis(self, search_filters: IrbisSearchParameters):
    loop = get_event_loop()
    task = IrbisSearchTask(search_filters)
    loop.run_until_complete(task.execute())
