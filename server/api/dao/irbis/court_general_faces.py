from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from server.api.models.irbis_models import CourtGeneralFacesTable
from server.api.dao.base import BaseDAO
from loguru import logger


class CourtGeneralFacesDAO(BaseDAO):
    model = CourtGeneralFacesTable

    @classmethod
    async def get_faces_by_case_id(
        cls,
        case_id: int,
        db: AsyncSession,
    ):
        """Получает данные о лицах по ID дела."""
        try:
            result = await db.execute(
                select(CourtGeneralFacesTable)
                .filter_by(case_id=case_id)
            )

            faces = result.scalars().all()

            if not faces:
                return None

            return faces

        except Exception as e:
            logger.error(f"Ошибка при получении лиц для дела {case_id}: {e}", exc_info=True)
            return None
