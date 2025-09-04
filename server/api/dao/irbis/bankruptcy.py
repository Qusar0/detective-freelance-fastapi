from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload, defer
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
    ):
        """Фильтрация и пагинация судебных дел по полю search_type."""
        try:
            logger.debug(f"DAO: Фильтрация по полю search_type: {search_type}")

            query = select(BankruptcyFullTable).where(
                BankruptcyFullTable.irbis_person_id == irbis_person_id
            )

            if search_type == "name":
                query = query.where(
                    (BankruptcyFullTable.first_name != None) &
                    (BankruptcyFullTable.first_name != '') |
                    (BankruptcyFullTable.second_name != None) &
                    (BankruptcyFullTable.second_name != '') |
                    (BankruptcyFullTable.last_name != None) &
                    (BankruptcyFullTable.last_name != '')
                )
            elif search_type == "inn":
                query = query.where(
                    (BankruptcyFullTable.inn != None) &
                    (BankruptcyFullTable.inn != '')
                )
            elif search_type == "all":
                pass  # Без фильтра - все записи
            else:
                logger.warning(f"Неизвестный search_type: {search_type}")
                return []

            # Пагинация
            offset = (page - 1) * size
            query = query.offset(offset).limit(size)

            result = await db.execute(query)
            results = result.scalars().all()

            logger.debug(f"DAO: Найдено {len(results)} записей для search_type = '{search_type}'")
            return results

        except Exception as e:
            logger.error(f"DAO: Ошибка при фильтрации: {e}", exc_info=True)
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
            logger.error(f"DAO: Ошибка при получении полной информации по делу {case_id}: {e}", exc_info=True)
            raise