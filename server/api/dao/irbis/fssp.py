from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.models.irbis_models import FSSPFullTable
from server.api.dao.base import BaseDAO
from loguru import logger


class FSSPDAO(BaseDAO):
    model = FSSPFullTable

    @staticmethod
    async def get_paginated_data(
        irbis_person_id: int,
        page: int,
        size: int,
        db: AsyncSession
    ) -> List[FSSPFullTable]:
        """Возвращает список ORM-объектов FSSPFullTable (без преобразования)."""
        try:
            logger.debug(
                f"DAO: Получение fssp list для irbis_person_id={irbis_person_id} page={page} size={size}",
            )
            offset = (page - 1) * size

            query = (
                select(FSSPFullTable)
                .where(FSSPFullTable.irbis_person_id == irbis_person_id)
                .offset(offset)
                .limit(size)
            )

            result = await db.execute(query)
            results: List[FSSPFullTable] = result.scalars().all()

            logger.debug(f"DAO: Найдено {len(results)} записей fssp")
            return results

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении списка fssp: {e}", exc_info=True)
            raise

    @staticmethod
    async def get_full_case_by_id(
        case_id: int,
        db: AsyncSession
    ) -> Optional[FSSPFullTable]:
        """Возвращает ORM-объект FSSPFullTable с подгрузкой связанного IrbisPerson."""
        try:
            logger.debug(f"DAO: Получение полной записи fssp id={case_id}")
            query = (
                select(FSSPFullTable)
                .options(selectinload(FSSPFullTable.irbis_person))
                .where(FSSPFullTable.id == case_id)
            )

            result = await db.execute(query)
            case: Optional[FSSPFullTable] = result.scalar_one_or_none()

            if not case:
                logger.warning(f"DAO: FSSP case id={case_id} не найден")
            return case

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении fssp case id={case_id}: {e}", exc_info=True)
            raise
