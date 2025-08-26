import logging
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.dao.base import BaseDAO
from server.api.dao.irbis.region_subjects import RegionSubjectDAO
from server.api.models.irbis_models import PersonRegions


class PersonRegionsDAO(BaseDAO):
    model = PersonRegions

    @classmethod
    async def add_regions(
        cls,
        irbis_person_id: int,
        regions: List[int],
        db: AsyncSession,
    ):
        """Получает тип поиска по имени."""
        try:
            for region_code in regions:
                region = await RegionSubjectDAO.get_region_by_code(region_code, db)
                if region:
                    person_region = PersonRegions(
                        person_id=irbis_person_id,
                        region_id=region.id,
                    )
                    db.add(person_region)
            return True
        except Exception as e:
            logging.error(f"Ошибка при добавлении региона искомого человека: {e}")
            return False
