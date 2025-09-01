from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.models.irbis_models import (
    ArbitrationCourtFullTable,
    ProcessType,
    PersonRegions,
    IrbisPerson,
)
from server.api.dao.base import BaseDAO
from loguru import logger


class ArbitrationCourtDAO(BaseDAO):
    model = ArbitrationCourtFullTable

    # @staticmethod
    # async def get_paginated_data(
    #     irbis_person_id: int,
    #     page: int,
    #     size: int,
    #     search_type: Optional[str],
    #     role: Optional[str],
    #     db: AsyncSession
    # ):
    #     """Получение пагинированных данных о судебных делах с фильтрацией."""
    #     try:
    #         logger.debug(
    #             f"DAO: Получение данных для irbis_person_id: {irbis_person_id}, "
    #             f"page: {page}, size: {size}, search_type {search_type}, "
    #             f"role: {role}"
    #         )

    #         query = select(ArbitrationCourtFullTable).where(
    #             ArbitrationCourtFullTable.irbis_person_id == irbis_person_id
    #         ).options(
    #             selectinload(ArbitrationCourtFullTable.region),
    #             selectinload(ArbitrationCourtFullTable.process_type),
    #         )

    #         if not all_regions:
    #             selected_regions_query = select(PersonRegions.region_id).where(
    #                 PersonRegions.person_id == irbis_person_id
    #             )
    #             selected_regions_result = await db.execute(selected_regions_query)
    #             selected_region_ids = selected_regions_result.scalars().all()

    #             if selected_region_ids:
    #                 logger.debug(f"Фильтрация по выбранным регионам: {selected_region_ids}")
    #                 query = query.where(CourtGeneralJurFullTable.region_id.in_(selected_region_ids))
    #             else:
    #                 logger.debug("Нет выбранных регионов, возвращаем пустой результат")
    #                 return []

    #         if case_categories:
    #             logger.debug(f"Фильтрация по категориям: {case_categories}")
    #             query = query.join(ProcessType).where(ProcessType.code.in_(case_categories))

    #         offset = (page - 1) * size
    #         query = query.offset(offset).limit(size)

    #         result = await db.execute(query)
    #         results = result.scalars().all()

    #         logger.debug(f"DAO: Найдено {len(results)} записей")
    #         return results

    #     except Exception as e:
    #         logger.error(f"DAO: Ошибка при получении данных судебных дел: {e}", exc_info=True)
    #         raise

    # @staticmethod
    # async def get_full_case_by_id(
    #     case_id: int,
    #     db: AsyncSession
    # ) -> Optional[CourtGeneralJurFullTable]:
    #     """Получение полной информации о деле по ID с связанными данными."""
    #     try:
    #         logger.debug(f"DAO: Получение полной информации по делу ID: {case_id}")

    #         query = select(CourtGeneralJurFullTable).where(
    #             CourtGeneralJurFullTable.id == case_id,
    #         ).options(
    #             selectinload(CourtGeneralJurFullTable.region),
    #             selectinload(CourtGeneralJurFullTable.process_type),
    #             selectinload(CourtGeneralJurFullTable.match_type),
    #             selectinload(CourtGeneralJurFullTable.faces),
    #             selectinload(CourtGeneralJurFullTable.progress),
    #             selectinload(CourtGeneralJurFullTable.irbis_person).selectinload(IrbisPerson.query),
    #         )

    #         result = await db.execute(query)
    #         case = result.scalar_one_or_none()

    #         return case

    #     except Exception as e:
    #         logger.error(f"DAO: Ошибка при получении полной информации по делу {case_id}: {e}", exc_info=True)
    #         raise
