from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.models.irbis_models import (
    PledgeFullTable,
    IrbisPerson
)
from server.api.dao.base import BaseDAO
from loguru import logger


class PledgessDAO(BaseDAO):
    model = PledgeFullTable

    @staticmethod
    async def get_paginated_data(
        irbis_person_id: int,
        page: int,
        size: int,
        db: AsyncSession
    ):
        """Фильтрация и пагинация с подгрузкой связанных данных."""
        try:

            query = select(PledgeFullTable).where(
                PledgeFullTable.irbis_person_id == irbis_person_id
            )
            
            query = query.options(
                selectinload(PledgeFullTable.parties),
                selectinload(PledgeFullTable.pledges)
            )
            
            offset = (page - 1) * size
            query = query.offset(offset).limit(size)

            result = await db.execute(query)
            results = result.scalars().all()
            
            logger.debug(f"DAO: Найдено {len(results)} записей")
            return results
        except Exception as e:
            logger.error(f"DAO: Ошибка при получении данных: {e}")
            raise

    @staticmethod
    async def get_full_case_by_id(
        case_id: int,
        db: AsyncSession
    ) -> Optional[PledgeFullTable]:
        """Получение полной информации о деле по ID с связанными данными."""
        try:
            logger.debug(f"DAO: Получение полной информации по делу ID: {case_id}")
            query = select(PledgeFullTable).options(
                selectinload(PledgeFullTable.irbis_person).selectinload(IrbisPerson.query)
            ).where(
                PledgeFullTable.id == case_id
            )
            query = query.options(
                selectinload(PledgeFullTable.parties),
                selectinload(PledgeFullTable.pledges)
            )
            result = await db.execute(query)
            case = result.scalar_one_or_none()
            return case

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении полной информации по делу {case_id}: {e}")
            raise
