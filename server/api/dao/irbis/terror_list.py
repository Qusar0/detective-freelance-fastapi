from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.models.irbis_models import TerrorListFullTable
from server.api.dao.base import BaseDAO
from loguru import logger


class TerroristsDAO(BaseDAO):
    model = TerrorListFullTable

    @staticmethod
    async def get_paginated_data(
        irbis_person_id: int,
        page: int,
        size: int,
        db: AsyncSession
    ) -> List[TerrorListFullTable]:
        """Возвращает список террористов с пагинацией"""
        try:
            logger.debug(
                f"DAO: Получение terrorist list для irbis_person_id={irbis_person_id} page={page} size={size}",
            )
            offset = max((page - 1) * size, 0)

            query = (
                select(TerrorListFullTable)
                .where(TerrorListFullTable.irbis_person_id == irbis_person_id)
                .offset(offset)
                .limit(size)
            )

            result = await db.execute(query)
            results: List[TerrorListFullTable] = result.scalars().all()

            logger.debug(f"DAO: Найдено {len(results)} записей terrorists")
            return results

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении списка terrorist: {e}", exc_info=True)
            raise
