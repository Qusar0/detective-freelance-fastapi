from typing import Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from server.api.models.irbis_models import (
    PledgeFullTable,
    ArbitrationCourtFullTable,
    BankruptcyFullTable,
    DisqualifiedPersonFullTable,
    CorruptionFullTable,
    CourtGeneralJurFullTable,
    TerrorListFullTable,
    TaxArrearsFullTable,
    FSSPFullTable,
    PartInOrgFullTable,
)
from server.api.dao.base import BaseDAO
from server.api.dao.queries_data import QueriesDataDAO
from loguru import logger


class StatisticsDAO(BaseDAO):

    TABLE_MAPPING = {
        "arbitration_court_full": ArbitrationCourtFullTable,
        "bankruptcy_full": BankruptcyFullTable,
        "corruption_full": CorruptionFullTable,
        "court_general_full": CourtGeneralJurFullTable,
        "disqualified_person_full": DisqualifiedPersonFullTable,
        "pledgess_full": PledgeFullTable,
        "terrorists": TerrorListFullTable,
        "tax_arrears": TaxArrearsFullTable,
        "fssp": FSSPFullTable,
        "part_in_org": PartInOrgFullTable
    }

    @staticmethod
    async def get_all_counts(
        person_id: int,
        db: AsyncSession
    ) -> Dict[str, int]:
        """Получить количество записей по всем таблицам за один вызов."""
        try:

            results = {}

            for table_name, table in StatisticsDAO.TABLE_MAPPING.items():
                results[table_name] = await StatisticsDAO._get_count_for_table(
                    table, person_id, db
                )
            
            resource_stats = await QueriesDataDAO.get_count_resource(
                query_id=person_id,
                db=db
            )
            results.update(resource_stats)
            logger.info(f"DAO: Получена статистика по irbis_person_id={person_id}")
            return results

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении статистики: {e}")
            return {table_name: 0 for table_name in StatisticsDAO.TABLE_MAPPING.keys()}

    @staticmethod
    async def _get_count_for_table(
        table: Any,
        person_id: int,
        db: AsyncSession,
        id_field: str = "irbis_person_id"
    ) -> int:
        """Вспомогательный метод для подсчета записей в таблице."""
        try:
            filter_field = getattr(table, id_field, None)
            if filter_field is None:
                logger.warning(f"Поле {id_field} не найдено в таблице {table.__name__}")
                return 0

            query = select(func.count()).where(filter_field == person_id)
            result = await db.execute(query)
            count = result.scalar() or 0

            return count

        except Exception as e:
            logger.error(f"Ошибка при подсчете записей в {table.__name__}: {e}")
            return 0
