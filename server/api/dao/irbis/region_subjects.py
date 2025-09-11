from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.dao.base import BaseDAO
from server.api.models.irbis_models import RegionSubject, PersonRegions


class RegionSubjectDAO(BaseDAO):
    model = RegionSubject

    @classmethod
    async def get_regions_map(
        cls,
        db: AsyncSession,
    ):
        """Получает все регионы в виде словаря {код: регион}."""
        try:
            result = await db.execute(select(RegionSubject))
            regions = result.scalars().all()
            regions_map = {region.subject_number: region for region in regions}
            return regions_map
        except Exception as e:
            logger.error(f"Ошибка при получении регионов: {e}")
            return {}

    @classmethod
    async def get_region_by_code(
        cls,
        region_code: int,
        db: AsyncSession,
    ):
        """Получает регион по коду субъекта."""
        try:
            result = await db.execute(
                select(RegionSubject)
                .where(RegionSubject.subject_number == region_code)
            )
            region = result.scalar_one_or_none()

            return region

        except Exception as e:
            logger.error(f"Ошибка при получении региона по коду {region_code}: {e}")

    @classmethod
    async def get_person_regions(cls, person_id: int, db: AsyncSession):
        """Получает регионы для конкретного человека."""
        try:
            result = await db.execute(
                select(RegionSubject)
                .join(PersonRegions)
                .where(PersonRegions.person_id == person_id)
            )
            regions = result.scalars().all()
            return regions
        except Exception as e:
            logger.error(f"Ошибка при получении регионов для person_id {person_id}: {e}")
            return []
