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
)
from server.api.dao.base import BaseDAO
from loguru import logger


class StatisticsDAO(BaseDAO):

    # Определяем все таблицы для статистики
    TABLE_MAPPING = {
        "arbitration_court": ArbitrationCourtFullTable,
        "bankruptcy": BankruptcyFullTable,
        "corruption": CorruptionFullTable,
        "court_general": CourtGeneralJurFullTable,
        "disqualified_person": DisqualifiedPersonFullTable,
        "pledgess": PledgeFullTable,
    }

    @staticmethod
    async def get_all_counts(
        query_id: int,
        db: AsyncSession
    ) -> Dict[str, int]:
        """Получить количество записей по всем таблицам за один вызов."""
        try:

            tasks = []
            for table_name, table in StatisticsDAO.TABLE_MAPPING.items():
                task = StatisticsDAO._get_count_for_table(table, query_id, db)
                tasks.append((table_name, task))

            results = {}
            for table_name, task in tasks:
                results[table_name] = await task

            logger.info(f"DAO: Получены данные для ID {query_id}")
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
