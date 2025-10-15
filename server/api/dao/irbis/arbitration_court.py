from typing import Optional, Tuple
from sqlalchemy import select, func
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
    ) -> Tuple[list, int]:
        """Получение пагинированных данных о судебных делах с фильтрацией и общим количеством."""
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

            count_query = select(func.count(ArbitrationCourtFullTable.id)).where(
                ArbitrationCourtFullTable.irbis_person_id == irbis_person_id
            )

            if search_type:
                logger.debug(f"Фильтрация по типу поиска: {search_type}")
                query = query.where(ArbitrationCourtFullTable.search_type == search_type)
                count_query = count_query.where(ArbitrationCourtFullTable.search_type == search_type)

            if role:
                logger.debug(f"Фильтрация по роли лица: {role}")
                query = query.join(PersonRoleType).where(
                    (PersonRoleType.russian_name == role.capitalize())
                )
                count_query = count_query.join(PersonRoleType).where(
                    (PersonRoleType.russian_name == role.capitalize())
                )

            offset = (page - 1) * size
            query = query.offset(offset).limit(size)

            result = await db.execute(query)
            results = result.scalars().all()

            count_result = await db.execute(count_query)
            total_count = count_result.scalar_one()

            logger.debug(f"DAO: Найдено {len(results)} записей из {total_count} всего")
            return results, total_count

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении данных арбитражных дел: {e}")
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
