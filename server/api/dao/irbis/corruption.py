from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.models.irbis_models import CorruptionFullTable
from server.api.dao.base import BaseDAO
from loguru import logger


class CorruptionDAO(BaseDAO):
    model = CorruptionFullTable

    @staticmethod
    async def get_paginated_data(
        irbis_person_id: int,
        page: int,
        size: int,
        db: AsyncSession
    ) -> List[CorruptionFullTable]:
        """Возвращает список ORM-объектов CorruptionFullTable (без преобразования)."""
        try:
            logger.debug(
                f"DAO: Получение corruption list для irbis_person_id={irbis_person_id} page={page} size={size}",
            )
            offset = (page - 1) * size

            query = (
                select(CorruptionFullTable)
                .where(CorruptionFullTable.irbis_person_id == irbis_person_id)
                .offset(offset)
                .limit(size)
            )

            result = await db.execute(query)
            results: List[CorruptionFullTable] = result.scalars().all()

            logger.debug(f"DAO: Найдено {len(results)} записей corruption")
            return results

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении списка corruption: {e}", exc_info=True)
            raise

    @staticmethod
    async def get_full_case_by_id(
        case_id: int,
        db: AsyncSession
    ) -> Optional[CorruptionFullTable]:
        """Возвращает ORM-объект CorruptionFullTable с подгрузкой связанного IrbisPerson."""
        try:
            logger.debug(f"DAO: Получение полной записи corruption id={case_id}")
            query = (
                select(CorruptionFullTable)
                .options(selectinload(CorruptionFullTable.irbis_person))
                .where(CorruptionFullTable.id == case_id)
            )

            result = await db.execute(query)
            case: Optional[CorruptionFullTable] = result.scalar_one_or_none()

            if not case:
                logger.warning(f"DAO: Corruption case id={case_id} не найден")
            return case

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении corruption case id={case_id}: {e}", exc_info=True)
            raise
