from typing import Optional, Tuple, List
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.models.irbis_models import (
    BankruptcyFullTable,
    IrbisPerson,
)
from server.api.dao.base import BaseDAO
from loguru import logger


class BankruptcyDAO(BaseDAO):
    model = BankruptcyFullTable

    @staticmethod
    async def get_paginated_data(
        irbis_person_id: int,
        page: int,
        size: int,
        search_type: str,
        db: AsyncSession
    ) -> Tuple[List[BankruptcyFullTable], int]:
        """Фильтрация и пагинация судебных дел по полю search_type с подсчетом общего количества."""
        try:
            logger.debug(f"DAO: Фильтрация по полю search_type: {search_type}")

            query = select(BankruptcyFullTable).where(
                BankruptcyFullTable.irbis_person_id == irbis_person_id
            )

            count_query = select(func.count(BankruptcyFullTable.id)).where(
                BankruptcyFullTable.irbis_person_id == irbis_person_id
            )

            if search_type:
                query = query.where(BankruptcyFullTable.search_type == search_type)
                count_query = count_query.where(BankruptcyFullTable.search_type == search_type)

            offset = (page - 1) * size
            query = query.offset(offset).limit(size)

            result = await db.execute(query)
            results = result.scalars().all()

            count_result = await db.execute(count_query)
            total_count = count_result.scalar_one()

            logger.debug(f"DAO:Найдено {len(results)} записей из {total_count} всего для search_type = '{search_type}'")
            return results, total_count

        except Exception as e:
            logger.error(f"DAO: Ошибка при фильтрации: {e}")
            raise

    @staticmethod
    async def get_full_case_by_id(
        case_id: int,
        db: AsyncSession
    ) -> Optional[BankruptcyFullTable]:
        """Получение полной информации о деле по ID с связанными данными."""
        try:
            logger.debug(f"DAO: Получение полной информации по делу ID: {case_id}")
            query = select(BankruptcyFullTable).options(
                selectinload(BankruptcyFullTable.irbis_person).selectinload(IrbisPerson.query)
            ).where(
                BankruptcyFullTable.id == case_id
            )

            result = await db.execute(query)
            case = result.scalar_one_or_none()
            return case

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении полной информации по делу {case_id}: {e}")
            raise
