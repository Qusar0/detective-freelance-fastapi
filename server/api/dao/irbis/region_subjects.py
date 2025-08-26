import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.dao.base import BaseDAO
from server.api.models.irbis_models import RegionSubject


class RegionSubjectDAO(BaseDAO):
    model = RegionSubject

    @classmethod
    async def get_region_by_code(
        cls,
        region_code: int,
        db: AsyncSession,
    ):
        """Получает тип поиска по имени."""
        try:
            result = await db.execute(
                select(RegionSubject)
                .where(RegionSubject.subject_number == region_code)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logging.error(f"Ошибка при получении региона по коду: {e}")
