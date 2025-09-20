from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.models.irbis_models import TaxArrearsFullTable
from server.api.dao.base import BaseDAO
from loguru import logger


class TaxArrearsDAO(BaseDAO):
    model = TaxArrearsFullTable

    @staticmethod
    async def get_paginated_data(
        irbis_person_id: int,
        page: int,
        size: int,
        db: AsyncSession
    ) -> List[TaxArrearsFullTable]:
        """Получение списка налоговых задолженностей с пагинацией"""
        try:
            logger.debug(
                f"DAO: Получение задолженностей для irbis_person_id={irbis_person_id} page={page} size={size}",
            )
            offset = max((page - 1) * size,0)

            query = (
                select(TaxArrearsFullTable)
                .where(TaxArrearsFullTable.irbis_person_id == irbis_person_id)
                .options(selectinload(TaxArrearsFullTable.fields))
                .offset(offset)
                .limit(size)
            )

            result = await db.execute(query)
            results: List[TaxArrearsFullTable] = result.scalars().all()

            logger.debug(f"DAO: Найдено {len(results)} записей налоговых задолженностей")
            return results

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении списка налоговых задолженностей: {e}", exc_info=True)
            raise