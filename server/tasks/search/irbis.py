from dataclasses import dataclass
from typing import Optional

from celery import shared_task

from server.api.IRBIS_parser.arbitration_court import ArbitrationCourt
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
        pass

    async def _update_balances(self, db):
        pass

    async def _arbitration_court_data(self, person_uuid: str):
        data_preview_name, data_preview_inn = await ArbitrationCourt.get_data_preview(person_uuid)

    async def _bankruptcy_data(self):
        pass

    async def _corruption_data(self):
        pass

    async def _court_of_gen_jur_data(self):
        pass

    async def _deposits_data(self):
        pass

    async def _disqualified_pers_data(self):
        pass

    async def _fssp_data(self):
        pass

    async def _ml_index_data(self):
        pass

    async def _part_in_org_data(self):
        pass

    async def _pass_check_data(self, person_uuid: str):
        pass

    async def _tax_areas_data(self):
        pass

    async def _terror_list_data(self):
        pass


@shared_task(bind=True, acks_late=True)
def start_search_by_irbis(self, search_filters: IrbisSearchParameters):
    loop = get_event_loop()
    task = IrbisSearchTask(search_filters)
    loop.run_until_complete(task.execute())