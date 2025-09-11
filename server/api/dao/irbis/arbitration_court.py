from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.models.irbis_models import (
    ArbitrationCourtFullTable,
    IrbisPerson,
    PersonRoleType,
)
from server.api.dao.base import BaseDAO
from loguru import logger


class ArbitrationCourtDAO(BaseDAO):
    model = ArbitrationCourtFullTable

    @staticmethod
    async def get_paginated_data(
        irbis_person_id: int,
        page: int,
        size: int,
        search_type: Optional[str],
        role: Optional[str],
        db: AsyncSession
    ):
        """Получение пагинированных данных о судебных делах с фильтрацией."""
        try:
            logger.debug(
                f"DAO: Получение данных для irbis_person_id: {irbis_person_id}, "
                f"page: {page}, size: {size}, search_type {search_type}, "
                f"role: {role}"
            )

            query = select(ArbitrationCourtFullTable).where(
                ArbitrationCourtFullTable.irbis_person_id == irbis_person_id
            ).options(
                selectinload(ArbitrationCourtFullTable.region),
                selectinload(ArbitrationCourtFullTable.case_type),
                selectinload(ArbitrationCourtFullTable.role),
            )

            if search_type:
                logger.debug(f"Фильтрация по типу поиска: {search_type}")
                query = query.where(ArbitrationCourtFullTable.search_type == search_type)

            if role:
                logger.debug(f"Фильтрация по роли лица: {role}")
                query = query.join(PersonRoleType).where(PersonRoleType.short_name == role)

            offset = (page - 1) * size
            query = query.offset(offset).limit(size)

            result = await db.execute(query)
            results = result.scalars().all()

            logger.debug(f"DAO: Найдено {len(results)} записей")
            return results

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении данных арбитражных дел дел: {e}")
            raise

    @staticmethod
    async def get_full_case_by_id(
        case_id: int,
        db: AsyncSession
    ):
        """Получение полной информации о деле по ID с связанными данными."""
        try:
            logger.debug(f"DAO: Получение полной информации по делу ID: {case_id}")

            query = select(ArbitrationCourtFullTable).where(
                ArbitrationCourtFullTable.id == case_id,
            ).options(
                selectinload(ArbitrationCourtFullTable.region),
                selectinload(ArbitrationCourtFullTable.oponents),
                selectinload(ArbitrationCourtFullTable.case_type),
                selectinload(ArbitrationCourtFullTable.role),
                selectinload(ArbitrationCourtFullTable.irbis_person).selectinload(IrbisPerson.query),
            )

            result = await db.execute(query)
            case = result.scalar_one_or_none()

            return case

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении полной информации по делу {case_id}: {e}")
            raise
