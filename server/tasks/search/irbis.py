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
        await self._arbitration_court_data(person_uuid, db)
        await self._bankruptcy_data(person_uuid, db)
        await self._corruption_data(person_uuid, db)
        await self._court_of_gen_jur_data(person_uuid, db)
        await self._deposits_data(person_uuid, db)
        await self._disqualified_pers_data(person_uuid, db)
        await self._fssp_data(person_uuid, db)
        await self._ml_index_data(person_uuid, db)
        await self._part_in_org_data(person_uuid, db)
        await self._tax_areas_data(person_uuid, db)
        await self._terror_list_data(person_uuid, db)

    async def _update_balances(self, db):
        pass

    async def _arbitration_court_data(self, person_uuid: str, db):
        data_preview_name, data_preview_inn = await ArbitrationCourt.get_data_preview(person_uuid)
        full_data = await ArbitrationCourt.get_full_data(person_uuid, 1, 50, 'all')

    async def _bankruptcy_data(self, person_uuid: str, db):
        data_preview_name, data_preview_inn = await Bankruptcy.get_data_preview(person_uuid)
        full_data_fio = await Bankruptcy.get_full_data(person_uuid, 1, 50, 'name')
        full_data_inn = await Bankruptcy.get_full_data(person_uuid, 1, 50, 'inn')

    async def _corruption_data(self, person_uuid: str, db):
        data_preview = await Corruption.get_data_preview(person_uuid)
        full_data = await Corruption.get_full_data(person_uuid, 1, 50)

    async def _court_of_gen_jur_data(self, person_uuid: str, db):
        full_fio_data_preview, short_fio_data_preview = await CourtGeneralJurisdiction.get_data_preview(
            person_uuid, "", "all"
        )

        category_data = await CourtGeneralJurisdiction.get_category_result(
            person_uuid, 'allData', '', 'all'
        )

        full_data = await CourtGeneralJurisdiction.get_full_data(
            person_uuid=person_uuid,
            page=1,
            rows=50,
            filter0='allData',
            filter_text='',
            strategy='all'
        )

    async def _deposits_data(self, person_uuid: str, db):
        data_preview = await Deposits.get_data_preview(person_uuid)
        full_data = await Deposits.get_full_data(person_uuid, 1, 50)

    async def _disqualified_pers_data(self, person_uuid: str, db):
        data_preview = await DisqualifiedPersons.get_data_preview(person_uuid)
        full_data = await DisqualifiedPersons.get_full_data(person_uuid, 1, 50)

    async def _fssp_data(self, person_uuid: str, db):
        data_preview = await FSSP.get_data_preview(person_uuid)
        data_full = await FSSP.get_full_data(person_uuid, 1, 50)

    async def _ml_index_data(self, person_uuid: str, db):
        full_data = await MLIndex.get_full_data(person_uuid)

    async def _part_in_org_data(self, person_uuid: str, db):
        data_preview = await ParticipationOrganization.get_data_preview(person_uuid)
        full_data = await ParticipationOrganization.get_full_data(
            person_uuid,
            1,
            50,
            'all'
        )

    async def _tax_areas_data(self, person_uuid: str, db):
        full_data = await TaxArrears.get_full_data(person_uuid)

    async def _terror_list_data(self, person_uuid: str, db):
        data_preview = await TerrorList.get_data_preview(person_uuid)
        full_data = await TerrorList.get_full_data(person_uuid, 1, 50)


@shared_task(bind=True, acks_late=True)
def start_search_by_irbis(self, search_filters: IrbisSearchParameters):
    loop = get_event_loop()
    task = IrbisSearchTask(search_filters)
    loop.run_until_complete(task.execute())