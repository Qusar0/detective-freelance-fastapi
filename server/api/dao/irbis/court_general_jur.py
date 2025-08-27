from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.models.irbis_models import (
    CourtGeneralJurFullTable,
    ProcessType,
    PersonRegions,
)
from server.api.dao.base import BaseDAO
from loguru import logger


class CourtGeneralJurDAO(BaseDAO):
    model = CourtGeneralJurFullTable

    @staticmethod
    async def get_paginated_court_general_data(
        irbis_person_id: int,
        page: int,
        size: int,
        all_regions: bool,
        case_categories: Optional[List[str]],
        db: AsyncSession
    ):
        """Получение пагинированных данных о судебных делах с фильтрацией."""
        try:
            logger.debug(
                f"DAO: Получение данных для irbis_person_id: {irbis_person_id}, "
                f"page: {page}, size: {size}, all_regions: {all_regions}, "
                f"categories: {case_categories}"
            )

            query = select(CourtGeneralJurFullTable).where(
                CourtGeneralJurFullTable.irbis_person_id == irbis_person_id
            ).options(
                selectinload(CourtGeneralJurFullTable.region),
                selectinload(CourtGeneralJurFullTable.process_type),
            )

            if not all_regions:
                selected_regions_query = select(PersonRegions.region_id).where(
                    PersonRegions.person_id == irbis_person_id
                )
                selected_regions_result = await db.execute(selected_regions_query)
                selected_region_ids = selected_regions_result.scalars().all()

                if selected_region_ids:
                    logger.debug(f"Фильтрация по выбранным регионам: {selected_region_ids}")
                    query = query.where(CourtGeneralJurFullTable.region_id.in_(selected_region_ids))
                else:
                    logger.debug("Нет выбранных регионов, возвращаем пустой результат")
                    return []

            if case_categories:
                logger.debug(f"Фильтрация по категориям: {case_categories}")
                query = query.join(ProcessType).where(ProcessType.code.in_(case_categories))

            offset = (page - 1) * size
            query = query.offset(offset).limit(size)

            result = await db.execute(query)
            results = result.scalars().all()

            logger.debug(f"DAO: Найдено {len(results)} записей")
            return results

        except Exception as e:
            logger.error(f"DAO: Ошибка при получении данных судебных дел: {e}", exc_info=True)
            raise
